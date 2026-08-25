---
name: analise-tematica-reflexiva
description: Use esta skill sempre que o usuario precisar realizar Analise Tematica Reflexiva (ATR) sobre dados qualitativos. Acione quando mencionar analise tematica, temas, codificacao qualitativa, entrevistas, grupos focais, documentos, categorias analiticas, mapa tematico, codebook, Braun e Clarke, reflexive thematic analysis, RTA ou trustworthiness. Conduz uma ATR completa em 7 fases obrigatorias (0-6), com verificacao literal de extratos, reflexividade, auditoria de frequencia, visualizacoes e trilha de auditoria.
---

# Analise Tematica Reflexiva (ATR)

> Licenca do repositorio: Creative Commons Attribution 4.0 International (CC BY 4.0). Veja `LICENSE`.

## Regra de Execucao

Execute ATR como pesquisa qualitativa interpretativa, nao como resumo automatizado. Temas sao construidos pelo analista a partir de padroes de significado compartilhado; eles nao "emergem" mecanicamente dos dados.

O agente de IA deve usar sua propria capacidade de linguagem para ler, comparar, interpretar, contrastar e propor codigos/temas. Scripts e frequencias entram como auditoria e visualizacao depois da interpretacao inicial, nunca como substituto da leitura qualitativa.

## Contrato de Profundidade

Quando o usuario pedir "analise completa", "AT completa", "ATR completa" ou equivalente, use sempre o modo `analise_completa`. Nao trate como teste rapido de pipeline.

No modo `analise_completa`, cada fase substantiva deve gerar texto amplo, profundo e auditavel. Regra simples para o agente: cada fase deve ter pelo menos 2.000 palavras, salvo corpus muito pequeno ou instrucao explicita do usuario para resumir. Se a fase ficar abaixo disso, explique a razao metodologica e marque o checkpoint como `NAO PASSOU` ate complementar.

Cada fase deve mostrar detalhadamente o que foi feito passo a passo:
- quais arquivos/fontes foram lidos;
- quais decisoes analiticas foram tomadas;
- quais extratos sustentam a decisao;
- quais alternativas foram consideradas e rejeitadas;
- quais dados divergentes, ambiguos ou pouco encaixados foram discutidos;
- o que o pesquisador humano deve revisar criticamente.

Inclua em todas as fases uma secao chamada `Auditoria de profundidade da fase`, com contagem aproximada de palavras, fontes usadas, numero de extratos citados/verificados, cobertura por fonte/participante, tensoes encontradas e pontos para revisao humana.

Use `modo teste_rapido` apenas se o usuario pedir explicitamente piloto, rascunho, smoke test, exemplo curto ou validacao de pipeline. Nesse caso, declare que a saida nao e ATR completa substantiva.

## Carregamento Obrigatorio

Para uma ATR completa, leia e siga estes arquivos antes de iniciar o trabalho. Nao trate como material opcional.

**Referencias metodologicas obrigatorias:**
- `referencias/hierarquia-analitica.md` - diferenca entre codigo, categoria, subtema e tema.
- `referencias/qualidade-dos-codigos.md` - criterios para bons codigos e revisao de codigos vagos.
- `referencias/construcao-de-temas.md` - tema genuino vs. resumo de dominio.
- `referencias/confiabilidade.md` - credibilidade, dependabilidade, confirmabilidade e transferibilidade.
- `referencias/visualizacoes.md` - regras de data viz, Graphviz/DOT, frequencia e exportacao.

**Templates obrigatorios, por fase:**
- `templates/fase-0-decisoes/decisoes-metodologicas.md`
- `templates/fase-1-familiarizacao/notas-de-familiarizacao.md`
- `templates/fase-2-codigos/codebook-inicial.md`
- `templates/fase-3-temas/temas-candidatos.md`
- `templates/fase-4-revisao/revisao-temas.md`
- `templates/fase-5-definicao/definicao-temas-finais.md`
- `templates/fase-6-relatorio/relatorio-final.md`

**Scripts obrigatorios quando gerar artefatos:**
- `scripts/gerar_diagramas.py` - biblioteca unica de diagramas, verificacao de citacoes e frequencia.
- `scripts/gerar_saida_final.py` - wrapper simples para gerar outputs a partir de JSON da analise.

**Testes e criterios adversariais:**
- `testes/TESTES.md` - cenarios de falha metodologica.
- `testes/test_scripts.py` - testes executaveis dos scripts.

