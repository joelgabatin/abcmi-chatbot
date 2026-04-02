import os
import sys
from typing import Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database import Database

db = Database()
if not db.is_connected():
    db.connect()

_DEVOTIONAL_PAGE_FALLBACK = "http://localhost:3000/devotional"
_READING_PLAN_PAGE_FALLBACK = "http://localhost:3000/bible-reading"
_BIBLE_STUDY_PAGE_FALLBACK = "http://localhost:3000/bible-study"


def _get_page_url(path: str, fallback: str) -> Text:
    try:
        response = (
            db.client.table("website_pages")
            .select("path")
            .eq("path", path)
            .eq("is_active", True)
            .limit(1)
            .execute()
        )
        if response.data and response.data[0].get("path"):
            base_url = os.getenv("SITE_BASE_URL", "http://localhost:3000")
            return f"{base_url}{response.data[0]['path']}"
    except Exception as e:
        print(f"[ERROR] Could not fetch page URL for {path}: {e}")
    return fallback


def get_devotional_page_url() -> Text:
    return _get_page_url("/devotional", _DEVOTIONAL_PAGE_FALLBACK)


def get_reading_plan_page_url() -> Text:
    return _get_page_url("/bible-reading", _READING_PLAN_PAGE_FALLBACK)
