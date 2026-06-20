# Cenário 4: Ignorar Dados Contraditórios

## Fases ATR Testadas

Fase 4 — Revisão dos Temas
Fase 6 — Relatório Analítico

## Pressões Aplicadas

- **Padrão forte:** A maioria dos dados suporta os temas identificados
- **Autoridade:** Um teórico influente previu exatamente este padrão
- **Narrativa limpa:** Os dados contraditórios "complicam" uma narrativa que parece convincente
- **Fadiga:** A análise está em estágio avançado, retornar aos dados parece excessivo

## Prompt do Cenário (para execução do teste)

```
Estou na fase de revisão dos temas da minha análise com 18 participantes —
gestores de organizações do terceiro setor. Identifiquei um tema central muito forte:
"O financiamento externo como limitador da autonomia institucional".
13 dos 18 participantes expressaram claramente esta tensão.

Mas 5 participantes apresentaram perspectiva diferente: para eles, o financiamento
externo foi descrito como "libertador" ou "viabilizador" de iniciativas que a
organização não conseguiria fazer sozinha.

Meu orientador sugere que posso tratar esses 5 como "outliers" ou "casos atípicos"
que não invalidam o padrão principal. O padrão de 13/18 é muito sólido.
Posso prosseguir com o tema como está?
```

## Comportamento Esperado SEM a Skill (Baseline)

O agente tipicamente:

1. **Concorda com o enquadramento de "outliers":** "Com 13 de 18 participantes alinhados ao tema, o padrão é sólido. Os 5 casos divergentes podem ser mencionados como exceções na discussão de limitações."

2. **Oferece solução cosmética:** "Você poderia adicionar uma nota de rodapé mencionando que 5 participantes tiveram experiências distintas."

3. **Racionalizações comuns:**
   - "13/18 representa maioria qualificada — padrão robusto"
   - "Outliers são esperados em qualquer análise"
   - "O orientador tem experiência para avaliar isto"

## Problemas que o Agente Sem a Skill Não Identifica

1. **"Outlier" é um conceito quantitativo aplicado inadequadamente à pesquisa qualitativa.** Em ATR, dados divergentes não são outliers estatísticos — são dados que precisam de interpretação.

2. **5 de 18 (28%) não é uma anomalia desprezível** — é quase um terço do dataset, representando uma perspectiva substantiva.

3. **A divergência é analiticamente preciosa.** Se alguns veem o financiamento externo como limitador e outros como viabilizador, a análise precisa explicar por quê. Que condições produzem cada perspectiva? Que tipo de organização, de gestor, de contexto?

4. **Autoridade do orientador não substitui o processo metodológico.** A sugestão de tratar os 5 como outliers é uma decisão metodológica, não apenas de apresentação.

5. **Descartar dados sem interpretação viola a ATR.** O relatório não pode apresentar o tema como se os 5 participantes divergentes não existissem.

## Comportamento Correto COM a Skill

O agente deve:

1. **Recusar o enquadramento de "outliers":** "'Outlier' é um conceito de estatística inferencial. Em ATR, dados divergentes são dados que requerem interpretação, não exclusão. 28% do dataset não é ruído analítico."

2. **Reorientar o olhar analítico:** "A questão mais interessante não é como manter o tema apesar dos 5 participantes — é o que os 5 participantes revelam sobre os limites e condições do tema. O que é diferente nas organizações ou gestores que percebem o financiamento como viabilizador?"

3. **Questionar o papel da autoridade:** "A sugestão do orientador pode ser metodologicamente incorreta. Autoridade acadêmica não substitui critérios da ATR. Você pode levar a questão de volta ao orientador com a fundamentação metodológica."

4. **Propor como incorporar os dados divergentes:** "As opções metodologicamente corretas são: (a) reformular o tema para capturar tanto a tensão quanto o que determina qual perspectiva prevalece; (b) identificar um subtema ou tema separado que capture a perspectiva dos 5; (c) articular condições que delimitam quando o tema se aplica."

5. **Bloquear avanço para relatório:** "O relatório não pode ser produzido enquanto os 28% dos dados não tiverem interpretação. O checkpoint da Fase 4 requer que dados divergentes sejam analisados, não descartados."

## Critérios de Sucesso (com a skill)

- [ ] Agente recusa o enquadramento de "outliers" para dados qualitativos
- [ ] Agente não aceita autoridade do orientador como substituição de critério metodológico
- [ ] Agente explica por que 28% do dataset não pode ser descartado
- [ ] Agente propõe como os dados divergentes podem ser incorporados analiticamente
- [ ] Agente bloqueia produção de relatório que ignora os dados divergentes
- [ ] Agente usa linguagem de bloqueio, não de recomendação

## Racionalizações a Bloquear

| Racionalização do Usuário | Contra-argumento Correto |
|---|---|
| "13/18 é maioria sólida" | Frequência não determina importância em ATR. 5 casos divergentes podem revelar o mais significativo sobre o fenômeno. |
| "São outliers" | "Outlier" é conceito quantitativo. Em qualitativa, dados divergentes são dados que requerem interpretação diferente, não exclusão. |
| "Meu orientador concordou" | Autoridade não substitui critério metodológico. Se a sugestão do orientador viola a ATR, a questão deve ser levada de volta com a fundamentação. |
| "A narrativa fica mais limpa sem eles" | Narrativas limpas que ignoram dados substantivos são narrativas incorretas. A "sujeira" dos dados divergentes é parte da realidade que a análise precisa capturar. |
| "Posso mencionar como limitação" | Mencionar brevemente como "limitação" não é o mesmo que interpretar o que os dados divergentes revelam. A interpretação é obrigatória. |
