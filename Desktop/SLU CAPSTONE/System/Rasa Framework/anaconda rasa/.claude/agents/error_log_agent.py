#!/usr/bin/env python3
"""
Error Log Agent — Grace Church Chatbot
=======================================
Runs via Claude Code PostToolUse hook after every Bash command.
Detects failures, categorizes them, and appends structured entries
to .claude/logs/errors.log and .claude/logs/errors.jsonl.

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
ERROR_LOG    = LOGS_DIR / "errors.log"
ERROR_JSONL  = LOGS_DIR / "errors.jsonl"
MAX_LOG_LINES = 500   # rotate after this many lines

# ── Error categories ───────────────────────────────────────────────────────────
CATEGORIES = {
    "DATABASE": [
        r"supabase", r"postgrest", r"psycopg2", r"mysql",
        r"connection refused", r"could not connect",
        r"relation .* does not exist", r"column .* does not exist",
        r"duplicate key", r"violates.*constraint",
        r"database.*error", r"OperationalError", r"IntegrityError",
    ],
    "API_SERVER": [
        r"flask", r"werkzeug", r"address already in use",
        r"port \d+ is already in use", r"http.*error",
        r"500 internal server error", r"404 not found",
        r"ConnectionRefusedError", r"requests\.exceptions",
    ],
    "RASA": [
        r"rasa", r"nlu", r"diet", r"fallback",
        r"failed to load model", r"no model found",
        r"action.*not found", r"slot.*not found",
        r"rasa\.exceptions", r"InvalidConfigError",
    ],
    "PYTHON": [
        r"traceback \(most recent call last\)",
        r"syntaxerror", r"indentationerror", r"nameerror",
        r"typeerror", r"valueerror", r"keyerror", r"importerror",
        r"modulenotfounderror", r"attributeerror", r"indexerror",
        r"zerodivisionerror", r"filenotfounderror",
    ],
    "GIT": [
        r"fatal:", r"error: pathspec", r"merge conflict",
        r"nothing to commit", r"not a git repository",
        r"rejected.*failed to push",
    ],
    "CONDA_ENV": [
        r"conda", r"packagenotfounderror", r"environment not found",
        r"pip.*error", r"could not find.*package",
    ],
}

# Keywords that indicate a genuine error even with exit_code 0
ERROR_SIGNALS = [
    "error", "exception", "traceback", "failed", "fatal",
    "critical", "cannot", "could not", "no such file", "permission denied",
]

# Output patterns that are NOT errors (false-positive suppression)
NOISE_PATTERNS = [
    r"^\s*$",                           # blank
    r"^warning:",                       # warnings only
    r"deprecat",                        # deprecation notices
    r"^successfully",
    r"✓", r"✅",
    r"migration completed",
    r"seeding completed",
]


# ── Helpers ────────────────────────────────────────────────────────────────────

def is_noise(text: str) -> bool:
    lo = text.lower()
    return any(re.search(p, lo) for p in NOISE_PATTERNS)


def categorize(output: str, command: str) -> str:
    combined = (output + " " + command).lower()
    for cat, patterns in CATEGORIES.items():
        if any(re.search(p, combined, re.IGNORECASE) for p in patterns):
            return cat
    return "GENERAL"


def extract_snippet(output: str, max_lines: int = 10) -> str:
    """Return the most relevant error lines (last N lines or traceback block)."""
    lines = output.strip().splitlines()

    # Try to find traceback block
    tb_start = -1
    for i, line in enumerate(lines):
        if re.search(r"traceback \(most recent call last\)", line, re.IGNORECASE):
            tb_start = i
            break

    if tb_start >= 0:
        block = lines[tb_start:]
        return "\n".join(block[:max_lines])

    # Otherwise last N non-empty lines
    non_empty = [l for l in lines if l.strip()]
    return "\n".join(non_empty[-max_lines:])


def is_error(exit_code: int, output: str) -> bool:
    if exit_code not in (0, None):
        return True
    lo = output.lower()
    if is_noise(lo):
        return False
    return any(sig in lo for sig in ERROR_SIGNALS)


def rotate_if_needed():
    """Trim errors.log to last MAX_LOG_LINES lines if it gets too large."""
    if not ERROR_LOG.exists():
        return
    lines = ERROR_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
    if len(lines) > MAX_LOG_LINES:
        ERROR_LOG.write_text(
            "\n".join(lines[-MAX_LOG_LINES:]) + "\n",
            encoding="utf-8"
        )


def append_log(entry: dict):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    rotate_if_needed()

    ts       = entry["timestamp"]
    level    = entry["level"]
    category = entry["category"]
    command  = entry["command"][:120]   # truncate long commands
    snippet  = entry["snippet"]
    exit_cd  = entry["exit_code"]

    # ── Human-readable log ──
    separator = "─" * 72
    block = (
        f"\n{separator}\n"
        f"[{ts}]  LEVEL={level}  CATEGORY={category}  EXIT={exit_cd}\n"
        f"CMD : {command}\n"
        f"---\n"
        f"{snippet}\n"
    )
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(block)

    # ── Machine-readable JSONL ──
    with open(ERROR_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def classify_level(exit_code: int, output: str) -> str:
    lo = output.lower()
    if exit_code not in (0, None):
        return "ERROR"
    if any(w in lo for w in ("critical", "fatal", "traceback")):
        return "CRITICAL"
    if any(w in lo for w in ("error", "exception", "failed")):
        return "ERROR"
    return "WARNING"


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # Read hook payload
    raw = sys.stdin.read() if not sys.stdin.isatty() else "{}"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    tool_input    = payload.get("tool_input", {})
    tool_response = payload.get("tool_response", {})

    command   = tool_input.get("command", "")
    output    = tool_response.get("output", "") or ""
    exit_code = tool_response.get("exit_code", 0)

    # Skip if not an error
    if not is_error(exit_code, output):
        sys.exit(0)

    category = categorize(output, command)
    snippet  = extract_snippet(output)
    level    = classify_level(exit_code, output)

    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "level":     level,
        "category":  category,
        "exit_code": exit_code,
        "command":   command,
        "snippet":   snippet,
    }

    append_log(entry)
    print(
        f"[ErrorLog] {level} [{category}] logged → .claude/logs/errors.log",
        file=sys.stderr
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
