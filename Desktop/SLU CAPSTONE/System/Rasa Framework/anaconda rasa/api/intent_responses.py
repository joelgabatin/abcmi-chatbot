"""
api/intent_responses.py
Maps a classified intent to a response string.
Fetches live data from the database; falls back to FALLBACK_RESPONSES on error.
"""

import re
import logging
from database import Database, SiteSettings, ChurchHistory, StatementOfBelief, ChurchCoreValues, ChurchBranch, Pastor
from api.constants import FALLBACK_RESPONSES

logger = logging.getLogger(__name__)


def get_response_for_intent(intent: str, sender: str = None, user_message: str = "",
                             conversation_state: dict = None) -> str:
    """
    Return a response string for the given intent.

    - sender & conversation_state are required for ask_branches (multi-turn flow).
    - user_message is used to distinguish count vs list for branch queries.
    """
    if conversation_state is None:
        conversation_state = {}

    # ── Branch statistics ────────────────────────────────────────────────────
    if intent in ("ask_total_branches", "ask_local_branches", "ask_international_branches"):
        return _handle_branch_stats(intent, user_message)

    # ── Church information ───────────────────────────────────────────────────
    if intent in ("ask_mission", "ask_vision", "ask_history",
                  "ask_statement_of_belief", "ask_driving_force", "ask_core_values"):
        return _handle_church_info(intent)

    # ── Branch finder (multi-turn) ───────────────────────────────────────────
    if intent == "ask_branches":
        from api.branch_flow import start_branch_search
        return start_branch_search(sender or "user", conversation_state)

    # ── Pastor queries ───────────────────────────────────────────────────────
    if intent == "ask_pastors":
        return _handle_all_pastors()

    if intent == "ask_specific_pastor":
        return _handle_specific_pastor(sender or "user", user_message, conversation_state)

    if intent == "ask_pastor_branch_schedule":
        return _handle_pastor_branch_schedule(sender or "user", conversation_state)

    # ── Simple responses ─────────────────────────────────────────────────────
    simple = {
        "greet": FALLBACK_RESPONSES["utter_greet"],
        "goodbye": FALLBACK_RESPONSES["utter_goodbye"],
    }
    return simple.get(intent, "I'm not sure how to respond to that. Could you rephrase?")


# ── Private helpers ───────────────────────────────────────────────────────────

def _wants_count(user_message: str) -> bool:
    msg = user_message.lower()
    return any(kw in msg for kw in ("how many", "count", "total", "number"))


def _handle_branch_stats(intent: str, user_message: str) -> str:
    try:
        db = Database()
        if db.connect():
            if intent == "ask_total_branches":
                total = ChurchBranch.get_total_count(db)
                db.disconnect()
                if total is not None:
                    return f"ABCMI currently has {total} active branch(es) in total."

            elif intent == "ask_local_branches":
                local = ChurchBranch.get_local_branches(db)
                db.disconnect()
                if local is not None:
                    if _wants_count(user_message):
                        return f"ABCMI has {len(local)} local branch(es) across the Philippines."
                    lines = [f"Here are the local branches of ABCMI ({len(local)} total):\n"]
                    for i, b in enumerate(local, 1):
                        lines.append(f"{i}. {b['name']} — {b['location']}")
                    return "\n".join(lines)

            elif intent == "ask_international_branches":
                intl = ChurchBranch.get_international_branches(db)
                db.disconnect()
                if intl is not None:
                    if _wants_count(user_message):
                        return f"ABCMI has {len(intl)} international branch(es)."
                    if not intl:
                        return "There are currently no active international branches."
                    lines = [f"Here are the international branches of ABCMI ({len(intl)} total):\n"]
                    for i, b in enumerate(intl, 1):
                        lines.append(f"{i}. {b['name']} — {b['location']}")
                    return "\n".join(lines)

            db.disconnect()
    except Exception as e:
        logger.warning(f"[intent_responses] DB error for {intent}: {e}")

    fallback_map = {
        "ask_total_branches": FALLBACK_RESPONSES["utter_total_branches"],
        "ask_local_branches": FALLBACK_RESPONSES["utter_local_branches"],
        "ask_international_branches": FALLBACK_RESPONSES["utter_international_branches"],
    }
    return fallback_map[intent]


def _handle_church_info(intent: str) -> str:
    try:
        db = Database()
        if db.connect():
            if intent == "ask_mission":
                val = SiteSettings.get_mission(db)
                db.disconnect()
                if val:
                    return val

            elif intent == "ask_vision":
                val = SiteSettings.get_vision(db)
                db.disconnect()
                if val:
                    return val

            elif intent == "ask_history":
                history = ChurchHistory.get_all(db)
                db.disconnect()
                if history:
                    lines = ["Here is the history of our church:\n"]
                    for item in history:
                        lines.append(f"• {item['year']}: {item['event']}")
                    return "\n".join(lines)

            elif intent == "ask_statement_of_belief":
                statements = StatementOfBelief.get_all(db)
                db.disconnect()
                if statements:
                    lines = ["Here is what ABCMI Church believes:\n"]
                    for item in statements:
                        lines.append(f"{item['item_number']}. {item['statement']}")
                    return "\n".join(lines)

            elif intent == "ask_driving_force":
                val = SiteSettings.get_driving_force(db)
                db.disconnect()
                if val:
                    return val

            elif intent == "ask_core_values":
                values = ChurchCoreValues.get_all(db)
                db.disconnect()
                if values:
                    lines = ["Here are the core values of ABCMI Church:\n"]
                    for i, item in enumerate(values, 1):
                        lines.append(f"{i}. {item['title']}")
                    return "\n".join(lines)

            db.disconnect()
    except Exception as e:
        logger.warning(f"[intent_responses] DB error for {intent}: {e}")

    fallback_map = {
        "ask_mission": FALLBACK_RESPONSES["utter_mission"],
        "ask_vision": FALLBACK_RESPONSES["utter_vision"],
        "ask_history": FALLBACK_RESPONSES["utter_history"],
        "ask_statement_of_belief": FALLBACK_RESPONSES["utter_statement_of_belief"],
        "ask_driving_force": FALLBACK_RESPONSES["utter_driving_force"],
        "ask_core_values": FALLBACK_RESPONSES["utter_core_values"],
    }
    return fallback_map.get(intent, "Sorry, I couldn't retrieve that information right now.")


