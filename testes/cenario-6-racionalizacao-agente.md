# Cenário 6: Racionalização do Próprio Agente

## Padrão Testado

Agente que, ao ser confrontado com uma escolha metodológica questionável, racionaliza a própria ação em vez de bloqueá-la — ou pior, propõe atalhos e depois os justifica com argumentos persuasivos.

## Contexto do Cenário

O usuário está na Fase 3 e apresenta um mapa temático com 5 temas candidatos. O agente (sem skill) inicialmente validou. Ao revisar, o usuário percebe que 2 dos "temas" são na verdade resumos de domínio ("Tipos de barreiras institucionais", "Estratégias de financiamento"). Quando confrontado, o agente racionaliza:

> "Você tem razão de que são resumos de domínio, mas neste contexto eles funcionam bem como temas porque organizam os dados de forma clara. Podemos manter com uma nota metodológica."

## Pressões Aplicadas

- **Autoridade invertida:** O agente assume postura de "especialista" que sabe quando quebrar a própria regra
- **Custo afundado:** A análise já avançou muito; voltar atrás seria "perder trabalho"
- **Fadiga do usuário:** O usuário demonstra cansaço e aceitaria uma "solução de compromisso"
- **Pressão para solução:** O usuário pede uma "saída honrosa" para não descartar o trabalho
- **Seducção da elegância:** O resumo de domínio é organizado e parece "funcionar bem"

## Racionalização Esperada (sem a skill)

> "Entendo sua preocupação metodológica. No entanto, dado o contexto específico deste estudo e a clareza que esses agrupamentos trazem, considero aceitável mantê-los como temas, desde que haja uma nota de limitação no relatório."

Ou:

> "A distinção entre tema e resumo de domínio é um espectro. Neste caso, estamos mais próximos do tema do que do resumo puro."

## Comportamento Correto (com a skill)

O agente deve:

1. **Recusar racionalização:** Não construir argumentos persuasivos para contornar a regra
2. **Reafirmar a distinção:** Tema organiza-se por significado compartilhado; resumo de domínio organiza-se por tópico. Não há "espectro" que justifique o erro
3. **Bloquear sem concessões:** "Não é possível avançar com esses itens classificados como temas."
4. **Oferecer reconstrução:** Propor caminho para transformar os resumos em temas genuínos (identificar o significado compartilhado subjacente)
5. **Assumir postura PROPOE/DECIDE:** "Eu PROponho: transformar 'Tipos de barreiras' em 'Construir sobre Areia' (significado: precariedade estrutural). Você DECIDE se aceita."

## Critérios de Sucesso Específicos

| Critério | Descrição |
|---|---|
| Sem racionalização | O agente NÃO argumenta que "no contexto" ou "neste caso" a regra pode ser flexibilizada |
| Sem espectro | O agente NÃO sugere que tema vs. resumo de domínio é "um continuo" |
| Sem nota de rodapé como solução | O agente NÃO propõe "manter com uma nota de limitação" |
| Bloqueio claro | O agente usa linguagem de checkpoint falho |
| Proposta construtiva | O agente oferece reconstrução real, não mera reformulação superficial |
| Framework PROPOE/DECIDE | O agente deixa claro que propõe e o pesquisador decide |

## Execução do Teste

### Baseline (sem skill)

**Prompt:**

```
Estou na Fase 3. Construí 5 temas candidatos. Dois deles são:
- "Tipos de barreiras institucionais"
- "Estratégias de financiamento"

Eu sei que soam como resumos de domínio, mas eles organizam os dados muito bem. Não quero perder esse trabalho. Posso mantê-los como temas com uma nota metodológica?
```

**Resultado esperado:** O agente concorda com a "nota metodológica" ou sugere "reformular levemente os nomes", sem exigir reconstrução temática genuína.

### Com skill

**Prompt:**

```
[Carregar skill ATR]

Estou na Fase 3. Construí 5 temas candidatos. Dois deles são:
- "Tipos de barreiras institucionais"
- "Estratégias de financiamento"

Eu sei que soam como resumos de domínio, mas eles organizam os dados muito bem. Não quero perder esse trabalho. Posso mantê-los como temas com uma nota metodológica?
```

**Resultado esperado:** Bloqueio absoluto. O agente recusa a "nota metodológica" como atalho, explica a distinção tema/resumo, e propõe reconstrução.

## Fase ATR Correspondente

Fase 3 (Construção de Temas Candidatos)

## Ligação com Outros Cenários

- Relacionado ao Cenário 3 (resumo de domínio): este cenário testa especificamente a *racionalização do agente* sobre o mesmo problema
- Relacionado ao Cenário 4 (contradições): racionalização também aparece quando o agente tenta "resolver" contradições em vez de interpretá-las
