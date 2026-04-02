from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_register_help_text


class ActionExplainResendVerificationInstructions(Action):
    def name(self) -> Text:
        return "action_explain_resend_verification_instructions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_register_help_text("resend_verification"))
        return []
