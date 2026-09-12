# Visualizações da análise

## Princípio

A visualização principal da ATR é o mapa temático em três colunas: códigos à esquerda, temas candidatos ao centro e temas finais à direita. O mapa é um argumento visual: as setas mostram como a análise agrupou significados, não apenas onde cada rótulo foi parar.

Prioridades:

1. legibilidade acadêmica;
2. editabilidade (SVG vetorial, não imagem raster);
3. fidelidade às relações reais da análise, nunca a um layout de software;
4. uma página de Word (entre meia lauda e uma lauda).

Regra dura: o mapa nunca deve ser gerado como imagem por modelo generativo. Alinhamentos, tipografia, setas e quebras de linha se degradam; o resultado deixa de ser auditável. Gerar SVG vetorial e, se necessário, exportar PNG.

## Formato e proporções

| Parâmetro | Especificação |
|---|---|
| Dimensão final | 1448 × 1086 px |
| Proporção | 4:3, paisagem |
| Fundo | branco quase puro (`#FEFEFE`) |
| Margem esquerda | 24 px |
| Margem direita | ~16 px |
| Margem superior | 8 px |
| Margem inferior | ~12 px |
| Estrutura | três colunas verticais |
| Fluxo | esquerda → direita |
| Unidades | códigos, temas candidatos, temas finais |

O desenho ocupa quase toda a altura. O vazio horizontal entre colunas faz parte da composição e não deve ser comprimido.

## Grade horizontal

| Zona | x inicial | x final | largura |
|---|---|---|---|
| Códigos | 24 | ~445 | ~421 px |
| Temas candidatos | 561–576 | ~995 | ~419–434 px |
| Temas finais | ~1169 | ~1426 | ~251–257 px |

Corredores entre colunas:

- códigos → temas candidatos: ~115–130 px;
- temas candidatos → temas finais: ~175 px.

As setas respiram nesses corredores brancos. Usar apenas segmentos retos diagonais ou horizontais; nunca cotovelos ortogonais.

## Cabeçalhos

Alinhados pelo topo, cantos arredondados (raio 5–7 px), fundo azul-acinzentado muito claro, contorno fino, texto centralizado, peso forte, sem sombra, sem ícone.

| Cabeçalho | x | y | largura | altura |
|---|---|---|---|---|
| Códigos | 23 | 8 | 421 | 41 |
| Temas candidatos | 567 | 8 | 425 | 40 |
| Temas finais | 1142 | 8 | 290 | 41 |

- preenchimento: `#D5DFE8` (variações discretas até `#E0E7ED`);
- contorno: `#8799A8`;
- texto: `#101E32`.

## Tipografia

Serifada clássica com aparência editorial. Ordem de preferência: Georgia, Cambria, Source Serif 4, Libre Baskerville, Times New Roman. Não usar fontes geométricas ou de interface (Montserrat, Poppins, Inter e similares).

| Elemento | Fonte | Tamanho | Peso | Entrelinha | Cor |
|---|---|---|---|---|---|
| Cabeçalhos | Georgia Bold | 25–27 px | 700 | ~1 | `#0D1C31` |
| Códigos | Georgia Regular | 17–18 px | 400 | 20–22 px | `#132033` |
| Temas candidatos | Georgia Regular | 17–18 px | 400 | 20–22 px | `#132033` |
| Temas finais | Georgia Bold | 22–24 px | 700 | 26–29 px | `#0D1C31`, caixa alta |

Margem interna mínima: 14 px horizontal, 7–10 px vertical. O texto nunca toca o contorno.

## Caixas

### Códigos

- preenchimento `#F0F1F1` (ou `#F2F2F1`);
- contorno `#AAB5BE`, 1–1,3 px;
- raio 5–7 px;
- quase brancas, nunca cinza médio;
- altura variável conforme o número de linhas — este detalhe deve ser preservado: caixas curtas ficam menores, caixas de duas ou três linhas ficam maiores.

