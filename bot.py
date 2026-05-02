"""
ButtonForge — Telegram bot: channel posts + inline keyboards, per-admin language
and default channel; native sends (no forward).
"""

from __future__ import annotations

import logging
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import admin_menu as am
import config
import i18n
import templates_store
import user_prefs
from keyboard_parser import parse_inline_keyboard

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("buttonforge")

REQ_PICK_DM = 1
REQ_PICK_DM_AFTER_CHANNEL = 2

_CHANNEL_TEXT_RE = re.compile(r"^@[A-Za-z0-9_]{4,}$")
_CHANNEL_NUM_RE = re.compile(r"^-100\d{8,}$")


def _uid(update: Update) -> int | None:
    return update.effective_user.id if update.effective_user else None


def _clear_aux(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("pick_shipping", None)
    context.user_data.pop("await_template_name", None)
    context.user_data.pop("template_save_payload", None)


def _is_admin(user_id: int | None) -> bool:
    if user_id is None:
        return False
    if config.OPEN_ACCESS:
        return True
    return user_id in config.ADMIN_IDS


def _channel_display(uid: int) -> str:
    ch = user_prefs.effective_channel(uid)
    if not ch:
        return i18n.tr(uid, "channel_none")
    return ch.replace("&", "&amp;").replace("<", "&lt;")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        await update.effective_message.reply_text(
            i18n.tr(uid, "access_denied", uid=str(uid)),
            parse_mode=ParseMode.HTML,
        )
        return
    if user_prefs.get_lang(uid) is None:
        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        i18n.STRINGS["en"]["btn_lang_en"], callback_data="uilang:en"
                    ),
                    InlineKeyboardButton(
                        i18n.STRINGS["fa"]["btn_lang_fa"], callback_data="uilang:fa"
                    ),
                ]
            ]
        )
        await update.effective_message.reply_text(
            i18n.STRINGS["en"]["choose_language"],
            parse_mode=ParseMode.HTML,
            reply_markup=kb,
        )
        return
    if user_prefs.get_channel(uid) is None and not (config.CHANNEL_ID or "").strip():
        await update.effective_message.reply_text(
            i18n.tr(uid, "need_setchannel"),
            parse_mode=ParseMode.HTML,
        )
        return
    ch = _channel_display(uid)
    await update.effective_message.reply_text(
        i18n.tr(uid, "help_block", channel=ch),
        parse_mode=ParseMode.HTML,
        reply_markup=am.kb_idle(i18n.ui_lang(uid)),
    )


