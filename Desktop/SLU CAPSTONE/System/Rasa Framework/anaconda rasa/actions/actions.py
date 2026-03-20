import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, SiteSettings, ChurchHistory, StatementOfBelief

db = Database()


class ActionGetMission(Action):

    def name(self) -> Text:
        return "action_get_mission"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        mission = SiteSettings.get_mission(db)
        if mission:
            dispatcher.utter_message(text=f"Our mission: {mission}")
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the mission right now."
            )
        return []


class ActionGetVision(Action):

    def name(self) -> Text:
        return "action_get_vision"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        vision = SiteSettings.get_vision(db)
        if vision:
            dispatcher.utter_message(text=f"Our vision: {vision}")
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the vision right now."
            )
        return []


class ActionGetHistory(Action):

    def name(self) -> Text:
        return "action_get_history"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        history = ChurchHistory.get_all(db)
        if history:
            lines = ["Here is the history of our church:\n"]
            for item in history:
                lines.append(f"• {item['year']}: {item['event']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the church history right now."
            )
        return []


class ActionGetStatementOfBelief(Action):

    def name(self) -> Text:
        return "action_get_statement_of_belief"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        db.connect()
        statements = StatementOfBelief.get_all(db)
        if statements:
            lines = ["Here is what ABCMI Church believes:\n"]
            for item in statements:
                lines.append(f"{item['item_number']}. {item['statement']}")
            dispatcher.utter_message(text="\n".join(lines))
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't retrieve the statement of belief right now."
            )
        return []
