import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, Ministry

db = Database()


class ActionGetMinistryDescription(Action):

    def name(self) -> Text:
        return "action_get_ministry_description"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()

        ministry_name = next(
            (e["value"] for e in tracker.latest_message.get("entities", []) if e["entity"] == "ministry_name"),
            None,
        )

        if not ministry_name:
            dispatcher.utter_message(text="Which ministry would you like to know about? For example: \"Tell me about the Youth Ministry.\"")
            return []

        ministry = Ministry.find_by_name(db, ministry_name)

        if not ministry:
            dispatcher.utter_message(text=f"I couldn't find a ministry matching \"{ministry_name}\". You can ask \"What are your ministries?\" to see the full list.")
            return []

        lines = [f"Here's information about the {ministry['name']}:\n"]

        desc = ministry.get("long_description") or ministry.get("description") or ""
        if desc:
            lines.append(f"{desc}\n")

        if ministry.get("meeting_time"):
            lines.append(f"Meeting Time: {ministry['meeting_time']}")
        if ministry.get("location"):
            lines.append(f"Location: {ministry['location']}")
        if ministry.get("overseer"):
            lines.append(f"Overseer: {ministry['overseer']}")
        if ministry.get("co_leader"):
            lines.append(f"Co-Leader: {ministry['co_leader']}")

        activities = ministry.get("activities")
        if activities:
            lines.append("\nActivities:")
            for activity in activities:
                lines.append(f"  • {activity}")

        dispatcher.utter_message(text="\n".join(lines))
        return []