## Regra de Ouro dos Extratos

Todo extrato citado deve cumprir os quatro criterios:

1. Ser transcricao literal do dado original, sem parafrase.
2. Trazer localizacao precisa: fonte, pagina/linha/ID quando disponivel.
3. Aparecer entre aspas como citacao direta.
4. Ser verificavel contra o corpus.

Use `verificar_citacoes()` em `scripts/gerar_diagramas.py` quando houver corpus textual disponivel. Aceite como validos por correspondencia exata os status `verificado` e `relocalizado`; `substituir` tambem vale, desde que a citacao seja substituida pelo `trecho_correspondente` exato do corpus e a verificacao seja repercorrida, com a substituicao registrada na trilha de auditoria. Antes de declarar `nao_encontrado`, execute os tres passos: (1) busca exata na fonte declarada; (2) busca normalizada (caixa, espacos, quebras e prefixos de locutor) em TODAS as fontes - a fonte declarada pode estar errada e o trecho pode estar em outro arquivo; (3) busca do melhor trecho similar, substituindo a citacao pelo trecho exato sugerido. Somente depois desses tres passos o extrato e `nao_encontrado`. Resultado `parcial` ou `nao_encontrado` (apos os tres passos) nao passa checkpoint.

Se o agente nao tiver acesso ao dado original, escreva exatamente: `[Extrato reconstruido da memoria - requer verificacao contra o original]`. Qualquer fase com extrato reconstruido nao pode ser marcada como concluida.

## Papel do Agente e do Pesquisador

**Agente propoe:** codigos, nomes, interpretacoes, alternativas, visualizacoes, revisoes.

**Pesquisador decide:** marco epistemologico, aceitacao de codigos/temas, nomes finais, encerramento da analise, uso de interpretacoes.

**Agente bloqueia:** pular fase, codificar sem familiarizacao, aceitar codigos vagos, aceitar resumos de dominio como temas, descartar dados divergentes, usar frequencia como importancia automatica, citar extratos nao verificados.

Declare no relatorio final que IA generativa foi usada e descreva seus riscos: tendencia a coerencia excessiva, generalizacao, suavizacao de contradicoes e preferencia por narrativas elegantes.

## Workflow Obrigatorio

Use as fases abaixo em ordem. O processo e recursivo: se uma fase posterior revelar problema anterior, volte, documente e refaca a etapa afetada.

### Fase 0 - Decisoes Metodologicas

Antes de ler/codificar os dados, preencha `templates/fase-0-decisoes/decisoes-metodologicas.md`.

Documente:
- tipo de AT: Reflexiva, Codebook ou Confiabilidade de Codificacao. Se for Confiabilidade, esta skill nao se aplica como metodo principal.
- marco epistemologico: essencialista, construtivista, critico ou outro.
- orientacao analitica: descritiva, explanatoria ou interpretativa.
- nivel de codificacao: semantico, latente ou ambos.
- tipo de dado: texto pronto, transcricao necessaria, documento, diario, grupo focal etc.
- questao de pesquisa.
- escala do corpus e estrategia de leitura.
- decisoes de transcricao, se houver audio/video.

Checkpoint: nao avance para Fase 1 sem todas as decisoes registradas.

Profundidade minima: em analise completa, registre tambem a auditoria de profundidade da fase. Se as decisoes metodologicas forem curtas por natureza, justifique; isso nao autoriza encurtar as fases analiticas posteriores.

### Fase 1 - Familiarizacao

Leia todo o corpus antes de codificar. Familiarizacao nao e a mesma coisa que ter conduzido entrevistas.

Preencha `templates/fase-1-familiarizacao/notas-de-familiarizacao.md` com observacoes, surpresas, perguntas, passagens relevantes e reflexividade. Nao gere codigos nesta fase.

Checkpoint: corpus lido, notas produzidas, passagens destacadas, reflexividade registrada.

Profundidade minima: em analise completa, `01-notas-familiarizacao.md` deve ter pelo menos 2.000 palavras. Para corpus com varias entrevistas/documentos, escreva um memo substantivo por fonte, normalmente 300-500 palavras por entrevista/documento, alem de uma sintese transversal. Inclua `Auditoria de profundidade da fase`.

### Fase 2 - Codificacao Inicial

Leia `referencias/qualidade-dos-codigos.md` e preencha `templates/fase-2-codigos/codebook-inicial.md`.

