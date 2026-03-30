---
name: pr-release-manager
description: Automate post-update Git workflows in this repository. Use when Codex needs to create a branch, commit verified changes, open a GitHub pull request, and merge it into main using the local PR automation agent.
---

# PR Release Manager

Use `.codex/agents/pr_agent.py` for PR automation in this repo.

Steps:
1. Confirm the update is successful and validated.
2. Confirm `GITHUB_TOKEN` is available in the environment.
3. Choose a concise PR title.
4. Run:

```powershell
python .codex/agents/pr_agent.py --title "short update title"
```

Notes:
- Default base branch is `main`.
- Use `--no-merge` if you want to inspect the PR before merging.
- If already on a feature branch, the script reuses that branch.
- If on `main`, the script creates a `codex/...` branch automatically.
