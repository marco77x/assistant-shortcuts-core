import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
ASSISTANT_TOKEN = os.getenv("ASSISTANT_TOKEN", "").strip()
LANGUAGE = os.getenv("LANGUAGE", "it").strip().lower()

app = FastAPI(title="Assistant Core Server", version="1.0.0")


class ShortcutRequest(BaseModel):
    text: str
    sender_id: Optional[str] = None


def _reply(it: str, en: str) -> str:
    return it if LANGUAGE == "it" else en


def _payload(action: str, message: str) -> dict:
    # reply + text to stay compatible with different Shortcut variants
    return {"ok": True, "action": action, "reply": message, "text": message}


def _authorize(token: Optional[str]) -> None:
    if ASSISTANT_TOKEN and token != ASSISTANT_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


def route_command(text: str) -> dict:
    t = text.lower().strip()

    wants_studio_light = "studio" in t and any(k in t for k in {"luce", "light", "lamp"})
    turn_on_words = {"accendi", "attiva", "turn on", "switch on"}
    turn_off_words = {"spegni", "disattiva", "turn off", "switch off"}

    if wants_studio_light and any(k in t for k in turn_on_words):
        return _payload(
            "home.light_studio.on",
            _reply("Accendo la luce in studio.", "Turning on the studio light."),
        )

    if wants_studio_light and any(k in t for k in turn_off_words):
        return _payload(
            "home.light_studio.off",
            _reply("Spengo la luce in studio.", "Turning off the studio light."),
        )

    if t in {"stop", "ferma", "esci", "fine", "end", "exit"}:
        return _payload("shortcut_stop", _reply("Sessione terminata.", "Session ended."))

    return _payload("qa.fallback", _reply(f"Hai detto: {text}", f"You said: {text}"))


@app.get("/health")
def health() -> dict:
    return {"ok": True, "service": "assistant-core-server", "host": HOST, "port": PORT}


@app.post("/assist")
def assist(payload: ShortcutRequest, x_assistant_token: Optional[str] = Header(default=None)) -> dict:
    _authorize(x_assistant_token)
    return route_command(payload.text)


@app.post("/shortcut")
def shortcut(payload: ShortcutRequest, x_assistant_token: Optional[str] = Header(default=None)) -> dict:
    _authorize(x_assistant_token)
    return route_command(payload.text)
