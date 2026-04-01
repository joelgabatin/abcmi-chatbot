class CounselingRequest:
    """Counseling request data model."""

    TABLE_NAME = "counseling_requests"

    @staticmethod
    def save(
        db,
        name,
        contact_number,
        address,
        facebook_account,
        preferred_date,
        preferred_time,
        counseling_type,
        is_member,
        concern,
    ):
        try:
            payload = {
                "full_name": name,
                "contact_number": contact_number,
                "address": address or "Not provided",
                "facebook_account": facebook_account or "Not provided",
                "preferred_date": preferred_date,
                "preferred_time": preferred_time,
                "counseling_type": counseling_type,
                "is_member": bool(is_member),
                "concern": concern,
                "status": "pending",
            }
            response = db.client.table(CounselingRequest.TABLE_NAME).insert(payload).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error saving counseling request: {e}")
            return None
