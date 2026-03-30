from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import SiteSettings, db


class ActionGetOfficeHours(Action):
    def name(self) -> Text:
        return "action_get_office_hours"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        office_hours = SiteSettings.get_office_hours(db)
        if office_hours:
            dispatcher.utter_message(text=f"Our office hours are {office_hours}.")
        else:
            dispatcher.utter_message(response="utter_office_hours")
        return []
