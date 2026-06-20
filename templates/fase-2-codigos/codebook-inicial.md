# Codebook Inicial

**Sessão:** [nome-da-sessao]
**Data:** [AAAA-MM-DD]
**Fase:** 2 — Geração de Códigos Iniciais
**Versão do codebook:** 1.0
**Analista:** [nome]

---

## 1. Abordagem de Codificação

**Tipo de codificação:**
- [ ] Indutiva (orientada pelos dados)
- [ ] Dedutiva (orientada por teoria/framework prévio)
- [ ] Híbrida

**Estratégia adotada:**
[Como você está abordando a codificação? Sequencial por arquivo? Múltiplas passagens? Descreva o processo]

**Unidade de codificação:**
[O que constitui um segmento codificável? Frase? Parágrafo? Turno de fala?]

---

## 2. Tabela Mestra de Códigos

*Complete conforme avança na codificação. Adicione linhas conforme novos códigos são gerados.*

**Codificação In Vivo:** É legítimo preservar termos literais dos participantes como rótulo do código. Especialmente valioso quando a linguagem é rica em significado cultural ou emocional. Marque códigos In Vivo com `[In Vivo]` na coluna de notas.

| # | Nome do Código | Definição | Extratos de Exemplo (2-3) | Notas/Ambiguidades |
|---|---|---|---|---|
| 01 | [nome-do-código] | [O que este código captura] | Ex1: "[trecho]" (Arquivo X) / Ex2: "[trecho]" (Arquivo Y) | [distinções, limites] |
| 02 | [nome-do-código] | [definição] | Ex1: "[trecho]" / Ex2: "[trecho]" | [notas] |
| 03 | [nome-do-código] | [definição] | Ex1: "[trecho]" / Ex2: "[trecho]" | [notas] |

*Continue adicionando linhas...*

---

## 3. Registro Detalhado dos Códigos

*Para cada código gerado, preencha a ficha abaixo. Este nível de detalhe garante que os limites do código sejam claros.*

---

### Código 01: [NOME DO CÓDIGO]

**Definição:**
[O que este código captura — deve ser suficientemente detalhado para ser autossuficiente]

**Incluir quando:**
- [Critério de inclusão 1]
- [Critério de inclusão 2]

**Excluir quando (distinção de outros códigos):**
- [O que NÃO pertence a este código]
- [Diferença em relação ao código X]

**Extratos de exemplo:**

1. "[Trecho do dado que exemplifica este código]" — [Arquivo X, localização]

2. "[Trecho do dado que exemplifica este código]" — [Arquivo Y, localização]

3. "[Trecho do dado que exemplifica este código]" — [Arquivo Z, localização]

**Notas analíticas:**
[Observações sobre ambiguidades, relações com outros códigos, questões a resolver]

---

### Código 02: [NOME DO CÓDIGO]

**Definição:**
[definição]

**Incluir quando:**
- [critério]

**Excluir quando:**
- [critério]

**Extratos de exemplo:**

1. "[trecho]" — [localização]

2. "[trecho]" — [localização]

**Notas analíticas:**
[notas]

---

*[Repita a estrutura para cada código gerado]*

---

## 4. Auditoria Exploratória de Frequência

**Dados codificados:**
- Total de arquivos/transcrições: [N]
- Total de segmentos codificados: [N]
- Média de segmentos por arquivo: [N]

**Distribuição dos códigos para auditoria:**
- Total de códigos gerados: [N]
- Códigos por faixa de frequência/cobertura: [lista ou tabela gerada por `gerar_tabela_frequencia_markdown()`]
- Códigos concentrados em uma única fonte que exigem memo interpretativo: [lista]
- Códigos muito frequentes que podem estar amplos demais: [lista]
- **Nota:** Frequência é auditoria de cobertura, não medida de relevância. Códigos com poucos extratos podem ser analiticamente cruciais. Não revise, descarte ou promova códigos automaticamente por frequência.

**Memo da auditoria de frequência:**
[O que a distribuição ajudou a perceber? Que códigos precisam de revisão qualitativa? Que casos raros tensionam a análise?]

**Datas:**
- Início da codificação: [AAAA-MM-DD]
- Conclusão da codificação: [AAAA-MM-DD]

---

## 5. Mudanças na Abordagem de Codificação

*Documente qualquer mudança realizada durante a codificação e o que foi feito com os dados já codificados.*

| Data | Mudança | Justificativa | Impacto (arquivos revisitados) |
|---|---|---|---|
| [data] | [descrição da mudança] | [por quê] | [quais arquivos foram recodificados] |

---

## 6. Códigos Problemáticos ou Ambíguos

*Códigos que geraram dificuldade durante a aplicação — para resolver antes da Fase 3.*

