import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

# Keyword groups → suggestion text shown to the user
SUGGESTIONS = [
    {
        "keywords": ["found", "founder", "foundress", "founding", "established", "started"],
        "suggestion": "Did you mean: 'Who founded ABCMI?'",
    },
    {
        "keywords": ["senior pastor", "overseer", "head pastor", "head of abcmi", "leads abcmi"],
        "suggestion": "Did you mean: 'Who is the Senior Pastor / ABCMI Overseer?'",
    },
    {
        "keywords": ["administrative pastor", "admin pastor", "administrator"],
        "suggestion": "Did you mean: 'Who is the ABCMI Administrative Pastor?'",
    },
    {
        "keywords": ["resident pastor", "pastor of branch", "pastor of the branch"],
        "suggestion": "Did you mean: 'Who is the resident pastor of [branch name]?'",
    },
    {
        "keywords": ["main branch", "headquarters", "head branch", "mother church", "central branch"],
        "suggestion": "Did you mean: 'What is the main branch of ABCMI?'",
    },
    {
        "keywords": ["pastor", "pastors", "who leads", "who serves"],
        "suggestion": "Did you mean: 'Who are the pastors of ABCMI?' or 'Who are the pastors in [region]?'",
    },
    {
        "keywords": ["branch", "branches", "location", "located", "region"],
        "suggestion": "Did you mean: 'What are the branches of ABCMI?' or 'What are the branches in [region]?'",
    },
    {
        "keywords": ["mission"],
        "suggestion": "Did you mean: 'What is the mission of ABCMI?'",
    },
    {
        "keywords": ["vision"],
        "suggestion": "Did you mean: 'What is the vision of ABCMI?'",
    },
    {
        "keywords": ["history", "started", "began", "when was"],
        "suggestion": "Did you mean: 'What is the history of ABCMI?'",
    },
    {
        "keywords": ["belief", "believe", "doctrine", "faith", "statement"],
        "suggestion": "Did you mean: 'What is the statement of belief of ABCMI?'",
    },
    {
        "keywords": ["core value", "values"],
        "suggestion": "Did you mean: 'What are the core values of ABCMI?'",
    },
    {
        "keywords": ["driving force"],
        "suggestion": "Did you mean: 'What is the driving force of ABCMI?'",
    },
]


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message = tracker.latest_message.get("text", "").lower()

        for group in SUGGESTIONS:
            if any(kw in message for kw in group["keywords"]):
                dispatcher.utter_message(
                    text=f"I'm not quite sure what you mean . {group['suggestion']}"
                )
                return [UserUtteranceReverted()]

        # Generic fallback if no keyword matched
        dispatcher.utter_message(
            text=(
                "I'm sorry, I didn't understand that. You can ask me about:\n"
                "- Pastors (senior pastor, administrative pastor, pastor by branch or region)\n"
                "- Branches (main branch, branches by region, branch location, branch service schedule)\n"
                "- Church identity (mission, vision, history, beliefs, core values)\n"
                "- Founders of ABCMI"
            )
        )
        return [UserUtteranceReverted()]
