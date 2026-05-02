"""UI strings (en/fa) and reply-keyboard label → action id."""

from __future__ import annotations

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "access_denied": "Access denied. Give this numeric id to a bot admin to add to <code>ADMIN_IDS</code>:\n<code>{uid}</code>",
        "choose_language": "<b>ButtonForge</b>\n\nChoose panel language / <b>زبان پنل را انتخاب کنید:</b>",
        "lang_saved": "Language saved.",
        "need_setchannel": "Set your <b>default channel</b> for publishing:\n<code>/setchannel @YourChannel</code>\n(or paste a numeric id like <code>-100…</code>)\n\nThe bot must be an <b>admin</b> in that channel with <b>Post messages</b>.",
        "setchannel_usage": "Usage: <code>/setchannel @channel_username</code>\nor: <code>/setchannel -100xxxxxxxxxx</code>",
        "channel_set_ok": "Default channel set to <code>{ch}</code>.",
        "channel_invalid": "That does not look like a channel id. Use @name or -100…",
        "no_channel_set": "No default channel yet. Use <code>/setchannel @…</code> first.",
        "channel_post_failed": "Could not post to the channel. Add the bot as admin with “Post messages”.\nError: {err}",
        "channel_not_admin": "The bot is not allowed to post there (not admin or missing rights). Error: {err}",
        "draft_cleared": "Draft cleared.",
        "pick_cancelled": "Recipient selection cancelled.",
        "no_draft": "No draft ready. Start with <code>/post_text</code> or <code>/post_photo</code>.",
        "no_preview_yet": "No preview yet. Start with a text or photo post first.",
        "save_template_first": "Build a preview first, then tap “Save template”.",
        "template_name_prompt": "Send the template name in the next message:",
        "template_name_short": "Please send a clearer template name.",
        "template_save_error": "Could not save; tap “Save template” again.",
        "template_saved": "Template saved. Open “Templates” to load it again.",
        "no_templates": "No templates yet. After a preview, tap “Save template” and send a name.",
        "pick_template": "Tap a template to load into your draft:",
        "tpl_not_found": "Template not found.",
        "tpl_btn_error": "Template buttons are invalid.",
        "tpl_loaded": "Template loaded.",
        "pick_dm_intro": "To send <b>without forwarding</b> to one private chat, tap the button below — Telegram opens its <b>native contact picker</b> (not inside this bot).",
        "confirm_all_after_ch": "Posted to the <b>channel</b>. To send the same to a <b>private</b> chat, use the button below (Telegram picker). You can skip this step (“Cancel recipient pick”).",
        "posted_channel": "Published to the channel (native message, not a forward).",
        "posted_dm_ok": "Sent to that chat as a native message (not a forward).",
        "posted_dm_fail": "Could not send there (user may need to /start the bot first).\nError: {err}",
        "pick_only_hint": "Use “Pick contact in Telegram” or “Cancel recipient pick”.",
        "begin_text": "<b>ButtonForge</b> — <b>Text post</b>.\nSend the post body (plain text).\nUse the bottom keys or commands.",
        "begin_photo": "<b>ButtonForge</b> — <b>Photo post</b>.\nSend a <b>photo</b> (not as a document file). Caption on the photo or in the next message.",
        "await_keys_text": "Send the button layout, or <code>-</code> for no buttons.\nExample:\n<code>Home url:https://t.me/telegram style:primary | Support url:https://t.me/support style:success</code>",
        "await_keys_photo": "Send the button layout, or <code>-</code> for no buttons.",
        "preview_text": "Preview below — bottom keys or commands:\n<code>/confirm</code> · <code>/confirm_private</code> · <code>/confirm_all</code> · <code>/cancel</code>",
        "preview_photo": "Photo preview — bottom keys or commands:\n<code>/confirm</code> · <code>/confirm_private</code> · <code>/confirm_all</code> · <code>/cancel</code>",
        "caption_from_photo": "Caption taken from the photo. Send button layout or <code>-</code>.",
        "await_caption": "Send caption text now, or <code>-</code> for no caption.",
        "preview_ready_line": "Preview — bottom keys or commands:\n<code>/confirm</code> · <code>/confirm_private</code> · <code>/confirm_all</code> · <code>/cancel</code>",
        "help_block": "<b>ButtonForge</b> — admin help\n\n"
        "• <code>/post_text</code> — text-only post (body, then button spec or <code>-</code>)\n"
        "• <code>/post_photo</code> — photo post (photo; caption on photo or next message)\n"
        "• <code>/confirm</code> — publish to <b>your</b> default channel (native, not forward)\n"
        "• <code>/confirm_private</code> — send to a user you pick in <b>Telegram’s picker</b>\n"
        "• <code>/confirm_all</code> — channel first, then optional private pick\n"
        "• <code>/cancel</code> — discard draft\n"
        "• <code>/setchannel @…</code> — set <b>your</b> default channel\n\n"
        "<b>Reply keyboard</b> — same actions; commands always work.\n"
        "<b>Templates</b> — save and reload posts.\n"
        "<b>Updates</b> on server: <code>bash update.sh</code>\n\n"
        "<b>Inline buttons</b> — one row per line; columns with <code>|</code>.\n"
        "<code>Label url:https://…</code> | <code>Label cb:…</code> | <code>Label webapp:https://…</code>\n"
        "<b>Button style</b> (API presets only, optional at end of a cell):\n"
        "<code>style:primary</code> / <code>success</code> / <code>danger</code> (aliases blue/green/red).\n"
        "<i>Custom hex colours are not supported.</i>\n\n"
        "<b>Your default channel:</b> <code>{channel}</code>",
        "btn_text_post": "◇ New text post",
        "btn_photo_post": "◇ New photo post",
        "btn_confirm_ch": "◇ Publish to channel",
        "btn_confirm_dm": "◇ Publish to private (Telegram picker)",
        "btn_confirm_all": "◇ Channel + private",
        "btn_cancel": "◇ Cancel draft",
        "btn_menu": "◇ Main menu",
        "btn_templates": "◇ Templates",
        "btn_save_template": "◇ Save template",
        "btn_pick_contact": "◇ Pick contact in Telegram",
        "btn_pick_cancel": "◇ Cancel recipient pick",
        "btn_lang_en": "English",
        "btn_lang_fa": "فارسی",
        "channel_none": "(not set — use /setchannel)",
    },
    "fa": {
        "access_denied": "دسترسی ندارید. این شناسهٔ عددی را به ادمین بدهید تا در <code>ADMIN_IDS</code> قرار بگیرد:\n<code>{uid}</code>",
        "choose_language": "<b>ButtonForge</b>\n\nChoose panel language / <b>زبان پنل را انتخاب کنید:</b>",
        "lang_saved": "زبان ذخیره شد.",
        "need_setchannel": "کانال <b>پیش‌فرض</b> خود را برای انتشار تنظیم کنید:\n<code>/setchannel @YourChannel</code>\n(یا آیدی عددی مثل <code>-100…</code>)\n\nربات باید در آن کانال <b>ادمین</b> با دسترسی <b>ارسال پیام</b> باشد.",
        "setchannel_usage": "استفاده: <code>/setchannel @نام_کانال</code>\nیا: <code>/setchannel -100xxxxxxxxxx</code>",
        "channel_set_ok": "کانال پیش‌فرض روی <code>{ch}</code> ذخیره شد.",
        "channel_invalid": "فرمت کانال درست نیست. از @نام یا -100… استفاده کنید.",
        "no_channel_set": "هنوز کانال پیش‌فرض ندارید. اول <code>/setchannel @…</code> بزنید.",
        "channel_post_failed": "ارسال به کانال ناموفق بود. ربات را ادمین کنید با «ارسال پیام».\nخطا: {err}",
        "channel_not_admin": "ربات اجازهٔ ارسال در آن کانال را ندارد (ادمین نیست یا حق ندارد). خطا: {err}",
        "draft_cleared": "پیش‌نویس پاک شد.",
        "pick_cancelled": "انتخاب گیرنده لغو شد.",
        "no_draft": "پیش‌نویسی آماده نیست. با <code>/post_text</code> یا <code>/post_photo</code> شروع کنید.",
        "no_preview_yet": "هنوز پیش‌نمایشی نیست. اول «پست متنی» یا «پست عکسی» را بزنید.",
        "save_template_first": "ابتدا پیش‌نمایش را بسازید، بعد «ذخیره قالب» را بزنید.",
        "template_name_prompt": "نام این قالب را در یک پیام جدا بفرستید:",
        "template_name_short": "نام قالب را واضح‌تر بفرستید.",
        "template_save_error": "خطا در ذخیره؛ دوباره «ذخیره قالب» را بزنید.",
        "template_saved": "قالب ذخیره شد. از «قالب‌ها» می‌توانید دوباره بارگذاری کنید.",
        "no_templates": "هنوز قالبی ذخیره نشده. بعد از پیش‌نمایش، «ذخیره قالب» را بزنید و نام بفرستید.",
        "pick_template": "یک قالب را برای بارگذاری در پیش‌نویس بزنید:",
        "tpl_not_found": "قالب پیدا نشد.",
        "tpl_btn_error": "خطا در دکمه‌های قالب.",
        "tpl_loaded": "قالب بارگذاری شد.",
        "pick_dm_intro": "برای ارسال <b>بدون فوروارد</b> به یک پیوی، دکمهٔ زیر را بزنید؛ تلگرام همان صفحهٔ انتخاب مخاطب خودش را باز می‌کند (نه داخل ربات).",
        "confirm_all_after_ch": "در <b>کانال</b> منتشر شد. اگر همان را برای یک <b>پیوی</b> هم می‌خواهید، با دکمهٔ زیر انتخاب مخاطب تلگرام را باز کنید؛ می‌توانید رد کنید («لغو انتخاب گیرنده»).",
        "posted_channel": "در کانال منتشر شد (پست عادی، بدون فوروارد).",
        "posted_dm_ok": "به آن پیوی به‌صورت مستقیم ارسال شد (بدون فوروارد).",
        "posted_dm_fail": "ارسال به آن پیوی ناموفق بود (مثلاً کاربر ربات را استارت نکرده).\nخطا: {err}",
        "pick_only_hint": "الان فقط «انتخاب مخاطب در تلگرام» یا «لغو انتخاب گیرنده».",
        "begin_text": "<b>ButtonForge</b> — پست <b>متنی</b>.\nمتن پست را بفرستید (متن ساده).\nمی‌توانید از دکمه‌های پایین یا کامندها استفاده کنید.",
        "begin_photo": "<b>ButtonForge</b> — پست <b>عکسی</b>.\nیک <b>عکس</b> بفرستید (نه فایل به‌صورت سند). کپشن روی همان عکس یا پیام بعد.",
        "await_keys_text": "الگوی دکمه‌ها را بفرستید یا <code>-</code> برای بدون دکمه.\nمثال:\n<code>خانه url:https://t.me/telegram style:primary | پشتیبانی url:https://t.me/support style:success</code>",
        "await_keys_photo": "الگوی دکمه‌ها را بفرستید یا <code>-</code> برای بدون دکمه.",
        "preview_text": "پیش‌نمایش پایین است — دکمه‌های پایین یا کامندها:\n<code>/confirm</code> · <code>/confirm_private</code> · <code>/confirm_all</code> · <code>/cancel</code>",
        "preview_photo": "پیش‌نمایش عکس — دکمه‌های پایین یا کامندها:\n<code>/confirm</code> · <code>/confirm_private</code> · <code>/confirm_all</code> · <code>/cancel</code>",
        "caption_from_photo": "کپشن از روی عکس گرفته شد. الگوی دکمه‌ها را بفرستید یا <code>-</code>.",
        "await_caption": "الان متن کپشن را بفرستید، یا <code>-</code> برای بدون کپشن.",
        "preview_ready_line": "پیش‌نمایش — دکمه‌های پایین یا کامندها:\n<code>/confirm</code> · <code>/confirm_private</code> · <code>/confirm_all</code> · <code>/cancel</code>",
        "help_block": "<b>ButtonForge</b> — راهنمای مدیر\n\n"
        "• <code>/post_text</code> — پست فقط متن\n"
        "• <code>/post_photo</code> — پست با عکس\n"
        "• <code>/confirm</code> — ارسال به <b>کانال پیش‌فرض شما</b> (بدون فوروارد)\n"
        "• <code>/confirm_private</code> — ارسال به پیوی که در <b>انتخابگر تلگرام</b> می‌زنید\n"
        "• <code>/confirm_all</code> — اول کانال، بعد پیوی اختیاری\n"
        "• <code>/cancel</code> — لغو پیش‌نویس\n"
        "• <code>/setchannel @…</code> — تنظیم <b>کانال پیش‌فرض شما</b>\n\n"
        "<b>کیبورد پایین</b> — همان کارها؛ کامندها فعال‌اند.\n"
        "<b>قالب‌ها</b> — ذخیره و بارگذاری دوباره.\n"
        "<b>به‌روزرسانی:</b> <code>bash update.sh</code>\n\n"
        "<b>دکمه‌های اینلاین:</b> هر خط یک ردیف؛ با <code>|</code> ستون.\n"
        "<code>عنوان url:…</code> | <code>عنوان cb:…</code> | <code>عنوان webapp:…</code>\n"
        "<b>رنگ دکمه:</b> <code>style:primary</code> / success / danger\n"
        "<i>رنگ hex دلخواه نیست.</i>\n\n"
        "<b>کانال پیش‌فرض شما:</b> <code>{channel}</code>",
        "btn_text_post": "◇ پست متنی",
        "btn_photo_post": "◇ پست عکسی",
        "btn_confirm_ch": "◇ ارسال به کانال",
        "btn_confirm_dm": "◇ ارسال به پیوی (انتخاب در تلگرام)",
        "btn_confirm_all": "◇ کانال و پیوی",
        "btn_cancel": "◇ لغو پیش‌نویس",
        "btn_menu": "◇ منوی اصلی",
        "btn_templates": "◇ قالب‌ها",
        "btn_save_template": "◇ ذخیره قالب",
        "btn_pick_contact": "◇ انتخاب مخاطب در تلگرام",
        "btn_pick_cancel": "◇ لغو انتخاب گیرنده",
        "btn_lang_en": "English",
        "btn_lang_fa": "فارسی",
        "channel_none": "(تنظیم نشده — /setchannel)",
    },
}

