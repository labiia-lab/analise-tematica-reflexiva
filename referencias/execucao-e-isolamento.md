# Execução, isolamento e andaime

## Sumário

1. Por que separar papéis
2. Perfis de execução
3. O que cada função isolada recebe
4. Instruções das funções isoladas
5. Teste de aptidão
6. Andaime reforçado
7. Leitura conferida
8. Hipóteses e antiancoragem

## 1. Por que separar papéis

Um modelo que constrói temas, contesta os próprios temas e depois aprova a fase tende a confirmar o que já escreveu. O resultado típico é uma rival que não ameaça o mapa, condições de derrota “não satisfeitas” em todos os temas e portões que sempre passam. Separar papéis não torna a análise verdadeira; tira de quem produziu a possibilidade de se aprovar.

Separar significa **contexto limpo**: a função recebe arquivos, não a conversa nem o raciocínio de quem produziu.

## 2. Perfis de execução

| | Isolado | Sequencial |
|---|---|---|
| Condição | o ambiente abre subagentes, sessões ou processos separados | um só contexto |
| Analista rival | contexto limpo, codifica o corpus com outra lente | passe separado, depois do mapa principal |
| Estatuto da rival | `independente`, se a separação for demonstrada | `informada` |
| Portões interpretativos | avaliador em contexto limpo | `autoavaliação` em passe separado |
| Casos múltiplos | um contexto por caso | isolamento não demonstrável |
| Evidência a registrar | o que cada função recebeu e o que não recebeu | a ordem dos passes e os arquivos lidos em cada um |

Escolher o perfil em F0 pelo que o ambiente realmente oferece. Não declarar `isolado` por intenção: registrar como a separação foi obtida (ferramenta, sessão, modelo). Na dúvida, `sequencial`.

No perfil sequencial, cada passe começa relendo somente os arquivos da análise, sem recorrer ao que foi “pensado” antes, e escreve seu resultado em arquivo antes do passe seguinte. Isso reduz, mas não elimina, a contaminação; por isso os rótulos mudam.

Quando houver mais de um modelo disponível, usar outro modelo para o analista rival e, se possível, para o avaliador de portões. Registrar qual. Modelos diferentes compartilham menos vocabulário; continuam não sendo triangulação humana.

## 3. O que cada função isolada recebe

| Função | Recebe | Não recebe |
|---|---|---|
| Analista rival | corpus, pergunta, `00-constituicao-analitica.md`, lente atribuída, formato do registro | memos, códigos, temas e hipóteses do analista principal |
| Contestador | corpus, pergunta, `03-temas-candidatos.md`, `evidencias.jsonl` | justificativas internas do analista; resultado esperado |
| Avaliador de adequação | excerto, janela de contexto, afirmação | nome do tema, restante do relatório, quem escreveu |
| Avaliador de portões | arquivos da fase, `evidencias.jsonl`, saídas do auditor, rubrica e âncoras | a conversa de produção; autoavaliações anteriores |
| Analista de um caso | corpus daquele caso, pergunta, F0 | corpus e resultados dos outros casos |

Registrar no dossiê, por função: ambiente e modelo, o que recebeu, o que foi ocultado e o artefato devolvido.

## 4. Instruções das funções isoladas

Adaptar ao caso, sem acrescentar conclusões nem pistas do mapa principal. Os textos abaixo dizem o que pedir; não são prompts para copiar com os dados dentro.

### Analista rival

Pedir uma análise temática reflexiva própria do corpus, até temas candidatos, respondendo à mesma pergunta. Atribuir uma lente diferente da principal e dizê-la: se a principal lê experiência e sentido vivido, a rival lê condições, normas e relações de poder que organizam o que é dito, ou o inverso. Pedir registro de evidências no mesmo formato, com excertos literais e localizador. Dizer que o objetivo é a melhor leitura possível do corpus, não discordar de alguém.

### Contestador

Entregar os temas candidatos e o registro. Pedir, nesta ordem:

1. para cada tema, antes de reler as evidências, a condição que o faria cair, perder a fronteira ou ser absorvido por outro;
2. busca no corpus dos excertos que mais tensionam cada tema, com localizador; se nada for achado, onde e como procurou;
3. teste de exclusão: como fica a resposta à pergunta sem o tema;
4. teste de fusão para cada par vizinho: o que se perde ao fundir, com excertos;
5. qual tema é o mais fraco e por quê.

