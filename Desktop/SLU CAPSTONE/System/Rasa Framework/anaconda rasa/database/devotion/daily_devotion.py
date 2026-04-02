from datetime import date as date_type
from typing import Dict, List, Optional


class DailyDevotion:
    TABLE = "daily_devotions"

    @staticmethod
    def get_today(db) -> Optional[Dict]:
        today = date_type.today().isoformat()
        response = (
            db.client.table(DailyDevotion.TABLE)
            .select("*")
            .eq("date", today)
            .eq("published", True)
            .eq("status", "active")
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_date(db, date_str: str) -> Optional[Dict]:
        response = (
            db.client.table(DailyDevotion.TABLE)
            .select("*")
            .eq("date", date_str)
            .eq("published", True)
            .eq("status", "active")
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None
