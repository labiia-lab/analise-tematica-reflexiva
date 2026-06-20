#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera outputs visuais e DOCX para uma análise temática reflexiva a partir de JSON.

Uso:
    python scripts/gerar_saida_final.py --input analise_atr.json --outdir output-analise

O JSON pode conter:
    codigos_por_documento, temas, estado_inicial, estado_revisado, relacoes,
    trajetoria, itens_por_etapa, temas_finais, fases_markdown.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gerar_diagramas import (
    gerar_diagrama_evolucao,
    gerar_diagrama_relacoes,
    gerar_diagrama_trajetoria,
    gerar_docx_fase,
    gerar_mapa_final,
    gerar_mapa_tematico,
    gerar_rede_codigos,
)


FASES_PADRAO = [
    ("01-notas-familiarizacao.md", "Fase 1 - Notas de Familiarizacao"),
    ("02-codebook-inicial.md", "Fase 2 - Codebook Inicial"),
    ("03-temas-candidatos.md", "Fase 3 - Temas Candidatos"),
    ("04-revisao-temas.md", "Fase 4 - Revisao de Temas"),
    ("05-definicao-temas.md", "Fase 5 - Definicao dos Temas Finais"),
    ("06-relatorio-final.md", "Fase 6 - Relatorio Final"),
]


def carregar_dados(input_path: str | os.PathLike) -> dict:
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {path}")
    with path.open("r", encoding="utf-8") as f:
        dados = json.load(f)
    if not isinstance(dados, dict):
        raise ValueError("O arquivo de entrada deve conter um objeto JSON.")
    return dados


def gerar_diagramas(dados: dict, outdir: str | os.PathLike) -> dict:
    outdir = Path(outdir)
    svg_dir = outdir / "diagramas"
    svg_dir.mkdir(parents=True, exist_ok=True)
    svgs = {}

    if dados.get("codigos_por_documento"):
        svgs["rede"] = str(svg_dir / "rede_coocorrencia.svg")
        gerar_rede_codigos(dados["codigos_por_documento"], svgs["rede"])

    if dados.get("temas"):
        svgs["mapa"] = str(svg_dir / "mapa_tematico.svg")
        gerar_mapa_tematico(dados["temas"], svgs["mapa"])

    if dados.get("estado_inicial") and dados.get("estado_revisado"):
        svgs["evolucao"] = str(svg_dir / "diagrama_evolucao.svg")
        gerar_diagrama_evolucao(dados["estado_inicial"], dados["estado_revisado"], svgs["evolucao"])

    if dados.get("temas") and dados.get("relacoes"):
        svgs["relacoes"] = str(svg_dir / "diagrama_relacoes.svg")
        gerar_diagrama_relacoes(dados["temas"], dados["relacoes"], svgs["relacoes"])

    if dados.get("trajetoria"):
        svgs["trajetoria"] = str(svg_dir / "diagrama_trajetoria.svg")
        gerar_diagrama_trajetoria(
            dados["trajetoria"],
            itens_por_etapa=dados.get("itens_por_etapa"),
            output_path=svgs["trajetoria"],
        )

    temas_finais = dados.get("temas_finais") or dados.get("temas")
    if temas_finais:
        svgs["mapa_final"] = str(svg_dir / "mapa_final.svg")
        gerar_mapa_final(temas_finais, svgs["mapa_final"])

    return svgs


def gerar_documentos(
    fases_dir: str | os.PathLike,
    outdir: str | os.PathLike,
    diagramas_svg: list[str],
    fases_markdown: list[tuple[str, str]] | None = None,
) -> list[str]:
    fases_dir = Path(fases_dir)
    outdir = Path(outdir)
    gerados = []

    for md_name, titulo in (fases_markdown or FASES_PADRAO):
        md_path = fases_dir / md_name
        if not md_path.exists():
            continue
        conteudo = md_path.read_text(encoding="utf-8")
        docx_path = outdir / md_name.replace(".md", ".docx")
        gerar_docx_fase(titulo, conteudo, diagramas_svg, str(docx_path))
        gerados.append(str(docx_path))

    return gerados


def main() -> int:
    parser = argparse.ArgumentParser(description="Gerar outputs ATR a partir de um JSON de analise.")
    parser.add_argument("--input", required=True, help="JSON com dados estruturados da analise.")
    parser.add_argument("--outdir", required=True, help="Diretorio de saida.")
    parser.add_argument("--fases-dir", help="Diretorio com arquivos Markdown das fases.")
    args = parser.parse_args()

    dados = carregar_dados(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    svgs = gerar_diagramas(dados, outdir)
    print(f"Diagramas gerados: {len(svgs)}")
    for nome, path in svgs.items():
        print(f"  - {nome}: {path}")

    if args.fases_dir:
        docx = gerar_documentos(args.fases_dir, outdir, list(svgs.values()))
        print(f"DOCX gerados: {len(docx)}")
        for path in docx:
            print(f"  - {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
