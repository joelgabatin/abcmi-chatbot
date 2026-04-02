from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_testimony_page_url


class ActionGetTestimonyWebsiteLink(Action):
    def name(self) -> Text:
        return "action_get_testimony_website_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_testimony_page_url()
        dispatcher.utter_message(
            text=(
                "To submit your testimony on our website:\n\n"
                f"Visit our Testimony page:\n{url}.\n"
                "1. Fillout the share your testimony form.\n"
                "2. Once done click submit my testompy and our team will review it and post it once approved.\n\n"
                "You can also submit directly here in chat by saying 'submit my testimony'."
            )
        )
        return []
