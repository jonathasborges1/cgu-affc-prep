#!/usr/bin/env python3
"""Valida invariantes do banco e separa erro critico de passivo de classificacao."""
import json, re, sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
BASE=Path(__file__).resolve().parent.parent
def lerj(p): return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def conc():
    a=BASE/'concursos'/'ativo.txt'; return BASE/'concursos'/a.read_text(encoding='utf-8').strip()
def main():
    d=conc(); b=lerj(d/'banco.jsonl'); ns={x['id'] for x in lerj(d/'nucleos.jsonl')}; erros=[]; avisos=[]; seen=set()
    req=('banca','ano','ref','url','url_gab','item','enunciado','gabarito','tema')
    for i,x in enumerate(b,1):
        falta=[k for k in req if not x.get(k)]
        if falta: erros.append({'linha':i,'tipo':'campos_ausentes','campos':falta})
        if urlparse(x.get('url','')).netloc!='cdn.cebraspe.org.br': erros.append({'linha':i,'tipo':'fonte_nao_oficial'})
        k=(x.get('url'),str(x.get('item')),re.sub(r'\W','',x.get('enunciado','').lower()))
        if k in seen: erros.append({'linha':i,'tipo':'duplicata'})
        seen.add(k)
        invalid=[n for n in (x.get('nucleos') or []) if n not in ns]
        if invalid: erros.append({'linha':i,'tipo':'nucleo_inexistente','nucleos':invalid})
        if not x.get('nucleos') or x.get('edital') in ('P1','P2','P3'):
            avisos.append({'linha':i,'tipo':'pendente_classificacao','fonte':x.get('fonte'),'item':x.get('item')})
    out={'banco':len(b),'nucleos':len(ns),'erros_criticos':erros,'avisos':avisos,
         'resumo':{'erros_criticos':len(erros),'pendentes_classificacao':sum(x['tipo']=='pendente_classificacao' for x in avisos)}}
    dest=BASE/'docs'/'qualidade-dados.json'; dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out['resumo'],ensure_ascii=False),'->',dest)
    return 1 if erros else 0
if __name__=='__main__': raise SystemExit(main())
