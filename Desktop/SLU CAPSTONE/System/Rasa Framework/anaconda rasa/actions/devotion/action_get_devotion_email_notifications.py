from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_devotional_page_url


class ActionGetDevotionEmailNotifications(Action):
    def name(self) -> Text:
        return "action_get_devotion_email_notifications"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_devotional_page_url()
        dispatcher.utter_message(
            text=(
                "When you subscribe to daily devotions, there is an option on the subscription form to enable email notifications. "
                "Simply check the 'Receive email reminders' option before submitting.\n\n"
                "Once enabled, you'll receive a daily email with the devotion. "
                "Note: At the moment, SMS/phone reminders are not available — only email.\n\n"
                f"You can subscribe here:\n{url}"
            )
        )
        return []
