from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_devotional_page_url


class ActionGetDevotionSubscribe(Action):
    def name(self) -> Text:
        return "action_get_devotion_subscribe"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_devotional_page_url()
        dispatcher.utter_message(
            text=(
                "You can subscribe to daily devotions in two ways:\n\n"
                f"1. Visit our devotional page and fill in the subscription form:\n{url}\n\n"
                "2. I can also subscribe you right here in this chat! Just say 'subscribe me to daily devotions' and I'll ask for your email."
            )
        )
        return []
