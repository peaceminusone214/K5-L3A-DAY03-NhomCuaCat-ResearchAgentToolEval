from __future__ import annotations

from typing import Any

from tools._shared import err


def dedupe_items(items: list[dict[str, Any]] | None = None, key: str = "url") -> dict[str, Any]:
    """Remove duplicate research items while preserving their first-seen order."""
    try:
        if items is None:
            items = []
        if not isinstance(items, list):
            raise TypeError("items must be a list")
        if key not in {"url", "title"}:
            raise ValueError("key must be 'url' or 'title'")
        unique: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in items:
            if not isinstance(item, dict):
                raise TypeError("every item must be an object")
            value = str(item.get(key) or "").strip()
            marker = value.casefold() if value else f"__missing_{len(unique)}"
            if marker not in seen:
                seen.add(marker)
                unique.append(item)
        return {"tool": "dedupe_items", "items": unique, "input_count": len(items), "removed_count": len(items) - len(unique)}
    except Exception as exc:
        return err("dedupe_items", exc)
