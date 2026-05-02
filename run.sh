#!/usr/bin/env bash
# ButtonForge — run from project root
set -euo pipefail
cd "$(dirname "$0")"
# shellcheck source=/dev/null
source venv/bin/activate
exec python bot.py
