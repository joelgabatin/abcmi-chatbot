import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchBranch

db = Database()


class ActionGetBranchesByRegion(Action):

    def name(self) -> Text:
        return "action_get_branches_by_region"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        region_name = next(tracker.get_latest_entity_values("region_name"), None)
        if not region_name:
            dispatcher.utter_message(
                text="Could you please tell me which region you're asking about? (e.g., CAR, Metro Manila)"
            )
            return []

        branches = ChurchBranch.get_branches_by_region_name(db, region_name)
        if branches:
            lines = [f"Here are the ABCMI branches in {region_name.upper()} ({len(branches)} total):\n"]
            for i, b in enumerate(branches, 1):
                lines.append(f"{i}. {b['name']} — {b['location']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text=f"I couldn't find any branches in the {region_name.upper()} region right now."
            )
        return []
