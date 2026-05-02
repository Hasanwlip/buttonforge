"""تبدیل متن دکمه‌ها به InlineKeyboardMarkup (ButtonForge)."""

import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Telegram: فقط این استایل‌ها (بدون رنگ دلخواه hex).
_STYLE_ALIASES: dict[str, str] = {
    "primary": "primary",
    "blue": "primary",
    "success": "success",
    "green": "success",
    "danger": "danger",
    "red": "danger",
}


def _split_trailing_style(raw: str) -> tuple[str, str | None, str | None]:
    s = raw.strip()
    m = re.search(r"\s+style:\s*(\w+)\s*$", s, re.IGNORECASE)
    if not m:
        return s, None, None
    key = m.group(1).lower()
    base = s[: m.start()].strip()
    norm = _STYLE_ALIASES.get(key)
    if norm is None:
        return (
            "",
            None,
            f"استایل ناشناس «{key}». مجاز: primary|blue، success|green، danger|red",
        )
    return base, norm, None


def _parse_one_cell(raw: str) -> tuple[InlineKeyboardButton | None, str | None]:
    if not raw.strip():
        return None, None

    s, style, style_err = _split_trailing_style(raw)
    if style_err:
        return None, style_err
    if not s:
        return None, None

    extra = {"style": style} if style else {}
    low = s.lower()

    if " webapp:" in low:
        i = low.rfind(" webapp:")
        title = s[:i].strip()
        url = s[i + len(" webapp:") :].strip().split()[0]
        if title and url.lower().startswith("https://"):
            return InlineKeyboardButton(text=title, web_app=WebAppInfo(url=url), **extra), None
        return None, None

    if " url:" in low:
        i = low.rfind(" url:")
        title = s[:i].strip()
        url = s[i + len(" url:") :].strip().split()[0]
        if title and re.match(r"^https?://", url, re.I):
            return InlineKeyboardButton(text=title, url=url, **extra), None
        return None, None

    if " cb:" in low:
        i = low.rfind(" cb:")
        title = s[:i].strip()
        data = s[i + len(" cb:") :].strip()
        if title and 1 <= len(data.encode("utf-8")) <= 64:
            return InlineKeyboardButton(text=title, callback_data=data, **extra), None
        return None, None

    return None, None


def parse_inline_keyboard(spec: str) -> tuple[InlineKeyboardMarkup | None, str | None]:
    spec = spec.strip()
    if not spec:
        return None, None

    rows: list[list[InlineKeyboardButton]] = []
    errors: list[str] = []

    for line_no, line in enumerate(spec.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        row: list[InlineKeyboardButton] = []
        for cell in line.split("|"):
            btn, cell_err = _parse_one_cell(cell)
            if cell_err:
                snippet = cell.strip()[:48] + ("…" if len(cell.strip()) > 48 else "")
                errors.append(f"خط {line_no}: {cell_err} (سلول «{snippet}»)")
            elif btn is None:
                snippet = cell.strip()[:48] + ("…" if len(cell.strip()) > 48 else "")
                errors.append(f"خط {line_no}: سلول نامعتبر «{snippet}»")
            else:
                row.append(btn)
        if row:
            rows.append(row)

    if errors and not rows:
        return None, "\n".join(errors[:5])
    if errors:
        return InlineKeyboardMarkup(rows), "هشدار:\n" + "\n".join(errors[:5])
    if not rows:
        return None, "هیچ دکمهٔ معتبری پیدا نشد."
    return InlineKeyboardMarkup(rows), None
