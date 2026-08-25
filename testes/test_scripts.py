import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


class CitationVerificationTests(unittest.TestCase):
    def test_exact_extract_returns_source_and_line_numbers(self):
        from gerar_diagramas import verificar_citacoes

        fontes = [
            {
                "fonte": "entrevista-01.txt",
                "texto": "Primeira linha.\nEste extrato precisa ser literal.\nTerceira linha.",
            }
        ]

        resultado = verificar_citacoes(
            ["Este extrato precisa ser literal."],
            fontes=fontes,
            fuzzy=False,
        )

        item = resultado["Este extrato precisa ser literal."]
        self.assertEqual(item["status"], "verificado")
        self.assertEqual(item["fonte"], "entrevista-01.txt")
        self.assertEqual(item["linha_inicio"], 2)
        self.assertEqual(item["linha_fim"], 2)
        self.assertEqual(item["trecho_correspondente"], "Este extrato precisa ser literal.")

    def test_surface_differences_are_relocalized(self):
        from gerar_diagramas import verificar_citacoes

        fontes = [
            {
                "fonte": "entrevista-01.txt",
                "texto": "Na minha opini\u00e3o, o pior de todos. \u00c9 uma falta de respeito.",
            }
        ]
        resultado = verificar_citacoes(
            ["o PIOR  de   todos. \u00c9 uma falta"],
            fontes=fontes,
        )
        item = resultado["o PIOR  de   todos. \u00c9 uma falta"]
        self.assertEqual(item["status"], "relocalizado")
        self.assertEqual(item["trecho_correspondente"], "o pior de todos. \u00c9 uma falta")
        self.assertEqual(item["metodo"], "normalizado")

    def test_truncated_extract_is_relocalized_in_another_source(self):
        from gerar_diagramas import verificar_citacoes

        fontes = [
            {"fonte": "entrevista-02.txt", "texto": "Outra conversa."},
            {"fonte": "entrevista-01.txt", "texto": "Ent\u00e3o, o sistema eleitoral brasileiro \u00e9 o melhor que tem do mundo."},
        ]
        resultado = verificar_citacoes(
            ["o nosso sistema eleitoral brasileiro \u00e9 o melhor que tem do mundo"],
            fontes=fontes,
        )
        item = resultado["o nosso sistema eleitoral brasileiro \u00e9 o melhor que tem do mundo"]
        self.assertEqual(item["status"], "substituir")
        self.assertEqual(item["fonte"], "entrevista-01.txt")
        self.assertEqual(item["trecho_correspondente"], "Ent\u00e3o, o sistema eleitoral brasileiro \u00e9 o melhor que tem do mundo.")

    def test_paraphrased_extract_is_not_verified_as_literal(self):
        from gerar_diagramas import verificar_citacoes

        resultado = verificar_citacoes(
            ["extrato parafraseado"],
            fontes=[{"fonte": "entrevista-01.txt", "texto": "O participante disse outra coisa."}],
            fuzzy=False,
        )

        self.assertEqual(resultado["extrato parafraseado"]["status"], "nao_encontrado")


class FinalOutputWrapperTests(unittest.TestCase):
    def test_trajetoria_receives_output_path(self):
        import gerar_saida_final

        with tempfile.TemporaryDirectory() as tmpdir:
            dados = {
                "codigos_por_documento": {"doc-1": ["codigo-a", "codigo-b"]},
                "temas": [{"nome": "Tema A", "subtemas": []}],
                "estado_inicial": {"temas": [{"nome": "A", "codigos": ["C1"]}]},
                "estado_revisado": {"temas": [{"nome": "Tema A", "codigos": ["C1"]}]},
                "relacoes": [{"de": "Tema A", "para": "Tema A", "tipo": "conexão"}],
                "trajetoria": {"codigos_iniciais": 2, "temas_finais": 1},
            }

            def touch_output(*args, **kwargs):
                output_path = kwargs.get("output_path")
                if output_path is None and args:
                    output_path = args[-1]
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                Path(output_path).write_text("<svg></svg>", encoding="utf-8")
                return output_path

            def assert_trajetoria_output_path(trajetoria, itens_por_etapa=None, output_path=None):
                self.assertIsNotNone(output_path)
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                Path(output_path).write_text("<svg></svg>", encoding="utf-8")
                return output_path

            with patch.object(gerar_saida_final, "gerar_rede_codigos", side_effect=touch_output), \
                 patch.object(gerar_saida_final, "gerar_mapa_tematico", side_effect=touch_output), \
                 patch.object(gerar_saida_final, "gerar_diagrama_evolucao", side_effect=touch_output), \
                 patch.object(gerar_saida_final, "gerar_diagrama_relacoes", side_effect=touch_output), \
                 patch.object(gerar_saida_final, "gerar_mapa_final", side_effect=touch_output), \
                 patch.object(gerar_saida_final, "gerar_diagrama_trajetoria", side_effect=assert_trajetoria_output_path):
                gerar_saida_final.gerar_diagramas(dados, tmpdir)


class MarkdownVisualizationTests(unittest.TestCase):
    def test_dot_map_and_frequency_table_are_markdown_safe(self):
        from gerar_diagramas import gerar_dot_mapa_tematico, gerar_tabela_frequencia_markdown

        temas = [
            {
                "nome": "Tema interpretativo",
                "subtemas": [
                    {
                        "nome": "Subtema",
                        "categorias": [{"nome": "Categoria", "codigos": ["codigo raro"]}],
                    }
                ],
            }
        ]

        dot = gerar_dot_mapa_tematico(temas)
        tabela = gerar_tabela_frequencia_markdown({"doc-1": ["codigo raro"], "doc-2": ["codigo comum", "codigo raro"]})

        self.assertTrue(dot.startswith("```dot"))
        self.assertIn("digraph atr_mapa_tematico", dot)
        self.assertIn("codigo raro", tabela)
        self.assertIn("Nunca use como proxy automatico", tabela)


class PublicRepositoryTests(unittest.TestCase):
    def test_public_metadata_files_exist(self):
        for relpath in [
            "README.md",
            "LICENSE",
            "CITATION.cff",
            ".gitignore",
            "requirements.txt",
        ]:
            self.assertTrue((ROOT / relpath).exists(), f"Arquivo obrigatorio ausente: {relpath}")

    def test_skill_documentation_has_no_private_local_paths(self):
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        private_windows_prefix = "C:" + "\\" + "Users" + "\\"
        private_codex_segment = "." + "codex"
        private_validator_name = "quick_" + "validate.py"
        self.assertNotIn(private_windows_prefix, skill_text)
        self.assertNotIn(private_codex_segment, skill_text)
        self.assertNotIn(private_validator_name, skill_text)


if __name__ == "__main__":
    unittest.main()
