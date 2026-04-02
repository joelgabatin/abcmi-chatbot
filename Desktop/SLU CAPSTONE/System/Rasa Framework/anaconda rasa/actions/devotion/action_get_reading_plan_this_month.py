from datetime import date as date_type
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import ReadingPlan
from .common import db


class ActionGetReadingPlanThisMonth(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_this_month"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        plans = ReadingPlan.get_this_month(db)
        month_name = date_type.today().strftime("%B %Y")
        if plans:
            lines = [f"Bible Reading Plan for {month_name}:\n"]
            for p in plans:
                lines.append(f"• {p['week_start']} ({p['day_of_week']}): {p['reading']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(text=f"There is no reading plan available for {month_name} yet.")
        return []
