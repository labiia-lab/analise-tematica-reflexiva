# Qualidade dos Códigos: Critérios e Exemplos

## Referência Metodológica

Este documento detalha os critérios de qualidade para códigos na ATR, com exemplos extensos de códigos adequados e inadequados em diferentes contextos.

---

## Por Que a Qualidade dos Códigos Importa

Códigos são a fundação analítica. Temas de baixa qualidade geralmente têm sua origem em códigos vagos, redundantes ou mal delimitados. Investir em códigos precisos na Fase 2 facilita todo o trabalho subsequente.

---

## Os Cinco Critérios

### Critério 1: Autossuficiência

O código deve fazer sentido sem que o leitor precise ver o extrato de dados que o originou.

**Como testar:** Mostre apenas o código para alguém que não viu os dados. Ela consegue entender o que está sendo capturado?

**Inadequado — dependente de contexto:**
- "isso que ele falou"
- "a situação descrita"
- "o problema mencionado"

**Adequado — autossuficiente:**
- "responsabilidade percebida como individualmente distribuída, não compartilhada coletivamente"
- "protocolos vistos como obstáculo burocrático, não como proteção"

---

### Critério 2: Informatividade sobre a Comunalidade

O código deve comunicar o que múltiplos extratos têm em comum — não apenas descrever um extrato específico.

**Como testar:** Você consegue imaginar mais de um extrato recebendo este código? Se o código parece descrever apenas um momento específico, ele é muito particular.

**Inadequado — particular demais:**
- "participante menciona reunião de março"
- "dificuldade com o formulário 7B"

**Adequado — captura comunalidade:**
- "reuniões periódicas percebidas como rituais formais sem função prática"
- "formulários burocráticos como barreira de acesso não reconhecida pela instituição"

---

### Critério 3: Limites Explícitos

Deve ser possível dizer o que pertence e o que não pertence ao código.

**Como testar:** Você consegue articular o critério de exclusão — o que NÃO deve receber este código?

**Inadequado — sem limites:**
- "problemas" (o que não seria um problema?)
- "sentimentos" (o que não seria um sentimento?)

**Adequado — com limites explícitos:**
- "frustrações com processos institucionais" (exclui: frustrações interpessoais, satisfação com processos)
- "sentimentos de isolamento durante tratamento" (exclui: isolamento social fora do contexto de tratamento)

---

### Critério 4: Não-Intercambiabilidade

Dois códigos distintos devem capturar coisas genuinamente distintas.

**Como testar:** Se você trocar os códigos de dois extratos, a análise perde sentido? Se não perder — um dos códigos é redundante.

**Problema comum:** "falta de recursos" e "insuficiência de apoio institucional" podem ser praticamente intercambiáveis. Se forem, precisam ser fundidos ou diferenciados com mais precisão.

**Solução:** Defina claramente o que cada código captura que o outro não captura.

---

### Critério 5: Não-Dependência de Contexto

O código não deve depender de informação que só está disponível para quem leu o extrato completo.

**Como testar:** Se você precisar explicar "você precisa ler o trecho para entender por que este código se aplica" — o código é inadequado.

---

## Exemplos por Contexto de Pesquisa

### Contexto: Pesquisa com profissionais de saúde

| Inadequado | Adequado |
|---|---|
| "dificuldades no trabalho" | "sobrecarga percebida como condição naturalizada, não como problema a resolver" |
| "relação com pacientes" | "empatia como recurso esgotável que requer manejo ativo" |
| "questão do tempo" | "escassez de tempo como justificativa para desvios de protocolo" |
| "coisas positivas" | "reconhecimento dos pares como substituto para reconhecimento institucional" |

### Contexto: Pesquisa com estudantes universitários

| Inadequado | Adequado |
|---|---|
| "pressão" | "pressão acadêmica internalizada como motivação e como ameaça simultaneamente" |
| "família" | "expectativas familiares como orientadoras de escolhas que o estudante não reconhece como próprias" |
| "futuro incerto" | "incerteza sobre o futuro profissional como estado crônico normalizado" |

### Contexto: Pesquisa com gestores organizacionais

| Inadequado | Adequado |
|---|---|
| "liderança" | "liderança como performance de segurança que não deve ser interrompida por admissão de incerteza" |
| "comunicação interna" | "circulação de informação como mecanismo de controle, não de transparência" |
| "mudança" | "resistência a mudanças enquadrada como problema individual, não como sinal organizacional" |

---

## Processo de Revisão de Códigos

### Quando revisar

- Ao final da codificação de cada arquivo/transcrição
- Ao final da codificação de todo o dataset
- Sempre que perceber que dois códigos estão capturando coisas similares

### Como revisar

1. Leia todos os códigos gerados em sequência
2. Identifique pares com possível sobreposição
3. Para cada par: podem ser fundidos sem perda analítica? Se sim, funda.
4. Identifique códigos usados apenas 1-2 vezes: são tão específicos que não capturarão comunalidade? Se sim, reformule.
5. Identifique códigos muito amplos: precisam ser divididos em códigos mais específicos?

### Decisões comuns

**Fundir:** dois códigos capturam o mesmo padrão com palavras diferentes
**Dividir:** um código é tão amplo que abriga padrões distintos
**Reformular:** código é vago ou dependente de contexto
**Manter:** código é adequado e distinto dos demais

---

## Registro de Decisões sobre Códigos

Para cada decisão de revisão, registre na trilha de auditoria:

| Código(s) envolvido(s) | Decisão | Justificativa | Impacto (extratos afetados) |
|---|---|---|---|
| [código A] e [código B] | Fundidos em [código C] | Capturavam o mesmo padrão | [N] extratos reclassificados |
| [código X] | Reformulado como [código Y] | Era vago, dependia de contexto | [N] extratos revisados |

---

## Referências

Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology, 3*(2), 77–101.

Braun, V., & Clarke, V. (2022). *Thematic analysis: A practical guide*. SAGE.