### Temas candidatos

- preenchimento `#EFF0F0`;
- contorno `#87949D`, ~1,2 px;
- raio 6–8 px;
- coluna visualmente intermediária.

### Temas finais

- preenchimento `#D5E0E8` (faixa `#D1DDE7`–`#DBE5EC`);
- contorno `#214966`, 2,5–3 px;
- raio 8–10 px;
- contraste hierárquico pela espessura da borda e peso tipográfico, não por saturação.

O contorno dos temas finais é claramente mais forte que o das demais caixas.

### Fundo com variação tonal

Gradiente vertical extremamente discreto:

- códigos e temas candidatos: topo `#F4F4F3`, base `#ECEEEE`;
- cabeçalhos: topo `#E1E7EC`, base `#D1DCE6`;
- temas finais: topo `#DEE7EE`, base `#D0DDE7`.

O contraste entre extremos permanece baixo; a caixa parece quase plana. Proibido: efeito de vidro, brilho, relevo, sombra pesada, textura.

## Setas

| Parâmetro | Especificação |
|---|---|
| Cor | `#4E5A61` |
| Espessura | 1,3–1,7 px |
| Ponta | triangular preenchida, ~9–11 px de comprimento, ~7 px de largura |

Regras:

- uma única linha reta entre origem e destino;
- sem curvas Bézier, sem cotovelos, sem linha dupla;
- nenhuma seta atravessa caixa;
- início exatamente no contorno direito da caixa de origem;
- fim exatamente no contorno da caixa de destino;
- linhas atrás dos textos;
- evitar duas linhas exatamente sobrepostas.

### Distribuição dos pontos de chegada

Quando várias setas chegam à mesma caixa, não concentrar todas no centro:

| Entradas | Posições na borda (fração da altura) |
|---|---|
| 2 | 0,35 / 0,65 |
| 3 | 0,25 / 0,50 / 0,75 |
| 5 | 0,15 / 0,32 / 0,50 / 0,68 / 0,85 |

Essa regra explica boa parte da legibilidade da terceira coluna.

## Relações do mapa

O mapa representa as relações reais da análise. Exemplo de estrutura típica:

| Códigos | Tema candidato |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 e 4 | 3 |
| 5 e 6 | 4 |

| Temas candidatos | Tema final |
|---|---|
| 1, 2 e 3 | Tema A |
| 4, 5, 6, 7 e 8 | Tema B |

O agrupamento deve ser inteligível apenas pela geometria das setas, sem caixas externas envolvendo grupos.

## Quebras de linha

Controladas manualmente; nunca delegadas ao motor gráfico.

- uma linha para rótulos curtos;
- duas linhas para a maioria dos códigos;
- três linhas só quando o texto exigir;
- máximo ~40 caracteres visuais por linha nos códigos;
- máximo ~43 caracteres nos temas candidatos;
- evitar última linha com uma única palavra;
- preservar unidades semânticas na mesma linha;
- nome do tema final em linha separada do identificador numérico;
- transcrever o texto exatamente, preservando capitalização e numeração.

## Alinhamento e espaçamento

- caixas de códigos compartilham a borda esquerda;
- temas candidatos compartilham o eixo central;
- temas finais compartilham o eixo central;
- espaçamento baseado em agrupamentos conceituais, não automático: vazios maiores separam conjuntos que pertencem a blocos distintos;
- espaçamento de pelo menos ~7 px entre caixas consecutivas.

## Hierarquia visual

Quatro níveis, obtidos por peso tipográfico, espessura de borda, dimensão e leve diferença de preenchimento — sem novas cores:

1. temas finais;
2. cabeçalhos das colunas;
3. temas candidatos;
4. códigos.

## Proibido

