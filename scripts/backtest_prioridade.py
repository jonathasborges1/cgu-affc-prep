#!/usr/bin/env python3
"""Backtest temporal do ranking usando somente itens classificados e persistidos."""
import json, math, os, re
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
def conc():
    a=BASE/'concursos'/'ativo.txt'; return BASE/'concursos'/(a.read_text(encoding='utf-8').strip() if a.exists() else 'cgu-affc-ti-ds')
def pai(c):
    c=str(c or '');
    if c=='FORA' or ' ' not in c: return None
    pre,num=c.rsplit(' ',1); return pre+' '+num.split('.')[0]
def main():
    b=[json.loads(x) for x in (conc()/'banco.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    b=[x for x in b if pai(x.get('edital')) and x.get('ano') and x.get('fonte','').startswith('oficial-')]
    anos=sorted({int(x['ano']) for x in b}); resultados=[]
    for ano in anos:
        treino=[x for x in b if int(x['ano'])<ano]; teste=[x for x in b if int(x['ano'])==ano]
        if len(treino)<20 or len(teste)<10: continue
        for bloco in ('P1','P2','P3'):
            tr=[x for x in treino if pai(x['edital']).startswith(bloco+'·')]; te=[x for x in teste if pai(x['edital']).startswith(bloco+'·')]
            if len(tr)<10 or len(te)<5: continue
            ct=Counter();
            for x in tr: ct[pai(x['edital'])]+=0.5**((ano-int(x['ano']))/4)
            total=sum(ct.values()); real=Counter(pai(x['edital']) for x in te); nr=sum(real.values()); cods=set(ct)|set(real)
            mae=sum(abs(ct.get(c,0)/total-real.get(c,0)/nr) for c in cods)/len(cods)
            top={c for c,_ in ct.most_common(5)}; recall=sum(n for c,n in real.items() if c in top)/nr
            resultados.append({'ano_teste':ano,'bloco':bloco,'treino':len(tr),'teste':len(te),'mae_share':mae,'recall_top5':recall})
    n=sum(x['teste'] for x in resultados); gate=len(resultados)>=3 and n>=100
    out={'modelo':'backtest-temporal-v1','n_itens_classificados':len(b),'folds':resultados,
         'resumo':{'folds':len(resultados),'itens_teste':n,
          'mae_share_medio':sum(x['mae_share']*x['teste'] for x in resultados)/max(1,n),
          'recall_top5_medio':sum(x['recall_top5']*x['teste'] for x in resultados)/max(1,n)},
         'gate_dados_minimos':gate,'conclusao':'avaliavel' if gate else 'dados classificados insuficientes para validar previsao'}
    dest=BASE/'docs'/'backtest-prioridade.json'; dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out['resumo'],ensure_ascii=False)); print(out['conclusao'],'->',dest)
if __name__=='__main__': main()
