#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_diagramas.py — Geração de diagramas SVG/DOCX para ATR (Braun & Clarke)

Estilo visual: ggplot-professional
- Paleta ColorBrewer qualitativa
- Grid sutil, spines removidos (top/right)
- Tipografia hierárquica com razão 1.25
- Sem chartjunk: sem sombras, gradientes decorativos, bordas desnecessárias
- Margens generosas

Dependências: matplotlib, python-docx, numpy
"""

import os
import re
import sys
import textwrap
import math
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── Configuração ggplot-professional ─────────────────────────────────────────
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica", "sans-serif"]
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.facecolor"] = "#FAFAFA"
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["grid.color"] = "#E8E8E8"
plt.rcParams["grid.linestyle"] = "-"
plt.rcParams["grid.linewidth"] = 0.4
plt.rcParams["axes.grid"] = True
plt.rcParams["axes.edgecolor"] = "#CCCCCC"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["xtick.labelsize"] = 9
plt.rcParams["ytick.labelsize"] = 9
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["figure.dpi"] = 150

# Paleta ColorBrewer qualitativa (Set2 + Dark2 combinados, 10 cores)
CORES_QUALITATIVAS = [
    "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854",
    "#FFD92F", "#E5C494", "#B3B3B3", "#1B9E77", "#D95F02",
]

CORES_SECUNDARIAS = [
    "#CCECE6", "#FDE0C4", "#D8DDEA", "#F6D2E6", "#E3F4C2",
    "#FFF2B3", "#F5E8D0", "#E0E0E0", "#A8E0CF", "#F4C2A1",
]

# Cores neutras sofisticadas (nunca #000 ou #fff puros)
C_NEUTRO_ESCURO = "#2E2E2E"
C_NEUTRO_MEDIO = "#555555"
C_NEUTRO_CLARO = "#888888"
C_FUNDO = "#FAFAFA"

FONT_MIN = 8

# ── Verificação de dependências opcionais ────────────────────────────────────

try:
    import cairosvg
    CAIROSVG_DISPONIVEL = True
except ImportError:
    CAIROSVG_DISPONIVEL = False

try:
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    DOCX_DISPONIVEL = True
except ImportError:
    DOCX_DISPONIVEL = False

try:
    from rapidfuzz import fuzz, process
    RAPIDFUZZ_DISPONIVEL = True
except ImportError:
    RAPIDFUZZ_DISPONIVEL = False

# ── Helpers ──────────────────────────────────────────────────────────────────

def _ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def _svg_para_png(svg_path: str, png_path: str, dpi: int = 200) -> str | None:
    if CAIROSVG_DISPONIVEL:
        try:
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), dpi=dpi)
            return png_path
        except Exception:
            pass
    return None


def _text_bbox(ax, texto: str, fontsize: float):
    renderer = ax.figure.canvas.get_renderer()
    t = ax.text(0, 0, texto, fontsize=fontsize, transform=ax.transData)
    bbox = t.get_window_extent(renderer=renderer)
    inv = ax.transData.inverted()
    data_bbox = bbox.transformed(inv)
    t.remove()
    return data_bbox.width, data_bbox.height


def _wrap_text(texto: str, largura: int = 30) -> str:
    return textwrap.fill(texto, width=largura, break_long_words=False, replace_whitespace=False)


def _dot_escape(texto: str) -> str:
    return str(texto).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


# ═══════════════════════════════════════════════════════════════════════════════
# 1. REDE DE CO-OCORRÊNCIA — Layout force-directed elegante
# ═══════════════════════════════════════════════════════════════════════════════

def gerar_rede_codigos(codigos_por_documento: dict, output_path: str) -> str:
    """
    Rede de co-ocorrência com layout force-directed e estilo ggplot.
    """
    _ensure_parent(output_path)

    # Cálculo de co-ocorrências e métricas
    coocorrencias = Counter()
    codigo_contagem = Counter()
    for doc_id, codigos in codigos_por_documento.items():
        codigos_unicos = list(set(codigos))
        for cod in codigos_unicos:
            codigo_contagem[cod] += 1
        for i in range(len(codigos_unicos)):
            for j in range(i + 1, len(codigos_unicos)):
                par = tuple(sorted([codigos_unicos[i], codigos_unicos[j]]))
                coocorrencias[par] += 1

    if not coocorrencias:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "Nenhuma co-ocorrência de códigos encontrada.",
                ha="center", va="center", fontsize=11, color=C_NEUTRO_MEDIO)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        fig.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close(fig)
        return output_path

    todos_codigos = sorted(codigo_contagem.keys())
    n = len(todos_codigos)

    # Layout force-directed simples (Fruchterman-Reingold-like via spring)
    pos = _force_directed_layout(todos_codigos, coocorrencias)

    # Escalar posições para área de plot [-1, 1]
    xs = [pos[c][0] for c in todos_codigos]
    ys = [pos[c][1] for c in todos_codigos]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    scale = max(max_x - min_x, max_y - min_y, 0.001)
    pos = {c: (((pos[c][0] - min_x) / scale - 0.5) * 2.2,
               ((pos[c][1] - min_y) / scale - 0.5) * 2.2) for c in todos_codigos}

    fig, ax = plt.subplots(figsize=(14, 12))
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.set_title("Rede de Co-ocorrência de Códigos", fontsize=15, fontweight="bold",
                 color=C_NEUTRO_ESCURO, pad=15)
    ax.set_facecolor(C_FUNDO)
    ax.grid(True, linestyle="-", alpha=0.3)

    max_cooc = max(coocorrencias.values()) if coocorrencias else 1
    max_cont = max(codigo_contagem.values()) if codigo_contagem else 1

    # Arestas — curvas de Bezier suaves com alpha proporcional
    for (cod_a, cod_b), freq in coocorrencias.items():
        x1, y1 = pos[cod_a]
        x2, y2 = pos[cod_b]
        alpha = 0.15 + 0.45 * (freq / max_cooc)
        lw = 0.8 + 2.5 * (freq / max_cooc)
        # Curva suave
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # Ponto de controle perpendicular
        dx, dy = x2 - x1, y2 - y1
        perp_x, perp_y = -dy, dx
        norm = math.hypot(perp_x, perp_y) or 1.0
        offset = 0.08 * (1 + 0.5 * math.sin(freq))
        cx = mx + perp_x / norm * offset
        cy = my + perp_y / norm * offset
        t = np.linspace(0, 1, 50)
        bx = (1 - t)**2 * x1 + 2 * (1 - t) * t * cx + t**2 * x2
        by = (1 - t)**2 * y1 + 2 * (1 - t) * t * cy + t**2 * y2
        ax.plot(bx, by, color=C_NEUTRO_CLARO, linewidth=lw, alpha=alpha, zorder=1)

    # Nós — pontos com tamanho proporcional à frequência
    for i, cod in enumerate(todos_codigos):
        x, y = pos[cod]
        cont = codigo_contagem[cod]
        size = 120 + 400 * (cont / max_cont)
        cor = CORES_QUALITATIVAS[i % len(CORES_QUALITATIVAS)]
        ax.scatter(x, y, s=size, c=cor, edgecolors="white", linewidths=1.5, zorder=5, alpha=0.9)

    # Labels com repel automático simples
    for i, cod in enumerate(todos_codigos):
        x, y = pos[cod]
        cor = CORES_QUALITATIVAS[i % len(CORES_QUALITATIVAS)]
        label = _wrap_text(cod, 22)
        # Posicionar label: preferencialmente acima/abaixo alternado
        offset_dir = 1 if i % 2 == 0 else -1
        label_y = y + offset_dir * 0.18
        ha = "center"
        # Se muito perto da borda, ajustar
        if x < -0.8:
            ha = "left"
        elif x > 0.8:
            ha = "right"
        ax.text(x, label_y, label, ha=ha, va="bottom" if offset_dir == 1 else "top",
                fontsize=8.5, color=C_NEUTRO_ESCURO, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=cor,
                          alpha=0.85, linewidth=0.8),
                zorder=6)

    # Legenda de tamanho
    sizes_legend = [min(max_cont, 1), max_cont // 2, max_cont]
    labels_legend = [str(s) for s in sizes_legend]
    handles = []
    for s in sizes_legend:
        size_pt = 120 + 400 * (s / max_cont)
        handles.append(ax.scatter([], [], s=size_pt, c=C_NEUTRO_MEDIO, edgecolors="white",
                                  linewidths=1.2, alpha=0.7, label=f"{s} doc(s)"))
    legend = ax.legend(handles, labels_legend, title="Frequência", loc="lower left",
                       frameon=True, fancybox=True, framealpha=0.9, edgecolor="#CCCCCC",
                       fontsize=8, title_fontsize=9)
    legend.get_title().set_fontweight("bold")

    # Nota metodológica
    fig.text(0.5, 0.01,
             "Co-ocorrência indica proximidade no corpus, não relação temática direta.",
             ha="center", fontsize=9, color=C_NEUTRO_CLARO, style="italic")

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(output_path, format="svg", bbox_inches="tight", facecolor="white")
    _png = output_path[:-4] + ".png"
    fig.savefig(_png, format="png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


def _force_directed_layout(codigos, coocorrencias, iterations=100):
    """Layout force-directed simples (spring + repulsion)."""
    pos = {}
    n = len(codigos)
    # Inicialização circular
    for i, cod in enumerate(codigos):
        ang = 2 * math.pi * i / n
        pos[cod] = (0.3 * math.cos(ang), 0.3 * math.sin(ang))

    for _ in range(iterations):
        forces = {cod: [0.0, 0.0] for cod in codigos}
        # Repulsão entre todos os pares
        for i, a in enumerate(codigos):
            for j in range(i + 1, len(codigos)):
                b = codigos[j]
                dx = pos[b][0] - pos[a][0]
                dy = pos[b][1] - pos[a][1]
                dist = math.hypot(dx, dy) + 0.001
                rep = 0.02 / dist
                forces[a][0] -= rep * dx / dist
                forces[a][1] -= rep * dy / dist
                forces[b][0] += rep * dx / dist
                forces[b][1] += rep * dy / dist
        # Atração por co-ocorrência
        for (a, b), freq in coocorrencias.items():
            dx = pos[b][0] - pos[a][0]
            dy = pos[b][1] - pos[a][1]
            dist = math.hypot(dx, dy) + 0.001
            att = 0.003 * freq * dist
            forces[a][0] += att * dx / dist
            forces[a][1] += att * dy / dist
            forces[b][0] -= att * dx / dist
            forces[b][1] -= att * dy / dist
        # Atualizar posições
        for cod in codigos:
            pos[cod] = (pos[cod][0] + forces[cod][0], pos[cod][1] + forces[cod][1])
    return pos


# ═══════════════════════════════════════════════════════════════════════════════
# 2. MAPA TEMÁTICO — Hierarquia limpa estilo ggplot
# ═══════════════════════════════════════════════════════════════════════════════

def gerar_mapa_tematico(temas: list[dict], output_path: str) -> str:
    """
    Mapa hierárquico: TEMA → Subtema → Categoria → Código.
    Estilo ggplot: grid sutil, tipografia hierárquica, cores de saturação baixa.
    """
    _ensure_parent(output_path)

    n_temas = len(temas)
    altura_total = sum(_altura_estimada_tema(t) for t in temas) + 1.5
    fig, ax = plt.subplots(figsize=(14, max(9, altura_total * 0.6)))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, altura_total)
    ax.axis("off")
    ax.set_title("Mapa Temático — Hierarquia", fontsize=15, fontweight="bold",
                 color=C_NEUTRO_ESCURO, pad=18)
    ax.set_facecolor(C_FUNDO)
    ax.grid(False)

    y_cursor = altura_total - 0.8

    for i, tema in enumerate(temas):
        cor = CORES_QUALITATIVAS[i % len(CORES_QUALITATIVAS)]
        cor_clara = CORES_SECUNDARIAS[i % len(CORES_SECUNDARIAS)]
        nome_tema = tema.get("nome", f"Tema {i + 1}")

        # Tema — barra horizontal colorida + texto (estilo ggplot facet header)
        rect = FancyBboxPatch(
            (0.2, y_cursor - 0.45), 9.6, 0.9,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            facecolor=cor, edgecolor="none", linewidth=0, zorder=5,
            alpha=0.9,
        )
        ax.add_patch(rect)
        ax.text(5, y_cursor, nome_tema, ha="center", va="center",
                fontsize=13, fontweight="bold", color="white", zorder=6)
        y_cursor -= 1.1

        itens_nivel1 = tema.get("subtemas", tema.get("categorias", []))
        for j, item1 in enumerate(itens_nivel1):
            nome_1 = item1.get("nome", f"Item {j + 1}")
            # Subtema — caixa com cor clara e borda da cor do tema
            _draw_box_text(
                ax, x=5.1, y=y_cursor - 0.32,
                texto=nome_1,
                box_w=8.4, box_h=0.62,
                facecolor=cor_clara, edgecolor=cor,
                textcolor=C_NEUTRO_ESCURO, fontsize=10.5, fontweight="bold",
                linewidth=1.0, zorder=5,
            )
            y_cursor -= 0.78

            itens_nivel2 = item1.get("categorias", item1.get("codigos", []))
            if isinstance(itens_nivel2, list):
                for k, item2 in enumerate(itens_nivel2):
                    if isinstance(item2, str):
                        nome_2 = item2
                    else:
                        nome_2 = item2.get("nome", f"Sub-item {k + 1}")

                    # Categoria — fundo quase branco, borda sutil
                    _draw_box_text(
                        ax, x=5.3, y=y_cursor - 0.24,
                        texto=nome_2,
                        box_w=7.8, box_h=0.48,
                        facecolor="#F8F8F8", edgecolor="#D0D0D0",
                        textcolor=C_NEUTRO_MEDIO, fontsize=9,
                        linewidth=0.6, zorder=5,
                    )
                    y_cursor -= 0.52

                    if isinstance(item2, dict) and "codigos" in item2:
                        codigos = item2.get("codigos", [])
                        for cod in codigos:
                            nome_cod = cod if isinstance(cod, str) else cod.get("nome", "")
                            # Código — linha única, alinhada à esquerda, truncada se necessário
                            _draw_box_text(
                                ax, x=5.55, y=y_cursor - 0.14,
                                texto=nome_cod,
                                box_w=7.8, box_h=0.28,
                                facecolor="white", edgecolor="#E0E0E0",
                                textcolor=C_NEUTRO_MEDIO, fontsize=9,
                                linewidth=0.3, zorder=5,
                                ha="left", truncar=True,
                            )
                            y_cursor -= 0.32

            y_cursor -= 0.15

        y_cursor -= 0.35

    plt.tight_layout()
    fig.savefig(output_path, format="svg", bbox_inches="tight", facecolor="white")
    _png = output_path[:-4] + ".png"
    fig.savefig(_png, format="png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


def _altura_estimada_tema(tema: dict, nivel: int = 0) -> float:
    alt = 1.1  # cabeçalho do tema
    subtemas = tema.get("subtemas", [])
    if subtemas:
        for sub in subtemas:
            alt += 0.78  # subtema
            cats = sub.get("categorias", [])
            for cat in cats:
                alt += 0.52  # categoria
                cods = cat.get("codigos", [])
                alt += len(cods) * 0.32
    else:
        cats = tema.get("categorias", [])
        for cat in cats:
            alt += 0.52
            cods = cat.get("codigos", [])
            alt += len(cods) * 0.32
    alt += 0.35
    return alt


def _draw_box_text(ax, x, y, texto: str, box_w: float, box_h: float,
                   facecolor: str, edgecolor: str, textcolor: str,
                   fontsize: float, fontweight="normal", linewidth: float = 1.0,
                   ha="center", va="center", zorder=5, truncar=False):
    rect = FancyBboxPatch(
        (x - box_w / 2, y - box_h / 2),
        box_w, box_h,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth, zorder=zorder,
    )
    ax.add_patch(rect)

    if truncar:
        # Uma linha só, trunca com ... se não couber
        fs = fontsize
        texto_final = texto
        for _ in range(4):
            tw, th = _text_bbox(ax, texto_final, fs)
            if tw <= box_w * 0.88:
                break
            # Tenta reduzir fonte
            if fs > FONT_MIN + 0.5:
                fs -= 0.5
            else:
                # Fonte mínima atingida, trunca texto
                max_chars = max(10, int(len(texto) * (box_w * 0.88 / max(tw, 0.001))) - 3)
                texto_final = texto[:max_chars] + "…"
                tw, th = _text_bbox(ax, texto_final, fs)
                if tw <= box_w * 0.88:
                    break
        # Ajusta x se alinhado à esquerda
        text_x = x - box_w / 2 + 0.15 if ha == "left" else x
        ax.text(text_x, y, texto_final, ha=ha, va=va, fontsize=fs, color=textcolor,
                fontweight=fontweight, zorder=zorder + 1)
    else:
        wrapped = _wrap_text(texto, max(14, int(box_w * 2.0)))
        fs = fontsize
        for _ in range(3):
            tw, th = _text_bbox(ax, wrapped, fs)
            if tw <= box_w * 0.92 and th <= box_h * 0.82:
                break
            fs = max(FONT_MIN, fs - 0.6)
        ax.text(x, y, wrapped, ha=ha, va=va, fontsize=fs, color=textcolor,
                fontweight=fontweight, zorder=zorder + 1, wrap=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. DIAGRAMA DE EVOLUÇÃO — Diferenças visuais claras
# ═══════════════════════════════════════════════════════════════════════════════

def gerar_diagrama_evolucao(estado_inicial: dict, estado_revisado: dict, output_path: str) -> str:
    """
    Comparativo Fase 3 → Fase 4 com destaque visual para mudanças.
    """
    _ensure_parent(output_path)

    nomes_inicial = {t["nome"] for t in estado_inicial.get("temas", [])}
    nomes_revisado = {t["nome"] for t in estado_revisado.get("temas", [])}

    adicionados = nomes_revisado - nomes_inicial
    removidos = nomes_inicial - nomes_revisado
    mantidos = nomes_inicial & nomes_revisado

    renomeados = []
    for t_ini in estado_inicial.get("temas", []):
        for t_rev in estado_revisado.get("temas", []):
            cods_ini = set(t_ini.get("codigos", []))
            cods_rev = set(t_rev.get("codigos", []))
            if cods_ini and cods_rev and cods_ini & cods_rev and t_ini["nome"] != t_rev["nome"]:
                if t_ini["nome"] not in adicionados and t_rev["nome"] not in removidos:
                    renomeados.append((t_ini["nome"], t_rev["nome"]))

    mergedados = []
    for t_rev in estado_revisado.get("temas", []):
        cods_rev = set(t_rev.get("codigos", []))
        origens = []
        for t_ini in estado_inicial.get("temas", []):
            cods_ini = set(t_ini.get("codigos", []))
            if cods_ini & cods_rev and t_ini["nome"] != t_rev["nome"]:
                origens.append(t_ini["nome"])
        if len(origens) > 1:
            mergedados.append((t_rev["nome"], origens))

    temas_ini_lista = estado_inicial.get("temas", [])
    temas_rev_lista = estado_revisado.get("temas", [])

    n_max = max(len(temas_ini_lista), len(temas_rev_lista))
    fig_h = max(8, n_max * 1.4 + 3)
    fig, axes = plt.subplots(1, 2, figsize=(16, fig_h))

    for ax in axes:
        ax.set_facecolor(C_FUNDO)
        ax.grid(False)

    def _desenhar_mapa(ax, titulo, temas_lista, col_base):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, len(temas_lista) * 2.2 + 1)
        ax.set_title(titulo, fontsize=13, fontweight="bold", color=C_NEUTRO_ESCURO, pad=12)
        ax.axis("off")

        for i, tema in enumerate(temas_lista):
            y = len(temas_lista) * 2.2 - 0.6 - i * 2.2
            nome = tema.get("nome", "?")
            codigos = tema.get("codigos", [])

            # Cor semântica: verde = novo, vermelho = removido, azul = mantido
            if nome in adicionados:
                cor = "#2A9D8F"
                label = "  [NOVO]"
            elif nome in removidos:
                cor = "#E76F51"
                label = "  [REMOVIDO]"
            else:
                cor = col_base
                label = ""

            rect = FancyBboxPatch((0.5, y - 0.45), 9, 0.9,
                                  boxstyle="round,pad=0.12", facecolor=cor,
                                  edgecolor="white", linewidth=2, alpha=0.9)
            ax.add_patch(rect)
            ax.text(5, y, nome + label, ha="center", va="center", fontsize=11,
                    fontweight="bold", color="white")

            texto_codigos = ", ".join(codigos[:5])
            if len(codigos) > 5:
                texto_codigos += f" … (+{len(codigos) - 5})"
            ax.text(5, y - 0.65, texto_codigos, ha="center", va="center",
                    fontsize=8.5, color=C_NEUTRO_MEDIO, style="italic")

    _desenhar_mapa(axes[0], "Fase 3 — Mapa Inicial", temas_ini_lista, "#264653")
    _desenhar_mapa(axes[1], "Fase 4 — Mapa Revisado", temas_rev_lista, "#2A9D8F")

    # Legenda de mudanças
    legenda = []
    if adicionados:
        legenda.append(f"Adicionados: {', '.join(adicionados)}")
    if removidos:
        legenda.append(f"Removidos: {', '.join(removidos)}")
    if renomeados:
        itens = [f"{a} → {b}" for a, b in renomeados]
        legenda.append(f"Renomeados: {', '.join(itens)}")
    if mergedados:
        itens = [f"{' + '.join(o)} → {d}" for d, o in mergedados]
        legenda.append(f"Mesclados: {', '.join(itens)}")
    if mantidos:
        legenda.append(f"Mantidos: {', '.join(mantidos)}")

    if legenda:
        fig.text(0.5, 0.02, "  |  ".join(legenda), ha="center", fontsize=10,
                 color=C_NEUTRO_MEDIO, style="italic",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#E0E0E0", alpha=0.9))

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(output_path, format="svg", bbox_inches="tight", facecolor="white")
    _png = output_path[:-4] + ".png"
    fig.savefig(_png, format="png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DIAGRAMA DE RELAÇÕES — Network circular elegante
# ═══════════════════════════════════════════════════════════════════════════════

def gerar_diagrama_relacoes(temas: list[dict], relacoes: list[dict], output_path: str) -> str:
    """
    Diagrama de rede com temas em círculo e relações como arestas curvas diferenciadas.
    """
    _ensure_parent(output_path)

    n = len(temas)
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Relações entre Temas", fontsize=15, fontweight="bold",
                 color=C_NEUTRO_ESCURO, pad=15)
    ax.set_facecolor(C_FUNDO)
    ax.grid(True, linestyle="-", alpha=0.2)

    # Posições circulares
    posicoes = {}
    raio = 1.0
    for i, tema in enumerate(temas):
        angulo = 2 * math.pi * i / n - math.pi / 2
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        posicoes[i] = (x, y)

    estilos_aresta = {
        "conexão": ("#1B9E77", "-", 2.5, 0.7),
        "tensão": ("#E78AC3", "--", 2.5, 0.7),
        "complementaridade": ("#8DA0CB", ":", 2.5, 0.7),
    }

    nomes_temas = {t.get("nome"): i for i, t in enumerate(temas)}

    # Desenhar arestas primeiro
    for rel in relacoes:
        nome_de = rel.get("de", "")
        nome_para = rel.get("para", "")
        tipo = rel.get("tipo", "conexão")
        descricao = rel.get("descricao", "")

        if nome_de in nomes_temas and nome_para in nomes_temas:
            i_de = nomes_temas[nome_de]
            i_para = nomes_temas[nome_para]
            x1, y1 = posicoes[i_de]
            x2, y2 = posicoes[i_para]
            cor, estilo, lw, alpha = estilos_aresta.get(tipo, ("#888888", "-", 1.5, 0.5))

            # Curva com rad = 0.15 para evitar sobreposição
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=cor, linestyle=estilo,
                                        lw=lw, connectionstyle="arc3,rad=0.15",
                                        alpha=alpha))

            # Label da aresta
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            perp_x, perp_y = -dy, dx
            norm = math.hypot(perp_x, perp_y) or 1.0
            perp_x, perp_y = perp_x / norm * 0.15, perp_y / norm * 0.15
            label = descricao if descricao else tipo
            wrapped_label = _wrap_text(label, 26)
            ax.text(mx + perp_x, my + perp_y, wrapped_label, fontsize=8.5,
                    ha="center", va="center", color=cor, style="italic",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=cor,
                              alpha=0.85, linewidth=0.5), zorder=4)

    # Desenhar nós — círculos grandes com nome dentro
    for i, tema in enumerate(temas):
        x, y = posicoes[i]
        cor = CORES_QUALITATIVAS[i % len(CORES_QUALITATIVAS)]
        nome = tema.get("nome", f"Tema {i+1}")
        wrapped = _wrap_text(nome, 20)

        # Círculo do nó
        circle = plt.Circle((x, y), 0.22, color=cor, ec="white", linewidth=2.5, zorder=5)
        ax.add_patch(circle)

        # Texto dentro do círculo
        fs = 9.5
        for _ in range(3):
            tw, th = _text_bbox(ax, wrapped, fs)
            if tw <= 0.38 and th <= 0.32:
                break
            fs = max(FONT_MIN, fs - 0.5)
        ax.text(x, y, wrapped, ha="center", va="center", fontsize=fs,
                fontweight="bold", color="white", zorder=6, wrap=True)

    # Legenda integrada
    legenda_itens = [
        ("Conexão", "#1B9E77", "-"),
        ("Tensão", "#E78AC3", "--"),
        ("Complementaridade", "#8DA0CB", ":"),
    ]
    for idx, (nome_l, cor_l, estilo_l) in enumerate(legenda_itens):
        ax.plot([], [], linestyle=estilo_l, color=cor_l, linewidth=3.0, label=nome_l)
    ax.legend(loc="lower right", fontsize=10, frameon=True, fancybox=True,
              framealpha=0.95, edgecolor="#CCCCCC", title="Tipo de relação",
              title_fontsize=10)

    plt.tight_layout()
    fig.savefig(output_path, format="svg", bbox_inches="tight", facecolor="white")
    _png = output_path[:-4] + ".png"
    fig.savefig(_png, format="png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# 5. DIAGRAMA DE TRAJETÓRIA — Painéis com setas visíveis
# ═══════════════════════════════════════════════════════════════════════════════

def gerar_diagrama_trajetoria(trajetoria: dict, itens_por_etapa: dict = None, output_path: str = None) -> str:
    """
    Trajetória analítica em painéis verticais com setas de evolução.
    """
    _ensure_parent(output_path)

    itens_default = {
        "codigos": [],
        "categorias": [],
        "subtemas": [],
        "temas": [],
    }
    if itens_por_etapa is not None:
        itens_default.update(itens_por_etapa)

    etapas = []
    if itens_default.get("codigos"):
        etapas.append((
            f"Códigos iniciais = {trajetoria.get('codigos_iniciais', len(itens_default['codigos']))}",
            itens_default["codigos"],
            CORES_QUALITATIVAS[0]
        ))
    if itens_default.get("categorias"):
        etapas.append((
            f"Categorias emergentes = {trajetoria.get('categorias_emergentes', len(itens_default['categorias']))}",
            itens_default["categorias"],
            CORES_QUALITATIVAS[1]
        ))
    reducao = trajetoria.get("reducao", {})
    if reducao:
        etapas.append((
            f"Redução/revisão: {reducao.get('de', '?')} → {reducao.get('para', '?')}",
            [reducao.get("justificativa", "")] if reducao.get("justificativa") else [],
            CORES_QUALITATIVAS[3]
        ))
    if itens_default.get("subtemas"):
        etapas.append((
            f"Sub-temas identificados = {trajetoria.get('subtemas', len(itens_default['subtemas']))}",
            itens_default["subtemas"],
            CORES_QUALITATIVAS[4]
        ))
    if itens_default.get("temas"):
        etapas.append((
            f"Temas finais = {trajetoria.get('temas_finais', len(itens_default['temas']))}",
            itens_default["temas"],
            CORES_QUALITATIVAS[2]
        ))

    if not etapas:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "Nenhum dado de trajetória fornecido.", ha="center", va="center", fontsize=11, color=C_NEUTRO_MEDIO)
        ax.axis("off")
        fig.savefig(output_path, format="svg")
        plt.close(fig)
        return output_path

    n_etapas = len(etapas)
    max_itens = max((len(itens) for _, itens, _ in etapas), default=0)
    altura_por_item = 0.70
    fig_h = max(10, max_itens * altura_por_item + 4.0)
    fig_w = max(18, n_etapas * 5.5)

    fig, axes = plt.subplots(1, n_etapas, figsize=(fig_w, fig_h))
    if n_etapas == 1:
        axes = [axes]

    for ax, (titulo, itens, cor) in zip(axes, etapas):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 100)
        ax.axis("off")
        ax.set_facecolor("white")

        # Cabeçalho
        header_h = 12
        rect = FancyBboxPatch(
            (0.3, 100 - header_h - 1), 9.4, header_h,
            boxstyle="round,pad=0.3,rounding_size=0.8",
            facecolor=cor, edgecolor="white", linewidth=2, zorder=3,
        )
        ax.add_patch(rect)
        ax.text(5, 100 - header_h / 2 - 1, titulo, ha="center", va="center",
                fontsize=13, fontweight="bold", color="white", zorder=4)

        ax.plot([0.5, 9.5], [100 - header_h - 2, 100 - header_h - 2],
                color="#E0E0E0", linewidth=1.5, zorder=2)

        if not itens:
            ax.text(5, 85, "(nenhum item)", ha="center", va="top",
                    fontsize=11, color=C_NEUTRO_CLARO, style="italic")
        else:
            y_top = 100 - header_h - 3.0
            y_bottom = 2
            espaco_disp = y_top - y_bottom
            altura_item = espaco_disp / max(len(itens), 1)
            altura_min = 6.0
            if altura_item < altura_min and len(itens) > 15:
                itens_exibidos = itens[:25]
                extras = len(itens) - 25
            else:
                itens_exibidos = itens
                extras = 0
                if altura_item < altura_min:
                    altura_item = altura_min

            for idx, item in enumerate(itens_exibidos):
                y = y_top - idx * altura_item - altura_item / 2
                bg = "#F5F5F5" if idx % 2 == 0 else "white"
                pad_y = 0.8
                item_rect = FancyBboxPatch(
                    (0.4, y - altura_item / 2 + pad_y), 9.2, altura_item - pad_y * 2,
                    boxstyle="round,pad=0.03,rounding_size=0.2",
                    facecolor=bg, edgecolor="#DDDDDD", linewidth=0.5, zorder=1,
                )
                ax.add_patch(item_rect)

                texto = str(item)
                if len(texto) > 50:
                    texto = texto[:47] + "..."
                ax.text(0.8, y, texto, ha="left", va="center",
                        fontsize=12, color=C_NEUTRO_ESCURO, zorder=2)

            if extras > 0:
                ax.text(5, y_bottom + 1, f"(+ {extras} itens)",
                        ha="center", va="bottom", fontsize=11, color=C_NEUTRO_CLARO, style="italic")

    # Setas grandes e visíveis entre painéis
    for i in range(n_etapas - 1):
        x1 = (i + 0.88) / n_etapas
        x2 = (i + 1.12) / n_etapas
        y = 0.55

        circ = plt.Circle(
            ((x1 + x2) / 2, y),
            0.025,
            transform=fig.transFigure,
            facecolor="white",
            edgecolor="none",
            zorder=9,
            clip_on=False,
        )
        fig.patches.append(circ)

        arrow = mpatches.FancyArrowPatch(
            (x1, y), (x2, y),
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=45,
            color="#264653",
            linewidth=4.0,
            zorder=10,
            clip_on=False,
            joinstyle="round",
            capstyle="round",
        )
        fig.patches.append(arrow)

    fig.suptitle("Trajetória Analítica", fontsize=17, fontweight="bold", color=C_NEUTRO_ESCURO, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(output_path, format="svg", bbox_inches="tight", facecolor="white")
    _png = output_path[:-4] + ".png"
    fig.savefig(_png, format="png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# 6. MAPA FINAL — Hierarquia pura sem conexões entre temas
# ═══════════════════════════════════════════════════════════════════════════════

def gerar_mapa_final(temas: list[dict], output_path: str) -> str:
    """
    Mapa temático final — hierarquia pura, sem conexões entre temas.
    """
    _ensure_parent(output_path)

    n_temas = len(temas)
    altura_total = sum(_altura_estimada_tema(t) for t in temas) + 1.5
    fig, ax = plt.subplots(figsize=(14, max(9, altura_total * 0.65)))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, altura_total)
    ax.axis("off")
    ax.set_title("Mapa Temático Final — Relatório", fontsize=15, fontweight="bold",
                 color=C_NEUTRO_ESCURO, pad=18)
    ax.set_facecolor(C_FUNDO)
    ax.grid(False)

    y_cursor = altura_total - 0.8

    for i, tema in enumerate(temas):
        cor = CORES_QUALITATIVAS[i % len(CORES_QUALITATIVAS)]
        cor_clara = CORES_SECUNDARIAS[i % len(CORES_SECUNDARIAS)]
        nome = tema.get("nome", f"Tema {i + 1}")

        # Tema
        rect = FancyBboxPatch(
            (0.2, y_cursor - 0.45), 9.6, 0.9,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            facecolor=cor, edgecolor="none", linewidth=0, zorder=5, alpha=0.9,
        )
        ax.add_patch(rect)
        ax.text(5, y_cursor, nome, ha="center", va="center",
                fontsize=13, fontweight="bold", color="white", zorder=6)
        y_cursor -= 1.1

        for sub in tema.get("subtemas", []):
            nome_sub = sub.get("nome", "")
            # Subtema
            _draw_box_text(
                ax, x=5.1, y=y_cursor - 0.30,
                texto=nome_sub,
                box_w=8.4, box_h=0.62,
                facecolor=cor_clara, edgecolor=cor,
                textcolor=C_NEUTRO_ESCURO, fontsize=10.5, fontweight="bold",
                linewidth=1.0, zorder=5,
            )
            y_cursor -= 0.78

            for cat in sub.get("categorias", []):
                nome_cat = cat.get("nome", "")
                # Categoria
                _draw_box_text(
                    ax, x=5.3, y=y_cursor - 0.24,
                    texto=nome_cat,
                    box_w=7.8, box_h=0.48,
                    facecolor="#F8F8F8", edgecolor="#D0D0D0",
                    textcolor=C_NEUTRO_MEDIO, fontsize=9,
                    linewidth=0.6, zorder=5,
                )
                y_cursor -= 0.52

        y_cursor -= 0.35

    plt.tight_layout()
    fig.savefig(output_path, format="svg", bbox_inches="tight", facecolor="white")
    _png = output_path[:-4] + ".png"
    fig.savefig(_png, format="png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# 7. VERIFICAÇÃO DE CITAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════

def _normalizar_fontes(dataset_texto: str | None = None, fontes: list[dict] | None = None) -> list[dict]:
    fontes_norm = []
    if fontes:
        for i, fonte in enumerate(fontes, start=1):
            if isinstance(fonte, dict):
                nome = fonte.get("fonte") or fonte.get("arquivo") or fonte.get("id") or f"fonte-{i}"
                texto = fonte.get("texto", "")
            else:
                nome = f"fonte-{i}"
                texto = str(fonte)
            fontes_norm.append({"fonte": str(nome), "texto": str(texto)})
    if dataset_texto is not None:
        fontes_norm.append({"fonte": "dataset_texto", "texto": str(dataset_texto)})
    return fontes_norm


def _linhas_do_intervalo(texto: str, inicio: int, fim: int) -> tuple[int, int]:
    linha_inicio = texto.count("\n", 0, inicio) + 1
    linha_fim = texto.count("\n", 0, fim) + 1
    return linha_inicio, linha_fim


def _janelas_linhas(texto: str, max_linhas: int = 5):
    linhas = texto.splitlines()
    offset = 0
    offsets = []
    for linha in linhas:
        offsets.append(offset)
        offset += len(linha) + 1
    for i in range(len(linhas)):
        for tamanho in range(1, max_linhas + 1):
            fim_i = i + tamanho
            if fim_i > len(linhas):
                break
            trecho = "\n".join(linhas[i:fim_i])
            inicio = offsets[i]
            fim = inicio + len(trecho)
            yield trecho, inicio, fim, i + 1, fim_i


def _normalizar_texto(valor: str) -> str:
    return re.sub(r"\s+", " ", valor).strip().lower()


def _relocalizar_exato_normalizado(
    extrato: str, fontes_norm: list[dict]
) -> dict | None:
    """Passo 2 da verificacao: texto exato apos normalizacao (caixa e espacos), em todas as fontes.

    Um extrato nao encontrado na fonte declarada nao encerra a busca. Diferencas
    de superficie (caixa, espaco duplo, quebra de linha, prefixo como
    "[LOCUTOR...] " no inicio da linha) nao significam ausencia do trecho.
    """
    palavras = _normalizar_texto(extrato).split()
    if not palavras:
        return None
    padrao = re.compile("\\s+".join(re.escape(p) for p in palavras), re.IGNORECASE)
    for fonte in fontes_norm:
        texto = fonte["texto"]
        m = padrao.search(texto)
        if m is not None:
            trecho = texto[m.start():m.end()]
            linha_inicio, linha_fim = _linhas_do_intervalo(texto, m.start(), m.end())
            return {
                "status": "relocalizado",
                "similaridade": 1.0,
                "trecho_correspondente": trecho,
                "trecho_original": extrato,
                "fonte": fonte["fonte"],
                "linha_inicio": linha_inicio,
                "linha_fim": linha_fim,
                "metodo": "normalizado",
            }
    return None


def _melhor_trecho_similar(
    extrato: str, fontes_norm: list[dict], sugestao_threshold: float
) -> dict | None:
    """Passo 3 da verificacao: melhor trecho similar para substituicao.

    Status sugerido: "substituir" (com a forma original em "trecho_original" e o
    trecho exato do corpus em "trecho_correspondente"). O agente deve substituir
    a citacao pelo trecho exato e repercorrer a verificacao.
    """
    melhor = None
    for fonte in fontes_norm:
        for trecho, inicio, fim, linha_inicio, linha_fim in _janelas_linhas(fonte["texto"]):
            if RAPIDFUZZ_DISPONIVEL:
                score = fuzz.ratio(extrato, trecho) / 100.0
            else:
                import difflib
                score = difflib.SequenceMatcher(None, extrato, trecho).ratio()
            if melhor is None or score > melhor["similaridade"]:
                melhor = {
                    "status": "substituir",
                    "similaridade": round(score, 3),
                    "trecho_correspondente": trecho,
                    "trecho_original": extrato,
                    "fonte": fonte["fonte"],
                    "linha_inicio": linha_inicio,
                    "linha_fim": linha_fim,
                    "metodo": "similar",
                }
    if melhor is None or melhor["similaridade"] < sugestao_threshold:
        return None
    return melhor


def verificar_citacoes(
    extratos_citados: list[str],
    dataset_texto: str | None = None,
    threshold: float = 0.98,
    fontes: list[dict] | None = None,
    fuzzy: bool = False,
    sugestao_threshold: float = 0.80,
) -> dict:
    """
    Verifica se extratos citados aparecem literalmente nas fontes.

    Fluxo em tres passos antes de declarar falta:
    (1) busca exata na fonte declarada;
    (2) relocalizacao por texto normalizado (caixa/espacos/prefixos) em TODAS as fontes;
    (3) busca do melhor trecho similar para substituir a citacao pelo trecho exato.

    Status validos por correspondencia exata: "verificado" e "relocalizado"
    (re-escrever a citacao com "trecho_correspondente" e reconferir). "substituir"
    exige substituicao pelo "trecho_correspondente" exato e nova verificacao.
    "parcial" (triagem, com fuzzy=True) e "nao_encontrado" so apos os tres passos.
    """
    resultados = {}
    fontes_norm = _normalizar_fontes(dataset_texto=dataset_texto, fontes=fontes)

    for extrato in extratos_citados:
        resultado = {
            "status": "nao_encontrado",
            "similaridade": 0.0,
            "trecho_correspondente": None,
            "trecho_original": None,
            "fonte": None,
            "linha_inicio": None,
            "linha_fim": None,
            "metodo": "exato",
        }

        for fonte in fontes_norm:
            texto = fonte["texto"]
            inicio = texto.find(extrato)
            if inicio >= 0:
                fim = inicio + len(extrato)
                linha_inicio, linha_fim = _linhas_do_intervalo(texto, inicio, fim)
                resultado = {
                    "status": "verificado",
                    "similaridade": 1.0,
                    "trecho_correspondente": extrato,
                    "trecho_original": extrato,
                    "fonte": fonte["fonte"],
                    "linha_inicio": linha_inicio,
                    "linha_fim": linha_fim,
                    "metodo": "exato",
                }
                break

        if resultado["status"] == "nao_encontrado":
            relocalizado = _relocalizar_exato_normalizado(extrato, fontes_norm)
            if relocalizado is not None:
                resultado = relocalizado
            else:
                similar = _melhor_trecho_similar(extrato, fontes_norm, sugestao_threshold)
                if similar is not None:
                    if fuzzy and similar["similaridade"] >= threshold:
                        similar["status"] = "parcial"
                        similar["metodo"] = "fuzzy"
                        resultado = similar
                    elif not fuzzy:
                        resultado = similar

        resultados[extrato] = resultado

    return resultados


# ═══════════════════════════════════════════════════════════════════════════════
# 8. GERADOR DOCX
# ═══════════════════════════════════════════════════════════════════════════════

def _parsear_markdown(conteudo_md: str):
    linhas = conteudo_md.split("\n")
    blocos = []
    i = 0
    while i < len(linhas):
        linha = linhas[i].rstrip()
        if not linha:
            i += 1
            continue
        if linha.startswith("### "):
            blocos.append(("h3", linha[4:].strip()))
            i += 1
        elif linha.startswith("## "):
            blocos.append(("h2", linha[3:].strip()))
            i += 1
        elif linha.startswith("# "):
            blocos.append(("h1", linha[2:].strip()))
            i += 1
        elif linha.startswith("- ") or linha.startswith("* "):
            itens = []
            while i < len(linhas) and (linhas[i].startswith("- ") or linhas[i].startswith("* ")):
                itens.append(linhas[i][2:].strip())
                i += 1
            blocos.append(("lista", itens))
        elif linha.startswith("|") and "|" in linha[1:]:
            linhas_tabela = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                linhas_tabela.append(linhas[i].strip())
                i += 1
            blocos.append(("tabela", linhas_tabela))
        else:
            texto_acumulado = linha
            i += 1
            while i < len(linhas) and linhas[i].strip() and not linhas[i].startswith(("#", "-", "*", "|")):
                texto_acumulado += " " + linhas[i].strip()
                i += 1
            blocos.append(("paragrafo", texto_acumulado))
    return blocos


def gerar_docx_fase(titulo: str, conteudo_md: str, diagramas_svg: list[str], output_path: str) -> str:
    if not DOCX_DISPONIVEL:
        raise ImportError("python-docx não está instalado.")

    _ensure_parent(output_path)
    import re
    doc = Document()

    estilo = doc.styles["Title"]
    estilo.font.size = Pt(22)
    estilo.font.color.rgb = RGBColor(0x2E, 0x2E, 0x2E)

    doc.add_heading(titulo, level=0)
    blocos = _parsear_markdown(conteudo_md)

    for tipo, conteudo in blocos:
        if tipo == "h1":
            doc.add_heading(conteudo, level=1)
        elif tipo == "h2":
            doc.add_heading(conteudo, level=2)
        elif tipo == "h3":
            doc.add_heading(conteudo, level=3)
        elif tipo == "paragrafo":
            texto_limpo = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", conteudo)
            doc.add_paragraph(texto_limpo)
        elif tipo == "lista":
            for item in conteudo:
                texto_limpo = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", item)
                doc.add_paragraph(texto_limpo, style="List Bullet")
        elif tipo == "tabela":
            linhas_limpas = []
            for l in conteudo:
                celulas = [c.strip() for c in l.strip("|").split("|")]
                linhas_limpas.append(celulas)
            if len(linhas_limpas) >= 2 and all(set(c) <= {"-", ":", " ", ""} for c in linhas_limpas[1]):
                linhas_limpas.pop(1)
            if linhas_limpas:
                n_cols = max(len(l) for l in linhas_limpas)
                for l in linhas_limpas:
                    while len(l) < n_cols:
                        l.append("")
                tabela = doc.add_table(rows=len(linhas_limpas), cols=n_cols)
                tabela.style = "Light Grid Accent 1"
                tabela.alignment = WD_TABLE_ALIGNMENT.CENTER
                for ri, linha in enumerate(linhas_limpas):
                    for ci, celula in enumerate(linha):
                        texto_limpo = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", celula)
                        tabela.rows[ri].cells[ci].text = texto_limpo

    for i, svg_path in enumerate(diagramas_svg):
        if not os.path.exists(svg_path):
            print(f"Aviso: diagrama não encontrado: {svg_path}", file=sys.stderr)
            continue
        png_path = os.path.splitext(svg_path)[0] + ".png"
        png_resultado = _svg_para_png(svg_path, png_path)
        if not (png_resultado and os.path.exists(png_resultado)):
            if os.path.exists(png_path):
                png_resultado = png_path
        if png_resultado and os.path.exists(png_resultado):
            titulo_diagrama = os.path.splitext(os.path.basename(svg_path))[0].replace("_", " ").title()
            doc.add_heading(f"Diagrama: {titulo_diagrama}", level=2)
            try:
                doc.add_picture(png_resultado, width=Inches(6.0))
            except Exception as e:
                doc.add_paragraph(f"[Diagrama: {svg_path}] (erro ao inserir: {e})")
        else:
            doc.add_heading(f"Diagrama: {os.path.basename(svg_path)}", level=2)
            doc.add_paragraph(f"Diagrama disponível em formato SVG: {svg_path}. Instale cairosvg para converter.")

    doc.save(output_path)
    return output_path


# Use scripts/gerar_saida_final.py como CLI. Este arquivo e uma biblioteca.


# ═══════════════════════════════════════════════════════════════════════════════
# 9. OUTPUTS MARKDOWN — Mindmap, Infographic, Infocard
# ═══════════════════════════════════════════════════════════════════════════════
# Geram texto markdown que será renderizado pelo Markdown Viewer (VS Code).
# Sem dependências externas — apenas strings formatadas.
# Python/matplotlib continua para exportação DOCX (PNGs embutidos).

CORES_TEMAS = {
    0: ("#66C2A5", "#CCECE6"),
    1: ("#FC8D62", "#FDE0C4"),
    2: ("#8DA0CB", "#D8DDEA"),
    3: ("#E78AC3", "#F6D2E6"),
    4: ("#A6D854", "#E3F4C2"),
    5: ("#FFD92F", "#FFF2B3"),
    6: ("#E5C494", "#F5E8D0"),
    7: ("#B3B3B3", "#E0E0E0"),
    8: ("#1B9E77", "#A8E0CF"),
    9: ("#D95F02", "#F4C2A1"),
}


def gerar_mindmap_tematico(temas: list[dict], titulo: str = "Mapa Temático") -> str:
    """
    Gera mindmap PlantUML para hierarquia tema → subtema → categoria → código.
    Primeira metade dos temas no lado direito, segunda metade no lado esquerdo.
    Usa sintaxe + (direita) e - (esquerda) para controle lateral.
    Retorna string markdown com bloco ```plantuml```.
    """
    linhas = ["@startmindmap"]
    linhas.append(f"* {titulo}")

    n_temas = len(temas)
    metade = (n_temas + 1) // 2

    for i, tema in enumerate(temas):
        idx = i % len(CORES_TEMAS)
        cor_escura, cor_clara = CORES_TEMAS[idx]
        nome_tema = tema.get("nome", f"Tema {i + 1}")
        prefix = "+" if i < metade else "-"

        linhas.append(f"{prefix}1[{cor_escura}] {nome_tema}")

        subtemas = tema.get("subtemas", tema.get("categorias", []))
        for sub in subtemas:
            nome_sub = sub.get("nome", "") if isinstance(sub, dict) else str(sub)
            linhas.append(f"{prefix}2[{cor_clara}] {nome_sub}")

            itens_n2 = sub.get("categorias", sub.get("codigos", [])) if isinstance(sub, dict) else []
            if isinstance(itens_n2, list):
                for cat in itens_n2:
                    if isinstance(cat, dict):
                        nome_cat = cat.get("nome", "")
                        codigos = cat.get("codigos", [])
                        linhas.append(f"{prefix}3 {nome_cat}")
                        for cod in codigos:
                            nome_cod = cod if isinstance(cod, str) else cod.get("nome", "")
                            linhas.append(f"{prefix}4_ {nome_cod}")
                    elif isinstance(cat, str):
                        linhas.append(f"{prefix}3 {cat}")
            elif isinstance(itens_n2, str):
                linhas.append(f"{prefix}3 {itens_n2}")

    linhas.append("@endmindmap")
    conteudo = "\n".join(linhas)
    return f"```plantuml\n{conteudo}\n```"


def gerar_mindmap_final(temas: list[dict], titulo: str = "Mapa Temático Final") -> str:
    """
    Mindmap estilizado para o mapa final (Fase 6).
    Usa + (direita) e - (esquerda) para equilibrar themes.
    Usa <style> blocks para hierarquia visual profissional.
    """
    linhas = [
        "@startmindmap",
        "<style>",
        "node {",
        "    FontName sans-serif",
        "    FontSize 12",
        "    FontColor #2E2E2E",
        "}",
        "depth 0 {",
        "    BackgroundColor #264653",
        "    FontColor white",
        "    FontSize 16",
        "    RoundCorner 10",
        "}",
        "depth 1 {",
        "    FontStyle bold",
        "    RoundCorner 8",
        "}",
        "depth 2 {",
        "    BackgroundColor #F0F0F0",
        "    RoundCorner 5",
        "}",
        "depth 3 {",
        "    FontStyle italic",
        "    FontSize 10",
        "}",
        "</style>",
        "",
        f"* {titulo}",
    ]

    n_temas = len(temas)
    metade = (n_temas + 1) // 2

    for i, tema in enumerate(temas):
        idx = i % len(CORES_TEMAS)
        cor_escura, _ = CORES_TEMAS[idx]
        nome_tema = tema.get("nome", f"Tema {i + 1}")
        prefix = "+" if i < metade else "-"

        linhas.append(f"{prefix}1[{cor_escura}] {nome_tema}")

        subtemas = tema.get("subtemas", tema.get("categorias", []))
        for sub in subtemas:
            nome_sub = sub.get("nome", "") if isinstance(sub, dict) else str(sub)
            linhas.append(f"{prefix}2 {nome_sub}")

            itens_n2 = sub.get("categorias", sub.get("codigos", [])) if isinstance(sub, dict) else []
            if isinstance(itens_n2, list):
                for cat in itens_n2:
                    if isinstance(cat, dict):
                        nome_cat = cat.get("nome", "")
                        codigos = cat.get("codigos", [])
                        linhas.append(f"{prefix}3 {nome_cat}")
                        for cod in codigos:
                            nome_cod = cod if isinstance(cod, str) else cod.get("nome", "")
                            linhas.append(f"{prefix}4_ {nome_cod}")
                    elif isinstance(cat, str):
                        linhas.append(f"{prefix}3 {cat}")
            elif isinstance(itens_n2, str):
                linhas.append(f"{prefix}3 {itens_n2}")

    linhas.append("@endmindmap")
    conteudo = "\n".join(linhas)
    return f"```plantuml\n{conteudo}\n```"


def gerar_infographic_tragetoria(trajetoria: dict, itens_por_etapa: dict = None) -> str:
    """
    Gera funnel infographic para trajetória analítica.
    Retorna string markdown com bloco ```infographic```.
    """
    itens_default = {
        "codigos": [],
        "categorias": [],
        "subtemas": [],
        "temas": [],
    }
    if itens_por_etapa is not None:
        itens_default.update(itens_por_etapa)

    n_codigos = trajetoria.get("codigos_iniciais", len(itens_default["codigos"]))
    n_categorias = trajetoria.get("categorias_emergentes", len(itens_default["categorias"]))
    n_subtemas = trajetoria.get("subtemas", len(itens_default["subtemas"]))
    n_temas = trajetoria.get("temas_finais", len(itens_default["temas"]))

    reducao = trajetoria.get("reducao", {})
    justificativa_reducao = reducao.get("justificativa", "")

    nomes_codigos = itens_default["codigos"][:5] if itens_default["codigos"] else []
    nomes_categorias = itens_default["categorias"][:5] if itens_default["categorias"] else []
    nomes_subtemas = itens_default["subtemas"][:5] if itens_default["subtemas"] else []
    nomes_temas = itens_default["temas"][:5] if itens_default["temas"] else []

    codigos_desc = ", ".join(nomes_codigos)
    if len(itens_default["codigos"]) > 5:
        codigos_desc += f" ... (+{len(itens_default['codigos']) - 5} mais)"
    categorias_desc = ", ".join(nomes_categorias)
    if len(itens_default["categorias"]) > 5:
        categorias_desc += f" ... (+{len(itens_default['categorias']) - 5} mais)"

    temas_desc = ", ".join(nomes_temas)

    items = f"""    - label Códigos iniciais
      value {n_codigos}
      desc {codigos_desc if codigos_desc else f'{n_codigos} códigos identificados no corpus'}
    - label Categorias emergentes
      value {n_categorias}
      desc {categorias_desc if categorias_desc else f'Agrupamento semântico em {n_categorias} categorias analíticas'}"""

    if reducao:
        de_val = reducao.get("de", n_categorias)
        para_val = reducao.get("para", n_subtemas)
        items += f"""
    - label Redução revisada
      value {para_val}
      desc {justificativa_reducao if justificativa_reducao else f'{de_val} categorias revisadas para {para_val} subtemas'}"""

    items += f"""
    - label Sub-temas identificados
      value {n_subtemas}
      desc Organização por significado compartilhado
    - label Temas finais
      value {n_temas}
      desc {temas_desc if temas_desc else f'{n_temas} temas construídos'}"""

    output = f"""```infographic
infographic sequence-filter-mesh-simple
data
  title Trajetória Analítica
  items
{items}
```"""
    return output


def gerar_infographic_evolucao(estado_inicial: dict, estado_revisado: dict) -> str:
    """
    Gera comparison infographic para evolução Fase 3 → Fase 4.
    Retorna string markdown com bloco ```infographic```.
    """
    nomes_ini = [t.get("nome", "?") for t in estado_inicial.get("temas", [])]
    nomes_rev = [t.get("nome", "?") for t in estado_revisado.get("temas", [])]

    n_ini = len(nomes_ini)
    n_rev = len(nomes_rev)

    antes_children = "\n".join(
        f"        - label {nome}" for nome in nomes_ini[:8]
    )
    depois_children = "\n".join(
        f"        - label {nome}" for nome in nomes_rev[:8]
    )

    output = f"""```infographic
infographic compare-binary-horizontal-underline-text-vs
data
  title Evolução dos Temas: Fase 3 → Fase 4
  items
    - label Fase 3 — Mapa Inicial ({n_ini} temas)
      children
{antes_children}
    - label Fase 4 — Mapa Revisado ({n_rev} temas)
      children
{depois_children}
```"""
    return output


def gerar_infocard_resumo_fase(
    fase: int,
    titulo_fase: str,
    descricao: str,
    kpis: list[dict],
    secoes: list[dict],
    meta_categoria: str = "ATR",
    meta_subcategoria: str = None,
) -> str:
    """
    Gera infocard research-abstract para resumo de cada fase.
    Retorna string markdown com HTML embutido.
    kpis: [{"label": "...", "value": "..."}]
    secoes: [{"title": "...", "text": "..."}]
    """
    meta = f"{meta_categoria} · Fase {fase}"
    if meta_subcategoria:
        meta = f"{meta_categoria} · {meta_subcategoria}"

    kpi_html = ""
    if kpis:
        kpi_cells = "\n".join(
            f'        <div class="card-kpi"><p class="card-kpi-value">{k["value"]}</p><p class="card-kpi-label">{k["label"]}</p></div>'
            for k in kpis
        )
        cols = min(len(kpis), 4)
        kpi_html = f"""    <div class="card-kpi-grid" style="grid-template-columns: repeat({cols}, 1fr);">
{kpi_cells}
    </div>"""

    sections_html = ""
    for sec in secoes:
        sections_html += f"""    <div class="card-section">
      <p class="card-section-title">{sec["title"]}</p>
      <p class="card-section-text">{sec["text"]}</p>
    </div>
