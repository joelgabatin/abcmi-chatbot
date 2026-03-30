import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchBranch

db = Database()


class ActionGetLocalBranches(Action):

    def name(self) -> Text:
        return "action_get_local_branches"

    def run(self, dispatcher, tracker, domain):
        db.connect()
        user_msg = tracker.latest_message.get("text", "").lower()
        local = ChurchBranch.get_local_branches(db)
        if local is not None:
            if "how many" in user_msg or "count" in user_msg or "total" in user_msg or "number" in user_msg:
                dispatcher.utter_message(text=f"ABCMI has {len(local)} local branch(es) across the Philippines.")
            else:
                lines = [f"Here are the local branches of ABCMI ({len(local)} total):\n"]
                for i, b in enumerate(local, 1):
                    lines.append(f"{i}. {b['name']} — {b['location']}")
                dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve local branch information right now.")
        return []
