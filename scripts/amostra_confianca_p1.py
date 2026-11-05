#!/usr/bin/env python3
"""Gera a amostra minima que falta para fechar a confianca de P1."""
import json, random
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
D=BASE/'concursos'/'cgu-affc-ti-ds'
def lerj(p):
    try:return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
    except Exception:return []
def key(pid,item):return str(pid)+'#'+str(item)
def main():
    mapa=lerj(D/'amostras'/'p1-verif-1-mapa.jsonl'); usados={key(x['prova_id'],x['item']) for x in mapa}
    itens={}; pred={}
    for f in sorted((D/'escopo').glob('*.jsonl')):
        if f.name.startswith('tema-'):continue
        for x in lerj(f):
            pid=x.get('prova_id') or f.stem;k=key(pid,x.get('item'));itens[k]=x
            c=((x.get('compat') or {}).get('edital_prov') or '')
            if c.startswith('P1·') and (x.get('compat') or {}).get('nivel')=='forte': pred[k]=c.rsplit('.',1)[0] if c.rsplit('.',1)[-1].isdigit() else c
    metas={'P1·SOC 4':3,'P1·ADM 5':3,'P1·ETICA 1':10,'P1·SOC 1':3}; rnd=random.Random(20261105); sel=[]
    for cod,n in metas.items():
        pool=[k for k,v in pred.items() if v.startswith(cod) and k not in usados]; rnd.shuffle(pool); sel += [('recuperado',k,cod) for k in pool[:n]]
    # Descartados das mesmas provas em que houve triagem de P1; amostra aleatoria para recall.
    provas={k.split('#',1)[0] for k in pred}; neg=[]
    for pid in provas:
        for x in lerj(BASE/'extraidos'/(pid+'.jsonl')):
            k=key(pid,x.get('item'))
            if k not in pred and k not in usados: itens.setdefault(k,dict(x,prova_id=pid)); neg.append(k)
    rnd.shuffle(neg); sel += [('descartado',k,'NAO_RECUPERADO') for k in neg[:30]]
    out=[]
    for i,(estrato,k,cod) in enumerate(sel,1):
        x=itens[k];out.append({'id':'p1c-%03d'%i,'origem':k,'estrato':estrato,'codigo_predito':cod,'codigo_real':None,
          'prova_id':x.get('prova_id') or k.split('#',1)[0],'item':x.get('item'),'enunciado':x.get('enunciado'),'gabarito':x.get('gabarito')})
    dest=BASE/'fila'/'calibracao-p1-complemento.jsonl';dest.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out),encoding='utf-8')
    print(len(out),'itens ->',dest)
if __name__=='__main__':main()
