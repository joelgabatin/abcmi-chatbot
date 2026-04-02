from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import Testimony
from .common import db, get_testimony_page_url


class ActionGetFeaturedTestimonies(Action):
    def name(self) -> Text:
        return "action_get_featured_testimonies"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        testimonies = Testimony.get_featured(db, limit=5)
        if testimonies:
            lines = ["Here are some testimonies from our church community:\n"]
            for i, t in enumerate(testimonies, 1):
                author = "Anonymous" if t.get("anonymous") else t.get("author", "Anonymous")
                lines.append(f"{i}. {t['title']} — {author} ({t['category']})")
            url = get_testimony_page_url()
            lines.append(f"\n Do you want to submit a testimony in this chat? just message \"I'm ready to share my testimony in chat\" \n{url}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            url = get_testimony_page_url()
            dispatcher.utter_message(
                text=(
                    "There are no published testimonies available at the moment.\n\n"
                    f"You can check our Testimony page directly:\n{url}"
                )
            )
        return []
