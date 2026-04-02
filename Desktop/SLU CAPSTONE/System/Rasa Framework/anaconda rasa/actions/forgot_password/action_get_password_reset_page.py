from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_forgot_password_help_text, get_forgot_password_page_url


class ActionGetPasswordResetPage(Action):
    def name(self) -> Text:
        return "action_get_password_reset_page"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                f"{get_forgot_password_help_text('reset_page')}\n\n"
                f"{get_forgot_password_page_url()}"
            )
        )
        return []
