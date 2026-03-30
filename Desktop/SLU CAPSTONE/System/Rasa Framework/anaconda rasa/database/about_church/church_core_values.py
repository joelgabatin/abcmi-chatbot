class ChurchCoreValues:
    """Church core values data model"""

    TABLE_NAME = "church_core_values"

    @staticmethod
    def get_all(db):
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
