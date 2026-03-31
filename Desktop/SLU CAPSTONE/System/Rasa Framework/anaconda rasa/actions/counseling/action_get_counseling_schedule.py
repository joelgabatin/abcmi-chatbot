from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .common import get_counseling_page_url


class ActionGetCounselingSchedule(Action):
    def name(self) -> Text:
        return "action_get_counseling_schedule"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "You can schedule a counseling session through our Counseling page:\n"
                f"{get_counseling_page_url()}\n\n"
                "If you prefer, I can also help you submit a counseling request here."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
