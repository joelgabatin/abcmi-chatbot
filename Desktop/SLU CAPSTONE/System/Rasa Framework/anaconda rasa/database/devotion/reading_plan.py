from calendar import monthrange
from datetime import date as date_type, timedelta
from typing import Dict, List, Optional


class ReadingPlan:
    TABLE = "weekly_reading_plans"

    @staticmethod
    def _week_start(d: date_type) -> date_type:
        """Return the Monday of d's ISO week."""
        return d - timedelta(days=d.weekday())

    @staticmethod
    def get_today(db) -> Optional[Dict]:
        today = date_type.today()
        ws = ReadingPlan._week_start(today).isoformat()
        day = today.strftime("%A")
        response = (
            db.client.table(ReadingPlan.TABLE)
            .select("*")
            .eq("week_start", ws)
            .eq("day_of_week", day)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_date(db, date_str: str) -> Optional[Dict]:
        try:
            from dateutil.parser import parse as dp
            d = dp(date_str).date()
        except Exception:
            return None
        ws = ReadingPlan._week_start(d).isoformat()
        day = d.strftime("%A")
        response = (
            db.client.table(ReadingPlan.TABLE)
            .select("*")
            .eq("week_start", ws)
            .eq("day_of_week", day)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def get_this_week(db) -> List[Dict]:
        ws = ReadingPlan._week_start(date_type.today()).isoformat()
        response = (
            db.client.table(ReadingPlan.TABLE)
            .select("*")
            .eq("week_start", ws)
            .execute()
        )
        return response.data or []

    @staticmethod
    def get_this_month(db) -> List[Dict]:
        today = date_type.today()
        return ReadingPlan._fetch_month(db, today.year, today.month)

    @staticmethod
    def get_by_month(db, year: int, month: int) -> List[Dict]:
        return ReadingPlan._fetch_month(db, year, month)

    @staticmethod
    def _fetch_month(db, year: int, month: int) -> List[Dict]:
        first = date_type(year, month, 1)
        last = date_type(year, month, monthrange(year, month)[1])
        first_ws = ReadingPlan._week_start(first).isoformat()
        response = (
            db.client.table(ReadingPlan.TABLE)
            .select("*")
            .gte("week_start", first_ws)
            .lte("week_start", last.isoformat())
            .execute()
        )
        return response.data or []

    @staticmethod
    def get_this_year(db) -> List[Dict]:
        return ReadingPlan.get_by_year(db, date_type.today().year)

    @staticmethod
    def get_by_year(db, year: int) -> List[Dict]:
        start = date_type(year, 1, 1).isoformat()
        end = date_type(year, 12, 31).isoformat()
        response = (
            db.client.table(ReadingPlan.TABLE)
            .select("*")
            .gte("week_start", start)
            .lte("week_start", end)
            .execute()
        )
        return response.data or []
