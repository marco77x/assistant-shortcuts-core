# 🧠 Assistant Shortcuts Core

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/marco77x/assistant-shortcuts-core/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/marco77x/assistant-shortcuts-core?style=social)](https://github.com/marco77x/assistant-shortcuts-core/stargazers)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%2B%20iOS-black.svg)](#)
[![Apple Shortcuts](https://img.shields.io/badge/built%20for-Apple%20Shortcuts-blueviolet.svg)](#shortcut-links)

A minimal local server for Apple Shortcuts voice flows.

This project is the **Core mode**: stable, simple, and reproducible.

- No OpenClaw required
- No Ollama required
- Works with `Assistant Start Core` + `Assistant Loop Core`

## Core Flow

```text
iPhone/iPad (Siri) -> Assistant Start Core -> Assistant Loop Core -> POST /shortcut -> Assistant Core Server -> response -> spoken reply
```

## What It Does

- Receives user voice command text from Shortcuts
- Routes basic intents
- Returns a normalized JSON response (`action`, `text`, `reply`)
- Supports loop stop action (`shortcut_stop`)

## Supported Commands (Current)

- Studio light ON (IT/EN keywords)
- Studio light OFF (IT/EN keywords)
- Stop session (`stop`, `ferma`, `esci`, `fine`, `end`, `exit`)
- Fallback echo for unknown commands

## Shortcut Links

- Assistant Start Core: [iCloud link](https://www.icloud.com/shortcuts/82ba5029d74a453d8fc9d7769c14a37b)
- Assistant Loop Core: [iCloud link](https://www.icloud.com/shortcuts/ebd919028e764d1490197dd7a364b3a5)

## Prerequisites

- macOS (Mac mini recommended, always on)
- Python 3.11+
- iPhone/iPad with Apple Shortcuts

## Setup

### 1. Clone repository

```bash
git clone https://github.com/marco77x/assistant-shortcuts-core.git
cd assistant-shortcuts-core
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

### 5. Run server

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## API

### Health

```bash
curl http://127.0.0.1:8000/health
```

### Shortcut endpoint

```bash
curl -X POST http://127.0.0.1:8000/shortcut \
  -H "Content-Type: application/json" \
  -d '{"sender_id":"test","text":"turn off the light in studio"}'
```

Example response:

```json
{
  "ok": true,
  "action": "home.light_studio.off",
  "reply": "Spengo la luce in studio.",
  "text": "Spengo la luce in studio."
}
```

## Shortcut Configuration

In `Assistant Loop Core`, configure URL:

`http://<MAC_MINI_IP>:8000/shortcut`

Request body JSON:

```json
{
  "sender_id": "your-device-id",
  "text": "<Shortcut variable: Command>"
}
```

Read response keys:

1. `action` (loop/stop logic)
2. `text` (spoken reply)

## Project Structure

```text
assistant-shortcuts-core/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── requirements.txt
└── docs/
    └── publish-checklist.md
```

## Environment Variables

- `HOST` default `0.0.0.0`
- `PORT` default `8000`
- `ASSISTANT_TOKEN` optional shared secret in header `x-assistant-token`
- `LANGUAGE` `it` or `en`

## Security

⚠️ Never commit secrets.

- `.env` is gitignored
- Keep API keys/tokens out of the repository
- Use `.env.example` as template only

## Roadmap

- Add optional OpenClaw mode as advanced stack
- Add mail/calendar/notes/reminders actions
- Add structured intent parser (JSON-first)
- Add optional action adapters for local automations

## License

MIT — use it, modify it, share it.
