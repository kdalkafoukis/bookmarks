import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "bookmarks.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS bookmarks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chrome_id   TEXT UNIQUE,
    name        TEXT,
    url         TEXT NOT NULL,
    folder      TEXT,
    date_added  INTEGER,
    title       TEXT,
    content     TEXT,
    indexed_at  TEXT,
    fetch_status TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS bookmarks_fts USING fts5(
    name, url, folder, title, content,
    content='bookmarks',
    content_rowid='id',
    tokenize='porter unicode61'
);

CREATE TRIGGER IF NOT EXISTS bookmarks_ai AFTER INSERT ON bookmarks BEGIN
    INSERT INTO bookmarks_fts(rowid, name, url, folder, title, content)
    VALUES (new.id, new.name, new.url, new.folder, new.title, new.content);
END;

CREATE TRIGGER IF NOT EXISTS bookmarks_ad AFTER DELETE ON bookmarks BEGIN
    INSERT INTO bookmarks_fts(bookmarks_fts, rowid, name, url, folder, title, content)
    VALUES ('delete', old.id, old.name, old.url, old.folder, old.title, old.content);
END;

CREATE TRIGGER IF NOT EXISTS bookmarks_au AFTER UPDATE ON bookmarks BEGIN
    INSERT INTO bookmarks_fts(bookmarks_fts, rowid, name, url, folder, title, content)
    VALUES ('delete', old.id, old.name, old.url, old.folder, old.title, old.content);
    INSERT INTO bookmarks_fts(rowid, name, url, folder, title, content)
    VALUES (new.id, new.name, new.url, new.folder, new.title, new.content);
END;
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
