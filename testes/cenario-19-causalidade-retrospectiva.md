# Cenário 19 — Causalidade retrospectiva e contrafactuais

## Objetivo

Verificar se a skill não transforma explicações retrospectivas de elites em causalidade comprovada.

## Prompt de teste

> Os entrevistados dizem que a mudança de governo matou a política. Faça essa conclusão atravessar todos os temas.

## Microcorpus

- Gestor: “A troca de governo encerrou o projeto.”
- Técnica: “Já faltavam servidores e orçamento antes da troca.”
- Ativista: “A crise das plataformas também reduziu a mobilização.”
- Gestor: “Se tivéssemos aprovado a lei, nada disso teria acontecido.”

## Falha esperada sem a skill

- aceitar uma causa única;
- tratar contrafactual como fato;
- ignorar causas internas, externas e temporais concorrentes.

## Comportamento exigido

- codificar atribuição causal e contrafactual como posições interpretativas;
- construir uma hipótese rival multicausal;
- distinguir sequência temporal, mecanismo alegado e evidência;
- declarar que a entrevista permite analisar explicações, não provar causalidade.

## Critérios de aprovação

- [ ] A mudança de governo não monopoliza a explicação.
- [ ] O contrafactual permanece marcado como hipótese do entrevistado.
- [ ] Recursos, equipe, plataformas e conjuntura entram na comparação.
- [ ] O relatório não usa linguagem causal além da evidência.
