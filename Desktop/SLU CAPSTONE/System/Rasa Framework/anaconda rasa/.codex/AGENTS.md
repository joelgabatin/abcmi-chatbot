# Project Codex Rules

Use this repo as a split-domain Rasa assistant backed by Supabase and custom action modules.

Follow these project rules:
- Keep NLU, rules, and stories split by feature and prefer one intent or rule per file.
- Put feature files inside matching folders such as `data/nlu/contact_us/` and `data/stories/contact_us/`.
- Edit the split domain files in `domain/` instead of `domain.yml`.
- Register new custom actions in both `actions/__init__.py` and `domain/actions.yml`.
- Prefer reading church contact and social links from Supabase via `database.py`.
- Retrain and restart services after changing intents, rules, stories, entities, slots, or actions.
- Use `.codex/agents/pr_agent.py` to handle the post-update Git workflow when you want branch creation, PR creation, and merge to `main`.

Important repo paths:
- `actions/` for custom action implementations by feature
- `data/nlu/` for training examples
- `data/rules/` for rule-based routing
- `data/stories/` for multi-turn flows
- `domain/` for split domain configuration
- `.codex/agents/` for local automation agents
- `.codex/commands/` for reusable Codex workflow prompts

Validation checklist:
- Run `python -m py_compile` on changed action and database files.
- Run `rasa data validate --domain domain/` when domain or training data changes.
- Run `rasa train --domain domain/` before final verification when model data changes.

PR automation notes:
- Set `GITHUB_TOKEN` before running the PR agent.
- Run the PR agent only after verification passes and you are ready to publish the update.
- Default base branch is `main`.
