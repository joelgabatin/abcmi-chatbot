import os
import sys
from typing import Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database import Database

db = Database()
if not db.is_connected():
    db.connect()

_TESTIMONY_PAGE_FALLBACK = "http://localhost:3000/testimony"


def get_testimony_page_url() -> Text:
    try:
        response = (
            db.client.table("website_pages")
            .select("path")
            .eq("path", "/testimony")
            .eq("is_active", True)
            .limit(1)
            .execute()
        )
        if response.data and response.data[0].get("path"):
            base_url = os.getenv("SITE_BASE_URL", "http://localhost:3000")
            return f"{base_url}{response.data[0]['path']}"
    except Exception as e:
        print(f"[ERROR] Could not fetch testimony page URL: {e}")
    return _TESTIMONY_PAGE_FALLBACK
