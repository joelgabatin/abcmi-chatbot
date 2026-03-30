class ChurchEvent:
    """Church events data model"""

    TABLE_NAME = "church_events"

    @staticmethod
    def get_upcoming(db):
        try:
            response = (
                db.client.table(ChurchEvent.TABLE_NAME)
                .select("id, title, description, date, time, end_time, location, capacity, status, open_registration, registration_url, is_published")
                .ilike("status", "%upcoming%")
                .eq("is_published", True)
                .order("date")
                .execute()
            )
            if response.data:
                return response.data

            fallback = (
                db.client.table(ChurchEvent.TABLE_NAME)
                .select("id, title, description, date, time, end_time, location, capacity, status, open_registration, is_published")
                .eq("is_published", True)
                .order("date")
                .execute()
            )
            return fallback.data if fallback.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching upcoming events: {e}")
            return []

    @staticmethod
    def get_past_activities(db):
        try:
            response = (
                db.client.table(ChurchEvent.TABLE_NAME)
                .select("id, title, description, date, time, end_time, location, category")
                .eq("is_featured_past", True)
                .order("date", desc=True)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching past activities: {e}")
            return []

    @staticmethod
    def find_by_name(db, name):
        try:
            response = (
                db.client.table(ChurchEvent.TABLE_NAME)
                .select("id, title, description, date, time, end_time, location, capacity, status, open_registration, registration_url, is_published")
                .ilike("title", f"%{name}%")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error finding event '{name}': {e}")
            return []
