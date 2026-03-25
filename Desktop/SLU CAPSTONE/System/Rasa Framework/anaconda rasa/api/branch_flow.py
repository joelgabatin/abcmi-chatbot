"""
api/branch_flow.py
Multi-turn conversation helpers for the branch-finder feature.

Flow:
  ask_branches → list regions   (state: awaiting_region)
  user picks region → list branches  (state: awaiting_branch)
  user picks branch → show details
"""

import logging
from database import Database, ChurchBranch
from api.constants import FALLBACK_RESPONSES

logger = logging.getLogger(__name__)


def start_branch_search(sender: str, conversation_state: dict) -> str:
    """List all regions and set state to awaiting_region."""
    try:
        db = Database()
        if db.connect():
            regions = ChurchBranch.get_all_regions(db)
            db.disconnect()
            if regions:
                conversation_state[sender] = {
                    "step": "awaiting_region",
                    "regions": regions,
                }
                lines = ["Which region are you looking for? Here are our available regions:\n"]
                for i, r in enumerate(regions, 1):
                    lines.append(f"{i}. {r['name']}")
                lines.append("\nPlease type the region name or its number.")
                return "\n".join(lines)
    except Exception as e:
        logger.warning(f"[branch_flow] Error starting branch search: {e}")
    return FALLBACK_RESPONSES["utter_branches"]


def handle_region_selection(sender: str, user_message: str, state: dict, conversation_state: dict) -> str:
    """Match user input to a region, then list its branches."""
    regions = state.get("regions", [])
    msg = user_message.strip()

    matched_region = None
    if msg.isdigit():
        idx = int(msg) - 1
        if 0 <= idx < len(regions):
            matched_region = regions[idx]
    else:
        msg_lower = msg.lower()
        for r in regions:
            if msg_lower == r["name"].lower() or msg_lower in r["name"].lower():
                matched_region = r
                break

    if not matched_region:
        lines = ["Sorry, I didn't recognize that region. Please choose from:\n"]
        for i, r in enumerate(regions, 1):
            lines.append(f"{i}. {r['name']}")
        return "\n".join(lines)

    try:
        db = Database()
        if db.connect():
            branches = ChurchBranch.get_branches_by_region(db, matched_region["id"])
            db.disconnect()
            if branches:
                conversation_state[sender] = {
                    "step": "awaiting_branch",
                    "region_id": matched_region["id"],
                    "region_name": matched_region["name"],
                    "branches": branches,
                }
                lines = [f"Here are the branches in {matched_region['name']}:\n"]
                for i, b in enumerate(branches, 1):
                    lines.append(f"{i}. {b['name']} — {b['location']}")
                lines.append("\nWhich branch would you like to know more about? Type the name or number.")
                return "\n".join(lines)
            else:
                conversation_state.pop(sender, None)
                return f"Sorry, there are no active branches in {matched_region['name']} at this time."
    except Exception as e:
        logger.warning(f"[branch_flow] Error in region selection: {e}")

    conversation_state.pop(sender, None)
    return "Sorry, I couldn't retrieve the branches. Please try again."


def handle_branch_selection(sender: str, user_message: str, state: dict, conversation_state: dict) -> str:
    """Match user input to a branch and return its full details."""
    branches = state.get("branches", [])
    region_name = state.get("region_name", "this region")
    msg = user_message.strip()

    matched_branch = None
    if msg.isdigit():
        idx = int(msg) - 1
        if 0 <= idx < len(branches):
            matched_branch = branches[idx]
    else:
        msg_lower = msg.lower()
        for b in branches:
            if msg_lower == b["name"].lower() or msg_lower in b["name"].lower():
                matched_branch = b
                break

    if not matched_branch:
        lines = [f"Sorry, I didn't recognize that branch. Branches in {region_name}:\n"]
        for i, b in enumerate(branches, 1):
            lines.append(f"{i}. {b['name']}")
        return "\n".join(lines)

    try:
        db = Database()
        if db.connect():
            details = ChurchBranch.get_branch_details(db, matched_branch["id"])
            db.disconnect()
            conversation_state.pop(sender, None)
            if details:
                return format_branch_details(details)
    except Exception as e:
        logger.warning(f"[branch_flow] Error in branch selection: {e}")

    conversation_state.pop(sender, None)
    return "Sorry, I couldn't retrieve the branch details. Please try again."


def format_branch_details(branch: dict) -> str:
    """Format a branch record into a readable chat message."""
    lines = [f"{branch['name']}\n"]
    lines.append(f"Location: {branch['location']}")

    if branch.get("pastors"):
        lines.append("\nPastor in Charge:")
        for p in branch["pastors"]:
            lines.append(f"  • {p['name']} ({p['role']})")

    if branch.get("schedules"):
        lines.append("\nService Schedule:")
        for s in branch["schedules"]:
            desc = f" — {s['description']}" if s.get("description") else ""
            lines.append(f"  • {s['day']} at {s['time']} ({s['type']}){desc}")

    lines.append("\nIs there anything else I can help you with?")
    return "\n".join(lines)
