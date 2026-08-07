from __future__ import annotations

import base64
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


def tree(repo: str):
    meta = request(f"/repos/{OWNER}/{repo}") or {}
    branch = meta.get("default_branch", "main")
    branch_data = request(f"/repos/{OWNER}/{repo}/branches/{branch}") or {}
    sha = branch_data.get("commit", {}).get("sha")
    if not sha:
        return []
    data = request(f"/repos/{OWNER}/{repo}/git/trees/{sha}?recursive=1") or {}
    return data.get("tree", [])


def file_contains(repo: str, path: str, needle: str) -> bool:
    data = request(f"/repos/{OWNER}/{repo}/contents/{path}")
    if not data or data.get("encoding") != "base64":
        return False
    content = base64.b64decode(data.get("content", "")).decode("utf-8", errors="replace")
    return needle.lower() in content.lower()


def score_repo(repo: str):
    paths = {item.get("path", "") for item in tree(repo) if item.get("type") == "blob"}
    test_files = sorted(p for p in paths if "/test" in p.lower() or p.startswith("tests/"))
    eval_harness = "scripts/run_evals.py" in paths or any(p.startswith("evals/") for p in paths)

    ci_path = ".github/workflows/ci.yml"
    security_path = ".github/workflows/security.yml"
    release_path = ".github/workflows/release.yml"
    supply_chain_path = ".github/workflows/supply-chain.yml"

    provenance = "PROVENANCE.md" in paths
    evals_or_tests = bool(test_files) or eval_harness
    ci = ci_path in paths or ".github/workflows/evals.yml" in paths
    security = security_path in paths or file_contains(repo, ci_path, "bandit") or file_contains(repo, ci_path, "pip-audit")
    sbom = supply_chain_path in paths or file_contains(repo, ci_path, "sbom") or file_contains(repo, release_path, "sbom")
    semver = "VERSION" in paths or "pyproject.toml" in paths or "backend/pyproject.toml" in paths
    release = release_path in paths and file_contains(repo, release_path, "v*.*.*")
    checksums = release_path in paths and file_contains(repo, release_path, "SHA256SUMS")

    checks = {
        "provenance": provenance,
        "evals_or_tests": evals_or_tests,
        "ci": ci,
        "security": security,
        "sbom": sbom,
        "semver": semver,
        "release": release,
        "release_checksums": checksums,
    }
    passed = sum(checks.values())

    return {
        "repository": f"{OWNER}/{repo}",
        "engineering_chain_score": round(100 * passed / len(checks), 1),
        "checks": checks,
        "test_files": len(test_files),
        "eval_harness": eval_harness,
        "production_grade": False,
        "production_grade_reason": (
            "Static repository evidence is necessary but insufficient. Production-grade status requires "
            "successful CI/security evidence for the referenced commit/release plus enforced branch protection."
        ),
    }


def main():
    repos = [score_repo(repo) for repo in FLAGSHIPS]
    data = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner": OWNER,
        "engineering_chain": [
            "provenance",
            "evals_or_tests",
            "ci",
            "security",
            "sbom",
            "semver",
            "release",
            "release_checksums",
        ],
        "flagships": repos,
        "summary": {
            "flagships": len(repos),
            "average_engineering_chain_score": round(
                sum(r["engineering_chain_score"] for r in repos) / len(repos), 1
            ),
            "flagships_with_complete_static_chain": sum(
                1 for r in repos if all(r["checks"].values())
            ),
            "test_files": sum(r["test_files"] for r in repos),
            "eval_harnesses": sum(1 for r in repos if r["eval_harness"]),
            "production_grade_projects": 0,
        },
        "limitations": [
            "Static repository evidence is not proof that workflows passed.",
            "Production-grade status remains false until successful CI/security evidence and enforced branch protection are verified.",
            "Test-file counts are not test-case counts.",
            "Eval-harness counts are not eval-case counts or quality scores.",
            "Do not publish vulnerability counts unless produced by completed security scans for the referenced commits/releases.",
        ],
    }
    out = Path("metrics/ecosystem.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(data["summary"], indent=2))


if __name__ == "__main__":
    main()
