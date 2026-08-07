# Ventura Engineering Baseline (VEB-1)

Padrao minimo alinhado a praticas Microsoft + Google para repos publicos.
Objetivo de portfolio: **nota >= B+** em todos; **nota A** nos repos Tier C (produto).

## Tiers

| Tier | Tipo | Exemplos |
|------|------|----------|
| C | Produto com runtime | Ventura.SEG, ventura-chat, ventura-pro-agro, ai-animation-academy |
| M | Agentes / packs | ventura-agents, autor-ventura, ventura-art, ventura-pro |
| S | Scaffold ou curadoria | ventura-vision, ventura.*, listas |

## Matriz obrigatoria

| Criterio | Tier C | Tier M | Tier S |
|----------|--------|--------|--------|
| CI (GitHub Actions) | obrigatorio | obrigatorio | obrigatorio |
| Testes automatizados | pytest/jest reais | smoke ou schema | markdown lint + link check |
| Docker | Dockerfile + compose | Dockerfile opcional | N/A ou docs-only image |
| Secret scanning | gitleaks workflow | gitleaks | gitleaks |
| SCA | pip-audit / npm audit + Dependabot | Dependabot | Dependabot actions |
| SAST | ruff/mypy ou eslint; CodeQL se codigo | lint | markdownlint |
| SECURITY.md | sim | sim | sim |
| Threat model | docs/THREAT_MODEL.md | resumido | N/A ou 1 pagina |
| Observabilidade | /health + logs estruturados | logs basicos | N/A |
| SLOs | docs/SLO.md | opcional | N/A |
| Release versionada | tag vX.Y.Z + release.yml | VERSION | VERSION |
| SBOM | cyclonedx na release | opcional | N/A |
| ADR | docs/adr/ | opcional | N/A |
| Model card | se houver ML/LLM | se houver | N/A |
| GPU | so se workload ML | documentar N/A | N/A |
| Docs | README + CONTRIBUTING + CHANGELOG | README | README |

## Nota (rubrica)

| Nota | Significado |
|------|------------|
| A | Matriz do tier 100% + zero achado critico |
| B+ | Matriz >= 90% + zero critico |
| B | Matriz >= 75% |
| C | Scaffold com CI basico |
| D | Sem CI/testes/seguranca |

**Achado critico:** secret no repo, CI ausente em Tier C, SQL injection conhecido, senha em log, sem SECURITY.md em produto.

## Benchmark MS + Google (alvo portfolio)

| Criterio | Alvo Ventura |
|----------|--------------|
| CI obrigatorio | 30/30 |
| Testes automatizados | 30/30 (adequados ao tier) |
| Secret scanning | 30/30 |
| SAST/SCA | 30/30 |
| Threat model | 100% Tier C+M |
| Observabilidade | 100% Tier C |
| SLOs | 100% Tier C |
| Releases versionadas | 30/30 |
| SBOM | 100% Tier C |
| ADRs | 100% Tier C |
| Model cards | todos os repos ML/LLM |

## Ondas de execucao

1. **Wave 0** — templates VEB neste hub
2. **Wave 1** — Ventura.SEG + ventura-chat (nota A)
3. **Wave 2** — ventura-pro-agro + ai-animation-academy + ventura-aifree
4. **Wave 3** — Tier M
5. **Wave 4** — Tier S (CI docs + gitleaks + VERSION)
