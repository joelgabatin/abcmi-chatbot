from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import DailyDevotion
from .common import db


class ActionGetDevotionAuthorToday(Action):
    def name(self) -> Text:
        return "action_get_devotion_author_today"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        devotion = DailyDevotion.get_today(db)
        if devotion:
            dispatcher.utter_message(text=f"Today's devotion was written by {devotion['author']}.")
        else:
            dispatcher.utter_message(text="There is no devotion posted for today yet. Please check back later or visit our devotional page.")
        return []
