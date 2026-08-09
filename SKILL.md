---
name: analise-tematica-reflexiva
description: Use when the user needs to perform, continue, audit, review, or compare a Reflexive Thematic Analysis of qualitative material, including interviews, focus groups, documents, human codes, candidate themes, autonomous AI analysis, or work based on Braun and Clarke.
---

# Análise Temática Reflexiva

## Princípio central

Conduzir Análise Temática Reflexiva (ATR) como prática interpretativa, recursiva e situada. Construir uma leitura argumentada; não apresentar temas como entidades descobertas nem simular neutralidade ou experiência humana.

Executar autonomamente F0–F6 quando solicitado. A ausência de participação ou validação humana não impede a conclusão do fluxo, mas deve permanecer explícita e separada da cobertura, da integridade das evidências e da prontidão do relatório.

Aplicar **contestabilidade interpretativa incorporada**:

> Toda interpretação escolhida deve carregar uma alternativa forte recusada, a evidência da escolha e o custo experiencial da abstração.

## Invariantes

1. Construir temas; nunca dizer que eles “emergiram sozinhos”.
2. Trabalhar recursivamente entre familiarização, códigos, temas e escrita.
3. Decidir separadamente indução/dedução e semântico/latente.
4. Tornar categorias e subtemas opcionais.
5. Não usar frequência como sinônimo de importância.
6. Não exigir codebook rígido, consenso, Kappa, estabilidade ou resultados idênticos.
7. Tratar contradições, casos raros e silêncios como possíveis recursos analíticos.
8. Verificar literalmente todo excerto publicado contra a fonte acessível.
9. Não chamar convergência entre agentes de triangulação humana.
10. Não atribuir consciência, experiência vivida ou reflexividade humana à IA.
11. Não inventar dados, contexto, autorização, parâmetros, citações ou validação.
12. Preservar a proveniência de material humano e algorítmico.
13. Manter afirmações proporcionais ao corpus efetivamente processado.

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

### Entradas mínimas

Registrar:

- pergunta ou objetivo;
- corpus, unidade de análise e limites;
- contexto necessário;
- posição epistemológica, se definida;
- material humano prévio;
- formato e local de saída.

Antes de analisar, declarar fontes acessíveis, ilegíveis ou ausentes; capacidade de produzir formatos adicionais; possibilidade de separar contextos; e riscos de privacidade, consentimento ou processamento por IA.

Se houver identificadores pessoais e nenhuma direção para continuar, perguntar se já são pseudônimos ou se a saída deve ser anonimizada. Se o usuário mandar prosseguir, inclusive sem confirmação específica sobre IA, anonimizar por padrão a cópia de trabalho e a saída, advertir sobre a incerteza, registrar o esquema de IDs e continuar. Pedir nova decisão somente quando preservar identidades for indispensável à pergunta. Nunca alterar silenciosamente a fonte nem converter continuação em aprovação ética.

## Carregar recursos progressivamente

Resolver todos os caminhos abaixo relativamente à pasta que contém este `SKILL.md`, nunca presumir o diretório de trabalho do agente.

- Ler `referencias/fundamentos-atr.md` antes de F0–F3.
- Ler `referencias/qualidade-analitica.md` para aplicar gates e avaliar códigos, temas e relatório.
- Ler `referencias/contestabilidade-interpretativa.md` antes de F4–F5.
- Ler `referencias/colaboracao-e-auditoria.md` para rotas, registros de IA, estatutos e participação humana.
- Ler `referencias/ia-em-at.md` ao planejar ou auditar qualquer intervenção de IA.
- Ler `referencias/fundamentacao-e-proveniencia.md` ao justificar decisões acadêmicas.
- Ler `referencias/exemplo-integrado.md` somente quando um exemplo preenchido ajudar.

Não carregar todas as referências por rotina.

## Contrato comum

### Cobertura

