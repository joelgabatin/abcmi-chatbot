"""
Database Configuration and Models
For Grace Church Chatbot - Supabase Backend
"""

from supabase import create_client, Client
from config import NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY

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
            self.client.table("church_vmd").select("id").limit(1).execute()
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
    """Site Settings Data Model — reads from the church_vmd table"""

    TABLE_NAME = "church_vmd"

    @staticmethod
    def get_about(db):
        """Get the VMD row from church_vmd table"""
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
        """Get church mission from church_vmd"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("mission_body")
        return None

    @staticmethod
    def get_vision(db):
        """Get church vision from church_vmd"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("vision_body")
        return None

    @staticmethod
    def update_about(db, about_data):
        """Update the church_vmd row with new data"""
        try:
            db.client.table(SiteSettings.TABLE_NAME).update(about_data).eq("id", 1).execute()
            return True
        except Exception as e:
            print(f"[ERROR] Error updating VMD: {e}")
            return False

    @staticmethod
    def update_mission(db, mission):
        """Update only the mission field in church_vmd"""
        return SiteSettings.update_about(db, {"mission_body": mission})

    @staticmethod
    def get_driving_force(db):
        """Get church driving force from church_vmd"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("driving_force")
        return None

    @staticmethod
    def update_vision(db, vision):
        """Update only the vision field in church_vmd"""
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


class ChurchBranch:
    """Church Branch Data Model — reads from branches, regions, pastors, service_schedules tables"""

    @staticmethod
    def get_all_regions(db):
        """Get all regions"""
        try:
            response = (
                db.client.table("regions")
                .select("id, name")
                .order("name")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching regions: {e}")
            return []

    @staticmethod
    def get_branches_by_region(db, region_id):
        """Get all active branches in a region"""
        try:
            response = (
                db.client.table("branches")
                .select("id, name, location, established")
                .eq("region_id", region_id)
                .eq("status", "active")
                .order("name")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching branches by region: {e}")
            return []

    @staticmethod
    def get_branch_details(db, branch_id):
        """Get full branch details including pastors and service schedules"""
        try:
            branch_resp = (
                db.client.table("branches")
                .select("id, name, location")
                .eq("id", branch_id)
                .limit(1)
                .execute()
            )
            branch = branch_resp.data[0] if branch_resp.data else None
            if not branch:
                return None

            pastor_resp = (
                db.client.table("pastors")
                .select("name, role")
                .eq("branch_id", branch_id)
                .eq("status", "active")
                .execute()
            )
            branch["pastors"] = pastor_resp.data if pastor_resp.data else []

            schedule_resp = (
                db.client.table("service_schedules")
                .select("day, time, type, description")
                .eq("branch_id", branch_id)
                .execute()
            )
            branch["schedules"] = schedule_resp.data if schedule_resp.data else []

            return branch
        except Exception as e:
            print(f"[ERROR] Error fetching branch details: {e}")
            return None

    @staticmethod
    def get_total_count(db):
        """Get total count of all active branches"""
        try:
            response = (
                db.client.table("branches")
                .select("id")
                .eq("status", "active")
                .execute()
            )
            return len(response.data) if response.data is not None else 0
        except Exception as e:
            print(f"[ERROR] Error counting total branches: {e}")
            return None

    @staticmethod
    def get_local_branches(db):
        """Get all active local branches (excludes International region)"""
        try:
            int_resp = (
                db.client.table("regions")
                .select("id")
                .eq("name", "International")
                .execute()
            )
            int_region_id = int_resp.data[0]["id"] if int_resp.data else None

            query = (
                db.client.table("branches")
                .select("id, name, location")
                .eq("status", "active")
                .order("name")
            )
            if int_region_id:
                query = query.neq("region_id", int_region_id)
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching local branches: {e}")
            return []

    @staticmethod
    def get_international_branches(db):
        """Get all active branches in the International region"""
        try:
            int_resp = (
                db.client.table("regions")
                .select("id")
                .eq("name", "International")
                .execute()
            )
            if not int_resp.data:
                return []
            int_region_id = int_resp.data[0]["id"]
            response = (
                db.client.table("branches")
                .select("id, name, location")
                .eq("status", "active")
                .eq("region_id", int_region_id)
                .order("name")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching international branches: {e}")
            return []


class Pastor:
    """Pastor Data Model — reads from the pastors table with branch info"""

    @staticmethod
    def get_all_with_branches(db):
        """Get all active pastors joined with their branch name and location"""
        try:
            response = (
                db.client.table("pastors")
                .select("id, name, role, branch_id, branches(name, location)")
                .eq("status", "active")
                .order("name")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching all pastors: {e}")
            return []

    @staticmethod
    def find_by_name(db, name):
        """Find active pastors by name (case-insensitive partial match)"""
        try:
            response = (
                db.client.table("pastors")
                .select("id, name, role, branch_id, branches(name, location)")
                .eq("status", "active")
                .ilike("name", f"%{name}%")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error finding pastor '{name}': {e}")
            return []

    @staticmethod
    def get_branch_schedule(db, branch_id):
        """Get all service schedules for a given branch"""
        try:
            response = (
                db.client.table("service_schedules")
                .select("day, time, type, description")
                .eq("branch_id", branch_id)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching schedule for branch {branch_id}: {e}")
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
