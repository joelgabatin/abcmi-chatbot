#!/usr/bin/env python3
"""
DB Health Agent — Grace Church Chatbot
=======================================
Runs via Claude Code PostToolUse hook after Bash commands that touch
database-related scripts or python files.

Detects if the command involved a DB operation, then verifies the
Supabase connection is still healthy. Logs a warning if it is not.

Hook payload received on stdin:
  {
    "tool_name":     "Bash",
    "tool_input":    {"command": "..."},
    "tool_response": {"output": "...", "exit_code": 0}
  }
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR     = PROJECT_ROOT / ".claude" / "logs"
HEALTH_LOG   = LOGS_DIR / "db_health.log"

# ── Triggers: commands that warrant a health check ─────────────────────────────
DB_TRIGGER_PATTERNS = [
    r"scripts/(seed|migrate|admin|sync_nlu)\.py",
    r"python.*database\.py",
    r"grace_api\.py",
    r"rasa run actions",
    r"from database import",
    r"supabase",
]

# ── Indicators of a DB failure in command output ──────────────────────────────
FAILURE_SIGNALS = [
    r"connection refused",
    r"could not connect",
    r"supabaseerror",
    r"postgrest.*error",
    r"failed to connect",
    r"invalid api key",
    r"jwt expired",
    r"relation .* does not exist",
    r"OperationalError",
    r"supabase.*exception",
]


def is_db_command(command: str) -> bool:
    return any(re.search(p, command, re.IGNORECASE) for p in DB_TRIGGER_PATTERNS)


def has_db_failure(output: str) -> bool:
    return any(re.search(p, output, re.IGNORECASE) for p in FAILURE_SIGNALS)


def log_health(status: str, command: str, detail: str):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {status} | CMD: {command[:100]} | {detail}\n"
    with open(HEALTH_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def main():
    raw = sys.stdin.read() if not sys.stdin.isatty() else "{}"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    command   = payload.get("tool_input", {}).get("command", "")
    output    = payload.get("tool_response", {}).get("output", "") or ""
    exit_code = payload.get("tool_response", {}).get("exit_code", 0)

    if not is_db_command(command):
        sys.exit(0)

    if exit_code != 0 or has_db_failure(output):
        detail = "DB connection or query failure detected"
        log_health("WARNING", command, detail)
        print(
            f"[DBHealth] WARNING — possible database issue detected. "
            f"Run /check-db to verify. See .claude/logs/db_health.log",
            file=sys.stderr
        )
    else:
        log_health("OK", command, "No DB errors detected")

    sys.exit(0)


if __name__ == "__main__":
    main()
