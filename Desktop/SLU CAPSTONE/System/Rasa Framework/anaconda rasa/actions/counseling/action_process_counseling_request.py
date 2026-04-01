from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from database import CounselingRequest

from .common import db, get_counseling_page_url


class ActionProcessCounselingRequest(Action):
    def name(self) -> Text:
        return "action_process_counseling_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("counseling_name") or "Friend"
        contact_number = tracker.get_slot("counseling_contact_number") or ""
        address = tracker.get_slot("counseling_address") or "Not provided"
        facebook_account = tracker.get_slot("counseling_facebook_account") or "Not provided"
        preferred_date = tracker.get_slot("counseling_preferred_date") or ""
        preferred_time = tracker.get_slot("counseling_preferred_time") or ""
        counseling_type = tracker.get_slot("counseling_type") or ""
        is_member = tracker.get_slot("counseling_is_member")
        concern = tracker.get_slot("counseling_concern") or ""

        result = CounselingRequest.save(
            db,
            name=name,
            contact_number=contact_number,
            address=address,
            facebook_account=facebook_account,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            counseling_type=counseling_type,
            is_member=bool(is_member),
            concern=concern,
        )

        if result:
            dispatcher.utter_message(
                text=(
                    f"Thank you, {name}. Your counseling request has been submitted.\n\n"
                    "A church representative will review your details, confirm the schedule with you, and contact you as soon as possible."
                )
            )
        else:
            dispatcher.utter_message(
                text=(
                    "I'm sorry, I couldn't submit your counseling request right now.\n\n"
                    "You can still continue through our Counseling page:\n"
                    f"{get_counseling_page_url()}"
                )
            )

        return [AllSlotsReset(), SlotSet("last_contact_topic", "counseling")]
