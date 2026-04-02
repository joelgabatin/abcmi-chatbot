from typing import Any, Dict, Text

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

from database import DevotionSubscriber


class ValidateDevotionSubscribeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_devotion_subscribe_form"

    def validate_devotion_subscriber_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value or not isinstance(slot_value, str):
            dispatcher.utter_message(text="Please provide a valid email address.")
            return {"devotion_subscriber_email": None}

        if not DevotionSubscriber.is_valid_email(slot_value):
            dispatcher.utter_message(
                text=f"'{slot_value}' doesn't look like a valid email address. Please try again. (e.g. yourname@email.com)"
            )
            return {"devotion_subscriber_email": None}

        return {"devotion_subscriber_email": slot_value.strip().lower()}
