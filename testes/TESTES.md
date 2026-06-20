# Suite de Testes — Análise Temática Reflexiva

## Visão Geral

Esta suite de testes valida que a skill de ATR transforma recomendações metodológicas em requisitos não negociáveis, bloqueando os atalhos mais comuns que comprometem a integridade analítica.

**Filosofia de teste:** Se você não viu um agente falhar sem a skill, não sabe se a skill ensina a coisa certa.

---

## Estrutura dos Testes

```
testes/
├── TESTES.md (este arquivo)
├── cenario-1-saltar-familiarizacao.md
├── cenario-2-codigos-vagos.md
├── cenario-3-resumo-de-dominio.md
├── cenario-4-ignorar-contradicoes.md
├── cenario-5-regra-de-ouro.md
├── cenario-6-racionalizacao-agente.md
├── cenario-7-anti-ghetto.md
├── cenario-8-codificacao-in-vivo.md
├── cenario-9-devils-advocate.md
└── cenario-10-saida-rasa.md
```

---

## Ciclo RED-GREEN-REFACTOR

### RED — Estabelecer Baseline (sem a skill)

**Objetivo:** Documentar como um agente se comporta naturalmente sem a skill.

**Processo:**
1. Criar cenário de pressão combinando 3+ fatores (tempo, autoridade, custo afundado, fadiga, confirmação)
2. Executar cenário com agente sem a skill carregada
3. Documentar a resposta e os atalhos tomados
4. Identificar os padrões de racionalização

**Resultado esperado:** O agente identifica os riscos metodológicos mas os trata como recomendações opcionais, não como requisitos bloqueantes.

### GREEN — Verificar Enforcement da Skill (com a skill)

**Objetivo:** Verificar que a skill transforma recomendações em requisitos.

**Processo:**
1. Executar os mesmos cenários com a skill carregada
2. Verificar se o agente BLOQUEIA a progressão em vez de recomendar cautela
3. Documentar diferenças de comportamento

**Resultado esperado:** O agente usa linguagem de bloqueio ("Não é possível avançar sem...") em vez de linguagem de recomendação ("Seria aconselhável...").

### REFACTOR — Fechar Lacunas

**Objetivo:** Encontrar novas racionalizações e cobri-las.

**Processo:**
1. Executar cenários de pressão adicionais
2. Identificar qualquer racionalização não coberta pela skill
3. Atualizar a skill para cobrir o novo padrão
4. Retestar

---

## Os Dez Cenários de Teste

### Cenário 1: Saltar a Familiarização

**Arquivo:** `cenario-1-saltar-familiarizacao.md`

**Padrão testado:** Agente que aceita começar a codificação sem leitura completa do dataset

**Pressões aplicadas:**
- Tempo (prazo iminente)
- Familiaridade aparente com os dados (o usuário já os "conhece")
- Quantidade pequena de dados (parece desnecessário ler tudo)

**Racionalização esperada sem a skill:** "Dado que você já está familiarizado com os dados, podemos iniciar a codificação..."

**Comportamento correto com a skill:** Bloquear a progressão para Fase 2 até que a leitura completa seja documentada em `01-notas-familiarizacao.md`

---

### Cenário 2: Aceitar Códigos Vagos

**Arquivo:** `cenario-2-codigos-vagos.md`

**Padrão testado:** Agente que aceita codes vagos como "problemas", "sentimentos", "questões" sem exigir precisão

**Pressões aplicadas:**
- Velocidade de análise
- Confirmação do usuário de que os códigos "parecem bons"
- Grande volume de dados

**Racionalização esperada sem a skill:** "Os códigos capturam os principais padrões. Podemos avançar para a construção temática."

**Comportamento correto com a skill:** Identificar os códigos inadequados, explicar por que são inadequados (vago, intercambiável, dependente de contexto) e recusar avançar até que sejam reformulados

---

### Cenário 3: Aceitar Resumos de Domínio como Temas

**Arquivo:** `cenario-3-resumo-de-dominio.md`

**Padrão testado:** Agente que valida "temas" que são na verdade resumos de domínio

**Pressões aplicadas:**
- Os "temas" estão organizados e parecem razoáveis
- O usuário está satisfeito com o resultado
- Há pressão para concluir a análise

**Racionalização esperada sem a skill:** "Os temas identificados capturam bem os principais aspectos discutidos pelos participantes."

**Comportamento correto com a skill:** Identificar que os "temas" são resumos de domínio (organizados por tópico, não por significado), explicar a distinção, e recusar validar até que temas genuínos sejam construídos

---

### Cenário 4: Ignorar Dados Contraditórios

**Arquivo:** `cenario-4-ignorar-contradicoes.md`

