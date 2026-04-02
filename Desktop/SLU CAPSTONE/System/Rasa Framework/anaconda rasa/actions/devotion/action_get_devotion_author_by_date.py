from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import DailyDevotion
from .common import db


class ActionGetDevotionAuthorByDate(Action):
    def name(self) -> Text:
        return "action_get_devotion_author_by_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date_entity = next(tracker.get_latest_entity_values("devotion_date"), None)
        if not date_entity:
            dispatcher.utter_message(text="Please specify a date. For example: 'Who wrote the September 6, 2026 devotion?'")
            return []
        try:
            from dateutil.parser import parse as dp
            date_str = dp(date_entity).date().isoformat()
        except Exception:
            dispatcher.utter_message(text="I couldn't understand that date. Please try a format like 'September 6, 2026'.")
            return []
        devotion = DailyDevotion.get_by_date(db, date_str)
        if devotion:
            dispatcher.utter_message(text=f"The devotion for {devotion['date']} was written by {devotion['author']}.")
        else:
            dispatcher.utter_message(text=f"I couldn't find a devotion for {date_entity}. It may not have been published yet.")
        return []
