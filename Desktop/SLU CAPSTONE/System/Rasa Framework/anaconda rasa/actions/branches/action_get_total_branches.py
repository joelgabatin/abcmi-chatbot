import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchBranch

db = Database()


class ActionGetTotalBranches(Action):

    def name(self) -> Text:
        return "action_get_total_branches"

    def run(self, dispatcher, tracker, domain):
        db.connect()
        total = ChurchBranch.get_total_count(db)
        if total is not None:
            dispatcher.utter_message(text=f"ABCMI currently has {total} active branch(es) in total.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve the branch count right now.")
        return []
