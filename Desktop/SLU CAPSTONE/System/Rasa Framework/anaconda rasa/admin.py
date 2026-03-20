#!/usr/bin/env python3
"""
Grace Church Chatbot - Admin Panel
Update mission, vision, and other church info without SQL.
Run with: python admin.py
"""

from database import Database, ChurchInfo
import sys


def print_menu():
    """Display admin menu"""
    print("\n" + "="*70)
    print("  ✝️  GRACE CHURCH CHATBOT - Admin Panel")
    print("="*70)
    print("\n[1] View Current Mission & Vision")
    print("[2] Update Mission")
    print("[3] Update Vision")
    print("[4] View All Information")
    print("[5] Reset to Default Values")
    print("[6] Exit")
    print("\n" + "-"*70)


def view_all(db):
    """View all church information"""
    data = ChurchInfo.get_all(db)
    if not data:
        print("\n⚠ No data found in database")
        return

    print("\n📌 CURRENT CHURCH INFORMATION:")
    print("-"*70)
    for item in data:
        print(f"\n{item['type'].upper()}:")
        print(f"{item['content']}\n")


def view_mission_vision(db):
    """View just mission and vision"""
    mission = ChurchInfo.get_mission(db)
    vision = ChurchInfo.get_vision(db)

    print("\n📌 CURRENT MISSION & VISION:")
    print("-"*70)
    if mission:
        print(f"\n🎯 MISSION:\n{mission}\n")
    else:
        print("\n🎯 MISSION: Not set")

    if vision:
        print(f"✨ VISION:\n{vision}\n")
    else:
        print("✨ VISION: Not set")


def update_info(db, info_type):
    """Update church information"""
    print(f"\n{'='*70}")
    print(f"UPDATE {info_type.upper()}")
    print(f"{'='*70}")

    # Get current value
    if info_type == "mission":
        current = ChurchInfo.get_mission(db)
    else:
        current = ChurchInfo.get_vision(db)

    if current:
        print(f"\nCurrent {info_type}:\n{current}\n")

    print("\nEnter the new text (press Enter twice when done):")
    print("-"*70)

    lines = []
    empty_count = 0
    while empty_count < 1:
        line = input()
        if line == "":
            empty_count += 1
        else:
            empty_count = 0
            lines.append(line)

    new_text = "\n".join(lines).strip()

    if not new_text:
        print("\n⚠ No text entered. Cancelled.")
        return False

    # Confirm update
    print(f"\n{'='*70}")
    print(f"New {info_type}:\n{new_text}\n")
    print(f"{'='*70}")

    confirm = input("\nIs this correct? (yes/no): ").strip().lower()

    if confirm in ["yes", "y"]:
        if ChurchInfo.update(db, info_type, new_text):
            print(f"\n✅ {info_type.upper()} updated successfully!")
            return True
        else:
            print(f"\n✗ Failed to update {info_type}")
            return False
    else:
        print("\n⚠ Update cancelled.")
        return False


def reset_to_defaults(db):
    """Reset to default mission and vision"""
    from seed import CHURCH_DATA

    print("\n" + "="*70)
    print("RESET TO DEFAULT VALUES")
    print("="*70)

    print("\nThis will overwrite current mission and vision with defaults:")
    for key, value in CHURCH_DATA.items():
        print(f"\n{key.upper()}:\n{value}")

    confirm = input("\n\nContinue? (yes/no): ").strip().lower()

    if confirm in ["yes", "y"]:
        ChurchInfo.clear_all(db)
        for info_type, content in CHURCH_DATA.items():
            ChurchInfo.upsert(db, info_type, content)
        print("\n✅ Reset to defaults successfully!")
        return True
    else:
        print("\n⚠ Reset cancelled.")
        return False


def main():
    """Main admin loop"""
    db = Database()

    print("\n🔐 Connecting to Supabase...")
    if not db.connect():
        print("✗ Failed to connect to Supabase!")
        print("\nCheck your credentials in database.py")
        return False

    print("✓ Connected to Supabase")

    while True:
        print_menu()
        choice = input("Select option (1-6): ").strip()

        if choice == "1":
            view_mission_vision(db)

        elif choice == "2":
            update_info(db, "mission")

        elif choice == "3":
            update_info(db, "vision")

        elif choice == "4":
            view_all(db)

        elif choice == "5":
            reset_to_defaults(db)

        elif choice == "6":
            print("\n✓ Goodbye!\n")
            break

        else:
            print("\n⚠ Invalid option. Please select 1-6.")

    db.disconnect()
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✓ Exited. Goodbye!\n")
        sys.exit(0)
