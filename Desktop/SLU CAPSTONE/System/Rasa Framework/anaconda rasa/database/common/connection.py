from supabase import create_client

from config import NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY


class Database:
    """Supabase database connection handler"""

    def __init__(self):
        self.client = None
        self._connected = False

    def connect(self):
        """Establish connection to Supabase"""
        try:
            self.client = create_client(NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY)
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
