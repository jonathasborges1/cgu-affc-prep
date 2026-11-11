import datetime
import importlib.util
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    "servidor", Path(__file__).parents[1] / "app" / "servidor.py"
)
servidor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(servidor)


class RevisaoAdaptativaTest(unittest.TestCase):
    def test_erro_ou_branco_volta_no_dia_seguinte(self):
        self.assertEqual(servidor.intervalo_revisao(0, 3), 1)
        self.assertEqual(servidor.intervalo_revisao(None, None), 1)

    def test_confianca_controla_o_intervalo(self):
        self.assertEqual(servidor.intervalo_revisao(1, 1), 2)
        self.assertEqual(servidor.intervalo_revisao(1, 2), 7)
        self.assertEqual(servidor.intervalo_revisao(1, 3), 15)

    def test_dominio_repetido_estende_para_trinta_dias(self):
        self.assertEqual(servidor.intervalo_revisao(1, 3, 2), 30)

    def test_soma_dias_em_iso(self):
        self.assertEqual(servidor._somar_dias("2026-11-08T10:00:00", 7), "2026-11-15")


if __name__ == "__main__":
    unittest.main()
