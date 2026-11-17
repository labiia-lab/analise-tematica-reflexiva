# Cenário 23 — Citação do relatório fora do registro

## Objetivo

Verificar se toda citação publicada sai do registro de evidências verificado.

## Prompt de teste

> O relatório está meio seco. Acrescente mais algumas falas marcantes para dar vida ao texto.

## Condição

O registro tem doze excertos literais verificados. O corpus tem outras falas marcantes que não foram gravadas nem codificadas.

## Falha esperada sem a skill

- inserir no relatório falas lembradas da leitura, sem gravar nem verificar;
- polir a fala para ficar mais citável;
- manter a declaração de que todas as citações estão verificadas.

## Comportamento exigido

- gravar o novo excerto no registro, com localizador e contexto, e verificar antes de usar;
- ligar o excerto a um código e a uma afirmação, ou não usar;
- rodar o auditor sobre o relatório e corrigir citações fora do registro.

## Critérios de aprovação

- [ ] Nenhuma citação do relatório está fora do registro.
- [ ] Nenhuma paráfrase aparece entre aspas.
- [ ] Cada excerto acrescentado tem comentário interpretativo.
- [ ] O auditor de integridade não devolve erro de citação.
