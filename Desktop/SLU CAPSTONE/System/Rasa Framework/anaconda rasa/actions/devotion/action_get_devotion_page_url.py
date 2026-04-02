from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_devotional_page_url


class ActionGetDevotionPageUrl(Action):
    def name(self) -> Text:
        return "action_get_devotion_page_url"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_devotional_page_url()
        dispatcher.utter_message(
            text=(
                f"You can browse all past and current devotions on our Daily Devotional page:\n{url}\n\n"
                "You can also ask me to read a devotion for a specific date directly in this chat!"
            )
        )
        return []
