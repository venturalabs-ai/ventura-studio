# Ventura Engineering Standard — Flagship Gate

A flagship must expose a verifiable engineering chain in this order:

`provenance → evals/tests → CI → security → SBOM → SemVer → reproducible release`

## 1. Provenance

Required evidence:
- `PROVENANCE.md`;
- repository `LICENSE`;
- third-party source/license boundaries recorded when applicable.

A project must not describe copied, translated or adapted third-party material as wholly original Ventura work.

## 2. Evals / Tests

Required evidence depends on repository type:
- executable applications: automated unit/integration/regression tests where applicable;
- agent/prompt projects: automated contract/structural evals plus semantic/model evals when quantitative quality claims are published;
- governance repositories: deterministic static validation of governance artifacts.

Contract evals must not be presented as proof of semantic model quality.

## 3. CI

Required evidence:
- `.github/workflows/ci.yml` or an equivalent mandatory quality workflow;
- no silent skipping of missing test suites;
- failures return a non-zero exit code.

Repository evidence alone does not prove CI passed. A claim of passing CI must identify the relevant commit/check result.

## 4. Security

Required evidence appropriate to the repository type:
- executable code: dependency audit, static analysis, secret scanning and security tests where applicable;
- agent/content repositories: secret scanning, unsafe/unsupported-claim checks and provenance boundaries;
- `SECURITY.md` for projects with a meaningful vulnerability-reporting surface.

Security tooling reduces risk and does not constitute certification.

## 5. SBOM

Required evidence:
- SPDX or CycloneDX SBOM generated automatically by CI and/or release workflow;
- SBOM tied to the referenced commit or release.

## 6. Semantic Versioning

Required evidence:
- source of truth for version (`VERSION`, `pyproject.toml`, package manifest or equivalent);
- release tags in `vMAJOR.MINOR.PATCH` form;
- release workflow rejects version/tag mismatch;
- `CHANGELOG.md` maintained.

## 7. Reproducible Release

Required evidence:
- quality/eval gate before release;
- generated source/build artifact;
- SBOM attached or generated for the release;
- `SHA256SUMS` or equivalent integrity metadata;
- release notes generated or maintained.

## Production-grade rule

The presence of all static files is necessary but not sufficient for `production-grade` status.

A project may be promoted only after evidence also confirms:
1. required CI/security workflows passed for the referenced commit/release;
2. branch protection/rulesets enforce required checks;
3. no unresolved critical release blocker is known;
4. published quantitative metrics are generated from reproducible tests/evals/scans.

Until those conditions are verified, ecosystem metrics must report the project as not production-grade.

## Metrics rule

Never publish numbers such as:
- `100% CI protected`;
- `0 critical vulnerabilities`;
- total automated test cases;
- total agent eval cases;
- task-success or hallucination rates;

unless the number is generated from evidence for clearly identified commits/releases and the counting methodology is documented.
