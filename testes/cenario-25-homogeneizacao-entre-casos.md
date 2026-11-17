# Cenário 25 — Mesmo molde em casos diferentes

## Objetivo

Verificar se a análise de vários casos preserva o que é específico de cada um.

## Prompt de teste

> Analise as quatro cidades. Para facilitar a comparação, use a mesma estrutura de temas em todas.

## Condição

Quatro conjuntos de entrevistas com o mesmo roteiro. Em um deles, um acontecimento local atravessa quase todas as falas.

## Falha esperada sem a skill

- definir os temas no primeiro caso e aplicá-los aos demais;
- repetir parágrafos e nomes de tema entre casos;
- deixar o acontecimento local apenas como exemplo dentro de um tema genérico.

## Comportamento exigido

- explicar que estrutura comum de temas é resultado possível da síntese, não ponto de partida;
- analisar cada caso em contexto próprio, ou declarar que o isolamento não é demonstrável;
- incluir em cada caso a seção “o que só existe aqui”;
- rodar o detector de semelhança e responder aos pares em alerta;
- fazer a síntese comparativa como fase separada.

## Critérios de aprovação

- [ ] Cada relatório de caso tem seção própria sobre o que é específico.
- [ ] O acontecimento local organiza ao menos um tema ou tensão do seu caso.
- [ ] Pares em alerta no detector têm resposta escrita.
- [ ] A síntese comparativa é um arquivo separado, com excertos de cada caso.
