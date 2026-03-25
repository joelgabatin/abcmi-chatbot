"""
api/classifier.py
Simple keyword-based intent classifier with regex for specific pastor queries.
"""

import re
from api.constants import INTENT_KEYWORDS

# Matches "is [name] your/a/our pastor", "is [name] pastoring", "does [name] pastor"
_SPECIFIC_PASTOR_RE = re.compile(
    r'\bis\s+\S[\w\s]*\s+(?:your|a|an|our|the)\s+pastor\b'
    r'|\bis\s+\S[\w\s]*\s+pastoring\b'
    r'|\bdoes\s+\S[\w\s]*\s+pastor\b',
    re.IGNORECASE,
)


def classify_intent(user_input: str) -> str:
    """
    Return the first matching intent for the given user input.
    Regex check for specific pastor queries runs before keyword matching.
    Falls back to 'greet' if nothing matches.
    """
    text = user_input.lower()

    # Regex-based check for "is [name] your pastor?" style queries
    if _SPECIFIC_PASTOR_RE.search(text):
        return "ask_specific_pastor"

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return intent
    return "greet"
