import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, ChurchEvent

db = Database()


class ActionGetPastEvents(Action):

    def name(self) -> Text:
        return "action_get_past_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db.connect()
        events = ChurchEvent.get_past_activities(db)
        if events:
            lines = [f"Here are the past activities of ABCMI ({len(events)} total):\n"]
            for i, e in enumerate(events, 1):
                date_str = e.get("date") or "Date not recorded"
                time_str = e.get("time") or "Time not recorded"
                location_str = e.get("location") or "Venue not recorded"
                lines.append(f"{i}. {e['title']}")
                lines.append(f"   Date: {date_str} ")                
                lines.append(f"   Time: {time_str} ")
                lines.append(f"   Venue: {location_str}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="There are no past activities posted publicly yet."
            )
        return []