"""

    output = f"""<div style="max-width: 840px; box-sizing: border-box; position: relative;">
  <style scoped>
    .card {{ position: relative; background: #fcfcfa; padding: 40px; font-family: serif; color: #202124; line-height: 1.72; }}
    .card-meta {{ margin: 0 0 12px; font-size: 12px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #6a717d; font-family: sans-serif; }}
    .card-title {{ margin: 0 0 14px; font-size: 32px; font-weight: 700; line-height: 1.2; color: #202124; }}
    .card-bar {{ width: 72px; height: 2px; margin: 0 0 20px; background: #355c9a; }}
    .card-subtitle {{ margin: 0 0 18px; font-size: 15px; line-height: 1.72; color: #444; }}
    .card-kpi-grid {{ display: grid; gap: 12px; margin-bottom: 18px; }}
    .card-kpi {{ padding: 14px 16px; background: rgba(53,92,154,0.05); border-top: 3px solid #355c9a; }}
    .card-kpi-value {{ margin: 0; font-size: 28px; font-weight: 700; color: #355c9a; font-family: sans-serif; }}
    .card-kpi-label {{ margin: 4px 0 0; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #6a717d; font-family: sans-serif; }}
    .card-doc {{ display: grid; gap: 12px; }}
    .card-section {{ padding: 16px 18px; background: rgba(53,92,154,0.05); border-left: 3px solid #355c9a; }}
    .card-section-title {{ margin: 0 0 6px; font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #355c9a; font-family: sans-serif; }}
    .card-section-text {{ margin: 0; font-size: 14px; line-height: 1.72; color: #444; }}
    .card-footer {{ margin-top: 22px; padding-top: 12px; border-top: 1px solid rgba(32,33,36,0.1); font-size: 11px; color: #6a717d; font-family: sans-serif; }}
  </style>
  <div class="card">
    <p class="card-meta">{meta}</p>
    <h1 class="card-title">{titulo_fase}</h1>
    <div class="card-bar"></div>
    <p class="card-subtitle">{descricao}</p>
{kpi_html}
    <div class="card-doc">
{sections_html}    </div>
    <div class="card-footer">Análise Temática Reflexiva · Braun &amp; Clarke</div>
  </div>
</div>"""
    return output


def gerar_md_fase(
    fase: int,
    titulo: str,
    conteudo_principal: str,
    diagramas_markdown: list[str],
    diagramas_svg_paths: list[str],
    output_path: str,
) -> str:
    """
    Gera arquivo markdown da fase com conteúdo + diagramas renderizáveis.
    diagramas_markdown: blocos markdown (plantuml, infographic, infocard HTML)
    diagramas_svg_paths: caminhos dos SVGs gerados por matplotlib (para referência)
    """
    _ensure_parent(output_path)

    partes = [f"# {titulo}\n"]
    partes.append(conteudo_principal)
    partes.append("")

    if diagramas_markdown:
        partes.append("---\n")
        partes.append("## Visualizações\n")
        for i, dm in enumerate(diagramas_markdown, 1):
            partes.append(f"### Diagrama {i}\n")
            partes.append(dm)
            partes.append("")

    if diagramas_svg_paths:
        partes.append("---\n")
        partes.append("## Diagramas para Exportação DOCX\n")
        partes.append("*Os diagramas SVG abaixo são incluídos automaticamente no DOCX pelo script de geração.*\n")
        for sp in diagramas_svg_paths:
            nome = os.path.splitext(os.path.basename(sp))[0].replace("_", " ").title()
            partes.append(f"- `{sp}` — {nome}")
        partes.append("")

    md_content = "\n".join(partes)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return output_path


def gerar_dot_mapa_tematico(temas: list[dict], titulo: str = "Mapa Tematico ATR") -> str:
    """
    Gera mapa hierarquico em Graphviz DOT para Markdown Viewer.
    Use para leitura/colaboracao. Para relatorios formais, gere SVG/PNG tambem.
    """
    linhas = [
        "digraph atr_mapa_tematico {",
        "  graph [rankdir=LR, bgcolor=\"white\", pad=\"0.3\", nodesep=\"0.35\", ranksep=\"0.75\", splines=ortho];",
        "  node [shape=box, style=\"rounded,filled\", fontname=\"Arial\", fontsize=10, margin=\"0.10,0.07\", color=\"#d6dbe1\", penwidth=1.2];",
        "  edge [color=\"#8a94a3\", arrowsize=0.6, penwidth=1.1];",
        f"  titulo [label=\"{_dot_escape(titulo)}\", shape=plaintext, fontsize=18, fontcolor=\"#1f2937\"];",
    ]

    previous_theme_id = None
    for i, tema in enumerate(temas, start=1):
        tema_id = f"tema_{i}"
        tema_nome = _dot_escape(tema.get("nome", f"Tema {i}"))
        linhas.append(f"  {tema_id} [label=\"{tema_nome}\", fillcolor=\"#264653\", fontcolor=\"white\", fontsize=12, penwidth=0];")
        linhas.append(f"  titulo -> {tema_id} [style=invis];")
        if previous_theme_id:
            linhas.append(f"  {previous_theme_id} -> {tema_id} [style=invis, weight=4];")
        previous_theme_id = tema_id

        for j, subtema in enumerate(tema.get("subtemas", []), start=1):
            sub_id = f"{tema_id}_sub_{j}"
            sub_nome = _dot_escape(subtema.get("nome", f"Subtema {j}"))
            linhas.append(f"  {sub_id} [label=\"{sub_nome}\", fillcolor=\"#e8f3f1\", color=\"#9cc8bf\", fontcolor=\"#1f2937\"];")
            linhas.append(f"  {tema_id} -> {sub_id};")

            for k, categoria in enumerate(subtema.get("categorias", []), start=1):
                cat_id = f"{sub_id}_cat_{k}"
                cat_nome = _dot_escape(categoria.get("nome", f"Categoria {k}"))
                linhas.append(f"  {cat_id} [label=\"{cat_nome}\", fillcolor=\"#f5f7fa\", color=\"#ccd3dc\", fontcolor=\"#374151\"];")
                linhas.append(f"  {sub_id} -> {cat_id};")

                for m, codigo in enumerate(categoria.get("codigos", []), start=1):
                    cod_id = f"{cat_id}_cod_{m}"
                    cod_nome = _dot_escape(codigo if isinstance(codigo, str) else codigo.get("nome", f"Codigo {m}"))
                    linhas.append(f"  {cod_id} [label=\"{cod_nome}\", shape=note, fillcolor=\"#fff8e6\", color=\"#f0d28a\", fontcolor=\"#4b5563\", fontsize=9];")
                    linhas.append(f"  {cat_id} -> {cod_id};")

    linhas.append("}")
    return "```dot\n" + "\n".join(linhas) + "\n```"


def calcular_frequencia_codigos(codigos_por_documento: dict) -> list[dict]:
    """Calcula frequencia exploratoria de codigos por documento."""
    contagem = Counter()
    docs_por_codigo = defaultdict(list)
    for doc_id, codigos in codigos_por_documento.items():
        for codigo in set(codigos):
            contagem[codigo] += 1
            docs_por_codigo[codigo].append(doc_id)
    return [
        {"codigo": codigo, "n_documentos": n, "documentos": sorted(docs_por_codigo[codigo])}
        for codigo, n in contagem.most_common()
    ]


def gerar_tabela_frequencia_markdown(codigos_por_documento: dict, max_linhas: int = 30) -> str:
    """
    Gera tabela de frequencia para auditoria exploratoria.
    Frequencia nunca deve ser usada como criterio automatico de relevancia.
    """
    linhas = [
        "| Codigo | Documentos | Fontes |",
        "|---|---:|---|",
    ]
    for item in calcular_frequencia_codigos(codigos_por_documento)[:max_linhas]:
        fontes = ", ".join(item["documentos"][:6])
        if len(item["documentos"]) > 6:
            fontes += f" ... (+{len(item['documentos']) - 6})"
        linhas.append(f"| {item['codigo']} | {item['n_documentos']} | {fontes} |")
    linhas.append("")
    linhas.append("> Auditoria exploratoria: use frequencia para checar cobertura, lacunas e casos raros. Nunca use como proxy automatico de importancia analitica.")
    return "\n".join(linhas)
