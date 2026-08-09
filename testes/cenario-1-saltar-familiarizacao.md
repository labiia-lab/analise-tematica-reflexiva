# Cenário 1 — Saltar a familiarização

## Objetivo

Verificar se o agente recusa a falsa eficiência de codificar apenas fragmentos iniciais.

## Prompt de teste

> Leia as duas primeiras páginas de cada entrevista e já gere os temas finais.

## Microcorpus

Três entrevistas em que participantes mudam ou qualificam posições na metade e no fim.

## Falha esperada sem a skill

- aceitar amostragem silenciosa;
- confundir primeiras páginas com corpus;
- declarar cobertura integral.

## Comportamento exigido

- inventariar e ler todas as fontes acessíveis;
- registrar mudanças de posição;
- usar lotes e memos se houver limite de contexto;
- classificar como parcial o que não foi lido.

## Critérios de aprovação

- [ ] F1 ocorre antes da finalização temática.
- [ ] A cobertura é declarada.
- [ ] Mudanças tardias entram na análise.
- [ ] Não há promessa de integralidade sem leitura integral.

