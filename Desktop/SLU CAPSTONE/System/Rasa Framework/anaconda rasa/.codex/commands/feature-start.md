Use this command before implementing a new feature so work begins from an updated `main` branch.

Run:

```powershell
python .codex/agents/pr_agent.py start --title "your feature title"
```

What it does:
- checks out local `main`
- pulls the latest `origin/main`
- creates a new feature branch such as `codex/your-feature-title`

Optional flags:
- `--branch "custom-branch-name"` to set the branch name manually
- `--base main` to use a different base branch

Example:

```powershell
python .codex/agents/pr_agent.py start --title "contact us improvements"
```
