#!/usr/bin/env python3
"""Gera caderno HTML com questões reais da aula; não altera o ledger."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('tema');ap.add_argument('--aula',type=int,required=True);ap.add_argument('--max',type=int,default=10);ap.add_argument('--confirmar',action='store_true');a=ap.parse_args()
    if not a.confirmar: raise SystemExit('Use --confirmar para materializar o caderno solicitado.')
    slug=a.tema.lower().replace('·','-').replace(' ','-'); d=ROOT/'aulas'/slug; m=json.loads((d/('aula%d'%a.aula)/'manifest.json').read_text(encoding='utf-8')); b=[json.loads(l) for l in open(ROOT/'concursos'/'cgu-affc-ti-ds'/'banco.jsonl',encoding='utf-8') if l.strip()]; ns=set(m.get('nucleos') or []); qs=[x for x in b if ns.intersection(x.get('nucleos') or [])][:a.max]
    out=d/('aula%d'%a.aula)/'cadernoA.html'; rows=[]
    for i,x in enumerate(qs,1): rows.append('<article><h3>%d. %s</h3><p>%s</p><p class="muted">%s · item %s · gabarito: %s</p></article>'%(i,x.get('ref',''),x.get('enunciado',''),x.get('url',''),x.get('item',''),x.get('gabarito','')))
    out.write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Caderno %s Aula %d</title></head><body><main><h1>Caderno A — %s · Aula %d</h1>%s</main></body></html>'%(a.tema,a.aula,a.tema,a.aula,''.join(rows)),encoding='utf-8');print('caderno criado:',out,'itens:',len(qs))
if __name__=='__main__':main()
