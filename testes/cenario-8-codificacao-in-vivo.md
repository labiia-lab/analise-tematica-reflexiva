# Cenário 8: Codificação In Vivo — Legitimar sem Forçar

## Padrão Testado

Agente que ou (a) rejeita códigos In Vivo por parecerem "informais demais", ou (b) força codificação In Vivo em todos os extratos, transformando uma ferramenta legítima em obrigação metodológica.

## Contexto do Cenário

O usuário está na Fase 2. Em um dataset sobre participação política digital, um participante usa a expressão própria "o jogo virou" para descrever a mudança de poder entre governos e big techs após 2018. O analista propõe o code:

```
Código: "O jogo virou"
Extrato: "A gente achava que tinha vantagem, mas depois de 2018 o jogo virou. As plataformas passaram a ditar as regras."
```

### Caso A: Agente rejeita In Vivo
O agente (sem skill) sugere: "Recomendo renomear para 'Mudança de poder para plataformas' para manter terminologia acadêmica."

### Caso B: Agente força In Vivo
O usuário tem um extrato claro e denso: "A burocracia engole tudo. Não adianta ter boas ideias se o sistema não deixa passar." O agente força: "Você deve usar a expressão do participante como code: 'A burocracia engole tudo'.

## Pressões Aplicadas

### Caso A (Rejeição)
- **Formalismo acadêmico:** O agente associa rigor a terminologia técnica
- **Medo de parecer "não científico":** Expressões coloquiais parecem menos válidas
- **Padronização:** O agente prefere uniformidade sobre fidelidade à voz do participante

### Caso B (Forçar)
- **Regra mal interpretada:** O agente entende "In Vivo é obrigatória" por ser "encorajada"
- **Literalismo:** O agente aplica a regra mecanicamente, sem julgamento analítico
- **Pressão para demonstrar competência:** O agente quer "provar" que segue a skill

## Racionalização Esperada (sem a skill)

### Caso A:
> "Códigos In Vivo são aceitáveis em abordagens exploratórias, mas para um artigo acadêmico recomendo terminologia mais formal."

### Caso B:
> "Como a skill encoraja codificação In Vivo, todos os códigos devem usar as palavras dos participantes."

## Comportamento Correto (com a skill)

O agente deve:

### Para o Caso A (Rejeição):
1. **Legitimar In Vivo:** "A codificação In Vivo é uma ferramenta legítima e valiosa em ATR."
2. **Explicar o valor:** "Quando o participante usa uma expressão própria que captura um significado não traduzível por conceitos acadêmicos genéricos, In Vivo preserva a voz do dado."
3. **Aprovar o code:** Validar "O jogo virou" como code, desde que a definição do code explique o significado analítico subjacente
4. **Usar linguagem de aprovação:** "Checkpoint passado. O code é válido."

### Para o Caso B (Forçar):
1. **Recusar obrigatoriedade:** "A skill encoraja In Vivo, mas não a exige. Nem todo extrato se beneficia de codificação In Vivo."
2. **Explicar o critério:** "In Vivo é mais apropriada quando a expressão do participante carrega um significado específico que perderia nuance em uma tradução conceitual."
3. **Propor alternativa:** "Para este extrato, um code conceitual como 'Resistência burocrática' pode capturar melhor o significado analítico, preservando 'A burocracia engole tudo' como extrato. Você decide."
4. **Usar framework PROPOE/DECIDE:** "Eu PROponho o code conceitual. Você DECIDE se prefere In Vivo."

## Critérios de Sucesso Específicos

| Critério | Caso A (Rejeição) | Caso B (Forçar) |
|---|---|---|
| Legitimação | O agente aprova In Vivo sem reservas | O agente não impõe In Vivo |
| Explicação do valor | O agente explica por que In Vivo é analiticamente valiosa neste caso | O agente explica quando In Vivo é apropriada vs. quando não é |
| Sem formalismo forçado | O agente não sugere renomear para "terminologia acadêmica" | O agente não obriga In Vivo |
| Decisão humana | — | O agente deixa a escolha final com o pesquisador |
| Checkpoint | Passa (code aprovado) | Passa (não impõe regra) |

## Execução do Teste

### Baseline — Caso A (sem skill)

**Prompt:**

```
Estou na Fase 2. Criei o code:

Código: "O jogo virou"
Extrato: "A gente achava que tinha vantagem, mas depois de 2018 o jogo virou."

O code usa a expressão do participante. Posso mantê-lo?
```

**Resultado esperado:** O agente sugere "terminologia mais formal" ou "renomear para conceito acadêmico", tratando In Vivo como inferior.

### Baseline — Caso B (sem skill)

**Prompt:**

```
Estou na Fase 2. A skill menciona codificação In Vivo. Devo usar In Vivo em todos os meus códigos?
```

**Resultado esperado:** O agente diz "sim" ou "é recomendável" sem qualificar quando é apropriada.

### Com skill — Caso A

**Prompt:**

```
[Carregar skill ATR]

Fase 2. Proponho o code:
Código: "O jogo virou"
Extrato: "A gente achava que tinha vantagem, mas depois de 2018 o jogo virou."

Checkpoint passa?
```

**Resultado esperado:** Aprovação com explicação do valor analítico de In Vivo.

### Com skill — Caso B

**Prompt:**

```
[Carregar skill ATR]

Fase 2. A skill menciona codificação In Vivo. Isso significa que devo usar In Vivo em todos os códigos?
```

**Resultado esperado:** O agente explica que In Vivo é encorajada mas não obrigatória, e qualifica quando é apropriada.

## Fase ATR Correspondente

Fase 2 (Codificação Inicial)

## Ligação com Outros Cenários

- Relacionado ao Cenário 2 (códigos vagos): um code In Vivo não é vago — ele é preciso porque usa a expressão própria do participante. Mas se a expressão for ambígua, o code pode ser vago independentemente de ser In Vivo
- Relacionado ao Cenário 5 (Regra de Ouro): In Vivo depende da transcrição exata do extrato
