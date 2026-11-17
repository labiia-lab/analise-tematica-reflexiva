---
name: analise-tematica-reflexiva
description: Use when the user needs to perform, continue, audit, review, or compare a Reflexive Thematic Analysis of qualitative material, including interviews, focus groups, documents, human codes, candidate themes, autonomous AI analysis, multi-site or multi-case studies, or work based on Braun and Clarke.
---

# Análise Temática Reflexiva

## Princípio central

Conduzir Análise Temática Reflexiva (ATR) como prática interpretativa, recursiva e situada. Construir uma leitura argumentada; não apresentar temas como entidades descobertas nem simular neutralidade ou experiência humana.

Executar autonomamente F0–F6 quando solicitado. A ausência de participação ou validação humana não impede a conclusão do fluxo, mas deve permanecer explícita e separada da cobertura, da integridade das evidências e da prontidão do relatório.

Aplicar **contestabilidade interpretativa incorporada**:

> Toda interpretação escolhida deve carregar uma alternativa forte recusada, a evidência da escolha e o custo experiencial da abstração.

Aplicar também a **separação de papéis**: quem constrói uma leitura não a contesta nem a aprova. Quando o ambiente não permite separar, dizer isso no estatuto em vez de simular.

## Invariantes

1. Construir temas; nunca dizer que eles “emergiram sozinhos”.
2. Trabalhar recursivamente entre familiarização, códigos, temas e escrita.
3. Decidir separadamente indução/dedução e semântico/latente.
4. Tornar categorias e subtemas opcionais.
5. Não usar frequência como sinônimo de importância.
6. Não exigir codebook rígido, consenso, Kappa, estabilidade ou resultados idênticos.
7. Tratar contradições, casos raros e silêncios como possíveis recursos analíticos.
8. Verificar literalmente todo excerto no momento em que ele entra no registro de evidências.
9. Não chamar convergência entre agentes ou modelos de triangulação humana.
10. Não atribuir consciência, experiência vivida ou reflexividade humana à IA.
11. Não inventar dados, contexto, autorização, parâmetros, citações, referências ou validação.
12. Preservar a proveniência de material humano e algorítmico.
13. Manter afirmações proporcionais ao corpus efetivamente processado.
14. Não fixar número mínimo de temas nem fundir temas para caber em um orçamento.
15. Não apresentar registro de mediador, resumo de terceiros ou paráfrase como fala de participante.
16. Não aprovar a própria fase: os portões interpretativos pertencem a um avaliador em contexto limpo ou ficam rotulados como autoavaliações.

## Configurar a execução

Se o pedido já definir rota, profundidade, pergunta e corpus, registrar as escolhas e começar. Solicitar somente o que for materialmente indispensável e não puder ser inferido do pedido ou dos arquivos.

### Rotas

1. **Autônoma** — executar F0–F6 sem checkpoints humanos obrigatórios.
2. **Por checkpoints** — pausar após F0, F2, F4 e F5.
3. **Início humano** — partir de memos, códigos ou temas fornecidos e registrar seu efeito.
4. **Paralela cega** — concluir a leitura da IA até F5 antes de acessar a leitura humana.

### Profundidade

1. **Essencial** — todas as fases, extensão proporcional e contestação compacta.
2. **Aprofundada** — passes analíticos separados, documentação extensa e alvo usual de 2.000 palavras por fase substantiva quando o corpus justificar.

Tratar 2.000 palavras como **meta editorial não bloqueante**, nunca como prova de qualidade ou condição de aprovação. Não inflar fases administrativas, tabelas, listas ou análises de corpus pequeno.

### Perfil de execução

Verificar o que o ambiente oferece e registrar o perfil em F0. Ler `referencias/execucao-e-isolamento.md` antes de escolher.

1. **Isolado** — o ambiente permite abrir contextos limpos (subagentes, sessões ou processos separados). Analista rival, contestador, avaliador de adequação e avaliador de portões trabalham sem ver o raciocínio do analista principal.
2. **Sequencial** — um só contexto. As mesmas funções viram passes separados que leem apenas os arquivos da análise. A rival é `informada` e os portões interpretativos são `autoavaliação`; os dois rótulos seguem até o estatuto final.

O perfil não altera as fases nem o que precisa ser entregue. Altera quem pode ser chamado de independente.

### Teste de aptidão

