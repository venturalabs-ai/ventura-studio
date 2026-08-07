from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OWNER = "venturalabs-ai"
FLAGSHIPS = [
    "Ventura.SEG",
    "ventura-pro-agro",
    "ventura-chat",
    "autor-ventura",
    "ventura-agents",
    "ventura-studio",
]
TOKEN = os.getenv("GITHUB_TOKEN", "")
API = "https://api.github.com"


def request(path: str):
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def exists(repo: str, path: str) -> bool:
    return request(f"/repos/{OWNER}/{repo}/contents/{path}") is not None


def tree(repo: str):
    meta = request(f"/repos/{OWNER}/{repo}") or {}
    branch = meta.get("default_branch", "main")
    branch_data = request(f"/repos/{OWNER}/{repo}/branches/{branch}") or {}
    sha = branch_data.get("commit", {}).get("sha")
    if not sha:
        return []
    data = request(f"/repos/{OWNER}/{repo}/git/trees/{sha}?recursive=1") or {}
    return data.get("tree", [])


def score_repo(repo: str):
    paths = {item.get("path", "") for item in tree(repo) if item.get("type") == "blob"}
    test_files = sorted(p for p in paths if "/test" in p.lower() or p.startswith("tests/"))
    eval_harness = "scripts/run_evals.py" in paths or any(p.startswith("evals/") for p in paths)
    checks = {
        "readme": "README.md" in paths,
        "license": "LICENSE" in paths,
        "changelog": "CHANGELOG.md" in paths,
        "version": "VERSION" in paths or "backend/pyproject.toml" in paths or "pyproject.toml" in paths,
        "ci_or_evals": ".github/workflows/ci.yml" in paths or ".github/workflows/evals.yml" in paths,
        "security_gate": ".github/workflows/security.yml" in paths or repo in {"ventura-pro-agro", "ventura-chat"},
        "release": ".github/workflows/release.yml" in paths,
        "tests_or_evals": bool(test_files) or eval_harness,
    }
    passed = sum(checks.values())
    return {
        "repository": f"{OWNER}/{repo}",
        "readiness_score": round(100 * passed / len(checks), 1),
        "checks": checks,
        "test_files": len(test_files),
        "eval_harness": eval_harness,
        "production_grade": False,
        "production_grade_reason": "Requires successful CI/security evidence and enforced branch protection; static repository checks alone are insufficient.",
    }


def main():
    repos = [score_repo(repo) for repo in FLAGSHIPS]
    data = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner": OWNER,
        "flagships": repos,
        "summary": {
            "flagships": len(repos),
            "average_readiness_score": round(sum(r["readiness_score"] for r in repos) / len(repos), 1),
            "test_files": sum(r["test_files"] for r in repos),
            "eval_harnesses": sum(1 for r in repos if r["eval_harness"]),
            "production_grade_projects": sum(1 for r in repos if r["production_grade"]),
        },
        "limitations": [
            "This score measures repository evidence, not software correctness.",
            "Production-grade status is intentionally false until successful CI/security and branch-protection evidence are incorporated.",
            "Do not publish vulnerability counts unless produced by completed security scans for the referenced commits/releases.",
        ],
    }
    out = Path("metrics/ecosystem.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(data["summary"], indent=2))


if __name__ == "__main__":
    main()
