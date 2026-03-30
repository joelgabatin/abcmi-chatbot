---
name: rasa-maintainer
description: Maintain and extend this Rasa chatbot project. Use when Codex needs to add or update intents, entities, slots, actions, rules, stories, or Supabase-backed chatbot features in this repository.
---

# Rasa Maintainer

Follow these repo-specific steps:

1. Inspect the split structure before editing:
   - `data/nlu/<feature>/`
   - `data/rules/<feature>/`
   - `data/stories/<feature>/`
   - `domain/`
   - `actions/<feature>/`

2. Keep training data granular:
   - Prefer one intent per NLU file.
   - Prefer one rule per rule file.
   - Prefer one story per story file unless the flow is tightly related.

3. When adding a new bot capability:
   - Add or update NLU examples.
   - Add entities and slots only if needed.
   - Add the intent to `domain/intents.yml`.
   - Add the custom action to `actions/` and register it in `actions/__init__.py`.
   - Register the action in `domain/actions.yml`.
   - Add a matching rule or story in the feature folder.
   - Add fallback responses in `domain/responses/` when appropriate.

4. When a feature reads church settings:
   - Check `database.py` first.
   - Prefer explicit Supabase table and column names instead of guessing.
   - Reuse `SiteSettings` helper methods rather than embedding queries in action files.

5. Validate after edits:
   - Run `python -m py_compile` for changed Python files.
   - Run `rasa data validate --domain domain/` after changing training data or domain files.
   - Run `rasa train --domain domain/` before handing off model-related changes when possible.