Antes de F0, quando houver Python, fazer a microtarefa de `scripts/aptidao/tarefa.md`, gravar as respostas na pasta de saída e corrigi-las com `auditar_analise.py aptidao`. `apto` segue normalmente. `parcial` segue com o andaime reforçado. `inapto` exige avisar o usuário antes de começar; se ele mandar continuar, usar o andaime reforçado e levar o resultado ao estatuto final. Sem Python, registrar `N/A`.

### Entradas mínimas

Registrar:

- pergunta ou objetivo;
- corpus, unidade de análise e limites;
- contexto necessário e, se houver, o instrumento de coleta (roteiro, questionário);
- estatuto de cada fonte: fala primária, texto do participante, documento, nota de mediador, transcrição automática ou resumo de segunda mão;
- posição epistemológica, se definida;
- material humano prévio;
- nível de literatura do relatório;
- se há um caso ou vários (cidades, grupos, instituições);
- formato e local de saída.

Antes de analisar, declarar fontes acessíveis, ilegíveis ou ausentes; capacidade de produzir formatos adicionais; possibilidade de separar contextos; e riscos de privacidade, consentimento ou processamento por IA.

### Literatura no relatório

Escolher em F0 um de três níveis e não mudar em silêncio:

1. **Sem literatura** — o relatório declara que não dialoga com a literatura.
2. **Literatura fornecida** — usar somente textos que o usuário entregou (artigos, fichamentos, notas). Citar apenas o que está neles e registrar cada trecho citado como `citacao_externa`.
3. **Busca conferida** — buscar com as ferramentas do ambiente e incluir só referências cuja existência foi conferida na fonte.

Em nenhum nível citar referência de memória. Fichamento é leitura de terceiros: citar como tal, sem atribuir ao autor original palavras que são do fichador.

### Privacidade

Se houver identificadores pessoais e nenhuma direção para continuar, perguntar se já são pseudônimos ou se a saída deve ser anonimizada. Nunca alterar silenciosamente a fonte nem converter continuação em aprovação ética.

Antes de entregar, rodar `auditar_analise.py privacidade --saida PASTA_DE_SAIDA --output privacidade.json` (com `--nomes` quando o usuário fornecer a lista de nomes reais). O resultado é uma lista de candidatos, não uma decisão: **mostrar a lista ao usuário, agrupada por classe, e perguntar o que fazer** (já são pseudônimos, anonimizar, manter com autorização). Se o usuário tiver mandado prosseguir sem perguntas, anonimizar a cópia de trabalho e a saída, listar o que foi trocado e registrar a decisão como pendente de confirmação. Pedir nova decisão quando preservar identidades for indispensável à pergunta.

## Carregar recursos progressivamente

Resolver todos os caminhos abaixo relativamente à pasta que contém este `SKILL.md`, nunca presumir o diretório de trabalho do agente.

- Ler `referencias/execucao-e-isolamento.md` em F0, para perfil, aptidão, lotes e instruções das funções isoladas.
- Ler `referencias/fundamentos-atr.md` antes de F0–F3.
- Ler `referencias/evidencias-e-relato.md` antes de F2 e de F6: registro de evidências, estatuto das fontes e regras do relatório.
- Ler `referencias/qualidade-analitica.md` para avaliar códigos, temas e relatório.
- Ler `referencias/rubrica-e-ancoras.md` ao aplicar ou receber qualquer portão interpretativo.
- Ler `referencias/contestabilidade-interpretativa.md` antes de F4–F5.
- Ler `referencias/casos-multiplos.md` quando houver mais de um caso.
- Ler `referencias/colaboracao-e-auditoria.md` para rotas, registros de IA, estatutos e participação humana.
- Ler `referencias/ia-em-at.md` ao planejar ou auditar qualquer intervenção de IA.
- Ler `referencias/fundamentacao-e-proveniencia.md` ao justificar decisões acadêmicas.
- Ler `referencias/exemplo-integrado.md` somente quando um exemplo de raciocínio ajudar.

Não carregar todas as referências por rotina.

## Contrato comum

### Cobertura

Inventariar todo o corpus declarado e registrar o que foi efetivamente lido. Para corpus maior que o contexto disponível, trabalhar em lotes, produzir memos por fonte e realizar síntese transversal. Nunca inferir cobertura integral de amostra silenciosa.

