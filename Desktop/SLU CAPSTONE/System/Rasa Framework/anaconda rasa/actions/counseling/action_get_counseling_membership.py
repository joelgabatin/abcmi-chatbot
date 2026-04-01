from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingMembership(Action):
    def name(self) -> Text:
        return "action_get_counseling_membership"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Yes. Counseling is open to both church members and non-members. "
                "If you need support, you are welcome to request a session."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
