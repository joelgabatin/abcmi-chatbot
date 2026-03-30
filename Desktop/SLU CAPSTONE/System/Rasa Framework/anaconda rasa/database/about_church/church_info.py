from .site_settings import SiteSettings


class ChurchInfo:
    """Legacy church information model kept for backwards compatibility"""

    TABLE_NAME = "church_info"

    @staticmethod
    def get_mission(db):
        return SiteSettings.get_mission(db)

    @staticmethod
    def get_vision(db):
        return SiteSettings.get_vision(db)

    @staticmethod
    def get_all(db):
        about = SiteSettings.get_about(db)
        if not about:
            return []
        return [{"type": key, "content": value} for key, value in about.items()]

    @staticmethod
    def update(db, info_type, content):
        if info_type == "mission":
            return SiteSettings.update_mission(db, content)
        if info_type == "vision":
            return SiteSettings.update_vision(db, content)
        about = SiteSettings.get_about(db) or {}
        about[info_type] = content
        return SiteSettings.update_about(db, about)

    @staticmethod
    def upsert(db, info_type, content):
        return ChurchInfo.update(db, info_type, content)

    @staticmethod
    def clear_all(db):
        return SiteSettings.update_about(db, {})

    @staticmethod
    def create_table(db):
        print("[INFO] Table creation is managed via the Supabase SQL editor.")
        return True
