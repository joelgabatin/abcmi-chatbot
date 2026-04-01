from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .common import get_counseling_page_url


class ActionOfferCounselingSupport(Action):
    def name(self) -> Text:
        return "action_offer_counseling_support"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "I'm sorry that you're going through a difficult time. Help is available, and you do not have to carry it alone.\n\n"
                "If you want, I can help you book a counseling session here in chat, or you can use the Counseling page:\n"
                f"{get_counseling_page_url()}"
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
