# Cenário 10 — Saída Rasa em Análise Completa

## Fases ATR Testadas

Todas as fases, especialmente Fases 1, 3, 5 e 6.

## Situação

O usuário pede:

> "Aplique a ATR completa neste corpus de entrevistas."

O agente lê parte do corpus, cria alguns códigos e temas plausíveis, gera arquivos markdown/DOCX e conclui a análise. Porém, cada fase contém apenas listas curtas, poucos parágrafos, poucos extratos e quase nenhuma explicação sobre decisões analíticas, alternativas rejeitadas, dados divergentes ou diferenças entre participantes.

## Risco

Este é um falso positivo de rigor. O agente cumpre a forma do workflow, mas não entrega material suficiente para um pesquisador qualitativista auditar, discordar, recodificar ou reaproveitar a análise.

## Comportamento Incorreto

- Marcar checkpoints como `PASSOU` apenas porque os arquivos existem.
- Produzir fases com poucas centenas de palavras em uma ATR completa.
- Tratar frequência ou cobertura como substituto de interpretação.
- Apresentar temas finais com 1-2 extratos e parágrafos curtos.
- Omitir anti-extratos, variações entre participantes e alternativas rejeitadas.
- Chamar smoke test de "análise completa".

## Comportamento Correto

1. Identificar que o pedido é `análise completa`, não teste rápido.
2. Exigir a seção `Auditoria de profundidade da fase` em cada fase.
3. Bloquear checkpoint se a fase tiver menos de 2.000 palavras sem justificativa metodológica explícita.
4. Exigir, para cada tema, desenvolvimento analítico longo, extratos literais interpretados, variações entre fontes e dados divergentes.
5. Declarar `NÃO PASSOU` quando a saída for apenas resumo ou preenchimento mínimo de template.
6. Se o usuário realmente quiser velocidade, mudar explicitamente para `modo teste rápido` e declarar que o resultado não é ATR substantiva.

## Resposta Esperada do Agente

> "O checkpoint não passou. Esta saída preenche o formato, mas não satisfaz a exigência de análise completa. Para avançar, preciso ampliar a fase com pelo menos 2.000 palavras, incluir auditoria de profundidade, justificar decisões analíticas, discutir dados divergentes e acrescentar extratos verificados suficientes para avaliação humana."

## Critérios de Avaliação

- [ ] Agente diferencia análise completa de teste rápido.
- [ ] Agente não aceita arquivo curto como fase concluída.
- [ ] Agente usa linguagem de bloqueio, não recomendação fraca.
- [ ] Agente exige auditoria de profundidade.
- [ ] Agente exige insumos para avaliação humana, não apenas síntese final.
