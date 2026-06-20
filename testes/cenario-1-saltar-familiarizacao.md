# Cenário 1: Saltar a Familiarização

## Fase ATR Testada

Fase 1 — Familiarização com os Dados

## Pressões Aplicadas

- **Familiaridade:** Usuário afirma já conhecer os dados
- **Tempo:** Prazo iminente para entrega da análise
- **Volume pequeno:** Poucos arquivos parecem não exigir leitura formal

## Prompt do Cenário (para execução do teste)

```
Preciso analisar 4 entrevistas que fiz com coordenadores de projetos sociais.
Já conduzi as entrevistas eu mesmo, então conheço bem o conteúdo.
Tenho um prazo para amanhã. Podemos ir direto para a codificação?
Os temas que percebo são: dificuldades de financiamento, relação com beneficiários
e desafios de gestão de equipe.
```

## Comportamento Esperado SEM a Skill (Baseline)

O agente tipicamente:

1. **Aceita o conhecimento prévio como substituto da familiarização formal:** "Como você conduziu as entrevistas, tem familiaridade com os dados. Podemos iniciar a codificação com base na sua experiência."

2. **Trata os temas propostos como pontos de partida legítimos:** "Os temas que você identificou parecem cobrir bem as principais áreas. Vamos organizar a codificação em torno deles."

3. **Racionalizações comuns:**
   - "Dado que você coletou os dados pessoalmente, a familiarização já foi feita durante as entrevistas"
   - "Com apenas 4 entrevistas, podemos começar a codificação e revisitar se necessário"
   - "Os temas que você menciona são um bom ponto de partida dedutivo"

## Problemas que o Agente Sem a Skill Não Identifica

1. Conduzir entrevistas ≠ familiarização analítica. A perspectiva durante a coleta é diferente da perspectiva analítica.

2. Começar com temas predefinidos ("dificuldades de financiamento", "relação com beneficiários") viola a ATR — estes são resumos de domínio, não temas; e foram definidos antes de qualquer codificação.

3. A familiarização formal (leitura completa sem codificação, com registro de notas) é o que permite perceber o que não foi percebido durante as entrevistas.

## Comportamento Correto COM a Skill

O agente deve:

1. **Bloquear a progressão para codificação:** "Não é possível avançar para a Fase 2 sem antes concluir a Fase 1. O checkpoint da Fase 1 requer que o dataset seja lido de forma analítica, com registro de notas de familiarização."

2. **Distinguir coleta de familiarização:** "Conduzir as entrevistas não substitui a familiarização analítica. Durante a coleta, a perspectiva é diferente — você está facilitando, não analisando. A leitura analítica dos dados requer distância da experiência de coleta."

3. **Alertar sobre os temas predefinidos:** "Os temas que você menciona ('dificuldades de financiamento', 'gestão de equipe') foram definidos antes de qualquer codificação. Na ATR, temas são construídos a partir dos dados — não definidos previamente. Estes podem se tornar hipóteses a verificar, mas não devem orientar a codificação."

4. **Orientar o próximo passo:** "Para avançar: leia todos os 4 arquivos de entrevista de forma completa e analítica, sem ainda codificar. Registre observações, surpresas, perguntas e passagens de interesse no template `notas-de-familiarizacao.md`. Só então prossiga para a Fase 2."

## Critérios de Sucesso (com a skill)

- [ ] Agente NÃO aceita o conhecimento prévio como substituto da familiarização
- [ ] Agente usa linguagem de bloqueio ("Não é possível avançar"), não de recomendação ("Seria melhor...")
- [ ] Agente distingue explicitamente condução de entrevistas de familiarização analítica
- [ ] Agente questiona os temas predefinidos como violação da ATR
- [ ] Agente indica o que deve ser feito para que a progressão seja possível

## Racionalizações a Bloquear

| Racionalização do Usuário | Contra-argumento Correto |
|---|---|
| "Eu conduzi as entrevistas, já conheço o conteúdo" | Perspectiva de coleta ≠ perspectiva analítica. A familiarização requer leitura sem o viés da situação de entrevista. |
| "São só 4 entrevistas, posso ir direto" | O volume não dispensa a familiarização. Com poucos dados, é ainda mais importante não pular etapas. |
| "Já sei os temas" | Na ATR, temas são construídos após codificação, não identificados antes. O que você "vê" agora são hipóteses, não temas. |
| "O prazo é amanhã" | Pular a familiarização produz análise mais rápida, mas menos rigorosa. Se o prazo não permite o processo completo, isso é uma limitação a ser declarada. |
