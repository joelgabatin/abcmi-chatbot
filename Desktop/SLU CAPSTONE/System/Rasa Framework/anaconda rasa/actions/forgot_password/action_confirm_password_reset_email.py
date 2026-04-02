from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_forgot_password_help_text


class ActionConfirmPasswordResetEmail(Action):
    def name(self) -> Text:
        return "action_confirm_password_reset_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_forgot_password_help_text("reset_email_sent"))
        return []
