import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from database import Database, ChurchBranch
from .utils import _clean_branch_name

db = Database()


class ActionGetBranchLocation(Action):
    """Return the location of a specifically named branch."""

    def name(self) -> Text:
        return "action_get_branch_location"

    def run(self, dispatcher, tracker, domain):
        db.connect()
        raw_entity = next(tracker.get_latest_entity_values("branch_name"), None)
        if not raw_entity:
            dispatcher.utter_message(
                text="Could you please tell me the name of the branch you're looking for?"
            )
            return []

        branch_name = _clean_branch_name(raw_entity)
        branches = ChurchBranch.find_by_name(db, branch_name)
        if not branches:
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find a branch named '{branch_name}' in our records."
            )
            return []

        branch = branches[0]
        location = branch.get("location") or "Location not available"
        dispatcher.utter_message(
            text=f"The {branch['name']} is located at: {location}"
        )
        return [SlotSet("last_branch_id", float(branch["id"])), SlotSet("last_branch_name", branch["name"])]
