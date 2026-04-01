from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingTimeSlots(Action):
    def name(self) -> Text:
        return "action_get_counseling_time_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "The available counseling time slots are from 9:00 AM to 4:00 PM. "
                "When you book a session, you can choose your preferred time within that range."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