Dizer que elogio não é resposta e que “não encontrei” só vale com o registro da busca.

### Avaliador de adequação

Entregar, por item, apenas o excerto, as linhas em volta e a afirmação que ele deveria sustentar. Pedir uma de três respostas, com uma frase de razão: `sustenta`, `tensiona` ou `não se relaciona`. Não informar o tema nem o restante do argumento: o teste é se o excerto carrega a afirmação sozinho.

### Avaliador de portões

Entregar os arquivos da fase, o registro, as saídas do auditor e `referencias/rubrica-e-ancoras.md`. Pedir a rubrica preenchida com trecho de evidência por critério, o tema mais fraco, o problema mais grave e o que mudaria a nota. Dizer que a função é encontrar o que falha e que uma fase sem nenhum problema apontado será lida como avaliação não feita.

## 5. Teste de aptidão

A tarefa está em `scripts/aptidao/tarefa.md`. Mede três coisas que a skill pressupõe: copiar um trecho sem alterá-lo, distinguir tema de tópico e perceber uma citação polida ou inventada.

| Resultado | O que fazer |
|---|---|
| `apto` | seguir com o perfil disponível |
| `parcial` | seguir com o andaime reforçado; registrar a parte que falhou |
| `inapto` | avisar o usuário antes de F0; se mandar continuar, andaime reforçado e resultado no estatuto final |

O teste é um piso. Passar não garante profundidade interpretativa; falhar indica risco alto de citação alterada e de temas que são assuntos.

## 6. Andaime reforçado

Usar quando a aptidão for `parcial` ou `inapto`, quando o corpus não couber com folga no contexto ou quando o modelo perder o fio entre fases.

- **Lotes pequenos.** Uma fonte por vez, ou trechos de até cerca de 1.500 palavras, sempre com o identificador da fonte e as linhas.
- **Memo por fonte.** Escrever e gravar o memo antes de abrir a fonte seguinte.
- **Excerto antes do código.** Gravar o excerto, rodar a verificação do lote e só então codificar.
- **Um código por vez contra os pares.** Antes de aceitar um código, compará-lo com o par contrastivo de `referencias/rubrica-e-ancoras.md`.
- **Arquivos como memória.** Reler `00`, o registro e o memo da fase anterior no início de cada fase; não confiar no que ficou no contexto.
- **Frase-teste por tema.** Completar “este tema argumenta que…” antes de dar nome ao tema.
- **Sem atalhos de formato.** Não resumir o corpus para “caber”; reduzir o lote.

O andaime reforçado torna a execução mais lenta e mais conferível. Não muda o que é exigido.

## 7. Leitura conferida

`leitura.jsonl` registra o que foi percorrido:

```json
{"fonte": "P01.txt", "inicio": 1, "fim": 240, "memo": "M01"}
```

- `fonte` é o caminho relativo que consta no manifesto;
- `inicio` e `fim` são linhas, inclusive;
- `memo` aponta o memo de familiarização que cobre o intervalo.

O auditor soma os intervalos, compara com as linhas do manifesto e devolve `integral` ou `parcial`, com a lista de fontes incompletas. Cobertura parcial declarada é legítima e delimita o que a análise pode afirmar. Cobertura parcial apresentada como integral é a falha.

## 8. Hipóteses e antiancoragem

A primeira leitura produz expectativas, e expectativas não registradas viram temas sem passar por teste. Em F1, gravar cada uma:

```json
{"tipo": "hipotese", "id": "H1", "texto": "a diferença principal seria entre faixas de renda", "destino": "pendente"}
```

Em F5, atualizar `destino` para `mantida`, `revista` ou `derrubada` e preencher `evidencia`. O auditor alerta quando não há hipóteses, quando alguma segue pendente e quando nenhuma foi revista ou derrubada. Esse último alerta não prova erro: pede que se mostre por que a leitura inicial resistiu a todo o corpus e à contestação.

Não escrever em F1 a lista de temas nem um mapa provisório com cara de final. Se a familiarização já contém os temas que aparecerão em F5, a codificação serviu para confirmá-los.
