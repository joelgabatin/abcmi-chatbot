from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_reading_plan_page_url


class ActionGetReadingPlanPageUrl(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_page_url"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_reading_plan_page_url()
        dispatcher.utter_message(
            text=f"You can find the Bible Reading Plan here:\n{url}\n\nYou can also ask me for today's or this week's reading plan right here in chat!"
        )
        return []
