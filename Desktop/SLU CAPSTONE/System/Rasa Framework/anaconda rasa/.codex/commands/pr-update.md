Use the Codex PR automation agent for the full feature workflow.

Workflow:
1. Before implementing the feature, start from `main` and create the feature branch:

```powershell
python .codex/agents/pr_agent.py start --title "your feature title"
```

2. After the update is successful and verified, set `GITHUB_TOKEN` and finish the workflow:

```powershell
$env:GITHUB_TOKEN="your_token_here"
python .codex/agents/pr_agent.py finish --title "your update title"
```

Optional flags for `start`:
- `--body "details"` to customize the pull request body
- `--branch "codex/feature-name"` to force a branch name
- `--base main` to target a different base branch

Default behavior:
- `start` checks out `main`, pulls `origin/main`, and creates the feature branch
- `finish` commits all current changes, pushes to `origin`, opens the PR, merges into `main`, checks out local `main`, and pulls the updated `origin/main`
- the agent prints notifications when each step completes
