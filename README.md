# Análise Temática Reflexiva

Skill pública em português para conduzir **Análise Temática Reflexiva (ATR)**
com agentes de IA. O pacote foi desenhado para executar uma análise autônoma
completa quando solicitado, mantendo rastreabilidade suficiente para revisão,
contestação, complementação e validação humana.

## O que a skill faz

- organiza F0–F6: constituição, familiarização, codificação, temas candidatos,
  contestação, definição e relatório;
- constrói temas como padrões de significado, sem número mínimo de temas e sem
  tratar frequência ou assunto como tema;
- separa quem constrói a leitura de quem a contesta e de quem a avalia: analista
  rival, contestador e avaliador trabalham em contextos limpos quando o ambiente
  permite, e ficam rotulados como `informada` e `autoavaliação` quando não;
- mantém um registro único de evidências que liga fonte, excerto, código e tema,
  e gera dele as tabelas de genealogia;
- verifica literalmente cada excerto no momento da codificação e confere que
  toda citação do relatório está no registro;
- distingue fala de participante, texto, documento, nota de mediador e resumo
  de segunda mão, e impede que registro mediado seja citado como fala;
- contesta cada tema com condições de derrota escritas por quem contesta, caça
  à contraevidência e testes de exclusão e de fusão, e declara quando a
  contestação não mudou o mapa;
- entrega relatório analítico e dossiê de auditoria em arquivos separados;
- confere identificadores pessoais na saída e devolve a decisão ao usuário;
- isola casos em estudos com várias cidades, grupos ou instituições e mede a
  semelhança entre os relatórios;
- oferece rotas autônoma, por checkpoints, de início humano e paralela cega.

A skill não transforma uma execução de IA em validação humana, consenso,
triangulação ou aprovação ética. Esses estatutos precisam ser declarados de
acordo com o que realmente ocorreu.

## Estrutura

- `SKILL.md`: contrato principal da execução.
- `referencias/`: documentos metodológicos carregados progressivamente
  (fundamentos, execução e isolamento, evidências e relato, qualidade, rubrica
  e âncoras, contestabilidade, casos múltiplos, IA em ATR etc.).
- `templates/`: roteiros de campos para F0–F6, dossiê de auditoria e síntese
  comparativa entre casos.
- `scripts/verificar_citacoes.py`: inventário do corpus e verificação literal
  de citações.
- `scripts/auditar_analise.py`: auditoria da parte computável da análise
  (integridade do registro, citações do relatório, cobertura de leitura,
  distribuição da evidência, identificadores pessoais, sobrealegação,
  semelhança entre casos e teste de aptidão do modelo).
- `testes/`: 28 cenários comportamentais e testes automatizados.
- `CHANGELOG.md`: notas de versão.

Os scripts usam apenas a biblioteca padrão do Python.

## Instalação

Clone ou copie o conteúdo deste repositório para o diretório de skills do seu
agente, preservando `SKILL.md` na raiz da pasta. O caminho de descoberta varia
entre ambientes; OpenCode, por exemplo, pode carregar a pasta local em
`.agents/skills/analise-tematica-reflexiva/`. Não é necessário conhecimento de
programação para executar a análise.

```bash
git clone --depth 1 https://github.com/labiia-lab/analise-tematica-reflexiva.git
# copie a pasta resultante para o diretório de skills do agente, preservando
# SKILL.md na raiz (ex.: .agents/skills/analise-tematica-reflexiva/)
```

## Validação local

A partir da raiz do repositório:

```bash
python -m py_compile scripts/verificar_citacoes.py scripts/auditar_analise.py
python -m unittest discover -s testes -p "test_*.py"
```

Os scripts conferem a trilha da análise; não medem qualidade interpretativa
nem substituem leitura qualitativa ou julgamento humano.
Os cenários comportamentais tornam falhas observáveis, mas não constituem
prova automática de validade científica.

## Como citar

> Sampaio, Rafael. *Análise Temática Reflexiva*. Skill para agentes de IA.
> Versão 2.0.0, 2026. https://github.com/labiia-lab/analise-tematica-reflexiva

Consulte também `CITATION.cff`.

## Licença

Creative Commons Attribution 4.0 International (CC BY 4.0). Consulte
[`LICENSE`](LICENSE).
