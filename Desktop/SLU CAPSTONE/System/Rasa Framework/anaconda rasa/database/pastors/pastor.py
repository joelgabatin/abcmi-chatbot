class Pastor:
    """Pastor data model"""

    @staticmethod
    def get_all_with_branches(db):
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
            branch_ids = [branch["id"] for branch in branch_resp.data]
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
            for pastor in (senior.data or []) + (overseer.data or []):
                if pastor["id"] not in seen:
                    seen.add(pastor["id"])
                    results.append(pastor)
            return results
        except Exception as e:
            print(f"[ERROR] Error fetching senior pastor: {e}")
            return []

    @staticmethod
    def get_administrative_pastor(db):
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
