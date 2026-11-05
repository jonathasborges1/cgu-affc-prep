import sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import prioridade as P
import suficiencia as S

class PrioridadeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resultado=P.priorizar(1)

    def linha(self,codigo):
        return next(x for x in self.resultado['linhas'] if x['codigo']==codigo)

    def test_p1_usa_participacao_calibrada(self):
        l=self.linha('P1·ADM 4')
        self.assertEqual(l['fonte_estimativa'],'calibracao_manual')
        self.assertAlmostEqual(l['share'],0.3037,4)

    def test_erro_lexical_nao_domina_p1(self):
        self.assertLess(self.linha('P1·ESTADO 9')['ordem'], 20)
        self.assertLess(self.linha('P1·ADM 4')['ordem'],self.linha('P1·ESTADO 9')['ordem'])

    def test_sem_rotulo_nao_recebe_pronto(self):
        l=self.linha('P2·DIR 3')
        self.assertFalse(l['calibrado'])
        self.assertEqual(l['acao'],'Calibrar triagem')

    def test_censo_pequeno_conta_como_calibrado(self):
        l=self.linha('P1·ETICA 1')
        self.assertTrue(l['calibrado'])
        self.assertTrue(l['calibracao']['censo_completo'])

    def test_p1_tem_ordem_conservadora_por_faixas(self):
        self.assertTrue(self.resultado['calibracao']['P1']['ordem_por_faixas_confiavel'])
        self.assertEqual(self.resultado['calibracao']['P1']['calibrados'],24)
        self.assertEqual(self.resultado['calibracao']['P1']['ordem_exata_confiavel'],3)

    def test_p3_vale_dois_pontos(self):
        base={'prova':'P1','codigo':'x','itens_esperados':1}
        p1=P._score(base,{},{}); base['prova']='P3'; p3=P._score(base,{}, {})
        self.assertGreater(p3['ganho_bruto'],p1['ganho_bruto'])

    def test_prova_antiga_pesa_menos(self):
        var={'nova':{'prior':8,'ano':2026},'velha':{'prior':8,'ano':2016}}
        self.assertGreater(S.peso_prova('nova',var,{}),S.peso_prova('velha',var,{}))

if __name__=='__main__': unittest.main()