# ── Pastor helpers ─────────────────────────────────────────────────────────────

# Regex patterns to extract a pastor name from queries like "is Joel Gabatin your pastor?"
_PASTOR_NAME_PATTERNS = [
    re.compile(r'\bis\s+(.+?)\s+(?:your|a|an|our|the)\s+pastor\b', re.IGNORECASE),
    re.compile(r'\bis\s+(.+?)\s+pastoring\b', re.IGNORECASE),
    re.compile(r'\bdoes\s+(.+?)\s+pastor\b', re.IGNORECASE),
    re.compile(r'pastor\s+named\s+(.+?)[\?.,]?$', re.IGNORECASE),
]


def _extract_pastor_name(user_message: str):
    """Extract a pastor name from a message. Returns title-cased name or None."""
    for pattern in _PASTOR_NAME_PATTERNS:
        match = pattern.search(user_message)
        if match:
            name = match.group(1).strip()
            # Remove a leading "pastor" prefix if user typed "is Pastor Joel your pastor?"
            name = re.sub(r'^pastor\s+', '', name, flags=re.IGNORECASE).strip()
            return name.title()
    return None


def _handle_all_pastors() -> str:
    """Return a list of all active pastors with their assigned branch."""
    try:
        db = Database()
        if db.connect():
            pastors = Pastor.get_all_with_branches(db)
            db.disconnect()
            if pastors:
                lines = ["Here are the pastors of ABCMI Church:\n"]
                for p in pastors:
                    branch = p.get("branches")
                    branch_name = branch["name"] if branch else "Unassigned"
                    lines.append(f"• {p['name']} ({p['role']}) — {branch_name}")
                return "\n".join(lines)
    except Exception as e:
        logger.warning(f"[intent_responses] DB error for ask_pastors: {e}")
    return FALLBACK_RESPONSES["utter_pastors"]


def _handle_specific_pastor(sender: str, user_message: str, conversation_state: dict) -> str:
    """
    Check if a named person is a pastor. Stores branch context in conversation_state
    so a follow-up ask_pastor_branch_schedule can retrieve it.
    """
    name = _extract_pastor_name(user_message)
    if not name:
        return "Could you please tell me the name of the pastor you are looking for?"
    try:
        db = Database()
        if db.connect():
            pastors = Pastor.find_by_name(db, name)
            db.disconnect()
            if pastors:
                p = pastors[0]
                branch = p.get("branches")
                branch_name = branch["name"] if branch else "an ABCMI branch"
                branch_id = p.get("branch_id")
                # Persist context for follow-up schedule question
                conversation_state.setdefault(sender, {})["pastor_context"] = {
                    "branch_id": branch_id,
                    "branch_name": branch_name,
                    "pastor_name": p["name"],
                }
                return (
                    f"Yes! {p['name']} is one of our pastors. "
                    f"He/She serves as {p['role']} at {branch_name}.\n\n"
                    f"You may also ask: \"What is the service schedule of {branch_name}?\""
                )
            else:
                conversation_state.get(sender, {}).pop("pastor_context", None)
                return f"No, {name} is not listed as a pastor in our records."
    except Exception as e:
        logger.warning(f"[intent_responses] DB error for ask_specific_pastor: {e}")
    return "Sorry, I couldn't look up pastor information right now."


def _handle_pastor_branch_schedule(sender: str, conversation_state: dict) -> str:
    """Return the service schedule for the branch remembered from the last pastor query."""
    pastor_ctx = conversation_state.get(sender, {}).get("pastor_context")
    if not pastor_ctx:
        return (
            "I don't have a branch in context yet. Please first ask about a specific pastor — "
            "for example: \"Is Joel Gabatin your pastor?\""
        )
    branch_id = pastor_ctx.get("branch_id")
    branch_name = pastor_ctx.get("branch_name", "the branch")
    if not branch_id:
        return f"Sorry, I don't have a branch ID linked to {branch_name}."
    try:
        db = Database()
        if db.connect():
            schedules = Pastor.get_branch_schedule(db, int(branch_id))
            db.disconnect()
            if schedules:
                lines = [f"Here is the service schedule for {branch_name}:\n"]
                for s in schedules:
                    desc = f" — {s['description']}" if s.get("description") else ""
                    lines.append(f"• {s['day']} at {s['time']} ({s['type']}){desc}")
                return "\n".join(lines)
            return f"Sorry, there is no service schedule available for {branch_name} right now."
    except Exception as e:
        logger.warning(f"[intent_responses] DB error for ask_pastor_branch_schedule: {e}")
    return "Sorry, I couldn't retrieve the service schedule right now."
