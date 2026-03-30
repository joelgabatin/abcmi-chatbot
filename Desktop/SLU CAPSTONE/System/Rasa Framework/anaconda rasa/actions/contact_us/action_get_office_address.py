from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import SiteSettings, db


class ActionGetOfficeAddress(Action):
    def name(self) -> Text:
        return "action_get_office_address"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        office_address = SiteSettings.get_office_address(db)
        if office_address:
            dispatcher.utter_message(text=f"Our main office is located at {office_address}.")
        else:
            dispatcher.utter_message(response="utter_office_address")
        return []
