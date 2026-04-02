from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import ReadingPlan
from .common import db


class ActionGetReadingPlanByMonth(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_by_month"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        period_entity = next(tracker.get_latest_entity_values("reading_period"), None)
        if not period_entity:
            dispatcher.utter_message(text="Please specify a month. For example: 'What is the September 2026 reading plan?'")
            return []
        try:
            from dateutil.parser import parse as dp
            d = dp(period_entity)
            year, month = d.year, d.month
            month_label = d.strftime("%B %Y")
        except Exception:
            dispatcher.utter_message(text="I couldn't understand that month. Please try a format like 'September 2026'.")
            return []
        plans = ReadingPlan.get_by_month(db, year, month)
        if plans:
            lines = [f"Bible Reading Plan for {month_label}:\n"]
            for p in plans:
                lines.append(f"• {p['week_start']} ({p['day_of_week']}): {p['reading']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(text=f"There is no reading plan available for {month_label}.")
        return []
