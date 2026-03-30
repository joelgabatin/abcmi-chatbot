import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from database import Database, Pastor, ChurchBranch

db = Database()


class ActionGetResidentPastorOfBranch(Action):

    def name(self) -> Text:
        return "action_get_resident_pastor_of_branch"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        branch_name = next(tracker.get_latest_entity_values("branch_name"), None)
        if not branch_name:
            dispatcher.utter_message(
                text="Could you please tell me the name of the branch you're asking about?"
            )
            return []

        branches = ChurchBranch.find_by_name(db, branch_name)
        if not branches:
            dispatcher.utter_message(
                text=f"I couldn't find a branch named '{branch_name}' in our records."
            )
            return []

        branch = branches[0]
        branch_id = branch["id"]
        branch_display = branch["name"]

        resident_pastors = Pastor.get_resident_pastor_by_branch(db, branch_id)
        if resident_pastors:
            if len(resident_pastors) == 1:
                p = resident_pastors[0]
                dispatcher.utter_message(
                    text=f"The resident pastor of {branch_display} is {p['name']} ({p['role']})."
                )
            else:
                names = ", ".join(f"{p['name']} ({p['role']})" for p in resident_pastors)
                dispatcher.utter_message(
                    text=f"The resident pastors of {branch_display} are: {names}."
                )
        else:
            dispatcher.utter_message(
                text=f"I don't have a resident pastor listed for the {branch_display} branch right now."
            )
        return [
            SlotSet("last_branch_id", float(branch_id)),
            SlotSet("last_branch_name", branch_display),
        ]
