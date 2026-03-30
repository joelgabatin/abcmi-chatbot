from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import SUPPORTED_SOCIAL_MEDIA, SiteSettings, db


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
            dispatcher.utter_message(text="Our official social media accounts are:\n" + "\n".join(available_links))
        else:
            dispatcher.utter_message(response="utter_social_media")
        return []
