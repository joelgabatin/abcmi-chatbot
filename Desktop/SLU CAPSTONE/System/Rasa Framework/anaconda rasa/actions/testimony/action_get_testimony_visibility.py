from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetTestimonyVisibility(Action):
    def name(self) -> Text:
        return "action_get_testimony_visibility"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Testimonies are not shown immediately after submission. All submitted testimonies go through a review process by our church administrators.\n\n"
                "Once reviewed and approved, your testimony will appear on the Testimony page. "
                "This ensures that the content shared is appropriate and uplifting for our community.\n\n"
                "Anonymous submissions are also supported — just indicate that when submitting."
            )
        )
        return []
