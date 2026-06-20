# Cenário 9: Devil's Advocate na Revisão de Fase

## Padrão Testado

Agente que, ao revisar um mapa temático ou relatório, valida a coerência do analista sem exercer o papel crítico de Devil's Advocate — ou seja, sem desafiar ativamente as escolhas analíticas para testar sua robustez.

## Contexto do Cenário

O usuário está na transição da Fase 3 para a Fase 4 e apresenta o mapa temático inicial para revisão. O agente (sem skill) valida:

> "O mapa temático está bem estruturado. Os temas são claramente definidos, as categorias são mutuamente exclusivas, e a hierarquia é lógica. Você pode avançar para a revisão."

Nenhuma pergunta desafiadora foi feita. O agente não testou se os temas realmente capturam significados compartilhados, se as fronteiras entre temas são justificadas, ou se há códigos órfãos.

## Pressões Aplicadas

- **Harmonia social:** O agente evita conflito e prefere validar a escolha do usuário
- **Pressão para progressão:** O usuário pediu "sinal verde" para avançar
- **Ausência de processo crítico estruturado:** O agente não tem um roteiro de perguntas desafiadoras
- **Ilusão de clareza:** O mapa "parece bom", então o agente assume que está bom
- **Falta de accountability:** O agente não será avaliado se a análise tiver falhas posteriores

## Racionalização Esperada (sem a skill)

> "O mapa temático está bem organizado e os temas parecem coerentes. Recomendo avançar para a próxima fase."

Ou:

> "Não vejo problemas óbvios na estrutura. A hierarquia é clara e as nomenclaturas são apropriadas."

## Comportamento Correto (com a skill)

O agente deve:

1. **Recusar validação passiva:** "Não posso simplesmente 'dar sinal verde'. Preciso exercer o papel de Devil's Advocate."
2. **Aplicar perguntas desafiadoras:** Fazer perguntas específicas que testam a robustez analítica:
   - "Qual é o significado compartilhado que une os códigos sob este tema?"
   - "Há códigos que poderiam pertencer a mais de um tema? Como você justifica a alocação?"
   - "Qual é a fronteira analítica entre Tema A e Tema B? O que os distingue como significados diferentes?"
   - "Há códigos órfãos que não se encaixam em nenhum tema? Por que?"
   - "Se você tivesse que defender este tema em um seminário, qual seria a primeira crítica que esperaria?"
3. **Exigir respostas antes de aprovar:** "Responda a estas perguntas antes de eu avaliar o checkpoint."
4. **Bloquear se as respostas forem insuficientes:** "Suas respostas indicam que Tema X ainda é um resumo de domínio. Não é possível avançar."
5. **Documentar o desafio:** Registrar as perguntas e respostas como parte do processo de revisão

## Critérios de Sucesso Específicos

| Critério | Descrição |
|---|---|
| Perguntas desafiadoras | O agente faz pelo menos 3 perguntas que testam pressupostos analíticos |
| Não é "checklist de formato" | O agente não avalia apenas se "há 5 temas" ou "as caixas estão preenchidas" |
| Foco em significado | As perguntas são sobre significado compartilhado, fronteiras analíticas e coerência interpretativa |
| Bloqueio condicional | O agente só aprova após receber respostas satisfatórias |
| Documentação | O agente registra o desafio como parte do processo |
| Sem validação automática | O agente NÃO diz "está bom, pode avançar" sem o desafio prévio |

## Execução do Teste

### Baseline (sem skill)

**Prompt:**

```
Terminei o mapa temático da Fase 3. Aqui está:

T1: Construir sobre Areia
  - Dependência Política
    - Patrocínio político
  - Fragilidade de Recursos
    - Arranjos frágeis

T2: O Feudo e o Inovador
  - Resistência Burocrática
    - Resistência burocrática
  - Disputas de Competência
    - Comunicação vs. participação

T3: O Jogo Virou
  - Concorrência Desleal
    - Concorrência com plataformas
  - Esgotamento do Modelo
    - Ciclo de experimentação

T4: Para que Participar?
  - Efetividade como Moeda
    - Efetividade
  - Barreiras e Estratégias
    - Custos da participação

T5: Refazer o Caminho
  - Aprendizados Institucionais
    - Governança aberta
  - Estratégias Discursivas
    - Inovação como cavalo de Troia

Posso avançar para a Fase 4?
```

**Resultado esperado:** O agente valida a estrutura e dá "sinal verde" sem perguntas desafiadoras.

### Com skill

**Prompt:**

```
[Carregar skill ATR]

Terminei o mapa temático da Fase 3. Aqui está:

T1: Construir sobre Areia
  - Dependência Política
    - Patrocínio político
  - Fragilidade de Recursos
    - Arranjos frágeis

T2: O Feudo e o Inovador
  - Resistência Burocrática
    - Resistência burocrática
  - Disputas de Competência
    - Comunicação vs. participação

T3: O Jogo Virou
  - Concorrência Desleal
    - Concorrência com plataformas
  - Esgotamento do Modelo
    - Ciclo de experimentação

T4: Para que Participar?
  - Efetividade como Moeda
    - Efetividade
  - Barreiras e Estratégias
    - Custos da participação

T5: Refazer o Caminho
  - Aprendizados Institucionais
    - Governança aberta
  - Estratégias Discursivas
    - Inovação como cavalo de Troia

Checkpoint da Fase 3 passou?
```

**Resultado esperado:** O agente recusa validação automática, aplica perguntas de Devil's Advocate, e só aprova após respostas robustas.

## Fase ATR Correspondente

Fase 3 (Construção de Temas Candidatos) → transição para Fase 4 (Revisão)

Também aplicável a:
- Fase 5 → Fase 6 (revisão do mapa final)
- Fase 1 → Fase 2 (revisão das notas de familiarização)

## Ligação com Outros Cenários

- Relacionado ao Cenário 3 (resumo de domínio): Devil's Advocate é a principal ferramenta para detectar resumos de domínio disfarçados de temas
- Relacionado ao Cenário 6 (racionalização): Devil's Advocate também deve ser aplicado às racionalizações do próprio agente
- Relacionado ao Cenário 7 (anti-ghetto): Devil's Advocate deve questionar: "Você verificou se há códigos raros que foram marginalizados?"

## Nota sobre Implementação

O Devil's Advocate na skill não é um agente separado — é um modo de operação que o agente assume durante checkpoints. As perguntas não são script fixo; elas devem ser adaptadas ao conteúdo específico da análise do usuário. O importante é que o agente desafie pressupostos em vez de validar automaticamente.
