class SiteSettings:
    """Site Settings data model"""

    TABLE_NAME = "church_vmd"

    @staticmethod
    def get_about(db):
        try:
            response = (
                db.client.table(SiteSettings.TABLE_NAME)
                .select("*")
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Error fetching VMD: {e}")
            return None

    @staticmethod
    def get_mission(db):
        about = SiteSettings.get_about(db)
        if about:
            return about.get("mission_body")
        return None

    @staticmethod
    def get_vision(db):
        about = SiteSettings.get_about(db)
        if about:
            return about.get("vision_body")
        return None

    @staticmethod
    def update_about(db, about_data):
        try:
            db.client.table(SiteSettings.TABLE_NAME).update(about_data).eq("id", 1).execute()
            return True
        except Exception as e:
            print(f"[ERROR] Error updating VMD: {e}")
            return False

    @staticmethod
    def update_mission(db, mission):
        return SiteSettings.update_about(db, {"mission_body": mission})

    @staticmethod
    def get_driving_force(db):
        about = SiteSettings.get_about(db)
        if about:
            return about.get("driving_force")
        return None

    @staticmethod
    def update_vision(db, vision):
        return SiteSettings.update_about(db, {"vision_body": vision})

    @staticmethod
    def get_email(db):
        about = SiteSettings.get_about(db)
        if about:
            return about.get("email")
        return None

    @staticmethod
    def get_phone_number(db):
        about = SiteSettings.get_about(db)
        if about:
            return about.get("phone_number")
        return None

    @staticmethod
    def get_office_hours(db):
        about = SiteSettings.get_about(db)
        if about:
            return about.get("office_hours")
        return None

    @staticmethod
    def get_office_address(db):
        about = SiteSettings.get_about(db)
        if about:
            return about.get("office_address")
        return None

    @staticmethod
    def get_facebook_url(db):
        try:
            response = (
                db.client.table("site_settings")
                .select("facebook_url")
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0].get("facebook_url")
            return None
        except Exception as e:
            print(f"[ERROR] Error fetching Facebook URL from site_settings: {e}")
            return None

    @staticmethod
    def get_social_media_links(db):
        try:
            response = (
                db.client.table("site_settings")
                .select("facebook_url, tiktok_url, instagram_url, youtube_url")
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"[ERROR] Error fetching social media links from site_settings: {e}")
            return {}

    @staticmethod
    def get_social_media_url(db, platform):
        platform_columns = {
            "facebook": "facebook_url",
            "tiktok": "tiktok_url",
            "instagram": "instagram_url",
            "youtube": "youtube_url",
        }

        column = platform_columns.get((platform or "").lower())
        if not column:
            return None

        try:
            response = (
                db.client.table("site_settings")
                .select(column)
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0].get(column)
            return None
        except Exception as e:
            print(f"[ERROR] Error fetching {platform} URL from site_settings: {e}")
            return None
