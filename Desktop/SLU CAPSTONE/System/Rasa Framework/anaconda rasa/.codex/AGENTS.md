# Project Codex Rules

Use this repo as a split-domain Rasa assistant backed by Supabase and custom action modules.

Follow these project rules:
- Keep NLU, rules, and stories split by feature and prefer one intent or rule per file.
- Put feature files inside matching folders such as `data/nlu/contact_us/` and `data/stories/contact_us/`.
- Edit the split domain files in `domain/` instead of `domain.yml`.
- Register new custom actions in both `actions/__init__.py` and `domain/actions.yml`.
- Prefer reading church contact and social links from Supabase via `database.py`.
- Retrain and restart services after changing intents, rules, stories, entities, slots, or actions.
- Use `.codex/agents/pr_agent.py start ...` before implementing a feature so the work begins on a fresh feature branch from updated `main`.
- Use `.codex/agents/pr_agent.py finish ...` after validation to commit the update, create the PR, merge it into `main`, and pull the updated `main` locally.

Important repo paths:
- `actions/` for custom action implementations by feature
- `data/nlu/` for training examples
- `data/rules/` for rule-based routing
- `data/stories/` for multi-turn flows
- `domain/` for split domain configuration
- `.codex/agents/` for local automation agents
- `.codex/agents/pr_agent.md` for the PR agent workflow guide
- `.codex/commands/` for reusable Codex workflow prompts
- `.codex/commands/feature-start.md` for the shortcut to start a feature branch from updated `main`
- `.codex/commands/feature-finish.md` for the shortcut to create the PR, merge it, and refresh local `main`

Validation checklist:
- Run `python -m py_compile` on changed action and database files.
- Run `rasa data validate --domain domain/` when domain or training data changes.
- Run `rasa train --domain domain/` before final verification when model data changes.

PR automation notes:
- Set `GITHUB_TOKEN` before running the PR agent.
- Always start from `main`, pull `origin/main`, then create the feature branch before editing files.
- Run the finish step only after verification passes and you are ready to publish the update.
- Default base branch is `main`.
- The PR agent prints notifications for branch creation, push, PR creation, merge, and local `main` refresh.
