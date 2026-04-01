from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetMultipleMinistryJoinInfo(Action):
    def name(self) -> Text:
        return "action_get_multiple_ministry_join_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Yes, you can generally join more than one ministry as long as you can commit to their schedules and responsibilities. "
                "It is best to coordinate with each ministry leader first so they can help you see if the commitments fit well together."
            )
        )
        return []
