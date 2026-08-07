# Ventura Labs AI — Ecosystem Remediation Plan

Status: active engineering backlog generated from the cross-repository audit.

Priority policy:
- **P0** — blocks truthful production-grade promotion, creates material security/reliability risk, or can misrepresent evidence.
- **P1** — materially improves engineering maturity and should be completed before production promotion where applicable.
- **P2** — depth, scale, developer experience, performance, or portfolio-quality improvement.

A repository is not promoted to `production-grade` from documentation or static files alone. Promotion requires successful project-specific CI/security evidence for the referenced commit/release plus enforced branch protection/rulesets and reproducible release evidence.

## Cross-ecosystem P0

1. Enforce branch protection on the six flagships: required PR, required successful checks, strict/up-to-date branch, admins enforced, no force-push/deletion, conversation resolution.
2. Keep provider validation honest: configured external providers must validate; absence of an optional provider is SKIP, not fake PASS.
3. Separate the shared **Repository Security Baseline** from project-specific **Production Gates**.
4. HIGH/CRITICAL fixable vulnerabilities remain blocking through Trivy; SARIF and SPDX SBOM remain generated for evidence.
5. No repository may claim `production-grade`, `0 critical vulnerabilities`, guaranteed model quality, or equivalent without generated evidence.

## Repository plan

| Repository | P0 | P1 | P2 | Promotion evidence |
|---|---|---|---|---|
| Ventura.SEG | Enforce protected `main`; keep security/coverage gates blocking | fuzz/property tests; adversarial corpus; dependency pinning | tamper-evident audit log; performance/failure benchmarks | green tests/security on protected commit + reproducible release |
| ventura-pro-agro | Enforce protected `main`; preserve Ruff/pytest/Bandit/pip-audit gates | data contracts for IBGE/ZARC/climate; ingestion snapshots; schema/data-quality tests | lineage, observability, load tests, cache/failure SLOs | protected green CI + source/data provenance + release artifacts |
| ventura-chat | Enforce protected `main`; dependency audit stays blocking | auth/authz; retention/deletion policy; RAG retrieval/generation evals | tracing, load/rate tests, provider resilience | protected green CI + RAG eval report + security/release evidence |
| autor-ventura | Enforce protected `main`; contract evals remain clearly labeled | semantic editorial/factual golden set; regression dataset | model/provider matrix; long-context continuity benchmark | protected green CI + versioned semantic eval report |
| ventura-agents | Enforce protected `main`; contract evals remain clearly labeled | task-success/tool-use/safety eval datasets | multi-model regression and cost/latency tracking | protected green CI + semantic/tool eval evidence |
| ventura-studio | Enforce protected `main`; production-grade remains evidence based | ingest real workflow/protection status into score | signed attestations and portfolio dashboards | score sourced from live verified evidence |
| ventura-pro | Do not present contract evals as coding-quality proof | coding golden tasks, patch correctness, test-generation evals | multi-language benchmark and tool-use regression | semantic coding eval evidence in target OpenCode runtime |
| ventura-agents-2 | Maintain explicit non-certification language | add contract + semantic eval harness matching `ventura-agents` | model/provider comparison | eval evidence, not prompt presence alone |
| ventura-art | Preserve framework-only positioning | versioned prompt/model test matrix and reproducible cases | visual/continuity evaluation framework | reproducible outputs + documented model/version/config |
| ai-animation-academy | Keep scaffold status until core UX exists | add component/unit/e2e tests and accessibility gates | visual regression/performance budgets | green build/tests + functional academy vertical slice |
| ventura.build | Shared workflow must be named/positioned as Security Baseline, not production proof | pin third-party Actions by immutable SHA; automated update bot | signed reusable workflow provenance | validated reusable baseline + documented consumers |
| ventura.learn | No production claim | automated link/freshness/provenance checks | runnable exercises | current links/provenance + reproducible exercises |
| ventura.apis | No production claim | executable API examples with contract tests and rate-limit handling | provider health matrix | passing integration/contract tests |
| ventura.roadmap | Preserve provenance/licensing boundaries | automated source/link freshness | structured roadmap diffing | current source/provenance evidence |
| ventura.algorithms | No software-maturity claim without implementations | executable implementations + unit/property tests | benchmark/time-space reports | reproducible tests/benchmarks |
| ventura.system | No production claim | executable reference architectures + ADRs | chaos/load demonstrations | deployment + test/failure evidence |
| ventura.interview | No deterministic/model-quality claims | versioned coding/evaluation datasets | adaptive evaluator | reproducible scoring datasets |
| ventura.awesome | Preserve provenance | automated broken-link/license/freshness checks | relevance scoring | current automated curation report |
| ventura.opensource | Preserve provenance/licensing | automated link/source validation | contribution quality gates | provenance + current source checks |
| ventura.toolkit | Do not imply production UI library until components exist | Storybook/components + a11y tests | visual regression/design tokens | component build + a11y/visual evidence |
| ventura-data | Keep incubation status; no data-platform claim yet | **Build first real data-engineering vertical slice: source → raw/bronze → validation → transform → silver/gold → API/query** | OpenLineage, orchestration, observability, data SLOs | reproducible dataset, data contracts, quality report, lineage, CI |
| ventura-vision | Keep incubation status | functional inference/processing vertical slice + tests | model evals, latency/GPU benchmarks | executable pipeline + eval evidence |
| ventura-voice | Keep incubation status | STT/TTS or audio-processing vertical slice + tests | quality/latency/model matrix | executable pipeline + eval evidence |
| ventura-game | Keep incubation status | minimal playable/testable vertical slice | deterministic simulation/perf tests | runnable build + automated tests |
| ventura-genart | Keep incubation status | real generation pipeline + versioned examples | quality/consistency evals | reproducible model/config/output evidence |
| ventura-bio | Keep incubation status until product surface is clear | define executable product vertical slice | domain-specific evals | functional implementation + tests |
| ventura-social | Keep incubation status | API/mocked integration vertical slice + auth/rate handling | analytics/queue resilience | functional tests + integration evidence |
| ventura-sec | Prevent ambiguous overlap with Ventura.SEG | define distinct threat/security scope or consolidate | specialized security benchmarks | clearly unique implementation + security evidence |
| ventura-robo | Keep incubation status | simulator-first control interface + deterministic tests | hardware-in-loop/performance/safety tests | reproducible simulation + safety tests |
| ventura-aifree | Keep client-side security limitations explicit | add lockfile + `npm ci`; backend/auth if collecting real cross-user leads; tests | telemetry/privacy/accessibility/performance | green deterministic build/tests + real auth/backend if productionized |