_BTN_KEYS = [
    ("text_post", "btn_text_post"),
    ("photo_post", "btn_photo_post"),
    ("confirm_ch", "btn_confirm_ch"),
    ("confirm_dm", "btn_confirm_dm"),
    ("confirm_all", "btn_confirm_all"),
    ("cancel", "btn_cancel"),
    ("menu", "btn_menu"),
    ("templates", "btn_templates"),
    ("save_template", "btn_save_template"),
    ("pick_contact", "btn_pick_contact"),
    ("pick_cancel", "btn_pick_cancel"),
]

_LABEL_TO_ACTION: dict[str, str] = {}
for _lng in ("en", "fa"):
    for _act, _sk in _BTN_KEYS:
        _LABEL_TO_ACTION[STRINGS[_lng][_sk]] = _act

ALL_MENU_LABELS: frozenset[str] = frozenset(_LABEL_TO_ACTION.keys())


def ui_lang(uid: int | None) -> str:
    """Language for UI; default English until user picks in onboarding."""
    if uid is None:
        return "en"
    import user_prefs

    v = user_prefs.get_lang(uid)
    return v if v in ("en", "fa") else "en"


def tr(uid: int | None, key: str, **kwargs: str) -> str:
    lang = ui_lang(uid)
    s = STRINGS[lang].get(key) or STRINGS["en"][key]
    return s.format(**kwargs) if kwargs else s


def menu_action_from_text(text: str) -> str | None:
    return _LABEL_TO_ACTION.get(text)
