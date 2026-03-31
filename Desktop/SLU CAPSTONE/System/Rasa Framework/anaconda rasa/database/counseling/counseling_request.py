from datetime import date


class CounselingRequest:
    """Counseling request data model."""

    TABLE_NAME = "counseling_requests"

    @staticmethod
    def save(db, name, contact_number, concern):
        try:
            payload = {
                "full_name": name,
                "contact_number": contact_number,
                # The existing Supabase schema requires scheduling fields even when the
                # chatbot only collects a lightweight counseling request.
                "address": "Not provided via chatbot",
                "facebook_account": "Not provided",
                "preferred_date": date.today().isoformat(),
                "preferred_time": "To be arranged",
                "counseling_type": "face-to-face",
                "is_member": False,
                "concern": concern,
                "status": "pending",
            }
            response = db.client.table(CounselingRequest.TABLE_NAME).insert(payload).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error saving counseling request: {e}")
            return None
