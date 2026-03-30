import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, Pastor

db = Database()


class ActionGetAdministrativePastor(Action):

    def name(self) -> Text:
        return "action_get_administrative_pastor"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        pastors = Pastor.get_administrative_pastor(db)
        if pastors:
            if len(pastors) == 1:
                p = pastors[0]
                dispatcher.utter_message(
                    text=f"The {p['role']} of ABCMI is {p['name']}."
                )
            else:
                lines = ["The ABCMI Administrative Pastor(s) are:\n"]
                for p in pastors:
                    lines.append(f"- {p['name']} ({p['role']})")
                dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="I don't have an Administrative Pastor listed in our records right now."
            )
        return []
