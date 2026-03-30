from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import SUPPORTED_SOCIAL_MEDIA, SiteSettings, db, get_requested_platform


class ActionGetSpecificSocialMedia(Action):
    def name(self) -> Text:
        return "action_get_specific_social_media"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        platform = get_requested_platform(tracker.latest_message)

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
                text=f"Yes, we do. You can visit our official {platform_label} account here: {social_url}"
            )
        else:
            dispatcher.utter_message(text=f"Sorry, we don't have a {platform_label} link available right now.")
        return []
