"""ساخت دکمه‌های اینلاین (لینک، کال‌بک، وب‌اپ شیشه‌ای تلگرام)."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def _is_http_url(s: str) -> bool:
    try:
        u = urlparse(s)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False


def parse_inline_keyboard(spec: str) -> InlineKeyboardMarkup:
    """
    هر خط = یک ردیف دکمه.
    در یک خط، دکمه‌ها با || از هم جدا می‌شوند.

    انواع دکمه:
    - لینک معمولی: متن | https://example.com
    - دکمه شیشه‌ای (وب‌اپ مینی): متن | webapp:https://example.com/app
    - کال‌بک: متن | cb:داده (حداکثر ۶۴ بایت برای داده)

    مثال:
      خرید | https://shop.example.com || پشتیبانی | https://t.me/support
      باز کردن اپ | webapp:https://mydomain.com/tg-app.html
    """
    rows: list[list[InlineKeyboardButton]] = []
    for raw_line in spec.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        row: list[InlineKeyboardButton] = []
        for cell in line.split("||"):
            cell = cell.strip()
            if not cell:
                continue
            if "|" not in cell:
                raise ValueError(
                    f"فرمت نامعتبر «{cell}». باید «متن | نوع» باشد (مثلاً متن | https://...)."
                )
            title, rest = cell.split("|", 1)
            title = title.strip()
            rest = rest.strip()
            if not title:
                raise ValueError("متن دکمه نباید خالی باشد.")

            low = rest.lower()
            if low.startswith("webapp:"):
                url = rest.split(":", 1)[1].strip()
                if not _is_http_url(url):
                    raise ValueError(f"آدرس وب‌اپ نامعتبر: {url}")
                row.append(
                    InlineKeyboardButton(title, web_app={"url": url})
                )
            elif low.startswith("cb:"):
                data = rest[3:].strip()
                if len(data.encode("utf-8")) > 64:
                    raise ValueError("داده callback خیلی بلند است (حداکثر ۶۴ بایت).")
                row.append(InlineKeyboardButton(title, callback_data=data))
            elif _is_http_url(rest):
                row.append(InlineKeyboardButton(title, url=rest))
            else:
                raise ValueError(
                    f"نوع دکمه نامشخص برای «{rest}». از https://... یا webapp:... یا cb:... استفاده کنید."
                )
        if row:
            rows.append(row)
    if not rows:
        raise ValueError("حداقل یک دکمه لازم است (یا /بدون_دکمه بزنید).")
    return InlineKeyboardMarkup(rows)


def optional_keyboard_from_spec(spec: str | None) -> InlineKeyboardMarkup | None:
    if spec is None:
        return None
    s = spec.strip()
    if not s:
        return None
    return parse_inline_keyboard(s)
