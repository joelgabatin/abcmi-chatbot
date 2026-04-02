from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from database import DevotionSubscriber
from .common import db


class ActionProcessDevotionSubscribe(Action):
    def name(self) -> Text:
        return "action_process_devotion_subscribe"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("devotion_subscriber_email") or ""

        result = DevotionSubscriber.subscribe(db, email=email, email_notifications=True)

        if result:
            dispatcher.utter_message(
                text=(
                    f"You're now subscribed to daily devotions!\n\n"
                    f"Email: {email}\n\n"
                    "You will receive daily devotion reminders to your inbox. "
                    "You can unsubscribe at any time by clicking the unsubscribe link in any email."
                )
            )
        else:
            dispatcher.utter_message(
                text=(
                    "I'm sorry, I couldn't complete your subscription right now.\n\n"
                    "Please try again later or visit our devotional page to subscribe directly."
                )
            )

        return [SlotSet("devotion_subscriber_email", None)]
