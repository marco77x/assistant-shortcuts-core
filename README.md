# Assistant Core Server

A minimal local server for Apple Shortcuts (`Assistant Start Core` + `Assistant Loop Core`).

This is the **core mode** (no OpenClaw, no Ollama required).

## What It Does

- Receives voice text from Shortcuts (`POST /shortcut`)
- Returns an action + a spoken response (`action`, `text`, `reply`)
- Handles basic commands (studio light on/off, stop session)
- Falls back with a simple response for unknown commands

## Shortcut Links

- Assistant Start Core: [iCloud link](https://www.icloud.com/shortcuts/82ba5029d74a453d8fc9d7769c14a37b)
- Assistant Loop Core: [iCloud link](https://www.icloud.com/shortcuts/ebd919028e764d1490197dd7a364b3a5)

## Requirements

- macOS (Mac mini recommended, always on)
- Python 3.11+
- iPhone/iPad with Apple Shortcuts

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## API

### Health

```bash
curl http://127.0.0.1:8000/health
```

### Shortcut Endpoint

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

## Environment

See `.env.example`:

- `HOST` default `0.0.0.0`
- `PORT` default `8000`
- `ASSISTANT_TOKEN` optional token for header `x-assistant-token`
- `LANGUAGE` `it` or `en`

## Shortcut Configuration

In `Assistant Loop Core` set URL to:

`http://<MAC_MINI_IP>:8000/shortcut`

Body JSON:

```json
{
  "sender_id": "your-device-id",
  "text": "<Shortcut variable: Command>"
}
```

Read and speak these response keys:

1. `action` (for stop logic)
2. `text` (spoken response)

## Notes

- This server does **not** directly control HomeKit accessories by API.
- It is designed as a stable core contract for your shortcut flow.
- You can add an OpenClaw mode later as a separate advanced stack.
