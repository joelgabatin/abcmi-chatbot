from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_testimony_page_url


class ActionGetTestimonyPageLink(Action):
    def name(self) -> Text:
        return "action_get_testimony_page_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_testimony_page_url()
        dispatcher.utter_message(
            text=(
                "You can read testimonies from our church community on our Testimony page:\n"
                f"{url}\n\n"
                "You will find stories of healing, salvation, provision, and more shared by members of our congregation.\n\n"
                "I can also show you some testimonies right here in this chat — just say 'Show me all the testimonies'."
            )
        )
        return []
