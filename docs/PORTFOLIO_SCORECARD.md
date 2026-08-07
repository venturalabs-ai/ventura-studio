# Portfolio Scorecard — Ventura Labs

Atualizado: 2026-08-07 (Wave 2 web apps)

## Tier C

| Repo | Nota | CI | Testes | Docker | Seguranca | Status |
|------|------|----|--------|--------|-----------|--------|
| Ventura.SEG | **A** | ✅ | ✅ | ✅ | ✅ | Concluido |
| ventura-chat | **A-** | ✅ | ✅ | ✅ | ✅ | Quase A |
| ventura-pro-agro | **B+** | ✅ | ✅ | ✅ | ✅ | Wave 2 |
| **ai-animation-academy** | **B+** | ✅ | lint+build | ✅ | ✅ | Wave 2 |
| **ventura-aifree** | **B+** | ✅ | lint+build | ✅ | ✅ | Wave 2 |

## Wave 2 entregue (academy + aifree)

- VERSION, Dockerfile standalone, compose
- CI (lint+build), security (gitleaks + npm audit), Dependabot, release
- THREAT_MODEL, SLO, MODEL_CARD, GPU, ADR, SECURITY
- next.config `output: 'standalone'`

## Proximo

- Wave 3 Tier M **ou** unit tests (vitest) para subir academy/aifree de B+ → A-
