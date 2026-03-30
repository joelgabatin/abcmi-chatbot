class ChurchHistory:
    """Church history data model"""

    TABLE_NAME = "church_history"

    @staticmethod
    def get_all(db):
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
