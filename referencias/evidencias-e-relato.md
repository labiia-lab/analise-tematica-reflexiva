# Evidências e relato

## Sumário

1. Registro único de evidências
2. Estatuto das fontes
3. Excertos: literal, paráfrase, contexto e falante
4. Distribuição da evidência
5. Relatório analítico
6. Literatura
7. Sobrealegação
8. Checklist de relato
9. Dossiê de auditoria

## 1. Registro único de evidências

`evidencias.jsonl` é a única fonte de verdade sobre o que sustenta o quê. Uma linha por registro, com o campo `tipo`. Genealogias, contagens e matrizes são geradas dele; quando o texto de uma fase discorda do registro, o texto está errado.

```json
{"tipo": "fonte", "id": "F01", "arquivo": "P01.txt", "estatuto": "fala_primaria"}
{"tipo": "excerto", "id": "Q001", "fonte": "F01", "forma": "literal", "texto": "...", "localizador": "linha 42", "contexto": "linhas 38-46", "falante": "P01", "provocacao": "pergunta 3 do roteiro"}
{"tipo": "codigo", "id": "C01", "rotulo": "...", "excertos": ["Q001"], "estado": "ativo"}
{"tipo": "tema", "id": "TC1", "fase": "candidato", "nome": "...", "conceito": "...", "codigos": ["C01"]}
{"tipo": "tema", "id": "TF1", "fase": "final", "nome": "...", "conceito": "...", "codigos": ["C01"], "origem": ["TC1"], "ancoras": ["Q001"], "evidencia_decisiva": ["Q001"], "tensoes": ["Q014"]}
{"tipo": "hipotese", "id": "H1", "texto": "...", "destino": "pendente"}
{"tipo": "nao_representado", "id": "N1", "excerto": "Q030", "tratamento": "fora do mapa; registrado como limite em TF2"}
{"tipo": "citacao_externa", "id": "L1", "texto": "...", "referencia": "..."}
```

| Tipo | Campos obrigatórios | Campos úteis |
|---|---|---|
| `fonte` | `id`, `arquivo`, `estatuto` | `caso` |
| `excerto` | `id`, `fonte`, `texto`, `forma`; se literal, `localizador` e `contexto` | `falante`, `voz`, `provocacao` |
| `codigo` | `id`, `rotulo`, `excertos` | `estado`, `destino`, `justificativa`, `compartilhado`, `nota`, `origem` |
| `tema` | `id`, `fase`, `nome`, `conceito`, `codigos` | `origem`, `ancoras`, `evidencia_decisiva`, `tensoes`, `busca_contraevidencia` |
| `hipotese` | `id`, `texto`, `destino` | `evidencia` |
| `nao_representado` | `id`, `excerto`, `tratamento` | |
| `citacao_externa` | `id`, `texto`, `referencia` | |

Regras que o auditor confere:

- `arquivo` é o caminho da fonte como aparece no campo `source` do manifesto;
- um excerto listado em `tensoes` pode também constar em `nao_representado`; um que esteja em `ancoras`, em `evidencia_decisiva` ou em código do tema, não;
- `estado` do código: `ativo` (padrão), `fundido` (com `destino`), `recusado` ou `residuo` (com `justificativa`);
- ao fim, todo código `ativo` pertence a um tema final;
- código em mais de um tema final precisa do campo `compartilhado`, dizendo o que ele faz em cada um;
- `ancoras` e `evidencia_decisiva` só aceitam excertos literais;
- tema final registra `tensoes` ou, se nada foi achado, `busca_contraevidencia` com a descrição da busca (a falta gera alerta);
- `origem` de um tema final lista os candidatos de que ele veio; é o que permite calcular fusões, divisões e abandonos.

O registro cresce durante a análise. Não apagar códigos recusados nem temas candidatos abandonados: mudar o estado. A história da análise fica no arquivo.

## 2. Estatuto das fontes

| Estatuto | O que é | Consequência |
|---|---|---|
| `fala_primaria` | transcrição conferida de fala | pode ser citada como fala |
| `texto_do_participante` | resposta escrita, postagem, carta | citada como texto de quem escreveu |
| `documento` | norma, relatório institucional, matéria | citado como documento, com autoria institucional |
| `transcricao_automatica` | fala transcrita por máquina, sem conferência | citar com a ressalva; não tratar como fala confirmada |
| `nota_de_mediador` | relatório de moderador, nota de campo, síntese de sessão | voz de quem mediou; nunca entre aspas como fala de participante |
| `resumo_de_segunda_mao` | fichamento, resenha, resumo feito por terceiros ou por IA | voz de quem resumiu, gravada como `voz: mediador`; a análise é sobre a leitura do resumidor |
| `outro` | descrever em F0 | definir a consequência em F0 |

Dois cuidados que mudam o que a análise pode afirmar:

**Nota de mediador.** “Considera os votos estratégicos” é uma frase do moderador sobre alguém. Pode ser evidência do que o moderador registrou. Não é excerto de fala e não sustenta, sozinha, uma afirmação sobre como participantes constroem sentido.

