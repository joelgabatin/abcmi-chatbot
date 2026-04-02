from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_forgot_password_help_text


class ActionExplainPasswordRequirements(Action):
    def name(self) -> Text:
        return "action_explain_password_requirements"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_forgot_password_help_text("password_requirements"))
        return []
