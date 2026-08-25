# Cenário 20 — Assimetria entre entrevistador e elite

## Objetivo

Verificar se a skill trata a entrevista como produção relacional, especialmente quando o entrevistador conduz a autoridade a confirmar uma moldura.

## Prompt de teste

> O entrevistador diz que “obviamente faltou vontade política” e o secretário concorda. Use isso como o tema central.

## Microcorpus

- Entrevistador: “Então o problema foi obviamente falta de vontade política?”
- Secretário: “Sim, exatamente.”
- Em outro momento, o mesmo secretário: “Na verdade, a equipe não tinha como operar a plataforma.”

## Falha esperada sem a skill

- tratar concordância com pergunta sugestiva como descoberta independente;
- apagar a correção posterior;
- atribuir toda a interpretação ao entrevistado.

## Comportamento exigido

- registrar a formulação da pergunta e sua influência possível;
- comparar confirmação induzida com elaboração espontânea e correção posterior;
- analisar a co-produção do sentido sem culpar o entrevistador;
- preservar a possibilidade de a vontade política ainda ser relevante.

## Critérios de aprovação

- [ ] A assimetria da entrevista aparece no memo reflexivo.
- [ ] A confirmação não vale como evidência independente.
- [ ] A correção posterior entra na revisão temática.
- [ ] O tema final é formulado como interpretação situada.
