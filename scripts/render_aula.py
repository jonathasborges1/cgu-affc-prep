#!/usr/bin/env python3
"""Renderiza uma aula: template dark.css + corpo.html -> PDF (precisa de playwright/chromium).
Uso: python3 render_aula.py aulas/p3-seg-1/aula1   (gera aula.pdf na mesma pasta)
Custo em tokens: zero (o texto já está salvo em corpo.html)."""
import sys,os
from pathlib import Path
d=Path(sys.argv[1]); base=Path(__file__).resolve().parent.parent  # cgu-bd/
css=(base/'aulas'/'_template'/'dark.css').read_text(encoding='utf-8')
corpo=(d/'corpo.html').read_text(encoding='utf-8')
t=json=None
import json
m=json.loads((d/'manifest.json').read_text(encoding='utf-8'))
if m.get('didatica_v2'):
    import re
    partes=re.split(r'<h2>(.*?)</h2>',corpo,flags=re.S)
    conceituais=[partes[i+1] for i in range(1,len(partes),2) if re.match(r'\s*(?:[2-9]|10)\.',partes[i])]
    falhas=[]
    for i,bloco in enumerate(conceituais,2):
        if 'data-didatica="cenario"' not in bloco and 'ped-par' not in bloco: falhas.append('bloco %d sem cenário'%i)
        if 'data-didatica="recuperacao"' not in bloco and 'ped-chk' not in bloco: falhas.append('bloco %d sem recuperação ativa'%i)
    if len(conceituais)!=9: falhas.append('esperados 9 blocos conceituais (2 a 10), encontrados %d'%len(conceituais))
    if falhas: raise SystemExit('GATE DIDÁTICO REPROVADO: '+'; '.join(falhas))
html='<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>'%(m.get('titulo','Aula'),css,corpo)
(d/'aula.html').write_text(html, encoding='utf-8')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file://'+str((d/'aula.html').resolve()))
    pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
    pg.pdf(path=str(d/'aula.pdf'),prefer_css_page_size=True,print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'}); b.close()
print('ok',d/'aula.pdf')