Codifique o corpus inteiro de forma sistematica. Um bom codigo e breve, mas autossuficiente; informa uma comunalidade; tem limites claros; nao e vago; nao e intercambiavel com outros codigos.

Codificacao In Vivo e permitida e muitas vezes desejavel quando a linguagem do participante carrega significado cultural, afetivo ou politico. Nao force In Vivo em todos os casos.

Depois da primeira codificacao interpretativa, faca auditoria de frequencia:
- Use a propria leitura LLM para codificar antes de calcular frequencias.
- Use `calcular_frequencia_codigos()` ou `gerar_tabela_frequencia_markdown()` em `scripts/gerar_diagramas.py`.
- Use frequencia para checar cobertura, lacunas, codigos amplos demais, codigos raros que merecem memo e distribuicao por fonte.
- Nunca use frequencia como criterio automatico de importancia, descarte ou promocao a tema.

Checkpoint: corpus inteiro codificado, codebook com definicoes, extratos literais verificados, codigos ambiguos documentados, frequencia auditada e dados divergentes codificados.

Profundidade minima: em analise completa, `02-codebook-inicial.md` deve ter pelo menos 2.000 palavras. Cada codigo principal precisa de definicao, criterios de inclusao, criterios de exclusao, 2-3 extratos literais, tensoes com codigos vizinhos e notas interpretativas. Inclua matriz de cobertura por fonte/participante e `Auditoria de profundidade da fase`.

### Fase 3 - Construcao de Temas Candidatos

Leia `referencias/hierarquia-analitica.md` e `referencias/construcao-de-temas.md`. Preencha `templates/fase-3-temas/temas-candidatos.md`.

Agrupe codigos em categorias e temas por significado compartilhado, nao por topico. Estrutura recomendada: Tema -> Subtema -> Categoria -> Codigo.

Crie "Miscelanea" para codigos ainda sem encaixe. Nao descarte codigo por baixa frequencia ou falta de elegancia narrativa.

Checkpoint: todos os codigos revisados, categorias intermediarias criadas, temas candidatos com conceito organizador, mapa tematico inicial produzido.

Profundidade minima: em analise completa, `03-temas-candidatos.md` deve ter pelo menos 2.000 palavras. Para cada tema candidato, explique conceito organizador, por que os codigos foram agrupados, quais agrupamentos alternativos foram rejeitados, quais extratos sustentam o tema, quais extratos tensionam o tema e como o tema responde a questao de pesquisa. Inclua `Auditoria de profundidade da fase`.

### Fase 4 - Revisao e Refinamento

Preencha `templates/fase-4-revisao/revisao-temas.md`.

Nivel 1: releia todos os extratos de cada tema e avalie coerencia interna.

Nivel 2: releia o dataset contra o mapa tematico e avalie se o mapa representa adequadamente os significados do corpus.

Para cada tema, aplique Devil's Advocate:
- Qual extrato menos se encaixa?
- O que precisaria ser verdadeiro para este tema estar errado?
- Se remover o tema, a analise ainda faz sentido? Se sim, talvez seja resumo de dominio.
- O tema integra tensoes e variacoes ou as esconde?

Dados divergentes devem ser interpretados dentro dos temas que tensionam ou usados para reformular o mapa. Nao crie um tema "outliers" sem interpretacao substantiva.

Regra de orcamento tematico (obrigatoria): a analise deve convergir para 4-8 temas finais. Nunca abaixo de 4. Acima de 8, apenas com boa justificativa explicita. Se houver 10 ou mais temas, tentar agregar da maneira mais substantiva possivel para chegar a 8 ou menos - agrupando por significado compartilhado, e nao por contagem ou conveniencia.
Checkpoint: homogeneidade interna, heterogeneidade externa, revisao contra dataset, anti-extratos e mudancas documentadas.

Profundidade minima: em analise completa, `04-revisao-temas.md` deve ter pelo menos 2.000 palavras. Para cada tema, documente revisao interna, revisao contra o dataset, anti-extratos, casos divergentes, condicao de falsificacao, limiar de colapso e decisao de manter, dividir, fundir ou reformular. Inclua `Auditoria de profundidade da fase`.

### Fase 5 - Definicao e Nomeacao

Preencha `templates/fase-5-definicao/definicao-temas-finais.md`.

