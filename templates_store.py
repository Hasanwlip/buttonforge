"""ذخیرهٔ قالب‌های پست برای استفادهٔ دوباره (فایل JSON در پوشهٔ data)."""

from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_DATA = _ROOT / "data"
_FILE = _DATA / "templates.json"


def _load() -> dict:
    if not _FILE.exists():
        return {"templates": []}
    with open(_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    _DATA.mkdir(parents=True, exist_ok=True)
    with open(_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def list_templates() -> list[dict]:
    return list(_load().get("templates", []))


def add_template(name: str, body: str, photo_file_id: str | None, keys_raw: str) -> None:
    data = _load()
    data.setdefault("templates", []).append(
        {
            "name": (name or "").strip()[:80],
            "body": body or "",
            "photo_file_id": photo_file_id,
            "keys_raw": keys_raw or "",
        }
    )
    _save(data)


def get_template(index: int) -> dict | None:
    t = list_templates()
    if 0 <= index < len(t):
        return t[index]
    return None
