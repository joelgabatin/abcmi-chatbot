from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCounselingOverview(Action):
    def name(self) -> Text:
        return "action_get_counseling_overview"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Yes. The church offers free and confidential pastoral counseling sessions. "
                "If you'd like, I can also help you schedule one or submit a counseling request here in chat."
            )
        )
        return [SlotSet("last_contact_topic", "counseling")]
