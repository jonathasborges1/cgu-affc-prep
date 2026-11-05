#!/usr/bin/env python3
"""Ordena o passivo de classificacao pelo impacto esperado no ranking."""
import json, sys
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/'scripts'))
import prioridade as PR, suficiencia as SU
def lerj(p):
    try: return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
    except Exception: return []
def conc():
    a=BASE/'concursos'/'ativo.txt'; return BASE/'concursos'/a.read_text(encoding='utf-8').strip()
def main():
    d=conc(); pri=PR.priorizar(1); rank={x['codigo']:x['score_estudo'] for x in pri['linhas']}
    provas={x['prova_id']:x for x in lerj(d/'provas.jsonl')}; var={x['prova_id']:x for x in lerj(d/'descoberta'/'varredura.jsonl')}
    out=[]
    for pid,p in provas.items():
        if p.get('estado') not in ('extraida','baixada'): continue
        itens=lerj(d/'escopo'/(pid+'.jsonl')); impacto=0; fortes=Counter()
        for x in itens:
            c=(x.get('compat') or {}); cod=c.get('edital_prov') or ''
            if c.get('nivel')!='forte' or ' ' not in cod: continue
            cod=SU._pai(cod,1); fortes[cod]+=1; impacto+=rank.get(cod,0)
        meta=var.get(pid,{}); peso=SU.peso_prova(pid,var,{})
        out.append({'prova_id':pid,'estado':p.get('estado'),'impacto':round(impacto*peso,2),'peso_fonte':round(peso,3),
                    'itens_escopo':len(itens),'fortes':sum(fortes.values()),'topicos':fortes.most_common(5)})
    out.sort(key=lambda x:(-x['impacto'],-x['fortes'],x['prova_id']))
    dest=BASE/'fila'/'classificacao-priorizada.json'; dest.write_text(json.dumps({'gerado_por':'fila_classificacao.py','total':len(out),'provas':out},ensure_ascii=False,indent=2),encoding='utf-8')
    print('fila',len(out),'->',dest)
    for x in out[:15]: print('%7.1f %-58s fortes=%d'%(x['impacto'],x['prova_id'][:58],x['fortes']))
if __name__=='__main__': main()
