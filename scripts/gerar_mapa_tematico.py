#!/usr/bin/env python3
"""Gera o mapa temático em três colunas como SVG vetorial e PNG.

Entrada: JSON com a estrutura da análise (códigos, temas candidatos, temas
finais e relações). Saídas: SVG editável e PNG de 1448 x 1086 px, prontos para
inserir em página A4 ou slide, entre meia e uma lauda.

Esquema mínimo:

{
  "codigos": {
    "rotulo": "Códigos",
    "itens": [{"id": "1", "texto": "Identificar requisitos de tolerância"}]
  },
  "temas_candidatos": {
    "rotulo": "Temas candidatos",
    "itens": [{"id": "1", "texto": "...", "codigos": ["1"], "grupo": 1}]
  },
  "temas_finais": {
    "rotulo": "Temas finais",
    "itens": [{"id": "TF1", "rotulo": "Tema 1", "texto": "IDENTIFICAÇÃO",
               "candidatos": ["1"], "grupo": 1}]
  }
}

Campos opcionais por item: "linhas" (quebras manuais, lista de strings) e
"grupo" (número; grupos diferentes ganham vazio vertical extra).

Encaixe do texto: antes de renderizar, cada linha é medida com a fonte real
(Georgia, via Pillow). Se exceder a largura útil da caixa, a fonte é reduzida
em passos de 0,5 px até caber; se não couber nem na fonte mínima, o item é
reportado. Nenhuma letra deve ficar fora do quadro.

PNG: além do SVG, um PNG 1448 x 1086 é sempre produzido. A exportação tenta
cairosvg, Inkscape e, por fim, o renderizador nativo com Pillow.

Regras: cada código precisa de ao menos um tema candidato de destino e cada
tema candidato precisa de ao menos um tema final. Relações quebradas são erro.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

LARGURA = 1448.0
ALTURA = 1086.0
MARGEM_SUPERIOR = 8.0
MARGEM_INFERIOR = 12.0
ALTURA_CABECALHO = 41.0
TOPO_CONTEUDO = MARGEM_SUPERIOR + ALTURA_CABECALHO + 10.0

FUNDO = "#FEFEFE"
COR_SETA = "#4E5A61"
ESPESSURA_SETA = 1.5
PONTA_COMPRIMENTO = 10.0
PONTA_LARGURA = 7.0

MARGEM_INTERNA_H = 14.0
PASSO_FONTE = 0.5
FONTE_MINIMA = 10.0
SUPERSAMPLE = 2

CABECALHO = {
    "preenchimento_topo": "#E1E7EC",
    "preenchimento_base": "#D1DCE6",
    "contorno": "#8799A8",
    "espessura": 1.1,
    "raio": 6.0,
    "cor_texto": "#101E32",
    "fonte": 26.0,
    "peso": 700,
    "largura_temas_finais": 290.0,
}

COLUNAS = {
    "codigos": {
        "x": 24.0,
        "largura": 421.0,
        "fonte": 17.5,
        "entrelinha": 21.0,
        "respiro_vertical": 8.0,
        "gap": 8.0,
        "gap_grupo": 6.0,
        "gap_minimo": 3.0,
        "max_caracteres": 40,
        "max_linhas": 3,
        "peso": 400,
        "preenchimento_topo": "#F4F4F3",
        "preenchimento_base": "#ECEEEE",
        "contorno": "#AAB5BE",
        "espessura": 1.2,
        "raio": 6.0,
        "cor_texto": "#132033",
        "rotulo_padrao": "Códigos",
    },
    "temas_candidatos": {
        "x": 567.0,
        "largura": 428.0,
        "fonte": 17.5,
        "entrelinha": 22.0,
        "respiro_vertical": 10.0,
        "gap": 8.0,
        "gap_grupo": 6.0,
        "gap_minimo": 3.0,
        "max_caracteres": 43,
        "max_linhas": 3,
        "peso": 400,
        "preenchimento_topo": "#F4F4F3",
        "preenchimento_base": "#ECEEEE",
        "contorno": "#87949D",
        "espessura": 1.2,
        "raio": 7.0,
        "cor_texto": "#132033",
        "rotulo_padrao": "Temas candidatos",
    },
    "temas_finais": {
        "x": 1169.0,
        "largura": 257.0,
        "fonte": 23.0,
        "fonte_rotulo": 19.0,
        "entrelinha": 27.0,
        "respiro_vertical": 12.0,
        "gap": 14.0,
        "gap_grupo": 10.0,
        "gap_minimo": 6.0,
        "max_caracteres": 20,
        "max_linhas": 4,
        "peso": 700,
        "preenchimento_topo": "#DEE7EE",
        "preenchimento_base": "#D0DDE7",
        "contorno": "#214966",
        "espessura": 2.75,
        "raio": 9.0,
        "cor_texto": "#0D1C31",
        "rotulo_padrao": "Temas finais",
    },
}

REFERENCIAS_CHAVE = {
    "temas_candidatos": "codigos",
    "temas_finais": "candidatos",
}

_CACHE_FONTES: dict[tuple[str, float], object] = {}
_CACHE_MEDIDAS: dict[tuple[str, float, int], float | None] = {}


def _id_seguro(valor: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "-", valor)


def quebrar_texto(texto: str, maximo: int) -> list[str]:
    palavras = texto.split()
    if not palavras:
        return [""]
    linhas: list[str] = []
    atual = ""
    for palavra in palavras:
        candidato = palavra if not atual else f"{atual} {palavra}"
        if len(candidato) <= maximo or not atual:
            atual = candidato
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    if len(linhas) >= 2 and len(linhas[-1].split()) == 1 and len(linhas[-2].split()) >= 2:
        anterior = linhas[-2].split()
        movida = anterior.pop()
        linhas[-2] = " ".join(anterior)
        linhas[-1] = f"{movida} {linhas[-1]}"
    return linhas


def largura_estimada(texto: str, fonte: float, peso: int) -> float:
    """Estimativa de largura em px; usada somente quando Pillow não está disponível."""
    fator = 0.56 if peso >= 700 else 0.50
    return len(texto) * fonte * fator


def _hex_para_rgb(valor: str) -> tuple[int, int, int]:
    valor = valor.lstrip("#")
    return tuple(int(valor[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _carregar_fonte(tamanho: float, peso: int):
    if tamanho <= 0:
        return None
    try:
        from PIL import ImageFont
    except ImportError:
        return None
    nomes = (
        ["georgiab.ttf", "georgia.ttf"]
        if peso >= 700
        else ["georgia.ttf", "georgiab.ttf"]
    )
    chave = (nomes[0], round(tamanho, 2))
    if chave in _CACHE_FONTES:
        return _CACHE_FONTES[chave]
    fonte = None
    for nome in nomes:
        try:
            fonte = ImageFont.truetype(nome, tamanho)
            break
        except OSError:
            continue
    _CACHE_FONTES[chave] = fonte
    return fonte


def medir_largura(texto: str, fonte: float, peso: int) -> float | None:
    chave = (texto, round(fonte, 2), peso)
    if chave in _CACHE_MEDIDAS:
        return _CACHE_MEDIDAS[chave]
    objeto = _carregar_fonte(fonte, peso)
    valor: float | None = None
    if objeto is not None:
        try:
            valor = float(objeto.getlength(texto))
        except Exception:
            valor = None
    _CACHE_MEDIDAS[chave] = valor
    return valor


def _largura_linha(texto: str, fonte: float, peso: int) -> float:
    medida = medir_largura(texto, fonte, peso)
    if medida is not None:
        return medida
    return largura_estimada(texto, fonte, peso)


def _offset_baseline(fonte: float, peso: int) -> float:
    objeto = _carregar_fonte(fonte, peso)
    if objeto is not None:
        try:
            ascent, descent = objeto.getmetrics()
            return (ascent - descent) / 2.0
        except Exception:
            pass
    return 0.35 * fonte


def fracoes_chegada(quantidade: int) -> list[float]:
    tabela = {
        2: [0.35, 0.65],
        3: [0.25, 0.50, 0.75],
        4: [0.20, 0.40, 0.60, 0.80],
        5: [0.15, 0.32, 0.50, 0.68, 0.85],
    }
    if quantidade <= 1:
        return [0.5] * max(quantidade, 0)
    if quantidade in tabela:
        return tabela[quantidade]
    return [0.15 + 0.70 * indice / (quantidade - 1) for indice in range(quantidade)]


def _ajustar_item(item: dict, config: dict, ajustes: list[dict], avisos: list[str]) -> None:
    """Reduz a fonte em passos de 0,5 px até todas as linhas caberem na largura útil."""
    largura_util = config["largura"] - 2 * MARGEM_INTERNA_H
    linhas = item["linhas"]

    def excede() -> bool:
        return any(
            _largura_linha(linha["texto"], linha["fonte"], linha["peso"]) > largura_util
            for linha in linhas
        )

    if not excede():
        item["altura_linhas"] = sum(linha["entrelinha"] for linha in linhas)
        return

    limite = max(linha["fonte_base"] for linha in linhas) - FONTE_MINIMA
    desconto = 0.0
    while excede() and desconto + 1e-9 < limite:
        desconto = round(desconto + PASSO_FONTE, 2)
        for linha in linhas:
            linha["fonte"] = max(FONTE_MINIMA, round(linha["fonte_base"] - desconto, 2))
            linha["entrelinha"] = linha["entrelinha_base"] * (
                linha["fonte"] / linha["fonte_base"]
            )

    item["altura_linhas"] = sum(linha["entrelinha"] for linha in linhas)
    if excede():
        avisos.append(
            f"item '{item['id']}' excede a largura mesmo na fonte mínima; "
            "reduza o texto ou aumente a caixa"
        )
        return
    if desconto > 0:
        base_principal = max(linha["fonte_base"] for linha in linhas)
        ajustes.append(
            {
                "id": item["id"],
                "fonte_base": base_principal,
                "fonte_final": round(base_principal - desconto, 2),
            }
        )


def _ajustar_cabecalho(rotulo: str, largura: float, avisos: list[str]) -> float:
    fonte = CABECALHO["fonte"]
    largura_util = largura - 2 * MARGEM_INTERNA_H
    while (
        _largura_linha(rotulo, fonte, CABECALHO["peso"]) > largura_util
        and fonte - PASSO_FONTE >= FONTE_MINIMA
    ):
        fonte = round(fonte - PASSO_FONTE, 2)
    if _largura_linha(rotulo, fonte, CABECALHO["peso"]) > largura_util:
        avisos.append(f"cabeçalho '{rotulo}' excede a largura mesmo na fonte mínima")
    return fonte


def _normalizar_item(
    item: dict,
    config: dict,
    chave_ref: str | None,
    ajustes: list[dict],
    avisos: list[str],
) -> dict:
    linhas_brutas = item.get("linhas")
    if linhas_brutas:
        textos = [str(linha) for linha in linhas_brutas]
    else:
        textos = []
        for parte in str(item.get("texto", "")).split("\n"):
            parte = parte.strip()
            if parte:
                textos.extend(quebrar_texto(parte, config["max_caracteres"]))
    for linha in textos:
        if len(linha) > config["max_caracteres"]:
            avisos.append(
                f"linha acima de {config['max_caracteres']} caracteres no item "
                f"'{item.get('id')}': {linha!r}"
            )
    if len(textos) > config["max_linhas"]:
        avisos.append(
            f"item '{item.get('id')}' com {len(textos)} linhas; "
            f"o limite editorial é {config['max_linhas']}"
        )
    linhas = [
        {
            "texto": texto,
            "fonte": config["fonte"],
            "fonte_base": config["fonte"],
            "peso": config["peso"],
            "entrelinha": config["entrelinha"],
            "entrelinha_base": config["entrelinha"],
        }
        for texto in textos
    ]
    rotulo = item.get("rotulo")
    if rotulo:
        fonte_rotulo = config.get("fonte_rotulo", config["fonte"] - 3)
        linhas.insert(
            0,
            {
                "texto": str(rotulo),
                "fonte": fonte_rotulo,
                "fonte_base": fonte_rotulo,
                "peso": 700,
                "entrelinha": config["entrelinha"],
                "entrelinha_base": config["entrelinha"],
            },
        )
    resultado = {
        "id": str(item.get("id", "")),
        "linhas": linhas,
        "grupo": item.get("grupo", 0),
        "refs": [str(ref) for ref in item.get(chave_ref, [])] if chave_ref else [],
    }
    _ajustar_item(resultado, config, ajustes, avisos)
    return resultado


def _itens(dados: dict, chave: str) -> list[dict]:
    bloco = dados.get(chave) or {}
    itens = bloco.get("itens") or []
    return [item for item in itens if isinstance(item, dict)]


def validar(dados: object) -> list[str]:
    if not isinstance(dados, dict):
        return ["a entrada precisa ser um objeto JSON"]
    erros: list[str] = []
    ids: dict[str, set[str]] = {}
    for chave in ("codigos", "temas_candidatos", "temas_finais"):
        vistos: set[str] = set()
        for item in _itens(dados, chave):
            identificador = str(item.get("id", "")).strip()
            if not identificador:
                erros.append(f"item sem id em '{chave}'")
                continue
            if identificador in vistos:
                erros.append(f"id duplicado em '{chave}': {identificador}")
            vistos.add(identificador)
        ids[chave] = vistos
    if not ids["temas_finais"]:
        erros.append("informe ao menos um tema final")
    referenciados_codigos: set[str] = set()
    referenciados_candidatos: set[str] = set()
    for item in _itens(dados, "temas_candidatos"):
        refs = item.get("codigos")
        if not isinstance(refs, list) or not refs:
            erros.append(f"tema candidato '{item.get('id')}' sem códigos de origem")
            continue
        for ref in refs:
            ref = str(ref)
            if ref not in ids["codigos"]:
                erros.append(
                    f"tema candidato '{item.get('id')}' referencia código inexistente: {ref}"
                )
            else:
                referenciados_codigos.add(ref)
    for item in _itens(dados, "temas_finais"):
        refs = item.get("candidatos")
        if not isinstance(refs, list) or not refs:
            erros.append(f"tema final '{item.get('id')}' sem temas candidatos de origem")
            continue
        for ref in refs:
            ref = str(ref)
            if ref not in ids["temas_candidatos"]:
                erros.append(
                    f"tema final '{item.get('id')}' referencia tema candidato inexistente: {ref}"
                )
            else:
                referenciados_candidatos.add(ref)
    for codigo in ids["codigos"] - referenciados_codigos:
        erros.append(f"código '{codigo}' sem tema candidato de destino")
    for candidato in ids["temas_candidatos"] - referenciados_candidatos:
        erros.append(f"tema candidato '{candidato}' sem tema final de destino")
    return erros


def layout_coluna(
    itens: list[dict], config: dict, avisos: list[str]
) -> tuple[list[dict], float]:
    if not itens:
        return [], 1.0
    disponivel = ALTURA - MARGEM_INFERIOR - TOPO_CONTEUDO
    alturas = [
        item["altura_linhas"] + 2 * config["respiro_vertical"] for item in itens
    ]
    if len(itens) == 1:
        altura = alturas[0]
        y = TOPO_CONTEUDO + max(0.0, (disponivel - altura) / 2)
        return [{"y": y, "h": altura, "it": itens[0]}], 1.0
    quebras = [
        itens[indice]["grupo"] != itens[indice + 1]["grupo"]
        for indice in range(len(itens) - 1)
    ]
    gaps = [
        config["gap"] + (config["gap_grupo"] if quebra else 0.0) for quebra in quebras
    ]
    natural = sum(alturas) + sum(gaps)
    escala = 1.0
    if natural > disponivel:
        reduzivel = sum(gap - config["gap_minimo"] for gap in gaps)
        excesso = natural - disponivel
        if reduzivel > 0 and excesso <= reduzivel:
            fator = excesso / reduzivel
            gaps = [gap - (gap - config["gap_minimo"]) * fator for gap in gaps]
        else:
            gaps = [config["gap_minimo"]] * len(gaps)
            base = sum(alturas) + sum(gaps)
            escala = disponivel / base
            if escala < 0.85:
                avisos.append(
                    "conteúdo excede uma lauda mesmo com compressão; "
                    "reduza itens ou divida o mapa em dois"
                )
            alturas = [altura * escala for altura in alturas]
            gaps = [gap * escala for gap in gaps]
    else:
        sobra = disponivel - natural
        if sobra > 0:
            pesos = [2.0 if quebra else 1.0 for quebra in quebras]
            total = sum(pesos)
            gaps = [gap + sobra * peso / total for gap, peso in zip(gaps, pesos)]
    saida: list[dict] = []
    y = TOPO_CONTEUDO
    for indice, (item, altura) in enumerate(zip(itens, alturas)):
        saida.append({"y": y, "h": altura, "it": item})
        if indice < len(gaps):
            y += altura + gaps[indice]
    return saida, escala


def layout_temas_finais(
    itens: list[dict],
    config: dict,
    layout_candidatos: list[dict],
    avisos: list[str],
) -> tuple[list[dict], float]:
    if not itens:
        return [], 1.0
    fundo = ALTURA - MARGEM_INFERIOR
    centros = {
        entrada["it"]["id"]: entrada["y"] + entrada["h"] / 2
        for entrada in layout_candidatos
    }
    alturas = [
        item["altura_linhas"] + 2 * config["respiro_vertical"] for item in itens
    ]
    posicoes: list[dict] = []
    anterior_fim: float | None = None
    for item, altura in zip(itens, alturas):
        referencia = [centros[ref] for ref in item["refs"] if ref in centros]
        alvo = (
            sum(referencia) / len(referencia)
            if referencia
            else (TOPO_CONTEUDO + fundo) / 2
        )
        y = alvo - altura / 2
        if anterior_fim is None:
            y = max(y, TOPO_CONTEUDO)
        else:
            y = max(y, anterior_fim + config["gap"])
        posicoes.append({"y": y, "h": altura, "it": item})
        anterior_fim = y + altura
    excesso = posicoes[-1]["y"] + posicoes[-1]["h"] - fundo
    if excesso > 0:
        deslocamento = min(excesso, posicoes[0]["y"] - TOPO_CONTEUDO)
        for posicao in posicoes:
            posicao["y"] -= deslocamento
        excesso = posicoes[-1]["y"] + posicoes[-1]["h"] - fundo
    if excesso > 0 and len(posicoes) > 1:
        gaps = [
            posicoes[indice + 1]["y"]
            - (posicoes[indice]["y"] + posicoes[indice]["h"])
            for indice in range(len(posicoes) - 1)
        ]
        reducivel = sum(gap - config["gap_minimo"] for gap in gaps)
        if reducivel > 0:
            fator = min(1.0, excesso / reducivel)
            deslocamento_acumulado = 0.0
            for indice in range(1, len(posicoes)):
                deslocamento_acumulado += (gaps[indice - 1] - config["gap_minimo"]) * fator
                posicoes[indice]["y"] -= deslocamento_acumulado
            excesso = posicoes[-1]["y"] + posicoes[-1]["h"] - fundo
    if excesso > 0.5:
        avisos.append(
            "temas finais excedem a altura da lauda; reduza temas ou encurte rótulos"
        )
    return posicoes, 1.0


def construir_cena(dados: dict) -> dict:
    ajustes: list[dict] = []
    avisos: list[str] = []
    layouts: dict[str, list[dict]] = {}
    escalas: dict[str, float] = {}
    for chave in ("codigos", "temas_candidatos"):
        config = COLUNAS[chave]
        itens = [
            _normalizar_item(item, config, REFERENCIAS_CHAVE.get(chave), ajustes, avisos)
            for item in _itens(dados, chave)
        ]
        posicoes, escala = layout_coluna(itens, config, avisos)
        layouts[chave] = posicoes
        escalas[chave] = escala
    config_finais = COLUNAS["temas_finais"]
    itens_finais = [
        _normalizar_item(
            item, config_finais, REFERENCIAS_CHAVE.get("temas_finais"), ajustes, avisos
        )
        for item in _itens(dados, "temas_finais")
    ]
    posicoes, escala = layout_temas_finais(
        itens_finais, config_finais, layouts["temas_candidatos"], avisos
    )
    layouts["temas_finais"] = posicoes
    escalas["temas_finais"] = escala

    caixas: list[dict] = []
    textos: list[dict] = []
    for chave in ("codigos", "temas_candidatos", "temas_finais"):
        config = COLUNAS[chave]
        bloco = dados.get(chave) or {}
        rotulo = str(bloco.get("rotulo") or config["rotulo_padrao"])
        largura_cabecalho = config["largura"]
        if chave == "temas_finais":
            largura_cabecalho = CABECALHO["largura_temas_finais"]
        x_cabecalho = config["x"] + (config["largura"] - largura_cabecalho) / 2
        fonte_cabecalho = _ajustar_cabecalho(rotulo, largura_cabecalho, avisos)
        caixas.append(
            {
                "x": x_cabecalho,
                "y": MARGEM_SUPERIOR,
                "largura": largura_cabecalho,
                "altura": ALTURA_CABECALHO,
                "raio": CABECALHO["raio"],
                "fill_topo": CABECALHO["preenchimento_topo"],
                "fill_base": CABECALHO["preenchimento_base"],
                "contorno": CABECALHO["contorno"],
                "espessura": CABECALHO["espessura"],
            }
        )
        textos.append(
            {
                "x": x_cabecalho + largura_cabecalho / 2,
                "y": MARGEM_SUPERIOR
                + ALTURA_CABECALHO / 2
                + _offset_baseline(fonte_cabecalho, CABECALHO["peso"]),
                "texto": rotulo,
                "fonte": fonte_cabecalho,
                "peso": CABECALHO["peso"],
                "cor": CABECALHO["cor_texto"],
                "largura_caixa": largura_cabecalho,
            }
        )
        escala = escalas[chave]
        for entrada in layouts[chave]:
            item = entrada["it"]
            caixas.append(
                {
                    "x": config["x"],
                    "y": entrada["y"],
                    "largura": config["largura"],
                    "altura": entrada["h"],
                    "raio": config["raio"],
                    "fill_topo": config["preenchimento_topo"],
                    "fill_base": config["preenchimento_base"],
                    "contorno": config["contorno"],
                    "espessura": config["espessura"],
                }
            )
            linhas = item["linhas"]
            total = sum(linha["entrelinha"] for linha in linhas) * escala
            acumulado = 0.0
            centro = entrada["y"] + entrada["h"] / 2
            for linha in linhas:
                fonte = linha["fonte"] * escala
                entrelinha = linha["entrelinha"] * escala
                centro_linha = centro + (acumulado + entrelinha / 2 - total / 2)
                textos.append(
                    {
                        "x": config["x"] + config["largura"] / 2,
                        "y": centro_linha + _offset_baseline(fonte, linha["peso"]),
                        "texto": linha["texto"],
                        "fonte": fonte,
                        "peso": linha["peso"],
                        "cor": config["cor_texto"],
                        "largura_caixa": config["largura"],
                    }
                )
                acumulado += entrelinha

    setas: list[dict] = []
    for origem, destino, chave in (
        (layouts["codigos"], layouts["temas_candidatos"], "codigos"),
        (layouts["temas_candidatos"], layouts["temas_finais"], "candidatos"),
    ):
        por_id = {entrada["it"]["id"]: entrada for entrada in origem}
        ordem = {entrada["it"]["id"]: indice for indice, entrada in enumerate(origem)}
        for alvo in destino:
            refs = [ref for ref in alvo["it"]["refs"] if ref in por_id]
            refs.sort(key=lambda ref: ordem[ref])
            for ref, fracao in zip(refs, fracoes_chegada(len(refs))):
                partida = por_id[ref]
                setas.append(
                    {
                        "x1": COLUNAS["codigos" if chave == "codigos" else "temas_candidatos"]["x"]
                        + COLUNAS["codigos" if chave == "codigos" else "temas_candidatos"][
                            "largura"
                        ],
                        "y1": partida["y"] + partida["h"] / 2,
                        "x2": COLUNAS["temas_candidatos" if chave == "codigos" else "temas_finais"][
                            "x"
                        ],
                        "y2": alvo["y"] + alvo["h"] * fracao,
                    }
                )

    return {
        "caixas": caixas,
        "textos": textos,
        "setas": setas,
        "avisos": avisos,
        "ajustes": ajustes,
    }


def verificar_encaixe(cena: dict) -> list[dict]:
    """Confere, após o ajuste, se alguma linha ainda ultrapassa a largura da caixa."""
    excedentes: list[dict] = []
    for texto in cena["textos"]:
        largura_caixa = texto.get("largura_caixa")
        if not largura_caixa:
            continue
        largura_util = largura_caixa - 2 * MARGEM_INTERNA_H
        if (
            _largura_linha(texto["texto"], texto["fonte"], texto["peso"])
            > largura_util + 0.5
        ):
            excedentes.append(texto)
    return excedentes


def _gradiente(identificador: str, topo: str, base: str) -> str:
    return (
        f'<linearGradient id="{identificador}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{topo}"/>'
        f'<stop offset="1" stop-color="{base}"/>'
        f"</linearGradient>"
    )


def _retangulo(
    identificador: str,
    x: float,
    y: float,
    largura: float,
    altura: float,
    preenchimento: str,
    contorno: str,
    espessura: float,
    raio: float,
) -> str:
    return (
        f'<rect id="{identificador}" x="{x:.1f}" y="{y:.1f}" '
        f'width="{largura:.1f}" height="{altura:.1f}" rx="{raio:.1f}" '
        f'fill="{preenchimento}" stroke="{contorno}" stroke-width="{espessura:.2f}"/>'
    )


def _texto(
    x: float,
    y: float,
    conteudo: str,
    fonte: float,
    peso: int,
    cor: str,
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
        f'font-family="Georgia, Cambria, \'Source Serif 4\', \'Libre Baskerville\', '
        f'\'Times New Roman\', serif" font-size="{fonte:.1f}" '
        f'font-weight="{peso}" fill="{cor}">{escape(conteudo)}</text>'
    )


def _seta(x1: float, y1: float, x2: float, y2: float) -> str:
    dx = x2 - x1
    dy = y2 - y1
    comprimento = math.hypot(dx, dy)
    if comprimento == 0:
        return ""
    ux = dx / comprimento
    uy = dy / comprimento
    px = -uy
    py = ux
    base_x = x2 - PONTA_COMPRIMENTO * ux
    base_y = y2 - PONTA_COMPRIMENTO * uy
    metade = PONTA_LARGURA / 2
    pontos = " ".join(
        [
            f"{x2:.1f},{y2:.1f}",
            f"{base_x + metade * px:.1f},{base_y + metade * py:.1f}",
            f"{base_x - metade * px:.1f},{base_y - metade * py:.1f}",
        ]
    )
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{base_x:.1f}" y2="{base_y:.1f}" '
        f'stroke="{COR_SETA}" stroke-width="{ESPESSURA_SETA}"/>'
        f'<polygon points="{pontos}" fill="{COR_SETA}"/>'
    )


def renderizar_svg(cena: dict) -> str:
    defs = "".join(
        [
            _gradiente(
                "grad-cabecalhos",
                CABECALHO["preenchimento_topo"],
                CABECALHO["preenchimento_base"],
            ),
            _gradiente(
                "grad-codigos",
                COLUNAS["codigos"]["preenchimento_topo"],
                COLUNAS["codigos"]["preenchimento_base"],
            ),
            _gradiente(
                "grad-temas-candidatos",
                COLUNAS["temas_candidatos"]["preenchimento_topo"],
                COLUNAS["temas_candidatos"]["preenchimento_base"],
            ),
            _gradiente(
                "grad-temas-finais",
                COLUNAS["temas_finais"]["preenchimento_topo"],
                COLUNAS["temas_finais"]["preenchimento_base"],
            ),
        ]
    )
    retangulos: list[str] = []
    textos: list[str] = []
    for indice, caixa in enumerate(cena["caixas"]):
        if indice == 0 or caixa["y"] == MARGEM_SUPERIOR:
            preenchimento = "url(#grad-cabecalhos)"
            identificador = f"cabecalho-{indice}"
        elif caixa["x"] == COLUNAS["codigos"]["x"]:
            preenchimento = "url(#grad-codigos)"
            identificador = f"caixa-codigos-{indice}"
        elif caixa["x"] == COLUNAS["temas_candidatos"]["x"]:
            preenchimento = "url(#grad-temas-candidatos)"
            identificador = f"caixa-temas-candidatos-{indice}"
        else:
            preenchimento = "url(#grad-temas-finais)"
            identificador = f"caixa-temas-finais-{indice}"
        retangulos.append(
            _retangulo(
                identificador,
                caixa["x"],
                caixa["y"],
                caixa["largura"],
                caixa["altura"],
                preenchimento,
                caixa["contorno"],
                caixa["espessura"],
                caixa["raio"],
            )
        )
    for texto in cena["textos"]:
        textos.append(
            _texto(
                texto["x"],
                texto["y"],
                texto["texto"],
                texto["fonte"],
                texto["peso"],
                texto["cor"],
            )
        )
    setas = [_seta(seta["x1"], seta["y1"], seta["x2"], seta["y2"]) for seta in cena["setas"]]
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(LARGURA)}" '
            f'height="{int(ALTURA)}" viewBox="0 0 {int(LARGURA)} {int(ALTURA)}">',
            f'<rect width="{int(LARGURA)}" height="{int(ALTURA)}" fill="{FUNDO}"/>',
            f"<defs>{defs}</defs>",
            '<g id="caixas">',
            *retangulos,
            "</g>",
            '<g id="setas">',
            *setas,
            "</g>",
            '<g id="textos">',
            *textos,
            "</g>",
            "</svg>",
        ]
    )


def _png_caixa(imagem, desenho, caixa: dict, ss: int) -> None:
    from PIL import Image, ImageDraw

    x = int(round(caixa["x"] * ss))
    y = int(round(caixa["y"] * ss))
    largura = max(1, int(round(caixa["largura"] * ss)))
    altura = max(1, int(round(caixa["altura"] * ss)))
    topo = _hex_para_rgb(caixa["fill_topo"])
    base = _hex_para_rgb(caixa["fill_base"])
    gradiente = Image.new("RGB", (largura, altura), topo)
    if altura > 1 and topo != base:
        gd = ImageDraw.Draw(gradiente)
        for j in range(altura):
            t = j / (altura - 1)
            cor = tuple(int(round(a + (b - a) * t)) for a, b in zip(topo, base))
            gd.line([(0, j), (largura, j)], fill=cor)
    raio = int(round(caixa["raio"] * ss))
    mascara = Image.new("L", (largura, altura), 0)
    md = ImageDraw.Draw(mascara)
    try:
        md.rounded_rectangle([0, 0, largura - 1, altura - 1], radius=raio, fill=255)
    except AttributeError:
        md.rectangle([0, 0, largura - 1, altura - 1], fill=255)
    imagem.paste(gradiente, (x, y), mascara)
    largura_borda = max(1, int(round(caixa["espessura"] * ss)))
    try:
        desenho.rounded_rectangle(
            [x, y, x + largura - 1, y + altura - 1],
            radius=raio,
            outline=_hex_para_rgb(caixa["contorno"]),
            width=largura_borda,
        )
    except AttributeError:
        desenho.rectangle(
            [x, y, x + largura - 1, y + altura - 1],
            outline=_hex_para_rgb(caixa["contorno"]),
            width=largura_borda,
        )


def _png_seta(desenho, seta: dict, ss: int) -> None:
    x1, y1, x2, y2 = (seta[chave] * ss for chave in ("x1", "y1", "x2", "y2"))
    dx = x2 - x1
    dy = y2 - y1
    comprimento = math.hypot(dx, dy)
    if comprimento == 0:
        return
    ux = dx / comprimento
    uy = dy / comprimento
    recuo = PONTA_COMPRIMENTO * ss
    base_x = x2 - recuo * ux
    base_y = y2 - recuo * uy
    desenho.line(
        [(x1, y1), (base_x, base_y)],
        fill=_hex_para_rgb(COR_SETA),
        width=max(1, int(round(ESPESSURA_SETA * ss))),
    )
    px = -uy
    py = ux
    metade = (PONTA_LARGURA * ss) / 2
    desenho.polygon(
        [
            (x2, y2),
            (base_x + metade * px, base_y + metade * py),
            (base_x - metade * px, base_y - metade * py),
        ],
        fill=_hex_para_rgb(COR_SETA),
    )


def _png_texto(desenho, texto: dict, ss: int) -> None:
    from PIL import ImageFont

    tamanho = texto["fonte"] * ss
    fonte = _carregar_fonte(tamanho, texto["peso"])
    if fonte is None:
        try:
            fonte = ImageFont.load_default(size=int(round(tamanho)))
        except TypeError:
            fonte = ImageFont.load_default()
    x = texto["x"] * ss
    y = texto["y"] * ss
    try:
        desenho.text(
            (x, y),
            texto["texto"],
            font=fonte,
            fill=_hex_para_rgb(texto["cor"]),
            anchor="ms",
        )
    except Exception:
        largura = desenho.textlength(texto["texto"], font=fonte)
        try:
            ascent, _ = fonte.getmetrics()
        except Exception:
            ascent = int(round(tamanho))
        desenho.text(
            (x - largura / 2.0, y - ascent),
            texto["texto"],
            font=fonte,
            fill=_hex_para_rgb(texto["cor"]),
        )


def renderizar_png(cena: dict, destino: Path) -> None:
    from PIL import Image, ImageDraw

    ss = SUPERSAMPLE
    imagem = Image.new(
        "RGB", (int(LARGURA * ss), int(ALTURA * ss)), _hex_para_rgb(FUNDO)
    )
    desenho = ImageDraw.Draw(imagem)
    for caixa in cena["caixas"]:
        _png_caixa(imagem, desenho, caixa, ss)
    for seta in cena["setas"]:
        _png_seta(desenho, seta, ss)
    for texto in cena["textos"]:
        _png_texto(desenho, texto, ss)
    final = imagem.resize((int(LARGURA), int(ALTURA)), Image.LANCZOS)
    final.save(destino, "PNG")


def exportar_png(
    svg: str, cena: dict, svg_path: Path, destino: Path
) -> str | None:
    try:
        import cairosvg

        cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            write_to=str(destino),
            output_width=int(LARGURA),
            output_height=int(ALTURA),
        )
        return "cairosvg"
    except ImportError:
        pass
    except Exception:
        pass
    inkscape = shutil.which("inkscape")
    if inkscape:
        try:
            subprocess.run(
                [
                    inkscape,
                    str(svg_path),
                    "--export-type=png",
                    f"--export-filename={destino}",
                    f"--export-width={int(LARGURA)}",
                    f"--export-height={int(ALTURA)}",
                ],
                check=True,
            )
            return "inkscape"
        except Exception:
            pass
    try:
        renderizar_png(cena, destino)
        return "pillow"
    except ImportError:
        return None
    except Exception as exc:
        print(f"[erro] PNG nativo falhou: {exc}", file=sys.stderr)
        return None


def construir_svg(dados: dict) -> tuple[str, list[str]]:
    cena = construir_cena(dados)
    return renderizar_svg(cena), cena["avisos"]


def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", required=True, type=Path, help="JSON da estrutura")
    parser.add_argument("--output", required=True, type=Path, help="SVG de saída")
    parser.add_argument(
        "--png",
        type=Path,
        help="PNG de saída (padrão: mesmo nome do SVG com extensão .png)",
    )
    args = parser.parse_args(argv)

    try:
        dados = json.loads(args.input.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[erro] entrada inválida: {exc}", file=sys.stderr)
        return 2
    erros = validar(dados)
    if erros:
        for erro in erros:
            print(f"[erro] {erro}", file=sys.stderr)
        return 2

    cena = construir_cena(dados)
    excedentes = verificar_encaixe(cena)
    for aviso in cena["avisos"]:
        print(f"[aviso] {aviso}", file=sys.stderr)
    for texto in excedentes:
        print(
            f"[aviso] texto fora do quadro: {texto['texto']!r} "
            f"(fonte {texto['fonte']:.1f} px)",
            file=sys.stderr,
        )
    for ajuste in cena["ajustes"]:
        print(
            f"[info] fonte reduzida no item '{ajuste['id']}': "
            f"{ajuste['fonte_base']:.1f} -> {ajuste['fonte_final']:.1f} px",
            file=sys.stderr,
        )

    svg = renderizar_svg(cena)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(f"SVG: {args.output}")

    destino_png = args.png or args.output.with_suffix(".png")
    destino_png.parent.mkdir(parents=True, exist_ok=True)
    motor = exportar_png(svg, cena, args.output, destino_png)
    if motor is None:
        print(
            "[erro] PNG não gerado: instale Pillow (pip install pillow), "
            "cairosvg ou Inkscape para produzir o PNG obrigatório.",
            file=sys.stderr,
        )
        return 3
    print(f"PNG ({motor}): {destino_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
