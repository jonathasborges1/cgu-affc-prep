#!/usr/bin/env python3
"""Minera provas-ESPELHO de P1/P2 (controle e administração/geral), que a ordenação por TI deixou para trás.
Uso: espelho.py [--grupo controle|adm|ambos] [--max-provas N] [--tempo-total S] [--pausa 3]
Reordena candidatas (não visitadas do grupo primeiro, mantendo a prioridade original dentro do grupo) e varre em rodadas."""
import os,sys,time,re,argparse,types
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); sys.path.insert(0,os.path.dirname(HERE))
import banco as B, descobrir as D, suficiencia as S
CTRL=re.compile(r'audit|controle|controlador|CGU|CGE|TCU|TCE|fiscaliza|tribut|fiscal',re.I)
ADMV=re.compile(r'administra|gest[aã]o|analista (t[eé]cnico|administrativ)|servidor|assistente',re.I)
ap=argparse.ArgumentParser(); ap.add_argument('--grupo',default='controle'); ap.add_argument('--max-provas',type=int,default=60); ap.add_argument('--tempo-total',type=int,default=540); ap.add_argument('--pausa',type=float,default=3.0)
a=ap.parse_args(); orig=B.baixa; B.baixa=lambda url,dest,pausa: orig(url,dest,max(pausa,a.pausa))
cand=B.lerj(B.PC('descoberta','candidatas.jsonl')); vis={v['prova_id'] for v in B.lerj(B.PC('descoberta','varredura.jsonl'))}
def g(c):
    t=c.get('cargo','')+' '+c.get('orgao','')
    return 0 if CTRL.search(t) else 1 if ADMV.search(t) else 2
alvo={'controle':{0},'adm':{1},'ambos':{0,1}}[a.grupo]
cand.sort(key=lambda c:(0 if (c['prova_id'] not in vis and g(c) in alvo) else 1, g(c) if a.grupo=='ambos' else 0, -c['prior']))
B.escj(B.PC('descoberta','candidatas.jsonl'),cand)
t0=time.time(); feitas=0
def p1():
    r=S.calcular(1); return r['n_provas'],r['n_forte']
n0=p1(); print('início: %d provas, %d fortes'%n0,flush=True)
while feitas<a.max_provas and time.time()-t0<a.tempo_total-40:
    ns=types.SimpleNamespace(max_provas=5,tempo=min(150,int(a.tempo_total-(time.time()-t0))),forte=10.0,fraco=8.0,ganho_min=-1,alvo_total=10**9)
    antes=p1()[0]
    try: D.varrer(ns)
    except SystemExit as x: print('PARADA (erro/bloqueio):',x); break
    n=p1(); novas=n[0]-antes; feitas+=max(novas,0); print('rodada: +%d provas (total %d, fortes %d)'%(novas,n[0],n[1]),flush=True)
    if novas<=0: print('PARADA: sem provas novas'); break
print('fim: %d provas novas nesta chamada'%feitas)
