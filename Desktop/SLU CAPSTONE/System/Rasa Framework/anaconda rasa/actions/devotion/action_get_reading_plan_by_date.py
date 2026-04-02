from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import ReadingPlan
from .common import db


class ActionGetReadingPlanByDate(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_by_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date_entity = next(tracker.get_latest_entity_values("reading_period"), None)
        if not date_entity:
            dispatcher.utter_message(text="Please specify a date. For example: 'What is the September 8, 2026 reading plan?'")
            return []
        plan = ReadingPlan.get_by_date(db, date_entity)
        if plan:
            notes = f"\n\n📝 {plan['notes']}" if plan.get("notes") else ""
            dispatcher.utter_message(
                text=f"Bible Reading Plan for {date_entity} ({plan['day_of_week']}):\n\n📖 {plan['reading']}{notes}"
            )
        else:
            dispatcher.utter_message(text=f"I couldn't find a reading plan for {date_entity}.")
        return []
