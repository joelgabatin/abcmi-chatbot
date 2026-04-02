from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_devotional_page_url


class ActionGetDevotionPageLink(Action):
    def name(self) -> Text:
        return "action_get_devotion_page_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_devotional_page_url()
        dispatcher.utter_message(
            text=f"You can read the full daily devotion here:\n{url}"
        )
        return []
