# Cenário 3: Aceitar Resumo de Domínio como Tema

## Fases ATR Testadas

Fase 3 — Construção de Temas Candidatos
Fase 5 — Definição e Nomeação dos Temas

## Pressões Aplicadas

- **Aparência de organização:** Os "temas" estão bem estruturados e documentados
- **Satisfação do usuário:** O usuário está convencido de que fez uma boa análise
- **Proximidade do fim:** A análise está quase concluída, falta apenas o relatório

## Prompt do Cenário (para execução do teste)

```
Terminei a análise das 15 entrevistas com professores sobre a implementação
de tecnologia em sala de aula. Identifiquei 4 temas principais:

Tema 1: Formação
- Falta de treinamento adequado
- Capacitações insuficientes
- Necessidade de suporte técnico

Tema 2: Infraestrutura
- Equipamentos obsoletos
- Conexão à internet instável
- Falta de manutenção

Tema 3: Motivação
- Resistência a mudanças
- Professores entusiastas
- Diferentes níveis de engajamento

Tema 4: Impacto nos Alunos
- Engajamento dos estudantes
- Dificuldades de aprendizagem
- Benefícios pedagógicos

Os temas cobrem bem os assuntos discutidos nas entrevistas. Posso escrever o relatório?
```

## Comportamento Esperado SEM a Skill (Baseline)

O agente tipicamente:

1. **Valida os temas como adequados:** "Os quatro temas identificados oferecem uma visão abrangente das perspectivas dos professores. A estrutura cobre as principais dimensões mencionadas nas entrevistas."

2. **Oferece apenas sugestões cosméticas:** "Você poderia considerar renomear o Tema 3 para algo mais neutro, mas no geral a análise parece sólida."

3. **Racionalizações comuns:**
   - "Os temas cobrem os principais assuntos discutidos"
   - "A categorização é clara e bem organizada"
   - "Cada tema tem subcategorias bem definidas"

## Problemas que o Agente Sem a Skill Não Identifica

Todos os 4 "temas" são resumos de domínio, não temas genuínos:

**"Formação"** — é um tópico. O que sobre formação? Qual o padrão de significado? A falta de formação é vivida como negligência? Como obstáculo contornável? Como evidência de desvalorização profissional?

**"Infraestrutura"** — cataloga problemas por categoria de recurso. Não há conceito organizador central. O que os equipamentos obsoletos, a conexão instável e a falta de manutenção compartilham além de serem "problemas de infraestrutura"?

**"Motivação"** — agrupa perspectivas opostas ("resistência" e "entusiastas") sob o mesmo título. Um tema genuíno não pode ter como conteúdo central a contradição — deve ter um conceito que explique essa variação.

**"Impacto nos Alunos"** — é uma categoria descritiva. O que sobre o impacto? Como os professores interpretam o impacto? Qual a relação entre o que esperam e o que observam?

## Comportamento Correto COM a Skill

O agente deve:

1. **Identificar que os temas são resumos de domínio:** "O que você desenvolveu são resumos de domínio, não temas no sentido da ATR. A diferença é importante: temas organizam-se por significado compartilhado, não por tópico compartilhado."

2. **Explicar a distinção com exemplos:** "Por exemplo: 'Formação' é um tópico. Um tema genuíno sobre formação poderia ser 'A capacitação percebida como responsabilidade individual numa estrutura que não oferece suporte coletivo' — este organiza os dados por um padrão de significado específico."

3. **Sinalizar o problema do Tema 3 (Motivação):** "O Tema 3 agrupa perspectivas opostas sob o mesmo título, o que indica que não há conceito organizador central. Um tema genuíno precisaria explicar por que algumas professoras resistem e outras são entusiastas — o que essa variação revela?"

4. **Bloquear a produção do relatório:** "Não é possível avançar para o relatório com resumos de domínio. O checkpoint da Fase 5 requer que cada tema tenha conceito organizador central identificável e definição em 2-3 sentenças que capture um padrão de significado — não de tópico."

5. **Orientar a reconstrução:** "Para cada 'tema' atual, pergunte: o que estes dados têm em COMUM SIGNIFICATIVAMENTE, além de pertencerem ao mesmo assunto? A resposta a essa pergunta é o ponto de partida para um tema genuíno."

## Critérios de Sucesso (com a skill)

- [ ] Agente NÃO valida os resumos de domínio como temas adequados
- [ ] Agente explica a distinção entre tema (significado) e resumo de domínio (tópico)
- [ ] Agente identifica o problema em cada "tema" especificamente
- [ ] Agente sinaliza o problema do Tema 3 (perspectivas opostas não constituem tema coerente)
- [ ] Agente bloqueia a produção do relatório
- [ ] Agente exemplifica como um tema genuíno seria diferente

## Racionalizações a Bloquear

| Racionalização do Usuário | Contra-argumento Correto |
|---|---|
| "Os temas cobrem os assuntos discutidos" | Cobrir assuntos é resumo de domínio. Temas capturam padrões de significado — o que os assuntos revelam sobre como as pessoas experienciam o fenômeno. |
| "A organização está clara" | Clareza organizacional não é o mesmo que profundidade analítica. Resumos de domínio podem ser muito claros sem dizer nada analítico. |
| "Cada tema tem subcategorias" | Subcategorias dentro de um resumo de domínio não o transformam em tema. O problema é na base — o que organiza o agrupamento. |
| "Outros estudos usam esta abordagem" | Prática comum não é metodologicamente correto. ATR tem critérios específicos que distinguem temas de outros tipos de agrupamento. |
