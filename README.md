# Análise Temática Reflexiva

Skill pública em português para conduzir **Análise Temática Reflexiva (ATR)**
com agentes de IA. O pacote foi desenhado para executar uma análise autônoma
completa quando solicitado, mantendo rastreabilidade suficiente para revisão,
contestação, complementação e validação humana.

## O que a skill faz

- organiza F0–F6: constituição, familiarização, codificação, temas candidatos,
  contestação, definição e relatório;
- constrói temas como padrões de significado, sem tratar frequência ou domínio
  temático como tema por si só;
- exige uma rival interpretativa forte, condições de derrota e resíduos
  experienciais;
- separa cobertura, evidência, contestação, participação humana, validação e
  prontidão no estatuto final;
- verifica literalmente os excertos publicados quando o corpus acessível
  permite;
- registra proveniência, delegação de IA, limites, privacidade e intervenções;
- oferece rotas autônoma, por checkpoints, de início humano e paralela cega.

A skill não transforma uma execução de IA em validação humana, consenso,
triangulação ou aprovação ética. Esses estatutos precisam ser declarados de
acordo com o que realmente ocorreu.

## Estrutura

- `SKILL.md`: contrato principal da execução.
- `referencias/`: sete documentos metodológicos carregados progressivamente.
- `templates/`: um template para cada fase F0–F6.
- `scripts/verificar_citacoes.py`: inventário do corpus e verificação literal
  de citações, usando apenas a biblioteca padrão do Python.
- `testes/`: 21 cenários adversariais e testes de integridade.

## Instalação

Clone ou copie o conteúdo deste repositório para o diretório de skills do seu
agente, preservando `SKILL.md` na raiz da pasta. O caminho de descoberta varia
entre ambientes; OpenCode, por exemplo, pode carregar a pasta local em
`.agents/skills/analise-tematica-reflexiva/`. Não é necessário conhecimento de
programação para executar a análise.

## Validação local

A partir da raiz do repositório:

```bash
python -m py_compile scripts/verificar_citacoes.py
python -m unittest discover -s testes -p "test_*.py"
```

O script de citações não substitui leitura qualitativa nem julgamento humano.
Os cenários comportamentais tornam falhas observáveis, mas não constituem
prova automática de validade científica.

## Como citar

> Sampaio, Rafael. *Análise Temática Reflexiva*. Skill para agentes de IA.
> 2026. https://github.com/labiia-lab/analise-tematica-reflexiva

Consulte também `CITATION.cff`.

## Licença

Creative Commons Attribution 4.0 International (CC BY 4.0). Consulte
[`LICENSE`](LICENSE).
