#!/usr/bin/env python3
"""Estimador corrigido de P3: lidas (exatas) + escondidas estimadas por faixa de score (amostra estratificada) .
Saida: docs/estimativa-p3-ml.json  (participacao por assunto com IC90 por bootstrap, recall, faixas A/B/C, estabilidade)
Uso: python scripts/estimador_p3_ml.py"""
import json,glob,os,random,collections
import numpy as np
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd=lambda p:[json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]
def rotulos(pref,mapa):
    L={}
    for f in glob.glob(B+'/tmp/p3fila/'+pref+'*.jsonl'):
        for x in rd(f):L[x['id']]=x['codigo']
    return {m['id']:(m,L[m['id']]) for m in mapa if m['id'] in L}
def main(nboot=1000,seed=5):
    R=json.load(open(B+'/docs/recall-triagem-p3.json'));prec=json.load(open(B+'/docs/precisao-triagem-p3.json'))
    fila=json.load(open(B+'/docs/ml-fila-p3.json'));npool=fila['n']
    topo=rotulos('lab-',json.load(open(B+'/tmp/p3fila/mapa.json')))          # 150 do topo: lidas exatas
    sort=rotulos('sorteio-lab-',json.load(open(B+'/tmp/p3fila/sorteio-mapa.json')))   # amostra estratificada
    ntopo=len(topo);ptopo=[c for m,c in topo.values() if c!='OUTRO']
    bandas={}
    for m,c in sort.values():
        b=bandas.setdefault(m['banda'],{'N':m['tam_banda'],'y':[]});b['y'].append(c)
    ass=sorted({c for m,c in sort.values() if c!='OUTRO'}|set(ptopo)|set(prec.keys()))
    # P3 ja lidas por assunto (estimativa anterior: base)
    base=collections.Counter({a:prec[a]['real'] for a in prec if a.startswith('P3')})  # P3 estimadas dentro do pool forte (lidas+triagem)
    rng=random.Random(seed);part=collections.defaultdict(list);rec=[];ocult=[]
    for _ in range(nboot):
        tot=collections.Counter(base)
        for c in ptopo:tot[c]+=1
        h=0
        for b,d in bandas.items():
            y=[rng.choice(d['y']) for _ in d['y']]
            for c in y:
                if c!='OUTRO':tot[c]+=d['N']/len(y);h+=d['N']/len(y)
        T=sum(tot.values())
        for a in ass:part[a].append(tot[a]/T)
        conhecidas=sum(base.values())+len(ptopo);rec.append(conhecidas/(conhecidas+h))
        ocult.append(h)
    out={'n_topo':ntopo,'p3_topo':len(ptopo),'bandas':{b:{'N':d['N'],'n':len(d['y']),'p3':sum(c!='OUTRO' for c in d['y']),'rend':round(sum(c!='OUTRO' for c in d['y'])/len(d['y']),3)} for b,d in bandas.items()},
         'recall':[round(float(np.percentile(rec,q)),3) for q in (5,50,95)],'ocultas':[round(float(np.percentile(ocult,q))) for q in (5,50,95)],
         'part':{a:[round(float(np.percentile(part[a],q)),4) for q in (5,50,95)] for a in ass}}
    json.dump(out,open(B+'/docs/estimativa-p3-ml.json','w'),ensure_ascii=False,indent=1)
    return out
if __name__=='__main__':
    o=main();print(json.dumps({k:v for k,v in o.items() if k!='part'},ensure_ascii=False))
    for a,v in sorted(o['part'].items(),key=lambda t:-t[1][1]):print('%-12s %.3f  [%.3f-%.3f]'%(a,v[1],v[0],v[2]))
