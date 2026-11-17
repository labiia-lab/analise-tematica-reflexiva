# Notas de versão

## 2.0.0 — 2026-11-16

Esta versão responde a uma avaliação das análises que a skill vinha produzindo. O diagnóstico: a trilha de auditoria era boa, mas a interpretação ficava aquém. Temas repetiam o roteiro de coleta, a contestação quase nunca mudava o mapa, o relatório citava trechos fora do conjunto verificado, os portões eram aprovados pelo mesmo sistema que produzia a fase e, em estudos com vários casos, os relatórios saíam com a mesma arquitetura.

A causa comum era um único contexto construir, contestar e aprovar. A versão 2.0.0 separa esses papéis, passa a conferir por script o que não depende de interpretação e muda o que se entrega.

### O que muda para quem usa

- **A análise pode chegar a menos temas.** Não há mais número mínimo. Dois temas densos são um resultado válido.
- **A entrega tem dois textos.** `06-relatorio-final.md` é o relatório analítico; `07-dossie-de-auditoria.md` reúne passaportes, registros e portões.
- **O estatuto final ficou mais informativo.** Passa a dizer o perfil de execução, se a contestação mudou o mapa, quem avaliou os portões e como a privacidade foi decidida.
- **A skill pergunta antes de entregar** quando encontra possíveis identificadores pessoais na saída.
- **Rodar a skill exige mais passos** e, onde o ambiente permitir, mais de um contexto de execução.

### Contestação

- O analista rival constrói o próprio mapa a partir do corpus, em contexto limpo e com outra lente, em vez de comentar o mapa principal. Quando houver outro modelo disponível, a rival roda nele.
- As condições de derrota de cada tema são escritas por quem contesta, antes de reler as evidências.
- Entram a caça à contraevidência, o teste de exclusão por tema e o teste de fusão por par de temas.
- O corpus é relido contra o mapa revisado; o que já sustenta um tema não pode constar como “não representado”.
- A regra de 4 a 8 temas foi retirada. Acima de oito há um alerta; fundir temas para atingir um número é proibido.
- O script calcula a diferença entre temas candidatos e finais. Se só nomes mudaram, a fase é rotulada “contestação sem efeito estrutural”.

### Relatório

- Relatório analítico separado do dossiê de auditoria.
- Cada tema segue o movimento afirmação, excerto, o que o excerto faz, variação ou tensão, resposta à pergunta.
- Nenhuma citação sem comentário; o script acusa citações seguidas e temas apoiados em uma só fonte.
- Literatura em três níveis, escolhidos no início: nenhuma, só a fornecida pelo usuário ou busca conferida. Referência de memória não entra em nenhum.
- Visão sinóptica dos temas obrigatória e seção “o que esta análise não pode afirmar”.
- Verificador de sobrealegação: generalizações, causalidade, contagens e vocabulário de outras tradições recebem resposta escrita.
- Checklist de relato aplicado por avaliador independente.

### Evidências

- Registro único, `evidencias.jsonl`, liga fonte, excerto, código e tema. As tabelas de genealogia passam a ser geradas dele.
- Todo código nasce de um excerto já gravado e verificado; a verificação acontece a cada lote, não ao fim.
- Cada fonte tem estatuto declarado. Nota de moderador e resumo de segunda mão são registro de quem mediou e não podem ser citados como fala.
- Excerto literal exige localizador estável e janela de contexto. Paráfrase tem formato próprio e não sustenta âncora nem evidência decisiva.
- Checagem de adequação: um avaliador recebe só o excerto, o contexto e a afirmação e diz se sustenta, tensiona ou não se relaciona.
- Matriz de distribuição da evidência por fonte, por falante e por posição no corpus.
- Ao aceitar a substituição de uma citação por trecho similar, a adequação é reavaliada.
- O pacote de saída inclui os arquivos de verificação, para que terceiros possam refazê-la.

### Portões de qualidade

