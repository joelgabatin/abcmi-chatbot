from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .helpers import find_ministry, get_ministry_name


class ActionGetMinistryContactInfo(Action):
    def name(self) -> Text:
        return "action_get_ministry_contact_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ministry_name = get_ministry_name(tracker)
        if not ministry_name:
            dispatcher.utter_message(
                text='Which ministry do you need the contact details for? For example: "What is the contact number for the Children\'s Ministry?"'
            )
            return []

        ministry = find_ministry(tracker)
        if not ministry:
            dispatcher.utter_message(
                text=f'I could not find a ministry matching "{ministry_name}". You can ask "What are your ministries?" to see the full list.'
            )
            return []

        lines = [f"Here are the contact details for the {ministry['name']}:\n"]
        if ministry.get("contact_number"):
            lines.append(f"Contact Number: {ministry['contact_number']}")
        if ministry.get("email"):
            lines.append(f"Email: {ministry['email']}")
        if ministry.get("overseer"):
            lines.append(f"Overseer: {ministry['overseer']}")
        if ministry.get("co_leader"):
            lines.append(f"Co-Leader: {ministry['co_leader']}")

        if len(lines) == 1:
            lines.append(
                "I do not have a direct phone number or email saved for this ministry yet. You can still ask who leads it so I can point you to the right person."
            )

        dispatcher.utter_message(text="\n".join(lines))
        return []
