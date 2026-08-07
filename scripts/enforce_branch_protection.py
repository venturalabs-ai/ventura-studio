#!/usr/bin/env python3
"""Apply strict branch protection to Ventura flagship repositories.

Requires VENTURA_GITHUB_ADMIN_TOKEN with repository Administration: write.
The token is read only from the environment and is never printed.

The script discovers successful check-run names from the current default-branch
HEAD and makes them required, avoiding stale hard-coded check contexts.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

OWNER = "venturalabs-ai"
REPOS = (
    "Ventura.SEG",
    "ventura-pro-agro",
    "ventura-chat",
    "autor-ventura",
    "ventura-agents",
    "ventura-studio",
)
API = "https://api.github.com"
TOKEN = os.getenv("VENTURA_GITHUB_ADMIN_TOKEN")


def request(method: str, path: str, payload: dict | None = None) -> dict:
    if not TOKEN:
        raise RuntimeError("VENTURA_GITHUB_ADMIN_TOKEN is not configured")
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        # Never expose response bodies because they may contain sensitive metadata.
        raise RuntimeError(f"GitHub API HTTP {exc.code} for {method} {path}") from exc


def repo_info(repo: str) -> tuple[str, str]:
    info = request("GET", f"/repos/{OWNER}/{repo}")
    branch = str(info.get("default_branch") or "main")
    ref = request("GET", f"/repos/{OWNER}/{repo}/git/ref/heads/{urllib.parse.quote(branch, safe='')}")
    sha = (((ref.get("object") or {}).get("sha")) or "")
    if not sha:
        raise RuntimeError(f"Could not resolve {repo}:{branch}")
    return branch, sha


def successful_checks(repo: str, sha: str) -> list[str]:
    result = request("GET", f"/repos/{OWNER}/{repo}/commits/{sha}/check-runs?per_page=100")
    names: list[str] = []
    for run in result.get("check_runs") or []:
        if run.get("status") == "completed" and run.get("conclusion") == "success":
            name = str(run.get("name") or "").strip()
            if name and name not in names:
                names.append(name)
    return sorted(names)


def protect(repo: str) -> dict:
    branch, sha = repo_info(repo)
    checks = successful_checks(repo, sha)
    if not checks:
        raise RuntimeError(f"No successful checks found on {repo}:{branch} HEAD; refusing to protect with an empty gate")

    payload = {
        "required_status_checks": {"strict": True, "contexts": checks},
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1,
            "require_last_push_approval": True,
        },
        "restrictions": None,
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": True,
        "lock_branch": False,
        "allow_fork_syncing": True,
    }
    request("PUT", f"/repos/{OWNER}/{repo}/branches/{urllib.parse.quote(branch, safe='')}/protection", payload)
    verification = request("GET", f"/repos/{OWNER}/{repo}/branches/{urllib.parse.quote(branch, safe='')}/protection")
    return {
        "repository": f"{OWNER}/{repo}",
        "branch": branch,
        "head": sha,
        "required_checks": checks,
        "enforce_admins": bool((verification.get("enforce_admins") or {}).get("enabled")),
        "required_pull_request_reviews": "required_pull_request_reviews" in verification,
    }


def main() -> int:
    if not TOKEN:
        print("ERROR: VENTURA_GITHUB_ADMIN_TOKEN secret is required", file=sys.stderr)
        return 2

    report: list[dict] = []
    failures: list[str] = []
    for repo in REPOS:
        try:
            result = protect(repo)
            report.append(result)
            print(f"PASS {result['repository']}:{result['branch']} checks={len(result['required_checks'])}")
        except Exception as exc:
            failures.append(f"{repo}: {exc}")
            print(f"FAIL {repo}: {exc}", file=sys.stderr)

    print(json.dumps({"protected": report, "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
