#!/usr/bin/env python3
"""Verifica citações UTF-8 e inventaria arquivos do corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


REQUIRED = ("citation_id", "text", "source", "declared_locator")
SIMILAR_THRESHOLD = 0.80


def locators(text: str, needle: str) -> list[str]:
    found: list[str] = []
    start = 0
    while (offset := text.find(needle, start)) >= 0:
        first = text.count("\n", 0, offset) + 1
        last = first + needle.count("\n")
        found.append(f"linha {first}" if first == last else f"linhas {first}-{last}")
        start = offset + max(len(needle), 1)
    return found


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalized_pattern(value: str) -> re.Pattern[str] | None:
    words = normalized(value).lower().split()
    if not words:
        return None
    return re.compile(r"\s+".join(re.escape(word) for word in words), re.IGNORECASE)


def similar_search(needle: str, text: str) -> tuple[float, str, int]:
    from difflib import SequenceMatcher

    best_score, best_seg, best_pos = 0.0, "", 0
    lines = text.splitlines()
    offsets: list[int] = []
    acc = 0
    for line in lines:
        offsets.append(acc)
        acc += len(line) + 1
    for i in range(len(lines)):
        for size in range(1, 6):
            fim_i = i + size
            if fim_i > len(lines):
                break
            seg = "\n".join(lines[i:fim_i])
            score = SequenceMatcher(None, needle, seg).ratio()
            if score > best_score:
                best_score, best_seg, best_pos = score, seg, offsets[i]
    return best_score, best_seg, best_pos


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def corpus_files(base: Path, exclude: frozenset[Path] = frozenset()) -> list[Path]:
    if not base.is_dir():
        return []
    excluded = {p.resolve() for p in exclude}
    return sorted(
        (p for p in base.rglob("*") if p.is_file() and p.resolve() not in excluded),
        key=lambda p: p.as_posix(),
    )


def decode(raw: bytes) -> str | None:
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None


def relocate(
    needle: str, base: Path, declared: Path, exclude: frozenset[Path] = frozenset()
) -> dict[str, object] | None:
    """Busca normalizada (caixa, espacos, quebras, prefixos) em todos os arquivos.

    A fonte declarada pode estar errada: o trecho pode existir em outro arquivo
    ou com diferencas de superficie (espaco duplo, caixa alta, prefixo de
    locutor no inicio da linha, truncamento). Isso nao significa ausencia.
    """
    pattern = normalized_pattern(needle)
    if pattern is None:
        return None
    for path in corpus_files(base, exclude):
        if path.resolve() == declared.resolve():
            continue
        text = decode(path.read_bytes())
        if text is None:
            continue
        match = pattern.search(text)
        if match is None:
            continue
        exact = text[match.start() : match.end()]
        found = locators(text, exact)
        return {
            "relocated_source": path.relative_to(base).as_posix(),
            "relocated_locator": found[0] if found else "",
            "candidate_exact": exact,
            "relocated_sha256": sha256(path.read_bytes()),
            "metodo": "normalizado",
        }
    return None


def suggest(
    needle: str, base: Path, exclude: frozenset[Path] = frozenset()
) -> dict[str, object] | None:
    """Melhor trecho similar para substituicao (>= 0.80)."""
    best: dict[str, object] | None = None
    for path in corpus_files(base, exclude):
        text = decode(path.read_bytes())
        if text is None:
            continue
        score, seg, pos = similar_search(needle, text)
        if best is None or score > best["similaridade"]:
            found = locators(text, seg)
            best = {
                "similaridade": round(score, 3),
                "suggested_source": path.relative_to(base).as_posix(),
                "suggested_locator": found[0] if found else "",
                "suggested_text": seg,
                "metodo": "similar",
            }
    if best is None or best["similaridade"] < SIMILAR_THRESHOLD:
        return None
    return best


def inventory(base: Path, output: Path) -> tuple[list[dict[str, object]], bool]:
    if not base.is_dir():
        return [{"status": "invalid_record", "error": "corpus não é diretório"}], False

    excluded = output.resolve()
    rows: list[dict[str, object]] = []
    try:
        files = sorted(
            (path for path in base.rglob("*") if path.is_file()),
            key=lambda path: path.relative_to(base).as_posix(),
        )
        for path in files:
            if path.resolve() == excluded:
                continue
            raw = path.read_bytes()
            rows.append(
                {
                    "source": path.relative_to(base).as_posix(),
                    "bytes": len(raw),
                    "lines": len(raw.splitlines()),
                    "sha256": sha256(raw),
                }
            )
    except OSError as exc:
        return [{"status": "invalid_record", "error": str(exc)}], False
    if not rows:
        return [{"status": "invalid_record", "error": "corpus sem arquivos"}], False
    return rows, True


def verify(
    record: object, base: Path, exclude: frozenset[Path] = frozenset()
) -> tuple[dict[str, object], bool]:
    if (
        not isinstance(record, dict)
        or any(key not in record or not isinstance(record[key], str) for key in REQUIRED)
        or any(not record[key].strip() for key in ("citation_id", "text", "source"))
    ):
        citation_id = record.get("citation_id", "") if isinstance(record, dict) else ""
        return {
            "citation_id": citation_id,
            "status": "invalid_record",
            "error": f"campos obrigatórios: {', '.join(REQUIRED)}",
        }, False

    result: dict[str, object] = {
        "citation_id": record["citation_id"],
        "source": record["source"],
        "declared_locator": record["declared_locator"],
    }
    source = Path(record["source"])
    if not source.is_absolute():
        source = base / source
    if not source.is_file():
        result.update(status="source_missing", computed_locators=[], source_sha256="")
        return result, True

    try:
        raw = source.read_bytes()
    except OSError as exc:
        result.update(
            status="source_unreadable",
            computed_locators=[],
            source_sha256="",
            error=str(exc),
        )
        return result, True
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        result.update(
            status="source_unreadable",
            computed_locators=[],
            source_sha256=sha256(raw),
            error=str(exc),
        )
        return result, True

    matches = locators(text, record["text"])
    result["computed_locators"] = matches
    result["source_sha256"] = sha256(raw)
    result["match_count"] = len(matches)

    declared = record["declared_locator"].strip()
    if len(matches) == 1:
        if declared and declared != matches[0]:
            result["status"] = "exact_locator_mismatch"
        else:
            result["status"] = "verified_exact"
        return result, True
    if len(matches) > 1:
        result["status"] = (
            "verified_exact" if declared in matches else "exact_multiple_needs_locator"
        )
        return result, True

    # Passo 2: relocalizacao por texto normalizado (caixa/espacos/quebras/prefixos)
    pattern = normalized_pattern(record["text"])
    if pattern is not None:
        match = pattern.search(text)
        if match is not None:
            exact = text[match.start() : match.end()]
            found = locators(text, exact)
            result.update(
                status="relocalizado",
                relocated_source=record["source"],
                relocated_locator=found[0] if found else "",
                candidate_exact=exact,
                relocated_sha256=result.get("source_sha256", ""),
                metodo="normalizado",
            )
            return result, True

    relocated = relocate(record["text"], base, source, exclude)
    if relocated is not None:
        result.update(status="relocalizado", **relocated)
        return result, True

    # Passo 3: substituicao pelo trecho similar mais proximo
    suggested = suggest(record["text"], base, exclude)
    if suggested is not None:
        result["status"] = "substituir"
        result["trecho_original"] = record["text"]
        result.update(
            similaridade=suggested["similaridade"],
            suggested_source=suggested["suggested_source"],
            suggested_locator=suggested["suggested_locator"],
            suggested_text=suggested["suggested_text"],
        )
        return result, True

    result["status"] = "not_found"
    return result, True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--input", type=Path, help="JSONL de citações")
    mode.add_argument("--inventario", type=Path, help="diretório do corpus")
    parser.add_argument("--base", type=Path, help="diretório das fontes")
    parser.add_argument("--output", required=True, type=Path, help="JSONL de resultados")
    args = parser.parse_args()

    if args.inventario is not None:
        results, valid = inventory(args.inventario, args.output)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in results),
            encoding="utf-8",
        )
        return 0 if valid else 2
    if args.base is None:
        parser.error("--base é obrigatório com --input")

    exclude = frozenset({args.input.resolve(), args.output.resolve()})
    results: list[dict[str, object]] = []
    invalid = False
    try:
        lines = args.input.read_text(encoding="utf-8-sig").splitlines()
        for line_number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                record: object = json.loads(line)
            except json.JSONDecodeError as exc:
                record = {"citation_id": "", "_error": str(exc)}
            result, valid = verify(record, args.base, exclude)
            if not valid:
                invalid = True
                result["input_line"] = line_number
            results.append(result)
        if not results:
            results = [
                {
                    "citation_id": "",
                    "status": "invalid_record",
                    "error": "nenhuma citação informada",
                }
            ]
            invalid = True
    except OSError as exc:
        results = [{"citation_id": "", "status": "invalid_record", "error": str(exc)}]
        invalid = True

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in results),
        encoding="utf-8",
    )
    if invalid:
        return 2
    return 0 if all(row["status"] == "verified_exact" for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
