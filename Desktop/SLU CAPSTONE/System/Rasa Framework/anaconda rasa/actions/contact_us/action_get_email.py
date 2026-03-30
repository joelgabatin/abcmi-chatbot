from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import SiteSettings, db


class ActionGetEmail(Action):
    def name(self) -> Text:
        return "action_get_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = SiteSettings.get_email(db)
        if email:
            dispatcher.utter_message(text=f"You can reach us via email at {email}.")
        else:
            dispatcher.utter_message(response="utter_email")
        return []
