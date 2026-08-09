# Colaboração, delegação e auditoria

## Sumário

1. Rotas
2. Delegação de IA
3. Registro de interações
4. Participação humana
5. Ética e privacidade
6. Estatutos

## 1. Rotas

### Autônoma

Executar F0–F6 sem checkpoint humano obrigatório. A análise pode ser completa quando cobertura, evidências e gates passarem. Declarar ausência de validação humana sem tratá-la como falha automática.

### Por checkpoints

Pausar após F0, F2, F4 e F5. Em cada pausa, mostrar síntese, decisões, limitações, opções reais e efeito provável de cada opção.

### Início humano

Aceitar memos, códigos, categorias, temas e texto analítico. Registrar origem, fase e efeito. Verificar contra o corpus e indicar o que foi mantido, reformulado ou recusado. Material humano não é ground truth.

### Paralela cega

1. Compartilhar pergunta, corpus e F0.
2. Ocultar a leitura humana até o encerramento de F5.
3. Abrir as leituras.
4. Comparar convergências, divergências, pontos cegos e perdas.
5. Não converter concordância em validade.

## 2. Delegação de IA

Preencher em F0:

| Fase | Função delegada | Nível | Ambiente/modelo | Verificação prevista | Papel humano |
|---|---|---|---|---|---|
| F0–F6 |  | 0–3 |  |  | não houve/descrição |

Níveis:

- **0 — sem IA:** trabalho externo à IA.
- **1 — apoio:** organização, busca, formatação ou crítica sem decisão temática principal.
- **2 — coprodução:** IA produz códigos, temas ou redação que serão integrados por outra função.
- **3 — autonomia:** IA executa e integra a fase; a saída continua sujeita aos gates.

O nível descreve delegação, não qualidade. Uma rota autônoma pode usar nível 3 em todas as fases e ainda reconhecer limites epistemológicos.

Registrar:

- ambiente, modelo e versão, quando expostos;
- data;
- parâmetros expostos;
- limites de contexto;
- processamento local ou remoto, quando conhecido;
- retenção e políticas conhecidas;
- alinhamento entre a posição epistemológica e o tipo de inferência solicitado;
- técnicas de verificação.

Usar “não informado pelo ambiente” em vez de adivinhar.

## 3. Registro de interações

Usar em todas as fases:

| ID | Fase/função | Ambiente/modelo | Objetivo e prompt sanitizado | Fontes por ID | Saída | Verificação | Intervenção humana/efeito |
|---|---|---|---|---|---|---|---|

Registrar a instrução reproduzível ou uma versão sanitizada suficiente para reconstruir a tarefa. Se o prompt incorporar dados sensíveis, registrar template, finalidade, IDs das fontes e hash do arquivo seguro, não o conteúdo integral.

Não registrar:

- raciocínio interno oculto;
- credenciais ou tokens;
- identificadores pessoais desnecessários;
- conversas integrais quando um resumo auditável bastar.

## 4. Participação humana

Usar:

| Fase | Participante/papel | Intervenção | Efeito analítico | Pendente |
|---|---|---|---|---|
| F0–F6 | não houve/descrição |  |  |  |

Distinguir fornecimento de contexto, decisão metodológica, revisão interpretativa, validação de excertos, diálogo participante e revisão editorial. Não resumir tudo como “validado”.

## 5. Ética e privacidade

Registrar:

- autorização declarada para uso do corpus;
- se o consentimento menciona IA;
- sensibilidade e identificadores;
- ambiente de processamento;
- minimização e desidentificação;
- incertezas e limites de alegação.

Nunca inventar aprovação ética ou consentimento. Incerteza pode permitir análise sob solicitação do usuário, mas bloqueia alegar adequação ética confirmada. Quando o usuário mandar continuar, anonimizar por padrão a cópia de trabalho e a saída, preservar proveniência por IDs seguros e registrar a perda de rastreabilidade. Perguntar novamente somente se a identidade for indispensável à pergunta.

## 6. Estatutos

Declarar dimensões independentes:

| Dimensão | Valores |
|---|---|
| fluxo | F0–F6 executado; interrompido |
| cobertura | integral; parcial; indeterminada |
| evidências | verificáveis; limitadas; inválidas |
| contestação | independente; informada; ausente |
| participação humana | mapa por fase |
| validação humana | realizada; parcial; ausente |
| prontidão | manuscrito; exploração; auditoria |

“Completa” exige cobertura do corpus declarado e acessível e `PASS` nos gates substantivos. Não exige participação humana. “Pronta para manuscrito” exige ainda citações verificadas e estatutos coerentes.

Formulação máxima:

> ATR autônoma completa no escopo declarado e auditável; redação pronta para incorporação em manuscrito; sem validação humana.

Não prometer publicação, verdade, equivalência humana ou aprovação ética.
