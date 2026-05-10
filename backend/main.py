from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .db import connect, init


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield


app = FastAPI(title="bookmarks", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _fts_query(q: str) -> str:
    """Turn a freeform query into an FTS5 MATCH expression with prefix search per token."""
    tokens = [t.replace('"', '""') for t in q.split() if t]
    return " ".join(f'"{t}"*' for t in tokens)


@app.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(50, ge=1, le=200)):
    fts_q = _fts_query(q)
    if not fts_q:
        return {"results": []}
    conn = connect()
    try:
        rows = conn.execute(
            """SELECT b.id, b.name, b.url, b.folder, b.title,
                      snippet(bookmarks_fts, -1, '<mark>', '</mark>', '...', 16) AS snippet,
                      bm25(bookmarks_fts) AS rank
                 FROM bookmarks_fts
                 JOIN bookmarks b ON b.id = bookmarks_fts.rowid
                WHERE bookmarks_fts MATCH ?
                ORDER BY rank
                LIMIT ?""",
            (fts_q, limit),
        ).fetchall()
    finally:
        conn.close()
    return {"results": [dict(r) for r in rows]}


@app.get("/stats")
def stats():
    conn = connect()
    try:
        total = conn.execute("SELECT COUNT(*) AS c FROM bookmarks").fetchone()["c"]
        ok = conn.execute(
            "SELECT COUNT(*) AS c FROM bookmarks WHERE fetch_status='ok'"
        ).fetchone()["c"]
    finally:
        conn.close()
    return {"total": total, "indexed_ok": ok}


def run() -> None:
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=7777, reload=False)


if __name__ == "__main__":
    run()