- Cada fase tem um portão computado, a cargo do script, e um interpretativo, a cargo de um avaliador em contexto limpo.
- O portão interpretativo usa rubrica graduada, com trecho de evidência por critério e ranking forçado: tema mais fraco, problema mais grave, afirmação mais exposta.
- Cada tema é classificado como padrão de significado, misto ou resumo de tópico.
- Âncoras contrastivas ficcionais calibram a rubrica, e há um roteiro de regressão por rubrica.
- Conferência de identificadores pessoais na pasta de saída. O resultado é mostrado ao usuário, que decide.

### Modelos, leitura e casos múltiplos

- Teste de aptidão antes de começar: citação literal, tema ou tópico, citação alterada.
- Dois perfis de execução. No isolado, rival e avaliadores trabalham em contextos limpos. No sequencial, a rival é `informada` e os portões são `autoavaliação`.
- Andaime reforçado para modelos com aptidão parcial: lotes menores, memo por fonte, excerto antes do código.
- Leitura conferida: os intervalos lidos são comparados com o inventário do corpus.
- Em estudos com vários casos, cada caso é analisado em contexto próprio, traz a seção “o que só existe aqui”, e a síntese comparativa é uma fase separada.
- Detector de semelhança entre relatórios de casos.
- Hipóteses da familiarização são registradas e recebem destino ao fim; o script alerta quando nenhuma foi revista.
- Registro de contaminação: análises anteriores, hipóteses do usuário e enquadramentos do pedido.
- Templates reescritos como roteiros de campos, sem os exemplos prontos que apareciam copiados nas saídas. O script acusa marcadores esquecidos e frases copiadas do template.

### Arquivos

- Novos: `scripts/auditar_analise.py`, `scripts/aptidao/`, `referencias/execucao-e-isolamento.md`, `referencias/evidencias-e-relato.md`, `referencias/rubrica-e-ancoras.md`, `referencias/casos-multiplos.md`, `templates/fase-6-relatorio/dossie-de-auditoria.md`, `templates/casos-multiplos/sintese-comparativa.md`, sete cenários comportamentais (22 a 28) e `testes/test_auditar_analise.py`.
- Reescritos: `SKILL.md` e os sete templates de fase.
- Atualizados: as demais referências, `scripts/verificar_citacoes.py`, `testes/TESTES.md` e os testes de integridade.

### Incompatibilidades

- Saídas de versões anteriores não têm `evidencias.jsonl` nem `leitura.jsonl`; o auditor não se aplica a elas sem reconstruir o registro.
- O apêndice auditável deixou de fazer parte de `06-relatorio-final.md`.
- A seção “Exemplo curto” foi removida dos templates. O exemplo integrado permanece como ilustração de raciocínio e não reproduz os controles desta versão.

### Limites conhecidos

- A versão foi verificada por testes automatizados do script, por um ensaio com corpus fictício mínimo e por uma execução curta, em perfil sequencial e profundidade Essencial, sobre cinco resumos de artigos. Ainda não foi executada no perfil isolado, sobre corpus de entrevistas ou com casos múltiplos, nem comparada por rubrica com as execuções anteriores.
- O auditor confere a trilha, não a qualidade interpretativa. O rótulo de efeito “estrutural” da contestação mostra que o mapa mudou, não que a mudança foi bem fundamentada; isso cabe ao avaliador. A lista de possíveis nomes próprios e a de sobrealegação geram falsos positivos por desenho: pedem leitura, não aceitação automática.
- As âncoras da rubrica são ficcionais. Análises reais usadas no diagnóstico não foram incluídas no repositório por conterem dados de participantes.
- O checklist de relato adapta critérios de Braun e Clarke a partir de fichamentos; conferir a fonte primária antes de citá-lo em manuscrito.
- No perfil sequencial, a separação de papéis é reduzida a passes distintos e não pode ser demonstrada.

## 1.x — até 2026-08-25

Versões anteriores, sem notas de versão. Histórico disponível nos commits.
