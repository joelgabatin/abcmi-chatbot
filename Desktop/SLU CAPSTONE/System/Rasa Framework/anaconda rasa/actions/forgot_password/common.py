import os
import sys
from typing import Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database import Database, ForgotPasswordHelp, SiteSettings


db = Database()
if not db.is_connected():
    db.connect()

_CONTACT_PAGE_URL_FALLBACK = "http://localhost:3000/contact"


def get_forgot_password_help_text(topic: Text) -> Text:
    return ForgotPasswordHelp.get_help(topic) or ""


def get_forgot_password_page_url() -> Text:
    return ForgotPasswordHelp.get_reset_page_url(db)


def get_support_email() -> Text | None:
    return SiteSettings.get_email(db)


def get_contact_page_url() -> Text:
    try:
        response = (
            db.client.table("website_pages")
            .select("url, path")
            .ilike("slug", "%contact%")
            .limit(1)
            .execute()
        )
        if response.data:
            page = response.data[0]
            if page.get("url"):
                return page["url"]
            if page.get("path"):
                base_url = os.getenv("SITE_BASE_URL", "http://localhost:3000")
                return f"{base_url}{page['path']}"
    except Exception as e:
        print(f"[ERROR] Could not fetch contact page URL: {e}")
    return _CONTACT_PAGE_URL_FALLBACK
