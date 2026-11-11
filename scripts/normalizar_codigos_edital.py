#!/usr/bin/env python3
"""Normaliza apenas separadores estruturais dos códigos P1/P2/P3.
Não substitui o caractere de reposição no texto livre das questões.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
PASTAS=[ROOT/'concursos'/'cgu-affc-ti-ds',ROOT/'docs',ROOT/'fila']
PAT=re.compile(r'\b(P[123])(?:\u00c2\u00b7|\ufffd|·)([A-Z][A-Z0-9]*\s+\d+(?:\.\d+)*)')

def main():
    alterados=0; substituicoes=0
    for base in PASTAS:
        if not base.exists(): continue
        for p in base.rglob('*'):
            if not p.is_file() or p.suffix.lower() not in {'.json','.jsonl','.md','.txt'}: continue
            try: s=p.read_text(encoding='utf-8')
            except Exception: continue
            n=0
            def f(m):
                nonlocal n
                if m.group(0)!='%s\u00b7%s'%(m.group(1),m.group(2)): n+=1
                return '%s\u00b7%s'%(m.group(1),m.group(2))
            out=PAT.sub(f,s)
            if out!=s:
                p.write_text(out,encoding='utf-8');alterados+=1;substituicoes+=n;print(p.relative_to(ROOT),n)
    print('arquivos alterados:',alterados,'códigos normalizados:',substituicoes)
if __name__=='__main__': main()
