from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from database import Database, SiteSettings

db = Database()
if not db.is_connected():
    db.connect()


SUPPORTED_SOCIAL_MEDIA = {
    "facebook": "Facebook",
    "tiktok": "TikTok",
    "instagram": "Instagram",
    "youtube": "YouTube",
}


def _get_requested_platform(tracker: Tracker) -> Text | None:
    for entity in tracker.latest_message.get("entities", []):
        if entity.get("entity") == "social_platform":
            return (entity.get("value") or "").strip().lower()
    return None


class ActionGetEmail(Action):
    def name(self) -> Text:
        return "action_get_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = SiteSettings.get_email(db)
        if email:
            dispatcher.utter_message(text=f"You can reach us via email at {email}.")
        else:
            dispatcher.utter_message(response="utter_email")
        return []


class ActionGetPhoneNumber(Action):
    def name(self) -> Text:
        return "action_get_phone_number"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone_number = SiteSettings.get_phone_number(db)
        if phone_number:
            dispatcher.utter_message(text=f"Our phone number is {phone_number}.")
        else:
            dispatcher.utter_message(response="utter_phone_number")
        return []


class ActionGetOfficeHours(Action):
    def name(self) -> Text:
        return "action_get_office_hours"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        office_hours = SiteSettings.get_office_hours(db)
        if office_hours:
            dispatcher.utter_message(text=f"Our office hours are {office_hours}.")
        else:
            dispatcher.utter_message(response="utter_office_hours")
        return []


class ActionGetOfficeAddress(Action):
    def name(self) -> Text:
        return "action_get_office_address"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        office_address = SiteSettings.get_office_address(db)
        if office_address:
            dispatcher.utter_message(text=f"Our main office is located at {office_address}.")
        else:
            dispatcher.utter_message(response="utter_office_address")
        return []


class ActionGetSocialMedia(Action):
    def name(self) -> Text:
        return "action_get_social_media"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        social_links = SiteSettings.get_social_media_links(db)
        available_links = []

        for platform, label in SUPPORTED_SOCIAL_MEDIA.items():
            url = social_links.get(f"{platform}_url")
            if url:
                available_links.append(f"{label}: {url}")

        if available_links:
            dispatcher.utter_message(
                text="Our official social media accounts are:\n" + "\n".join(available_links)
            )
        else:
            dispatcher.utter_message(response="utter_social_media")
        return [] 


class ActionGetSpecificSocialMedia(Action):
    def name(self) -> Text:
        return "action_get_specific_social_media"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        platform = _get_requested_platform(tracker)

        if not platform:
            dispatcher.utter_message(response="utter_social_media")
            return []

        if platform not in SUPPORTED_SOCIAL_MEDIA:
            dispatcher.utter_message(text=f"Sorry, we don't have {platform}.")
            return []

        platform_label = SUPPORTED_SOCIAL_MEDIA[platform]
        social_url = SiteSettings.get_social_media_url(db, platform)

        if social_url:
            dispatcher.utter_message(
                text=f"Yes, we do. You can visit our Official {platform_label} account here: {social_url}"
            )
        else:
            dispatcher.utter_message(
                text=f"Sorry, we don't have a {platform_label} link available right now."
            )
        return []
