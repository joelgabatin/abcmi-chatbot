#!/usr/bin/env python3
"""
Database Seeding Script for Grace Church Chatbot
Populates Supabase with mission and vision data.
Run with: python seed.py
"""

from database import Database, ChurchInfo, SiteSettings
import sys

# Church Information Data
CHURCH_DATA = {
    "mission": "Our mission at Grace Church is to spread God's love, serve our community with compassion, and equip believers to grow in faith and make a positive impact in the world.",
    "vision": "Our vision is to be a thriving community of faith where all people feel welcomed, valued, and empowered to live out their God-given purpose and transform the world with God's love."
}


def seed_database():
    """Seed database with church information"""
    print("\n" + "="*70)
    print("  ✝️  GRACE CHURCH CHATBOT - Database Seeding")
    print("="*70)

    db = Database()

    print("\n[1/3] Connecting to Supabase...")
    if not db.connect():
        print("✗ Failed to connect to Supabase")
        return False

    print("✓ Connected to Supabase")

    print("\n[2/3] Updating mission and vision in about_section...")
    if SiteSettings.update_about(db, CHURCH_DATA):
        print("✓ Mission and vision updated successfully")
    else:
        print("✗ Failed to update data")
        db.disconnect()
        return False

    # Verify seeded data
    print("\n" + "="*70)
    print("Seeded Data")
    print("="*70)

    about = SiteSettings.get_about(db) or {}
    for key, value in about.items():
        print(f"\n📌 {key.upper()}:")
        print(f"   {value}")

    db.disconnect()

    print("\n" + "="*70)
    print("✅ Seeding completed successfully!")
    print("="*70)
    print("\nYou can now start the chatbot with: python grace_api.py\n")

    return True


if __name__ == "__main__":
    success = seed_database()
    sys.exit(0 if success else 1)
