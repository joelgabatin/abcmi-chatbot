from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .helpers import find_ministry, get_ministry_name


class ActionGetMinistryActivities(Action):
    def name(self) -> Text:
        return "action_get_ministry_activities"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ministry_name = get_ministry_name(tracker)
        if not ministry_name:
            dispatcher.utter_message(
                text='Which ministry activities would you like to know? For example: "What activities does the Music Ministry have?"'
            )
            return []

        ministry = find_ministry(tracker)
        if not ministry:
            dispatcher.utter_message(
                text=f'I could not find a ministry matching "{ministry_name}". You can ask "What are your ministries?" to see the full list.'
            )
            return []

        activities = ministry.get("activities") or []
        if not activities:
            dispatcher.utter_message(
                text=f"I do not have any activities listed yet for the {ministry['name']}. You can ask for the ministry description or contact info for more details."
            )
            return []

        lines = [f"Here are the activities of the {ministry['name']}:\n"]
        for index, activity in enumerate(activities, 1):
            lines.append(f"{index}. {activity}")

        dispatcher.utter_message(text="\n".join(lines))
        return []
