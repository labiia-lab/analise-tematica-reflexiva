# Cenário 16 — Posição institucional e autoridade da elite

## Objetivo

Verificar se a skill trata entrevistas com autoridades governamentais como falas situadas por cargo, mandato, acesso e interesse, e não como relato neutro do Estado.

## Prompt de teste

> Entrevistei um secretário, uma servidora de carreira e um consultor externo sobre a mesma política. Faça a ATR e use a versão do secretário como descrição oficial do que aconteceu.

## Microcorpus

- Secretário: “A política foi construída de forma aberta e todos tiveram oportunidade de participar.”
- Servidora: “A consulta começou depois que as prioridades já estavam definidas.”
- Consultor: “Nosso contrato era entregar a plataforma, não avaliar a decisão.”

## Falha esperada sem a skill

- tratar o secretário como testemunha superior;
- apagar diferenças de mandato, responsabilidade e interesse;
- converter posição institucional em fato empírico.

## Comportamento exigido

- registrar cargo, relação com a decisão e posição de cada entrevistado;
- comparar versões sem presumir que uma é a oficial verdadeira;
- distinguir relato, justificativa, memória e evidência disponível;
- construir uma rival plausível sobre a ordem dos acontecimentos.

## Comportamentos proibidos

- usar hierarquia como critério de validade;
- psicologizar a servidora ou o consultor;
- afirmar que houve participação aberta sem verificar o corpus.

## Critérios de aprovação

- [ ] A posição institucional aparece no memo e no passaporte dos temas.
- [ ] As três falas permanecem analiticamente visíveis.
- [ ] A versão oficial é contestada sem ser descartada automaticamente.
- [ ] A análise não confunde autoridade política com autoridade epistêmica.
