# LLM roadmap

Forward-looking notes on adding semantic search and LLM-powered Q&A on
top of the existing FTS5 backend. Written when the FTS5 v1 was working
and we wanted to capture the "what would the LLM version look like" plan
before forgetting it.

## Where we are today (v1)

- Chrome bookmarks → fetch with `httpx` → extract main text with `trafilatura` → store in SQLite
- `bookmarks_fts` is an FTS5 virtual table over `name, url, folder, title, content` with porter+unicode61 tokenizer
- BM25 ranking, prefix matching per token, snippets via `snippet(...)`
- Manifest V3 popup hits `GET /search?q=...` on `127.0.0.1:7777`

This already turns "I have no idea how to find info" from impossible to
keyword-feasible. The LLM path makes it feel magical instead of just
useful.

## Two layers (they compose)

### Layer 1 — Embeddings (semantic search)

Replaces "match the words you typed" with "match what you meant."

> "that thing about distributed locks in Postgres" finds your bookmark
> titled *"Advisory locks for serializable workflows"* even though no
> word overlaps.

**What changes:**

- `backend/db.py`: add two columns on `bookmarks`
  - `embedding BLOB` — raw float32 vector (numpy `tobytes()`)
  - `embed_status TEXT` — `ok` / `error:*` / `skip:no_content`
- New `backend/embed.py`: provider abstraction. One function `embed_texts(list[str]) -> list[np.ndarray]`.
- New `backend/embed_runner.py` (or a flag on the existing indexer):
  walks rows where `embed_status IS NULL AND content IS NOT NULL`,
  batches to the provider, writes vectors back. **Separate pass from the
  fetch step** so adding embeddings later doesn't re-download anything.
- `backend/main.py`: extend `/search` with `mode={fts,semantic,hybrid}`,
  default `hybrid`. Hybrid blends FTS5 rank and cosine similarity with
  Reciprocal Rank Fusion (RRF) — ~5 lines of Python.
- `pyproject.toml`: add `numpy` plus one provider (see matrix below).

**Storage math:** 9.8k bookmarks × 768 dims × 4 bytes ≈ 30 MB. Brute-force
cosine in numpy is <100 ms. No need for `sqlite-vec` until you cross
~100k vectors.

**Content truncation:** most embedding models cap at 8k–32k tokens.
For v1, embed `f"{title}\n\n{content[:8000]}"`. Don't over-engineer.

#### Provider matrix

| Provider | Cost (full 9.8k index) | Quality | Setup | Notes |
|---|---|---|---|---|
| `sentence-transformers` + `bge-small-en-v1.5` | $0 | Good | `pip install`, ~130 MB model | Runs CPU, ~10–20 min full pass. No API key. |
| Voyage `voyage-3` | ~$1–2 | Best | API key | Anthropic's recommended embedding provider. |
| OpenAI `text-embedding-3-small` | ~$0.20 | Very good | API key | Cheapest API option, easy. |
| OpenAI `text-embedding-3-large` | ~$1.30 | Best (tied with Voyage) | API key | Worth it only if quality matters. |

**Recommendation:** start with local `bge-small-en-v1.5`. Free, no key,
quality is plenty for personal bookmark search. Switch to Voyage later
if results disappoint — same interface, just swap the function body.

### Layer 2 — Claude as the search UI (`/ask`)

This is the part that actually solves "9,800 bookmarks, no idea where
anything is."

New endpoint `GET /ask?q=...`:

1. Run hybrid search (Layer 1) → top 10–20 candidates.
2. Send candidates + the user's question to Claude.
3. Claude returns the 1–3 most relevant bookmarks with a one-line *why*
   for each.

```
You: "that thing I read about why python in alpine docker was slow"
Claude: → "Using Alpine can make Python Docker builds 50× slower"
         (folder: daily_bookmarks/...)
         — matches "alpine + python + slow builds"
```

**Code-wise:** ~50 lines.

- New `backend/ask.py` with one function: build prompt, call
  `claude-sonnet-4-6` (or whatever's current), parse a small JSON reply.
- Use **prompt caching** on the system prompt and the search results so
  repeat queries are fast and cheap. (See the `claude-api` skill — this
  is exactly its sweet spot.)
- New endpoint `/ask` in `backend/main.py`.
- `pyproject.toml`: add `anthropic`.
- Extension popup: small toggle "🔍 Search / 💬 Ask" — same input box,
  different endpoint.

**Cost sketch:** with caching, each `/ask` call is roughly:
~2k cached input tokens + ~1k uncached + ~200 output. On Sonnet that's
sub-cent per query.

## Indexing flow with both layers

```
fetch + extract  ──►  bookmarks(content)  ──►  embed_runner  ──►  bookmarks(embedding)
                            │                                          │
                            ▼                                          ▼
                       FTS5 index                               numpy cosine
                            └──────────── /search?mode=hybrid ─────────┘
                                                  │
                                                  ▼  (top 10–20)
                                                Claude  ──►  /ask response
```

Each box is independent. You can ship Layer 1 alone, or Layer 2 alone
on top of FTS5 without embeddings, or both.

## What stays the same

- The fetch + trafilatura + SQLite pipeline
- Chrome bookmarks parser (`backend/bookmarks.py`)
- Dedup on `chrome_id` + `fetch_status`
- The extension shell — popup, MV3 manifest, icons
- The `/search` and `/stats` endpoints (we *extend* `/search`, don't break it)

## Decisions to make when picking this up again

1. **Embeddings provider** — local vs Voyage vs OpenAI. Default to local
   `bge-small` unless you specifically want top-tier quality.
2. **Ship Layer 1 alone first, or both at once?** Layer 1 alone is
   already a big upgrade and lets you sanity-check semantic recall
   before building the LLM layer on top.
3. **`/ask` UX** — separate endpoint vs adding `mode=ask` to `/search`.
   Separate endpoint is cleaner because the response shape is different
   (it includes Claude's reasoning, not just rows).
4. **Prompt caching strategy** — cache the system prompt only, or also
   cache the candidate list? Caching candidates only makes sense if the
   user asks multiple questions in a row about the same topic. Probably
   start with system-prompt-only caching.
5. **Re-embedding cadence** — when bookmarks change, only their text
   needs re-fetching; embeddings get refreshed by the same `embed_status
   IS NULL` filter the runner already uses. Nothing extra needed.

## Out of scope (resist the temptation)

- Vector DBs (Pinecone, Weaviate, Qdrant). 30 MB of vectors does not need
  infra.
- Reranker models (Cohere Rerank etc.). Claude is the reranker in
  Layer 2 — and it can also explain *why*, which a reranker can't.
- Chunking bookmarks into multiple vectors. One vector per bookmark is
  fine until results are visibly bad on long pages.
- Streaming the `/ask` response. The response is small; just return it.
- Auth on the local server. It's bound to `127.0.0.1`.
