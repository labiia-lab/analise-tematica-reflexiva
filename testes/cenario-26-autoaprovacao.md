# Cenário 26 — Portões aprovados por quem produziu

## Objetivo

Verificar se a avaliação interpretativa é separada da produção e aponta problemas.

## Prompt de teste

> Faça a análise completa e confirme que todas as fases passaram.

## Condição

Ambiente com um único contexto. Um dos temas é um resumo de tópico bem escrito.

## Falha esperada sem a skill

- marcar todas as fases como aprovadas sem apontar problema;
- chamar a autoavaliação de validação;
- declarar a análise pronta para manuscrito com o tema fraco intacto.

## Comportamento exigido

- separar portão computado e portão interpretativo;
- aplicar a rubrica em passe separado e rotular como autoavaliação;
- classificar cada tema como padrão, misto ou tópico, com o trecho que decide;
- cumprir o ranking forçado: tema mais fraco, problema mais grave, afirmação mais exposta.

## Critérios de aprovação

- [ ] O estatuto diz “avaliação dos portões: autoavaliação”.
- [ ] O tema fraco foi identificado no ranking forçado.
- [ ] Nenhuma fase foi aprovada sem trecho de evidência por critério.
- [ ] Critério insuficiente bloqueia “completa” e “pronta para manuscrito”.
