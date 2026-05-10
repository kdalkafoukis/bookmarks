import json
import platform
from pathlib import Path
from typing import Iterator


def chrome_bookmarks_path() -> Path:
    home = Path.home()
    system = platform.system()
    if system == "Darwin":
        return home / "Library/Application Support/Google/Chrome/Default/Bookmarks"
    if system == "Linux":
        return home / ".config/google-chrome/Default/Bookmarks"
    if system == "Windows":
        return home / "AppData/Local/Google/Chrome/User Data/Default/Bookmarks"
    raise RuntimeError(f"Unsupported OS: {system}")


def _walk(node: dict, folder_path: list[str]) -> Iterator[dict]:
    node_type = node.get("type")
    if node_type == "url":
        url = node.get("url", "")
        if not url.startswith(("http://", "https://")):
            return
        yield {
            "chrome_id": node["id"],
            "name": node.get("name", ""),
            "url": url,
            "folder": " / ".join(folder_path),
            "date_added": int(node.get("date_added", 0)),
        }
    elif node_type == "folder":
        new_path = folder_path + [node.get("name", "")]
        for child in node.get("children", []):
            yield from _walk(child, new_path)


def load_bookmarks(path: Path | None = None) -> list[dict]:
    path = path or chrome_bookmarks_path()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out: list[dict] = []
    for root_name in ("bookmark_bar", "other", "synced"):
        root = data.get("roots", {}).get(root_name)
        if root:
            out.extend(_walk(root, [root_name]))
    return out
