#!/usr/bin/env python3
"""
Grace Church Chatbot - Custom Flask API Server with MySQL Backend
Bypasses Rasa's Windows tar extraction issues
Run with: python grace_api.py
Then access: http://localhost:8000/webhooks/rest/webhook
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from database import Database, ChurchInfo, ChurchHistory, StatementOfBelief

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database connection
db = Database()
db_connected = False

try:
    if db.connect():
        db_connected = True
        logger.info("✓ Database connected successfully")
    else:
        logger.warning("⚠ Database connection failed - using fallback responses")
except Exception as e:
    logger.warning(f"⚠ Database error: {e} - using fallback responses")

# Fallback responses if database is unavailable
FALLBACK_RESPONSES = {
    "utter_greet": "Welcome to Grace Church! I'm here to help. How are you doing today?",
    "utter_mission": "Our mission at Grace Church is to spread God's love, serve our community with compassion, and equip believers to grow in faith and make a positive impact in the world.",
    "utter_vision": "Our vision is to be a thriving community of faith where all people feel welcomed, valued, and empowered to live out their God-given purpose and transform the world with God's love.",
    "utter_goodbye": "Bye",
    "utter_iamabot": "I am a bot, powered by Rasa.",
    "utter_history": "Arise and Build For Christ Ministries (ABCMI) was founded in 1986 by Rev. Marino S. Coyoy and Elizabeth L. Coyoy as a house church in Quirino Hill. It has since grown into a thriving ministry with multiple church plants across the Philippines.",
    "utter_statement_of_belief": "ABCMI Church believes in the One True God, the Deity of Christ, the Scripture as Inspired by God, the Fall of Man and hope for Salvation, and more. Ask me for the full list!",
}

# Intent keywords for simple classification
INTENT_KEYWORDS = {
    "ask_mission": ["mission", "stand for", "aim", "accomplish", "goal"],
    "ask_vision": ["vision", "future", "dream", "where", "becoming"],
    "ask_history": ["history", "founded", "started", "background", "milestone", "years", "how old", "who founded", "began", "abcmi"],
    "ask_statement_of_belief": ["believe", "belief", "beliefs", "doctrine", "faith statement", "articles of faith", "core beliefs", "what do you stand for spiritually"],
    "goodbye": ["bye", "goodbye", "see you", "farewell", "exit", "quit"],
    "greet": ["hello", "hi", "hey", "greet", "start", "begin"],
}

def classify_intent(user_input):
    """Simple intent classification based on keywords"""
    user_input = user_input.lower()
    
    # Check each intent's keywords
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in user_input:
                return intent
    
    # Default to greeting if no match
    return "greet"

def get_response_for_intent(intent):
    """Map intent to response - fetches from database for mission/vision"""
    
    # Always try database first for mission/vision/history/beliefs
    if intent in ["ask_mission", "ask_vision", "ask_history", "ask_statement_of_belief"]:
        try:
            temp_db = Database()
            if temp_db.connect():
                if intent == "ask_mission":
                    mission = ChurchInfo.get_mission(temp_db)
                    if mission:
                        logger.info("✓ Mission fetched from database")
                        temp_db.disconnect()
                        return mission
                elif intent == "ask_vision":
                    vision = ChurchInfo.get_vision(temp_db)
                    if vision:
                        logger.info("✓ Vision fetched from database")
                        temp_db.disconnect()
                        return vision
                elif intent == "ask_history":
                    history = ChurchHistory.get_all(temp_db)
                    if history:
                        logger.info("✓ Church history fetched from database")
                        temp_db.disconnect()
                        lines = ["Here is the history of our church:\n"]
                        for item in history:
                            lines.append(f"• {item['year']}: {item['event']}")
                        return "\n".join(lines)
                elif intent == "ask_statement_of_belief":
                    statements = StatementOfBelief.get_all(temp_db)
                    if statements:
                        logger.info("✓ Statement of belief fetched from database")
                        temp_db.disconnect()
                        lines = ["Here is what ABCMI Church believes:\n"]
                        for item in statements:
                            lines.append(f"{item['item_number']}. {item['statement']}")
                        return "\n".join(lines)

                temp_db.disconnect()
            else:
                logger.warning(f"Could not connect to database - using fallback for {intent}")
        except Exception as e:
            logger.warning(f"Database error fetching {intent}: {e} - using fallback")

    # Fallback to hardcoded responses
    intent_to_response = {
        "greet": FALLBACK_RESPONSES["utter_greet"],
        "ask_mission": FALLBACK_RESPONSES["utter_mission"],
        "ask_vision": FALLBACK_RESPONSES["utter_vision"],
        "ask_history": FALLBACK_RESPONSES["utter_history"],
        "ask_statement_of_belief": FALLBACK_RESPONSES["utter_statement_of_belief"],
        "goodbye": FALLBACK_RESPONSES["utter_goodbye"],
    }
    return intent_to_response.get(intent, "I'm not sure how to respond to that. Could you rephrase?")

@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return "Hello from Rasa: 3.6.21"

@app.route("/webhooks/rest/webhook", methods=["POST"])
def webhook():
    """Main chatbot endpoint"""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        sender = data.get("sender", "user")
        
        if not user_message:
            return jsonify([]), 200
        
        logger.info(f"Message from {sender}: {user_message}")
        
        # Classify the intent
        intent = classify_intent(user_message)
        logger.info(f"Classified intent: {intent}")
        
        # Get response
        response_text = get_response_for_intent(intent)
        
        # Return Rasa-compatible format
        response = [{
            "recipient_id": sender,
            "text": response_text
        }]
        
        logger.info(f"Response: {response_text}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return jsonify([{
            "recipient_id": "user",
            "text": "Sorry, an error occurred. Please try again."
        }]), 500

@app.route("/webhooks/rest/webhook", methods=["GET"])
def webhook_get():
    """GET endpoint info"""
    return jsonify({"status": "ok", "message": "Grace Church Chatbot API"}), 200

@app.route("/model/parse", methods=["POST"])
def parse():
    """Alternative endpoint compatible with Rasa's parse endpoint"""
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"intent": {}, "entities": [], "text": ""}), 200
        
        intent = classify_intent(text)
        
        return jsonify({
            "intent": {"name": intent, "confidence": 0.98},
            "entities": [],
            "text": text
        }), 200
        
    except Exception as e:
        logger.error(f"Error parsing: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    db_status = "connected" if db_connected else "disconnected"
    return jsonify({
        "status": "ok",
        "api": "Grace Church Chatbot API",
        "database": db_status,
        "version": "1.0.0"
    }), 200

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close database connection on shutdown"""
    if db_connected:
        db.disconnect()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  ✝️  GRACE CHURCH CHATBOT API")
    print("="*70)
    print("\n✓ Starting Flask server...")
    print("✓ API will be available at: http://localhost:8000")
    print("✓ Webhook endpoint: http://localhost:8000/webhooks/rest/webhook")
    print("✓ Health check: http://localhost:8000/health")
    if db_connected:
        print("✓ Database: Connected")
    else:
        print("⚠ Database: Not connected (using fallback responses)")
    print("✓ Press Ctrl+C to stop\n")
    
    try:
        app.run(host="127.0.0.1", port=8000, debug=False)
    finally:
        if db_connected:
            db.disconnect()