**Resumo de segunda mão.** Quando o corpus é formado por fichamentos, o vocabulário recorrente pode ser do fichador. Um padrão “encontrado” em vinte resumos escritos pela mesma mão pode ser um hábito de escrita. Declarar em F0 que a análise trata de leituras de textos, formular a pergunta nesse nível e não atribuir aos autores originais palavras que só existem no resumo.

**Citação dentro de resumo.** Quando o fichamento ou a nota reproduz entre aspas um documento ou uma fala, o excerto continua sendo do resumo: quem escolheu e recortou o trecho foi quem resumiu. Gravar com `voz: mediador` e dizer no texto “o fichamento cita…”. Para afirmar algo sobre o documento ou a pessoa citada, é preciso a fonte original no corpus.

**Como nomear a fonte no relatório.** Identificar o resumo e o texto resumido sem transferir a autoria das palavras: “o fichamento de [autor, ano] descreve…”, e não “[autor] afirma…”. O auditor alerta quando mais da metade dos excertos dos temas vem de fonte mediada, resumida ou transcrita por máquina; a resposta é dizer, no relatório, de quem é a voz analisada.

Corpus que mistura estatutos é comum. Registrar o estatuto por fonte e conferir, na matriz de distribuição, se os temas se apoiam em fala ou em registro mediado.

## 3. Excertos: literal, paráfrase, contexto e falante

**Literal.** Copiado caractere por caractere, com localizador estável (linha, turno, página ou tempo) e `verified_exact`. Preferir o formato `linha N` do derivado textual: é o que o verificador calcula e o que a análise de posição no corpus consegue ler; página ou tempo do original entram como complemento. Supressão interna marcada com `[...]`; cada fragmento precisa existir no mesmo excerto.

**Paráfrase.** Qualquer texto alterado, resumido, “limpo” ou reconstruído. Registrar com `forma: parafrase`, sem aspas no relatório, com a fonte e a palavra “paráfrase”. Não ancora tema nem serve de evidência decisiva. Citação montada com trechos de duas falas ou de dois arquivos é paráfrase.

**Contexto.** `contexto` aponta a janela em volta do excerto. Uma frase de quatro palavras raramente carrega uma interpretação; o auditor alerta para âncoras curtas. Ler a janela antes de interpretar e registrar em `provocacao` a pergunta ou a fala que provocou o excerto quando ela muda o sentido: resposta a pergunta sugestiva é coprodução.

**Falante.** Usar o identificador anonimizado. Quando a transcrição não atribui a fala, gravar `nao_atribuido` e escrever “uma participante do grupo”, não um indivíduo. Não inferir perfil (renda, voto, religião) que não esteja no corpus.

**Substituição.** Quando o verificador devolve `substituir`, o trecho sugerido é outro texto. Reler em contexto, confirmar que sustenta o mesmo código e a mesma afirmação e só então trocar. Se o sentido mudou, descartar o excerto e rever o que dependia dele.

## 4. Distribuição da evidência

O auditor devolve a matriz tema por fonte e a posição dos excertos no corpus. Ler antes de fechar F5:

| Sinal | Pergunta a responder |
|---|---|
| tema apoiado em uma só fonte | é um padrão ou o relato de um caso? |
| um falante ancora mais da metade dos temas | a análise está contando a história de uma pessoa articulada? |
| excertos concentrados em um terço do corpus | o restante foi lido com a mesma atenção? |
| fonte ou tipo de fonte nunca citado | o que essas fontes dizem que os temas não alcançam? |
| muitos excertos de fonte mediada | os temas descrevem participantes ou o olhar de quem mediou? |

Não corrigir a distribuição por cota. Um tema pode legitimamente apoiar-se em poucas fontes; o que não pode é isso ficar invisível.

## 5. Relatório analítico

O relatório é o lugar em que a análise acontece por escrito. Um relatório que lista citações ou resume assuntos não é a análise com outra roupa: é a falta dela.

### Estrutura

1. título analítico, estatuto em poucas linhas e resumo;
2. pergunta, corpus e como a análise foi feita, em poucos parágrafos;
3. **visão sinóptica**: tabela ou mapa com os temas, o conceito organizador de cada um e como se relacionam;
4. narrativa integradora: a resposta geral antes dos temas;
5. um argumento por tema;
6. relações entre temas e, conforme o nível escolhido, diálogo com a literatura;
7. **o que esta análise não pode afirmar**;
8. conclusão proporcional ao corpus e referências efetivamente citadas.

Passaportes, registros de IA, portões e tabelas de verificação ficam no dossiê. O leitor do relatório não deve atravessar auditoria para chegar ao argumento.

### Movimento de cada tema

1. **Afirmação.** O que o tema argumenta, em uma ou duas frases.
2. **Excerto.** Literal, do registro, com fonte e localizador.
3. **O que o excerto faz.** Não repetir o excerto com outras palavras. Dizer o que nele sustenta a afirmação: uma escolha de palavra, uma condição, uma hesitação, o que ele pressupõe.
4. **Variação ou tensão.** O caso que complica, com o seu excerto. Tema sem variação costuma ser tópico.
5. **Resposta.** O que o tema acrescenta à resposta à pergunta.

