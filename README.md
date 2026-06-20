# Análise Temática Reflexiva

Skill pública em português para conduzir **Análise Temática Reflexiva (ATR)** com agentes de IA, com foco em rigor metodológico, verificação literal de extratos, trilha de auditoria, visualizações e saída final reutilizável.

Todo o conteúdo deste repositório está licenciado sob **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Consulte [LICENSE](LICENSE).

## O que esta skill faz

- conduz ATR em 7 fases obrigatórias, da decisão metodológica ao relatório final;
- bloqueia atalhos metodológicos comuns, como pular familiarização ou aceitar temas que são apenas resumos de domínio;
- exige extratos literais verificáveis;
- fornece templates para cada fase analítica;
- inclui scripts Python para gerar diagramas, tabelas e DOCX de apoio;
- traz cenários adversariais e testes executáveis para validar o comportamento da skill.

## Para quem serve

- pesquisadoras e pesquisadores que trabalham com entrevistas, grupos focais, documentos, diários e outros dados qualitativos;
- equipes que desejam usar agentes de IA sem abrir mão de checkpoints metodológicos claros;
- laboratórios e grupos de pesquisa que querem reaproveitar uma skill ATR já documentada e testada.

## Estrutura do repositório

- `SKILL.md`: instrução principal da skill.
- `agents/`: metadados para integração com agentes.
- `referencias/`: referências metodológicas e regras de visualização.
- `templates/`: modelos de saída por fase.
- `scripts/`: utilitários Python para diagramas e geração de artefatos.
- `testes/`: suíte de testes executáveis e cenários adversariais.

## Como instalar

Copie a pasta deste repositório para a pasta de skills do seu ambiente. Exemplos comuns:

- `$CODEX_HOME/skills/analise-tematica-reflexiva`
- `~/.agents/skills/analise-tematica-reflexiva`

Se o seu ambiente usa outra convenção, mantenha a estrutura interna do repositório intacta.

## Dependências dos scripts

Instale as dependências Python listadas em `requirements.txt`.

Exemplo:

```bash
pip install -r requirements.txt
```

## Como validar

Rode os checks abaixo a partir da raiz do repositório:

```bash
python -m py_compile scripts/gerar_diagramas.py scripts/gerar_saida_final.py
python -m unittest testes.test_scripts
```

Se você usa esta skill dentro de um ambiente com validador próprio de skills, rode também a validação nativa desse ambiente.

## Como citar

Citação preferencial:

> Sampaio, Rafael. Análise Temática Reflexiva. Skill para agentes de codificação. 2026. Disponível em: https://github.com/labiia-lab/analise-tematica-reflexiva

O repositório também inclui `CITATION.cff`, para permitir citação estruturada pela interface do GitHub.

## Licença

Este repositório é distribuído sob a licença **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
