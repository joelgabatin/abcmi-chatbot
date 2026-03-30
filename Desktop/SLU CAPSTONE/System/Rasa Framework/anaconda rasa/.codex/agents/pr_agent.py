#!/usr/bin/env python3
"""
PR automation agent for Codex workflows.

This script can:
1. Create or reuse a feature branch
2. Commit tracked changes
3. Push the branch to origin
4. Create a pull request on GitHub
5. Merge the pull request into the base branch

Requirements:
- git must be available
- remote "origin" must point to GitHub
- GITHUB_TOKEN must be set
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
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


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


def ensure_branch(base_branch: str, branch_name: str | None) -> str:
    current_branch = run_git("rev-parse", "--abbrev-ref", "HEAD")

    if current_branch == "HEAD":
        raise RuntimeError("Detached HEAD is not supported for PR automation.")

    if current_branch == base_branch:
        if not branch_name:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            branch_name = f"codex/{base_branch}/{timestamp}"
        run_git("checkout", "-b", branch_name)
        return branch_name

    if branch_name and branch_name != current_branch:
        raise RuntimeError(
            f"Current branch is '{current_branch}', but requested branch is '{branch_name}'."
        )

    return current_branch


def ensure_changes() -> None:
    status = run_git("status", "--porcelain", check=False)
    if not status.strip():
        raise RuntimeError("There are no changes to commit.")


def commit_changes(commit_message: str) -> None:
    run_git("add", "-A")

    diff_cached = run_git("diff", "--cached", "--name-only", check=False)
    if not diff_cached.strip():
        raise RuntimeError("No staged changes were found after git add.")

    run_git("commit", "-m", commit_message)


def push_branch(branch_name: str) -> None:
    run_git("push", "-u", "origin", branch_name)


def find_open_pr(owner: str, repo: str, branch_name: str, token: str) -> dict | None:
    encoded_head = urllib.parse.quote(f"{owner}:{branch_name}", safe="")
    data = github_request(
        "GET",
        f"/repos/{owner}/{repo}/pulls?state=open&head={encoded_head}",
        token,
    )
    if isinstance(data, list) and data:
        return data[0]
    return None


def create_pr(owner: str, repo: str, base_branch: str, branch_name: str, title: str, body: str, token: str) -> dict:
    existing = find_open_pr(owner, repo, branch_name, token)
    if existing:
        return existing

    return github_request(
        "POST",
        f"/repos/{owner}/{repo}/pulls",
        token,
        {
            "title": title,
            "head": branch_name,
            "base": base_branch,
            "body": body,
        },
    )


def merge_pr(owner: str, repo: str, pr_number: int, token: str, commit_title: str) -> dict:
    return github_request(
        "PUT",
        f"/repos/{owner}/{repo}/pulls/{pr_number}/merge",
        token,
        {
            "merge_method": "squash",
            "commit_title": commit_title,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a branch, PR, and merge to main.")
    parser.add_argument("--title", required=True, help="Pull request title")
    parser.add_argument("--body", default="Automated update from Codex PR agent.", help="Pull request body")
    parser.add_argument("--commit-message", help="Commit message to use")
    parser.add_argument("--branch", help="Branch name to create or reuse")
    parser.add_argument("--base", default="main", help="Base branch for the pull request")
    parser.add_argument("--no-merge", action="store_true", help="Create the PR without merging it")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is required.", file=sys.stderr)
        return 1

    try:
        ensure_changes()

        branch_name = args.branch or f"codex/{slugify(args.title)}"
        branch_name = ensure_branch(args.base, branch_name)

        commit_message = args.commit_message or args.title
        commit_changes(commit_message)
        push_branch(branch_name)

        remote_url = run_git("remote", "get-url", "origin")
        owner, repo = parse_remote(remote_url)

        pr = create_pr(
            owner=owner,
            repo=repo,
            base_branch=args.base,
            branch_name=branch_name,
            title=args.title,
            body=args.body,
            token=token,
        )

        print(f"PR created: {pr.get('html_url', 'unknown')}")

        if not args.no_merge:
            merge_result = merge_pr(owner, repo, pr["number"], token, args.title)
            print(f"Merged into {args.base}: {merge_result.get('sha', 'unknown')}")

        return 0
    except Exception as exc:
        print(f"PR agent failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
