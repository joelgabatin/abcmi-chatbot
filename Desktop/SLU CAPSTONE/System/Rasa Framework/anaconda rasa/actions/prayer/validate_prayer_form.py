import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


class ValidatePrayerForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_prayer_form"

    def validate_prayer_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        name = slot_value.strip() if slot_value else ""
        if not name or len(name) < 2:
            dispatcher.utter_message(
                text="I didn't catch your name. Could you please tell me your name?"
            )
            return {"prayer_name": None}
        return {"prayer_name": name}

    def validate_prayer_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        phone = slot_value.strip() if slot_value else ""
        digits = "".join(filter(str.isdigit, phone))
        if len(digits) < 7:
            dispatcher.utter_message(
                text="Please provide a valid phone number so we can reach you."
            )
            return {"prayer_phone": None}
        return {"prayer_phone": phone}

    def validate_prayer_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        value = slot_value.strip().lower() if slot_value else ""
        # Allow user to skip address
        if value in ["skip", "none", "no", "n/a", "not applicable", "-"]:
            return {"prayer_address": "Not provided"}
        return {"prayer_address": slot_value.strip()}

    def validate_prayer_request(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        request = slot_value.strip() if slot_value else ""
        if not request or len(request) < 5:
            dispatcher.utter_message(
                text="Please share what you'd like us to pray for. "
                     "You can be as brief or as detailed as you feel comfortable with."
            )
            return {"prayer_request": None}
        return {"prayer_request": request}

    def validate_prayer_face_to_face(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        value = slot_value.strip().lower() if slot_value else ""
        yes_words = ["yes", "yeah", "yep", "sure", "please", "i would", "i'd like", "okay", "ok", "true"]
        no_words = ["no", "nope", "not", "don't", "no thanks", "false", "not necessary"]

        if any(w in value for w in yes_words):
            return {"prayer_face_to_face": True}
        if any(w in value for w in no_words):
            return {"prayer_face_to_face": False}

        dispatcher.utter_message(
            text="Just to clarify — would you like one of our pastors to visit you in person? "
                 "Please answer with yes or no."
        )
        return {"prayer_face_to_face": None}