Inventariar todo o corpus declarado e registrar o que foi efetivamente lido. Para corpus maior que o contexto disponível, trabalhar em lotes, produzir memos por fonte e realizar síntese transversal. Nunca inferir cobertura integral de amostra silenciosa.

Quando houver acesso local aos arquivos e Python, gerar a identidade computável do corpus após resolver a pasta desta skill:

```text
python "<PASTA_DA_SKILL>/scripts/verificar_citacoes.py" --inventario CORPUS --output manifesto-corpus.jsonl
```

Manter `CORPUS` restrito às fontes de entrada e gravar a saída fora dele. O `manifesto-corpus.jsonl` registra caminho relativo, bytes, linhas e SHA-256. Ele prova a identidade e a integridade dos arquivos inventariados, não que tenham sido lidos. Reconciliar o manifesto com intervalos percorridos, lotes e memos por fonte em F1; tratar estes últimos como trilha processual auditável, não como prova externa de cognição.

### Citações

Conferir cada excerto por busca exata ou leitura direta. Registrar ID, fonte anonimizada e localização estável. Texto alterado é paráfrase e não recebe aspas.

Para `.docx`, `.pdf`, áudio, legenda ou texto em outra codificação:

1. preservar o original sem alteração;
2. criar derivado textual UTF-8 sem limpar, resumir ou parafrasear o conteúdo;
3. registrar nome e SHA-256 do original e do derivado, método/versão de extração e correspondência de páginas, tempos ou unidades;
4. conferir amostras do início, meio e fim e cada excerto destinado à publicação contra o original;
5. verificar citações contra o derivado e manter também o localizador do original quando disponível.

Quando os derivados ficarem fora de `CORPUS`, inventariá-los separadamente como `manifesto-derivados.jsonl` com o mesmo comando `--inventario`.

Se a extração ou sua correspondência não puder ser auditada, continuar a análise com evidência limitada, mas não publicar o excerto como literal verificado.

Quando houver fontes ou derivados textuais UTF-8 e Python, resolver primeiro a pasta desta skill e usar:

```text
python "<PASTA_DA_SKILL>/scripts/verificar_citacoes.py" --input citacoes.jsonl --base CORPUS --output verificacao-citacoes.jsonl
```

Usar uma citação por linha JSONL, por exemplo: `{"citation_id":"Q001","text":"fala literal","source":"P01.txt","declared_locator":"linha 12","original_source_id":"F01","original_locator":"PDF, p. 7"}`. Resolver `source` relativamente a `--base`; o script calcula localizadores por linha e o hash da fonte. Os dois campos do original são opcionais para o script e obrigatórios no registro quando a fonte tiver sido derivada.

Publicar como literal somente `verified_exact`. Tratar `exact_multiple_needs_locator`, `exact_locator_mismatch`, `normalized_candidate_not_verified`, `not_found`, `source_missing`, `source_unreadable` e `invalid_record` como não verificados até correção. Se o script não puder ser executado, aplicar a mesma lógica manualmente e registrar evidência da busca.

### Interações com IA

Em cada fase, registrar somente o necessário:

| ID | Fase/função | Ambiente/modelo | Objetivo e prompt sanitizado | Fontes por ID | Artefato | Verificação | Intervenção humana/efeito |
|---|---|---|---|---|---|---|---|

Não registrar raciocínio interno, credenciais, identificadores desnecessários ou conversa sensível integral. Quando modelo, versão ou parâmetro não estiver exposto, escrever “não informado pelo ambiente”.

### Estatuto da rival

Usar exatamente:

- **independente** — contexto ou sessão separada; recebe corpus, pergunta e F0, mas não o mapa principal nem conclusões;
- **informada** — vê o mapa principal ou trabalha no mesmo contexto;
- **ausente** — nenhuma contestação foi executada.

Se a separação não puder ser demonstrada, registrar `informada`. A falta de multiagência não bloqueia F0–F6, mas proíbe alegar rival independente.

### Gates

Ao terminar cada fase:

