from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_contact_page_url, get_register_help_text, get_support_email


class ActionHelpFailedRegistration(Action):
    def name(self) -> Text:
        return "action_help_failed_registration"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = get_register_help_text("failed_registration")
        support_email = get_support_email()
        contact_page_url = get_contact_page_url()

        if support_email:
            message += f"\n\nSupport email: {support_email}"
        message += f"\n\nContact page: {contact_page_url}"

        dispatcher.utter_message(text=message)
        return []
