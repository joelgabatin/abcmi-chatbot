import os
import sys
from typing import Any, Dict, Optional, Text

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rasa_sdk import Tracker

from database import Database, Ministry


db = Database()


def get_ministry_name(tracker: Tracker) -> Optional[Text]:
    return next(
        (
            entity["value"]
            for entity in tracker.latest_message.get("entities", [])
            if entity.get("entity") == "ministry_name"
        ),
        None,
    )


def find_ministry(tracker: Tracker) -> Optional[Dict[Text, Any]]:
    db.connect()
    ministry_name = get_ministry_name(tracker)
    if not ministry_name:
        return None
    return Ministry.find_by_name(db, ministry_name)
