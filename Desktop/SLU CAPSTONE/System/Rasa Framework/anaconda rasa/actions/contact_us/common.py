import os
import sys
from typing import Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database import Database, SiteSettings


db = Database()
if not db.is_connected():
    db.connect()

_CONTACT_PAGE_URL_FALLBACK = "http://localhost:3000/contact"


def get_contact_page_url() -> Text:
    """Fetch the contact page URL from website_pages table."""
    try:
        response = (
            db.client.table("website_pages")
            .select("url")
            .ilike("slug", "%contact%")
            .limit(1)
            .execute()
        )
        if response.data and response.data[0].get("url"):
            return response.data[0]["url"]
    except Exception as e:
        print(f"[ERROR] Could not fetch contact page URL: {e}")
    return _CONTACT_PAGE_URL_FALLBACK


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
