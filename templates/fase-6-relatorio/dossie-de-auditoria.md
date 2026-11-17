# F6 — Dossiê de auditoria

Guia de uso: este arquivo vira `07-dossie-de-auditoria.md`. Reúne o que permite refazer e contestar a análise. Apagar guias e colchetes na saída.

## A. Estatuto da entrega

| Dimensão | Registro |
|---|---|
| Fluxo |  |
| Perfil de execução |  |
| Aptidão |  |
| Cobertura |  |
| Evidências |  |
| Contestação e seu efeito |  |
| Avaliação dos portões |  |
| Privacidade |  |
| Participação humana |  |
| Validação humana |  |
| Prontidão |  |

Valores possíveis: fluxo F0–F6 executado ou interrompido; perfil isolado ou sequencial; aptidão apto, parcial, inapto ou N/A; cobertura integral, parcial ou indeterminada; evidências verificáveis, limitadas ou inválidas; contestação independente, informada ou ausente, com ou sem efeito estrutural; avaliação independente ou autoavaliação; privacidade decidida pelo usuário, padrão aplicado e pendente de confirmação, ou não aplicável; validação humana realizada, parcial ou ausente; prontidão manuscrito, exploração ou auditoria.

Formulação máxima permitida, quando todos os portões substantivos passarem e a cobertura for integral:

> ATR autônoma completa no escopo declarado e auditável; redação pronta para incorporação em manuscrito; sem validação humana.

## B. Manifesto estruturado de IA

| Campo | Registro final |
|---|---|
| Data e ambiente |  |
| Modelo/versão do analista principal |  |
| Modelo/versão das funções isoladas |  |
| Parâmetros expostos |  |
| Skill e versão | analise-tematica-reflexiva |
| Rota, profundidade e perfil |  |
| Corpus processado |  |
| Limitações |  |

## C. Funções e isolamento

| Função | Ambiente/modelo | O que recebeu | O que foi ocultado | Artefato devolvido |
|---|---|---|---|---|
| analista rival |  |  |  |  |
| contestador |  |  |  |  |
| avaliador de adequação |  |  |  |  |
| avaliador de portões |  |  |  |  |

## D. Matriz final de delegação

| Fase | Função delegada | Nível 0–3 | Ambiente/modelo | Verificação | Papel humano |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## E. Registro de interação com IA

| ID | Fase/função | Ambiente/modelo | Objetivo e prompt sanitizado | Fontes por ID | Artefato | Verificação | Intervenção humana/efeito |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## F. Mapa de participação humana

| Fase | Participante/papel | Intervenção | Efeito analítico | Pendente |
|---|---|---|---|---|
|  |  |  |  |  |

## G. Cobertura

Arquivos: `manifesto-corpus.jsonl`, `leitura.jsonl` e, se aplicável, `manifesto-derivados.jsonl`.

- resultado do auditor:
- fontes incompletas e consequência:
- estatuto das fontes e peso de cada tipo nos temas:

## H. Verificação de citações

Arquivos: `citacoes.jsonl` e `verificacao-citacoes.jsonl`.

- excertos literais no registro e quantos estão `verified_exact`:
- correções por relocalização:
- substituições aceitas, com a reavaliação de adequação de cada uma:
- excertos descartados:
- citações do relatório conferidas contra o registro:

## I. Checagem de adequação

| Excerto | Afirmação | Resposta | Ação |
|---|---|---|---|
|  |  |  |  |

## J. Portões

| Fase | Computado | Evidência | Interpretativo | Avaliador/independência | Efeito no estatuto |
|---|---|---|---|---|---|
| F0 |  |  |  |  |  |
| F1 |  |  |  |  |  |
| F2 |  |  |  |  |  |
| F3 |  |  |  |  |  |
| F4 |  |  |  |  |  |
| F5 |  |  |  |  |  |
| F6 |  |  |  |  |  |

Avaliador/independência: contexto limpo, autoavaliação ou humano. Qualquer `FAIL` substantivo, ou critério `insuficiente`, bloqueia “completa” e “pronta para manuscrito”, sem impedir a entrega diagnóstica.

### Ranking forçado por fase

| Fase | Tema mais fraco | Problema mais grave | Afirmação mais exposta | O que foi feito |
|---|---|---|---|---|
|  |  |  |  |  |

### Checklist de relato

| Item | sim / em parte / não | Trecho do relatório |
|---|---|---|
|  |  |  |

## K. Alertas do auditor e respostas

Arquivo: `auditoria-integridade.json`.

| Código | Alerta | Resposta | Mudança feita |
|---|---|---|---|
|  |  |  |  |

Guia: todo alerta recebe resposta. Erros são corrigidos antes da entrega; os que restarem são listados aqui com o efeito no estatuto.

## L. Sobrealegação

Arquivo: `sobrealegacao.json`.

| Onde | Termo | Resposta | Razão |
|---|---|---|---|
|  |  |  |  |

Respostas: manter com evidência, restringir, cortar.

## M. Privacidade

Arquivo: `privacidade.json`.

- classes de candidatos encontradas:
- o que foi perguntado ao usuário e o que ele decidiu:
- trocas feitas na saída:
- pendências:

## N. Contestação

- efeito calculado:

| Tema | Rival | Estatuto | Condição de derrota e quem a escreveu | Contraevidência | Exclusão | Decisão |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## O. Hipóteses e contaminação

| Hipótese | Destino | Evidência |
|---|---|---|
|  |  |  |

- itens do registro de contaminação e o que aconteceu com cada um:

## P. Passaportes dos temas

[Inserir os passaportes de F5 ou apontar `05-temas-finais-e-passaportes.md`.]

## Q. Pacote de saída

| Arquivo | Presente? | Observação |
|---|---|---|
| `00` a `07` (.md) |  |  |
| `evidencias.jsonl` |  |  |
| `genealogia.md` |  |  |
| `citacoes.jsonl` e `verificacao-citacoes.jsonl` |  |  |
| `manifesto-corpus.jsonl` e `leitura.jsonl` |  |  |
| `auditoria-integridade.json` |  |  |
| `privacidade.json` e `sobrealegacao.json` |  |  |
| `manifesto-derivados.jsonl` |  |  |
| `aptidao.json` |  |  |
| pasta `rival/` |  |  |
| `homogeneizacao.json` e síntese comparativa |  |  |

Registrar `N/A` para o que não se aplicar.
