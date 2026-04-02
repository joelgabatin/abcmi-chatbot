from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import DailyDevotion
from .common import db


class ActionGetDevotionScriptureToday(Action):
    def name(self) -> Text:
        return "action_get_devotion_scripture_today"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        devotion = DailyDevotion.get_today(db)
        if devotion:
            dispatcher.utter_message(
                text=f"Today's scripture passage is {devotion['scripture']}.\n\n_{devotion['scripture_text']}_"
            )
        else:
            dispatcher.utter_message(text="There is no devotion posted for today yet. Please check back later.")
        return []
