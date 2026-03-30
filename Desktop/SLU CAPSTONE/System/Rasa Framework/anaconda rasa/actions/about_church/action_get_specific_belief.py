import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, StatementOfBelief

db = Database()


class ActionGetSpecificBelief(Action):

    def name(self) -> Text:
        return "action_get_specific_belief"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        user_msg = tracker.latest_message.get("text", "").lower()

        # Strip punctuation and remove stop words to isolate the topic keywords
        stop_words = {
            "does", "the", "church", "believe", "in", "do", "you", "abcmi",
            "what", "is", "about", "a", "an", "that", "this", "are", "of",
            "grace", "i", "it", "its", "can", "has", "have", "had", "and",
            "or", "not", "no", "yes", "be", "was", "were", "will", "would",
            "part", "your", "our", "their", "belief", "beliefs", "faith",
        }
        words = [w.strip("?.,!") for w in user_msg.split()]
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        statements = StatementOfBelief.get_all(db)
        if not statements:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the statement of belief right now."
            )
            return []

        # Find beliefs whose statement contains any of the topic keywords
        matched = [
            item for item in statements
            if any(kw in item["statement"].lower() for kw in keywords)
        ]

        if matched:
            if len(matched) == 1:
                dispatcher.utter_message(
                    text=f"Yes, the church believes in this:\n\n{matched[0]['statement']}"
                )
            else:
                lines = ["Yes, here are the related beliefs of the church:\n"]
                for item in matched:
                    lines.append(f"{item['item_number']}. {item['statement']}")
                dispatcher.utter_message(text="\n".join(lines))
        else:
            lines = [
                "I couldn't find a specific belief matching your question. "
                "Here are all of ABCMI's beliefs:\n"
            ]
            for item in statements:
                lines.append(f"{item['item_number']}. {item['statement']}")
            dispatcher.utter_message(text="\n".join(lines))

        return []
