import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verificar_citacoes.py"


class VerificarCitacoesTest(unittest.TestCase):
    def run_script(self, records, extra_sources=None):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "fonte.txt").write_text(
                "Primeira fala literal.\nA fala repetida.\nA fala repetida.\n",
                encoding="utf-8",
            )
            for name, content in (extra_sources or {}).items():
                path = base / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            input_path = base / "citacoes.jsonl"
            output_path = base / "resultado.jsonl"
            input_path.write_text(
                "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--base",
                    str(base),
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            rows = []
            if output_path.exists():
                rows = [
                    json.loads(line)
                    for line in output_path.read_text(encoding="utf-8").splitlines()
                ]
            return result, rows

    def test_exact_quote_is_verified(self):
        result, rows = self.run_script(
            [
                {
                    "citation_id": "Q1",
                    "text": "Primeira fala literal.",
                    "source": "fonte.txt",
                    "declared_locator": "linha 1",
                }
            ]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(rows[0]["status"], "verified_exact")
        self.assertEqual(rows[0]["computed_locators"], ["linha 1"])
        self.assertEqual(len(rows[0]["source_sha256"]), 64)

    def test_non_exact_results_fail_closed(self):
        result, rows = self.run_script(
            [
                {
                    "citation_id": "Q2",
                    "text": "A fala repetida.",
                    "source": "fonte.txt",
                    "declared_locator": "",
                },
                {
                    "citation_id": "Q3",
                    "text": "Primeira   fala literal.",
                    "source": "fonte.txt",
                    "declared_locator": "linha 1",
                },
                {
                    "citation_id": "Q4",
                    "text": "Fala ausente.",
                    "source": "fonte.txt",
                    "declared_locator": "",
                },
                {
                    "citation_id": "Q5",
                    "text": "Qualquer fala.",
                    "source": "ausente.txt",
                    "declared_locator": "",
                },
                {
                    "citation_id": "Q6",
                    "text": "Primeira fala literal.",
                    "source": "fonte.txt",
                    "declared_locator": "linha 99",
                },
            ]
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            [row["status"] for row in rows],
            [
                "exact_multiple_needs_locator",
                "normalized_candidate_not_verified",
                "not_found",
                "source_missing",
                "exact_locator_mismatch",
            ],
        )

    def test_invalid_record_returns_usage_error(self):
        result, rows = self.run_script(
            [
                {"citation_id": "Q7"},
                {
                    "citation_id": "Q8",
                    "text": "",
                    "source": "fonte.txt",
                    "declared_locator": "",
                },
            ]
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            [row["status"] for row in rows],
            ["invalid_record", "invalid_record"],
        )

    def test_empty_input_is_invalid(self):
        result, rows = self.run_script([])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(rows[0]["status"], "invalid_record")

    def test_existing_non_utf8_source_is_unreadable_not_missing(self):
        result, rows = self.run_script(
            [
                {
                    "citation_id": "Q9",
                    "text": "fala",
                    "source": "binario.txt",
                    "declared_locator": "",
                }
            ],
            {"binario.txt": b"\xff\xfe\x00\x01"},
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(rows[0]["status"], "source_unreadable")
        self.assertEqual(len(rows[0]["source_sha256"]), 64)

    def test_inventory_mode_emits_deterministic_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            corpus = base / "corpus"
            (corpus / "sub").mkdir(parents=True)
            (corpus / "a.txt").write_text("um\ndois\n", encoding="utf-8")
            (corpus / "sub" / "b.bin").write_bytes(b"\x00\x01")
            expected_bytes = len((corpus / "a.txt").read_bytes())
            output = corpus / "manifesto-corpus.jsonl"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--inventario",
                    str(corpus),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            rows = [
                json.loads(line)
                for line in output.read_text(encoding="utf-8").splitlines()
            ]

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row["source"] for row in rows], ["a.txt", "sub/b.bin"])
        self.assertEqual(rows[0]["bytes"], expected_bytes)
        self.assertEqual(rows[0]["lines"], 2)
        self.assertEqual(len(rows[0]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
