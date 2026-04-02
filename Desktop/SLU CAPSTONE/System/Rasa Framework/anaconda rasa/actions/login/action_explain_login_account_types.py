from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_login_help_text


class ActionExplainLoginAccountTypes(Action):
    def name(self) -> Text:
        return "action_explain_login_account_types"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_login_help_text("account_types"))
        return []