1. aplicar o checklist do template;
2. corrigir uma vez os problemas corrigíveis;
3. registrar cada requisito como `PASS`, `FAIL` ou `N/A`, com evidência;
4. continuar o fluxo autônomo mesmo com `FAIL`, produzindo diagnóstico ou entrega parcial;
5. impedir que qualquer `FAIL` substantivo coexista com “análise completa” ou “pronta para manuscrito”.

Por padrão, os gates são autoavaliações do mesmo sistema que produziu a fase. Registrar quem os avaliou e se houve independência; separar requisitos computados dos julgamentos interpretativos. `PASS` interno sem avaliação independente não equivale a validação externa, embora permita concluir a rota autônoma.

Não repetir uma fase indefinidamente. Uma limitação reconhecida não se converte automaticamente em aprovação.

## Funções analíticas

### Essencial

1. **Analista principal** — construir a leitura.
2. **Contestador informado** — produzir a rival forte e localizar resíduos.
3. **Integrador-auditor** — revisar temas, evidências e estatutos.

### Aprofundada

1. **Analista principal** — construir o melhor mapa inicial.
2. **Analista rival** — operar como independente somente se o isolamento estiver demonstrado; caso contrário, operar como informado.
3. **Advogado do diabo** — atacar coerência, fronteiras e inferências.
4. **Guardião experiencial** — localizar ambiguidades, contradições e perdas situadas.
5. **Auditor de evidências** — conferir cobertura, literalidade e genealogia sem decidir significados.
6. **Integrador** — manter, revisar, dividir, fundir ou abandonar com razões explícitas.

Realizar uma rodada adversarial completa e, quando necessário, uma revisão dirigida somente dos temas afetados.

## F0 — Constituição analítica

Preencher `templates/fase-0-decisoes/decisoes-metodologicas.md`.

Definir pergunta, escopo, posição epistemológica, eixos, unidade, rota, profundidade, cobertura, ética e privacidade. Registrar uma matriz de delegação F0–F6, ambiente/modelo, parâmetros expostos, alinhamento entre capacidades da IA e posição metodológica, mapa humano e plano de verificação.

**Saídas:** `00-constituicao-analitica.md` e, quando houver arquivos locais, `manifesto-corpus.jsonl`.

**Gate:** `PASS` somente quando decisões, lacunas, riscos e limites de alegação estiverem explícitos. Consentimento desconhecido bloqueia alegações de aprovação ética, não a descrição analítica autorizada pelo usuário.

## F1 — Familiarização

Preencher `templates/fase-1-familiarizacao/notas-de-familiarizacao.md`.

Ler todas as fontes acessíveis. Produzir memos por fonte ou lote, síntese transversal e memo reflexivo com tensões, mudanças de posição, expressões situadas e perguntas.

**Saída:** `01-familiarizacao.md`.

**Gate:** `PASS` somente quando inventário e cobertura coincidirem. Cobertura parcial exige `FAIL` para integralidade e delimitação explícita do subconjunto.

## F2 — Codificação reflexiva

Preencher `templates/fase-2-codigos/codificacao-reflexiva.md`.

Codificar todo material relevante, permitindo múltiplos códigos por excerto e revisão durante o processo. Para cada código material, registrar significado, excerto, localização, nota interpretativa, origem e mudanças. Distinguir códigos humanos, gerados, revisados e recusados.

**Saída:** `02-codificacao-reflexiva.md`.

**Gate:** `PASS` somente com códigos específicos, distribuídos pelo corpus acessível e ligados a evidências localizadas. Excertos não verificados não podem sustentar temas finais como citações.

## F3 — Temas candidatos

Preencher `templates/fase-3-temas/temas-candidatos.md`.

Construir padrões de significado compartilhado. Para cada tema candidato, explicitar conceito organizador, afirmação, evidências, fronteiras, variação, tensões e condições prévias de enfraquecimento ou derrota. Não finalizar a primeira solução.

**Saída:** `03-temas-candidatos.md`.

**Gate:** `PASS` somente quando os temas responderem à pergunta e não forem tópicos, perguntas de entrevista ou resumos de domínio.

