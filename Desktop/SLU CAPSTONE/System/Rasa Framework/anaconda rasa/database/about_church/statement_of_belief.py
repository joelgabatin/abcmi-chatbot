class StatementOfBelief:
    """Statement of Belief data model"""

    TABLE_NAME = "church_beliefs"

    @staticmethod
    def get_all(db):
        try:
            response = (
                db.client.table(StatementOfBelief.TABLE_NAME)
                .select("id, belief")
                .order("sort_order")
                .execute()
            )
            if not response.data:
                return []
            return [{"item_number": i + 1, "statement": row["belief"]} for i, row in enumerate(response.data)]
        except Exception as e:
            print(f"[ERROR] Error fetching church beliefs: {e}")
            return []
