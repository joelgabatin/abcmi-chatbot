import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from database import Database, Pastor

db = Database()


class ActionFindPastor(Action):

    def name(self) -> Text:
        return "action_find_pastor"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        pastor_name = next(tracker.get_latest_entity_values("pastor_name"), None)
        if not pastor_name:
            dispatcher.utter_message(
                text="Could you please tell me the name of the pastor you're looking for?"
            )
            return []

        pastors = Pastor.find_by_name(db, pastor_name)
        if pastors:
            p = pastors[0]
            branch = p.get("branches")
            branch_name = branch["name"] if branch else "an ABCMI branch"
            branch_id = p.get("branch_id")
            dispatcher.utter_message(
                text=f"Yes! {p['name']} is one of our pastors. "
                     f"He/She serves as {p['role']} at {branch_name}."
            )
            return [
                SlotSet("last_pastor_name", p["name"]),
                SlotSet("last_branch_id", float(branch_id) if branch_id else None),
                SlotSet("last_branch_name", branch_name),
            ]
        else:
            dispatcher.utter_message(
                text=f"No, {pastor_name} is not listed as a pastor in our records."
            )
            return [
                SlotSet("last_pastor_name", None),
                SlotSet("last_branch_id", None),
                SlotSet("last_branch_name", None),
            ]
