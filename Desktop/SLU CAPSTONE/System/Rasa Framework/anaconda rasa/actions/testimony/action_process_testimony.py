from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from database import Testimony
from .common import db


class ActionProcessTestimony(Action):
    def name(self) -> Text:
        return "action_process_testimony"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("testimony_name") or "Anonymous"
        title = tracker.get_slot("testimony_title") or ""
        category = tracker.get_slot("testimony_category") or "Other"
        content = tracker.get_slot("testimony_content") or ""
        branch = tracker.get_slot("testimony_branch") or "Not specified"
        is_member = tracker.get_slot("testimony_is_member") or False
        is_anonymous = name.strip().lower() == "anonymous"

        result = Testimony.save(
            db,
            name=name,
            title=title,
            category=category,
            content=content,
            branch=branch,
            is_member=bool(is_member),
            is_anonymous=is_anonymous,
        )

        if result:
            display_name = "Anonymous" if is_anonymous else name
            dispatcher.utter_message(
                text=(
                    f"Thank you, Your testimony has been submitted successfully.\n\n"
                    "Our church team will review it and once approved, it will appear on our Testimony page. God bless you!"
                )
            )
        else:
            dispatcher.utter_message(
                text=(
                    "I'm sorry, I couldn't submit your testimony right now. Please try again later or visit our Testimony page to submit directly."
                )
            )

        return [
            SlotSet("testimony_name", None),
            SlotSet("testimony_title", None),
            SlotSet("testimony_category", None),
            SlotSet("testimony_content", None),
            SlotSet("testimony_branch", None),
            SlotSet("testimony_is_member", None),
        ]
