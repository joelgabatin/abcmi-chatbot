import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchEvent

db = Database()

EVENTS_PAGE_URL = "http://localhost:3000/events/upcoming"


class ActionRegisterEvent(Action):

    def name(self) -> Text:
        return "action_register_event"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db.connect()
        event_name = next(tracker.get_latest_entity_values("event_name"), None)
        if not event_name:
            dispatcher.utter_message(
                text=f"I'm sorry, I can't register you directly. "
                     f"Please visit our events page to register: {EVENTS_PAGE_URL}"
            )
            return []

        events = ChurchEvent.find_by_name(db, event_name)
        if events:
            e = events[0]
            dispatcher.utter_message(
                text=f"I'm sorry, I can't register you directly for {e['title']}. "
                     f"Please visit our events page to register: {EVENTS_PAGE_URL}"
            )
        else:
            dispatcher.utter_message(
                text=f"I couldn't find an event named '{event_name}'. "
                     f"You can view all upcoming events here: {EVENTS_PAGE_URL}"
            )
        return []
