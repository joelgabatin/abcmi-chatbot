import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from database import Database, ChurchBranch

db = Database()


class ActionGetMainBranch(Action):

    def name(self) -> Text:
        return "action_get_main_branch"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        branch = ChurchBranch.get_main_branch(db)
        if branch:
            location = branch.get("location") or "location not available"
            dispatcher.utter_message(
                text=f"The main branch of ABCMI is {branch['name']}, located at {location}."
            )
            return [
                SlotSet("last_branch_id", float(branch["id"])),
                SlotSet("last_branch_name", branch["name"]),
            ]
        else:
            dispatcher.utter_message(
                text="I'm sorry, I couldn't find the main branch information right now."
            )
            return []