Para cada tema, escreva 2-3 frases com a essencia, o conceito organizador, os limites e a historia analitica. Nomear tema e ato analitico: evite "Tipos de...", "Beneficios de...", "Barreiras para...", palavras unicas e reflexos do roteiro.

Documente relacoes entre temas: sequencial, complementar, tensao ou hierarquica.

Checkpoint: temas definidos, nomes interpretativos, extratos verificados, relacoes documentadas, decisoes humanas registradas.

Profundidade minima: em analise completa, `05-definicao-temas.md` deve ter pelo menos 2.000 palavras. A definicao curta de 2-3 frases e obrigatoria, mas nao substitui a analise longa. Cada tema final deve ter historia interpretativa, limites, relacao com outros temas, 4-6 extratos literais interpretados, variacoes entre fontes e dado divergente discutido. Inclua `Auditoria de profundidade da fase`.

### Fase 6 - Relatorio Analitico

Preencha `templates/fase-6-relatorio/relatorio-final.md`.

O relatorio deve contar uma historia analitica coerente em relacao a questao de pesquisa. Inclua extratos suficientes, interpretacao, variacao, contradicoes, mapa final, trilha de auditoria, confiabilidade e declaracao de IA.

Leia `referencias/confiabilidade.md` antes de escrever a secao de qualidade.

Checkpoint: narrativa integradora, metodologia, confiabilidade, limites, uso de IA, codebook e anexos finalizados.

Profundidade minima: em analise completa, `06-relatorio-final.md` deve ter pelo menos 2.000 palavras. Para corpus medio ou grande, o relatorio deve ser maior; cada tema final deve ter desenvolvimento analitico robusto, preferencialmente 1.200-2.000 palavras por tema quando o corpus permitir, com 4-6 extratos literais interpretados, comparacao entre participantes/fontes, dado divergente e implicacao analitica. Inclua `Auditoria de profundidade final`.

## Visualizacoes e Scripts

Use `referencias/visualizacoes.md` antes de gerar graficos.

Padrao simples para agentes:

1. Produza Markdown renderizavel:
   - Graphviz/DOT para mapas hierarquicos.
   - Infographic/infocard para resumo de fases.
   - Tabela Markdown para auditoria de frequencia.
2. Produza SVG/PNG para DOCX:
   - `gerar_mapa_tematico()`
   - `gerar_diagrama_evolucao()`
   - `gerar_diagrama_relacoes()`
   - `gerar_diagrama_trajetoria()`
   - `gerar_mapa_final()`
3. Gere documentos com `gerar_saida_final.py` a partir de JSON externo. Nao coloque dados reais dentro dos scripts.

Data viz deve ser explicativa, nao decorativa: titulos claros, paleta segura para daltonismo, labels diretos, sem 3D, sem grafico de pizza, sem gradiente ornamental, sem barras que sugiram importancia analitica por frequencia.

## Terminologia Correta

Use:
- "temas foram construidos/gerados"
- "a analise identificou"
- "o mapa tematico foi refinado"
- "dados divergentes tensionam o tema"

Nao use:
- "temas emergiram"
- "os dados revelaram"
- "descobri temas"
- "outliers foram descartados"

## Bloqueios Obrigatorios

Bloqueie a progressao quando ocorrer:
- tentativa de saltar familiarizacao.
- ausencia de decisoes da Fase 0.
- codigo vago ou sem limites.
- tema candidato que e resumo de dominio.
- extrato citado sem verificacao literal.
- descarte de dado divergente por inconveniencia.
- remocao de codigo por baixa frequencia.
- relatorio sem contradicoes, limitacoes ou declaracao de IA.
- fase de analise completa com texto curto, sem auditoria de profundidade ou com menos de 2.000 palavras sem justificativa.
- arquivo criado, mas sem trabalho interpretativo suficiente para auditoria humana.
- teste rapido apresentado como ATR completa.

Use linguagem direta: "Nao e possivel avancar"; "O checkpoint nao passou"; "Esta fase precisa ser refeita".

## Validacao

Antes de devolver trabalho final:

1. Rode `python -m py_compile scripts/gerar_diagramas.py scripts/gerar_saida_final.py`.
2. Rode `python -m unittest testes.test_scripts`.
3. Se estiver usando esta skill dentro de um ecossistema que ofereca um validador proprio de skills, rode tambem a validacao nativa do seu ambiente.
4. Confirme que nao ha outputs gerados, `__pycache__` ou dados reais hardcoded dentro de `scripts/`.
