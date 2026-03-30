import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchHistory

db = Database()


class ActionGetHistory(Action):

    def name(self) -> Text:
        return "action_get_history"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        history = ChurchHistory.get_all(db)
        if history:
            lines = ["Here is the history of our church:\n"]
            for item in history:
                lines.append(f"• {item['year']}: {item['event']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the church history right now."
            )
        return []
