Use the Codex PR automation agent after a successful and verified update.

Workflow:
1. Confirm validation is complete.
2. Set `GITHUB_TOKEN` in the shell.
3. Run:

```powershell
python .codex/agents/pr_agent.py --title "your update title"
```

Optional flags:
- `--body "details"` to customize the pull request body
- `--commit-message "message"` to customize the commit message
- `--branch "codex/feature-name"` to force a branch name
- `--base main` to target a different base branch
- `--no-merge` to stop after PR creation

Default behavior:
- creates a branch if you are on `main`
- commits all current changes
- pushes to `origin`
- opens a GitHub pull request
- merges the PR into `main` unless `--no-merge` is used
