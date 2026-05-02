<div align="center">

```
      ╭────────────────────────────╮
     ╱   ◇────────────────◇       ╲
    │  ■■■  B U T T O N   ■■■  │  ← forge
    │      F O R G E            │
     ╲   ───  · · ·  ───        ╱
      ╰────────────────────────────╯
```

# **ButtonForge**

*Forge the keyboard. Drop the post. No forward games.*

**Telegram · inline keys · channel · DM · templates**

[BotFather](https://t.me/BotFather) token + one install. You run the show.

</div>

---

## What it is

Channel-grade **button builder** on Telegram: text or photo, **your** rows of URL / callback / Mini App keys, then **native** send — straight to the channel or into a hand-picked private chat. Templates remember the heat. Installer + optional systemd for servers that never sleep.

**Per-user channel · EN/FA panel · lock it to your IDs or open the floor** — config lives in `.env`; details in `.env.example`.

---

## Run it

**Linux (the script way):**

```bash
sed -i 's/\r$//' install.sh run.sh update.sh   # if you copied from Windows
bash install.sh
bash run.sh
```

**Elsewhere:** `python3 -m venv venv` → activate → `pip install -r requirements.txt` → `python bot.py` with `.env` set.

Updates without drama: `bash update.sh`.

---

## Under the hood

Python · **python-telegram-bot** 22.x · dotenv. That’s the stack.

---

## Files worth knowing

`bot.py` · `admin_menu.py` · `keyboard_parser.py` · `templates_store.py` · `config.py` · `install.sh` · `run.sh` · `update.sh`

---

<div align="center">

**ButtonForge** — *buttons first. noise never.*

◇ · ■ · ◇

</div>
