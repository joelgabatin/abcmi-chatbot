import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchBranch

db = Database()


class ActionGetInternationalBranches(Action):

    def name(self) -> Text:
        return "action_get_international_branches"

    def run(self, dispatcher, tracker, domain):
        db.connect()
        user_msg = tracker.latest_message.get("text", "").lower()
        intl = ChurchBranch.get_international_branches(db)
        if intl is not None:
            if "how many" in user_msg or "count" in user_msg or "total" in user_msg or "number" in user_msg:
                dispatcher.utter_message(text=f"ABCMI has {len(intl)} international branch(es).")
            else:
                if not intl:
                    dispatcher.utter_message(text="There are currently no active international branches.")
                else:
                    lines = [f"Here are the international branches of ABCMI ({len(intl)} total):\n"]
                    for i, b in enumerate(intl, 1):
                        lines.append(f"{i}. {b['name']} — {b['location']}")
                    dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve international branch information right now.")
        return []
