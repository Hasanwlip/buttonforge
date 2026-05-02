#!/usr/bin/env bash
# ButtonForge — به‌روزرسانی بدون نصب از اول (روی همان venv)
# Usage: bash update.sh
# نیاز: قبلاً install.sh زده باشید. اگر systemd دارید، سرویس را ریستارت می‌کند.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -d venv ]]; then
  echo "پوشهٔ venv نیست. یک بار bash install.sh را اجرا کنید."
  exit 1
fi

# shellcheck source=/dev/null
source venv/bin/activate
pip install -q -r requirements.txt

if systemctl is-active --quiet buttonforge.service 2>/dev/null; then
  sudo systemctl restart buttonforge.service
  echo "ربات ریستارت شد (buttonforge.service)."
else
  echo "سرویس systemd فعال نبود. اجرای دستی: bash run.sh"
fi

echo "به‌روزرسانی تمام شد."
