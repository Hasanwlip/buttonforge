"""Per-admin UI language and default channel (JSON under data/)."""

from __future__ import annotations

import json
from pathlib import Path

import config

_ROOT = Path(__file__).resolve().parent
_FILE = _ROOT / "data" / "user_prefs.json"


def _load() -> dict:
    if not _FILE.exists():
        return {"users": {}}
    with open(_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    _FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = _FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(_FILE)


def get_lang(uid: int) -> str | None:
    v = _load()["users"].get(str(uid), {}).get("lang")
    if v in ("en", "fa"):
        return v
    return None


def set_lang(uid: int, lang: str) -> None:
    data = _load()
    data["users"].setdefault(str(uid), {})
    data["users"][str(uid)]["lang"] = lang
    _save(data)


def get_channel(uid: int) -> str | None:
    v = _load()["users"].get(str(uid), {}).get("channel_id")
    if v and str(v).strip():
        return str(v).strip()
    return None


def set_channel(uid: int, channel_id: str) -> None:
    data = _load()
    data["users"].setdefault(str(uid), {})
    data["users"][str(uid)]["channel_id"] = channel_id.strip()
    _save(data)


def effective_channel(uid: int) -> str | None:
    ch = get_channel(uid)
    if ch:
        return ch
    g = (config.CHANNEL_ID or "").strip()
    return g or None
