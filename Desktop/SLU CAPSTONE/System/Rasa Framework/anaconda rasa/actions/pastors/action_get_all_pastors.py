import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, Pastor

db = Database()


class ActionGetAllPastors(Action):

    def name(self) -> Text:
        return "action_get_all_pastors"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        pastors = Pastor.get_all_with_branches(db)
        if pastors:
            lines = ["Here are the pastors of ABCMI Church:\n"]
            for p in pastors:
                branch = p.get("branches")
                branch_name = branch["name"] if branch else "Unassigned"
                lines.append(f"• {p['name']} ({p['role']}) — {branch_name}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the list of pastors right now."
            )
        return []
