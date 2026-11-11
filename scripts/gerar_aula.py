#!/usr/bin/env python3
"""Materializa uma aula HTML a partir do plano já calculado.
Não cria caderno nem grava no ledger; a geração do caderno é uma etapa separada.
"""
import argparse,json,datetime,hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('tema'); ap.add_argument('--aula',type=int,default=1); ap.add_argument('--confirmar',action='store_true'); a=ap.parse_args()
    if not a.confirmar: raise SystemExit('Use --confirmar para materializar a aula solicitada.')
    slug=a.tema.lower().replace('·','-').replace(' ','-'); base=ROOT/'aulas'/slug; plan=json.loads((base/'plano.json').read_text(encoding='utf-8')); x=plan['aulas'][a.aula-1]; out=base/('aula%d'%a.aula); out.mkdir(parents=True,exist_ok=True)
    hs=[]
    for i,n in enumerate(x['nucleos'],1):
        t=n.get('texto') or n.get('id'); hs.append(f'<h2>{i}. {t}</h2><div class="ped-par"><b>Cenário:</b> um gestor precisa decidir como controlar, corrigir e comunicar um resultado público relacionado a este núcleo.</div><p><b>Ideia central:</b> {t}. Relacione o ator responsável, o objeto fiscalizado e a consequência jurídica.</p><div class="ped-chk"><details><summary>Recuperação ativa</summary><p>Explique a ideia sem consultar o texto e compare-a com controle interno, externo e social.</p></details></div>')
    body='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Aula %d — %s</title><link rel="stylesheet" href="../../_template/dark.css"></head><body><main><p class="muted">%s · Aula %d · v1</p><h1>Trilha de estudo: aula %d</h1><p>Material gerado a partir do plano de prioridade. Use os cenários e a recuperação ativa antes de abrir o caderno.</p>%s</main></body></html>'%(a.aula,a.tema,a.tema,a.aula,a.aula,''.join(hs))
    (out/'corpo.html').write_text(body,encoding='utf-8')
    man={'tema':a.tema,'aula':a.aula,'versao':1,'titulo':'Aula %d · %s'%(a.aula,a.tema),'origem':'gerar_aula.py','data':str(datetime.date.today()),'didatica_v2':True,'nucleos':[n['id'] for n in x['nucleos']],'caderno':[],'estado':{},'hash':hashlib.sha1(body.encode()).hexdigest()[:12]}
    (out/'manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=1),encoding='utf-8')
    print('aula criada:',out)
if __name__=='__main__': main()
