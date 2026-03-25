#!/usr/bin/env python3
"""
grace_api.py — Flask entry point for the Grace Church Chatbot API.

All business logic lives in the api/ package:
  api/constants.py        — fallback responses, intent keywords
  api/classifier.py       — keyword-based intent classifier
  api/branch_flow.py      — multi-turn branch-finder conversation
  api/intent_responses.py — maps intents to database responses
  api/state_manager.py    — per-sender conversation state + message router

Database credentials are in config.py.
Database models are in database.py.

Run:  python grace_api.py
"""

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from api.state_manager import handle_message

# ── App setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify DB connectivity at startup (informational only — API still runs without it)
db_connected = False
try:
    _db = Database()
    if _db.connect():
        db_connected = True
        _db.disconnect()
        logger.info("✓ Database connected successfully")
    else:
        logger.warning("⚠ Database connection failed — using fallback responses")
except Exception as e:
    logger.warning(f"⚠ Database error at startup: {e}")


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def root():
    return "Hello from Rasa: 3.6.21"


@app.route("/webhooks/rest/webhook", methods=["POST"])
def webhook():
    """Main chatbot endpoint — accepts {sender, message} and returns [{text}]."""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        sender = data.get("sender", "user")

        if not user_message:
            return jsonify([]), 200

        logger.info(f"[webhook] {sender}: {user_message}")
        response_text = handle_message(sender, user_message)
        logger.info(f"[webhook] response: {response_text[:80]}...")

        return jsonify([{"recipient_id": sender, "text": response_text}]), 200

    except Exception as e:
        logger.error(f"[webhook] Unhandled error: {e}", exc_info=True)
        return jsonify([{
            "recipient_id": "user",
            "text": "Sorry, an error occurred. Please try again.",
        }]), 500


@app.route("/webhooks/rest/webhook", methods=["GET"])
def webhook_info():
    return jsonify({"status": "ok", "message": "Grace Church Chatbot API"}), 200


@app.route("/model/parse", methods=["POST"])
def parse():
    """Rasa-compatible parse endpoint."""
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"intent": {}, "entities": [], "text": ""}), 200
        from api.classifier import classify_intent
        intent = classify_intent(text)
        return jsonify({"intent": {"name": intent, "confidence": 0.98}, "entities": [], "text": text}), 200
    except Exception as e:
        logger.error(f"[parse] Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "api": "Grace Church Chatbot API",
        "database": "connected" if db_connected else "disconnected",
        "version": "1.0.0",
    }), 200


# ── Startup ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  ✝️  GRACE CHURCH CHATBOT API")
    print("=" * 70)
    print("✓ http://localhost:8000")
    print("✓ Webhook: http://localhost:8000/webhooks/rest/webhook")
    print("✓ Health:  http://localhost:8000/health")
    print(f"{'✓' if db_connected else '⚠'} Database: {'Connected' if db_connected else 'Not connected (fallback active)'}")
    print("✓ Press Ctrl+C to stop\n")
    app.run(host="127.0.0.1", port=8000, debug=False)
