from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import SUPPORTED_SOCIAL_MEDIA, SiteSettings, db, get_contact_page_url


class ActionGetAllContactDetails(Action):
    def name(self) -> Text:
        return "action_get_all_contact_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = SiteSettings.get_email(db)
        phone = SiteSettings.get_phone_number(db)
        address = SiteSettings.get_office_address(db)
        hours = SiteSettings.get_office_hours(db)
        social_info = SiteSettings.get_social_media_links(db)
        contact_url = get_contact_page_url()

        lines = ["You can contact us through these details:"]
        lines.append(f"Email: {email or 'Not available right now'}")
        lines.append(f"Phone: {phone or 'Not available right now'}")
        lines.append(f"Address: {address or 'Not available right now'}")
        lines.append(f"Office hours: {hours or 'Not available right now'}")

        social_lines = []
        for platform, label in SUPPORTED_SOCIAL_MEDIA.items():
            url = social_info.get(f"{platform}_url")
            if url:
                social_lines.append(f"- {label}: {url}")

        if social_lines:
            lines.append("")
            lines.append("Social media:")
            lines.extend(social_lines)

        lines.append("")
        lines.append(f"Contact page: {contact_url}")
        lines.append('You can also send a message here in chat by saying "I want to send a message to the church."')

        dispatcher.utter_message(text="\n".join(lines))
        return []
