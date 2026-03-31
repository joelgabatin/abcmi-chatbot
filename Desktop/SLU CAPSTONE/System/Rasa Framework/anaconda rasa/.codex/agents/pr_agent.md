# PR Agent

This document explains how to use `.codex/agents/pr_agent.py`.

## Purpose

The PR agent manages the full Git workflow for this project:
- start from updated `main`
- create a feature branch before development
- commit and push the finished update
- create a GitHub pull request
- merge the PR into `main`
- pull the updated `main` locally
- print notifications when each step is complete

## Requirements

- `git` must be installed
- remote `origin` must point to the GitHub repository
- `GITHUB_TOKEN` must be available for the `finish` step

## Commands

### Start a Feature

Run this before making changes:

```powershell
python .codex/agents/pr_agent.py start --title "my feature"
```

What it does:
- checks out `main`
- pulls `origin/main`
- creates a feature branch named `codex/my-feature`

Optional flags:
- `--branch "custom-branch-name"` to set the branch name manually
- `--base main` to change the base branch

### Finish a Feature

Run this after the update is complete and validated:

```powershell
$env:GITHUB_TOKEN="your_token_here"
python .codex/agents/pr_agent.py finish --title "my feature"
```

What it does:
- commits all current changes
- pushes the feature branch to `origin`
- creates a GitHub pull request
- merges the pull request into `main`
- checks out local `main`
- pulls the updated `origin/main`

Optional flags:
- `--body "details"` to customize the PR body
- `--commit-message "message"` to customize the commit message
- `--base main` to change the target branch

## Notifications

The agent prints notifications for completed steps, including:
- branch checkout
- pull from origin
- branch creation
- commit creation
- push to origin
- PR creation
- PR merge
- local `main` refresh

## Example Workflow

```powershell
python .codex/agents/pr_agent.py start --title "contact us refactor"

# implement and validate changes

$env:GITHUB_TOKEN="your_token_here"
python .codex/agents/pr_agent.py finish --title "Refactor contact us structure"
```

## Notes

- Do not run `finish` on `main`.
- Use the `start` step first so every feature begins from the latest `main`.
- The `finish` step assumes the current branch is the feature branch you want to publish.
