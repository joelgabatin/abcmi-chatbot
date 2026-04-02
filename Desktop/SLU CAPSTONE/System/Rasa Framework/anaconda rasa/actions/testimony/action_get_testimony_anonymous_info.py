from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_testimony_page_url


class ActionGetTestimonyAnonymousInfo(Action):
    def name(self) -> Text:
        return "action_get_testimony_anonymous_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = get_testimony_page_url()
        dispatcher.utter_message(
            text=(
                "Yes, anonymous submissions are fully supported! If you prefer not to share your name, your testimony will be displayed as 'Anonymous'.\n\n"
                "You can submit anonymously through our Testimony page:\n"
                f"{url}\n\n"
                "Or say 'submit my testimony' and I will walk you through it here. When I ask for your name, you can type 'anonymous' to keep it private."
            )
        )
        return []
