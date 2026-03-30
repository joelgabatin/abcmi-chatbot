import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchEvent

db = Database()


class ActionGetUpcomingEvents(Action):

    def name(self) -> Text:
        return "action_get_upcoming_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db.connect()
        events = ChurchEvent.get_upcoming(db)
        if events:
            lines = [f"Here are the upcoming events of ABCMI ({len(events)} total):\n"]
            for i, e in enumerate(events, 1):
                date_str = e.get("date") or "Date TBA"
                time_str = e.get("time") or "Time TBA"
                location_str = e.get("location") or "Venue TBA"
                lines.append(f"{i}. {e['title']}")
                lines.append(f"   Date: {date_str} at {time_str}")
                lines.append(f"   Venue: {location_str}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="There are no upcoming events at the moment. Please check back later."
            )
        return []
