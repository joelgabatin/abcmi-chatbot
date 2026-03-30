class ChurchFounders:
    """Church founders data model"""

    TABLE_NAME = "church_founders"

    @staticmethod
    def get_all(db):
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
