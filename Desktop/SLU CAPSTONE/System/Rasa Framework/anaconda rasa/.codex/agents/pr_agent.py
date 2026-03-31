#!/usr/bin/env python3
"""
Codex PR workflow agent.

Supported workflow:
1. start  -> checkout main, pull origin/main, create feature branch
2. finish -> commit changes, push branch, create PR, merge PR, checkout main, pull origin/main
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def notify(message: str) -> None:
    print(f"[NOTIFY] {message}")


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "update"


def parse_remote(remote_url: str) -> tuple[str, str]:
    remote_url = remote_url.strip()
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    ssh_match = re.match(r"git@github\.com:(?P<owner>[^/]+)/(?P<repo>.+)$", remote_url)
    https_match = re.match(r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>.+)$", remote_url)

    match = ssh_match or https_match
    if not match:
        raise RuntimeError("Origin remote is not a supported GitHub URL.")

    return match.group("owner"), match.group("repo")


def github_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    url = f"https://api.github.com{path}"
    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "codex-pr-agent",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"GitHub API error ({error.code}): {details}") from error


def require_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required.")
    return token


def current_branch() -> str:
    branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
    if branch == "HEAD":
        raise RuntimeError("Detached HEAD is not supported for this workflow.")
    return branch


def ensure_changes() -> None:
    status = run_git("status", "--porcelain", check=False)
    if not status.strip():
        raise RuntimeError("There are no changes to commit.")


def checkout(branch_name: str) -> None:
    run_git("checkout", branch_name)
    notify(f"Checked out '{branch_name}'.")


def pull_origin(branch_name: str) -> None:
    run_git("pull", "origin", branch_name)
    notify(f"Pulled latest changes from origin/{branch_name}.")


def create_branch(branch_name: str) -> None:
    run_git("checkout", "-b", branch_name)
    notify(f"Created feature branch '{branch_name}'.")


def commit_changes(commit_message: str) -> None:
    run_git("add", "-A")
    diff_cached = run_git("diff", "--cached", "--name-only", check=False)
    if not diff_cached.strip():
        raise RuntimeError("No staged changes were found after git add.")
    run_git("commit", "-m", commit_message)
    notify(f"Committed changes with message: {commit_message}")


def push_branch(branch_name: str) -> None:
    run_git("push", "-u", "origin", branch_name)
    notify(f"Pushed branch '{branch_name}' to origin.")


def find_open_pr(owner: str, repo: str, branch_name: str, token: str) -> dict | None:
    encoded_head = urllib.parse.quote(f"{owner}:{branch_name}", safe="")
    data = github_request("GET", f"/repos/{owner}/{repo}/pulls?state=open&head={encoded_head}", token)
    if isinstance(data, list) and data:
        return data[0]
    return None


def create_pr(owner: str, repo: str, base_branch: str, branch_name: str, title: str, body: str, token: str) -> dict:
    existing = find_open_pr(owner, repo, branch_name, token)
    if existing:
        notify(f"Reusing existing PR: {existing.get('html_url', 'unknown')}")
        return existing

    pr = github_request(
        "POST",
        f"/repos/{owner}/{repo}/pulls",
        token,
        {"title": title, "head": branch_name, "base": base_branch, "body": body},
    )
    notify(f"Created PR: {pr.get('html_url', 'unknown')}")
    return pr


def merge_pr(owner: str, repo: str, pr_number: int, token: str, commit_title: str) -> dict:
    merged = github_request(
        "PUT",
        f"/repos/{owner}/{repo}/pulls/{pr_number}/merge",
        token,
        {"merge_method": "squash", "commit_title": commit_title},
    )
    notify("Merged PR into main.")
    return merged


def start_feature(branch_name: str, base_branch: str) -> int:
    checkout(base_branch)
    pull_origin(base_branch)
    create_branch(branch_name)
    notify("Feature workflow is ready. You can start implementing the update now.")
    return 0


def finish_update(title: str, body: str, commit_message: str | None, base_branch: str) -> int:
    token = require_token()
    branch_name = current_branch()

    if branch_name == base_branch:
        raise RuntimeError("Finish step cannot run on the base branch. Create a feature branch first.")

    ensure_changes()
    commit_changes(commit_message or title)
    push_branch(branch_name)

    remote_url = run_git("remote", "get-url", "origin")
    owner, repo = parse_remote(remote_url)
    pr = create_pr(owner, repo, base_branch, branch_name, title, body, token)
    merge_pr(owner, repo, pr["number"], token, title)

    checkout(base_branch)
    pull_origin(base_branch)
    notify("Workflow complete: branch created earlier, PR created, merged into main, and local main is up to date.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex PR workflow agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Pull main and create a feature branch")
    start_parser.add_argument("--title", required=True, help="Short feature title used to build the branch name")
    start_parser.add_argument("--branch", help="Explicit branch name")
    start_parser.add_argument("--base", default="main", help="Base branch to start from")

    finish_parser = subparsers.add_parser("finish", help="Create PR, merge to main, and update local main")
    finish_parser.add_argument("--title", required=True, help="Pull request title")
    finish_parser.add_argument("--body", default="Automated update from Codex PR agent.", help="Pull request body")
    finish_parser.add_argument("--commit-message", help="Commit message to use")
    finish_parser.add_argument("--base", default="main", help="Base branch for the pull request")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "start":
            branch_name = args.branch or f"codex/{slugify(args.title)}"
            return start_feature(branch_name, args.base)
        if args.command == "finish":
            return finish_update(args.title, args.body, args.commit_message, args.base)
        raise RuntimeError(f"Unsupported command: {args.command}")
    except Exception as exc:
        print(f"PR agent failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