Sombra projetada evidente, gradientes fortes, azul saturado, caixas coloridas por categoria, ícones, emojis, números em círculos, cards de dashboard, fundo bege, linhas tracejadas, cabeçalhos com barras escuras, sans serif pesada, molduras envolvendo grupos, efeitos 3D, setas curvas, conectores grossos, excesso de espaço interno, aparência de organograma empresarial ou de tabela do PowerPoint.

## Ordem de construção

1. canvas 1448 × 1086 px, fundo `#FEFEFE`;
2. definir os três eixos horizontais;
3. posicionar os cabeçalhos;
4. criar as caixas dos códigos;
5. criar as caixas dos temas candidatos;
6. criar os temas finais;
7. posicionar os conectores;
8. ajustar os pontos de chegada um a um;
9. inserir textos com quebras manuais;
10. conferir margens internas e limites;
11. exportar SVG;
12. exportar PNG 1448 × 1086 px com antialiasing — obrigatório na mesma execução.

## Controle de qualidade

Antes de considerar pronto, verificar:

- nenhum texto cortado;
- nenhuma seta encostando em texto ou atravessando caixa;
- nenhuma ponta escondida;
- caixas alinhadas em seus eixos;
- espaçamento ≥ ~7 px entre caixas consecutivas e maior entre grupos;
- ausência de cores saturadas;
- consistência tipográfica;
- bordas dos temas finais claramente mais fortes;
- legibilidade com a figura reduzida a ~70% e em página A4 ou slide.

### Encaixe automático do texto

Antes de concluir, o gerador confere se alguma linha ultrapassa a largura útil da caixa (largura da caixa menos 14 px de margem interna de cada lado), medindo com a fonte real (Georgia, via Pillow). Se houver excesso, a fonte da linha é reduzida em passos de 0,5 px e re-medida até caber; o processo para na fonte mínima (10 px) e reporta o item que não pôde ser ajustado. Nenhuma letra deve ficar para fora do quadro. O comando informa cada redução aplicada:

```text
[info] fonte reduzida no item 'TF3': 23.0 -> 20.0 px
```

Se um item exigir fonte abaixo de 14 px, prefira encurtar o texto ou simplificar a quebra de linha a aceitar letras pequenas.

### Arquivos produzidos

Toda execução produz **dois arquivos**: o SVG vetorial editável e um PNG de 1448 × 1086 px para inserção direta em Word, PDF ou slide. O PNG é obrigatório e usa, nesta ordem: cairosvg, Inkscape ou o renderizador nativo (Pillow); sem nenhum deles, a execução falha com erro explícito. O nome padrão do PNG acompanha o do SVG (`mapa-tematico.svg` → `mapa-tematico.png`); `--png` permite outro caminho.

## Operacionalização nesta skill

O script `scripts/gerar_mapa_tematico.py` gera o SVG editável **e o PNG** a partir de um JSON de estrutura (códigos, temas candidatos, tema final, agrupamentos e quebras de linha). Ele não decide conteúdo: recebe as relações da análise e aplica a grade, a tipografia, as cores, as setas e as distribuições especificadas neste documento, além do encaixe automático de texto.

```text
python "<PASTA_DA_SKILL>/scripts/gerar_mapa_tematico.py" --input mapa.json --output mapa-tematico.svg
```

Dois arquivos saem desta execução: `mapa-tematico.svg` e `mapa-tematico.png` (1448 × 1086 px). PNG em outro caminho, quando necessário:

```text
python "<PASTA_DA_SKILL>/scripts/gerar_mapa_tematico.py" --input mapa.json --output mapa-tematico.svg --png outro-nome.png
```

O script valida a estrutura, recusa relações quebradas (código ou tema candidato sem destino), reduz a fonte em passos de 0,5 px quando uma linha excede a caixa e reporta qualquer texto que não caiba. SVG e PNG são entregas conjuntas; sem renderizador disponível, a execução falha (instale Pillow, cairosvg ou Inkscape).

O mapa não substitui o passaporte dos temas nem a auditoria de citações: ele apresenta a arquitetura, os passaportes sustentam a interpretação.
