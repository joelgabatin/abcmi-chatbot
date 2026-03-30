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
                .select("*")
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

    @staticmethod
    def get_email(db):
        """Get church email from church_vmd"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("email")
        return None

    @staticmethod
    def get_phone_number(db):
        """Get church phone number from church_vmd"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("phone_number")
        return None

    @staticmethod
    def get_office_hours(db):
        """Get church office hours from church_vmd"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("office_hours")
        return None

    @staticmethod
    def get_office_address(db):
        """Get church office address from church_vmd"""
        about = SiteSettings.get_about(db)
        if about:
            return about.get("office_address")
        return None

    @staticmethod
    def get_facebook_url(db):
        """Get church Facebook URL from site settings"""
        try:
            response = (
                db.client.table("site_settings")
                .select("facebook_url")
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0].get("facebook_url")
            return None
        except Exception as e:
            print(f"[ERROR] Error fetching Facebook URL from site_settings: {e}")
            return None

    @staticmethod
    def get_social_media_links(db):
        """Get supported church social media links from site settings"""
        try:
            response = (
                db.client.table("site_settings")
                .select("facebook_url, tiktok_url, instagram_url, youtube_url")
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"[ERROR] Error fetching social media links from site_settings: {e}")
            return {}

    @staticmethod
    def get_social_media_url(db, platform):
        """Get a specific social media URL from site settings"""
        platform_columns = {
            "facebook": "facebook_url",
            "tiktok": "tiktok_url",
            "instagram": "instagram_url",
            "youtube": "youtube_url",
        }

        column = platform_columns.get((platform or "").lower())
        if not column:
            return None

        try:
            response = (
                db.client.table("site_settings")
                .select(column)
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0].get(column)
            return None
        except Exception as e:
            print(f"[ERROR] Error fetching {platform} URL from site_settings: {e}")
            return None



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

    @staticmethod
    def find_by_name(db, name):
        """Find an active branch by partial name match (case-insensitive)"""
        try:
            response = (
                db.client.table("branches")
                .select("id, name, location")
                .ilike("name", f"%{name}%")
                .eq("status", "active")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error finding branch by name: {e}")
            return []

    @staticmethod
    def get_main_branch(db):
        """Get the main/headquarters branch (is_main=true, or fallback to name match)"""
        try:
            response = (
                db.client.table("branches")
                .select("id, name, location")
                .eq("is_main", True)
                .eq("status", "active")
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            # Fallback: look for a branch with 'main' in the name
            fallback = (
                db.client.table("branches")
                .select("id, name, location")
                .ilike("name", "%main%")
                .eq("status", "active")
                .limit(1)
                .execute()
            )
            return fallback.data[0] if fallback.data else None
        except Exception as e:
            print(f"[ERROR] Error fetching main branch: {e}")
            return None

    @staticmethod
    def get_branches_by_region_name(db, region_name):
        """Get all active branches in a region matched by name (case-insensitive partial match)"""
        try:
            region_resp = (
                db.client.table("regions")
                .select("id, name")
                .ilike("name", f"%{region_name}%")
                .execute()
            )
            if not region_resp.data:
                return []
            region_id = region_resp.data[0]["id"]
            response = (
                db.client.table("branches")
                .select("id, name, location")
                .eq("region_id", region_id)
                .eq("status", "active")
                .order("name")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching branches by region name '{region_name}': {e}")
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
    def get_resident_pastor_by_branch(db, branch_id):
        """Get the resident pastor(s) for a given branch (role contains 'Resident')"""
        try:
            response = (
                db.client.table("pastors")
                .select("id, name, role")
                .eq("branch_id", branch_id)
                .eq("status", "active")
                .ilike("role", "%resident%")
                .execute()
            )
            if response.data:
                return response.data
            # Fallback: return any active pastor at that branch
            fallback = (
                db.client.table("pastors")
                .select("id, name, role")
                .eq("branch_id", branch_id)
                .eq("status", "active")
                .execute()
            )
            return fallback.data if fallback.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching resident pastor for branch {branch_id}: {e}")
            return []

    @staticmethod
    def get_by_region_name(db, region_name):
        """Get all active pastors in branches belonging to a region (partial name match)"""
        try:
            region_resp = (
                db.client.table("regions")
                .select("id, name")
                .ilike("name", f"%{region_name}%")
                .execute()
            )
            if not region_resp.data:
                return []
            region_id = region_resp.data[0]["id"]
            branch_resp = (
                db.client.table("branches")
                .select("id")
                .eq("region_id", region_id)
                .eq("status", "active")
                .execute()
            )
            if not branch_resp.data:
                return []
            branch_ids = [b["id"] for b in branch_resp.data]
            response = (
                db.client.table("pastors")
                .select("id, name, role, branch_id, branches(name, location)")
                .eq("status", "active")
                .in_("branch_id", branch_ids)
                .order("name")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching pastors by region '{region_name}': {e}")
            return []

    @staticmethod
    def get_senior_pastor(db):
        """Get pastors with 'Senior' or 'Overseer' in their role"""
        try:
            senior = (
                db.client.table("pastors")
                .select("id, name, role")
                .eq("status", "active")
                .ilike("role", "%senior%")
                .execute()
            )
            overseer = (
                db.client.table("pastors")
                .select("id, name, role")
                .eq("status", "active")
                .ilike("role", "%overseer%")
                .execute()
            )
            seen = set()
            results = []
            for p in (senior.data or []) + (overseer.data or []):
                if p["id"] not in seen:
                    seen.add(p["id"])
                    results.append(p)
            return results
        except Exception as e:
            print(f"[ERROR] Error fetching senior pastor: {e}")
            return []

    @staticmethod
    def get_administrative_pastor(db):
        """Get pastors with 'Administrative' in their role"""
        try:
            response = (
                db.client.table("pastors")
                .select("id, name, role")
                .eq("status", "active")
                .ilike("role", "%administrative%")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching administrative pastor: {e}")
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


class ChurchEvent:
    """Church Events Data Model — reads from the church_events table"""

    TABLE_NAME = "church_events"

    @staticmethod
    def get_upcoming(db):
        """Get all upcoming events ordered by date"""
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
            # Fallback: all published events regardless of status
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
        """Get all events marked as featured past activities (is_featured_past=true)"""
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
        """Find an event by partial title match (case-insensitive)"""
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


class PrayerRequest:
    """Prayer Request Data Model — writes to the prayer_requests table"""

    TABLE_NAME = "prayer_requests"

    @staticmethod
    def save(db, name, contact, address, request, face_to_face):
        """Insert a new prayer request record"""
        try:
            payload = {
                "name": name,
                "contact": contact,
                "address": address,
                "request": request,
                "face_to_face": face_to_face,
            }
            response = (
                db.client.table(PrayerRequest.TABLE_NAME)
                .insert(payload)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error saving prayer request: {e}")
            return None


class Ministry:
    """Ministry Data Model — reads from the ministries table"""

    TABLE_NAME = "ministries"

    @staticmethod
    def get_all(db):
        """Get all visible ministries"""
        try:
            response = (
                db.client.table(Ministry.TABLE_NAME)
                .select("id, name, description, meeting_time, location, overseer, contact_number, email")
                .eq("visible", True)
                .order("name")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching ministries: {e}")
            return []

    @staticmethod
    def find_by_name(db, name):
        """Find a ministry by name (case-insensitive partial match)"""
        try:
            response = (
                db.client.table(Ministry.TABLE_NAME)
                .select("id, name, description, long_description, meeting_time, location, overseer, co_leader, contact_number, email, activities")
                .eq("visible", True)
                .ilike("name", f"%{name}%")
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error finding ministry: {e}")
            return None


class ChurchFounders:
    """Church Founders Data Model — reads from the church_founders table"""

    TABLE_NAME = "church_founders"

    @staticmethod
    def get_all(db):
        """Get all founders ordered by sort_order"""
        try:
            response = (
                db.client.table(ChurchFounders.TABLE_NAME)
                .select("id, name, title, role, description")
                .order("sort_order")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"[ERROR] Error fetching church founders: {e}")
            return []
