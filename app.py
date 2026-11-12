import os
import time
import hmac
from collections import deque
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

app = Flask(__name__)
recent = deque()
SYSTEM = "You are J.A.R.V.I.S., a helpful, concise and courteous personal assistant. Speak in a calm, natural British style. Never pretend to control devices or access data without tools."

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.post("/api/chat")
def chat():
    pin = os.environ.get("JARVIS_ACCESS_PIN", "")
    if not pin:
        return jsonify(error="Set JARVIS_ACCESS_PIN in your server environment."), 503
    if not hmac.compare_digest(request.headers.get("X-Jarvis-Pin", ""), pin):
        return jsonify(error="Incorrect access PIN."), 401
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return jsonify(error="Set OPENAI_API_KEY in your server environment."), 503
    now = time.monotonic()
    while recent and now - recent[0] > 3600:
        recent.popleft()
    if len(recent) >= 60:
        return jsonify(error="Hourly safety limit reached. Try later."), 429
    data = request.get_json(silent=True) or {}
    message = data.get("message")
    if not isinstance(message, str) or not message.strip() or len(message) > 1500:
        return jsonify(error="Message must be 1–1500 characters."), 400
    messages = [{"role": "system", "content": SYSTEM}]
    history = data.get("history", [])
    if isinstance(history, list):
        for item in history[-12:]:
            if isinstance(item, dict) and item.get("role") in ("user", "assistant") and isinstance(item.get("content"), str):
                messages.append({"role": item["role"], "content": item["content"][:1500]})
    messages.append({"role": "user", "content": message})
    recent.append(now)
    try:
        result = OpenAI(api_key=key, timeout=25).chat.completions.create(
            model=os.environ.get("JARVIS_MODEL", "gpt-4o-mini"),
            messages=messages,
            max_tokens=350,
        )
        return jsonify(reply=result.choices[0].message.content or "I have no reply yet.")
    except Exception:
        app.logger.exception("AI request failed")
        return jsonify(error="AI request failed. Check server logs, API key and credits."), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
