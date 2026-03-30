import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, SiteSettings

db = Database()


class ActionGetDrivingForce(Action):

    def name(self) -> Text:
        return "action_get_driving_force"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        driving_force = SiteSettings.get_driving_force(db)
        if driving_force:
            dispatcher.utter_message(text=driving_force)
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the driving force right now."
            )
        return []
