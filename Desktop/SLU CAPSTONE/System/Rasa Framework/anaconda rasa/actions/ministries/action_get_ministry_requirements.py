from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .helpers import find_ministry, get_ministry_name


class ActionGetMinistryRequirements(Action):
    def name(self) -> Text:
        return "action_get_ministry_requirements"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ministry_name = get_ministry_name(tracker)
        if not ministry_name:
            dispatcher.utter_message(
                text='Which ministry requirements would you like to know? For example: "What are the requirements to join the choir?"'
            )
            return []

        ministry = find_ministry(tracker)
        if not ministry:
            dispatcher.utter_message(
                text=f'I could not find a ministry matching "{ministry_name}". You can ask "What are your ministries?" to see the full list.'
            )
            return []

        lines = [f"Here is what I can share about joining the {ministry['name']}:\n"]
        lines.append("The general expectation is a heart to serve, willingness to attend meetings, and readiness to coordinate with the ministry leaders.")

        if ministry.get("overseer") or ministry.get("co_leader"):
            leader_names = ", ".join(
                [name for name in [ministry.get("overseer"), ministry.get("co_leader")] if name]
            )
            lines.append(f"For ministry-specific qualifications, it is best to confirm directly with: {leader_names}.")

        if ministry.get("contact_number"):
            lines.append(f"Contact Number: {ministry['contact_number']}")
        if ministry.get("email"):
            lines.append(f"Email: {ministry['email']}")

        dispatcher.utter_message(text="\n".join(lines))
        return []
