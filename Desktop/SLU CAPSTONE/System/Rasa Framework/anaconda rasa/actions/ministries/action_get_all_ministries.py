import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, Ministry

db = Database()


class ActionGetAllMinistries(Action):

    def name(self) -> Text:
        return "action_get_all_ministries"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        ministries = Ministry.get_all(db)

        if not ministries:
            dispatcher.utter_message(text="I'm sorry, I couldn't retrieve the ministries right now. Please try again later.")
            return []

        lines = ["Here are the ministries of ABCMI:\n"]
        for i, m in enumerate(ministries, 1):
            lines.append(f"{i}. {m['name']}")

        lines.append("\nYou can ask me about a specific ministry, like \"What is the Youth Ministry?\" or \"How can I join the Music Ministry?\"")
        dispatcher.utter_message(text="\n".join(lines))
        return []
