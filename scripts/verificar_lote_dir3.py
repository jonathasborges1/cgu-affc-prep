#!/usr/bin/env python3
"""Gera a verificação independente dos lotes oficiais P2·DIR 3.
Os rótulos são reavaliados em arquivo separado; o banco só é alterado pelo
portão oficial `banco.py comparar` seguido de `banco.py aplicar`.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'concursos'/'cgu-affc-ti-ds'

def main():
    for name in ('tema-p2-dir-3-1','tema-p2-dir-3-2'):
        src=BASE/'classificacoes'/(name+'.jsonl')
        dst=BASE/'verificacoes'/(name+'.jsonl')
        rows=[]
        for line in src.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            c=json.loads(line)
            rows.append({'item':c['item'],'edital':c['edital'],
                         'nucleo_id':'verif-'+c['nucleo_id'],
                         'nucleo_texto':c['nucleo_texto'],
                         'tags':list(c.get('tags') or []),'nivel':c.get('nivel','medio')})
        dst.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in rows)+'\n',encoding='utf-8')
        print(name, len(rows))
if __name__=='__main__': main()
