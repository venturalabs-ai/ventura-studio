# Portfolio Scorecard — Ventura Labs

Atualizado: 2026-08-07
Baseline: [ENGINEERING_BASELINE.md](./ENGINEERING_BASELINE.md) (VEB-1)

## Sumario executivo

| Meta | Estado |
|------|--------|
| Nota >= B+ em todos | **Em progresso** (Wave 1 iniciada) |
| Nota A nos Tier C | **ventura-chat ~A-** apos Docker/API/threat/SLO/model card |
| Achados criticos | **0 conhecidos** nos repos Wave 1 |
| Benchmark MS+Google 100% verde | **Nao** — portfolio inteiro ainda parcial |

### Benchmark Microsoft + Google (portfolio)

| Criterio | MS | Google | Ventura agora | Status |
|----------|----|--------|---------------|--------|
| CI obrigatorio | sim | sim | ~4–6/30 com CI real; outros placeholder/ausente | 🟡 |
| Testes automatizados | sim | sim | chat + SEG (+ agro parcial) | 🟡 |
| Secret scanning | sim | sim | chat (gitleaks); SEG security.yml | 🟡 |
| SAST/SCA | sim | sim | chat bandit+pip-audit; SEG parcial | 🟡 |
| Threat model | sim | parcial | chat + SEG | 🟡 |
| Observabilidade | sim | sim | chat /health | 🟡 |
| SLOs | parcial | sim | chat docs/SLO.md | 🟡 |
| Releases versionadas | sim | sim | chat+SEG release.yml | 🟡 |
| SBOM | sim | parcial | chat CI/release SBOM | 🟡 |
| ADRs | parcial | sim | chat ADR-0001 | 🟡 |
| Model cards | parcial | sim | chat MODEL_CARD | 🟡 |

> Nota honesta: marcar 30/30 verde **hoje** seria teatro. Ondas VEB-1 levam o portfolio a verde **por criterio**, com evidencia.

## Ranking por repositorio (Wave 1 focus)

| Repo | Tier | Nota | CI | Testes | Docker | Seguranca | Status |
|------|------|------|----|--------|--------|-----------|--------|
| ventura-chat | C | **A-** | ✅ | ✅ | ✅ | ✅ gitleaks+SCA+SECURITY | **Quase A** |
| Ventura.SEG | C | **B+/A-** | ✅ | ✅ | ✅ (existente) | ✅ workflows | **Consolidar** |
| ventura-pro-agro | C | B | parcial | parcial | ? | parcial | Wave 2 |
| ai-animation-academy | C | B | ? | ? | ? | ? | Wave 2 |
| ventura-aifree | C | B | ? | ? | ? | ? | Wave 2 |
| Tier M (agents, art, pro…) | M | C–B | misto | baixo | baixo | baixo | Wave 3 |
| Tier S (vision, curadoria…) | S | C | placeholder | lint-only | N/A | fraco | Wave 4 |

## O que foi entregue nesta sessao (Wave 1 — chat)

- Dockerfile + docker-compose + user nao-root + HEALTHCHECK
- FastAPI `/health` + `/v1/chat`
- security.yml (gitleaks + pip-audit)
- Dependabot
- THREAT_MODEL, SLO, MODEL_CARD, ADR, GPU policy
- test_api_health
- VEB-1 publicado em ventura-studio

## Proximas acoes (ordem)

1. Fechar **nota A** no chat (coverage gate estavel, tag `v0.1.0`)
2. Auditoria VEB em **Ventura.SEG** (preencher gaps vs matriz)
3. Wave 2 produtos
4. Script de propagacao Wave 4 (gitleaks + VERSION + SECURITY.md) em massa nos Tier S
