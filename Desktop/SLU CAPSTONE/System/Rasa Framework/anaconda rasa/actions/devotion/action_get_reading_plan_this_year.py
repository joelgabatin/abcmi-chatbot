from datetime import date as date_type
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import ReadingPlan
from .common import db, get_reading_plan_page_url


class ActionGetReadingPlanThisYear(Action):
    def name(self) -> Text:
        return "action_get_reading_plan_this_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        year = date_type.today().year
        plans = ReadingPlan.get_this_year(db)
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
                    f"The reading plan for {year} is not yet available in the chatbot.\n\n"
                    f"You can check our Bible Reading page for the latest updates:\n{url}"
                )
            )
        return []