async def on_ui_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q or not q.data or not _is_admin(_uid(update)):
        return
    m = re.match(r"^uilang:(en|fa)$", q.data)
    if not m:
        return
    uid = q.from_user.id if q.from_user else None
    if uid is None:
        return
    user_prefs.set_lang(uid, m.group(1))
    await q.answer()
    try:
        await q.edit_message_text(
            i18n.tr(uid, "lang_saved"), parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    if user_prefs.get_channel(uid) is None and not (config.CHANNEL_ID or "").strip():
        await context.bot.send_message(
            chat_id=q.message.chat_id,
            text=i18n.tr(uid, "need_setchannel"),
            parse_mode=ParseMode.HTML,
        )
    else:
        await context.bot.send_message(
            chat_id=q.message.chat_id,
            text=i18n.tr(uid, "help_block", channel=_channel_display(uid)),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_idle(i18n.ui_lang(uid)),
        )


def _channel_error_i18n_key(err: str) -> str:
    low = err.lower()
    if any(
        s in low
        for s in (
            "not enough rights",
            "chat_admin",
            "forbidden",
            "not a member",
            "kicked",
            "chat_write",
            "need administrator",
            "can't write",
            "cannot write",
        )
    ):
        return "channel_not_admin"
    return "channel_post_failed"


async def set_channel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        return
    raw = ""
    if context.args:
        raw = context.args[0].strip()
    elif update.message and update.message.text:
        m = re.match(
            r"/setchannel(?:@\S+)?\s+(.+)",
            update.message.text.strip(),
            re.IGNORECASE | re.DOTALL,
        )
        if m:
            raw = m.group(1).strip()
    if not raw:
        await update.effective_message.reply_text(
            i18n.tr(uid, "setchannel_usage"), parse_mode=ParseMode.HTML
        )
        return
    if not (_CHANNEL_TEXT_RE.match(raw) or _CHANNEL_NUM_RE.match(raw)):
        await update.effective_message.reply_text(i18n.tr(uid, "channel_invalid"))
        return
    user_prefs.set_channel(uid, raw)
    esc = raw.replace("&", "&amp;").replace("<", "&lt;")
    await update.effective_message.reply_text(
        i18n.tr(uid, "channel_set_ok", ch=esc),
        parse_mode=ParseMode.HTML,
        reply_markup=am.kb_idle(i18n.ui_lang(uid)),
    )


async def cancel_draft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        return
    context.user_data.pop("draft", None)
    _clear_aux(context)
    await update.effective_message.reply_text(
        i18n.tr(uid, "draft_cleared"), reply_markup=am.kb_idle(i18n.ui_lang(uid))
    )


def _draft(context: ContextTypes.DEFAULT_TYPE) -> dict:
    d = context.user_data.get("draft")
    if not isinstance(d, dict):
        d = {}
        context.user_data["draft"] = d
    return d


async def begin_pick_user_send(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    request_id: int,
    *,
    intro_html: str | None = None,
) -> None:
    uid = _uid(update)
    lang = i18n.ui_lang(uid)
    d = _ready_draft(context)
    if not d:
        await update.effective_message.reply_text(
            i18n.tr(uid, "no_draft"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_idle(lang),
        )
        return
    context.user_data["pick_shipping"] = {
        "request_id": request_id,
        "body": d.get("body") or "",
        "markup": d.get("markup"),
        "photo_file_id": d.get("photo_file_id"),
    }
    context.user_data.pop("draft", None)
    intro = intro_html or i18n.tr(uid, "pick_dm_intro")
    await update.effective_message.reply_text(
        intro,
        parse_mode=ParseMode.HTML,
        reply_markup=am.kb_pick_user(lang, request_id),
    )


async def show_templates_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    lang = i18n.ui_lang(uid)
    rows = templates_store.list_templates()
    if not rows:
        await update.effective_message.reply_text(
            i18n.tr(uid, "no_templates"), reply_markup=am.kb_idle(lang)
        )
        return
    kb: list[list[InlineKeyboardButton]] = []
    for i, t in enumerate(rows[:40]):
        name = (t.get("name") or f"#{i}")[:40]
        kb.append([InlineKeyboardButton(name, callback_data=f"tpl:{i}")])
    await update.effective_message.reply_text(
        i18n.tr(uid, "pick_template"), reply_markup=InlineKeyboardMarkup(kb)
    )


async def present_ready_preview(
    update: Update, context: ContextTypes.DEFAULT_TYPE, d: dict
) -> None:
    uid = _uid(update)
    lang = i18n.ui_lang(uid)
    await update.effective_chat.send_message(
        i18n.tr(uid, "preview_ready_line"),
        parse_mode=ParseMode.HTML,
        reply_markup=am.kb_ready(lang),
    )
    if d.get("photo_file_id"):
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=d["photo_file_id"],
            caption=d.get("body") or None,
            reply_markup=d.get("markup"),
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=d.get("body") or "",
            reply_markup=d.get("markup"),
        )


async def on_template_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q or not q.data:
        return
    m = re.match(r"^tpl:(\d+)$", q.data)
    uid = _uid(update)
    if not m or not _is_admin(uid):
        return
    idx = int(m.group(1))
    tpl = templates_store.get_template(idx)
    if not tpl:
        await q.answer(i18n.tr(uid, "tpl_not_found"), show_alert=True)
        return
    keys_raw = tpl.get("keys_raw") or ""
    markup = None
    if keys_raw.strip():
        markup, warn = parse_inline_keyboard(keys_raw)
        if markup is None and warn:
            await q.answer(i18n.tr(uid, "tpl_btn_error"), show_alert=True)
            return
    d = _draft(context)
    d.clear()
    d["mode"] = "ready"
    d["body"] = tpl.get("body") or ""
    d["photo_file_id"] = tpl.get("photo_file_id")
    d["markup"] = markup
    d["keys_raw"] = keys_raw
    await q.answer(i18n.tr(uid, "tpl_loaded"))
    try:
        await q.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass
    await present_ready_preview(update, context, d)


async def on_users_shared(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        return
    msg = update.message
    if not msg or not msg.users_shared:
        return
    us = msg.users_shared
    ps = context.user_data.get("pick_shipping")
    if not ps or us.request_id != ps["request_id"]:
        return
    tgt = us.users[0].user_id
    lang = i18n.ui_lang(uid)
    try:
        await _send_draft_native(
            context.bot,
            tgt,
            ps.get("markup"),
            ps.get("body") or "",
            ps.get("photo_file_id"),
        )
    except Exception as e:
        logger.warning("pick send failed: %s", e)
        await msg.reply_text(
            i18n.tr(uid, "posted_dm_fail", err=str(e)),
            reply_markup=am.kb_idle(lang),
        )
        context.user_data.pop("pick_shipping", None)
        return
    context.user_data.pop("pick_shipping", None)
    await msg.reply_text(
        i18n.tr(uid, "posted_dm_ok"), reply_markup=am.kb_idle(lang)
    )


async def _begin_text_post_flow(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    uid = _uid(update)
    lang = i18n.ui_lang(uid)
    _clear_aux(context)
    _draft(context).clear()
    _draft(context)["mode"] = "await_text"
    await update.effective_message.reply_text(
        i18n.tr(uid, "begin_text"),
        parse_mode=ParseMode.HTML,
        reply_markup=am.kb_busy(lang),
    )


async def _begin_photo_post_flow(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    uid = _uid(update)
    lang = i18n.ui_lang(uid)
    _clear_aux(context)
    _draft(context).clear()
    _draft(context)["mode"] = "await_photo"
    await update.effective_message.reply_text(
        i18n.tr(uid, "begin_photo"),
        parse_mode=ParseMode.HTML,
        reply_markup=am.kb_busy(lang),
    )


async def post_text_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(_uid(update)):
        return
    await _begin_text_post_flow(update, context)


async def post_photo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(_uid(update)):
        return
    await _begin_photo_post_flow(update, context)


async def try_admin_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, d: dict
) -> bool:
    act = am.menu_action_from_text(text)
    if act is None:
        return False
    uid = _uid(update)
    lang = i18n.ui_lang(uid)
    msg = update.effective_message
    if act == "pick_cancel":
        context.user_data.pop("pick_shipping", None)
        await msg.reply_text(
            i18n.tr(uid, "pick_cancelled"), reply_markup=am.kb_idle(lang)
        )
        return True
    if act == "cancel":
        context.user_data.pop("draft", None)
        _clear_aux(context)
        await msg.reply_text(
            i18n.tr(uid, "draft_cleared"), reply_markup=am.kb_idle(lang)
        )
        return True
    if act == "menu":
        context.user_data.pop("draft", None)
        _clear_aux(context)
        await start(update, context)
        return True
    if act == "text_post":
        await _begin_text_post_flow(update, context)
        return True
    if act == "photo_post":
        await _begin_photo_post_flow(update, context)
        return True
    if act == "templates":
        await show_templates_list(update, context)
        return True
    if act == "save_template":
        if d.get("mode") != "ready":
            await msg.reply_text(
                i18n.tr(uid, "save_template_first"), reply_markup=am.kb_idle(lang)
            )
            return True
        context.user_data["template_save_payload"] = {
            "body": d.get("body") or "",
            "photo_file_id": d.get("photo_file_id"),
            "keys_raw": d.get("keys_raw", ""),
        }
        context.user_data["await_template_name"] = True
        await msg.reply_text(
            i18n.tr(uid, "template_name_prompt"), reply_markup=am.kb_busy(lang)
        )
        return True
    if act in ("confirm_ch", "confirm_dm", "confirm_all"):
        if d.get("mode") != "ready":
            await msg.reply_text(
                i18n.tr(uid, "no_preview_yet"), reply_markup=am.kb_idle(lang)
            )
            return True
        if act == "confirm_ch":
            await confirm_send(update, context)
        elif act == "confirm_dm":
            await begin_pick_user_send(update, context, REQ_PICK_DM)
        else:
            await confirm_all(update, context)
        return True
    return False


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        return
    lang = i18n.ui_lang(uid)
    d = _draft(context)
    mode = d.get("mode")
    text = (update.message.text or "").strip()

    if user_prefs.get_lang(uid) and user_prefs.get_channel(uid) is None:
        if not (config.CHANNEL_ID or "").strip():
            if _CHANNEL_TEXT_RE.match(text) or _CHANNEL_NUM_RE.match(text):
                user_prefs.set_channel(uid, text)
                esc = text.replace("&", "&amp;").replace("<", "&lt;")
                await update.message.reply_text(
                    i18n.tr(uid, "channel_set_ok", ch=esc),
                    parse_mode=ParseMode.HTML,
                    reply_markup=am.kb_idle(lang),
                )
                return

    if await try_admin_menu(update, context, text, d):
        return

    if context.user_data.get("await_template_name"):
        name = text.strip()
        if len(name) < 1:
            await update.message.reply_text(
                i18n.tr(uid, "template_name_short"), reply_markup=am.kb_busy(lang)
            )
            return
        payload = context.user_data.pop("template_save_payload", None)
        context.user_data.pop("await_template_name", None)
        if not payload:
            await update.message.reply_text(
                i18n.tr(uid, "template_save_error"), reply_markup=am.kb_idle(lang)
            )
            return
        templates_store.add_template(
            name,
            payload.get("body") or "",
            payload.get("photo_file_id"),
            payload.get("keys_raw") or "",
        )
        await update.message.reply_text(
            i18n.tr(uid, "template_saved"), reply_markup=am.kb_ready(lang)
        )
        return

    if context.user_data.get("pick_shipping") and not context.user_data.get(
        "await_template_name"
    ):
        if text not in am.MENU_LABELS:
            rid = context.user_data["pick_shipping"]["request_id"]
            await update.message.reply_text(
                i18n.tr(uid, "pick_only_hint"),
                reply_markup=am.kb_pick_user(lang, rid),
            )
            return

    if mode == "await_text":
        d["body"] = text
        d["photo_file_id"] = None
        d["mode"] = "await_keys_text"
        await update.message.reply_text(
            i18n.tr(uid, "await_keys_text"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_busy(lang),
        )
        return

    if mode == "await_keys_text":
        markup = None
        if text != "-":
            markup, warn = parse_inline_keyboard(text)
            if markup is None and warn:
                await update.message.reply_text(
                    "Button parse error:\n" + warn, reply_markup=am.kb_busy(lang)
                )
                return
            if warn:
                await update.message.reply_text(warn, reply_markup=am.kb_busy(lang))
        d["keys_raw"] = text if text != "-" else ""
        d["markup"] = markup
        d["mode"] = "ready"
        await update.message.reply_text(
            i18n.tr(uid, "preview_text"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_ready(lang),
        )
        await update.message.reply_text(
            d.get("body", ""), reply_markup=d.get("markup")
        )
        return

    if mode == "await_caption":
        d["body"] = "" if text == "-" else text
        d["mode"] = "await_keys_photo"
        await update.message.reply_text(
            i18n.tr(uid, "await_keys_photo"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_busy(lang),
        )
        return

    if mode == "await_keys_photo":
        markup = None
        if text != "-":
            markup, warn = parse_inline_keyboard(text)
            if markup is None and warn:
                await update.message.reply_text(
                    "Button parse error:\n" + warn, reply_markup=am.kb_busy(lang)
                )
                return
            if warn:
                await update.message.reply_text(warn, reply_markup=am.kb_busy(lang))
        d["keys_raw"] = text if text != "-" else ""
        d["markup"] = markup
        d["mode"] = "ready"
        await update.message.reply_text(
            i18n.tr(uid, "preview_photo"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_ready(lang),
        )
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=d["photo_file_id"],
            caption=d.get("body") or None,
            reply_markup=d.get("markup"),
        )
        return


async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        return
    lang = i18n.ui_lang(uid)
    d = _draft(context)
    if d.get("mode") != "await_photo":
        return
    photos = update.message.photo
    if not photos:
        return
    d["photo_file_id"] = photos[-1].file_id
    cap = update.message.caption
    if cap:
        d["body"] = cap.strip()
        d["mode"] = "await_keys_photo"
        await update.message.reply_text(
            i18n.tr(uid, "caption_from_photo"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_busy(lang),
        )
    else:
        d["body"] = ""
        d["mode"] = "await_caption"
        await update.message.reply_text(
            i18n.tr(uid, "await_caption"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_busy(lang),
        )


async def _send_draft_native(
    bot,
    chat_id: int | str,
    markup,
    body: str,
    photo_id: str | None,
) -> None:
    if photo_id:
        await bot.send_photo(
            chat_id=chat_id,
            photo=photo_id,
            caption=body or None,
            reply_markup=markup,
        )
    else:
        await bot.send_message(chat_id=chat_id, text=body, reply_markup=markup)


def _ready_draft(context: ContextTypes.DEFAULT_TYPE) -> dict | None:
    d = context.user_data.get("draft") or {}
    if d.get("mode") != "ready":
        return None
    return d


async def confirm_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        return
    lang = i18n.ui_lang(uid)
    d = _ready_draft(context)
    if not d:
        await update.effective_message.reply_text(
            i18n.tr(uid, "no_draft"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_idle(lang),
        )
        return
    ch = user_prefs.effective_channel(uid)
    if not ch:
        await update.effective_message.reply_text(
            i18n.tr(uid, "no_channel_set"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_idle(lang),
        )
        return
    markup = d.get("markup")
    body = d.get("body") or ""
    photo_id = d.get("photo_file_id")
    try:
        await _send_draft_native(context.bot, ch, markup, body, photo_id)
    except Exception as e:
        logger.exception("send to channel")
        err = str(e)
        key = _channel_error_i18n_key(err)
        await update.effective_message.reply_text(
            i18n.tr(uid, key, err=err),
            reply_markup=am.kb_ready(lang),
        )
        return
    context.user_data.pop("draft", None)
    await update.effective_message.reply_text(
        i18n.tr(uid, "posted_channel"), reply_markup=am.kb_idle(lang)
    )


async def confirm_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(_uid(update)):
        return
    await begin_pick_user_send(update, context, REQ_PICK_DM)


async def confirm_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _uid(update)
    if not _is_admin(uid):
        return
    lang = i18n.ui_lang(uid)
    d = _ready_draft(context)
    if not d:
        await update.effective_message.reply_text(
            i18n.tr(uid, "no_draft"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_idle(lang),
        )
        return
    ch = user_prefs.effective_channel(uid)
    if not ch:
        await update.effective_message.reply_text(
            i18n.tr(uid, "no_channel_set"),
            parse_mode=ParseMode.HTML,
            reply_markup=am.kb_idle(lang),
        )
        return
    markup = d.get("markup")
    body = d.get("body") or ""
    photo_id = d.get("photo_file_id")
    try:
        await _send_draft_native(context.bot, ch, markup, body, photo_id)
    except Exception as e:
        logger.exception("send to channel (confirm_all)")
        err = str(e)
        key = _channel_error_i18n_key(err)
        await update.effective_message.reply_text(
            i18n.tr(uid, key, err=err),
            reply_markup=am.kb_ready(lang),
        )
        return
    context.user_data["pick_shipping"] = {
        "request_id": REQ_PICK_DM_AFTER_CHANNEL,
        "body": body,
        "markup": markup,
        "photo_file_id": photo_id,
    }
    context.user_data.pop("draft", None)
    await update.effective_message.reply_text(
        i18n.tr(uid, "confirm_all_after_ch"),
        parse_mode=ParseMode.HTML,
        reply_markup=am.kb_pick_user(lang, REQ_PICK_DM_AFTER_CHANNEL),
    )


async def callback_dummy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if q:
        await q.answer()


def main() -> None:
    errs = config.validate()
    if errs:
        raise SystemExit("\n".join(errs))

    app = Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setchannel", set_channel_cmd))
    app.add_handler(CommandHandler("post_text", post_text_cmd))
    app.add_handler(CommandHandler("post_photo", post_photo_cmd))
    app.add_handler(CommandHandler("confirm", confirm_send))
    app.add_handler(CommandHandler("confirm_private", confirm_private))
    app.add_handler(CommandHandler("confirm_all", confirm_all))
    app.add_handler(CommandHandler("cancel", cancel_draft))
    app.add_handler(CallbackQueryHandler(on_ui_lang, pattern=r"^uilang:(en|fa)$"))
    app.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & filters.StatusUpdate.USERS_SHARED,
            on_users_shared,
        )
    )
    app.add_handler(CallbackQueryHandler(on_template_chosen, pattern=r"^tpl:\d+$"))
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(CallbackQueryHandler(callback_dummy))

    logger.info("ButtonForge polling started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
