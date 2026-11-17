#!/usr/bin/env python3
"""Testes de scripts/auditar_analise.py (Python padrão).

Cada teste monta uma análise mínima e fictícia e confere que a regra
correspondente dispara. Os dados não descrevem pessoas reais.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import auditar_analise as aa  # noqa: E402

FALA_1 = "Quem cobra regra de mim tem que estar com a mão na terra também"
FALA_2 = "Levar alface para casa sem ter plantado não é roubo"
FALA_3 = "cada um passou a avisar o vizinho do lado"


def base() -> list[dict]:
    """Registro íntegro: duas fontes, três excertos, dois temas finais."""
    return [
        {"tipo": "fonte", "id": "F01", "arquivo": "p1.txt", "estatuto": "fala_primaria"},
        {"tipo": "fonte", "id": "F02", "arquivo": "p2.txt", "estatuto": "fala_primaria"},
        {"tipo": "excerto", "id": "Q001", "fonte": "F01", "texto": FALA_1, "forma": "literal",
         "localizador": "linha 4", "contexto": "linhas 3-5", "falante": "P2"},
        {"tipo": "excerto", "id": "Q002", "fonte": "F02", "texto": FALA_2, "forma": "literal",
         "localizador": "linha 7", "contexto": "linhas 6-8", "falante": "P4"},
        {"tipo": "excerto", "id": "Q003", "fonte": "F01", "texto": FALA_3, "forma": "literal",
         "localizador": "linha 9", "contexto": "linhas 8-10", "falante": "P1"},
        {"tipo": "codigo", "id": "C01", "rotulo": "autoridade exige trabalho junto", "excertos": ["Q001"]},
        {"tipo": "codigo", "id": "C02", "rotulo": "colher sem plantar desloca o pertencimento", "excertos": ["Q002"]},
        {"tipo": "codigo", "id": "C03", "rotulo": "avisar o vizinho substitui o controle", "excertos": ["Q003"]},
        {"tipo": "tema", "id": "TC1", "fase": "candidato", "nome": "Regras da horta",
         "conceito": "regra", "codigos": ["C01", "C03"]},
        {"tipo": "tema", "id": "TC2", "fase": "candidato", "nome": "Colheita",
         "conceito": "colheita", "codigos": ["C02"]},
        {"tipo": "tema", "id": "TF1", "fase": "final", "nome": "A regra vale quando quem cobra trabalha junto",
         "conceito": "legitimidade pelo trabalho comum", "codigos": ["C01", "C02"], "origem": ["TC1", "TC2"],
         "ancoras": ["Q001", "Q002"], "evidencia_decisiva": ["Q001"]},
        {"tipo": "tema", "id": "TF2", "fase": "final", "nome": "Avisar no lugar de vigiar",
         "conceito": "cuidado lateral", "codigos": ["C03"], "origem": ["TC1"], "ancoras": ["Q003"]},
        {"tipo": "hipotese", "id": "H1", "texto": "a horta seria vivida como lazer",
         "destino": "derrubada", "evidencia": "Q001 e Q002 tratam de regra e pertencimento"},
    ]


def auditar(registros: list[dict], **extras) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp)
        registro = pasta / "evidencias.jsonl"
        registro.write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in registros), encoding="utf-8"
        )
        argumentos = ["integridade", "--registro", str(registro), "--output", str(pasta / "r.json")]
        for nome, conteudo in extras.items():
            if nome == "relatorio":
                alvo = pasta / "06-relatorio-final.md"
                alvo.write_text(conteudo, encoding="utf-8")
                argumentos += ["--relatorio", str(alvo)]
            elif nome == "saida":
                destino = pasta / "saida"
                destino.mkdir()
                (destino / "03-temas.md").write_text(conteudo, encoding="utf-8")
                argumentos += ["--saida", str(destino)]
            elif nome == "verificacao":
                alvo = pasta / "verificacao.jsonl"
                alvo.write_text("".join(json.dumps(r) + "\n" for r in conteudo), encoding="utf-8")
                argumentos += ["--verificacao", str(alvo)]
            elif nome == "leitura":
                manifesto, lidos = conteudo
                (pasta / "manifesto.jsonl").write_text(
                    "".join(json.dumps(r) + "\n" for r in manifesto), encoding="utf-8"
                )
                (pasta / "leitura.jsonl").write_text(
                    "".join(json.dumps(r) + "\n" for r in lidos), encoding="utf-8"
                )
                argumentos += ["--manifesto", str(pasta / "manifesto.jsonl"), "--leitura", str(pasta / "leitura.jsonl")]
        codigo = aa.main(argumentos)
        resultado = json.loads((pasta / "r.json").read_text(encoding="utf-8"))
        resultado["_saida"] = codigo
        return resultado


def codigos(resultado: dict, chave: str) -> set[str]:
    return {item["codigo"] for item in resultado[chave]}


class RegistroTest(unittest.TestCase):
    def test_registro_integro_passa_sem_erros(self):
        resultado = auditar(base())
        self.assertEqual(resultado["erros"], [])
        self.assertEqual(resultado["_saida"], 0)
        self.assertEqual(resultado["diff_temas"]["efeito"], "estrutural")
        self.assertEqual(resultado["contagens"]["temas_finais"], 2)

    def test_codigo_orfao_e_codigo_repetido_sem_justificativa(self):
        registros = base()
        registros.append({"tipo": "excerto", "id": "Q004", "fonte": "F02", "texto": "outra fala qualquer do grupo",
                          "forma": "literal", "localizador": "linha 2", "contexto": "linhas 1-3"})
        registros.append({"tipo": "codigo", "id": "C04", "rotulo": "sem tema", "excertos": ["Q004"]})
        registros[10]["codigos"] = ["C01", "C02", "C03"]
        resultado = auditar(registros)
        self.assertIn("E05", codigos(resultado, "erros"))
        self.assertIn("E06", codigos(resultado, "erros"))
        self.assertEqual(resultado["_saida"], 1)

    def test_codigo_compartilhado_com_justificativa_e_residuo_justificado(self):
        registros = base()
        registros[10]["codigos"] = ["C01", "C02", "C03"]
        registros[7]["compartilhado"] = "o aviso lateral sustenta os dois argumentos"
        registros.append({"tipo": "codigo", "id": "C05", "rotulo": "caso isolado", "excertos": ["Q003"],
                          "estado": "residuo", "justificativa": "não altera nenhum argumento"})
        self.assertEqual(auditar(registros)["erros"], [])

    def test_parafrase_nao_sustenta_ancora_nem_evidencia_decisiva(self):
        registros = base()
        registros[2]["forma"] = "parafrase"
        self.assertIn("E07", codigos(auditar(registros), "erros"))

    def test_fonte_mediada_exige_voz_de_mediador(self):
        registros = base()
        registros[1]["estatuto"] = "nota_de_mediador"
        self.assertIn("E13", codigos(auditar(registros), "erros"))
        registros[3]["voz"] = "mediador"
        resultado = auditar(registros)
        self.assertNotIn("E13", codigos(resultado, "erros"))
        self.assertEqual(resultado["mediados"], ["Q002"])

    def test_excerto_literal_exige_localizador_e_contexto(self):
        registros = base()
        del registros[2]["contexto"]
        self.assertIn("E03", codigos(auditar(registros), "erros"))

    def test_contestacao_sem_efeito_estrutural_gera_alerta(self):
        registros = base()
        registros[10].update(codigos=["C01", "C03"], origem=["TC1"], ancoras=["Q001", "Q003"])
        registros[11].update(codigos=["C02"], origem=["TC2"], ancoras=["Q002"])
        resultado = auditar(registros)
        self.assertEqual(resultado["diff_temas"]["efeito"], "sem efeito estrutural")
        self.assertIn("A09", codigos(resultado, "alertas"))
        self.assertEqual(len(resultado["diff_temas"]["renomeados"]), 2)

    def test_dado_nao_representado_nao_pode_ja_sustentar_tema(self):
        registros = base()
        registros.append({"tipo": "nao_representado", "id": "N1", "excerto": "Q001", "tratamento": "tensão"})
        self.assertIn("E11", codigos(auditar(registros), "erros"))

    def test_tensao_pode_constar_como_nao_representada(self):
        registros = base()
        registros.append({"tipo": "excerto", "id": "Q007", "fonte": "F02", "texto": "eu obedeço porque foi ela que começou tudo",
                          "forma": "literal", "localizador": "linha 12", "contexto": "linhas 11-13"})
        registros[10]["tensoes"] = ["Q007"]
        registros.append({"tipo": "nao_representado", "id": "N1", "excerto": "Q007", "tratamento": "preservado como tensão em TF1"})
        self.assertNotIn("E11", codigos(auditar(registros), "erros"))

    def test_predominio_de_fonte_mediada_gera_alerta(self):
        registros = base()
        for indice in (0, 1):
            registros[indice]["estatuto"] = "resumo_de_segunda_mao"
        for indice in (2, 3, 4):
            registros[indice]["voz"] = "mediador"
        resultado = auditar(registros)
        self.assertEqual(resultado["erros"], [])
        self.assertIn("A17", codigos(resultado, "alertas"))

    def test_hipoteses_intactas_geram_alerta_de_ancoragem(self):
        registros = base()
        registros[12]["destino"] = "mantida"
        self.assertIn("A10", codigos(auditar(registros), "alertas"))
        self.assertIn("A10", codigos(auditar(registros[:12]), "alertas"))

    def test_tema_em_uma_so_fonte_e_ancora_curta(self):
        registros = base()
        registros[4]["texto"] = "Muita falta de juízo"
        alertas = codigos(auditar(registros), "alertas")
        self.assertIn("A01", alertas)
        self.assertIn("A13", alertas)

    def test_verificacao_exige_verified_exact(self):
        verificacao = [
            {"citation_id": "Q001", "status": "verified_exact"},
            {"citation_id": "Q002", "status": "substituir"},
        ]
        resultado = auditar(base(), verificacao=verificacao)
        erros = [e for e in resultado["erros"] if e["codigo"] == "E04"]
        self.assertEqual({e["ref"] for e in erros}, {"Q002", "Q003"})


class RelatorioTest(unittest.TestCase):
    def test_citacao_registrada_passa_e_citacao_fora_do_registro_falha(self):
        texto = (
            "# Relatório\n\nA autoridade só convence quando partilha o trabalho.\n\n"
            f"> “{FALA_1}” (F01, linha 4)\n\n"
            "O excerto condiciona a regra a quem a cobra, e não ao conteúdo da regra em si mesma.\n\n"
            "Um participante disse “a horta nos devolveu o sentido de comunidade perdido” ao fim.\n"
        )
        resultado = auditar(base(), relatorio=texto)
        erros = [e for e in resultado["erros"] if e["codigo"] == "E08"]
        self.assertEqual(len(erros), 1)
        self.assertEqual(resultado["relatorio"]["excertos_publicados"], ["Q001"])

    def test_citacao_com_elipse_e_citacao_externa_registrada(self):
        registros = base()
        registros.append({"tipo": "citacao_externa", "id": "L1", "referencia": "fonte fornecida pelo usuário",
                          "texto": "a subjetividade do pesquisador funciona como recurso analítico"})
        texto = (
            "Texto.\n\n“Quem cobra regra de mim [...] com a mão na terra também” mostra a condição.\n\n"
            "A literatura fala em “a subjetividade do pesquisador funciona como recurso analítico”.\n"
        )
        self.assertEqual(auditar(registros, relatorio=texto)["erros"], [])

    def test_parafrase_entre_aspas_e_citacoes_seguidas(self):
        registros = base()
        registros.append({"tipo": "excerto", "id": "Q009", "fonte": "F02", "forma": "parafrase",
                          "texto": "ela diz que só volta quando pararem de fiscalizar"})
        texto = (
            "Abertura.\n\n"
            f"> “{FALA_1}”\n\n> “{FALA_2}”\n\n"
            "Disse que “ela diz que só volta quando pararem de fiscalizar” o canteiro.\n"
        )
        resultado = auditar(registros, relatorio=texto)
        self.assertIn("E09", codigos(resultado, "erros"))
        self.assertIn("A08", codigos(resultado, "alertas"))

    def test_marcadores_de_template_e_contagens_divergentes(self):
        saida = (
            "# F3\n\n[Explicar como os temas constroem a resposta analítica.]\n\n"
            "Estatuto: independente | informada | ausente\n\n"
            "| TF1 |  |  |\n\n*Continuar para todos os códigos.*\n\n"
            "A fase consolidou 30 códigos e 5 temas finais. Ver [o registro](evidencias.jsonl).\n"
        )
        resultado = auditar(base(), saida=saida)
        erros = [e for e in resultado["erros"] if e["codigo"] == "E10"]
        self.assertEqual(len(erros), 4)
        alertas = [a for a in resultado["alertas"] if a["codigo"] == "A07"]
        self.assertEqual(len(alertas), 2)

    def test_leitura_parcial_e_concentracao_de_evidencia(self):
        manifesto = [{"source": "p1.txt", "lines": 10}, {"source": "p2.txt", "lines": 90}]
        lidos = [{"fonte": "p1.txt", "inicio": 1, "fim": 10, "memo": "M1"},
                 {"fonte": "p2.txt", "inicio": 1, "fim": 30, "memo": ""}]
        resultado = auditar(base(), leitura=(manifesto, lidos))
        self.assertEqual(resultado["cobertura"]["estado"], "parcial")
        self.assertEqual(resultado["cobertura"]["lidas"], 40)
        self.assertEqual(sum(resultado["distribuicao"]["excertos_por_terco_do_corpus"]), 3)
        alertas = codigos(resultado, "alertas")
        self.assertIn("A15", alertas)
        self.assertIn("A14", alertas)
        lidos[1].update(fim=90, memo="M2")
        self.assertEqual(auditar(base(), leitura=(manifesto, lidos))["cobertura"]["estado"], "integral")


class ComandosTest(unittest.TestCase):
    def rodar(self, argumentos: list[str], arquivos: dict[str, str]) -> tuple[int, dict | str]:
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            for nome, conteudo in arquivos.items():
                alvo = pasta / nome
                alvo.parent.mkdir(parents=True, exist_ok=True)
                alvo.write_text(conteudo, encoding="utf-8")
            saida = pasta / "resultado.out"
            codigo = aa.main([a.replace("@", str(pasta) + "/") for a in argumentos] + ["--output", str(saida)])
            texto = saida.read_text(encoding="utf-8")
            try:
                return codigo, json.loads(texto)
            except json.JSONDecodeError:
                return codigo, texto

    def test_privacidade_lista_candidatos_sem_decidir(self):
        codigo, resultado = self.rodar(
            ["privacidade", "--saida", "@saida", "--nomes", "@nomes.txt"],
            {
                "saida/00.md": "Exclusões: recusas de Fulano B. e contato em pessoa@exemplo.org.\n"
                               "A fala de P03 foi mantida. Segundo beltrana, não.\n",
                "nomes.txt": "Beltrana\n",
            },
        )
        self.assertEqual(codigo, 1)
        classes = {(c["classe"], c["texto"]) for c in resultado["candidatos"]}
        self.assertIn(("nome com sobrenome abreviado", "Fulano B."), classes)
        self.assertIn(("e-mail", "pessoa@exemplo.org"), classes)
        self.assertIn(("nome informado pelo usuário", "Beltrana"), classes)
        self.assertIn("perguntar", resultado["orientacao"])

    def test_sobrealegacao_ignora_o_que_esta_dentro_de_citacao(self):
        codigo, resultado = self.rodar(
            ["sobrealegacao", "--relatorio", "@r.md"],
            {"r.md": "Os temas emergiram e a confiança opera como variável independente.\n"
                     "P1 disse “todo mundo sempre soube disso” em tom de queixa.\n"
                     "Políticas que proíbem tendem a intensificar o medo.\n"},
        )
        self.assertEqual(codigo, 1)
        termos = {i["termo"].lower() for i in resultado["itens"]}
        self.assertEqual(termos, {"emergiram", "variável independente", "tendem a"})
        codigo, resultado = self.rodar(
            ["sobrealegacao", "--relatorio", "@r.md"],
            {"r.md": "O texto é curto. Não busquei saturação nem consenso. Isso prova que o grupo mudou.\n"},
        )
        negados = {i["termo"].lower(): i["negado_na_frase"] for i in resultado["itens"]}
        self.assertEqual(negados, {"saturação": True, "prova que": False})

    def test_homogeneizacao_compara_casos_e_desconta_o_molde(self):
        comum = "A proteção só convence quando não parece muleta nem imposição para quem recebe a ajuda do Estado. "
        arquivos = {
            "a/05.md": "# Relatório\n\n## Ajuda só convence quando parece justa\n\n" + comum * 3 + "Em A havia rio e balsa.\n",
            "b/05.md": "# Relatório\n\n## Ajuda só convence quando parece justa aqui\n\n" + comum * 3 + "Em B havia frio e fábrica.\n",
            "c/05.md": "# Relatório\n\n## O porto organiza a memória do trabalho\n\nNada em comum com os outros dois casos analisados.\n",
            "molde/t.md": "# Relatório\n",
        }
        codigo, resultado = self.rodar(
            ["homogeneizacao", "--relatorios", "@a/05.md", "@b/05.md", "@c/05.md", "--templates", "@molde"], arquivos
        )
        self.assertEqual(codigo, 1)
        primeiro = resultado["pares"][0]
        self.assertTrue(primeiro["alerta"])
        self.assertEqual({Path(p).parent.name for p in primeiro["par"]}, {"a", "b"})
        self.assertTrue(primeiro["titulos_parecidos"])
        self.assertFalse(any("relatório ~ relatório" in t for p in resultado["pares"] for t in p["titulos_parecidos"]))
        self.assertFalse(resultado["pares"][-1]["alerta"])

    def test_aptidao_apto_parcial_e_inapto(self):
        certas = {
            "citacoes": [
                {"texto": "cada um passou a avisar o vizinho do lado", "linha": 9},
                {"texto": "sei quem aparece no mutirão e quem só aparece na colheita", "linha": 3},
                {"texto": "o caderno sumiu na segunda semana", "linha": 8},
            ],
            "classificacao": {"A": "topico", "B": "tema", "C": "topico", "D": "tema", "E": "topico", "F": "tema"},
            "nao_literais": ["X2", "X4", "X5"],
        }
        codigo, resultado = self.rodar(["aptidao", "--respostas", "@r.json"], {"r.json": json.dumps(certas)})
        self.assertEqual((codigo, resultado["resultado"]), (0, "apto"))
        parcial = dict(certas, nao_literais=["X2", "X5"])
        codigo, resultado = self.rodar(["aptidao", "--respostas", "@r.json"], {"r.json": json.dumps(parcial)})
        self.assertEqual((codigo, resultado["resultado"]), (1, "parcial"))
        inapto = dict(certas)
        inapto["citacoes"] = certas["citacoes"][:2] + [{"texto": "a horta devolveu o sentido de comunidade", "linha": 1}]
        codigo, resultado = self.rodar(["aptidao", "--respostas", "@r.json"], {"r.json": json.dumps(inapto)})
        self.assertEqual(resultado["resultado"], "inapto")

    def test_citacoes_e_tabelas_saem_do_registro(self):
        registro = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in base())
        codigo, texto = self.rodar(["citacoes", "--registro", "@e.jsonl"], {"e.jsonl": registro})
        linhas = [json.loads(l) for l in str(texto).splitlines()] if isinstance(texto, str) else [texto]
        self.assertEqual(codigo, 0)
        self.assertEqual(linhas[0]["source"], "p1.txt")
        self.assertEqual(linhas[0]["declared_locator"], "linha 4")
        codigo, tabela = self.rodar(["tabelas", "--registro", "@e.jsonl"], {"e.jsonl": registro})
        self.assertEqual(codigo, 0)
        self.assertIn("| C01 | autoridade exige trabalho junto | Q001 | literal | F01 | linha 4 |", tabela)
        self.assertIn("efeito da contestação: estrutural", tabela)


if __name__ == "__main__":
    unittest.main()
