#!/usr/bin/env python3
"""Audita a parte computável de uma Análise Temática Reflexiva.

Lê o registro único de evidências (`evidencias.jsonl`) e os arquivos de saída
e confere o que não depende de interpretação: referências entre excertos,
códigos e temas, citações do relatório, cobertura de leitura, distribuição da
evidência, marcadores de template, identificadores pessoais, vocabulário de
sobrealegação e semelhança entre relatórios de casos diferentes.

O script não decide significados. Um resultado sem erros diz apenas que a
trilha é íntegra; a qualidade interpretativa continua a cargo do avaliador.
Usa somente a biblioteca padrão do Python.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ESTATUTOS = {
    "fala_primaria",
    "texto_do_participante",
    "documento",
    "nota_de_mediador",
    "transcricao_automatica",
    "resumo_de_segunda_mao",
    "outro",
}
# Fontes em que quem escreve não é o participante: o excerto registra a voz
# de quem mediou e não pode ser apresentado como fala.
ESTATUTOS_MEDIADOS = {"nota_de_mediador", "resumo_de_segunda_mao"}
ESTADOS_CODIGO = {"ativo", "fundido", "recusado", "residuo"}
DESTINOS_HIPOTESE = {"pendente", "mantida", "revista", "derrubada"}
OBRIGATORIOS = {
    "fonte": ("id", "arquivo", "estatuto"),
    "excerto": ("id", "fonte", "texto", "forma"),
    "codigo": ("id", "rotulo", "excertos"),
    "tema": ("id", "fase", "nome", "conceito", "codigos"),
    "hipotese": ("id", "texto", "destino"),
    "nao_representado": ("id", "excerto", "tratamento"),
    "citacao_externa": ("id", "texto", "referencia"),
}
TETO_TEMAS = 8
MIN_PALAVRAS_CITACAO = 5
MIN_PALAVRAS_ANCORA = 6
LIMIAR_HOMOGENEIZACAO = 0.05

ASPAS = "“”\"«»"
RE_CITACAO = re.compile(r"[“\"«]([^“”\"«»]{12,}?)[”\"»]")
RE_ELIPSE = re.compile(r"\[\s*(?:\.\.\.|…)\s*\]|\(\s*(?:\.\.\.|…)\s*\)|…|\.\.\.")
RE_LINHA = re.compile(r"linhas?\s+(\d+)", re.IGNORECASE)


# ---------------------------------------------------------------- utilidades


def ler_jsonl(path: Path) -> tuple[list[dict], list[str]]:
    registros: list[dict] = []
    problemas: list[str] = []
    try:
        linhas = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        return [], [f"{path.name}: {exc}"]
    for numero, linha in enumerate(linhas, 1):
        if not linha.strip():
            continue
        try:
            dado = json.loads(linha)
        except json.JSONDecodeError as exc:
            problemas.append(f"{path.name}, linha {numero}: JSON inválido ({exc.msg})")
            continue
        if not isinstance(dado, dict):
            problemas.append(f"{path.name}, linha {numero}: registro não é objeto")
            continue
        dado["_linha"] = numero
        registros.append(dado)
    return registros, problemas


def normalizar(texto: str) -> str:
    texto = texto.lower().replace("’", "'").replace("‘", "'")
    texto = re.sub(r"[*_`>]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip(" .,;:!?" + ASPAS)


def palavras(texto: str) -> list[str]:
    return re.findall(r"[\wÀ-ÿ'-]+", texto)


def paragrafos(texto: str) -> list[str]:
    blocos = re.split(r"\n\s*\n", texto)
    return [re.sub(r"\n\s*>?\s*", " ", bloco).strip() for bloco in blocos if bloco.strip()]


def sem_citacoes(texto: str) -> str:
    return RE_CITACAO.sub(" ", texto)


def arquivos_md(pasta: Path) -> list[Path]:
    return sorted(p for p in pasta.rglob("*.md") if p.is_file())


def gravar(saida: Path | None, resultado: dict) -> None:
    texto = json.dumps(resultado, ensure_ascii=False, indent=2) + "\n"
    if saida is None:
        sys.stdout.write(texto)
        return
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(texto, encoding="utf-8")


# ------------------------------------------------------------------ registro


class Registro:
    """Registro único de evidências, indexado por tipo e identificador."""

    def __init__(self, registros: list[dict]) -> None:
        self.erros: list[dict] = []
        self.alertas: list[dict] = []
        self.por_tipo: dict[str, dict[str, dict]] = defaultdict(dict)
        for item in registros:
            tipo = item.get("tipo")
            if tipo not in OBRIGATORIOS:
                self.erro("E01", f"tipo desconhecido: {tipo!r}", f"linha {item['_linha']}")
                continue
            faltando = [campo for campo in OBRIGATORIOS[tipo] if item.get(campo) in (None, "", [])]
            # Um código pode nascer sem excertos somente se for recusado.
            if tipo == "codigo" and item.get("estado") == "recusado":
                faltando = [campo for campo in faltando if campo != "excertos"]
            if faltando:
                self.erro(
                    "E01",
                    f"{tipo} sem campos obrigatórios: {', '.join(faltando)}",
                    str(item.get("id") or f"linha {item['_linha']}"),
                )
                if "id" in faltando:
                    continue
            ident = str(item["id"])
            if ident in self.por_tipo[tipo]:
                self.erro("E01", f"identificador repetido em {tipo}", ident)
                continue
            self.por_tipo[tipo][ident] = item

    def erro(self, codigo: str, mensagem: str, ref: str = "") -> None:
        self.erros.append({"codigo": codigo, "mensagem": mensagem, "ref": ref})

    def alerta(self, codigo: str, mensagem: str, ref: str = "") -> None:
        self.alertas.append({"codigo": codigo, "mensagem": mensagem, "ref": ref})

    @property
    def fontes(self) -> dict[str, dict]:
        return self.por_tipo["fonte"]

    @property
    def excertos(self) -> dict[str, dict]:
        return self.por_tipo["excerto"]

    @property
    def codigos(self) -> dict[str, dict]:
        return self.por_tipo["codigo"]

    def temas(self, fase: str) -> dict[str, dict]:
        return {k: v for k, v in self.por_tipo["tema"].items() if v.get("fase") == fase}

    def excertos_do_tema(self, tema: dict) -> set[str]:
        usados = set(tema.get("ancoras") or []) | set(tema.get("evidencia_decisiva") or [])
        usados |= set(tema.get("tensoes") or [])
        for codigo_id in tema.get("codigos") or []:
            usados |= set(self.codigos.get(codigo_id, {}).get("excertos") or [])
        return usados


def conferir_estrutura(reg: Registro) -> None:
    for ident, fonte in reg.fontes.items():
        if fonte.get("estatuto") not in ESTATUTOS:
            reg.erro("E01", f"estatuto de fonte inválido: {fonte.get('estatuto')!r}", ident)

    for ident, excerto in reg.excertos.items():
        fonte = reg.fontes.get(str(excerto.get("fonte")))
        if fonte is None:
            reg.erro("E02", "excerto aponta para fonte inexistente", ident)
        forma = excerto.get("forma")
        if forma not in ("literal", "parafrase"):
            reg.erro("E01", f"forma de excerto inválida: {forma!r}", ident)
        if forma == "literal":
            if not str(excerto.get("localizador") or "").strip():
                reg.erro("E03", "excerto literal sem localizador estável", ident)
            if not str(excerto.get("contexto") or "").strip():
                reg.erro("E03", "excerto literal sem janela de contexto registrada", ident)
        if fonte and fonte.get("estatuto") in ESTATUTOS_MEDIADOS and excerto.get("voz") != "mediador":
            reg.erro(
                "E13",
                "excerto de fonte mediada precisa de voz 'mediador': é registro de quem mediou, não fala",
                ident,
            )
        if str(excerto.get("falante") or "") == "nao_atribuido":
            reg.alerta("A06", "falante não atribuído: não individualizar no relatório", ident)

    for ident, codigo in reg.codigos.items():
        estado = codigo.get("estado", "ativo")
        if estado not in ESTADOS_CODIGO:
            reg.erro("E01", f"estado de código inválido: {estado!r}", ident)
        for excerto_id in codigo.get("excertos") or []:
            if excerto_id not in reg.excertos:
                reg.erro("E02", f"código aponta para excerto inexistente: {excerto_id}", ident)
        if estado == "fundido" and codigo.get("destino") not in reg.codigos:
            reg.erro("E02", "código fundido sem destino válido", ident)

    for ident, tema in reg.por_tipo["tema"].items():
        if tema.get("fase") not in ("candidato", "final"):
            reg.erro("E01", f"fase de tema inválida: {tema.get('fase')!r}", ident)
        for codigo_id in tema.get("codigos") or []:
            if codigo_id not in reg.codigos:
                reg.erro("E02", f"tema aponta para código inexistente: {codigo_id}", ident)
        for campo in ("ancoras", "evidencia_decisiva", "tensoes"):
            for excerto_id in tema.get(campo) or []:
                excerto = reg.excertos.get(excerto_id)
                if excerto is None:
                    reg.erro("E02", f"{campo} aponta para excerto inexistente: {excerto_id}", ident)
                elif excerto.get("forma") != "literal" and campo != "tensoes":
                    reg.erro("E07", f"paráfrase usada em {campo}: {excerto_id}", ident)
        for origem in tema.get("origem") or []:
            if origem not in reg.temas("candidato"):
                reg.erro("E02", f"tema final com origem inexistente: {origem}", ident)

    for ident, hipotese in reg.por_tipo["hipotese"].items():
        if hipotese.get("destino") not in DESTINOS_HIPOTESE:
            reg.erro("E01", f"destino de hipótese inválido: {hipotese.get('destino')!r}", ident)


def conferir_temas_finais(reg: Registro) -> None:
    finais = reg.temas("final")
    if not finais:
        return
    onde: dict[str, list[str]] = defaultdict(list)
    for tema_id, tema in finais.items():
        for codigo_id in tema.get("codigos") or []:
            onde[codigo_id].append(tema_id)

    for codigo_id, codigo in reg.codigos.items():
        estado = codigo.get("estado", "ativo")
        if estado == "ativo" and codigo_id not in onde:
            reg.erro(
                "E05",
                "código ativo fora de todos os temas finais: alocar, fundir, recusar ou marcar como resíduo",
                codigo_id,
            )
        if estado == "residuo" and not str(codigo.get("justificativa") or "").strip():
            reg.erro("E05", "código marcado como resíduo sem justificativa", codigo_id)
        if len(onde.get(codigo_id, [])) > 1 and not str(codigo.get("compartilhado") or "").strip():
            reg.erro(
                "E06",
                f"código em mais de um tema final sem justificativa: {', '.join(onde[codigo_id])}",
                codigo_id,
            )

    if len(finais) > TETO_TEMAS:
        reg.alerta(
            "A12",
            f"{len(finais)} temas finais: acima de {TETO_TEMAS}, conferir se há resumos de tópico ou fronteiras frágeis",
        )

    falantes: dict[str, set[str]] = defaultdict(set)
    for tema_id, tema in finais.items():
        ancoras = [reg.excertos[q] for q in tema.get("ancoras") or [] if q in reg.excertos]
        if not ancoras:
            reg.erro("E07", "tema final sem excerto-âncora literal", tema_id)
            continue
        fontes = {str(a.get("fonte")) for a in ancoras}
        if len(fontes) == 1 and len(reg.fontes) > 1:
            reg.alerta("A01", f"tema ancorado em uma só fonte ({next(iter(fontes))})", tema_id)
        for ancora in ancoras:
            if len(palavras(str(ancora.get("texto", "")))) < MIN_PALAVRAS_ANCORA:
                reg.alerta("A13", f"âncora curta demais para sustentar interpretação: {ancora['id']}", tema_id)
            falante = str(ancora.get("falante") or "")
            if falante and falante != "nao_atribuido":
                falantes[f"{ancora.get('fonte')}/{falante}"].add(tema_id)
        if not (tema.get("tensoes") or str(tema.get("busca_contraevidencia") or "").strip()):
            reg.alerta(
                "A16",
                "tema final sem excerto que o tensione nem registro de como a contraevidência foi buscada",
                tema_id,
            )
    if len(finais) >= 3:
        for falante, temas in sorted(falantes.items()):
            if len(temas) * 2 > len(finais):
                reg.alerta(
                    "A02",
                    f"um mesmo falante ancora {len(temas)} de {len(finais)} temas finais",
                    falante,
                )

    usados: set[str] = set()
    sustentam: set[str] = set()
    for tema in finais.values():
        usados |= reg.excertos_do_tema(tema)
        sustentam |= reg.excertos_do_tema(tema) - set(tema.get("tensoes") or [])
    for ident, item in reg.por_tipo["nao_representado"].items():
        if item.get("excerto") not in reg.excertos:
            reg.erro("E02", "dado não representado aponta para excerto inexistente", ident)
        elif item["excerto"] in sustentam:
            reg.erro(
                "E11",
                f"'{item['excerto']}' consta como não representado, mas já sustenta um tema final",
                ident,
            )

    fontes_dos_usados = [str(reg.excertos[q].get("fonte")) for q in usados if q in reg.excertos]
    indiretos = [
        f for f in fontes_dos_usados
        if reg.fontes.get(f, {}).get("estatuto") in ESTATUTOS_MEDIADOS | {"transcricao_automatica"}
    ]
    if fontes_dos_usados and len(indiretos) * 2 > len(fontes_dos_usados):
        reg.alerta(
            "A17",
            f"{len(indiretos)} de {len(fontes_dos_usados)} excertos dos temas finais vêm de fonte mediada, resumida "
            "ou transcrita por máquina: o relatório precisa dizer de quem é a voz analisada",
        )
    citadas = set(fontes_dos_usados)
    ausentes = sorted(set(reg.fontes) - citadas)
    if ausentes:
        reg.alerta("A04", f"{len(ausentes)} fonte(s) sem nenhum excerto nos temas finais", ", ".join(ausentes))
    estatutos_ausentes = sorted(
        {str(f.get("estatuto")) for f in reg.fontes.values()}
        - {str(reg.fontes[f].get("estatuto")) for f in citadas if f in reg.fontes}
    )
    if estatutos_ausentes:
        reg.alerta("A04", "tipo de fonte nunca citado nos temas finais", ", ".join(estatutos_ausentes))


def diff_temas(reg: Registro) -> dict:
    candidatos, finais = reg.temas("candidato"), reg.temas("final")
    if not candidatos or not finais:
        return {}
    origem_de = {tid: list(t.get("origem") or []) for tid, t in finais.items()}
    usos = Counter(c for origens in origem_de.values() for c in origens)
    fusoes = sorted(tid for tid, origens in origem_de.items() if len(origens) > 1)
    divisoes = sorted(c for c, n in usos.items() if n > 1)
    abandonos = sorted(set(candidatos) - set(usos))
    novos = sorted(tid for tid, origens in origem_de.items() if not origens)
    renomeados, codigos_movidos = [], []
    for tid, origens in origem_de.items():
        if len(origens) != 1 or origens[0] not in candidatos:
            continue
        candidato = candidatos[origens[0]]
        if normalizar(str(candidato.get("nome"))) != normalizar(str(finais[tid].get("nome"))):
            renomeados.append({"de": candidato.get("nome"), "para": finais[tid].get("nome")})
        antes, depois = set(candidato.get("codigos") or []), set(finais[tid].get("codigos") or [])
        if antes != depois:
            codigos_movidos.append(
                {"tema": tid, "entraram": sorted(depois - antes), "sairam": sorted(antes - depois)}
            )
    estrutural = bool(fusoes or divisoes or abandonos or novos or codigos_movidos)
    resultado = {
        "candidatos": len(candidatos),
        "finais": len(finais),
        "fusoes": fusoes,
        "divisoes": divisoes,
        "abandonos": abandonos,
        "novos": novos,
        "codigos_movidos": codigos_movidos,
        "renomeados": renomeados,
        "efeito": "estrutural" if estrutural else "sem efeito estrutural",
    }
    if not estrutural:
        reg.alerta(
            "A09",
            "contestação sem efeito estrutural: de candidatos a finais só mudaram nomes ou nada mudou",
        )
    return resultado


def conferir_hipoteses(reg: Registro) -> dict:
    hipoteses = reg.por_tipo["hipotese"]
    destinos = Counter(str(h.get("destino")) for h in hipoteses.values())
    if not reg.temas("final"):
        return dict(destinos)
    if not hipoteses:
        reg.alerta("A10", "nenhuma hipótese de familiarização registrada: não há como testar ancoragem")
    else:
        if destinos.get("pendente"):
            reg.alerta("A10", f"{destinos['pendente']} hipótese(s) ainda sem destino ao fim da análise")
        if not destinos.get("revista") and not destinos.get("derrubada"):
            reg.alerta(
                "A10",
                "nenhuma hipótese de familiarização foi revista ou derrubada: conferir ancoragem na primeira leitura",
            )
        for ident, hipotese in hipoteses.items():
            if hipotese.get("destino") != "pendente" and not str(hipotese.get("evidencia") or "").strip():
                reg.erro("E01", "hipótese com destino declarado sem evidência", ident)
    return dict(destinos)


def conferir_verificacao(reg: Registro, path: Path) -> dict:
    linhas, problemas = ler_jsonl(path)
    for problema in problemas:
        reg.erro("E01", problema)
    estados = {str(l.get("citation_id")): str(l.get("status")) for l in linhas}
    contagem: Counter[str] = Counter()
    for ident, excerto in reg.excertos.items():
        if excerto.get("forma") != "literal":
            continue
        estado = estados.get(ident, "ausente_da_verificacao")
        contagem[estado] += 1
        if estado != "verified_exact":
            reg.erro("E04", f"excerto literal não verificado ({estado})", ident)
    return dict(contagem)


# ----------------------------------------------------------------- relatório


def fragmentos(citacao: str) -> list[str]:
    partes = [normalizar(p) for p in RE_ELIPSE.split(citacao)]
    return [p for p in partes if len(palavras(p)) >= 3]


def conferir_relatorio(reg: Registro, relatorios: list[Path]) -> dict:
    literais = {k: normalizar(str(v.get("texto"))) for k, v in reg.excertos.items() if v.get("forma") == "literal"}
    parafrases = {k: normalizar(str(v.get("texto"))) for k, v in reg.excertos.items() if v.get("forma") == "parafrase"}
    externas = {k: normalizar(str(v.get("texto"))) for k, v in reg.por_tipo["citacao_externa"].items()}
    publicados: set[str] = set()
    total = 0
    for path in relatorios:
        try:
            texto = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            reg.erro("E01", str(exc), path.name)
            continue
        blocos = paragrafos(texto)
        e_citacao = []
        for bloco in blocos:
            achadas = [c for c in RE_CITACAO.findall(bloco) if len(palavras(c)) >= MIN_PALAVRAS_CITACAO]
            for citacao in achadas:
                total += 1
                partes = fragmentos(citacao)
                if not partes:
                    continue
                dono = next((k for k, t in literais.items() if all(p in t for p in partes)), None)
                if dono:
                    publicados.add(dono)
                    continue
                if any(all(p in t for p in partes) for t in externas.values()):
                    continue
                trecho = citacao.strip()[:90]
                if any(all(p in t for p in partes) for t in parafrases.values()):
                    reg.erro("E09", f"paráfrase apresentada entre aspas: “{trecho}”", path.name)
                else:
                    reg.erro("E08", f"citação fora do registro de evidências: “{trecho}”", path.name)
            resto = len(palavras(sem_citacoes(bloco)))
            dentro = sum(len(palavras(c)) for c in achadas)
            e_citacao.append(bool(achadas) and dentro >= 4 * max(resto, 1) and not bloco.startswith("|"))
        for indice, marcado in enumerate(e_citacao):
            if not marcado:
                continue
            seguinte = blocos[indice + 1] if indice + 1 < len(blocos) else ""
            if not seguinte or seguinte.startswith("#") or e_citacao[indice + 1]:
                reg.alerta(
                    "A08",
                    f"citação sem comentário interpretativo em seguida: “{blocos[indice][:70]}”",
                    path.name,
                )
    return {"citacoes_no_relatorio": total, "excertos_publicados": sorted(publicados)}


def conferir_marcadores(reg: Registro, pasta: Path, templates: Path | None) -> None:
    modelo: set[str] = set()
    if templates and templates.is_dir():
        for path in arquivos_md(templates):
            for linha in path.read_text(encoding="utf-8-sig").splitlines():
                limpa = linha.strip()
                if limpa.startswith(("#", "|", ">", "```")) or len(palavras(limpa)) < 8:
                    continue
                modelo.add(normalizar(limpa))
    re_colchete = re.compile(r"\[([^\]\[]{12,})\](?!\()")
    for path in arquivos_md(pasta):
        for numero, linha in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            limpa = linha.strip()
            ref = f"{path.name}:{numero}"
            for conteudo in re_colchete.findall(limpa):
                if len(palavras(conteudo)) >= 4 and not RE_ELIPSE.fullmatch(conteudo.strip()):
                    reg.erro("E10", f"marcador de template não preenchido: [{conteudo[:60]}]", ref)
            if re.search(r"continuar para todos|\bTODO\b|lorem ipsum", limpa, re.IGNORECASE):
                reg.erro("E10", "resto de template ou anotação de rascunho", ref)
            if not limpa.startswith("|") and limpa.count(" | ") >= 2 and len(palavras(limpa)) <= 12:
                reg.erro("E10", f"alternativas do template não escolhidas: {limpa[:70]}", ref)
            if limpa.startswith("|") and not set(limpa) <= set("|-: "):
                celulas = [c.strip() for c in limpa.strip("|").split("|")]
                if len(celulas) >= 3 and celulas[0] and not any(celulas[1:]):
                    reg.erro("E10", f"linha de tabela vazia: {limpa[:60]}", ref)
            if modelo and normalizar(limpa) in modelo:
                reg.alerta("A11", f"frase copiada do template: {limpa[:70]}", ref)


def conferir_contagens(reg: Registro, pasta: Path) -> None:
    codigos = reg.codigos
    aceitos_codigos = {
        len(codigos),
        sum(1 for c in codigos.values() if c.get("estado", "ativo") == "ativo"),
        sum(1 for c in codigos.values() if c.get("estado", "ativo") != "recusado"),
    }
    aceitos = {
        "finais": {len(reg.temas("final"))},
        "candidatos": {len(reg.temas("candidato"))},
    }
    for path in arquivos_md(pasta):
        texto = sem_citacoes(path.read_text(encoding="utf-8-sig"))
        for numero in re.findall(r"\b(\d+)\s+c[óo]digos\b", texto):
            if int(numero) not in aceitos_codigos:
                reg.alerta(
                    "A07",
                    f"texto declara {numero} códigos; o registro tem {sorted(aceitos_codigos)}",
                    path.name,
                )
        for numero, fase in re.findall(r"\b(\d+)\s+temas\s+(finais|candidatos)\b", texto):
            if aceitos[fase] != {0} and int(numero) not in aceitos[fase]:
                reg.alerta(
                    "A07",
                    f"texto declara {numero} temas {fase}; o registro tem {sorted(aceitos[fase])}",
                    path.name,
                )


# ---------------------------------------------------- cobertura e distribuição


def conferir_leitura(reg: Registro, manifesto: Path, leitura: Path) -> dict:
    fontes, problemas = ler_jsonl(manifesto)
    lidos, problemas_leitura = ler_jsonl(leitura)
    for problema in problemas + problemas_leitura:
        reg.erro("E01", problema)
    intervalos: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for item in lidos:
        try:
            inicio, fim = int(item["inicio"]), int(item["fim"])
        except (KeyError, TypeError, ValueError):
            reg.erro("E01", "intervalo de leitura sem 'inicio' e 'fim' numéricos", f"linha {item['_linha']}")
            continue
        if not str(item.get("memo") or "").strip():
            reg.alerta("A14", "intervalo de leitura sem memo associado", str(item.get("fonte")))
        intervalos[str(item.get("fonte"))].append((inicio, fim))
    por_fonte, total, coberto = [], 0, 0
    for fonte in fontes:
        nome, linhas = str(fonte.get("source")), int(fonte.get("lines") or 0)
        marcadas = [False] * (linhas + 1)
        for inicio, fim in intervalos.get(nome, []):
            for posicao in range(max(inicio, 1), min(fim, linhas) + 1):
                marcadas[posicao] = True
        lidas = sum(marcadas)
        total += linhas
        coberto += lidas
        if lidas < linhas:
            por_fonte.append({"fonte": nome, "linhas": linhas, "lidas": lidas})
    estado = "integral" if total and coberto == total else "parcial"
    if estado == "parcial":
        reg.alerta(
            "A15",
            f"leitura declarada cobre {coberto} de {total} linhas: a cobertura é parcial e deve constar no estatuto",
            ", ".join(item["fonte"] for item in por_fonte[:8]),
        )
    return {"estado": estado, "linhas": total, "lidas": coberto, "fontes_incompletas": por_fonte}


def distribuicao(reg: Registro, manifesto: Path | None) -> dict:
    finais = reg.temas("final")
    matriz: dict[str, dict[str, int]] = {}
    posicoes: list[float] = []
    inicio_de: dict[str, int] = {}
    total = 0
    if manifesto:
        linhas, _ = ler_jsonl(manifesto)
        for item in linhas:
            inicio_de[str(item.get("source"))] = total
            total += int(item.get("lines") or 0)
    for tema_id, tema in finais.items():
        contagem: Counter[str] = Counter()
        for excerto_id in reg.excertos_do_tema(tema):
            excerto = reg.excertos.get(excerto_id)
            if not excerto:
                continue
            fonte = reg.fontes.get(str(excerto.get("fonte")), {})
            contagem[str(excerto.get("fonte"))] += 1
            achado = RE_LINHA.search(str(excerto.get("localizador") or ""))
            arquivo = str(fonte.get("arquivo"))
            if total and achado and arquivo in inicio_de:
                posicoes.append((inicio_de[arquivo] + int(achado.group(1))) / total)
        matriz[tema_id] = dict(sorted(contagem.items()))
    tercos = [0, 0, 0]
    for posicao in posicoes:
        tercos[min(int(posicao * 3), 2)] += 1
    if len(posicoes) >= 6 and max(tercos) >= 0.7 * len(posicoes):
        nomes = ("inicial", "intermediário", "final")
        reg.alerta(
            "A03",
            f"{max(tercos)} de {len(posicoes)} excertos vêm do terço {nomes[tercos.index(max(tercos))]} do corpus",
        )
    return {"tema_por_fonte": matriz, "excertos_por_terco_do_corpus": tercos}


# ------------------------------------------------------------------ comandos


def carregar(path: Path) -> Registro | None:
    registros, problemas = ler_jsonl(path)
    if problemas and not registros:
        gravar(None, {"erros": [{"codigo": "E01", "mensagem": p, "ref": ""} for p in problemas]})
        return None
    reg = Registro(registros)
    for problema in problemas:
        reg.erro("E01", problema)
    return reg


def cmd_integridade(args: argparse.Namespace) -> int:
    reg = carregar(args.registro)
    if reg is None:
        return 2
    resultado: dict = {}
    conferir_estrutura(reg)
    conferir_temas_finais(reg)
    resultado["diff_temas"] = diff_temas(reg)
    resultado["hipoteses"] = conferir_hipoteses(reg)
    if args.verificacao:
        resultado["verificacao"] = conferir_verificacao(reg, args.verificacao)
    if args.relatorio:
        resultado["relatorio"] = conferir_relatorio(reg, args.relatorio)
    if args.saida:
        conferir_marcadores(reg, args.saida, args.templates)
        conferir_contagens(reg, args.saida)
    if args.manifesto and args.leitura:
        resultado["cobertura"] = conferir_leitura(reg, args.manifesto, args.leitura)
    resultado["distribuicao"] = distribuicao(reg, args.manifesto)
    resultado["contagens"] = {
        "fontes": len(reg.fontes),
        "excertos_literais": sum(1 for e in reg.excertos.values() if e.get("forma") == "literal"),
        "parafrases": sum(1 for e in reg.excertos.values() if e.get("forma") == "parafrase"),
        "codigos": len(reg.codigos),
        "temas_candidatos": len(reg.temas("candidato")),
        "temas_finais": len(reg.temas("final")),
    }
    resultado["mediados"] = sorted(
        k for k, e in reg.excertos.items()
        if reg.fontes.get(str(e.get("fonte")), {}).get("estatuto") in ESTATUTOS_MEDIADOS
    )
    resultado["erros"], resultado["alertas"] = reg.erros, reg.alertas
    gravar(args.output, resultado)
    return 1 if reg.erros else 0


def cmd_citacoes(args: argparse.Namespace) -> int:
    reg = carregar(args.registro)
    if reg is None:
        return 2
    linhas = []
    for ident, excerto in reg.excertos.items():
        if excerto.get("forma") != "literal":
            continue
        fonte = reg.fontes.get(str(excerto.get("fonte")), {})
        linhas.append(
            {
                "citation_id": ident,
                "text": excerto.get("texto", ""),
                "source": fonte.get("arquivo", ""),
                "declared_locator": excerto.get("localizador", ""),
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(l, ensure_ascii=False) + "\n" for l in linhas), encoding="utf-8"
    )
    return 0 if linhas else 2


def cmd_tabelas(args: argparse.Namespace) -> int:
    reg = carregar(args.registro)
    if reg is None:
        return 2
    conferir_estrutura(reg)
    saida = ["# Genealogia gerada do registro de evidências", ""]
    saida.append("Gerado por `auditar_analise.py tabelas`. Não editar à mão: corrigir o registro e gerar de novo.")
    for fase, titulo in (("final", "Temas finais"), ("candidato", "Temas candidatos")):
        temas = reg.temas(fase)
        if not temas:
            continue
        saida += ["", f"## {titulo}", ""]
        for tema_id, tema in temas.items():
            origem = ", ".join(tema.get("origem") or []) or "—"
            saida += [f"### {tema_id} — {tema.get('nome')}", "", f"- conceito organizador: {tema.get('conceito')}"]
            if fase == "final":
                saida.append(f"- origem: {origem}")
            saida += ["", "| Código | Rótulo | Excerto | Forma | Fonte | Localizador |", "|---|---|---|---|---|---|"]
            for codigo_id in tema.get("codigos") or []:
                codigo = reg.codigos.get(codigo_id, {})
                for excerto_id in codigo.get("excertos") or [""]:
                    excerto = reg.excertos.get(excerto_id, {})
                    saida.append(
                        f"| {codigo_id} | {codigo.get('rotulo', '')} | {excerto_id} | {excerto.get('forma', '')} "
                        f"| {excerto.get('fonte', '')} | {excerto.get('localizador', '')} |"
                    )
            saida.append("")
    fora = [k for k, c in reg.codigos.items() if c.get("estado", "ativo") != "ativo"]
    if fora:
        saida += ["## Códigos fundidos, recusados ou tratados como resíduo", "", "| Código | Rótulo | Estado | Destino ou justificativa |", "|---|---|---|---|"]
        for codigo_id in fora:
            codigo = reg.codigos[codigo_id]
            saida.append(
                f"| {codigo_id} | {codigo.get('rotulo', '')} | {codigo.get('estado')} "
                f"| {codigo.get('destino') or codigo.get('justificativa') or ''} |"
            )
        saida.append("")
    diferenca = diff_temas(reg)
    if diferenca:
        saida += ["## De candidatos a finais", "", f"- efeito da contestação: {diferenca['efeito']}"]
        for chave in ("fusoes", "divisoes", "abandonos", "novos"):
            saida.append(f"- {chave}: {', '.join(diferenca[chave]) or 'nenhum'}")
        saida.append("")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(saida) + "\n", encoding="utf-8")
    return 0


RE_PRIVACIDADE = {
    "e-mail": re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    "telefone": re.compile(r"(?<!\d)(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}(?!\d)"),
    "CPF": re.compile(r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)"),
    "perfil em rede": re.compile(r"(?<![\w/])@[A-Za-z0-9_.]{3,}"),
}
RE_NOME = re.compile(
    r"\b[A-ZÀ-Ý][a-zà-ÿ]+(?:\s+(?:d[aeo]s?\s+)?[A-ZÀ-Ý][a-zà-ÿ]+)*(?:\s+[A-Z]\.)?"
)
# Palavras que aparecem em maiúscula sem identificar ninguém.
NAO_NOMES = {
    "análise", "temática", "reflexiva", "braun", "clarke", "markdown", "python", "tema",
    "temas", "código", "códigos", "fonte", "fontes", "excerto", "fase", "relatório",
    "dossiê", "apêndice", "tabela", "figura", "brasil", "estado", "deus", "internet",
    "essencial", "aprofundada", "isolado", "sequencial", "claude", "sonnet", "opus", "haiku",
    "gpt", "gemini", "codex", "deepseek", "qwen", "mistral", "llama", "openai", "anthropic",
    "google", "windows", "linux", "json", "utf",
    "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
    "setembro", "outubro", "novembro", "dezembro",
}


def cmd_privacidade(args: argparse.Namespace) -> int:
    conhecidos: list[str] = []
    if args.nomes:
        conhecidos = [l.strip() for l in args.nomes.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    achados: dict[tuple[str, str], list[str]] = defaultdict(list)
    for path in arquivos_md(args.saida):
        for numero, linha in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            ref = f"{path.name}:{numero}"
            for classe, padrao in RE_PRIVACIDADE.items():
                for item in padrao.findall(linha):
                    achados[(classe, item.strip())].append(ref)
            for nome in conhecidos:
                if re.search(rf"(?<!\w){re.escape(nome)}(?!\w)", linha, re.IGNORECASE):
                    achados[("nome informado pelo usuário", nome)].append(ref)
            corpo = re.sub(r"^[\s#>*\-|\d.]+", "", linha)
            for encontro in RE_NOME.finditer(corpo):
                nome = encontro.group(0)
                anterior = corpo[: encontro.start()].rstrip()
                inicio_de_frase = not anterior or anterior[-1] in ".!?:|(“\"*—–-"
                partes = nome.split()
                if all(p.lower().strip(".") in NAO_NOMES for p in partes):
                    continue
                abreviado = bool(re.search(r"\s[A-Z]\.$", nome))
                if abreviado:
                    achados[("nome com sobrenome abreviado", nome)].append(ref)
                elif len(partes) > 1 or not inicio_de_frase:
                    achados[("possível nome próprio", nome)].append(ref)
    itens = [
        {"classe": classe, "texto": texto, "ocorrencias": len(refs), "onde": refs[:5]}
        for (classe, texto), refs in sorted(achados.items(), key=lambda kv: (kv[0][0], -len(kv[1])))
    ]
    gravar(
        args.output,
        {
            "orientacao": "Lista de candidatos, não decisão. Mostrar ao usuário e perguntar o que fazer com cada classe.",
            "candidatos": itens,
        },
    )
    return 1 if itens else 0


PADROES_SOBREALEGACAO = {
    "generalização": r"\btod[oa]s\s+[oa]s\b|\bsempre\b|\bnunca\b|\bninguém\b|\ba maioria\b|\bem geral\b|\bunânim\w*|\bpredominant\w*|\bdominante\w*|\bo eleitor\b|\bos brasileiros\b|\ba população\b",
    "causalidade": r"\bcausa[mr]?\b|\bleva[m]?\s+[aà]\b|\bprovoca[m]?\b|\bresulta[m]?\s+em\b|\bpor causa de\b|\btende[m]?\s+a\b|\bdetermina[m]?\b|\bprova[m]?\s+que\b|\bdemonstra[m]?\s+que\b|\bcomprova[m]?\b|\bexplica[m]?\s+por\s+que\b|\bfaz(?:em)?\s+com\s+que\b|\bgarante[m]?\b",
    "quantificação": r"\d+\s?%|\b\d+\s+(?:de|dos|das)\s+\d+\b|\bminoria\b",
    "vocabulário incompatível com ATR": r"\bemerg\w+|\bsaturaç\w+|\bvi[ée]s\b|\bvieses\b|\bvariáve(?:l|is)\s+(?:in)?dependentes?\b|\bcorrelacion\w+|\bconfiabilidade\b|\brepresentativ\w+|\bgeneraliz\w+|\btriangulaç\w+|\bconsenso entre\b|\bconcordância entre\b",
}


def cmd_sobrealegacao(args: argparse.Namespace) -> int:
    itens = []
    for path in args.relatorio:
        for numero, linha in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            for frase in re.split(r"(?<=[.!?;])\s+", sem_citacoes(linha)):
                for classe, padrao in PADROES_SOBREALEGACAO.items():
                    for encontro in re.finditer(padrao, frase, re.IGNORECASE):
                        antes = frase[: encontro.start()]
                        itens.append(
                            {
                                "classe": classe,
                                "termo": encontro.group(0),
                                "onde": f"{path.name}:{numero}",
                                "frase": frase.strip()[:240],
                                # Termo usado para recusar ("não busquei saturação") costuma ser legítimo.
                                "negado_na_frase": bool(re.search(r"\b(não|sem|nem|nenhum\w*|recus\w+|evit\w+)\b", antes, re.IGNORECASE)),
                            }
                        )
    gravar(
        args.output,
        {
            "orientacao": "Cada item pede uma de três respostas: manter com a evidência que sustenta, restringir ou cortar. Termos negados ou citados para recusar não são falha.",
            "itens": itens,
        },
    )
    return 1 if itens else 0


def cmd_homogeneizacao(args: argparse.Namespace) -> int:
    molde: set[tuple[str, ...]] = set()
    titulos_do_molde: set[str] = set()

    def perfil(path: Path) -> tuple[set[tuple[str, ...]], list[str]]:
        texto = path.read_text(encoding="utf-8-sig")
        titulos = [normalizar(l.lstrip("#")) for l in texto.splitlines() if l.startswith("#")]
        termos = palavras(normalizar(sem_citacoes(texto)))
        return {tuple(termos[i : i + 6]) for i in range(len(termos) - 5)}, titulos

    if args.templates and args.templates.is_dir():
        for path in arquivos_md(args.templates):
            trechos, titulos = perfil(path)
            molde |= trechos
            titulos_do_molde |= set(titulos)
    perfis = {}
    for path in args.relatorios:
        trechos, titulos = perfil(path)
        rotulo = f"{path.parent.name}/{path.name}"
        perfis[rotulo] = (trechos - molde, [t for t in titulos if t not in titulos_do_molde])
    pares, acima = [], False
    nomes = sorted(perfis)
    for i, a in enumerate(nomes):
        for b in nomes[i + 1 :]:
            ta, tb = perfis[a][0], perfis[b][0]
            uniao = len(ta | tb)
            indice = round(len(ta & tb) / uniao, 4) if uniao else 0.0
            titulos = sorted(
                {
                    f"{x} ~ {y}"
                    for x in perfis[a][1]
                    for y in perfis[b][1]
                    if len(palavras(x)) >= 4 and SequenceMatcher(None, x, y).ratio() >= 0.75
                }
            )
            alerta = indice >= args.limiar or bool(titulos)
            acima = acima or alerta
            pares.append({"par": [a, b], "texto_em_comum": indice, "titulos_parecidos": titulos, "alerta": alerta})
    gravar(
        args.output,
        {
            "limiar": args.limiar,
            "orientacao": "Semelhança alta entre casos pede releitura: o padrão é dos dados ou do molde da análise?",
            "pares": sorted(pares, key=lambda p: -p["texto_em_comum"]),
        },
    )
    return 1 if acima else 0


# Gabarito do teste de aptidão. Quem executa a análise não deve abrir este
# trecho antes de responder: o teste mede o que o modelo faz sem consulta.
GABARITO_CLASSIFICACAO = {"A": "topico", "B": "tema", "C": "topico", "D": "tema", "E": "topico", "F": "tema"}
GABARITO_NAO_LITERAIS = {"X2", "X4", "X5"}


def cmd_aptidao(args: argparse.Namespace) -> int:
    corpus = (Path(__file__).resolve().parent / "aptidao" / "microcorpus.txt").read_text(encoding="utf-8").splitlines()
    try:
        respostas = json.loads(args.respostas.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        gravar(args.output, {"resultado": "invalido", "erro": str(exc)})
        return 2
    citacoes = respostas.get("citacoes") or []
    corretas, vistas = 0, set()
    for item in citacoes:
        texto, linha = str(item.get("texto", "")), item.get("linha")
        if (
            isinstance(linha, int)
            and 1 <= linha <= len(corpus)
            and len(palavras(texto)) >= 6
            and texto in corpus[linha - 1]
            and texto not in vistas
        ):
            corretas += 1
            vistas.add(texto)
    classificacao = respostas.get("classificacao") or {}
    acertos = sum(1 for k, v in GABARITO_CLASSIFICACAO.items() if str(classificacao.get(k, "")).lower() == v)
    nao_literais = {str(x).upper() for x in respostas.get("nao_literais") or []}
    partes = {
        "citacao_literal": corretas >= 3 and len(citacoes) == corretas,
        "tema_ou_topico": acertos >= 5,
        "deteccao_de_citacao_alterada": nao_literais == GABARITO_NAO_LITERAIS,
    }
    if all(partes.values()):
        resultado = "apto"
    elif partes["citacao_literal"]:
        resultado = "parcial"
    else:
        resultado = "inapto"
    gravar(
        args.output,
        {
            "resultado": resultado,
            "partes": partes,
            "detalhe": {"citacoes_corretas": corretas, "classificacoes_corretas": acertos},
        },
    )
    return 0 if resultado == "apto" else 1


def main(argv: list[str] | None = None) -> int:
    # Consoles que não usam UTF-8 por padrão corrompem os acentos da saída.
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="comando", required=True)

    p = sub.add_parser("integridade", help="confere o registro de evidências e os arquivos de saída")
    p.add_argument("--registro", required=True, type=Path)
    p.add_argument("--verificacao", type=Path, help="saída de verificar_citacoes.py")
    p.add_argument("--relatorio", type=Path, action="append", help="relatório analítico (repetível)")
    p.add_argument("--saida", type=Path, help="pasta com os arquivos .md da análise")
    p.add_argument("--templates", type=Path, help="pasta de templates da skill")
    p.add_argument("--manifesto", type=Path)
    p.add_argument("--leitura", type=Path)
    p.add_argument("--output", type=Path)
    p.set_defaults(func=cmd_integridade)

    p = sub.add_parser("citacoes", help="exporta os excertos literais para verificar_citacoes.py")
    p.add_argument("--registro", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.set_defaults(func=cmd_citacoes)

    p = sub.add_parser("tabelas", help="gera a genealogia em Markdown a partir do registro")
    p.add_argument("--registro", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.set_defaults(func=cmd_tabelas)

    p = sub.add_parser("privacidade", help="lista possíveis identificadores pessoais na saída")
    p.add_argument("--saida", required=True, type=Path)
    p.add_argument("--nomes", type=Path, help="lista de nomes reais conhecidos, um por linha")
    p.add_argument("--output", type=Path)
    p.set_defaults(func=cmd_privacidade)

    p = sub.add_parser("sobrealegacao", help="marca generalizações, causalidade e vocabulário incompatível")
    p.add_argument("--relatorio", required=True, type=Path, action="append")
    p.add_argument("--output", type=Path)
    p.set_defaults(func=cmd_sobrealegacao)

    p = sub.add_parser("homogeneizacao", help="mede semelhança entre relatórios de casos diferentes")
    p.add_argument("--relatorios", required=True, type=Path, nargs="+")
    p.add_argument("--templates", type=Path)
    p.add_argument("--limiar", type=float, default=LIMIAR_HOMOGENEIZACAO)
    p.add_argument("--output", type=Path)
    p.set_defaults(func=cmd_homogeneizacao)

    p = sub.add_parser("aptidao", help="corrige o teste de aptidão do modelo")
    p.add_argument("--respostas", required=True, type=Path)
    p.add_argument("--output", type=Path)
    p.set_defaults(func=cmd_aptidao)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
