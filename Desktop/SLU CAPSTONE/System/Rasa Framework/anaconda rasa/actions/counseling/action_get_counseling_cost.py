from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingCost(Action):
    def name(self) -> Text:
        return "action_get_counseling_cost"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Yes. Counseling is provided free of charge as part of the church's pastoral ministry."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
