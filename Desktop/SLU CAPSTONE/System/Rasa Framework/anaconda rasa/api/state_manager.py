"""
api/state_manager.py
Manages per-sender conversation state for multi-turn flows.
Delegates to branch_flow for region/branch selection steps.

Conversation state shape per sender:
  {
    "step": "awaiting_region" | "awaiting_branch" | None,
    "regions": [...],          # used during branch search
    "region_id": int,
    "region_name": str,
    "branches": [...],
    "pastor_context": {        # persists across steps for schedule follow-ups
        "branch_id": int,
        "branch_name": str,
        "pastor_name": str,
    }
  }
"""

import logging
from api.constants import STATE_RESET_KEYWORDS
from api.classifier import classify_intent
from api.branch_flow import handle_region_selection, handle_branch_selection
from api.intent_responses import get_response_for_intent

logger = logging.getLogger(__name__)

# In-memory conversation state, keyed by sender ID.
CONVERSATION_STATE: dict = {}

# Intents that should interrupt an active branch-search flow
_BRANCH_OVERRIDE_INTENTS = {
    "ask_pastors", "ask_specific_pastor", "ask_pastor_branch_schedule",
    "ask_mission", "ask_vision", "ask_history", "ask_statement_of_belief",
    "ask_driving_force", "ask_core_values", "ask_total_branches",
    "ask_local_branches", "ask_international_branches", "goodbye",
}


def should_reset_state(user_message: str) -> bool:
    """Return True if the user is clearly switching to a different topic."""
    msg = user_message.lower()
    return any(kw in msg for kw in STATE_RESET_KEYWORDS)


def _clear_branch_flow(sender: str) -> None:
    """Remove the multi-step branch flow keys but keep pastor_context."""
    state = CONVERSATION_STATE.get(sender, {})
    pastor_ctx = state.get("pastor_context")
    if pastor_ctx:
        CONVERSATION_STATE[sender] = {"pastor_context": pastor_ctx}
    else:
        CONVERSATION_STATE.pop(sender, None)


def handle_message(sender: str, user_message: str) -> str:
    """
    Main message router.
    Checks active conversation state first; otherwise classifies intent normally.
    """
    state = CONVERSATION_STATE.get(sender, {})
    step = state.get("step")

    if step in ("awaiting_region", "awaiting_branch"):
        if should_reset_state(user_message):
            logger.info(f"[state_manager] Resetting branch flow for {sender} (reset keyword)")
            _clear_branch_flow(sender)
        else:
            # Peek at intent — if user switched to a non-branch topic, clear the flow
            peeked_intent = classify_intent(user_message)
            if peeked_intent in _BRANCH_OVERRIDE_INTENTS:
                logger.info(f"[state_manager] Overriding branch flow for {sender} (intent={peeked_intent})")
                _clear_branch_flow(sender)
                # Fall through to handle the new intent below
            elif step == "awaiting_region":
                return handle_region_selection(sender, user_message, state, CONVERSATION_STATE)
            else:
                return handle_branch_selection(sender, user_message, state, CONVERSATION_STATE)

    intent = classify_intent(user_message)
    logger.info(f"[state_manager] Intent for {sender}: {intent}")
    return get_response_for_intent(intent, sender, user_message, CONVERSATION_STATE)
