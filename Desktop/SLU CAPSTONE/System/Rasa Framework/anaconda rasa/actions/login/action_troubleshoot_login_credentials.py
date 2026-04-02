from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_login_help_text


class ActionTroubleshootLoginCredentials(Action):
    def name(self) -> Text:
        return "action_troubleshoot_login_credentials"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_login_help_text("invalid_credentials"))
        return []
