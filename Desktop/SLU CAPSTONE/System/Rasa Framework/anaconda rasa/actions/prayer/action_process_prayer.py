import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from database import Database, PrayerRequest

db = Database()

# ── Comforting Bible verses ───────────────────────────────────────────────────
BIBLE_VERSES = [
    '"Cast all your anxiety on Him because He cares for you." — 1 Peter 5:7',
    '"The Lord is close to the brokenhearted and saves those who are crushed in spirit." — Psalm 34:18',
    '"Come to me, all you who are weary and burdened, and I will give you rest." — Matthew 11:28',
    '"Do not be anxious about anything, but in every situation, by prayer and petition, '
    'with thanksgiving, present your requests to God." — Philippians 4:6',
    '"For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, '
    'plans to give you hope and a future." — Jeremiah 29:11',
    '"The Lord himself goes before you and will be with you; He will never leave you nor forsake you." — Deuteronomy 31:8',
    '"He heals the brokenhearted and binds up their wounds." — Psalm 147:3',
    '"I can do all this through Him who gives me strength." — Philippians 4:13',
]


class ActionProcessPrayer(Action):

    def name(self) -> Text:
        return "action_process_prayer"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # ── Extract slots ─────────────────────────────────────────────────────
        name         = tracker.get_slot("prayer_name") or "Friend"
        phone        = tracker.get_slot("prayer_phone") or "Not provided"
        address      = tracker.get_slot("prayer_address") or "Not provided"
        request      = tracker.get_slot("prayer_request") or ""
        face_to_face = tracker.get_slot("prayer_face_to_face")

        # ── Save to database ──────────────────────────────────────────────────
        db.connect()

        PrayerRequest.save(
            db,
            name=name,
            contact=phone,
            address=address,
            request=request,
            face_to_face=bool(face_to_face),
        )

        # ── Build closing message ─────────────────────────────────────────────
        face_msg = (
            "One of our pastors will reach out to arrange a visit with you. 🤝"
            if face_to_face
            else "Our prayer team will keep you in their prayers. 🙏"
        )

        verse = random.choice(BIBLE_VERSES)

        dispatcher.utter_message(
            text=(
                f"Thank you, {name}. Your prayer request has been received by our prayer team. 🙏\n\n"
                f"{face_msg}\n\n"
                "Remember, you don't need to be a member to be loved and prayed for. "
                "This church's doors — and hearts — are open to everyone.\n\n"
                f"Here is a verse for you today:\n\n{verse}"
            )
        )

        return [AllSlotsReset()]