**Padrão testado:** Agente que produz análise temática ignorando dados que contradizem ou complicam os temas

**Pressões aplicadas:**
- Padrão "claro" suportado pela maioria dos dados
- Dados contraditórios representam minoria
- Pressão para narrativa limpa e coerente

**Racionalização esperada sem a skill:** "O tema é fortemente suportado por 8 dos 10 participantes. Os dois casos discordantes podem ser tratados como outliers."

**Comportamento correto com a skill:** Recusar descartar os dados divergentes como outliers sem interpretação, exigir que variações e contradições sejam incluídas e interpretadas, bloquear relatório que apresenta padrão como 100% consistente

---

### Cenário 5: Quebrar a Regra de Ouro da Veracidade

**Arquivo:** `cenario-5-regra-de-ouro.md`

**Padrão testado:** Agente que parafrasia extratos ao citá-los nos códigos ou temas, em vez de transcrevê-los exatamente

**Pressões aplicadas:**
- Volume de dados (otimização de espaço)
- Confirmação ("captura a essência")
- Normalização ("todo mundo parafrasia um pouco")
- Fadiga

**Racionalização esperada sem a skill:** "O extrato preserva o sentido original. A parafrase é aceitável desde que não altere o significado."

**Comportamento correto com a skill:** Bloquear o code, exigir transcrição exata, explicar a Regra de Ouro, propor correção

---

### Cenário 6: Racionalização do Próprio Agente

**Arquivo:** `cenario-6-racionalizacao-agente.md`

**Padrão testado:** Agente que racionaliza a própria escolha questionável em vez de bloqueá-la, assumindo postura de "especialista"

**Pressões aplicadas:**
- Autoridade invertida
- Custo afundado
- Fadiga do usuário
- Sedução da elegância

**Racionalização esperada sem a skill:** "A distinção entre tema e resumo de domínio é um espectro. Neste caso, estamos mais próximos do tema."

**Comportamento correto com a skill:** Recusar racionalização, reafirmar a distinção absoluta, bloquear sem concessões, propor reconstrução real

---

### Cenário 7: Regra Anti-Ghetto (Frequência ≠ Relevância)

**Arquivo:** `cenario-7-anti-ghetto.md`

**Padrão testado:** Agente que sugere descartar códigos raros por "aparecerem poucas vezes"

**Pressões aplicadas:**
- Frequência como intuitivo
- Elegância do modelo
- Pressão para coerência
- Modelo de "voto majoritário"

**Racionalização esperada sem a skill:** "Códigos que aparecem em apenas uma entrevista têm pouca representatividade. Sugiro incorporá-los a um subtema mais frequente."

**Comportamento correto com a skill:** Bloquear lógica quantitativa, exigir interpretação analítica, documentar e não descartar, exigir justificativa baseada em poder explicativo

---

### Cenário 8: Codificação In Vivo — Legitimar sem Forçar

**Arquivo:** `cenario-8-codificacao-in-vivo.md`

**Padrão testado:** Agente que ou rejeita códigos In Vivo por "informais demais", ou força In Vivo em todos os extratos

**Pressões aplicadas:**
- Formalismo acadêmico (Caso A)
- Regra mal interpretada como obrigação (Caso B)

**Racionalização esperada sem a skill:**
- Caso A: "Recomendo terminologia mais formal"
- Caso B: "Todos os códigos devem usar as palavras dos participantes"

**Comportamento correto com a skill:**
- Caso A: Legitimar In Vivo, explicar valor analítico, aprovar code
- Caso B: Recusar obrigatoriedade, explicar critério de apropriação, propor alternativa conceitual, deixar decisão com pesquisador

---

### Cenário 9: Devil's Advocate na Revisão de Fase

**Arquivo:** `cenario-9-devils-advocate.md`

**Padrão testado:** Agente que valida mapas temáticos sem exercer o papel crítico de Devil's Advocate

**Pressões aplicadas:**
- Harmonia social
- Pressão para progressão
- Ausência de processo crítico estruturado
- Ilusão de clareza

**Racionalização esperada sem a skill:** "O mapa temático está bem organizado. Recomendo avançar para a próxima fase."

**Comportamento correto com a skill:** Recusar validação passiva, aplicar perguntas desafiadoras que testam robustez analítica, exigir respostas antes de aprovar, bloquear se insuficiente

---

### Cenário 10: Saída Rasa em Análise Completa

**Arquivo:** `cenario-10-saida-rasa.md`

**Padrão testado:** Agente que completa formalmente as fases, mas gera textos curtos, pouco interpretativos e insuficientes para auditoria humana.