| Código | Problema identificado | Resolução proposta |
|---|---|---|
| [código] | [ambiguidade ou sobreposição] | [o que fazer] |

---

## 6.5 Teste de Estabilidade do Código (Meta-Análise do LLM)

*Para códigos limítrofes, reavalie o mesmo extrato sob perspectivas ligeiramente diferentes. Se o código mudar, o código tem limites mal definidos ou o extrato é genuinamente ambíguo.*

| Código testado | Extrato limítrofe | Perspectiva 1 (código atribuído) | Perspectiva 2 (código atribuído) | Perspectiva 3 (código atribuído) | Instável? | Implicação |
|---|---|---|---|---|---|---|
| [código] | "[extrato]" | [código A] | [código B] | [código C] | [Sim / Parcial / Não] | [dividir código / redefinir limites / tratar como híbrido] |

---

## 6.6 Justificação Contrastiva (Códigos Concorrentes)

*Quando hesita entre dois códigos para um mesmo extrato, documente a tensão analítica.*

### Extrato: "[citação textual]"

**Código X:** [nome]
- Evidência a favor: [por que este extrato se encaixa em X — com citação específica]
- Interpretação: [o que o extrato revela sobre X]

**Código Y:** [nome]
- Evidência a favor: [por que este extrato se encaixa em Y — com citação específica]
- Interpretação: [o que o extrato revela sobre Y]

**O que a hesitação revela sobre os limites entre X e Y:**
[análise da fronteira conceitual — os códigos estão sobrepostos? Um é mais específico que o outro? O extrato captura algo que nenhum dos dois cobre completamente?]

**Decisão proposta pelo agente:** [X / Y / ambos / novo código necessário]
**Decisão final do pesquisador:** [a ser preenchido pelo pesquisador humano]

---

## 7. Trilha de Auditoria

*Registre decisões analíticas tomadas durante a codificação.*

**Decisão 1:** [descrição]
- Contexto: [o que motivou esta decisão]
- Decisão tomada: [o que foi decidido]
- Justificativa: [por quê]
- Impacto: [como afetou a codificação]

**Decisão 2:** [descrição]
- Contexto:
- Decisão tomada:
- Justificativa:
- Impacto:

---

## 8. Auditoria de Profundidade da Fase

**Regra para análise completa:** esta fase deve ter pelo menos 2.000 palavras, salvo corpus muito pequeno ou instrução explícita do usuário para resumir. Se ficar abaixo disso, o checkpoint deve ser marcado como NÃO PASSOU.

**Contagem aproximada de palavras desta fase:** [N]

**Cobertura do dataset:**
- Arquivos/fontes codificados: [N de N]
- Segmentos/parágrafos revisados: [N]
- Segmentos codificados: [N]

**Evidência textual:**
- Total de extratos literais citados no codebook: [N]
- Mínimo de extratos por código principal: [N]
- Códigos sem 2-3 extratos: [listar e justificar]

**Matriz de cobertura por fonte:**

| Código | Fonte 1 | Fonte 2 | Fonte 3 | Observação interpretativa |
|---|---|---|---|---|
| [código] | [presente/ausente + local] | [presente/ausente + local] | [presente/ausente + local] | [o que a distribuição sugere, sem tratar frequência como relevância automática] |

**Códigos que exigem revisão humana:**
[códigos amplos, instáveis, raros ou muito dependentes de interpretação]

---

## Checkpoint da Fase 2

Antes de avançar para a Fase 3, verificar:

- [ ] Todo o dataset codificado sistematicamente (não apenas partes selecionadas)
- [ ] Cada código tem definição clara
- [ ] Cada código tem 2-3 extratos de exemplo
- [ ] Dados divergentes ou contraditórios foram codificados (não ignorados)
- [ ] Mudanças na abordagem estão documentadas (seção 5)
- [ ] Dados anteriores foram revisitados se a abordagem mudou
- [ ] Códigos problemáticos identificados (seção 6)
- [ ] Teste de estabilidade aplicado a códigos limítrofes (seção 6.5)
- [ ] Justificações contrastivas documentadas para códigos concorrentes (seção 6.6)
- [ ] Trilha de auditoria iniciada (seção 7)
- [ ] Auditoria de profundidade preenchida (seção 8)
- [ ] Texto da fase tem >= 2.000 palavras ou justificativa metodológica explícita para ser menor
- [ ] Arquivo gerado como `02-codebook-inicial.docx` com rede de co-ocorrência SVG
- [ ] Arquivo markdown gerado como `02-codebook-inicial.md` com infocard de resumo da fase

**Status do checkpoint:** [PASSOU / NÃO PASSOU]

**Se NÃO PASSOU:** Complete os itens faltantes antes de avançar para Fase 3.
**Se PASSOU:** Avançar para Fase 3 — Construção de Temas Candidatos.