Quando houver acesso local aos arquivos e Python, gerar a identidade computável do corpus após resolver a pasta desta skill:

```text
python "<PASTA_DA_SKILL>/scripts/verificar_citacoes.py" --inventario CORPUS --output manifesto-corpus.jsonl
```

Manter `CORPUS` restrito às fontes de entrada e gravar a saída fora dele. O `manifesto-corpus.jsonl` registra caminho relativo, bytes, linhas e SHA-256. Ele prova a identidade e a integridade dos arquivos inventariados, não que tenham sido lidos.

Registrar a leitura em `leitura.jsonl`, uma linha por intervalo percorrido: `{"fonte":"P01.txt","inicio":1,"fim":240,"memo":"M01"}`. O auditor compara esses intervalos com o manifesto e devolve `integral` ou `parcial`. Declarar um intervalo que não foi lido é invenção de dado. Os intervalos e memos formam trilha processual auditável, não prova externa de cognição.

### Registro de evidências

Manter um único arquivo, `evidencias.jsonl`, com fontes, excertos, códigos, temas, hipóteses e dados não representados. O formato está em `referencias/evidencias-e-relato.md`. Regras:

1. Todo código nasce de um excerto já gravado no registro. Não codificar a partir de lembrança ou resumo.
2. Excerto `literal` exige fonte, localizador estável, janela de contexto e, quando houver, falante e a pergunta que provocou a fala.
3. Texto alterado é `parafrase`: não recebe aspas, não serve de âncora e não é evidência decisiva.
4. Excerto de nota de mediador ou de resumo de segunda mão recebe `voz: mediador` e é apresentado como registro de quem mediou.
5. Falante marcado `nao_atribuido` não vira indivíduo no relatório.
6. As tabelas de genealogia dos arquivos de fase são geradas do registro, não digitadas:

```text
python "<PASTA_DA_SKILL>/scripts/auditar_analise.py" tabelas --registro evidencias.jsonl --output genealogia.md
```

### Citações

Verificar os excertos literais a cada lote de codificação, não ao fim:

```text
python "<PASTA_DA_SKILL>/scripts/auditar_analise.py" citacoes --registro evidencias.jsonl --output citacoes.jsonl
python "<PASTA_DA_SKILL>/scripts/verificar_citacoes.py" --input citacoes.jsonl --base CORPUS --output verificacao-citacoes.jsonl
```

Para `.docx`, `.pdf`, áudio, legenda ou texto em outra codificação:

1. preservar o original sem alteração;
2. criar derivado textual UTF-8 sem limpar, resumir ou parafrasear o conteúdo;
3. registrar nome e SHA-256 do original e do derivado, método/versão de extração e correspondência de páginas, tempos ou unidades;
4. conferir amostras do início, meio e fim e cada excerto destinado à publicação contra o original;
5. verificar citações contra o derivado e manter também o localizador do original quando disponível.

Quando os derivados ficarem fora de `CORPUS`, inventariá-los separadamente como `manifesto-derivados.jsonl` com o mesmo comando `--inventario`. Se a extração ou sua correspondência não puder ser auditada, continuar a análise com evidência limitada, mas não publicar o excerto como literal verificado.

Publicar como literal somente `verified_exact`. Antes de aceitar `not_found`, percorrer três passos: (1) busca exata na fonte declarada; (2) `relocalizado`: busca normalizada em TODAS as fontes do corpus, pois a fonte declarada pode estar errada; (3) `substituir`: melhor trecho similar (similaridade >= 0.80), com `suggested_text` exato do corpus. `relocalizado` exige reescrever o excerto com `candidate_exact` e verificar de novo. `substituir` propõe **outro texto**: antes de aceitar, reler o trecho sugerido em contexto e confirmar que ele sustenta o mesmo código e a mesma afirmação; se não sustentar, descartar o excerto e rever o que dependia dele. Registrar cada correção. Tratar `exact_multiple_needs_locator`, `exact_locator_mismatch`, `not_found`, `source_missing`, `source_unreadable` e `invalid_record` como não verificados até correção. Se o script não puder ser executado, aplicar a mesma lógica manualmente e registrar evidência da busca.

### Auditoria computável

Rodar ao fim de F2, F5 e F6, corrigir os erros e repetir:

