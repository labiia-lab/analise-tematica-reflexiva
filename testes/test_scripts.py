#!/usr/bin/env python3
"""Testes executáveis para scripts/verificar_citacoes.py (Python padrão)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


class CitationVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        (self.base / "entrevista-01.txt").write_text(
            "Primeira linha.\nNa minha opinião o pior de todos. É uma falta.\n",
            encoding="utf-8",
        )
        (self.base / "entrevista-02.txt").write_text(
            "Então, o sistema eleitoral brasileiro é o melhor que tem do mundo.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _verify(self, record: dict) -> dict:
        from verificar_citacoes import verify

        result, valid = verify(record, self.base)
        self.assertTrue(valid)
        return result

    def test_exact_extract_is_verified(self) -> None:
        result = self._verify(
            {
                "citation_id": "Q001",
                "text": "o pior de todos",
                "source": "entrevista-01.txt",
                "declared_locator": "linha 2",
            }
        )
        self.assertEqual(result["status"], "verified_exact")
        self.assertEqual(result["computed_locators"], ["linha 2"])

    def test_surface_differences_are_relocalized(self) -> None:
        result = self._verify(
            {
                "citation_id": "Q002",
                "text": "o PIOR  de   todos. É uma falta",
                "source": "entrevista-01.txt",
                "declared_locator": "linha 10",
            }
        )
        self.assertEqual(result["status"], "relocalizado")
        self.assertEqual(result["candidate_exact"], "o pior de todos. É uma falta")
        self.assertEqual(result["relocated_locator"], "linha 2")
        self.assertEqual(result["metodo"], "normalizado")

    def test_truncated_extract_is_relocalized_in_another_source(self) -> None:
        result = self._verify(
            {
                "citation_id": "Q003",
                "text": "o sistema eleitoral brasileiro é o melhor que tem do mundo",
                "source": "entrevista-01.txt",
                "declared_locator": "linha 1",
            }
        )
        self.assertEqual(result["status"], "relocalizado")
        self.assertEqual(result["relocated_source"], "entrevista-02.txt")
        self.assertEqual(
            result["candidate_exact"],
            "o sistema eleitoral brasileiro é o melhor que tem do mundo",
        )

    def test_word_drift_suggests_substitution(self) -> None:
        result = self._verify(
            {
                "citation_id": "Q004",
                "text": "o nosso sistema eleitoral brasileiro é o melhor que tem do mundo",
                "source": "entrevista-01.txt",
                "declared_locator": "linha 1",
            }
        )
        self.assertEqual(result["status"], "substituir")
        self.assertGreaterEqual(result["similaridade"], 0.80)
        self.assertEqual(result["suggested_source"], "entrevista-02.txt")
        self.assertIn("sistema eleitoral brasileiro", result["suggested_text"])

    def test_paraphrase_far_from_corpus_is_not_found(self) -> None:
        result = self._verify(
            {
                "citation_id": "Q005",
                "text": "extrato parafraseado desconexo do corpus",
                "source": "entrevista-01.txt",
                "declared_locator": "linha 1",
            }
        )
        self.assertEqual(result["status"], "not_found")

    def test_locator_mismatch_on_exact_text(self) -> None:
        result = self._verify(
            {
                "citation_id": "Q006",
                "text": "o pior de todos",
                "source": "entrevista-01.txt",
                "declared_locator": "linha 5",
            }
        )
        self.assertEqual(result["status"], "exact_locator_mismatch")


class CliSmokeTests(unittest.TestCase):
    def test_inventory_output_is_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "a.txt").write_text("linha\n", encoding="utf-8")
            out = tmp / "manifesto.jsonl"
            code = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "verificar_citacoes.py"),
                    "--inventario",
                    str(tmp),
                    "--output",
                    str(out),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(code.returncode, 0)
            rows = [json.loads(line) for line in out.read_text(encoding="utf-8-sig").splitlines()]
            self.assertEqual(rows[0]["source"], "a.txt")
            self.assertIn("sha256", rows[0])

    def test_full_citation_run_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "f.txt").write_text("fala literal do participante.\n", encoding="utf-8")
            cit = tmp / "citacoes.jsonl"
            cit.write_text(
                json.dumps(
                    {"citation_id": "Q1", "text": "fala literal do participante",
                     "source": "f.txt", "declared_locator": "linha 1"},
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            out = tmp / "ver.jsonl"
            code = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "verificar_citacoes.py"),
                    "--input",
                    str(cit),
                    "--base",
                    str(tmp),
                    "--output",
                    str(out),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(code.returncode, 0)
            record = json.loads(out.read_text(encoding="utf-8-sig").splitlines()[0])
            self.assertEqual(record["status"], "verified_exact")


if __name__ == "__main__":
    unittest.main()
