from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_register_help_text, get_register_page_url


class ActionGetRegistrationSteps(Action):
    def name(self) -> Text:
        return "action_get_registration_steps"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                f"{get_register_help_text('registration_steps')}\n\n"
                f"Registration page: {get_register_page_url()}"
            )
        )
        return []
