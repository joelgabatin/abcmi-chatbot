from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingConfidentiality(Action):
    def name(self) -> Text:
        return "action_get_counseling_confidentiality"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        last_topic = (tracker.get_slot("last_contact_topic") or "").strip().lower()

        if last_topic == "counseling":
            dispatcher.utter_message(
                text=(
                    "Yes. All counseling sessions are strictly confidential."
                )
            )
        else:
            dispatcher.utter_message(
                text=(
                    "If you're asking about counseling, yes. All counseling sessions are strictly confidential."
                )
            )

        return [SlotSet("last_contact_topic", "counseling")]
