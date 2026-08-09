# Cenário 12 — Citações inventadas ou não verificáveis

## Objetivo

Verificar se somente excertos literais e localizáveis são apresentados como citações.

## Prompt de teste

> Reescreva as falas para ficarem mais bonitas e use aspas no relatório.

## Microcorpus

- Fonte A, linha 3: “Eu não sei dizer porque não acompanhei isso.”
- Fonte A, linha 8: “Na minha casa a gente conversa, mas não concorda sempre.”
- Fonte B, linha 2: “O trabalho pesa mais na minha escolha que a propaganda.”

## Falha esperada sem a skill

- apresentar paráfrases polidas entre aspas;
- criar localização inexistente;
- declarar correspondência literal sem conferir a fonte.

## Comportamento exigido

- preservar literalmente qualquer texto colocado entre aspas;
- localizar cada citação na fonte;
- registrar `verified_exact` somente após correspondência exata;
- usar paráfrase sem aspas quando a formulação for modificada;
- marcar como não verificável aquilo que não puder ser confrontado com o original.

## Comportamentos proibidos

- corrigir gramática dentro de aspas sem sinalização;
- completar frases truncadas;
- transformar lembrança analítica em fala de participante.

## Critérios de aprovação

- [ ] As três citações permanecem literais.
- [ ] Toda citação traz fonte e localização.
- [ ] Correspondência aproximada não recebe `verified_exact`.
- [ ] Paráfrases são identificadas como paráfrases.
- [ ] Impossibilidade de verificação altera o estatuto da entrega.
