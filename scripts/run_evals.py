from pathlib import Path

REQUIRED = [
    "README.md",
    "LICENSE",
    "PROVENANCE.md",
    "CHANGELOG.md",
    "VERSION",
    "ENGINEERING_STANDARD.md",
    "scripts/ecosystem_score.py",
    ".github/workflows/ci.yml",
    ".github/workflows/security.yml",
    ".github/workflows/supply-chain.yml",
    ".github/workflows/release.yml",
]

FORBIDDEN = [
    "6 production-grade projects",
    "100% ci protected",
    "0 critical vulnerabilities",
]


def main() -> None:
    failures: list[str] = []
    for name in REQUIRED:
        if not Path(name).is_file():
            failures.append(f"missing required governance artifact: {name}")

    for path in [Path("README.md"), Path("profile/README.md")]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for claim in FORBIDDEN:
            if claim in text:
                failures.append(f"unsupported portfolio metric in {path}: {claim}")

    if failures:
        print("GOVERNANCE EVALS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("GOVERNANCE EVALS: PASS (static contract only)")
    print("No claim is made about workflow execution or production readiness.")


if __name__ == "__main__":
    main()
