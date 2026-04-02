from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import DailyDevotion
from .common import db


class ActionGetDevotionFullToday(Action):
    def name(self) -> Text:
        return "action_get_devotion_full_today"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        devotion = DailyDevotion.get_today(db)
        if devotion:
            dispatcher.utter_message(
                text=(
                    f"{devotion['title']}\n"
                    f"📖 {devotion['scripture']}\n\n"
                    f"_{devotion['scripture_text']}_\n\n"
                    f"{devotion['reflection']}\n\n"
                    f"✨ \"{devotion['featured_verse']}\" — {devotion['featured_verse_ref']}\n\n"
                    f"— Written by {devotion['author']}"
                )
            )
        else:
            dispatcher.utter_message(text="There is no devotion posted for today yet. Please check back later.")
        return []
