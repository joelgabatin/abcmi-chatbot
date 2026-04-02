from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_contact_page_url, get_forgot_password_help_text, get_support_email


class ActionEscalatePasswordResetSupport(Action):
    def name(self) -> Text:
        return "action_escalate_password_reset_support"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        support_email = get_support_email()
        contact_page_url = get_contact_page_url()

        message = get_forgot_password_help_text("support_escalation")
        if support_email:
            message += f"\n\nYou can contact support by email at {support_email}."
        message += f"\n\nYou can also submit a message through the Contact page:\n{contact_page_url}"

        dispatcher.utter_message(text=message)
        return []
