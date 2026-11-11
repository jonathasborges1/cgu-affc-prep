#!/usr/bin/env python3
"""Lote-AMOSTRA de um assunto: pega N itens 'fortes' (aleatorio com semente, 1 por prova antes de repetir prova) para classificar e medir a precisao da triagem.
  amostra_tema.py "P1·ESTADO 9" --id tema-p1-estado-9-a [--n 15] [--seed 7]
Cria o lote como 'extraida' (nada de aula/caderno)."""
import sys,json,random,argparse,subprocess,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); sys.path.insert(0,str(Path(__file__).parent.parent))
import descobrir as D
B=D.B
ap=argparse.ArgumentParser(); ap.add_argument('codigo'); ap.add_argument('--id',required=True); ap.add_argument('--n',type=int,default=15); ap.add_argument('--seed',type=int,default=7)
a=ap.parse_args()
cands=[]
for p in B.provas():
    if p['estado']=='persistida' or p['prova_id'].startswith('tema-'): continue
    for i in B.lerj(B.PC('escopo',p['prova_id']+'.jsonl')):
        if B.ematch(i['compat'].get('edital_prov'),a.codigo) and i['compat']['nivel']=='forte': cands.append((p['prova_id'],i))
rnd=random.Random(a.seed); por=collections.defaultdict(list)
for pid,i in cands: por[pid].append(i)
for v in por.values(): rnd.shuffle(v)
provas=list(por); rnd.shuffle(provas); esc=[]; r=0
while len(esc)<a.n and any(len(por[p])>r for p in provas):
    for p in provas:
        if len(por[p])>r and len(esc)<a.n: esc.append((p,por[p][r]))
    r+=1
itens=[]
for n,(pid,i) in enumerate(esc,1):
    j={k:v for k,v in i.items() if k!='compat'}; j.update({'item_orig':i['item'],'prova_origem':pid,'item':str(n),'compat':i['compat']}); itens.append(j)
B.escj(B.P('extraidos',a.id+'.jsonl'),[{k:v for k,v in j.items() if k!='compat'} for j in itens]); B.escj(B.PC('escopo',a.id+'.jsonl'),itens)
pr={'prova_id':a.id,'ref':'Lote-amostra %s (%d itens fortes de %d provas)'%(a.codigo,len(itens),len({j['prova_origem'] for j in itens})),'url':'lote','url_gab':'lote','ano':2024,'orgao':'varias','cargo':a.codigo,'peso':1.0,'hash':None,'n_itens':len(itens),'n_gab':len(itens),'verificacao':None,'historico':[]}
for e in ('descoberta','baixada','extraida'): B.hist(pr,e,'amostra por tema (precisao da triagem)')
B.prova_put(pr); print('%s: %d itens (de %d candidatos fortes, %d provas)'%(a.id,len(itens),len(cands),len(por)))
