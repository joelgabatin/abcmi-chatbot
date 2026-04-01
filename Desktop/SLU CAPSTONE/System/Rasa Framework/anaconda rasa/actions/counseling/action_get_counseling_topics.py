from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingTopics(Action):
    def name(self) -> Text:
        return "action_get_counseling_topics"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Counseling can cover concerns such as family issues, marriage concerns, personal struggles, "
                "spiritual growth, and grief. If you are carrying something heavy, you are welcome to bring it to counseling."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
