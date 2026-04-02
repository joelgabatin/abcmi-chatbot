from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_login_help_text, get_login_page_url


class ActionGetLoginSteps(Action):
    def name(self) -> Text:
        return "action_get_login_steps"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = get_login_help_text("steps")
        login_url = get_login_page_url()
        dispatcher.utter_message(text=f"{message}\n\nLogin page: {login_url}")
        return []
