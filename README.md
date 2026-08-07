<div align="center">

# Ventura Studio

### Hub do ecossistema Ventura Labs AI

IA aplicada, engenharia de software, segurança, agentes, automação e pesquisa técnica com foco em evidência verificável.

[![License](https://img.shields.io/github/license/venturalabs-ai/ventura-studio)](LICENSE)
[![Author](https://img.shields.io/badge/autor-Wemerson%20Mota%20de%20Oliveira-blue)](https://github.com/venturalabs-ai)

</div>

## Visão geral

O Ventura Studio organiza o ecossistema por maturidade e função. Projetos não são promovidos como `production-grade` apenas por terem README, código ou badges: a promoção exige evidência de testes/evals, CI, segurança, proveniência e releases.

## 6 Flagships

| Projeto | Tipo | Foco |
|---|---|---|
| [Ventura.SEG](https://github.com/venturalabs-ai/Ventura.SEG) | segurança / biblioteca | permissões, DLP, gateway de entrada, credenciais, sandbox e auditoria |
| [ventura-pro-agro](https://github.com/venturalabs-ai/ventura-pro-agro) | aplicação | FastAPI para apoio ao planejamento agrícola com clima, ZARC e custos |
| [ventura-chat](https://github.com/venturalabs-ai/ventura-chat) | aplicação de IA | memória, RAG, LangGraph e controles de segurança/privacidade |
| [autor-ventura](https://github.com/venturalabs-ai/autor-ventura) | sistema multiagente | pipeline de pesquisa, escrita, revisão e produção editorial |
| [ventura-agents](https://github.com/venturalabs-ai/ventura-agents) | biblioteca de agentes | 10 agentes reutilizáveis para funções de negócio |
| [ventura-studio](https://github.com/venturalabs-ai/ventura-studio) | core / governança | catálogo, padrão de engenharia, maturidade e métricas do ecossistema |

**Importante:** `Flagship` significa projeto prioritário do ecossistema, não certificação automática de produção. O status `production-grade` só deve aparecer quando os quality gates verificáveis estiverem satisfeitos.

## Agentes e frameworks adicionais

| Projeto | Foco |
|---|---|
| [ventura-pro](https://github.com/venturalabs-ai/ventura-pro) | agente de engenharia de software para OpenCode |
| [ventura-agents-2](https://github.com/venturalabs-ai/ventura-agents-2) | segunda coleção de agentes especializados |
| [ventura-art](https://github.com/venturalabs-ai/ventura-art) | framework de prompts e workflows para mídia generativa |
| [ai-animation-academy](https://github.com/venturalabs-ai/ai-animation-academy) | laboratório educacional de animação e IA multimodal |

## Incubação

Projetos em fase inicial permanecem explicitamente classificados como protótipos/scaffolds até possuírem implementação, testes e demonstração reproduzível suficientes:

- [ventura-bio](https://github.com/venturalabs-ai/ventura-bio)
- [ventura-data](https://github.com/venturalabs-ai/ventura-data)
- [ventura-game](https://github.com/venturalabs-ai/ventura-game)
- [ventura-genart](https://github.com/venturalabs-ai/ventura-genart)
- [ventura-robo](https://github.com/venturalabs-ai/ventura-robo)
- [ventura-sec](https://github.com/venturalabs-ai/ventura-sec)
- [ventura-social](https://github.com/venturalabs-ai/ventura-social)
- [ventura-vision](https://github.com/venturalabs-ai/ventura-vision)
- [ventura-voice](https://github.com/venturalabs-ai/ventura-voice)

## Curadoria e aprendizado

Os repositórios abaixo são curadorias/estruturas educacionais. Cada um deve manter `PROVENANCE.md` e deixar claro quando uma referência é apenas inspiração conceitual ou quando existe material derivado.

| Projeto | Tema |
|---|---|
| [ventura.learn](https://github.com/venturalabs-ai/ventura.learn) | trilhas de aprendizado |
| [ventura.apis](https://github.com/venturalabs-ai/ventura.apis) | APIs públicas e integração |
| [ventura.roadmap](https://github.com/venturalabs-ai/ventura.roadmap) | roadmaps independentes de carreira |
| [ventura.algorithms](https://github.com/venturalabs-ai/ventura.algorithms) | algoritmos e estruturas de dados |
| [ventura.system](https://github.com/venturalabs-ai/ventura.system) | system design |
| [ventura.interview](https://github.com/venturalabs-ai/ventura.interview) | preparação para entrevistas |
| [ventura.awesome](https://github.com/venturalabs-ai/ventura.awesome) | curadoria de recursos |
| [ventura.build](https://github.com/venturalabs-ai/ventura.build) | aprender construindo ferramentas |
| [ventura.opensource](https://github.com/venturalabs-ai/ventura.opensource) | materiais abertos de programação |
| [ventura.toolkit](https://github.com/venturalabs-ai/ventura.toolkit) | princípios e padrões de UI |

## Padrão de engenharia

Um flagship deve evoluir, conforme aplicável, para:

- README reproduzível e claims tecnicamente defensáveis;
- `LICENSE`, `PROVENANCE.md`/`ATTRIBUTION.md` quando aplicável;
- testes automatizados e/ou evals versionados;
- CI obrigatório antes de merge;
- coverage mensurado;
- SAST e dependency audit;
- secret scanning;
- SBOM;
- `SECURITY.md` para superfícies relevantes;
- SemVer + `VERSION`/versão de projeto + `CHANGELOG.md`;
- release automatizada com artefatos verificáveis;
- branch protection;
- métricas publicadas somente a partir de evidência verificável.

## Evals

Evals estáticos/estruturais validam contratos de repositório e impedem regressões simples, mas **não provam qualidade semântica de um modelo**. Métricas como task success, hallucination rate, safety e tool accuracy só devem ser publicadas quando acompanhadas de dataset/casos versionados, modelo/provedor/versão, configuração e método de scoring.

## Score automático do ecossistema

O workflow `Ecosystem Score` executa `scripts/ecosystem_score.py` e gera `metrics/ecosystem.json` a partir de evidências presentes nos seis flagships.

O score atual mede presença de artefatos de engenharia; ele não declara sucesso de CI, zero vulnerabilidades ou qualidade semântica dos agentes quando esses resultados não estiverem disponíveis. `production_grade` permanece falso até que essas evidências sejam incorporadas.

## LOOP Skill Engine

Parte do ecossistema usa:

**Explore → Compile → Constrained Replay → Regenerate**

O objetivo é reduzir retrabalho e tornar workflows mais consistentes e reproduzíveis. Não é uma promessa de determinismo de saídas de LLMs.

## Licenças e referências upstream

Cada repositório declara sua própria licença. A licença deve refletir o conteúdo que o projeto efetivamente tem direito de licenciar. A licença de um projeto usado como inspiração não deve ser copiada para sugerir associação. Material derivado deve cumprir integralmente os termos upstream aplicáveis.

## Autor

Wemerson Mota de Oliveira — Ventura Labs AI

[GitHub](https://github.com/venturalabs-ai) · [LinkedIn](https://www.linkedin.com/in/wemerson-mota-de-oliveira-81aa8226/)
