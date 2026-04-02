import re
from typing import Dict, Optional


class DevotionSubscriber:
    TABLE = "devotion_subscribers"

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def subscribe(db, email: str, email_notifications: bool = True) -> Optional[Dict]:
        try:
            email = email.strip().lower()
            response = (
                db.client.table(DevotionSubscriber.TABLE)
                .upsert(
                    {
                        "email": email,
                        "email_notifications": email_notifications,
                        "status": "active",
                        "subscribed_via": "chatbot",
                    },
                    on_conflict="email",
                )
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] DevotionSubscriber.subscribe: {e}")
            return None
