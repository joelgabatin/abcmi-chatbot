"""
Database Configuration and Models
For Grace Church Chatbot - Supabase Backend
"""

from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = "https://mddptbrpkswbmkovsldw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1kZHB0YnJwa3N3Ym1rb3ZzbGR3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM3Mjc5MDIsImV4cCI6MjA4OTMwMzkwMn0.XolzOBVy4NoEzKcnM0lm8DPm57WNVb5CLpdU7-LtXZ0"


class Database:
    """Supabase database connection handler"""

    def __init__(self):
        self.client = None
        self._connected = False

    def connect(self):
        """Establish connection to Supabase"""
        try:
            self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
            # Test connection with a lightweight query
            self.client.table("about_section").select("id").limit(1).execute()
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
    """Site Settings Data Model — reads from the about_section table"""

    TABLE_NAME = "about_section"

    @staticmethod
    def get_about(db):
        """Get the about section row from about_section table"""
        try:
            response = (
                db.client.table(SiteSettings.TABLE_NAME)
                .select("mission, vision")
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error fetching about section: {e}")
            return None

    @staticmethod
    def get_mission(db):
        """Get church mission from about_section"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("mission")
        return None

    @staticmethod
    def get_vision(db):
        """Get church vision from about_section"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("vision")
        return None

    @staticmethod
    def update_about(db, about_data):
        """Update the about_section row with new data"""
        try:
            db.client.table(SiteSettings.TABLE_NAME).update(about_data).neq("id", "00000000-0000-0000-0000-000000000000").execute()
            return True
        except Exception as e:
            print(f"[ERROR] Error updating about section: {e}")
            return False

    @staticmethod
    def update_mission(db, mission):
        """Update only the mission field in about_section"""
        return SiteSettings.update_about(db, {"mission": mission})

    @staticmethod
    def update_vision(db, vision):
        """Update only the vision field in about_section"""
        return SiteSettings.update_about(db, {"vision": vision})


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
