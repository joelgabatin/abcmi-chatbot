import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchEvent

db = Database()


class ActionGetEventDate(Action):

    def name(self) -> Text:
        return "action_get_event_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db.connect()
        event_name = next(tracker.get_latest_entity_values("event_name"), None)
        if not event_name:
            dispatcher.utter_message(
                text="Could you please tell me the name of the event you're asking about?"
            )
            return []

        events = ChurchEvent.find_by_name(db, event_name)
        if events:
            e = events[0]
            date_str = e.get("date") or "Date not yet set"
            time_str = e.get("time") or "Time not yet set"
            dispatcher.utter_message(
                text=f"{e['title']} is happening on {date_str} at {time_str}."
            )
        else:
            dispatcher.utter_message(
                text=f"I couldn't find an event named '{event_name}'. "
                     f"You can ask me 'What are the upcoming events?' to see all available events."
            )
        return []
