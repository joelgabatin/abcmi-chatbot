import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import Database, StatementOfBelief

db = Database()


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
