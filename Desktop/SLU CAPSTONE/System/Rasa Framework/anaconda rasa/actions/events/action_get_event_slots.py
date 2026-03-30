import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchEvent

db = Database()


class ActionGetEventSlots(Action):

    def name(self) -> Text:
        return "action_get_event_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db.connect()
        event_name = next(tracker.get_latest_entity_values("event_name"), None)
        if not event_name:
            dispatcher.utter_message(
                text="Could you please tell me which event you're asking about?"
            )
            return []

        events = ChurchEvent.find_by_name(db, event_name)
        if events:
            e = events[0]
            capacity = e.get("capacity")
            open_reg = e.get("open_registration")
            if capacity is None:
                dispatcher.utter_message(
                    text=f"Slot information for {e['title']} is not available yet."
                )
            elif not open_reg:
                dispatcher.utter_message(
                    text=f"Registration for {e['title']} is currently closed. "
                         f"The event has a capacity of {capacity} participants."
                )
            else:
                dispatcher.utter_message(
                    text=f"{e['title']} has a capacity of {capacity} participant(s) and registration is open."
                )
        else:
            dispatcher.utter_message(
                text=f"I couldn't find an event named '{event_name}'. "
                     f"You can ask me 'What are the upcoming events?' to see all available events."
            )
        return []
