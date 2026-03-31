from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from database import ContactMessage

from .common import db, get_contact_page_url


class ActionProcessContactMessage(Action):
    def name(self) -> Text:
        return "action_process_contact_message"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("contact_name") or "Friend"
        email = tracker.get_slot("contact_email") or ""
        phone = tracker.get_slot("contact_phone")
        subject = tracker.get_slot("contact_subject")
        message = tracker.get_slot("contact_message") or ""

        result = ContactMessage.save(
            db,
            name=name,
            email=email,
            message=message,
            phone_number=phone,
            subject=subject,
        )

        if result:
            dispatcher.utter_message(
                text=(
                    f"Thank you, {name}! Your message has been submitted to the church. 🙏\n\n"
                    f"Subject: {subject or 'General Inquiry'}\n"
                    "We usually reply within 1 to 2 business days."
                )
            )
        else:
            contact_url = get_contact_page_url()
            dispatcher.utter_message(
                text=(
                    "I'm sorry, I couldn't submit your message right now.\n\n"
                    f"You can still reach us directly through our Contact page:\n{contact_url}"
                )
            )

        return [AllSlotsReset()]
