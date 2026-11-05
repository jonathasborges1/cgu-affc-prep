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
def _ano(pid):
    m=re.search(r'(20\d{2})',pid or ''); return int(m.group(1)) if m else None
def backtest_rotulos_p1(d):
    """Holdout temporal dos 650 rotulos independentes de P1."""
    mapa={x['id']:x for x in [json.loads(s) for s in (d/'amostras'/'p1-verif-1-mapa.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]}
    rot={}
    for f in sorted((d/'classificacoes').glob('p1-verif-1-*.jsonl')):
        for x in [json.loads(s) for s in f.read_text(encoding='utf-8').splitlines() if s.strip()]: rot[x['id']]=x
    L=[]
    for k,m in mapa.items():
        r=rot.get(k); ano=_ano(m.get('prova_id'))
        if not r or not ano: continue
        real=pai(r.get('codigo')) if r.get('codigo')!='OUTRO' else None
        L.append({'ano':ano,'pred':pai(m.get('triagem')),'real':real})
    folds=[]
    for ano in sorted({x['ano'] for x in L}):
        tr=[x for x in L if x['ano']<ano]; te=[x for x in L if x['ano']==ano and x['real']]
        if len(tr)<80 or len(te)<15: continue
        pred=Counter(x['pred'] for x in tr); tp=Counter(x['pred'] for x in tr if x['real']==x['pred'])
        score={c:pred[c]*(tp[c]+1)/(pred[c]+2) for c in pred}; total=sum(score.values()); real=Counter(x['real'] for x in te); nr=sum(real.values()); cods=set(score)|set(real)
        mae=sum(abs(score.get(c,0)/max(1,total)-real.get(c,0)/nr) for c in cods)/len(cods)
        top={c for c,_ in sorted(score.items(),key=lambda z:-z[1])[:5]}; recall=sum(n for c,n in real.items() if c in top)/nr
        folds.append({'ano_teste':ano,'treino':len(tr),'teste':len(te),'mae_share':mae,'recall_top5':recall})
    n=sum(x['teste'] for x in folds)
    return {'rotulos':len(L),'folds':folds,'itens_teste':n,
            'mae_share_medio':sum(x['mae_share']*x['teste'] for x in folds)/max(1,n),
            'recall_top5_medio':sum(x['recall_top5']*x['teste'] for x in folds)/max(1,n),
            'gate_dados_minimos':len(folds)>=3 and n>=100}
def main():
    d=conc(); b=[json.loads(x) for x in (d/'banco.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
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
    p1=backtest_rotulos_p1(d)
    out={'modelo':'backtest-temporal-v2','n_itens_classificados':len(b),'folds_banco':resultados,'p1_rotulos':p1,
         'resumo':{'folds':len(resultados),'itens_teste':n,
          'mae_share_medio':sum(x['mae_share']*x['teste'] for x in resultados)/max(1,n),
          'recall_top5_medio':sum(x['recall_top5']*x['teste'] for x in resultados)/max(1,n)},
         'gate_dados_minimos':gate or p1['gate_dados_minimos'],
         'conclusao':('P1 avaliavel; P2/P3 ainda sem rotulos temporais suficientes' if p1['gate_dados_minimos'] else ('avaliavel' if gate else 'dados classificados insuficientes para validar previsao'))}
    dest=BASE/'docs'/'backtest-prioridade.json'; dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'banco':out['resumo'],'p1_rotulos':p1},ensure_ascii=False)); print(out['conclusao'],'->',dest)
if __name__=='__main__': main()
