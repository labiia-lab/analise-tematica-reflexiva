# Testes comportamentais da skill

## Princípio

Uma skill metodológica precisa tornar o comportamento observável. Estes cenários especificam falhas, respostas exigidas e critérios de aprovação.

Eles não são prova automática de qualidade e não substituem forward-test com instâncias independentes.

## Formato obrigatório

Cada cenário deve conter objetivo, prompt, microcorpus ou condição, falha esperada, comportamento exigido e critérios observáveis.

## Matriz dos 21 cenários

| ID | Risco | Comportamento central |
|---|---|---|
| 1 | saltar familiarização | cobertura integral ou estatuto parcial |
| 2 | códigos vagos | especificidade e ligação ao excerto |
| 3 | resumo de domínio | conceito organizador e argumento |
| 4 | ignorar contradições | tensão como recurso analítico |
| 5 | primeira solução final | contestação obrigatória |
| 6 | racionalização | evidência antes de alegação |
| 7 | gueto de raridades | resíduo pode alterar tema central |
| 8 | in vivo rígido | linguagem preservada com interpretação |
| 9 | advogado decorativo | rival capaz de mudar o mapa |
| 10 | saída rasa | profundidade com substância |
| 11 | sycophancy | hipótese do usuário é contestável |
| 12 | citação inventada | literalidade e localização |
| 13 | apagamento experiencial | conservação e tratamento da perda |
| 14 | ilusão de profundidade | lastro e conceito organizador |
| 15 | consentimento/IA | alerta, minimização e transparência |
| 16 | posição institucional | cargo não equivale a neutralidade ou autoridade epistêmica |
| 17 | autolegitimação | crédito individual confrontado com trabalho coletivo |
| 18 | silêncio/eufemismo | separar dito, não dito, inferido e documentado |
| 19 | causalidade retrospectiva | rival multicausal e contrafactual marcado |
| 20 | assimetria da entrevista | pergunta sugestiva e co-produção do sentido |
| 21 | confidencialidade/proveniência | rastreabilidade com minimização de identificadores |

## Protocolo estrutural local

- validar frontmatter e nome;
- conferir links internos;
- confirmar 7 templates, 7 referências e 21 cenários;
- executar `python -m unittest discover -s testes -p "test_*.py"`;
- compilar `scripts/verificar_citacoes.py`;
- confirmar ausência de caches e dependências externas;
- procurar instruções residuais de NLP, frequência, coocorrência, Kappa ou estabilidade;
- conferir que o núcleo usa somente o padrão Agent Skills e caminhos relativos;
- auditar os exemplos para nomes, cidades, detalhes identificadores e citações tratadas como dados reais;
- conferir cenários específicos para posição, poder, memória retrospectiva e confidencialidade de elites governamentais.

### Regra de anonimização

Os microcorpora dos cenários usam somente identificadores neutros (`P1`, `P2` etc.) ou papéis analíticos genéricos. Não devem conter nomes próprios, localidades, órgãos, departamentos, contatos ou combinações biográficas que permitam reconhecer uma pessoa. Papéis como “secretário” ou “gestora” permanecem apenas quando são necessários para testar posição institucional; não funcionam como nomes.

## Forward-test

Antes de publicar:

1. executar cenários sem skill;
2. executar com a skill revisada;
3. usar contextos independentes e sem conclusões vazadas;
4. separar geração e avaliação;
5. registrar aderência por critério e falhas novas;
6. revisar e repetir os cenários afetados.

Forward-test mede aderência comportamental, não eficácia científica, equivalência humana ou validade da ATR. Não usar concordância entre agentes como medida de validade.
