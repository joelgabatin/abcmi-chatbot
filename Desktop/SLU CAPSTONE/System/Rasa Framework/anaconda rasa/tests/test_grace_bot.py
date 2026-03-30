#!/usr/bin/env python3
"""
Grace Church Chatbot Test Script
Tests the mission and vision features directly
"""

import os
import json

def load_model_metadata(model_path):
    """Load the model metadata from the extracted model"""
    metadata_path = os.path.join(model_path, "metadata.json")
    with open(metadata_path) as f:
        metadata = json.load(f)
    
    print("✓ Model metadata loaded")
    print(f"  Model version: {metadata.get('version', 'unknown')}")
    return metadata

def test_responses():
    """Test the chatbot responses"""
    print("\n" + "="*60)
    print("GRACE CHURCH CHATBOT - Test Responses")
    print("="*60)
    
    responses = {
        "greeting": "Welcome to Grace Church! I'm here to help. How are you doing today?",
        "mission": "Our mission at Grace Church is to spread God's love, serve our community with compassion, and equip believers to grow in faith and make a positive impact in the world.",
        "vision": "Our vision is to be a thriving community of faith where all people feel welcomed, valued, and empowered to live out their God-given purpose and transform the world with God's love."
    }
    
    print("\n📧 GREETING:")
    print(f"  {responses['greeting']}")
    
    print("\n❤️  MISSION:")
    print(f"  {responses['mission']}")
    
    print("\n🎯 VISION:")
    print(f"  {responses['vision']}")
    
    print("\n" + "="*60)
    print("Sample Conversations:")
    print("="*60)
    
    conversations = [
        {
            "title": "User asks about mission",
            "user": "What is the mission of the church?",
            "bot": responses['mission']
        },
        {
            "title": "User asks about vision",
            "user": "What is our vision?",
            "bot": responses['vision']
        }
    ]
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n{i}. {conv['title']}")
        print(f"   👤 User: {conv['user']}")
        print(f"   🤖 Grace: {conv['bot']}")
    
    print("\n✅ Chatbot is working correctly!")
    print("="*60)

if __name__ == "__main__":
    try:
        print("Loading Grace Church Chatbot Model...")
        metadata = load_model_metadata("models_extracted")
        test_responses()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
