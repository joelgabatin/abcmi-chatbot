class PrayerRequest:
    """Prayer request data model"""

    TABLE_NAME = "prayer_requests"

    @staticmethod
    def save(db, name, contact, address, request, face_to_face):
        try:
            payload = {
                "name": name,
                "contact": contact,
                "address": address,
                "request": request,
                "face_to_face": face_to_face,
            }
            response = db.client.table(PrayerRequest.TABLE_NAME).insert(payload).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error saving prayer request: {e}")
            return None
