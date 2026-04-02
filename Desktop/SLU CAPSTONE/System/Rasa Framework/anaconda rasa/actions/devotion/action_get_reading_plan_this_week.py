from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import ReadingPlan
from .common import db


class ActionGetReadingPlanThisWeek(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_this_week"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        plans = ReadingPlan.get_this_week(db)
        if plans:
            days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            plans.sort(key=lambda p: days_order.index(p["day_of_week"]) if p["day_of_week"] in days_order else 99)
            lines = [f"This Week's Bible Reading Plan (Week of {plans[0]['week_start']}):"]
            for p in plans:
                lines.append(f"• {p['day_of_week']}: {p['reading']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(text="There is no reading plan available for this week yet.")
        return []
