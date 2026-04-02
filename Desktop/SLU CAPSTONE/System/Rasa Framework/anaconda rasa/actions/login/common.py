import os
import sys
from typing import Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database import Database, LoginHelp


db = Database()
if not db.is_connected():
    db.connect()


def get_login_page_url() -> Text:
    return LoginHelp.get_login_page_url(db)


def get_login_help_text(topic: Text) -> Text:
    return LoginHelp.get_login_help(topic) or ""
