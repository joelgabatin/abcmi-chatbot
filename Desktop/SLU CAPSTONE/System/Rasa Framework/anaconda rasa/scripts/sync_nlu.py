#!/usr/bin/env python3
"""
sync_nlu.py — Sync select_region and select_branch NLU examples from the database.

Run this before `rasa train` whenever regions or branches change in Supabase:
    python scripts/sync_nlu.py
    rasa train
"""

import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database, ChurchBranch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NLU_FILE = os.path.join(ROOT, "data", "nlu.yml")

# Static extra examples per region to help Rasa recognize natural phrasing
REGION_ALIASES = {
    "CAR": ["CAR", "Cordillera", "Cordillera Administrative Region", "I'm in CAR", "CAR region"],
    "Region I": ["Region I", "Region 1", "Ilocos", "Ilocos region", "Region I please"],
    "Region II": ["Region II", "Region 2", "Cagayan Valley", "Region II please"],
    "Region III": ["Region III", "Region 3", "Central Luzon", "Region III please"],
    "International": ["International", "international branch", "abroad", "overseas"],
}


def build_select_region_block(regions):
    lines = ["- intent: select_region", "  examples: |"]
    seen = set()
    for i, r in enumerate(regions, 1):
        name = r["name"]
        # Add number shortcut
        example = f"    - {i}"
        if example not in seen:
            lines.append(example)
            seen.add(example)
        # Add exact name
        example = f"    - {name}"
        if example not in seen:
            lines.append(example)
            seen.add(example)
        # Add aliases if defined
        for alias in REGION_ALIASES.get(name, []):
            example = f"    - {alias}"
            if example not in seen:
                lines.append(example)
                seen.add(example)
    return "\n".join(lines)


def build_select_branch_block(regions, db):
    lines = ["- intent: select_branch", "  examples: |"]
    seen = set()
    counter = 1
    for r in regions:
        branches = ChurchBranch.get_branches_by_region(db, r["id"])
        for b in branches:
            example = f"    - {counter}"
            if example not in seen:
                lines.append(example)
                seen.add(example)
            example = f"    - {b['name']}"
            if example not in seen:
                lines.append(example)
                seen.add(example)
            # Also add a short version (e.g. "Camp 8" from "Camp 8 Branch")
            short = b["name"].replace(" Branch", "").replace(" Church", "").strip()
            if short != b["name"]:
                example = f"    - {short}"
                if example not in seen:
                    lines.append(example)
                    seen.add(example)
            counter += 1
    return "\n".join(lines)


def update_nlu_file(new_region_block, new_branch_block):
    with open(NLU_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace select_region block
    content = re.sub(
        r"- intent: select_region\n  examples: \|.*?(?=\n- intent:|\Z)",
        new_region_block + "\n",
        content,
        flags=re.DOTALL,
    )

    # Replace select_branch block
    content = re.sub(
        r"- intent: select_branch\n  examples: \|.*?(?=\n- intent:|\Z)",
        new_branch_block + "\n",
        content,
        flags=re.DOTALL,
    )

    with open(NLU_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("Connecting to database...")
    db = Database()
    if not db.connect():
        print("[ERROR] Could not connect to database.")
        return

    print("Fetching regions...")
    regions = ChurchBranch.get_all_regions(db)
    if not regions:
        print("[ERROR] No regions found.")
        db.disconnect()
        return

    print(f"  Found {len(regions)} region(s): {[r['name'] for r in regions]}")

    region_block = build_select_region_block(regions)
    branch_block = build_select_branch_block(regions, db)
    db.disconnect()

    update_nlu_file(region_block, branch_block)
    print(f"\n[OK] {NLU_FILE} updated successfully.")
    print("Next step: run `rasa train` to rebuild the model.\n")


if __name__ == "__main__":
    main()