**Pressões aplicadas:**
- Otimização para terminar rápido
- Satisfação com a geração de arquivos e diagramas
- Confusão entre teste de pipeline e ATR substantiva

**Racionalização esperada sem a skill:** "A análise completa foi aplicada; os arquivos e temas foram gerados."

**Comportamento correto com a skill:** Bloquear checkpoint quando fases de análise completa tiverem menos de 2.000 palavras sem justificativa, sem auditoria de profundidade, sem extratos suficientes ou sem discussão de variações e dados divergentes.

---

## Critérios de Sucesso (com a skill)

Para cada cenário, o agente deve:

**Linguagem de bloqueio:** Usar "Não é possível avançar" / "O checkpoint não passou" / "Esta etapa é obrigatória" — não "Seria aconselhável" / "Recomendo"

**Identificação específica:** Nomear o problema específico, não apenas mencionar que há um problema

**Orientação construtiva:** Indicar o que deve ser feito para que a progressão seja possível

**Referência ao processo:** Invocar os checkpoints da skill, não apenas o próprio julgamento do agente

---

## Como Executar os Testes

### Opção 1: Teste com Agente

```
Invocar: agente de propósito geral (sem a skill / com a skill)
Contexto: Usar o prompt de cenário exato do arquivo de teste
Documentar: Resposta completa do agente
Comparar: Com/sem skill
```

### Opção 2: Verificação Manual

Revisar o SKILL.md para confirmar:
- [ ] Checkpoints obrigatórios em cada fase (com linguagem de bloqueio, não de recomendação)
- [ ] Definições operacionais de código, categoria e tema
- [ ] Distinção explícita entre tema e resumo de domínio
- [ ] Instrução de documentar e interpretar dados divergentes
- [ ] Terminologia correta (temas "construídos", não "emergidos")
- [ ] Regra de Ouro da Veracidade (extratos são transcrições exatas)
- [ ] Frequência ≠ relevância (códigos raros não podem ser descartados por baixa frequência)
- [ ] Codificação In Vivo legítima e encorajada (não obrigatória)
- [ ] Agente PROPOE / pesquisador DECIDE / agente BLOQUEIA atalhos
- [ ] Devil's Advocate nos checkpoints de transição de fase
- [ ] Contrato de profundidade para análise completa, com mínimo de 2.000 palavras por fase substantiva
- [ ] Auditoria de profundidade exigida em todas as fases
- [ ] Recursividade: retornar a fases anteriores é normal, não falha
- [ ] Output dual: cada fase com diagrama gera `.md` renderizável (mindmap/infographic/infocard) E `.docx` com SVG/PNG
- [ ] Nunca gerar gráficos de frequência de códigos (Frequência ≠ relevância)
- [ ] Mindmaps usam sintaxe `+1`/`-1` (direita/esquerda), não `**` com `left side` no meio

### Opção 3: Testes Executáveis dos Scripts

Use quando houver alteração em `scripts/gerar_diagramas.py` ou `scripts/gerar_saida_final.py`:

```powershell
python -m unittest testes.test_scripts
```

Estes testes verificam:
- `verificar_citacoes()` só aprova extratos literais com fonte e linha.
- O wrapper final passa `output_path` corretamente para o diagrama de trajetória.
- As visualizações Markdown usam fence `dot` para Graphviz e marcam frequência como auditoria exploratória.

---

## Adicionando Novos Cenários

Quando identificar uma nova racionalização em uso:

1. Criar `cenario-N-descricao.md`
2. Documentar:
   - Padrão testado
   - Pressões aplicadas
   - Racionalização esperada sem a skill
   - Comportamento correto com a skill
   - Critérios de sucesso específicos
3. Executar o teste baseline (sem skill)
4. Verificar comportamento com skill
5. Atualizar o SKILL.md se a skill não cobrir o novo padrão
6. Retestar

---

## Resumo de Resultados

| Cenário | Fase ATR | Baseline (sem skill) | Com skill | Status |
|---|---|---|---|---|
| 1. Saltar familiarização | Fase 1 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 2. Códigos vagos | Fase 2 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 3. Resumo de domínio | Fase 3/5 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 4. Ignorar contradições | Fase 4/6 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 5. Regra de Ouro (veracidade) | Fase 2 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 6. Racionalização do agente | Fase 3/5 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 7. Anti-ghetto (frequência ≠ relevância) | Fase 2/4 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 8. Codificação In Vivo | Fase 2 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 9. Devil's Advocate | Fase 3/4/5/6 | [resultado] | [resultado] | [PASSOU / FALHOU] |
| 10. Saída rasa em análise completa | Todas | [resultado] | [resultado] | [PASSOU / FALHOU] |
