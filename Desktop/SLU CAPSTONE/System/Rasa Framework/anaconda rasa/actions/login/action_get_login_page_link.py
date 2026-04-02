from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_login_page_url


class ActionGetLoginPageLink(Action):
    def name(self) -> Text:
        return "action_get_login_page_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "You can sign in here:\n"
                f"{get_login_page_url()}"
            )
        )
        return []
