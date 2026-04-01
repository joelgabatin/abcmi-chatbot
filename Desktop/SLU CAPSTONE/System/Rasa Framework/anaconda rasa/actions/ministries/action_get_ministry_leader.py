from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .helpers import find_ministry, get_ministry_name


class ActionGetMinistryLeader(Action):
    def name(self) -> Text:
        return "action_get_ministry_leader"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ministry_name = get_ministry_name(tracker)
        if not ministry_name:
            dispatcher.utter_message(
                text='Which ministry leader are you asking about? For example: "Who leads the Music Ministry?"'
            )
            return []

        ministry = find_ministry(tracker)
        if not ministry:
            dispatcher.utter_message(
                text=f'I could not find a ministry matching "{ministry_name}". You can ask "What are your ministries?" to see the full list.'
            )
            return []

        lines = [f"Here is the leadership information for the {ministry['name']}:\n"]
        if ministry.get("overseer"):
            lines.append(f"Leader / Overseer: {ministry['overseer']}")
        if ministry.get("co_leader"):
            lines.append(f"Co-Leader: {ministry['co_leader']}")

        if len(lines) == 1:
            lines.append("I do not have the leader information saved for this ministry yet.")

        dispatcher.utter_message(text="\n".join(lines))
        return []
