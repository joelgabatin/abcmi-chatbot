import re
from datetime import datetime
from typing import Any, Dict, Text

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


MIN_COUNSELING_CONCERN_CHARACTERS = 25
MAX_COUNSELING_CONCERN_CHARACTERS = 400
_PHONE_RE = re.compile(r"^[+\d\s\-().]{7,20}$")
_OPTIONAL_SKIP_VALUES = {"", "skip", "n/a", "none", "-"}
_FACEBOOK_RE = re.compile(r"^(https?://)?(www\.)?(facebook\.com|fb\.com)/.+$", re.IGNORECASE)
_TIME_FORMATS = ("%I:%M %p", "%I %p", "%H:%M")
_COUNSELING_TYPE_CHOICES = {
    "1": "face-to-face",
    "face-to-face": "face-to-face",
    "face to face": "face-to-face",
    "facetoface": "face-to-face",
    "2": "call",
    "call": "call",
    "phone call": "call",
    "3": "video-call",
    "video call": "video-call",
    "video-call": "video-call",
    "videocall": "video-call",
}
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

    def validate_counseling_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        address = (slot_value or "").strip()
        if address.lower() in _OPTIONAL_SKIP_VALUES:
            return {"counseling_address": "Not provided"}
        if len(address) < 5:
            dispatcher.utter_message(
                text="Please enter a fuller address, or type `skip` if you prefer not to share it here."
            )
            return {"counseling_address": None}
        return {"counseling_address": address}

    def validate_counseling_facebook_account(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        facebook_account = (slot_value or "").strip()
        if facebook_account.lower() in _OPTIONAL_SKIP_VALUES:
            return {"counseling_facebook_account": "Not provided"}
        if len(facebook_account) < 5:
            dispatcher.utter_message(
                text="Please enter a Facebook name or profile link, or type `skip`."
            )
            return {"counseling_facebook_account": None}
        if "facebook" in facebook_account.lower() or "fb.com" in facebook_account.lower():
            if not _FACEBOOK_RE.match(facebook_account):
                dispatcher.utter_message(
                    text="That Facebook link looks incomplete. Please send a valid profile link or type `skip`."
                )
                return {"counseling_facebook_account": None}
        return {"counseling_facebook_account": facebook_account}

    def validate_counseling_preferred_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        raw_date = (slot_value or "").strip()
        parsed_date = None
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                parsed_date = datetime.strptime(raw_date, fmt).date()
                break
            except ValueError:
                continue

        if not parsed_date:
            dispatcher.utter_message(
                text="Please enter the preferred date using `dd/mm/yyyy`, for example `31/03/2026`."
            )
            return {"counseling_preferred_date": None}

        if parsed_date < datetime.now().date():
            dispatcher.utter_message(
                text="Please choose today or a future date for the counseling session."
            )
            return {"counseling_preferred_date": None}

        return {"counseling_preferred_date": parsed_date.isoformat()}

    def validate_counseling_preferred_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        raw_time = (slot_value or "").strip().upper()
        for fmt in _TIME_FORMATS:
            try:
                parsed_time = datetime.strptime(raw_time, fmt)
                return {
                    "counseling_preferred_time": parsed_time.strftime("%I:%M %p").lstrip("0")
                }
            except ValueError:
                continue

        dispatcher.utter_message(
            text="Please enter a valid time like `9:00 AM`, `2:30 PM`, or `14:00`."
        )
        return {"counseling_preferred_time": None}

    def validate_counseling_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        value = (slot_value or "").strip().lower()
        normalized = _COUNSELING_TYPE_CHOICES.get(value)
        if not normalized:
            dispatcher.utter_message(
                text="Please reply with `1`, `2`, or `3`, or type `face-to-face`, `call`, or `video call`."
            )
            return {"counseling_type": None}
        return {"counseling_type": normalized}

    def validate_counseling_is_member(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        value = (slot_value or "").strip().lower()
        if value not in _BOOLEAN_CHOICES:
            dispatcher.utter_message(
                text="Please reply with `yes` or `no`."
            )
            return {"counseling_is_member": None}
        return {"counseling_is_member": _BOOLEAN_CHOICES[value]}

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
