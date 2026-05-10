import asyncio
from datetime import datetime, timezone

import httpx

from .bookmarks import load_bookmarks
from .db import connect, init
from .extract import extract

CONCURRENCY = 10
USER_AGENT = "Mozilla/5.0 (compatible; bookmarks-indexer/0.1)"

# Statuses that are usually transient and worth retrying.
TRANSIENT_STATUSES = {
    "http_202", "http_429",
    "http_500", "http_502", "http_503", "http_504",
    "http_520", "http_521", "http_522", "http_523", "http_524",
    "http_525", "http_526", "http_530",
    "error:ConnectError", "error:ConnectTimeout",
    "error:ReadTimeout", "error:RemoteProtocolError",
}

# Slow-mode tuning — used with --slow to be polite to rate-limiters.
SLOW_CONCURRENCY = 3
SLOW_MIN_GAP_SECONDS = 0.5


async def index_all(
    force: bool = False,
    retry_failed: bool = False,
    retry_only: str | None = None,
    slow: bool = False,
    limit: int | None = None,
) -> None:
    init()
    conn = connect()
    bookmarks = load_bookmarks()

    existing: set[str] = set()
    if not force:
        # Decide which already-attempted rows to skip.
        if retry_only == "transient":
            placeholders = ",".join("?" for _ in TRANSIENT_STATUSES)
            rows = conn.execute(
                f"SELECT chrome_id FROM bookmarks "
                f"WHERE fetch_status IS NOT NULL "
                f"  AND fetch_status NOT IN ({placeholders})",
                tuple(TRANSIENT_STATUSES),
            ).fetchall()
        elif retry_failed:
            rows = conn.execute(
                "SELECT chrome_id FROM bookmarks WHERE fetch_status = 'ok'"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT chrome_id FROM bookmarks WHERE fetch_status IS NOT NULL"
            ).fetchall()
        existing = {r["chrome_id"] for r in rows}

    todo = [b for b in bookmarks if b["chrome_id"] not in existing]
    if limit is not None:
        todo = todo[:limit]

    concurrency = SLOW_CONCURRENCY if slow else CONCURRENCY
    min_gap = SLOW_MIN_GAP_SECONDS if slow else 0.0
    mode = "slow" if slow else "normal"
    print(
        f"Indexing {len(todo)} of {len(bookmarks)} bookmarks "
        f"({len(existing)} already done) — mode: {mode}, "
        f"concurrency: {concurrency}"
    )

    sem = asyncio.Semaphore(concurrency)
    write_lock = asyncio.Lock()
    pace_lock = asyncio.Lock()
    next_start = 0.0
    done = 0

    async def acquire_start_slot() -> None:
        nonlocal next_start
        if min_gap <= 0:
            return
        async with pace_lock:
            now = asyncio.get_event_loop().time()
            if now < next_start:
                await asyncio.sleep(next_start - now)
            next_start = max(now, next_start) + min_gap

    async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}) as client:

        async def process(b: dict) -> None:
            nonlocal done
            async with sem:
                await acquire_start_slot()
                title, content, status = await extract(client, b["url"])
                async with write_lock:
                    conn.execute(
                        """INSERT INTO bookmarks
                               (chrome_id, name, url, folder, date_added,
                                title, content, indexed_at, fetch_status)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT(chrome_id) DO UPDATE SET
                               name=excluded.name,
                               url=excluded.url,
                               folder=excluded.folder,
                               title=excluded.title,
                               content=excluded.content,
                               indexed_at=excluded.indexed_at,
                               fetch_status=excluded.fetch_status""",
                        (
                            b["chrome_id"], b["name"], b["url"], b["folder"],
                            b["date_added"], title, content,
                            datetime.now(timezone.utc).isoformat(), status,
                        ),
                    )
                    conn.commit()
                    done += 1
                    print(f"  [{done}/{len(todo)}] [{status}] {(b['name'] or b['url'])[:70]}")

        await asyncio.gather(*(process(b) for b in todo))

    conn.close()
    print("Done.")


def run() -> None:
    import sys
    args = sys.argv[1:]
    force = "--force" in args
    retry_failed = "--retry-failed" in args
    slow = "--slow" in args
    limit: int | None = None
    retry_only: str | None = None
    for i, a in enumerate(args):
        if a == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
        elif a == "--retry-only" and i + 1 < len(args):
            retry_only = args[i + 1]
        elif a.startswith("--retry-only="):
            retry_only = a.split("=", 1)[1]
    asyncio.run(
        index_all(
            force=force,
            retry_failed=retry_failed,
            retry_only=retry_only,
            slow=slow,
            limit=limit,
        )
    )


if __name__ == "__main__":
    run()