Repetir os passos 2 a 4 quantas vezes o argumento pedir. O teste de cada excerto: se ele pode ser retirado sem o parágrafo perder sentido, estava ali como ilustração.

### Regras

- Nenhuma citação sem comentário interpretativo em seguida. Duas citações seguidas pedem um comentário entre elas ou a escolha de uma.
- Nenhum tema apoiado em um único excerto, e de preferência não em uma única fonte.
- Toda citação está no registro como literal verificada. Citação de literatura entra como `citacao_externa`.
- Contagens (“a maioria”, percentuais) não sustentam temas. Quando descrevem o corpus, ficam na apresentação do corpus.
- Primeira pessoa e verbos de construção: “construí”, “interpreto”, “proponho”. Tema não emerge.
- Nome de tema que afirma algo. “Opiniões sobre X” e “Vantagens e desvantagens de Y” são nomes de tópico.

## 6. Literatura

| Nível | O que entra | Como registrar |
|---|---|---|
| sem literatura | nada | uma frase no método e nos limites |
| literatura fornecida | apenas textos entregues pelo usuário | lista das fontes em F0; trechos citados como `citacao_externa` |
| busca conferida | referências localizadas e abertas no ambiente | referência completa e onde foi conferida |

Usar a literatura para situar, tensionar ou nomear o que a análise construiu, não para emprestar autoridade. Um conceito alheio só entra se o corpus o sustenta; dizer onde.

Quando a literatura fornecida vier em fichamentos, citar o fichamento como a fonte consultada. Aspas só para o que estiver literalmente no arquivo, e sem afirmar que são palavras do autor original, salvo se o fichamento trouxer a citação com página.

Referência lembrada e não conferida não entra em nenhum nível. Sem acesso à fonte, escrever que o diálogo com a literatura ficou por fazer.

## 7. Sobrealegação

`auditar_analise.py sobrealegacao` lista frases com quatro famílias de termos, fora das citações:

| Família | Exemplos | Risco |
|---|---|---|
| generalização | todos, sempre, a maioria, “o eleitor de…” | afirmar sobre uma população a partir de um corpus qualitativo |
| causalidade | leva a, tende a, prova que, determina | afirmar mecanismo que o desenho não observa |
| quantificação | percentuais, “12 de 40” | usar contagem como peso de evidência |
| vocabulário incompatível | emergiu, saturação, viés, variável independente, confiabilidade, triangulação | importar critérios de outra tradição |

O script marca `negado_na_frase` quando há negação antes do termo na mesma frase; costuma ser uso legítimo, mas ainda pede resposta. Para cada item, uma de três respostas, registrada no dossiê: **manter** com a evidência que sustenta, **restringir** ao corpus (“neste grupo”, “nas falas analisadas”) ou **cortar**. Termo citado para recusar (“não busquei saturação”) é uso legítimo: responder “manter” com essa razão.

A lista não é exaustiva. O avaliador de portões lê o relatório procurando o mesmo problema sem depender dos termos.

## 8. Checklist de relato

Aplicado pelo avaliador de portões sobre o relatório. Adaptado de Braun e Clarke (2006, lista de quinze critérios; 2021, perguntas de avaliação); conferir a fonte primária antes de citar em manuscrito.

**Coerência entre o que se diz e o que se faz**

- [ ] A abordagem de análise temática e seus pressupostos estão declarados.
- [ ] O que o método descreve corresponde ao que os arquivos mostram.
- [ ] A linguagem é coerente com a posição declarada; o pesquisador aparece como ativo.
- [ ] Não há critérios importados de outra tradição apresentados como qualidade.

**Temas**

- [ ] Os temas são padrões de significado com conceito organizador, não assuntos nem perguntas do instrumento.
- [ ] São coerentes por dentro e distintos entre si.
- [ ] Foram conferidos uns contra os outros e contra o corpus.

**Evidência e interpretação**

- [ ] Os dados foram interpretados, não parafraseados.
- [ ] Análise e excertos se correspondem: o excerto mostra o que o texto afirma.
- [ ] Há equilíbrio entre narrativa analítica e excertos; nenhum excerto fala sozinho.
- [ ] A codificação cobriu o corpus, sem depender de poucos exemplos vívidos.

**Texto**

- [ ] O relatório conta uma história organizada e responde à pergunta.
- [ ] Há visão sinóptica dos temas.
- [ ] Os limites do que se pode afirmar estão escritos.

Cada item recebe `sim`, `em parte` ou `não`, com o trecho do relatório que justifica. O avaliador aponta os dois itens mais fracos.

## 9. Dossiê de auditoria

`07-dossie-de-auditoria.md` reúne o que permite refazer e contestar a análise: estatuto completo, manifesto de IA, delegação, funções isoladas e o que cada uma recebeu, interações, mapa humano, cobertura, verificação de citações, adequação, portões computados e interpretativos, alertas do auditor com resposta, itens de sobrealegação com resposta, decisão de privacidade, efeito da contestação, destino das hipóteses, passaportes e lista do pacote de saída.

O dossiê pode ser longo. O relatório não deve sê-lo por causa dele.
