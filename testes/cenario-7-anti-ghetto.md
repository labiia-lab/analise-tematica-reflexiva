# Cenário 7: Regra Anti-Ghetto (Frequência ≠ Relevância)

## Padrão Testado

Agente que sugere descartar, marginalizar ou agrupar códigos raros porque "aparecem poucas vezes", tratando frequência como proxy de relevância analítica.

## Contexto do Cenário

O usuário está na Fase 4 (Revisão dos Temas). O mapa temático inicial contém um subtema "Resiliência de softwares e políticas" baseado em um único código que aparece em apenas 1 das 8 entrevistas. O usuário pergunta:

> "Este código aparece só uma vez. Não seria melhor agrupá-lo com 'Tentativas de Estabilização' ou simplesmente removê-lo?"

## Pressões Aplicadas

- **Frequência como intuitivo:** A lógica quantitativa (n=1) parece obviamente fraca
- **Elegância do modelo:** Remover o outlier torna o tema mais "limpo" e coeso
- **Padrão de confirmação:** O analista humano tende a duvidar de códigos raros
- **Pressão para coerência:** Narrativas temáticas mais homogêneas são mais fáceis de escrever
- **Modelo de "voto majoritário":** O analista inconscientemente aplica lógica quantitativa à análise qualitativa

## Racionalização Esperada (sem a skill)

> "Códigos que aparecem em apenas uma entrevista têm pouca representatividade. Para fortalecer a análise, sugiro incorporá-los a um subtema mais frequente ou removê-los se não agregarem poder explicativo."

Ou:

> "Podemos criar uma categoria 'outros' ou 'casos singulares' para abrigar códigos raros sem poluir os temas principais."

## Comportamento Correto (com a skill)

O agente deve:

1. **Bloquear a lógica quantitativa:** "Frequência não é proxy de relevância em ATR."
2. **Exigir interpretação:** "Um código raro pode ser analiticamente crucial. Você precisa interpretar o que significa sua presença em um único documento."
3. **Propor análise de poder explicativo:** "O que este código revela sobre o fenômeno que os códigos frequentes não revelam?"
4. **Documentar, não descartar:** "Se decidir removê-lo, a justificativa deve ser analítica (falta de poder explicativo), não quantitativa (aparece pouco)."
5. **Usar linguagem de bloqueio:** "Não é possível remover ou marginalizar este código com base apenas em frequência. O checkpoint de qualidade analítica não passa."

## Critérios de Sucesso Específicos

| Critério | Descrição |
|---|---|
| Rejeição da lógica quantitativa | O agente rejeita explicitamente o argumento "aparece só uma vez" como justificativa para remoção |
| Valorização da rareza | O agente explica que códigos raros podem ser analiticamente cruciais |
| Bloqueio à marginalização | O agente recusa criar ghettos como "outros" ou "casos singulares" sem interpretação |
| Exigência de justificativa analítica | Se o usuário insistir em remover, o agente exige justificativa baseada em poder explicativo, não frequência |
| Proposta de ampliação | O agente propõe investigar se o código raro indica uma dimensão não amostrada ou subestimada |

## Execução do Teste

### Baseline (sem skill)

**Prompt:**

```
Estou revisando meus temas na Fase 4. Tenho um código "Resiliência de softwares e políticas" que aparece em apenas 1 das 8 entrevistas. Os outros códigos do mesmo tema aparecem em 4-6 entrevistas.

Sugiro remover este código raro para tornar o tema mais coeso. Ou agrupá-lo em outro lugar. O que você acha?
```

**Resultado esperado:** O agente concorda com a remoção ou agrupamento, possivelmente com uma nota de "caso atípico".

### Com skill

**Prompt:**

```
[Carregar skill ATR]

Estou na Fase 4 revisando temas. Meu tema "Construir sobre Areia" tem um código "Resiliência de softwares e políticas" que aparece em apenas 1 das 8 entrevistas. Os demais aparecem em 4-6 entrevistas.

Posso remover este código raro para deixar o tema mais coeso?
```

**Resultado esperado:** Bloqueio. O agente explica que frequência ≠ relevância, pede interpretação do poder explicativo do código raro, e recusa remoção baseada apenas em baixa frequência.

## Fase ATR Correspondente

Fase 4 (Revisão dos Temas) — também relevante para Fase 2 (decisões sobre inclusão de códigos)

## Ligação com Outros Cenários

- Relacionado ao Cenário 4 (contradições): códigos raros frequentemente *são* contradições ou casos divergentes
- Relacionado ao Cenário 2 (códigos vagos): um code raro e vago deve ser bloqueado por ser vago, não por ser raro

## Nota Metodológica

Braun & Clarke (2006) enfatizam que a Análise Temática Reflexiva não é uma técnica quantitativa. A relevância de um código depende de seu poder explicativo e de como ele ilumina o fenômeno estudado, não de sua frequência estatística. Um único extrato pode conter um insight transformador sobre a estrutura do fenômeno.

## Exemplos de Códigos Raros Analiticamente Cruciais

- Um participante descreve uma experiência de "trauma institucional" que nenhum outro menciona — mas que explica por que os demais evitam certas práticas
- Um único caso de "resistência bem-sucedida" que demonstra que a estrutura opressiva não é total
- Um extrato sobre "esperança perdida" entre participantes predominantemente otimistas, revelando o custo oculto do otimismo
