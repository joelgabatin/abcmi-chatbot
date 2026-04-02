from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_devotional_page_url


class ActionGetDevotionUnsubscribe(Action):
    def name(self) -> Text:
        return "action_get_devotion_unsubscribe"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_devotional_page_url()
        dispatcher.utter_message(
            text=(
                "To unsubscribe from daily devotion reminders, click the Unsubscribe link at the bottom of any devotion email you received. "
                "You can also visit our devotional page and use the unsubscribe option there:\n"
                f"{url}\n\n"
                "Please note that I am not able to unsubscribe you directly from this chat — you'll need to do it through your email or the page above."
            )
        )
        return []
