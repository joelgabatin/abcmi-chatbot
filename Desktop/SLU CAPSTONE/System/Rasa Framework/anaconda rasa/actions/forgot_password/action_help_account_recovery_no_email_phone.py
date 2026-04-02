from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_contact_page_url, get_forgot_password_help_text, get_support_email


class ActionHelpAccountRecoveryNoEmailPhone(Action):
    def name(self) -> Text:
        return "action_help_account_recovery_no_email_phone"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = get_forgot_password_help_text("no_access_to_email_or_phone")
        support_email = get_support_email()
        contact_page_url = get_contact_page_url()

        if support_email:
            message += f"\n\nSupport email: {support_email}"
        message += f"\n\nContact page: {contact_page_url}"

        dispatcher.utter_message(text=message)
        return []
