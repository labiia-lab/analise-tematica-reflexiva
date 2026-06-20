# Visualizacoes e Auditoria Quantitativa na ATR

## Principio

Visualizacoes na ATR devem ajudar o pesquisador a inspecionar a analise, nao substituir a interpretacao qualitativa. O LLM deve primeiro ler, codificar e construir temas por significado. Depois, use frequencias, tabelas e diagramas para auditar cobertura, localizar tensoes e comunicar o processo.

## Ordem Recomendada

1. Codificacao interpretativa pelo agente, com revisao humana.
2. Verificacao literal de extratos.
3. Auditoria de frequencia dos codigos por fonte.
4. Revisao qualitativa de codigos raros, amplos demais ou concentrados demais.
5. Mapas hierarquicos de tema -> subtema -> categoria -> codigo.
6. Diagramas finais para relatorio.

## Frequencia: Fazer, Mas Nao Fetichizar

Use frequencia para:
- identificar codigos concentrados em uma unica fonte.
- checar se um codigo esta amplo demais.
- localizar codigos raros que merecem memo interpretativo.
- verificar cobertura do corpus.
- comparar a propria leitura do LLM com padroes de distribuicao.

Nao use frequencia para:
- decidir importancia automatica.
- descartar codigo raro.
- promover codigo frequente a tema.
- afirmar representatividade estatistica.
- esconder contradicoes minoritarias.

Rotule graficos/tabelas como "Auditoria exploratoria de frequencia" ou "Cobertura dos codigos por fonte", nunca como "temas mais importantes".

## Melhor Padrao Para Agentes Simples

Use apenas dois scripts:
- `scripts/gerar_diagramas.py` para funcoes de visualizacao, frequencia e verificacao.
- `scripts/gerar_saida_final.py` para gerar artefatos a partir de JSON externo.

Evite criar scripts novos para cada estudo. Se um estudo precisar de dados, salve os dados em JSON fora de `scripts/`.

## Graphviz/DOT Para Markdown

Use Graphviz quando precisar de hierarquia clara e roteamento automatico:
- mapa tematico inicial.
- mapa tematico final.
- fluxo de decisoes.
- trilha de revisao.

Use fence `dot`, nao `graphviz`:

```dot
digraph exemplo {
  graph [rankdir=LR, splines=ortho, nodesep="0.35", ranksep="0.75"];
  node [shape=box, style="rounded,filled", fillcolor="#f5f7fa", color="#ccd3dc"];
  tema [label="Tema interpretativo", fillcolor="#264653", fontcolor="white"];
  subtema [label="Subtema"];
  categoria [label="Categoria"];
  codigo [label="Codigo", shape=note, fillcolor="#fff8e6"];
  tema -> subtema -> categoria -> codigo;
}
```

Para gerar automaticamente, use `gerar_dot_mapa_tematico()` em `scripts/gerar_diagramas.py`.

## Matplotlib/SVG Para DOCX

Use SVG/PNG quando o resultado precisa entrar em DOCX ou PDF. As funcoes ja existentes em `gerar_diagramas.py` devem ser preferidas:
- `gerar_rede_codigos()` para co-ocorrencia/cobertura.
- `gerar_mapa_tematico()` para mapa inicial.
- `gerar_diagrama_evolucao()` para comparar Fase 3 e Fase 4.
- `gerar_diagrama_relacoes()` para relacoes entre temas.
- `gerar_diagrama_trajetoria()` para caminho codigos -> categorias -> temas.
- `gerar_mapa_final()` para mapa final.

## Boas Praticas De Data Viz

- Titulo deve dizer o que o grafico mostra.
- Subtitulo ou nota deve declarar limitacao metodologica quando houver frequencia.
- Use labels diretos; evite legenda quando o label no proprio elemento resolver.
- Use paleta segura para daltonismo.
- Use poucas cores: cor deve codificar nivel, fase ou tipo de relacao.
- Evite 3D, pizza, gradientes decorativos, sombras e efeitos ornamentais.
- Ordene tabelas/graficos por criterio claro.
- Nunca use area/tamanho exagerado para sugerir importancia qualitativa.
- Em graficos de frequencia, prefira tabela, dot plot ou barra horizontal discreta.

## Schema JSON Minimo Para `gerar_saida_final.py`

```json
{
  "codigos_por_documento": {
    "doc-1": ["codigo A", "codigo B"]
  },
  "temas": [
    {
      "nome": "Tema interpretativo",
      "subtemas": [
        {
          "nome": "Subtema",
          "categorias": [
            {"nome": "Categoria", "codigos": ["codigo A"]}
          ]
        }
      ]
    }
  ],
  "estado_inicial": {"temas": [{"nome": "Tema inicial", "codigos": ["C1"]}]},
  "estado_revisado": {"temas": [{"nome": "Tema revisado", "codigos": ["C1"]}]},
  "relacoes": [
    {"de": "Tema interpretativo", "para": "Outro tema", "tipo": "tensao", "descricao": "o que tensiona"}
  ],
  "trajetoria": {"codigos_iniciais": 10, "categorias_emergentes": 5, "subtemas": 4, "temas_finais": 3},
  "itens_por_etapa": {
    "codigos": ["C1: exemplo"],
    "categorias": ["Categoria"],
    "subtemas": ["Subtema"],
    "temas": ["Tema"]
  }
}
```

Comando:

```powershell
python scripts\gerar_saida_final.py --input analise_atr.json --outdir output-analise --fases-dir output-analise
```
