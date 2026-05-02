#!/usr/bin/env bash
# ButtonForge — Ubuntu/Debian auto-installer
# Usage: bash install.sh
# This file must use Unix line endings (LF only). If bash says $'\r' or pipefail is invalid, run on the server:
#   sed -i 's/\r$//' install.sh && bash install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if command -v tput >/dev/null 2>&1 && [[ -t 1 ]]; then
  B="$(tput bold)"
  C="$(tput setaf 6)"
  G="$(tput setaf 2)"
  Y="$(tput setaf 3)"
  M="$(tput setaf 5)"
  R="$(tput sgr0)"
else
  B="" C="" G="" Y="" M="" R=""
fi

clear

# Distinctive “icon” banner (terminal-safe UTF-8 box + chip motif)
printf '\n'
printf '%b' "${C}${B}"
cat <<'LOGO'
      ╭────────────────────────────╮
     ╱   ◇────────────────◇       ╲
    │  ■■■  B U T T O N   ■■■  │  ← forge
    │      F O R G E            │
     ╲   ───  · · ·  ───        ╱
      ╰────────────────────────────╯
LOGO
printf '%b\n\n' "${R}${G}  Telegram bot — inline keyboards, direct channel posts${R}"
printf '%b\n\n' "${M}  ▸ Installer${R}"

echo "==> Updating packages and installing Python …"
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip

prompt_env() {
  local overwrite="n"
  if [[ -f .env ]]; then
    read -r -p ".env already exists. Overwrite? [y/N]: " overwrite || true
    if [[ ! "${overwrite,,}" =~ ^y(es)?$ ]]; then
      echo "==> Keeping existing .env"
      return 0
    fi
  fi

  echo ""
  printf '%b\n' "${Y}Create .env (stored as plain text in this folder).${R}"
  echo ""

  local BOT_TOKEN="" ADMIN_IDS="" CHANNEL_ID="" OPEN_ACCESS="0" access_choice=""

  printf '%b' "Telegram BOT_TOKEN from @BotFather ${C}(hidden while typing)${R}: "
  read -rs BOT_TOKEN
  echo ""
  while [[ -z "${BOT_TOKEN// }" ]]; do
    printf '%b' "BOT_TOKEN cannot be empty. Retry: "
    read -rs BOT_TOKEN
    echo ""
  done

  echo ""
  printf '%b\n' "${Y}Who can use the bot panel?${R}"
  echo "  1) Open — anyone with the bot can use it (no ADMIN_IDS required)"
  echo "  2) Admin-only — only the numeric Telegram user IDs you list"
  read -r -p "Choose 1 or 2 [default: 2]: " access_choice || true
  access_choice="${access_choice// /}"
  access_choice="${access_choice:-2}"
  if [[ "${access_choice}" == "1" ]]; then
    OPEN_ACCESS="1"
    ADMIN_IDS=""
    printf '%b\n' "${Y}Open mode: any user can compose and send (to channels where the bot is allowed).${R}"
  else
    OPEN_ACCESS="0"
    read -r -p "ADMIN_IDS (comma-separated numeric user IDs, e.g. 123,456): " ADMIN_IDS
    while [[ -z "${ADMIN_IDS// }" ]]; do
      read -r -p "ADMIN_IDS cannot be empty in admin-only mode. Retry: " ADMIN_IDS
    done
  fi

  read -r -p "CHANNEL_ID optional legacy default (press Enter to skip; each user sets /setchannel): " CHANNEL_ID || true

  {
    printf '%s\n' "BOT_TOKEN=${BOT_TOKEN}"
    printf '%s\n' "OPEN_ACCESS=${OPEN_ACCESS}"
    printf '%s\n' "ADMIN_IDS=${ADMIN_IDS}"
    printf '%s\n' "CHANNEL_ID=${CHANNEL_ID:-}"
  } > .env

  echo ""
  printf '%b\n' "${G}==> Wrote ${SCRIPT_DIR}/.env${R}"
}

prompt_env

echo "==> Creating Python virtual environment …"
python3 -m venv venv
# shellcheck source=/dev/null
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

optional_systemd() {
  echo ""
  read -r -p "Install systemd service (background + start on boot)? [y/N]: " sysd || true
  if [[ ! "${sysd,,}" =~ ^y(es)?$ ]]; then
    echo "==> Skipping systemd. Foreground: bash ${SCRIPT_DIR}/run.sh"
    return 0
  fi

  if [[ ${EUID:-0} -eq 0 && -z "${SUDO_USER:-}" ]]; then
    printf '%b\n' "${Y}Warning: you are root without SUDO_USER. Prefer: your normal user + sudo only for apt/systemctl.${R}"
  fi

  local RUN_AS="${SUDO_USER:-$USER}"
  local UNIT_PATH="/etc/systemd/system/buttonforge.service"
  local PY="${SCRIPT_DIR}/venv/bin/python"
  local BOT="${SCRIPT_DIR}/bot.py"

  if [[ ! -x "$PY" ]]; then
    echo "ERROR: venv python missing at $PY"
    return 1
  fi

  printf '%b\n' "${G}==> Installing ${UNIT_PATH} (runs as user: ${RUN_AS})${R}"

  sudo tee "$UNIT_PATH" >/dev/null <<UNIT
[Unit]
Description=ButtonForge Telegram bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${RUN_AS}
WorkingDirectory=${SCRIPT_DIR}
Environment=PYTHONUNBUFFERED=1
ExecStart=${PY} ${BOT}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

  sudo systemctl daemon-reload
  sudo systemctl enable buttonforge.service
  sudo systemctl restart buttonforge.service

  printf '%b\n' "${G}==> systemd: buttonforge.service enabled and started.${R}"
  echo "  Status:  sudo systemctl status buttonforge.service"
  echo "  Logs:    sudo journalctl -u buttonforge.service -f"
  echo "  Stop:    sudo systemctl stop buttonforge.service"
  echo "  Disable: sudo systemctl disable buttonforge.service"
}

optional_systemd

printf '\n%b\n' "${B}${G}ButtonForge install complete.${R}"
echo "Foreground (no systemd): bash ${SCRIPT_DIR}/run.sh"
echo "Later updates (no full reinstall): bash ${SCRIPT_DIR}/update.sh"
echo "Template unit (paths not filled): ${SCRIPT_DIR}/telegram-bot.service.example"
