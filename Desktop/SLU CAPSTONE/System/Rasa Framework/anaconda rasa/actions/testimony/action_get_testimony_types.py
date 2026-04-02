from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetTestimonyTypes(Action):
    def name(self) -> Text:
        return "action_get_testimony_types"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "The church accepts testimonies under the following categories:\n\n"
                "- Healing\n"
                "- Salvation\n"
                "- Provision\n"
                "- Protection\n"
                "- Deliverance\n"
                "- Restoration\n"
                "- Answered Prayer\n"
                "- Other\n\n"
                "Any testimony of God's faithfulness and goodness is welcome. If your story does not fit a specific category, you can choose 'Other'."
            )
        )
        return []
