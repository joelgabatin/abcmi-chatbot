from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetMinistryVolunteerInfo(Action):
    def name(self) -> Text:
        return "action_get_ministry_volunteer_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "No, you cannot volunteer for a ministry if you are not yet a formal member. "
                "The usual next step is to contact the ministry leader, let them know how you want to serve, and ask about any orientation or ministry-specific expectations."
            )
        )
        return []
