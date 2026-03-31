import re
from typing import Any, Dict, Text

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


MIN_COUNSELING_CONCERN_CHARACTERS = 25
MAX_COUNSELING_CONCERN_CHARACTERS = 400
_PHONE_RE = re.compile(r"^[+\d\s\-().]{7,20}$")


class ValidateCounselingRequestForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_counseling_request_form"

    def validate_counseling_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        name = (slot_value or "").strip()
        if len(name) < 2:
            dispatcher.utter_message(
                text="Please enter your full name using at least 2 characters."
            )
            return {"counseling_name": None}
        return {"counseling_name": name}

    def validate_counseling_contact_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        contact_number = (slot_value or "").strip()
        if not _PHONE_RE.match(contact_number):
            dispatcher.utter_message(
                text="That doesn't look like a valid contact number. Please enter a valid phone number with country code if possible."
            )
            return {"counseling_contact_number": None}
        return {"counseling_contact_number": contact_number}

    def validate_counseling_concern(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        concern = (slot_value or "").strip()
        character_count = len(concern)
        if character_count < MIN_COUNSELING_CONCERN_CHARACTERS:
            dispatcher.utter_message(
                text=(
                    "Please share a bit more detail so we can understand your concern. "
                    f"Use at least {MIN_COUNSELING_CONCERN_CHARACTERS} characters."
                )
            )
            return {"counseling_concern": None}
        if character_count > MAX_COUNSELING_CONCERN_CHARACTERS:
            dispatcher.utter_message(
                text=(
                    "Your concern is a bit too long for this form. "
                    f"Please keep it under {MAX_COUNSELING_CONCERN_CHARACTERS} characters."
                )
            )
            return {"counseling_concern": None}
        return {"counseling_concern": concern}
