import os
import sys
from typing import Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database import Database


db = Database()
if not db.is_connected():
    db.connect()

_COUNSELING_PAGE_URL_FALLBACK = "http://localhost:3000/counseling"


def get_counseling_page_url() -> Text:
    """Fetch the counseling page URL from website_pages table."""
    try:
        response = (
            db.client.table("website_pages")
            .select("url")
            .ilike("slug", "%counsel%")
            .limit(1)
            .execute()
        )
        if response.data and response.data[0].get("url"):
            return response.data[0]["url"]
    except Exception as e:
        print(f"[ERROR] Could not fetch counseling page URL: {e}")
    return _COUNSELING_PAGE_URL_FALLBACK
