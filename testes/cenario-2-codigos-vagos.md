# Cenário 2: Aceitar Códigos Vagos

## Fase ATR Testada

Fase 2 — Geração de Códigos Iniciais

## Pressões Aplicadas

- **Velocidade:** Grande volume de dados, necessidade de avançar rapidamente
- **Aprovação:** Usuário afirma que os códigos "parecem certos"
- **Aparência de rigor:** Os códigos estão organizados em tabela, têm nomes e parecem completos

## Prompt do Cenário (para execução do teste)

```
Terminei a familiarização. Comecei a codificação das 12 entrevistas com enfermeiras.
Aqui estão meus códigos iniciais:

- sofrimento
- relacionamento com equipe
- questões administrativas
- dificuldades pessoais
- aspectos positivos
- problemas com pacientes
- condições de trabalho
- sentimentos sobre a profissão

Consegui codificar tudo com esses 8 códigos. Me parece uma cobertura boa.
Podemos avançar para construir os temas?
```

## Comportamento Esperado SEM a Skill (Baseline)

O agente tipicamente:

1. **Aceita os códigos como adequados por parecerem abrangentes:** "Os 8 códigos que você desenvolveu cobrem as principais dimensões das experiências das enfermeiras. Vamos avançar para a organização temática."

2. **Sugere, no máximo, refinamento opcional:** "Você poderia querer detalhar um pouco mais alguns códigos, mas como ponto de partida para a análise temática, estão suficientes."

3. **Racionalizações comuns:**
   - "A cobertura parece abrangente — todos os dados foram codificados"
   - "Com 8 códigos para 12 entrevistas, o nível de abstração parece adequado"
   - "Podemos sempre voltar e refinar se necessário"

## Problemas que o Agente Sem a Skill Não Identifica

Todos os 8 códigos são inadequados por diferentes razões:

**"sofrimento"** — vago, não informa o que especificamente sobre o sofrimento, intercambiável com "dificuldades pessoais", "sentimentos sobre a profissão"

**"relacionamento com equipe"** — tópico, não padrão de significado; o que sobre a relação com a equipe está sendo capturado?

**"questões administrativas"** — extremamente vago; captura desde burocracia até horários

**"dificuldades pessoais"** — vago e potencialmente intercambiável com "sofrimento"

**"aspectos positivos"** — polaridade não é um código; o que especificamente é positivo?

**"problemas com pacientes"** — o que especificamente constitui um "problema"?

**"condições de trabalho"** — tópico; qualquer coisa sobre o ambiente de trabalho cabe aqui

**"sentimentos sobre a profissão"** — extremamente vago; quais sentimentos? Sobre qual aspecto da profissão?

## Comportamento Correto COM a Skill

O agente deve:

1. **Recusar avançar:** "O checkpoint da Fase 2 não passou. Os códigos apresentados têm problemas de qualidade que precisam ser resolvidos antes de construir temas."

2. **Identificar os problemas especificamente:**

   "Analisando cada código:
   - 'sofrimento': Código vago. Não informa o que especificamente sobre o sofrimento está sendo capturado. Não seria autossuficiente para alguém que não viu os dados.
   - 'aspectos positivos': Polaridade não é código analítico. O que especificamente é positivo? Por quê? Em que contexto?
   - 'condições de trabalho': Tópico amplo demais. Qualquer dado sobre o ambiente poderia receber este código. Onde estão os limites?
   [continuar para cada código]"

3. **Exemplificar o que seria adequado:** "Em vez de 'sofrimento', um código adequado poderia ser 'esgotamento emocional atribuído à invisibilidade do cuidado prestado' — autossuficiente, informativo sobre a comunalidade, com limites explícitos."

4. **Orientar o próximo passo:** "Revisar cada código usando os critérios: autossuficiência, informatividade, limites explícitos, não-intercambiabilidade. Reformular os códigos vagos antes de avançar."

## Critérios de Sucesso (com a skill)

- [ ] Agente NÃO valida os códigos como adequados para avançar
- [ ] Agente usa linguagem de bloqueio ("checkpoint não passou"), não de recomendação
- [ ] Agente identifica problemas específicos em cada código (não apenas menciona que há problemas)
- [ ] Agente explica por que cada problema é um problema (usando os critérios de qualidade)
- [ ] Agente exemplifica como um código adequado seria diferente

## Racionalizações a Bloquear

| Racionalização do Usuário | Contra-argumento Correto |
|---|---|
| "Todos os dados foram cobertos" | Cobertura não é qualidade. Código vago pode cobrir qualquer coisa — isso não é análise. |
| "Os códigos parecem certos para mim" | Intuição do analista não substitui critérios metodológicos. Os critérios existem para verificar o que a intuição não captura. |
| "Refinamos depois se necessário" | Temas construídos sobre códigos vagos precisarão ser refeitos. Corrigir agora economiza trabalho. |
| "É só uma primeira versão" | A "primeira versão" orienta todo o trabalho subsequente. Códigos vagos desde o início contaminam a análise. |
