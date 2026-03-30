class Ministry:
    """Ministry data model"""

    TABLE_NAME = "ministries"

    @staticmethod
    def get_all(db):
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