```text
python "<PASTA_DA_SKILL>/scripts/auditar_analise.py" integridade --registro evidencias.jsonl --verificacao verificacao-citacoes.jsonl --manifesto manifesto-corpus.jsonl --leitura leitura.jsonl --saida PASTA_DE_SAIDA --relatorio PASTA_DE_SAIDA/06-relatorio-final.md --templates "<PASTA_DA_SKILL>/templates" --output auditoria-integridade.json
```

Erros (`E..`) são falhas de trilha: citação do relatório fora do registro, paráfrase entre aspas, código órfão, código em dois temas sem justificativa, excerto não verificado, marcador de template esquecido. Alertas (`A..`) pedem leitura e resposta escrita: evidência concentrada em uma fonte, um falante ou um terço do corpus, contestação sem efeito estrutural, hipóteses intactas, contagens divergentes, citação sem comentário, frase copiada do template. Um alerta respondido com razão permanece no dossiê; um alerta ignorado é falha.

Códigos de saída: `integridade` devolve 1 quando há erros. `privacidade`, `sobrealegacao` e `homogeneizacao` devolvem 1 quando há itens a ler; não é falha de execução. Em todos, 2 indica entrada inválida.

O registro é cumulativo: uma hipótese gravada como `pendente` em F1 é atualizada no mesmo arquivo em F5, e códigos e temas abandonados mudam de estado em vez de serem apagados. `arquivo`, no registro, é o caminho da fonte como consta no campo `source` do manifesto.

O auditor confere a trilha. Não mede qualidade interpretativa e não substitui nenhum portão. O efeito “estrutural” é calculado do registro: mostra que o mapa mudou, não que a mudança foi bem fundamentada.

### Interações com IA

Em cada fase, registrar somente o necessário:

| ID | Fase/função | Ambiente/modelo | Objetivo e prompt sanitizado | Fontes por ID | Artefato | Verificação | Intervenção humana/efeito |
|---|---|---|---|---|---|---|---|

Não registrar raciocínio interno, credenciais, identificadores desnecessários ou conversa sensível integral. Quando modelo, versão ou parâmetro não estiver exposto, escrever “não informado pelo ambiente”.

### Contaminação

Registrar em F0, e atualizar quando acontecer, tudo o que chegou à análise antes do corpus: análise anterior do mesmo material, hipótese do usuário, enquadramento embutido no pedido, resultado de outro caso. Para cada item, dizer o que foi feito para não herdá-lo. A pergunta de pesquisa registrada em F0 vale para todas as fases; se mudar, registrar a mudança e o motivo.

### Estatuto da rival

Usar exatamente:

- **independente** — contexto ou sessão separada; recebe corpus, pergunta e F0, mas não o mapa principal nem conclusões;
- **informada** — vê o mapa principal ou trabalha no mesmo contexto;
- **ausente** — nenhuma contestação foi executada.

Se a separação não puder ser demonstrada, registrar `informada`. A falta de multiagência não bloqueia F0–F6, mas proíbe alegar rival independente. Quando houver outro modelo disponível, preferi-lo para a rival e registrar qual foi; modelo diferente reduz vocabulário compartilhado, não vira triangulação.

### Portões

Cada fase tem dois portões, registrados separadamente.

**Computado.** Resultado do auditor e dos verificadores: `PASS`, `FAIL` ou `N/A`, com o arquivo que comprova.

**Interpretativo.** Rubrica graduada de `referencias/rubrica-e-ancoras.md`, aplicada por um avaliador em contexto limpo que recebe os arquivos da fase e a rubrica, não o raciocínio de quem produziu. Para cada critério: `forte`, `adequado`, `frágil` ou `insuficiente`, com o trecho que justifica. O avaliador é obrigado a apontar o tema mais fraco e o problema mais grave da fase, mesmo quando tudo parecer adequado. `insuficiente` conta como `FAIL` substantivo.

Ao terminar cada fase:

1. rodar o portão computado e corrigir;
2. submeter ao portão interpretativo;
3. corrigir uma vez os problemas corrigíveis e registrar o que mudou;
4. continuar o fluxo autônomo mesmo com `FAIL`, produzindo diagnóstico ou entrega parcial;
5. impedir que qualquer `FAIL` substantivo coexista com “análise completa” ou “pronta para manuscrito”.

