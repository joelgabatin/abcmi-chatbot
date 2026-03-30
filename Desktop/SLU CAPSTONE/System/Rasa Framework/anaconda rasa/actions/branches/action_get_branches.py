import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchBranch

db = Database()


class ActionGetBranches(Action):
    """Multi-turn branch finder: region → branch → details"""

    def name(self) -> Text:
        return "action_get_branches"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        intent = tracker.latest_message.get("intent", {}).get("name")
        region_id = tracker.get_slot("selected_region_id")
        region_name = tracker.get_slot("selected_region_name")

        # Step 1: User asked about branches — list regions
        if intent == "ask_branches" or (not region_id):
            regions = ChurchBranch.get_all_regions(db)
            if regions:
                lines = ["Which region are you looking for? Here are our available regions:\n"]
                for i, r in enumerate(regions, 1):
                    lines.append(f"{i}. {r['name']}")
                lines.append("\nPlease type the region name or its number.")
                dispatcher.utter_message(text="\n".join(lines))
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the regions right now.")
            return []

        # Step 2: User selected a region — list its branches
        if intent == "select_region" and region_id and not tracker.get_slot("selected_branch_id"):
            branches = ChurchBranch.get_branches_by_region(db, int(region_id))
            if branches:
                lines = [f"Here are the branches in {region_name}:\n"]
                for i, b in enumerate(branches, 1):
                    lines.append(f"{i}. {b['name']} — {b['location']}")
                lines.append("\nWhich branch would you like to know more about?")
                dispatcher.utter_message(text="\n".join(lines))
            else:
                dispatcher.utter_message(text=f"Sorry, no active branches found in {region_name}.")
            return []

        dispatcher.utter_message(text="Please tell me which region you are looking for.")
        return []
