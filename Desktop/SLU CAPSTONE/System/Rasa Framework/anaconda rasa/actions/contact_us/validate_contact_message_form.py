import re
from typing import Any, Dict, Text

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

# Ordered list — position maps to choice number (1-based)
SUBJECTS = [
    "General Inquiry",
    "Prayer Request",
    "Church Membership",
    "Missions & Training",
    "Donations & Giving",
    "Events & Activities",
    "Other",
]

MIN_MESSAGE_CHARACTERS = 25
MAX_MESSAGE_CHARACTERS = 200

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^[+\d\s\-().]{7,20}$")

_SUBJECTS_PROMPT = "\n".join(f"{i}. {s}" for i, s in enumerate(SUBJECTS, 1))


class ValidateContactMessageForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_contact_message_form"

    def validate_contact_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        name = (slot_value or "").strip()
        if len(name) < 2:
            dispatcher.utter_message(text="Please enter your full name (at least 2 characters).")
            return {"contact_name": None}
        return {"contact_name": name}

    def validate_contact_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        email = (slot_value or "").strip()
        if not _EMAIL_RE.match(email):
            dispatcher.utter_message(text="That doesn't look like a valid email address. Please enter a valid one (e.g. you@example.com).")
            return {"contact_email": None}
        return {"contact_email": email}

    def validate_contact_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        phone = (slot_value or "").strip()
        if phone.lower() in ("skip", "n/a", "none", "-"):
            return {"contact_phone": None}
        if not _PHONE_RE.match(phone):
            dispatcher.utter_message(text="That doesn't look like a valid phone number. Please enter a valid number or type 'skip' to leave it blank.")
            return {"contact_phone": None}
        return {"contact_phone": phone}

    def validate_contact_subject(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        value = (slot_value or "").strip()

        # Accept number choice (1–8)
        if value.isdigit():
            idx = int(value) - 1
            if 0 <= idx < len(SUBJECTS):
                return {"contact_subject": SUBJECTS[idx]}
            dispatcher.utter_message(
                text=f"Please enter a number between 1 and {len(SUBJECTS)}.\n\n{_SUBJECTS_PROMPT}"
            )
            return {"contact_subject": None}

        # Also accept typing the subject name directly
        value_lower = value.lower()
        for subject in SUBJECTS:
            if value_lower == subject.lower():
                return {"contact_subject": subject}

        dispatcher.utter_message(
            text=f"Please enter the number of your chosen subject:\n\n{_SUBJECTS_PROMPT}"
        )
        return {"contact_subject": None}

    def validate_contact_message(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        message = (slot_value or "").strip()
        character_count = len(message)
        if character_count < MIN_MESSAGE_CHARACTERS:
            dispatcher.utter_message(
                text=f"Your message is too short. Please enter at least {MIN_MESSAGE_CHARACTERS} characters."
            )
            return {"contact_message": None}
        if character_count > MAX_MESSAGE_CHARACTERS:
            dispatcher.utter_message(
                text=f"Your message is too long. Please keep it under {MAX_MESSAGE_CHARACTERS} characters."
            )
            return {"contact_message": None}
        return {"contact_message": message}