No perfil sequencial, os portões interpretativos são autoavaliações do mesmo sistema que produziu a fase: aplicar a rubrica em passe separado, lendo só os arquivos, e registrar `autoavaliação`. Um portão que nunca aponta problema não informa nada; desconfiar dele. Avaliação independente por outro agente não equivale a validação humana.

Não repetir uma fase indefinidamente. Uma limitação reconhecida não se converte automaticamente em aprovação.

## Funções analíticas

1. **Analista principal** — constrói códigos, mapa e narrativa.
2. **Analista rival** — constrói outro mapa a partir do corpus, com lente declarada e diferente da principal.
3. **Contestador** — escreve as condições de derrota de cada tema, caça contraevidência e aplica os testes de exclusão e fusão.
4. **Guardião experiencial** — localiza ambiguidades, contradições e perdas situadas.
5. **Avaliador de adequação** — recebe excerto, contexto e afirmação, e diz se o excerto sustenta, tensiona ou não se relaciona.
6. **Avaliador de portões** — aplica a rubrica e o checklist de relato.
7. **Integrador** — mantém, revisa, divide, funde ou abandona com razões explícitas.

No Essencial, contestador e guardião podem ser um só passe, a rival pode ser compacta e os arquivos de fase trazem só os campos que se aplicam ao caso; nenhum teste de F4 é dispensado. Na Aprofundada, cada função é um passe próprio. Em qualquer profundidade, analista principal e integrador não acumulam os papéis 2, 3, 5 e 6 no perfil isolado.

Realizar uma rodada adversarial completa e, quando necessário, uma revisão dirigida somente dos temas afetados.

## F0 — Constituição analítica

Preencher `templates/fase-0-decisoes/decisoes-metodologicas.md`.

Definir pergunta, escopo, posição epistemológica, eixos, unidade, rota, profundidade, perfil, nível de literatura, cobertura, ética e privacidade. Registrar estatuto das fontes, contaminação, matriz de delegação F0–F6, ambiente/modelo, parâmetros expostos, alinhamento entre capacidades da IA e posição metodológica, mapa humano e plano de verificação.

**Saídas:** `00-constituicao-analitica.md`, `manifesto-corpus.jsonl` quando houver arquivos locais e `aptidao.json` quando o teste for feito.

**Portão:** `PASS` somente quando decisões, lacunas, riscos e limites de alegação estiverem explícitos. Consentimento desconhecido bloqueia alegações de aprovação ética, não a descrição analítica autorizada pelo usuário.

## F1 — Familiarização

Preencher `templates/fase-1-familiarizacao/notas-de-familiarizacao.md`.

Ler todas as fontes acessíveis. Produzir memos por fonte ou lote, síntese transversal e memo reflexivo com tensões, mudanças de posição, expressões situadas e perguntas. Gravar `leitura.jsonl`.

Registrar no registro de evidências, como `hipotese`, o que a leitura faz esperar encontrar. Hipótese não é tema: não nomear temas nem esboçar o mapa final nesta fase. Em F5, cada hipótese recebe destino (`mantida`, `revista`, `derrubada`) com evidência.

**Saídas:** `01-familiarizacao.md`, `leitura.jsonl`.

**Portão:** `PASS` somente quando o auditor devolver cobertura `integral`. Cobertura `parcial` exige `FAIL` para integralidade e delimitação explícita do subconjunto.

## F2 — Codificação reflexiva

Preencher `templates/fase-2-codigos/codificacao-reflexiva.md`.

Codificar todo material relevante, permitindo múltiplos códigos por excerto e revisão durante o processo. Gravar primeiro o excerto, verificar, depois codificar. Para cada código, registrar rótulo, excertos, nota interpretativa, origem e mudanças. Distinguir códigos humanos, gerados, revisados e recusados. Rótulo que repete uma pergunta do instrumento de coleta ou cabe em quase qualquer fala volta para os excertos.

No perfil isolado, o analista rival codifica o corpus em paralelo, em contexto limpo e com outra lente, gravando `rival/evidencias.jsonl`.

**Saídas:** `02-codificacao-reflexiva.md`, `evidencias.jsonl`, `citacoes.jsonl`, `verificacao-citacoes.jsonl`.

**Portão:** `PASS` computado somente com todos os excertos literais `verified_exact` e sem erro de registro.

## F3 — Temas candidatos

Preencher `templates/fase-3-temas/temas-candidatos.md`.

