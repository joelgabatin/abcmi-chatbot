from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import SiteSettings, db


class ActionGetPhoneNumber(Action):
    def name(self) -> Text:
        return "action_get_phone_number"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone_number = SiteSettings.get_phone_number(db)
        if phone_number:
            dispatcher.utter_message(text=f"Our phone number is {phone_number}.")
        else:
            dispatcher.utter_message(response="utter_phone_number")
        return []
