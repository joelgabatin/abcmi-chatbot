from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_forgot_password_help_text, get_forgot_password_page_url


class ActionHandleExpiredResetLink(Action):
    def name(self) -> Text:
        return "action_handle_expired_reset_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                f"{get_forgot_password_help_text('expired_link')}\n\n"
                f"You can request a new one here: {get_forgot_password_page_url()}"
            )
        )
        return []
