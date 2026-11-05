#!/usr/bin/env python3
"""Amostra positivos e descartados e mede precisao/recall sem fabricar rotulos.

Uso:
  python scripts/calibrar_triagem.py amostrar --bloco P2 --n 120 --saida fila/calibracao-p2.jsonl
  # preencher codigo_real com um codigo do edital ou OUTRO, por revisao independente
  python scripts/calibrar_triagem.py avaliar fila/calibracao-p2.jsonl --saida docs/calibracao-p2.json
"""
import argparse, glob, json, os, random, sys
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
def conc():
    a=BASE/'concursos'/'ativo.txt'; return BASE/'concursos'/(a.read_text(encoding='utf-8').strip() if a.exists() else 'cgu-affc-ti-ds')
def lerj(p):
    try: return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
    except Exception: return []
def pai(c):
    c=str(c or '');
    if ' ' not in c: return c
    pre,num=c.rsplit(' ',1); return pre+' '+num.split('.')[0]
def chave(pid,item): return str(pid)+'#'+str(item)

def amostrar(a):
    d=conc(); predito={}; itens={}
    for f in sorted((d/'escopo').glob('*.jsonl')):
        if f.name.startswith('tema-'): continue
        pid=f.stem
        for x in lerj(f):
            k=chave(x.get('prova_id') or pid,x.get('item')); itens[k]=x
            cod=((x.get('compat') or {}).get('edital_prov') or '')
            if cod.startswith(a.bloco+'·'): predito[k]=pai(cod)
    # Itens descartados das mesmas provas: necessarios para estimar falsos negativos/recall.
    provas={k.split('#',1)[0] for k in predito}
    for pid in provas:
        for x in lerj(BASE/'extraidos'/(pid+'.jsonl')): itens.setdefault(chave(pid,x.get('item')),dict(x,prova_id=pid))
    pos=[k for k in predito]; neg=[k for k in itens if k.split('#',1)[0] in provas and k not in predito]
    rnd=random.Random(a.seed); npos=min(len(pos),a.n//2); nneg=min(len(neg),a.n-npos)
    sp=rnd.sample(pos,npos) if npos else []; sn=rnd.sample(neg,nneg) if nneg else []
    out=[]
    for estrato,ks,N in [('recuperado',sp,len(pos)),('descartado',sn,len(neg))]:
        for k in ks:
            x=itens[k]; out.append({'id':k,'bloco':a.bloco,'estrato':estrato,'peso_amostral':N/max(1,len(ks)),
              'codigo_predito':predito.get(k,'NAO_RECUPERADO'),'codigo_real':None,
              'prova_id':x.get('prova_id') or k.split('#',1)[0],'item':x.get('item'),
              'enunciado':x.get('enunciado'),'gabarito':x.get('gabarito')})
    Path(a.saida).parent.mkdir(parents=True,exist_ok=True)
    Path(a.saida).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out),encoding='utf-8')
    print('amostra',len(out),'recuperados',len(sp),'de',len(pos),'descartados',len(sn),'de',len(neg),'->',a.saida)

def avaliar(a):
    L=lerj(a.arquivo); pend=[x['id'] for x in L if not x.get('codigo_real')]
    if pend: sys.exit('faltam rotulos codigo_real: %d (ex.: %s)'%(len(pend),pend[0]))
    cods=sorted({pai(x['codigo_predito']) for x in L if x['codigo_predito']!='NAO_RECUPERADO'}|{pai(x['codigo_real']) for x in L if x['codigo_real']!='OUTRO'})
    out={'arquivo':a.arquivo,'n':len(L),'metodo':'amostra estratificada ponderada','topicos':{}}
    for c in cods:
        pred=[x for x in L if pai(x['codigo_predito'])==c]; tp=sum(x['peso_amostral'] for x in pred if pai(x['codigo_real'])==c); pp=sum(x['peso_amostral'] for x in pred)
        reais=[x for x in L if pai(x['codigo_real'])==c]; rp=sum(x['peso_amostral'] for x in reais)
        out['topicos'][c]={'n_rotulado':len(pred),'tp_ponderado':tp,'preditos_ponderado':pp,'reais_ponderado':rp,
                          'precisao':tp/pp if pp else None,'recall':tp/rp if rp else None}
    Path(a.saida).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8'); print('gravado',a.saida)

def main():
    ap=argparse.ArgumentParser(); s=ap.add_subparsers(dest='cmd',required=True)
    p=s.add_parser('amostrar'); p.add_argument('--bloco',choices=['P1','P2','P3'],required=True); p.add_argument('--n',type=int,default=120); p.add_argument('--seed',type=int,default=20261105); p.add_argument('--saida',required=True); p.set_defaults(f=amostrar)
    p=s.add_parser('avaliar'); p.add_argument('arquivo'); p.add_argument('--saida',required=True); p.set_defaults(f=avaliar)
    a=ap.parse_args(); a.f(a)
if __name__=='__main__': main()
