import os

from dotenv import load_dotenv

load_dotenv()


def _truthy_env(name: str) -> bool:
    v = os.environ.get(name, "").strip().lower()
    return v in ("1", "true", "yes", "on")


BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("CHANNEL_ID", "").strip()
OPEN_ACCESS = _truthy_env("OPEN_ACCESS")
_raw_admins = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS = {
    int(x.strip())
    for x in _raw_admins.split(",")
    if x.strip().isdigit()
}


def validate() -> list[str]:
    errors: list[str] = []
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN is empty in .env")
    if not OPEN_ACCESS and not ADMIN_IDS:
        errors.append(
            "Set OPEN_ACCESS=1 for public mode, or add valid numeric ADMIN_IDS (comma-separated)."
        )
    return errors
