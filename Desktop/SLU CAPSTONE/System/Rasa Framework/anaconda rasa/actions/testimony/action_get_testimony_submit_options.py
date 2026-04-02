from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_testimony_page_url


class ActionGetTestimonySubmitOptions(Action):
    def name(self) -> Text:
        return "action_get_testimony_submit_options"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_testimony_page_url()
        dispatcher.utter_message(
            text=(
                "Yes! You can submit your testimony right here in this chat.\n\n"
                "Just say 'I want to submit my testimony' and I will process it for you.\n\n"
                "You can also submit through our Testimony page on the website:\n"
                f"{url}"
            )
        )
        return []
