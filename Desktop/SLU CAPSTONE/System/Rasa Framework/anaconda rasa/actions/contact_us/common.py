import os
import sys
from typing import Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database import Database, SiteSettings


db = Database()
if not db.is_connected():
    db.connect()


SUPPORTED_SOCIAL_MEDIA = {
    "facebook": "Facebook",
    "tiktok": "TikTok",
    "instagram": "Instagram",
    "youtube": "YouTube",
}


def get_requested_platform(latest_message: dict) -> Text | None:
    for entity in latest_message.get("entities", []):
        if entity.get("entity") == "social_platform":
            return (entity.get("value") or "").strip().lower()
    return None
