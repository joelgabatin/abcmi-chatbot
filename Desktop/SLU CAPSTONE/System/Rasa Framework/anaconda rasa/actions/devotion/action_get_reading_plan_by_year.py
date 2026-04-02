from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import ReadingPlan
from .common import db, get_reading_plan_page_url


class ActionGetReadingPlanByYear(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_by_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        period_entity = next(tracker.get_latest_entity_values("reading_period"), None)
        if not period_entity:
            dispatcher.utter_message(text="Please specify a year. For example: 'Provide the 2025 reading plan'.")
            return []
        try:
            from dateutil.parser import parse as dp
            year = dp(period_entity).year
        except Exception:
            dispatcher.utter_message(text="I couldn't understand that year. Please try a format like '2025'.")
            return []
        plans = ReadingPlan.get_by_year(db, year)
        if plans:
            url = get_reading_plan_page_url()
            dispatcher.utter_message(
                text=(
                    f"There are {len(plans)} reading plan entries for {year}.\n\n"
                    f"You can view the full {year} reading plan on our Bible Reading page:\n{url}"
                )
            )
        else:
            url = get_reading_plan_page_url()
            dispatcher.utter_message(
                text=(
                    f"The reading plan for {year} is not available in the chatbot.\n\n"
                    f"You can check our Bible Reading page for updates:\n{url}"
                )
            )
        return []
