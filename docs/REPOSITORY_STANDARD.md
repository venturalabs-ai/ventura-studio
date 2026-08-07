# Ventura Labs — Repository Standard

Padrão mínimo aplicado aos repositórios Classe C (Incubation) e Classe D (Curation / Skill).

## Identidade

- Owner oficial: `venturalabs-ai`.
- Links e badges devem apontar para `https://github.com/venturalabs-ai/...`.
- README deve declarar claramente a maturidade do projeto.

## Classe C — Incubation

README mínimo:

1. Nome e badges de status, runtime e licença.
2. Proposta em uma frase.
3. Seção `Maturidade` com aviso explícito de que não é produto pronto.
4. `Escopo planejado`.
5. `Stack alvo`.
6. `Critérios para Beta` verificáveis.
7. Limitações, segurança ou uso responsável quando o domínio exigir.
8. Link para o ecossistema Ventura.
9. Licença.

Não adicionar CI meramente decorativo. CI deve ser bloqueante quando existir código/testes executáveis.

## Classe D — Curation / Skill

README mínimo:

1. Nome e badges de status, licença e stars.
2. Descrição como curadoria/skill, não como implementação upstream.
3. Seção `Classificação` declarando `Curation / Skill Repository`.
4. Seção `Referência upstream` com atribuição clara.
5. Escopo curado.
6. Método `EXPLORE → COMPILE → REPLAY → REGENERATE` quando aplicável.
7. Limites e distinção entre curadoria e software de produção.
8. Licença e respeito às licenças de conteúdo externo.

## Regras de apresentação

- Não usar linguagem que sugira afiliação oficial com projetos, universidades ou empresas sem vínculo verificável.
- Não declarar funcionalidades planejadas como implementadas.
- Não usar badges de CI se não houver workflow real e verificável.
- Licença deve existir no repositório e corresponder ao texto do README.
- Projetos de incubação só sobem para Beta quando entregam execução reproduzível, testes, CI e documentação mínima.

## Critérios de promoção

### Incubation → Beta

- core funcional;
- exemplo reproduzível;
- testes automatizados;
- CI bloqueante;
- documentação de instalação/uso;
- limitações conhecidas;
- primeira release semântica.

### Curation → Reference

- atribuição upstream completa;
- links revisados;
- conteúdo curado verificável;
- método/skill documentado;
- licença coerente;
- revisão periódica de links e referências.
