# Qualidade analítica em ATR

## Sumário

1. Três camadas de qualidade
2. Códigos
3. Temas
4. Rigor e auditabilidade
5. Erros recorrentes
6. Gates por fase
7. Auditoria final

## 1. Três camadas de qualidade

Avaliar cumulativamente:

1. **Fidelidade à ATR:** pesquisador ativo, recursividade, coerência epistemológica e temas construídos.
2. **Qualidade analítica:** riqueza interpretativa, conceito organizador, coerência, distinção, complexidade e narrativa.
3. **Qualificação da IA:** rastreabilidade, contestabilidade e conservação experiencial.

A terceira camada não corrige falhas nas duas primeiras. Uma análise superficial com boa documentação continua superficial.

## 2. Códigos

Um código útil:

- nomeia algo específico;
- esclarece o aspecto do excerto que importa;
- permanece ligado à fonte;
- pode ser revisado;
- distingue descrição e interpretação quando necessário;
- evita julgamento moral não sustentado.

### Diagnóstico de vaguidade

Perguntar:

- o código poderia ser aplicado a quase qualquer fala?
- ele apenas repete o tópico da pergunta?
- é possível explicar por que este excerto recebeu o código?
- dois códigos vizinhos têm diferença analítica clara?
- o código depende de contexto que não foi registrado?

Não exigir:

- mínimo de ocorrências;
- estabilidade entre rodadas;
- critérios rígidos de inclusão e exclusão;
- uma única aplicação correta;
- distribuição uniforme por fonte.

Um código de ocorrência única pode preservar uma contradição decisiva. Um código frequente pode ser banal.

## 3. Temas

Um tema forte:

- responde à pergunta;
- tem conceito organizador central;
- produz uma afirmação, não apenas um título;
- reúne excertos por significado compartilhado;
- apresenta coerência sem apagar variação;
- é distinto dos demais;
- possui escopo manejável;
- contribui para uma narrativa integradora.

### Teste do conceito organizador

Completar:

> Este tema argumenta que...

Se a frase apenas listar assuntos, participantes ou perguntas, o tema provavelmente resume um domínio.

### Coerência interna

Os dados não precisam dizer a mesma coisa. Precisam participar de uma relação interpretativa explicável. Contradição pode compor o tema quando o argumento mostra sua função.

### Distinção externa

Perguntar o que se perderia se dois temas fossem fundidos. Se nada substantivo se perde, revisar fronteiras.

### Casos divergentes

Não usar como teste positivista de falsificação. Examinar como restringem, complicam ou redirecionam a leitura.

## 4. Rigor e auditabilidade

Adaptar a tradição de trustworthiness sem importar pressupostos incompatíveis:

### Credibilidade

Demonstrar envolvimento com o corpus, interpretações densas, tensões tratadas e diálogo humano quando ocorrido.

### Dependabilidade

Permitir reconstruir decisões, mudanças e condições do processo. Não prometer que outro analista produziria os mesmos temas.

O manifesto computado prova identidade, tamanho e integridade dos arquivos; não prova leitura. Intervalos percorridos, lotes e memos sustentam a alegação de cobertura como trilha processual, mas continuam reconferíveis e não devem ser apresentados como observação externa da atividade do agente.

### Confirmabilidade

Mostrar como afirmações se ligam aos dados e como posicionamentos influenciaram escolhas. Não prometer objetividade.

### Transferibilidade

Oferecer contexto suficiente para que leitores avaliem pertinência em outros cenários. Não reivindicar validade externa estatística.

### Reflexividade

Para humanos, registrar posição, relações, experiência e escolhas. Para IA, registrar somente reflexividade operacional:

- instruções recebidas;
- pressupostos mobilizados;
- influência da pergunta e de teorias fornecidas;
- incertezas e alternativas;
- limitações de acesso, contexto e capacidade.

## 5. Erros recorrentes

| Erro | Correção |
|---|---|
| temas iguais às perguntas | reconstruir por significado compartilhado |
| muitos códigos genéricos | retornar aos excertos e precisar ação/ideia |
| frequência como importância | justificar relevância para a pergunta |
| categoria obrigatória | remover quando não acrescentar interpretação |
| consenso de agentes | substituir por rivalidade argumentada |
| citação polida | usar literal ou marcar paráfrase |
| teoria sugerida domina o corpus | produzir rival material; independente somente se houver isolamento demonstrado |
| prosa sofisticada sem lastro | demonstrar genealogia e excertos |
| casos raros isolados em gueto | testar se tensionam temas centrais |
| incerteza apagada | registrar zona e consequência |

### Poder, memória e situação de entrevista

| Situação | Tratamento |
|---|---|
| autoridade institucional | tratar cargo, mandato, interesse e acesso como posição; não como superioridade epistêmica |
| reivindicação de liderança ou crédito | comparar autoria declarada, temporalidade, trabalho coletivo e condições de possibilidade |
| eufemismo ou recusa | separar dito, não dito, inferido e documentado; não converter silêncio em confirmação |
| explicação retrospectiva | analisar atribuição causal como posição; distinguir sequência, mecanismo, evidência e contrafactual |
| pergunta sugestiva | registrar co-produção, assimetria e correções posteriores |
| conteúdo confidencial | separar material analisável de excerto publicável e manter proveniência por ID seguro |

Evitar deferência e moralização. Uma versão institucional pode ser relevante sem ser automaticamente verdadeira; uma contestação pode ser forte sem acusar participantes de mentira ou intenção oculta.

## 6. Gates por fase

Usar `PASS`, `FAIL` ou `N/A` e anexar uma evidência curta. Um `FAIL` permite continuar o fluxo e produzir diagnóstico, mas bloqueia “análise completa” e “pronta para manuscrito”.

| Fase | Requisito duro | Falha que impede aprovação |
|---|---|---|
| F0 | escopo, decisões, delegação, riscos e limites explícitos | inventar autorização, modelo, parâmetro ou posição |
| F1 | manifesto reconciliado com intervalos, lotes e memos | ler amostra e alegar corpus integral |
| F2 | códigos específicos, localizados e distribuídos | código material sem fonte/localização |
| F3 | conceito organizador e afirmação por tema | tópico, pergunta ou resumo de domínio |
| F4 | rival material, estatuto correto e condições de derrota testadas | rival ausente, caricatural, falsamente independente ou incapaz de ameaçar o mapa |
| F5 | passaporte e âncoras verificadas | tema sem genealogia ou citação não verificada |
| F6 | relato proporcional e estatutos separados | sobrealegação ou literalidade não demonstrada |

Aplicar bloqueio à alegação, não ao arquivo:

- manter a saída parcial para auditoria;
- excluir citações não verificadas do corpo publicado;
- delimitar o subconjunto realmente analisado;
- não converter aviso em `PASS`;
- não exigir validação humana para concluir uma rota autônoma.

## 7. Auditoria final

- [ ] A pergunta, epistemologia e afirmações são coerentes.
- [ ] A cobertura do corpus está declarada.
- [ ] Códigos materiais têm excertos e localização.
- [ ] Temas não reproduzem tópicos do roteiro.
- [ ] Conceitos organizadores são claros.
- [ ] Variação e contradição foram interpretadas.
- [ ] Excertos publicados estão `verified_exact`.
- [ ] Rivais e resíduos foram tratados.
- [ ] O estatuto da rival é independente, informada ou ausente sem ambiguidade.
- [ ] Todos os `FAIL` aparecem no estatuto final.
- [ ] O texto apresenta argumento, não inventário.
- [ ] Limitações não foram convertidas em promessas.
