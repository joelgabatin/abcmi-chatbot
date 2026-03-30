import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, Pastor

db = Database()


class ActionGetPastorBranchSchedule(Action):

    def name(self) -> Text:
        return "action_get_pastor_branch_schedule"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        branch_id = tracker.get_slot("last_branch_id")
        branch_name = tracker.get_slot("last_branch_name")

        if not branch_id:
            dispatcher.utter_message(
                text="I don't have a branch in context yet. "
                     "Please first ask about a specific pastor so I know which branch to look up."
            )
            return []

        schedules = Pastor.get_branch_schedule(db, int(branch_id))
        if schedules:
            lines = [f"Here is the service schedule for {branch_name}:\n"]
            for s in schedules:
                desc = f" — {s['description']}" if s.get("description") else ""
                lines.append(f"• {s['day']} at {s['time']} ({s['type']}){desc}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find a service schedule for {branch_name} right now."
            )
        return []
