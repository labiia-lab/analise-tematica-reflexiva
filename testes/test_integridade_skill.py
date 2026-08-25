import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class IntegridadeSkillTest(unittest.TestCase):
    def test_package_is_universal_and_self_contained(self):
        forbidden = [
            "agents",
            "caminho.md",
            "exemplos",
            "PARECER-CRITICO-SKILL.md",
            "Review IA.txt",
            "Teste-1",
        ]
        self.assertFalse([name for name in forbidden if (ROOT / name).exists()])
        self.assertTrue((ROOT / "referencias" / "ia-em-at.md").is_file())
        self.assertTrue((ROOT / "scripts" / "verificar_citacoes.py").is_file())

        markdown = "\n".join(
            path.read_text(encoding="utf-8")
            for path in ROOT.rglob("*.md")
        )
        for token in [
            "C:\\",
            "agents/openai.yaml",
            "Original/",
            "conhecimento-atr/",
            "biblioteca local",
            "capítulo local",
        ]:
            self.assertNotIn(token, markdown)

    def test_public_contract_is_explicit(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for token in [
            "independente",
            "informada",
            "ausente",
            "verified_exact",
            "PASS",
            "FAIL",
            "N/A",
            "meta editorial não bloqueante",
            "sem validação humana",
            "referencias/ia-em-at.md",
            "scripts/verificar_citacoes.py",
        ]:
            self.assertIn(token, skill)

        frontmatter = skill.split("---", 2)[1]
        keys = re.findall(r"^([a-zA-Z0-9_-]+):", frontmatter, flags=re.MULTILINE)
        self.assertEqual(keys, ["name", "description"])

    def test_existing_behavioral_suite_count_is_unchanged(self):
        scenarios = list((ROOT / "testes").glob("cenario-*.md"))
        templates = [
            path
            for path in (ROOT / "templates").rglob("*.md")
            if path.is_file()
        ]
        self.assertEqual(len(scenarios), 21)
        self.assertEqual(len(templates), 7)

    def test_final_review_corrections_are_operationalized(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        f1 = (
            ROOT
            / "templates"
            / "fase-1-familiarizacao"
            / "notas-de-familiarizacao.md"
        ).read_text(encoding="utf-8")
        f3 = (
            ROOT / "templates" / "fase-3-temas" / "temas-candidatos.md"
        ).read_text(encoding="utf-8")
        f4 = (
            ROOT / "templates" / "fase-4-revisao" / "revisao-temas.md"
        ).read_text(encoding="utf-8")
        f6 = (
            ROOT / "templates" / "fase-6-relatorio" / "relatorio-final.md"
        ).read_text(encoding="utf-8")
        quality = (ROOT / "referencias" / "qualidade-analitica.md").read_text(
            encoding="utf-8"
        )
        provenance = (
            ROOT / "referencias" / "fundamentacao-e-proveniencia.md"
        ).read_text(encoding="utf-8")

        for token in [
            "<PASTA_DA_SKILL>",
            "manifesto-corpus.jsonl",
            "source_unreadable",
            "autoavaliações",
        ]:
            self.assertIn(token, skill)
        self.assertIn("evidência de processamento", f1)
        self.assertIn("manifesto-corpus.jsonl", f1)
        self.assertIn("condição de enfraquecimento ou derrota", f3)
        self.assertIn("condições de enfraquecimento/derrota testadas", f4)
        self.assertIn("citacoes.jsonl", f6)
        self.assertIn("verificacao-citacoes.jsonl", f6)
        self.assertIn("Avaliador/independência", f6)
        self.assertIn("não prova leitura", quality)
        self.assertIn("https://ceur-ws.org/Vol-4114/7_paper.pdf", provenance)


if __name__ == "__main__":
    unittest.main()
