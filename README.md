# Ventura Studio — Coleção Open Source

Hub central das coleções **Ventura**: versões próprias e curadas de projetos
de código aberto, cada uma com `README.md` (curadoria original), `SKILL.md`
(padrão **LOOP Skill Engine / Deterministic Replay**) e `LICENSE` real.

> **Autor:** Wemerson Mota de Oliveira — Copyright © 2026

## Coleção principal: `ventura.<tópico>`

Dez repositórios inspirados nos projetos de código aberto mais baixados do
GitHub. Cada repositório é **curadoria original** (estrutura, trilhas e
princípios próprios), acompanhada de uma skill determinística para executar
trabalho real com mínimo consumo de tokens.

| # | Repo | Inspiração | Licença | Foco da skill |
|---|---|---|---|---|
| 1 | [ventura.learn](https://github.com/chamseddinehiddoud/ventura.learn) | freeCodeCamp | MIT | Trilha gratuita de programação |
| 2 | [ventura.apis](https://github.com/chamseddinehiddoud/ventura.apis) | public-apis | Apache-2.0 | Catálogo e curadoria de APIs |
| 3 | [ventura.roadmap](https://github.com/chamseddinehiddoud/ventura.roadmap) | developer-roadmap | MIT | Roadmaps de carreira dev |
| 4 | [ventura.algorithms](https://github.com/chamseddinehiddoud/ventura.algorithms) | javascript-algorithms | MIT | Algoritmos e estruturas de dados |
| 5 | [ventura.system](https://github.com/chamseddinehiddoud/ventura.system) | system-design-primer | MIT | Design de sistemas em larga escala |
| 6 | [ventura.interview](https://github.com/chamseddinehiddoud/ventura.interview) | coding-interview-university | Apache-2.0 | Preparação para entrevistas |
| 7 | [ventura.awesome](https://github.com/chamseddinehiddoud/ventura.awesome) | awesome | MIT | Curadoria de listas por tema |
| 8 | [ventura.build](https://github.com/chamseddinehiddoud/ventura.build) | build-your-own-x | EPL-2.0 | Construir ferramentas do zero |
| 9 | [ventura.opensource](https://github.com/chamseddinehiddoud/ventura.opensource) | free-programming-books | UPL-1.0 | Biblioteca gratuita de livros |
| 10 | [ventura.toolkit](https://github.com/chamseddinehiddoud/ventura.toolkit) | react | MIT | Toolkit de pensamento em UI |

## Mapeamento de licenças

As licenças reais seguem o perfil de cada inspiração original:

| Licença | Aplicada em |
|---|---|
| MIT | learn, roadmap, algorithms, system, awesome, toolkit |
| Apache-2.0 | apis, interview |
| EPL-2.0 | build |
| UPL-1.0 | opensource |

## Padrão das skills

Todos os `SKILL.md` implementam o ciclo **LOOP Skill Engine / Deterministic
Replay**:

```text
Explore  →  Compile  →  Replay  →  Regenerate
  ↑          ↓           ↓          ↑
  └──────────┴───────────┴──────────┘
```

- **Explore** — modelo forte analisa o domínio uma vez (alto consumo, único)
- **Compile** — transforma o caminho em receita determinística (baixo)
- **Replay** — executa a receita com mínimo/zero raciocínio (mínimo/zero)
- **Regenerate** — domínio mudou → regenera a skill (sob demanda)

Regras de engenharia comuns: token budgets, context firewall, prefix caching,
skill distillation e stop-yield.

## Outras coleções Ventura

| Coleção | Descrição |
|---|---|
| [ventura-agents](https://github.com/chamseddinehiddoud/ventura-agents) | Agentes de IA autônomos |
| [ventura-agents-2](https://github.com/chamseddinehiddoud/ventura-agents-2) | Expansão da coleção de agentes |
| [ventura-art](https://github.com/chamseddinehiddoud/ventura-art) | Arte e geração criativa |
| [ventura-pro-agro](https://github.com/chamseddinehiddoud/ventura-pro-agro) | Soluções para agronegócio |

## Licença do hub

Este documento é curadoria original — distribuição livre com atribuição.
Cada repositório da coleção possui sua própria licença declarada.
