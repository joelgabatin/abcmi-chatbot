from typing import Any, Dict, Text

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

VALID_CATEGORIES = [
    "healing", "salvation", "provision", "protection",
    "deliverance", "restoration", "answered prayer", "other"
]


class ValidateTestimonyForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_testimony_form"

    def validate_testimony_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value or not slot_value.strip():
            dispatcher.utter_message(text="Please provide your name, or type 'anonymous' to keep it private.")
            return {"testimony_name": None}
        return {"testimony_name": slot_value.strip()}

    def validate_testimony_title(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value or len(slot_value.strip()) < 3:
            dispatcher.utter_message(text="Please provide a title for your testimony (at least 3 characters).")
            return {"testimony_title": None}
        return {"testimony_title": slot_value.strip()}

    def validate_testimony_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(
                text="Please choose a category: Healing, Salvation, Provision, Protection, Deliverance, Restoration, Answered Prayer, or Other."
            )
            return {"testimony_category": None}
        normalized = slot_value.strip().lower()
        match = next((c for c in VALID_CATEGORIES if c in normalized), None)
        if not match:
            dispatcher.utter_message(
                text="Please choose one of these categories: Healing, Salvation, Provision, Protection, Deliverance, Restoration, Answered Prayer, or Other."
            )
            return {"testimony_category": None}
        return {"testimony_category": match.title()}

    def validate_testimony_content(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value or len(slot_value.strip()) < 50:
            dispatcher.utter_message(
                text="Your testimony is too short. Please share at least 50 characters so we can post it meaningfully."
            )
            return {"testimony_content": None}
        if len(slot_value.strip()) > 2000:
            dispatcher.utter_message(
                text="Your testimony is a bit too long (maximum 2000 characters). Please shorten it a little."
            )
            return {"testimony_content": None}
        return {"testimony_content": slot_value.strip()}

    def validate_testimony_branch(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value or not slot_value.strip():
            dispatcher.utter_message(text="Please enter your branch name, or type 'none' if you are not from a specific branch.")
            return {"testimony_branch": None}
        return {"testimony_branch": slot_value.strip()}

    def validate_testimony_is_member(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Please reply with 'yes' or 'no' — are you a church member?")
            return {"testimony_is_member": None}
        val = slot_value.strip().lower()
        if val in ("yes", "y", "true", "1"):
            return {"testimony_is_member": True}
        if val in ("no", "n", "false", "0"):
            return {"testimony_is_member": False}
        dispatcher.utter_message(text="Please reply with 'yes' or 'no'.")
        return {"testimony_is_member": None}
