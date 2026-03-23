Read the file `.claude/logs/errors.log` and `.claude/logs/errors.jsonl` if they exist.

Then do the following:

1. Count total errors logged, broken down by category (DATABASE, API_SERVER, RASA, PYTHON, GIT, CONDA_ENV, GENERAL) and by level (CRITICAL, ERROR, WARNING).

2. Show the **5 most recent errors** with:
   - Timestamp
   - Level and Category
   - The command that triggered it
   - The error snippet

3. If any CRITICAL errors exist, highlight them at the top as a priority section.

4. If the log file does not exist yet, say "No errors logged yet — the error logging agent will create .claude/logs/errors.log automatically when the first error is detected."

5. End with a one-line health summary, e.g. "System looks healthy — no critical errors." or "⚠ 3 unresolved errors detected (1 CRITICAL)."