Construir padrões de significado compartilhado. Para cada tema candidato, explicitar conceito organizador, afirmação, evidências, fronteiras, variação e tensões, e declarar a aposta: o que precisa ser verdade no corpus para o tema se sustentar. Não finalizar a primeira solução. No perfil isolado, o analista rival constrói seu próprio mapa candidato sem ver este.

**Saída:** `03-temas-candidatos.md` e, no perfil isolado, `rival/03-temas-candidatos.md`.

**Portão:** nenhum tema `insuficiente` no critério “padrão de significado”. Tema classificado como resumo de tópico volta para reconstrução antes de F4.

## F4 — Contestação e revisão

Preencher `templates/fase-4-revisao/revisao-temas.md`.

1. **Mapa rival.** Comparar o mapa principal com o mapa do analista rival, argumento contra argumento, sem votação.
2. **Condições de derrota.** O contestador, não o autor do tema, escreve o que faria cada tema cair, perder a fronteira ou ser absorvido, antes de reler as evidências.
3. **Caça à contraevidência.** Buscar no corpus os excertos que mais tensionam cada tema e gravá-los no registro. Quando nada for encontrado, registrar onde e como se procurou.
4. **Teste de exclusão.** Reescrever a resposta à pergunta sem o tema. Se nada substantivo se perde, o tema cai ou é absorvido.
5. **Teste de fusão.** Para cada par vizinho, dizer com excertos o que se perderia ao fundir. Se nada se perde, fundir.
6. **Releitura contra o mapa.** Voltar ao corpus com o mapa revisado e gravar como `nao_representado` o que ele deixa de fora. Trecho que já sustenta um tema não entra nessa lista.
7. **Decisão do integrador.** Manter, revisar, dividir, fundir ou abandonar, com razões.

Não há número mínimo de temas. Acima de oito, o auditor alerta: conferir se há resumos de tópico ou fronteiras frágeis e justificar o que ficar. Fundir para caber em um número, sem conceito organizador que una os temas, é proibido.

O auditor calcula a diferença entre candidatos e finais. Quando só nomes mudaram, a fase fica rotulada **“contestação sem efeito estrutural”**, e o rótulo vai ao estatuto final. Não é falha automática: é a informação de que a contestação não mudou o mapa.

**Saída:** `04-contestacao-e-revisao.md`.

**Portão:** `PASS` somente quando houver rival material, condição de derrota, contraevidência, exclusão e fusão registradas e mudança ou recusa justificada. Contestação `ausente` é `FAIL`; contestação `informada` pode passar, mas não virar independente.

## F5 — Temas finais e passaportes

Preencher `templates/fase-5-definicao/definicao-temas-finais.md`.

Para cada tema, registrar nome, conceito organizador, afirmação, história, genealogia gerada do registro, excertos-âncora verificados, excertos que o tensionam, rival, evidência decisiva, resíduo, decisão, incerteza, estatuto da rival e participação humana. Dar destino a cada hipótese de F1.

Submeter cada par excerto–afirmação ao avaliador de adequação. `não se relaciona` exige trocar o excerto ou reescrever a afirmação; `tensiona` exige tratar a tensão no texto.

**Saídas:** `05-temas-finais-e-passaportes.md`, `genealogia.md`, registro e verificações atualizados.

**Portão:** `PASS` somente quando cada tema for coerente, distinto, contestável e sustentado por evidência verificada e adequada. Não usar percentuais de confiança.

## F6 — Relato

Produzir dois arquivos, com `templates/fase-6-relatorio/relatorio-final.md` e `templates/fase-6-relatorio/dossie-de-auditoria.md`.

1. **`06-relatorio-final.md`** — o texto analítico: pergunta, método em poucas linhas, visão sinóptica dos temas, um argumento por tema, relações, o que a análise não pode afirmar e, conforme o nível escolhido, diálogo com a literatura.
2. **`07-dossie-de-auditoria.md`** — passaportes, manifesto de IA, delegação, interações, mapa humano, cobertura, verificação, adequação, portões, alertas respondidos e decisões adversariais.

Regras do relatório, detalhadas em `referencias/evidencias-e-relato.md`:

