"""
Database Configuration and Models
For Grace Church Chatbot - Supabase Backend
"""

from supabase import create_client, Client

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL="https://hxeyrlacblbbfflfyqyb.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh4ZXlybGFjYmxiYmZmbGZ5cXliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwODE2MDksImV4cCI6MjA4OTY1NzYwOX0.kE-8Dj2o1jUIIvLOlB21r0jq_Fo5NDXXiotiYp37Nto"
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh4ZXlybGFjYmxiYmZmbGZ5cXliIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDA4MTYwOSwiZXhwIjoyMDg5NjU3NjA5fQ.SlRUHp8XfvCjaHjuuQdKB4SwWEnxaq03AgTWae3arns"

class Database:
    """Supabase database connection handler"""

    def __init__(self):
        self.client = None
        self._connected = False

    def connect(self):
        """Establish connection to Supabase"""
        try:
            self.client = create_client(NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY)
            # Test connection with a lightweight query
            self.client.table("church_VMD").select("id").limit(1).execute()
            self._connected = True
            print("[OK] Connected to Supabase database")
            return True
        except Exception as e:
            print(f"[ERROR] Error connecting to Supabase: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        self.client = None
        self._connected = False
        print("[OK] Disconnected from Supabase")

    def is_connected(self):
        return self._connected


class SiteSettings:
    """Site Settings Data Model — reads from the church_VMD table"""

    TABLE_NAME = "church_VMD"

    @staticmethod
    def get_about(db):
        """Get the VMD row from church_VMD table"""
        try:
            response = (
                db.client.table(SiteSettings.TABLE_NAME)
                .select("mission_body, vision_body, driving_force")
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error fetching VMD: {e}")
            return None

    @staticmethod
    def get_mission(db):
        """Get church mission from church_VMD"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("mission_body")
        return None

    @staticmethod
    def get_vision(db):
        """Get church vision from church_VMD"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("vision_body")
        return None

    @staticmethod
    def update_about(db, about_data):
        """Update the church_VMD row with new data"""
        try:
            db.client.table(SiteSettings.TABLE_NAME).update(about_data).eq("id", 1).execute()
            return True
        except Exception as e:
            print(f"[ERROR] Error updating VMD: {e}")
            return False

    @staticmethod
    def update_mission(db, mission):
        """Update only the mission field in church_VMD"""
        return SiteSettings.update_about(db, {"mission_body": mission})

    @staticmethod
    def get_driving_force(db):
        """Get church driving force from church_VMD"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("driving_force")
        return None

    @staticmethod
    def update_vision(db, vision):
        """Update only the vision field in church_VMD"""
        return SiteSettings.update_about(db, {"vision_body": vision})


class StatementOfBelief:
    """Statement of Belief Data Model — reads from the church_beliefs table"""

    TABLE_NAME = "church_beliefs"

    @staticmethod
    def get_all(db):
        """Get all beliefs ordered by sort_order"""
        try:
            response = (
                db.client.table(StatementOfBelief.TABLE_NAME)
                .select("id, belief")
                .order("sort_order")
                .execute()
            )
            # Normalize to item_number/statement for compatibility with grace_api.py
            return [{"item_number": i + 1, "statement": row["belief"]} for i, row in enumerate(response.data)] if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching church beliefs: {e}")
            return []


class ChurchHistory:
    """Church History Data Model — reads from the church_history table"""

    TABLE_NAME = "church_history"

    @staticmethod
    def get_all(db):
        """Get all church history records ordered by display_order"""
        try:
            response = (
                db.client.table(ChurchHistory.TABLE_NAME)
                .select("year, event")
                .order("sort_order")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching church history: {e}")
            return []


class ChurchCoreValues:
    """Church Core Values Data Model — reads from the church_core_values table"""

    TABLE_NAME = "church_core_values"

    @staticmethod
    def get_all(db):
        """Get all core values ordered by sort_order"""
        try:
            response = (
                db.client.table(ChurchCoreValues.TABLE_NAME)
                .select("title")
                .order("sort_order")
                .execute()
            )
            return [{"title": row["title"]} for row in response.data] if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching church core values: {e}")
            return []


class ChurchInfo:
    """Church Information Data Model (legacy — kept for backwards compatibility)"""

    TABLE_NAME = "church_info"

    @staticmethod
    def get_mission(db):
        return SiteSettings.get_mission(db)

    @staticmethod
    def get_vision(db):
        return SiteSettings.get_vision(db)

    @staticmethod
    def get_all(db):
        """Get all church information from site_settings about JSON"""
        about = SiteSettings.get_about(db)
        if not about:
            return []
        return [{"type": k, "content": v} for k, v in about.items()]

    @staticmethod
    def update(db, info_type, content):
        """Update church information — writes into site_settings about JSON"""
        if info_type == "mission":
            return SiteSettings.update_mission(db, content)
        elif info_type == "vision":
            return SiteSettings.update_vision(db, content)
        # fallback for other types: patch the about JSON directly
        about = SiteSettings.get_about(db) or {}
        about[info_type] = content
        return SiteSettings.update_about(db, about)

    @staticmethod
    def upsert(db, info_type, content):
        """Insert or update church information in site_settings about JSON"""
        return ChurchInfo.update(db, info_type, content)

    @staticmethod
    def clear_all(db):
        """Reset the about JSON to empty"""
        return SiteSettings.update_about(db, {})

    @staticmethod
    def create_table(db):
        """Table is managed in the Supabase dashboard — this is a no-op."""
        print("[INFO] Table creation is managed via the Supabase SQL editor.")
        return True
