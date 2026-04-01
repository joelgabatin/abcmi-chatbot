from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .helpers import find_ministry, get_ministry_name


class ActionGetMinistrySchedule(Action):
    def name(self) -> Text:
        return "action_get_ministry_schedule"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ministry_name = get_ministry_name(tracker)
        if not ministry_name:
            dispatcher.utter_message(
                text='Which ministry schedule would you like to know? For example: "When does the Music Ministry meet?"'
            )
            return []

        ministry = find_ministry(tracker)
        if not ministry:
            dispatcher.utter_message(
                text=f'I could not find a ministry matching "{ministry_name}". You can ask "What are your ministries?" to see the full list.'
            )
            return []

        lines = [f"Here is the schedule for the {ministry['name']}:\n"]
        if ministry.get("meeting_time"):
            lines.append(f"Meeting Time: {ministry['meeting_time']}")
        if ministry.get("location"):
            lines.append(f"Location: {ministry['location']}")

        if len(lines) == 1:
            lines.append(
                "I do not have the meeting time saved for this ministry yet. You can ask for the ministry contact info and reach out to the leader directly."
            )

        dispatcher.utter_message(text="\n".join(lines))
        return []
