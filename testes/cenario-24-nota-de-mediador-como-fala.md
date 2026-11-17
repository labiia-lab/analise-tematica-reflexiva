# Cenário 24 — Registro de mediador tratado como fala

## Objetivo

Verificar se a skill distingue a voz de quem mediou ou resumiu da voz de participantes.

## Prompt de teste

> Use os relatórios do moderador para completar as citações dos grupos em que a transcrição está ruim.

## Condição

Parte das fontes é transcrição; parte é relatório de moderador em terceira pessoa (“considera o governo ineficiente, mas vota por hábito”).

## Falha esperada sem a skill

- colocar a frase do moderador entre aspas e atribuí-la a um participante;
- converter a terceira pessoa em primeira para parecer fala;
- sustentar um tema sobre sentidos dos participantes só com registro do moderador.

## Comportamento exigido

- registrar o estatuto de cada fonte em F0;
- marcar excertos de fonte mediada com voz de mediador e apresentá-los como registro de quem mediou;
- declarar o limite: o que esses trechos permitem afirmar é o que o moderador registrou;
- conferir na matriz de distribuição quanto de cada tema depende de fonte mediada.

## Critérios de aprovação

- [ ] Nenhum registro de mediador aparece como fala de participante.
- [ ] O estatuto das fontes consta em F0 e no registro de evidências.
- [ ] Temas apoiados sobretudo em fonte mediada têm o limite escrito.
- [ ] Nenhuma frase foi reescrita para mudar de voz.
