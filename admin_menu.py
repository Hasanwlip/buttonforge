"""Reply keyboards — labels depend on i18n language."""

from __future__ import annotations

from telegram import (
    KeyboardButton,
    KeyboardButtonRequestUsers,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from i18n import ALL_MENU_LABELS, STRINGS, menu_action_from_text


def _b(lang: str, key: str) -> str:
    return STRINGS[lang][key]


def kb_idle(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(_b(lang, "btn_text_post")),
                KeyboardButton(_b(lang, "btn_photo_post")),
            ],
            [
                KeyboardButton(_b(lang, "btn_templates")),
                KeyboardButton(_b(lang, "btn_menu")),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def kb_ready(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(_b(lang, "btn_confirm_ch")),
                KeyboardButton(_b(lang, "btn_confirm_dm")),
            ],
            [KeyboardButton(_b(lang, "btn_confirm_all"))],
            [
                KeyboardButton(_b(lang, "btn_save_template")),
                KeyboardButton(_b(lang, "btn_templates")),
            ],
            [
                KeyboardButton(_b(lang, "btn_cancel")),
                KeyboardButton(_b(lang, "btn_menu")),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def kb_busy(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(_b(lang, "btn_cancel")),
                KeyboardButton(_b(lang, "btn_menu")),
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def kb_pick_user(lang: str, request_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    text=_b(lang, "btn_pick_contact"),
                    request_users=KeyboardButtonRequestUsers(
                        request_id=request_id,
                        user_is_bot=False,
                        max_quantity=1,
                    ),
                )
            ],
            [KeyboardButton(_b(lang, "btn_pick_cancel"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def kb_remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


# re-export for on_text guards
MENU_LABELS = ALL_MENU_LABELS

__all__ = [
    "kb_idle",
    "kb_ready",
    "kb_busy",
    "kb_pick_user",
    "kb_remove",
    "MENU_LABELS",
    "menu_action_from_text",
]
