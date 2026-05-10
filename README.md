# bookmarks

Local full-text search over your Chrome bookmarks. Fetches each bookmarked
page, extracts the main article text with `trafilatura`, indexes it in
SQLite FTS5, and exposes a tiny FastAPI server. A Manifest V3 Chrome
extension queries that server from a popup.

```
Chrome bookmarks JSON  ──►  indexer (httpx + trafilatura)  ──►  SQLite (FTS5)
                                                                      ▲
                                            FastAPI on 127.0.0.1:7777 ┘
                                                       ▲
                                            Chrome extension popup
```

## Requirements

- Python 3.11+ (this project was set up against Homebrew's `python3.13`)
- Google Chrome

## Install

```sh
python3.13 -m venv .venv
.venv/bin/pip install -e .
```

## Index your bookmarks

The indexer reads Chrome's bookmarks file directly (auto-detected on
macOS / Linux / Windows), fetches each URL with `httpx`, and stores the
extracted main text in `bookmarks.db` (created in the project root).

```sh
.venv/bin/bookmarks-index                  # incremental — skips anything already attempted
.venv/bin/bookmarks-index --limit 50       # only index the first 50 not-yet-attempted
.venv/bin/bookmarks-index --retry-failed   # also retry previous failures (skip only successes)
.venv/bin/bookmarks-index --force          # re-fetch everything
```

Dedup key is Chrome's stable `chrome_id`. By default the indexer skips
anything that already has a `fetch_status` row in the DB — so failed
fetches (dead links, paywalls, JS-only pages, timeouts) are *not*
retried unless you ask for it. Use `--retry-failed` if you suspect
transient failures on the last run.

## Run the search server

```sh
.venv/bin/bookmarks-serve
```

Listens on `http://127.0.0.1:7777`. Endpoints:

- `GET /search?q=<terms>&limit=50` — FTS5 with prefix matching, ranked by bm25
- `GET /stats` — total bookmarks vs successfully indexed

## Load the extension

1. Visit `chrome://extensions`
2. Toggle **Developer mode** (top right)
3. Click **Load unpacked** and pick the `extension/` folder
4. Pin the icon, click it, search

The popup expects the local server to be running on
`http://127.0.0.1:7777`. If it isn't, the popup shows an error.

## Layout

```
backend/         FastAPI app, SQLite/FTS5 schema, indexer
extension/       Manifest V3 Chrome extension (popup-only)
pyproject.toml   Dependencies + console scripts
bookmarks.db     SQLite database (gitignored, created on first run)
```
