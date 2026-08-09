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


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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


def verify(record: object, base: Path) -> tuple[dict[str, object], bool]:
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
    elif len(matches) > 1:
        result["status"] = (
            "verified_exact" if declared in matches else "exact_multiple_needs_locator"
        )
    elif normalized(record["text"]) in normalized(text):
        result["status"] = "normalized_candidate_not_verified"
    else:
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
            result, valid = verify(record, args.base)
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
