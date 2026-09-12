import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "gerar_mapa_tematico.py"

ESTRUTURA = {
    "codigos": {
        "itens": [
            {"id": "1", "texto": "Identificar requisitos de tolerância", "grupo": 1},
            {"id": "2", "texto": "Selecionar a classe de tolerância", "grupo": 1},
            {"id": "3", "texto": "Identificar conexões com riscos", "grupo": 1},
        ]
    },
    "temas_candidatos": {
        "itens": [
            {"id": "1", "texto": "Identificar requisitos dimensionais", "codigos": ["1"], "grupo": 1},
            {"id": "2", "texto": "Selecionar a classe de tolerâncias", "codigos": ["2"], "grupo": 1},
            {"id": "3", "texto": "Identificar riscos de tolerância", "codigos": ["3"], "grupo": 1},
        ]
    },
    "temas_finais": {
        "itens": [
            {"id": "TF1", "rotulo": "Tema 1", "texto": "IDENTIFICAÇÃO", "candidatos": ["1", "2", "3"], "grupo": 1},
        ]
    },
}


class GerarMapaTematicoTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)

    def run_script(self, dados, png=False):
        base = self.base
        entrada = base / "mapa.json"
        saida = base / "mapa.svg"
        entrada.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        comando = [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(entrada),
            "--output",
            str(saida),
        ]
        if png:
            comando += ["--png", str(base / "saida.png")]
        result = subprocess.run(
            comando, capture_output=True, text=True, encoding="utf-8"
        )
        svg = saida.read_text(encoding="utf-8") if saida.exists() else ""
        return result, svg, base

    def test_valid_structure_generates_svg_with_canvas_and_columns(self):
        result, svg, _ = self.run_script(ESTRUTURA)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('width="1448" height="1086"', svg)
        self.assertIn("Códigos", svg)
        self.assertIn("Temas candidatos", svg)
        self.assertIn("Temas finais", svg)
        self.assertIn("IDENTIFICAÇÃO", svg)
        self.assertGreaterEqual(svg.count("<rect"), 8)
        self.assertGreaterEqual(svg.count("<line"), 5)
        self.assertGreaterEqual(svg.count("<polygon"), 5)

    def test_broken_relation_is_rejected(self):
        quebrada = json.loads(json.dumps(ESTRUTURA))
        quebrada["temas_candidatos"]["itens"][0]["codigos"] = ["99"]
        result, svg, _ = self.run_script(quebrada)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(svg, "")
        self.assertIn("código inexistente", result.stderr)

    def test_candidate_without_final_theme_is_rejected(self):
        quebrada = json.loads(json.dumps(ESTRUTURA))
        quebrada["temas_candidatos"]["itens"].append(
            {"id": "4", "texto": "Tema órfão", "codigos": ["1"]}
        )
        result, _, _ = self.run_script(quebrada)
        self.assertEqual(result.returncode, 2)
        self.assertIn("sem tema final de destino", result.stderr)

    def test_manual_breaks_are_preserved(self):
        dados = json.loads(json.dumps(ESTRUTURA))
        dados["codigos"]["itens"][0]["linhas"] = ["Primeira linha", "Segunda linha"]
        result, svg, _ = self.run_script(dados)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(">Primeira linha<", svg)
        self.assertIn(">Segunda linha<", svg)

    def test_png_is_always_produced(self):
        result, svg, base = self.run_script(ESTRUTURA, png=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("svg", svg[:200].lower())
        png = base / "saida.png"
        self.assertTrue(png.exists(), result.stderr)
        self.assertGreater(png.stat().st_size, 1000)

    def test_default_png_path_matches_svg(self):
        result, _, base = self.run_script(ESTRUTURA)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((base / "mapa.png").exists(), result.stderr)

    def test_long_text_shrinks_font_instead_of_overflowing(self):
        dados = json.loads(json.dumps(ESTRUTURA))
        dados["temas_finais"]["itens"][0]["linhas"] = [
            "IDENTIFICAÇÃO DE REQUISITOS",
            "DIMENSIONAIS E GEOMÉTRICOS",
        ]
        result, svg, _ = self.run_script(dados)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[info] fonte reduzida", result.stderr)
        self.assertNotIn("texto fora do quadro", result.stderr)

    def test_text_within_box_on_short_labels(self):
        result, _, _ = self.run_script(ESTRUTURA)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("texto fora do quadro", result.stderr)


if __name__ == "__main__":
    unittest.main()
