# F5 — Temas finais e passaportes

## 1. Arquitetura final

| ID | Tema final | Conceito organizador | Afirmação | Relação com a pergunta |
|---|---|---|---|---|
| TF1 |  |  |  |  |

## 2. Narrativa integradora

[Explicar como os temas constroem conjuntamente a resposta analítica.]

## 3. Passaporte contestável

### [ID — nome]

**Conceito organizador central:**  

**Definição temática (1–2 parágrafos):**

[Definição formal escrita que fixa o escopo exato do tema, seus limites analíticos e a essência do conceito organizador (2016-capitulo). Não substituir por lista de campos: a redação integrada é onde ambiguidades de escopo aparecem.]

**Título:**  

- ativo, conciso e informativo?
- expressa o conceito organizador em vez de rótulo burocrático (“Barreiras”, “Experiências de...”, “Impactos”)?
- incorpora expressão literal marcante do corpus quando pertinente, como em “Ser ‘mentalmente voltado para o exercício’ (ou não)”?

**Afirmação interpretativa:**  

**Genealogia:**

- códigos principais:
- tema(s) candidato(s):
- mudanças após F4:

**Excertos-âncora verificados:**

| ID | Excerto literal | Fonte/localização | Verificação | Função analítica | Uso |
|---|---|---|---|---|---|
| Q001 |  |  | verified_exact |  | analítico/ilustrativo |

**Teste do uso analítico (2016-capitulo):**

- é possível remover o excerto ou substituí-lo por outro equivalente sem alterar o sentido da narrativa analítica?
  - sim → uso ilustrativo: aceitável como apoio, mas o tema precisa de pelo menos uma âncora analítica;
  - não → uso analítico: o excerto é insubstituível e sustenta a interpretação.

Âncoras centrais de cada tema devem ser de uso analítico. Uso meramente ilustrativo não sustenta a interpretação.

**Rival interpretativa mais forte:**  

**Estatuto da rival:** independente | informada | ausente  

**Evidência decisiva da escolha:**  

**Resíduo experiencial e interpretativo:**  

**Tratamento do resíduo:** reincorporado | preservado como tensão | deslocado | excluído com justificativa

**Decisão:** manter | revisar | dividir | fundir | abandonar

**Zona de incerteza:**  

**Participação humana:**  

[Repetir para cada tema.]

## 4. Relações e fronteiras

| Par de temas | Relação | Diferença decisiva | Sobreposição aceita |
|---|---|---|---|
|  |  |  |  |

## 5. Mapa final

### Estrutura para o diagrama

Preencher o JSON do script `scripts/gerar_mapa_tematico.py` com a estrutura real:

| Código | Tema candidato | Tema final |
|---|---|---|
|  |  |  |

- quebras de linha manuais quando necessário (campo `linhas`);
- agrupamentos conceituais marcados com `grupo` (vazio extra entre blocos);
- um tema final por bloco conceitual distinto.

Comando:

```text
python "<PASTA_DA_SKILL>/scripts/gerar_mapa_tematico.py" --input mapa.json --output mapa-tematico.svg
```

Produzir sempre os dois arquivos: `mapa-tematico.svg` (editável) e `mapa-tematico.png` (1448 × 1086 px). O script reduz automaticamente a fonte de cada linha em passos de 0,5 px até o texto caber dentro do quadro — conferir no stderr se algum item não pôde ser ajustado e encurtar o texto nesse caso. Ajustes visuais e regras de tipografia, cores e setas estão em `referencias/visualizacoes.md`.

### Esboço textual

```text
Resposta integradora
├── Tema final 1
│   └── tensão preservada
├── Tema final 2
└── Tema final 3
```

## 6. Registro de interação com IA

| ID | Fase/função | Ambiente/modelo | Objetivo e prompt sanitizado | Fontes por ID | Artefato | Verificação | Intervenção humana/efeito |
|---|---|---|---|---|---|---|---|
|  | F5 |  |  |  |  |  |  |

## 7. Gate F5

| Requisito | PASS/FAIL/N/A | Evidência |
|---|---|---|
| passaporte completo por tema |  |  |
| definição temática formal redigida |  |  |
| títulos expressam conceito organizador |  |  |
| genealogia e fronteiras explícitas |  |  |
| âncoras `verified_exact` |  |  |
| âncoras centrais de uso analítico |  |  |
| mapa temático vetorial produzido (SVG) e PNG correspondente |  |  |
| nenhum texto fora do quadro |  |  |
| rival, resíduo e incerteza visíveis |  |  |

Arquivos de verificação: `citacoes.jsonl` e `verificacao-citacoes.jsonl`.

## 8. Exemplo curto

**Tema:** A opinião precisa mostrar seu caminho  
**Rival:** faixas de renda produziriam critérios fixos e opostos de competência política.  
**Decisão:** rejeitar o determinismo; fontes verificáveis e experiência cotidiana aparecem como formas móveis de prestar contas pelo julgamento.  
**Resíduo:** a fala “depende do contexto” não é mero vazio; limita generalizações e permanece como tensão.

## 9. Critério de saída

- [ ] Cada tema possui conceito, afirmação e fronteira.
- [ ] Cada tema possui definição temática formal de 1–2 parágrafos.
- [ ] Os títulos expressam conceitos organizadores, não rótulos descritivos.
- [ ] Cada passaporte está completo.
- [ ] Excertos-âncora estão `verified_exact` e localizados.
- [ ] As âncoras centrais são de uso analítico, não meramente ilustrativo.
- [ ] O mapa temático foi gerado em SVG com PNG correspondente e representa os agrupamentos reais.
- [ ] Nenhum texto ficou para fora do quadro (verificado pelo gerador).
- [ ] Rival, evidência decisiva e resíduo estão visíveis.
- [ ] Não há confiança numérica.
- [ ] O mapa final preserva complexidade sem redundância.
