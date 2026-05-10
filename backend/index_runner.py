import asyncio
from datetime import datetime, timezone

import httpx

from .bookmarks import load_bookmarks
from .db import connect, init
from .extract import extract

CONCURRENCY = 10
USER_AGENT = "Mozilla/5.0 (compatible; bookmarks-indexer/0.1)"


async def index_all(
    force: bool = False,
    retry_failed: bool = False,
    limit: int | None = None,
) -> None:
    init()
    conn = connect()
    bookmarks = load_bookmarks()

    existing: set[str] = set()
    if not force:
        # Skip anything we've already attempted. With --retry-failed, only
        # skip the successful ones so failures get re-tried.
        where = "fetch_status = 'ok'" if retry_failed else "fetch_status IS NOT NULL"
        rows = conn.execute(
            f"SELECT chrome_id FROM bookmarks WHERE {where}"
        ).fetchall()
        existing = {r["chrome_id"] for r in rows}

    todo = [b for b in bookmarks if b["chrome_id"] not in existing]
    if limit is not None:
        todo = todo[:limit]
    print(
        f"Indexing {len(todo)} of {len(bookmarks)} bookmarks "
        f"({len(existing)} already done)"
    )

    sem = asyncio.Semaphore(CONCURRENCY)
    write_lock = asyncio.Lock()
    done = 0

    async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}) as client:

        async def process(b: dict) -> None:
            nonlocal done
            async with sem:
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
    limit: int | None = None
    if "--limit" in args:
        i = args.index("--limit")
        if i + 1 < len(args):
            limit = int(args[i + 1])
    asyncio.run(index_all(force=force, retry_failed=retry_failed, limit=limit))


if __name__ == "__main__":
    run()
