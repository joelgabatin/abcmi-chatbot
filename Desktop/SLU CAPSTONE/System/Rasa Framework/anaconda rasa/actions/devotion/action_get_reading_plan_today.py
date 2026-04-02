from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import ReadingPlan
from .common import db


class ActionGetReadingPlanToday(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_today"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        plan = ReadingPlan.get_today(db)
        if plan:
            notes = f"\n\n{plan['notes']}" if plan.get("notes") else ""
            dispatcher.utter_message(
                text=f"Today's Bible Reading Plan ({plan['day_of_week']}):\n\n📖 {plan['reading']}{notes}"
            )
        else:
            dispatcher.utter_message(text="There is no reading plan entry for today yet. Please check back later.")
        return []
