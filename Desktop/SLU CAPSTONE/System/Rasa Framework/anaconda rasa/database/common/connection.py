from supabase import create_client

from config import (
    NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


class Database:
    """Supabase database connection handler"""

    def __init__(self):
        self.client = None
        self._connected = False

    def connect(self):
        """Establish connection to Supabase"""
        try:
            api_key = SUPABASE_SERVICE_ROLE_KEY or NEXT_PUBLIC_SUPABASE_ANON_KEY
            self.client = create_client(NEXT_PUBLIC_SUPABASE_URL, api_key)
            self.client.table("church_vmd").select("id").limit(1).execute()
            self._connected = True
            print("[OK] Connected to Supabase database")
            return True
        except Exception as e:
            print(f"[ERROR] Error connecting to Supabase: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        self.client = None
        self._connected = False
        print("[OK] Disconnected from Supabase")

    def is_connected(self):
        return self._connected
