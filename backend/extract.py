import httpx
import trafilatura


async def extract(client: httpx.AsyncClient, url: str) -> tuple[str | None, str | None, str]:
    """Fetch a URL and return (title, main_text, status)."""
    try:
        r = await client.get(url, follow_redirects=True, timeout=15)
    except httpx.HTTPError as e:
        return None, None, f"error:{type(e).__name__}"

    if r.status_code != 200:
        return None, None, f"http_{r.status_code}"

    ctype = r.headers.get("content-type", "")
    if "html" not in ctype and "xml" not in ctype:
        return None, None, f"skip:{ctype.split(';')[0] or 'unknown'}"

    text = trafilatura.extract(
        r.text, include_comments=False, include_tables=False, favor_recall=True
    )
    meta = trafilatura.extract_metadata(r.text)
    title = meta.title if meta else None
    return title, text, "ok"
