#!/usr/bin/env python3
"""
Database Verification Script for Grace Church Chatbot
Verifies Supabase connection and table existence.
Run with: python scripts/migrate.py

NOTE: The church_info table must be created in the Supabase SQL editor first.
SQL to run in Supabase:

    CREATE TABLE IF NOT EXISTS church_info (
        id BIGSERIAL PRIMARY KEY,
        type VARCHAR(50) UNIQUE NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database, ChurchInfo


def run_migrations():
    """Verify Supabase connection and table"""
    print("\n" + "="*70)
    print("  ✝️  GRACE CHURCH CHATBOT - Supabase Verification")
    print("="*70)

    db = Database()

    print("\n[1/2] Connecting to Supabase...")
    if not db.connect():
        print("✗ Failed to connect to Supabase")
        print("\nCheck your SUPABASE_URL and SUPABASE_KEY in database.py")
        return False

    print("\n[2/2] Verifying church_info table...")
    try:
        rows = ChurchInfo.get_all(db)
        print(f"✓ church_info table found — {len(rows)} row(s) present")
    except Exception as e:
        print(f"✗ Could not access church_info table: {e}")
        print("\nMake sure you created the table in the Supabase SQL editor.")
        db.disconnect()
        return False

    db.disconnect()

    print("\n" + "="*70)
    print("✅ Verification completed successfully!")
    print("="*70)
    print("\nNext step: Run 'python scripts/seed.py' to populate with data\n")

    return True


if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