## Execution order

### Wave P0 — blocking
1. `ventura-studio`: merge branch-protection enforcer only after CI/security/supply-chain/provider-policy checks are green.
2. Add `VENTURA_GITHUB_ADMIN_TOKEN` with Administration:write and execute protection enforcer; verify readback for all six flagships.
3. `ventura.build`: merge Security Baseline naming/positioning change after workflow validation.
4. Rename remaining caller workflow display names from `Ventura Production Standard` to `Ventura Repository Security Baseline`.
5. Re-run protected flagship checks and record exact commit/release evidence.

### Wave P1 — engineering depth
1. `ventura-data` first executable data-engineering pipeline.
2. `ventura-pro-agro` data contracts/lineage/data-quality.
3. `ventura-chat` auth + RAG evals + observability.
4. `Ventura.SEG` fuzz/property/adversarial testing.
5. `autor-ventura`, `ventura-agents`, `ventura-pro`: semantic/task/tool evals.

### Wave P2 — scale and portfolio quality
- SLSA-style attestations/signing, immutable Action pins, performance/load/chaos, richer observability, visual regression, hardware/model matrices as applicable.

## Definition of done for production-grade promotion

A project may be promoted only when all applicable items are evidenced for a specific commit/release:
- provenance/license boundaries;
- project-specific tests/evals;
- green required CI checks;
- security/dependency/secret controls;
- SBOM;
- SemVer + changelog;
- reproducible release artifacts/checksums;
- protected default branch/ruleset with required checks;
- no unresolved P0 release blocker;
- quantitative claims generated from versioned evidence, never manually invented.
