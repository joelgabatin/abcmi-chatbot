import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, Pastor

db = Database()


class ActionGetPastorsByRegion(Action):

    def name(self) -> Text:
        return "action_get_pastors_by_region"

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

        pastors = Pastor.get_by_region_name(db, region_name)
        if pastors:
            lines = [f"Here are the pastors serving in the {region_name.upper()} region ({len(pastors)} total):\n"]
            for i, p in enumerate(pastors, 1):
                branch_info = p.get("branches")
                branch_name = branch_info["name"] if branch_info else "Unknown Branch"
                lines.append(f"{i}. {p['name']} ({p['role']}) — {branch_name}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text=f"I couldn't find any pastors in the {region_name.upper()} region right now."
            )
        return []
