#!/usr/bin/env python3
"""
Grace Church Chatbot - Interactive Chat Interface
Run with: python run_grace_chatbot.py
"""

import json
import os

# Hardcoded responses (you can extend this)
RESPONSES = {
    "utter_greet": "Welcome to Grace Church! I'm here to help. How are you doing today?",
    "utter_mission": "Our mission at Grace Church is to spread God's love, serve our community with compassion, and equip believers to grow in faith and make a positive impact in the world.",
    "utter_vision": "Our vision is to be a thriving community of faith where all people feel welcomed, valued, and empowered to live out their God-given purpose and transform the world with God's love.",
    "utter_goodbye": "Bye",
    "utter_iamabot": "I am a bot, powered by Rasa.",
}

# Intent keywords
INTENTS = {
    "ask_mission": ["mission", "stand for", "aim"],
    "ask_vision": ["vision", "future", "goal"],
    "goodbye": ["bye", "goodbye", "see you", "farewell"],
    "greet": ["hello", "hi", "hey", "greet"],
}

def classify_intent(user_input):
    """Simple intent classification based on keywords"""
    user_input = user_input.lower()
    
    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in user_input:
                return intent
    return None

def get_response(intent):
    """Get response for intent"""
    response_map = {
        "greet": RESPONSES["utter_greet"],
        "ask_mission": RESPONSES["utter_mission"],
        "ask_vision": RESPONSES["utter_vision"],
        "goodbye": RESPONSES["utter_goodbye"],
    }
    return response_map.get(intent, "I'm not sure what you mean. Could you rephrase that?")

def print_header():
    """Print welcome header"""
    print("\n" + "="*70)
    print("  ✝️  GRACE CHURCH CHATBOT - Interactive Chat")
    print("="*70)
    print("Welcome! I'm Grace, your church assistant.")
    print("You can ask me about our mission, vision, and more.")
    print("Type 'bye' to exit.\n")

def main():
    """Main chat loop"""
    print_header()
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["bye", "goodbye", "exit", "quit"]:
            print("Grace: " + RESPONSES["utter_goodbye"])
            print("\nThank you for chatting with Grace! God bless you! 🙏")
            break
        
        intent = classify_intent(user_input)
        response = get_response(intent)
        
        print(f"Grace: {response}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGrace: Thank you for chatting! God bless you! 🙏")
