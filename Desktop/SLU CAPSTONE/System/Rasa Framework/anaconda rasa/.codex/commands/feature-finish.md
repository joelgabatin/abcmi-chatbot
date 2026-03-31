Use this command after a feature update is complete and validated so Codex can publish it through PR and merge it into `main`.

Run:

```powershell
$env:GITHUB_TOKEN="your_token_here"
python .codex/agents/pr_agent.py finish --title "your update title"
```

What it does:
- commits the current feature-branch changes
- pushes the branch to `origin`
- creates a GitHub pull request
- merges the pull request into `main`
- checks out local `main`
- pulls the updated `origin/main`
- prints notifications for each completed step

Optional flags:
- `--body "details"` to customize the pull request body
- `--commit-message "message"` to customize the commit message
- `--base main` to use a different base branch

Example:

```powershell
$env:GITHUB_TOKEN="your_token_here"
python .codex/agents/pr_agent.py finish --title "Refactor contact us structure"
```
