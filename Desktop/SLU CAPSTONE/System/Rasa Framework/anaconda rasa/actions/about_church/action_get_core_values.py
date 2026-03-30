import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchCoreValues

db = Database()


class ActionGetCoreValues(Action):

    def name(self) -> Text:
        return "action_get_core_values"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        core_values = ChurchCoreValues.get_all(db)
        if core_values:
            lines = ["Here are the core values of ABCMI Church:\n"]
            for i, item in enumerate(core_values, 1):
                lines.append(f"{i}. {item['title']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the core values right now."
            )
        return []