- cada tema segue o movimento afirmação, excerto, o que o excerto faz, variação ou tensão, resposta à pergunta;
- nenhuma citação fica sem comentário, e nenhuma citação aparece fora do registro;
- uma tabela ou mapa apresenta os temas e suas relações antes do desenvolvimento;
- rodar `auditar_analise.py sobrealegacao --relatorio 06-relatorio-final.md --output sobrealegacao.json` e responder a cada item: manter com evidência, restringir ou cortar;
- o avaliador de portões aplica o checklist de relato.

Markdown é obrigatório. Produzir DOCX ou outro formato quando solicitado e suportado; a indisponibilidade de formato adicional não muda o estatuto metodológico.

**Pacote de saída.** Entregar juntos, na mesma pasta: os arquivos `00` a `07`, `evidencias.jsonl`, `genealogia.md`, `citacoes.jsonl`, `verificacao-citacoes.jsonl`, `manifesto-corpus.jsonl`, `leitura.jsonl`, `auditoria-integridade.json`, `privacidade.json`, `sobrealegacao.json` e, quando existirem, `manifesto-derivados.jsonl`, `aptidao.json` e a pasta `rival/`. Registrar `N/A` no dossiê para o que não se aplicar. Sem esses arquivos, a verificação não pode ser refeita por terceiros.

**Portão:** `PASS` somente quando o texto estiver alinhado a F0, o auditor não devolver erros e nenhum estatuto exceder o trabalho realizado.

## Casos múltiplos

Quando o corpus reunir casos comparáveis (cidades, grupos, instituições), ler `referencias/casos-multiplos.md` e:

1. analisar cada caso em contexto próprio, sem acesso aos demais nem aos seus resultados;
2. não reutilizar entre casos nomes de tema, conceitos organizadores ou parágrafos;
3. exigir de cada caso a seção “o que só existe aqui”, ou a declaração fundamentada de que nada é específico;
4. fazer a síntese comparativa como fase separada, depois de todos os casos, com `templates/casos-multiplos/sintese-comparativa.md`;
5. rodar `auditar_analise.py homogeneizacao` sobre os relatórios dos casos e reler os pares em alerta.

No perfil sequencial, o isolamento entre casos não pode ser demonstrado: declarar isso e tratar a semelhança entre casos como suspeita até ser explicada pelos dados.

## Estatuto final

Declarar separadamente:

- **Fluxo:** F0–F6 executado ou interrompido.
- **Perfil:** isolado ou sequencial.
- **Aptidão:** apto, parcial, inapto ou N/A.
- **Cobertura:** integral, parcial ou indeterminada.
- **Evidências:** verificáveis, limitadas ou inválidas.
- **Contestação:** independente, informada ou ausente; com efeito estrutural ou sem efeito estrutural.
- **Avaliação dos portões:** independente ou autoavaliação.
- **Privacidade:** decidida pelo usuário, padrão aplicado e pendente de confirmação, ou não aplicável.
- **Participação humana:** mapa por fase.
- **Validação humana:** realizada, parcial ou ausente.
- **Prontidão:** manuscrito, exploração ou auditoria.

Usar “ATR autônoma completa” somente se todo o corpus declarado e acessível tiver sido tratado e todos os portões substantivos tiverem `PASS`. A validação humana pode permanecer ausente:

> ATR autônoma completa no escopo declarado e auditável; redação pronta para incorporação em manuscrito; sem validação humana.

Não prometer verdade, publicação, equivalência humana ou aprovação ética.

## Checklist final

- [ ] Inventário, leitura e cobertura foram reconciliados pelo auditor.
- [ ] Todo excerto literal está `verified_exact` e toda citação do relatório está no registro.
- [ ] Códigos e temas mantêm genealogia até a fonte, gerada do registro.
- [ ] Temas possuem conceito organizador e respondem à pergunta.
- [ ] Rival, condições de derrota, contraevidência, exclusão e fusão foram tratadas.
- [ ] O efeito da contestação foi calculado e declarado.
- [ ] Cada par excerto–afirmação passou pela checagem de adequação.
- [ ] Cada hipótese de familiarização recebeu destino.
- [ ] Portões computados e interpretativos estão separados, com avaliador identificado.
- [ ] A lista de privacidade foi mostrada ao usuário ou o padrão foi aplicado e declarado.
- [ ] Relatório e dossiê estão em arquivos separados e o pacote de saída está completo.
- [ ] O estatuto final corresponde ao trabalho realizado.
