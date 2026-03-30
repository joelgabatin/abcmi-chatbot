import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchFounders

db = Database()


class ActionGetChurchFounders(Action):

    def name(self) -> Text:
        return "action_get_church_founders"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        founders = ChurchFounders.get_all(db)
        if founders:
            if len(founders) == 1:
                f = founders[0]
                title = f.get("title") or ""
                name = f"{title} {f['name']}".strip()
                dispatcher.utter_message(
                    text=f"ABCMI was founded by {name} ({f['role']})."
                )
            else:
                names = []
                for f in founders:
                    title = f.get("title") or ""
                    name = f"{title} {f['name']}".strip()
                    names.append(f"{name} ({f['role']})")
                founders_str = " and ".join(names)
                dispatcher.utter_message(
                    text=f"ABCMI was founded by {founders_str}."
                )
        else:
            dispatcher.utter_message(
                text="I don't have information about the founders of ABCMI right now."
            )
        return []