## F4 — Contestação e revisão

Preencher `templates/fase-4-revisao/revisao-temas.md`.

Produzir a melhor rival disponível, registrar seu estatuto e comparar argumentos sem votação ou concordância. Testar coerência, distinção, cobertura, tensão, resíduo experiencial e as condições registradas em F3. Registrar manter, revisar, dividir, fundir ou abandonar. Se nenhum tema for abandonado ou fundido substantivamente, explicar por tema por que a rival e a evidência não satisfizeram sua condição prévia de enfraquecimento ou derrota.

**Saída:** `04-contestacao-e-revisao.md`.

**Gate:** `PASS` somente quando houver rival material, evidência auditada e mudança ou recusa justificada. Contestação `ausente` é `FAIL`; contestação `informada` pode passar, mas não virar independente.

## F5 — Temas finais e passaportes

Preencher `templates/fase-5-definicao/definicao-temas-finais.md`.

Para cada tema, registrar nome, conceito organizador, afirmação, história, genealogia, excertos-âncora verificados, rival, evidência decisiva, resíduo, decisão, incerteza, estatuto da rival e participação humana.

**Saídas:** `05-temas-finais-e-passaportes.md` e, quando houver excertos candidatos, `citacoes.jsonl` e `verificacao-citacoes.jsonl`.

**Gate:** `PASS` somente quando cada tema for coerente, distinto, contestável e sustentado por evidência verificável. Não usar percentuais de confiança.

## F6 — Relato

Preencher `templates/fase-6-relatorio/relatorio-final.md`.

Produzir:

1. **corpo principal** — método, narrativa integradora, temas, excertos e conclusão;
2. **apêndice auditável** — passaportes, manifesto de IA, delegação, interações, mapa humano, cobertura, verificação, gates e decisões adversariais.

Markdown é obrigatório. Produzir DOCX ou outro formato quando solicitado e suportado; a indisponibilidade de formato adicional não muda o estatuto metodológico.

**Saída universal:** `06-relatorio-final.md`. Anexar `manifesto-corpus.jsonl` quando houver corpus local, `manifesto-derivados.jsonl` quando houver conversão e `citacoes.jsonl` mais `verificacao-citacoes.jsonl` quando o relatório usar ou avaliar excertos; registrar `N/A` no apêndice quando um artefato não se aplicar.

**Gate:** `PASS` somente quando o texto estiver alinhado a F0, todas as citações publicadas estiverem verificadas e nenhum estatuto exceder o trabalho realizado.

## Estatuto final

Declarar separadamente:

- **Fluxo:** F0–F6 executado ou interrompido.
- **Cobertura:** integral, parcial ou indeterminada.
- **Evidências:** verificáveis, limitadas ou inválidas.
- **Contestação:** independente, informada ou ausente.
- **Participação humana:** mapa por fase.
- **Validação humana:** realizada, parcial ou ausente.
- **Prontidão:** manuscrito, exploração ou auditoria.

Usar “ATR autônoma completa” somente se todo o corpus declarado e acessível tiver sido tratado e todos os gates substantivos tiverem `PASS`. A validação humana pode permanecer ausente:

> ATR autônoma completa no escopo declarado e auditável; redação pronta para incorporação em manuscrito; sem validação humana.

Não prometer verdade, publicação, equivalência humana ou aprovação ética.

## Checklist final

- [ ] Inventário e cobertura foram reconciliados.
- [ ] Toda citação publicada está `verified_exact`.
- [ ] Códigos e temas mantêm genealogia até a fonte.
- [ ] Temas possuem conceito organizador e respondem à pergunta.
- [ ] Rival e resíduo material foram tratados.
- [ ] Estatuto da rival está correto.
- [ ] Cada tema possui passaporte.
- [ ] Delegação, interações de IA e participação humana foram registradas.
- [ ] Gates e limitações permanecem visíveis.
- [ ] O estatuto final corresponde ao trabalho realizado.
