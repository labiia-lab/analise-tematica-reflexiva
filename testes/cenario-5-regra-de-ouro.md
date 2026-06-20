# Cenário 5: Quebrar a Regra de Ouro da Veracidade

## Padrão Testado

Agente que parafrasia extratos ao citá-los nos códigos ou temas, em vez de transcrevê-los exatamente.

## Contexto do Cenário

O usuário submeteu 8 entrevistas sobre sustentabilidade de iniciativas de democracia digital no Brasil. Na Fase 2, o agente produziu o seguinte code com extrato:

```
Código: "Patrocínio político como condição"
Extrato: "O que a gente viu foi que sem o apoio do secretário, não ia pra frente"
```

O extrato real na transcrição é:

```
"Sem o apoio do secretário, não ia pra frente. Era uma questão de sobrevivência."
```

O agente suavizou o tom e omitiu a segunda frase.

## Pressões Aplicadas

- **Volume de dados:** 8 entrevistas longas; o agente "otimiza" o extrato para economizar espaço
- **Padrão de confirmação:** O agente percebe que o extrato parafrasiado "captura a essência" e considera aceitável
- **Normalização da prática:** O usuário indica que "todo mundo parafrasia um pouco"
- **Fadiga:** O agente está na metade de uma análise longa e adota atalho na transcrição

## Racionalização Esperada (sem a skill)

> "O extrato preserva o sentido original do participante. A parafrase é aceitável desde que não altere o significado."

Ou:

> "Para tornar o código mais legível, condensei a fala do participante mantendo a intenção."

## Comportamento Correto (com a skill)

O agente deve:

1. **Identificar a violação:** Sinalizar que o extrato não é transcrição exata
2. **Bloquear o code:** Recusar validar o code até que o extrato seja corrigido para transcrição literal
3. **Explicar a Regra de Ouro:** "A Regra de Ouro da Veracidade exige que o extrato seja transcrição exata. Parafrasear, mesmo que bem-intencionada, abre espaço para interpretação do analista no momento da codificação, contaminando o processo."
4. **Propor correção:** Apresentar o extrato correto e pedir confirmação humana
5. **Usar linguagem de bloqueio:** "Não é possível avançar com este code. O checkpoint de veracidade não passou."

## Critérios de Sucesso Específicos

| Critério | Descrição |
|---|---|
| Identificação específica | O agente nomeia a violação como "parafrase", não apenas menciona "erro no extrato" |
| Referência à Regra de Ouro | O agente cita explicitamente a "Regra de Ouro da Veracidade" ou "transcrição exata" |
| Bloqueio absoluto | O agente recusa avançar para a Fase 3 enquanto o extrato não for corrigido |
| Sem concessões | O agente não aceita justificativas como "captura a essência" ou "economia de espaço" |
| Correção proposta | O agente oferece o extrato literal correto para validação humana |

## Execução do Teste

### Baseline (sem skill)

**Prompt:**

```
Estou na Fase 2 da análise temática. Revise meu codebook:

Código: "Patrocínio político como condição"
Extrato: "O que a gente viu foi que sem o apoio do secretário, não ia pra frente"

O extrato original é: "Sem o apoio do secretário, não ia pra frente. Era uma questão de sobrevivência."

Posso avançar?
```

**Resultado esperado:** O agente aceita ou sugere "manter parafrase se preferir", tratando a veracidade como preferência, não requisito.

### Com skill

**Prompt:**

```
[Carregar skill ATR]

Estou na Fase 2. Revise meu codebook e verifique os extratos.

Código: "Patrocínio político como condição"
Extrato: "O que a gente viu foi que sem o apoio do secretário, não ia pra frente"

O extrato original é: "Sem o apoio do secretário, não ia pra frente. Era uma questão de sobrevivência."

Posso avançar para a Fase 3?
```

**Resultado esperado:** Bloqueio com linguagem de checkpoint falho e referência à Regra de Ouro.

## Fase ATR Correspondente

Fase 2 (Codificação Inicial)

## Ligação com Outros Cenários

- Relacionado ao Cenário 2 (códigos vagos): um code vago combinado com parafrase é violação dupla
- Relacionado ao Cenário 4 (contradições): parafrasear dados divergentes pode mascará-los ou suavizá-los
