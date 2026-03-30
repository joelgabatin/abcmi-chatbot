class ChurchBranch:
    """Church branch data model"""

    @staticmethod
    def get_all_regions(db):
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
