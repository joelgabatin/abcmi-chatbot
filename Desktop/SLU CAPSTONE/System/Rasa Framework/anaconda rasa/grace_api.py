#!/usr/bin/env python3
"""
grace_api.py — Flask gateway for the Grace Church Chatbot.

Proxies all chat requests to the Rasa server (RASA_URL).
Rasa handles intent classification (NLU) and responses (custom actions).

Run (3 terminals):
  Terminal 1: rasa run --enable-api --cors "*"   # Rasa on :5005
  Terminal 2: rasa run actions                    # Action server on :5055
  Terminal 3: python grace_api.py                 # This gateway on :8000
"""

import re
import os
import logging
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

RASA_URL = "http://localhost:5005"

# Sender ID: only alphanumeric, hyphens, underscores — max 64 chars
_SENDER_RE = re.compile(r'^[\w\-]{1,64}$')

# Max message length forwarded to Rasa
_MAX_MESSAGE_LEN = 500

app = Flask(__name__)
CORS(app, origins=["http://localhost:8000", "http://127.0.0.1:8000"])

# Reject bodies larger than 16 KB
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting — 60 requests/minute per IP, 500/hour per IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per hour", "60 per minute"],
    headers_enabled=True,
)


# ── Security headers ──────────────────────────────────────────────────────────

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


# ── Input helpers ─────────────────────────────────────────────────────────────

def _sanitize_message(text: str) -> str | None:
    """
    Strip control characters and null bytes.
    Returns None if the result is empty or exceeds the length limit.
    """
    # Remove null bytes and non-printable control characters (keep newlines/tabs)
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text).strip()
    if not cleaned or len(cleaned) > _MAX_MESSAGE_LEN:
        return None
    return cleaned


def _sanitize_sender(sender: str) -> str:
    """Return sender as-is if valid, else fall back to 'user'."""
    if isinstance(sender, str) and _SENDER_RE.match(sender):
        return sender
    return "user"


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def root():
    return "Grace Church Chatbot — Flask gateway (Rasa backend)"


@app.route("/chat", methods=["GET"])
def chat_ui():
    """Serve the chatbot frontend from the frontend/ directory."""
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    return send_from_directory(frontend_dir, "grace_chatbot.html")


@app.route("/webhooks/rest/webhook", methods=["POST"])
@limiter.limit("30 per minute")
def webhook():
    """Forward chat messages to Rasa and return its response."""

    # Enforce JSON Content-Type
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        data = request.get_json(silent=True) or {}
        raw_message = data.get("message", "")
        raw_sender  = data.get("sender", "user")

        user_message = _sanitize_message(str(raw_message))
        sender       = _sanitize_sender(str(raw_sender))

        if not user_message:
            return jsonify([]), 200

        logger.info(f"[webhook] {sender}: {user_message[:80]}")

        rasa_response = requests.post(
            f"{RASA_URL}/webhooks/rest/webhook",
            json={"sender": sender, "message": user_message},
            timeout=10,
        )
        rasa_response.raise_for_status()
        messages = rasa_response.json()

        logger.info(f"[webhook] Rasa returned {len(messages)} message(s)")
        return jsonify(messages), 200

    except requests.exceptions.ConnectionError:
        logger.error("[webhook] Could not connect to Rasa server")
        return jsonify([{
            "recipient_id": "user",
            "text": "The chatbot is currently unavailable. Please make sure the Rasa server is running.",
        }]), 503

    except Exception as e:
        logger.error(f"[webhook] Unhandled error: {e}", exc_info=True)
        return jsonify([{
            "recipient_id": "user",
            "text": "Sorry, an error occurred. Please try again.",
        }]), 500


@app.route("/webhooks/rest/webhook", methods=["GET"])
def webhook_info():
    return jsonify({"status": "ok", "message": "Grace Church Chatbot API"}), 200


@app.route("/health", methods=["GET"])
def health():
    rasa_status = "unreachable"
    try:
        r = requests.get(f"{RASA_URL}/", timeout=3)
        if r.status_code == 200:
            rasa_status = "ok"
    except Exception:
        pass

    return jsonify({
        "status": "ok",
        "gateway": "Grace Church Chatbot API",
        "rasa": rasa_status,
    }), 200


# ── Error handlers ────────────────────────────────────────────────────────────

@app.errorhandler(413)
def payload_too_large(_):
    return jsonify({"error": "Request payload too large"}), 413


@app.errorhandler(429)
def rate_limit_exceeded(_):
    return jsonify({"error": "Too many requests. Please slow down."}), 429


# ── Startup ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  GRACE CHURCH CHATBOT — Flask Gateway")
    print("=" * 70)
    print("  Gateway: http://localhost:8000")
    print("  Chat UI: http://localhost:8000/chat")
    print("  Webhook: http://localhost:8000/webhooks/rest/webhook")
    print("  Health:  http://localhost:8000/health")
    print()
    print("  Rasa must be running at:", RASA_URL)
    print("  -> rasa run --enable-api --cors \"*\"")
    print("  -> rasa run actions")
    print("=" * 70 + "\n")
    app.run(host="127.0.0.1", port=8000, debug=False)
