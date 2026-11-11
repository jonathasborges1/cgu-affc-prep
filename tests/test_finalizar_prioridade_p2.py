import importlib.util
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('fp2',BASE/'scripts'/'finalizar_prioridade_p2.py')
fp2=importlib.util.module_from_spec(spec);spec.loader.exec_module(fp2)

class FinalizacaoP2Test(unittest.TestCase):
    def test_primeira_leitura_cobre_amostra(self):
        itens=fp2.rows(fp2.AMOSTRA)
        primeira=fp2.norm_primeira(itens)
        self.assertEqual({x['id'] for x in itens},set(primeira))
        self.assertTrue(all(primeira.values()))

    def test_diagnostico_expoe_seis_gates(self):
        d=fp2.diagnostico()
        self.assertEqual(6,len(d['gates']))
        self.assertEqual(all(d['gates'].values()),d['objetivo_atingido'])

if __name__=='__main__':unittest.main()
