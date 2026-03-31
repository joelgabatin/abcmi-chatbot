---
name: pr-release-manager
description: Automate the full Git feature workflow in this repository. Use when Codex needs to start from updated main, create a feature branch before implementation, then commit verified changes, open a GitHub pull request, merge it into main, and pull the updated main locally using the local PR automation agent.
---

# PR Release Manager

Use `.codex/agents/pr_agent.py` for the full branch-to-merge workflow in this repo.

Steps:
1. Before implementing a feature, run:

```powershell
python .codex/agents/pr_agent.py start --title "short feature title"
```

2. After the update is successful and validated, set `GITHUB_TOKEN` and run:

```powershell
python .codex/agents/pr_agent.py finish --title "short update title"
```

Notes:
- Default base branch is `main`.
- `start` checks out local `main`, pulls `origin/main`, and creates the feature branch.
- `finish` commits current changes, pushes the feature branch, creates the PR, merges it to `main`, checks out local `main`, and pulls the updated repository.
- The agent prints notifications when each major step is done.
