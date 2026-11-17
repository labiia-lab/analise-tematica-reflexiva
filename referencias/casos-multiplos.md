# Casos múltiplos

## Sumário

1. O risco
2. Isolamento entre casos
3. O que só existe aqui
4. Detector de semelhança
5. Síntese comparativa
6. Estatuto

## 1. O risco

Quando o mesmo agente analisa vários casos comparáveis em sequência (cidades, grupos, escolas), o mapa do primeiro caso tende a virar molde dos seguintes. Os sinais: mesma ordem de temas em todos os casos, nomes com a mesma construção, parágrafos idênticos, familiarização de um caso comparando-se a outro, e o que é local sobrevivendo só nos exemplos. O resultado parece comparável e é, em parte, a mesma análise aplicada várias vezes.

Semelhança entre casos pode ser achado. Para ser achado, precisa ter sido construída depois de cada caso ser lido por si.

## 2. Isolamento entre casos

No perfil isolado:

1. um contexto por caso, que recebe o corpus daquele caso, a pergunta e F0;
2. nenhum caso recebe corpus, memos, códigos, temas ou relatório de outro;
3. cada caso tem pasta de saída e registro de evidências próprios, com o campo `caso` nas fontes;
4. a pergunta e as decisões de F0 são comuns; lente, nomes e arquitetura de temas não são;
5. a ordem de execução e o que cada contexto recebeu ficam registrados.

No perfil sequencial, o isolamento não pode ser demonstrado. Reduzir o dano: concluir e gravar cada caso antes de abrir o seguinte, não reler arquivos de casos anteriores, e declarar a limitação. Tratar a semelhança entre casos como suspeita.

Em qualquer perfil, não usar como ponto de partida um “modelo de temas” comum, nem pedir que os casos sigam a mesma estrutura temática para facilitar a comparação. A comparação é trabalho da síntese.

## 3. O que só existe aqui

Cada relatório de caso tem uma seção com esse nome. Ela responde:

- que tema, tensão ou modo de dizer aparece neste caso e dependem de algo dele (um acontecimento, um lugar, uma instituição, uma história);
- que excertos mostram isso;
- o que se perderia se este caso fosse lido como mais um exemplo do conjunto.

Se a resposta for “nada é específico”, mostrar a busca: o que foi procurado e onde. Detalhe local que aparece em `nao_representado` e não chega ao relatório é o sinal mais comum de que o molde venceu o dado.

## 4. Detector de semelhança

Depois de todos os casos:

```text
python "<PASTA_DA_SKILL>/scripts/auditar_analise.py" homogeneizacao --relatorios CASO_A/06-relatorio-final.md CASO_B/06-relatorio-final.md CASO_C/06-relatorio-final.md --templates "<PASTA_DA_SKILL>/templates" --output homogeneizacao.json
```

O script compara os relatórios dois a dois, fora das citações e descontando o texto dos templates, e devolve a proporção de sequências de seis palavras em comum e os títulos parecidos. Acima do limiar, ou com títulos parecidos, o par entra em alerta.

Para cada par em alerta, responder por escrito:

1. o que é igual: estrutura, nomes, parágrafos de método, interpretação;
2. se a interpretação igual se sustenta nos excertos de cada caso separadamente;
3. o que será reescrito, a partir dos dados do caso, e o que fica como convergência a tratar na síntese.

O limiar é um gatilho de releitura, não uma medida de validade. Semelhança baixa não prova sensibilidade ao dado.

## 5. Síntese comparativa

É uma fase própria, feita depois de todos os casos, com `templates/casos-multiplos/sintese-comparativa.md`. Trabalha sobre os relatórios e registros dos casos e volta ao corpus quando precisa conferir.

Perguntas da síntese:

- que padrões de significado atravessam casos, e com que diferença em cada um;
- que padrões existem em um caso e faltam em outro, e o que isso sugere;
- onde a mesma palavra faz trabalhos diferentes em casos diferentes;
- o que a comparação não permite dizer (casos não são amostras de populações).

Regras:

- convergência entre casos não é validação: os casos foram analisados pelo mesmo tipo de sistema;
- uma categoria comparativa só vale se cada caso a sustenta com excertos próprios;
- a síntese pode mostrar que um tema de um caso era, afinal, fraco; registrar e voltar ao caso, em revisão dirigida;
- a síntese tem contestação própria: uma leitura rival sobre o que une e o que separa os casos.

## 6. Estatuto

Declarar, além do estatuto de cada caso:

- isolamento entre casos: demonstrado, parcial ou não demonstrável;
- resultado do detector e pares em alerta, com a resposta dada;
- o que na síntese é convergência construída e o que é apenas estrutura comum do relato.
