class ContactMessage:
    """Contact message data model"""

    TABLE_NAME = "contact_messages"

    @staticmethod
    def save(db, name, email, message, phone_number=None, subject=None):
        try:
            payload = {
                "name": name,
                "email": email,
                "message": message,
            }
            if phone_number:
                payload["phone"] = phone_number
            if subject:
                payload["subject"] = subject
            response = db.client.table(ContactMessage.TABLE_NAME).insert(payload).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error saving contact message: {e}")
            return None
