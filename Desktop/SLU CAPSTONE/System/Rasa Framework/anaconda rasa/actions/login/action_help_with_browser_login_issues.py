from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .common import get_login_help_text


class ActionHelpWithBrowserLoginIssues(Action):
    def name(self) -> Text:
        return "action_help_with_browser_login_issues"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_login_help_text("browser_issues"))
        return []
