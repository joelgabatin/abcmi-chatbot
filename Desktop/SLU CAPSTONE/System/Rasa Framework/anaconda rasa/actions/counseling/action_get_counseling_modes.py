from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingModes(Action):
    def name(self) -> Text:
        return "action_get_counseling_modes"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Counseling is available in three modes: face-to-face, phone call, and video call. "
                "You can choose the option that is most comfortable and practical for you."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
