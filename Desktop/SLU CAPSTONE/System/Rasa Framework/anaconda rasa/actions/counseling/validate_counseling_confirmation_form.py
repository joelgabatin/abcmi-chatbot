from typing import Any, Dict, Text

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


_BOOLEAN_CHOICES = {
    "yes": True,
    "y": True,
    "true": True,
    "1": True,
    "no": False,
    "n": False,
    "false": False,
    "0": False,
}


class ValidateCounselingConfirmationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_counseling_confirmation_form"

    def validate_counseling_continue_confirmation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        value = (slot_value or "").strip().lower()
        if value not in _BOOLEAN_CHOICES:
            dispatcher.utter_message(
                text="Sorry, I can't understand please enter yes or no"
            )
            return {"counseling_continue_confirmation": None}
        return {"counseling_continue_confirmation": _BOOLEAN_CHOICES[value]}
