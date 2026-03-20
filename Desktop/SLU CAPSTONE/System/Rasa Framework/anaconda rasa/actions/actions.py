import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, SiteSettings

db = Database()


class ActionGetMission(Action):

    def name(self) -> Text:
        return "action_get_mission"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        mission = SiteSettings.get_mission(db)
        if mission:
            dispatcher.utter_message(text=f"Our mission: {mission}")
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the mission right now."
            )
        return []


class ActionGetVision(Action):

    def name(self) -> Text:
        return "action_get_vision"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        vision = SiteSettings.get_vision(db)
        if vision:
            dispatcher.utter_message(text=f"Our vision: {vision}")
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the vision right now."
            )
        return []
