from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingTeam(Action):
    def name(self) -> Text:
        return "action_get_counseling_team"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Counseling sessions are handled by the church's trained pastoral and counseling ministry team. "
                "They are prepared to listen, pray with you, and guide you with care and confidentiality."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
