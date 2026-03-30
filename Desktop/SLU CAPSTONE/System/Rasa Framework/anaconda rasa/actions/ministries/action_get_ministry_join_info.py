import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, Ministry

db = Database()


class ActionGetMinistryJoinInfo(Action):

    def name(self) -> Text:
        return "action_get_ministry_join_info"

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
            dispatcher.utter_message(text="Which ministry would you like to join? For example: \"I want to join the Youth Ministry.\"")
            return []

        ministry = Ministry.find_by_name(db, ministry_name)

        if not ministry:
            dispatcher.utter_message(text=f"I couldn't find a ministry matching \"{ministry_name}\". You can ask \"What are your ministries?\" to see the full list.")
            return []

        lines = [f"Great interest in joining the {ministry['name']}! 🙌\n"]
        lines.append("Here's how you can get in touch:\n")

        if ministry.get("overseer"):
            lines.append(f"Ministry Overseer: {ministry['overseer']}")
        if ministry.get("co_leader"):
            lines.append(f"Co-Leader: {ministry['co_leader']}")
        if ministry.get("contact_number"):
            lines.append(f"Contact Number: {ministry['contact_number']}")
        if ministry.get("email"):
            lines.append(f"Email: {ministry['email']}")
        if ministry.get("meeting_time"):
            lines.append(f"They meet: {ministry['meeting_time']}")
        if ministry.get("location"):
            lines.append(f"Location: {ministry['location']}")

        lines.append("\nFeel free to reach out to them directly — they'd love to have you!")
        dispatcher.utter_message(text="\n".join(lines))
        return []
