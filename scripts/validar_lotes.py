#!/usr/bin/env python3
"""Valida saídas já produzidas sem avançar estado nem gravar no banco.

Confere completude/estrutura das classificações, códigos do edital e tags. Saída
JSON local própria para orientar revisão humana; aprovação semântica segue sendo
responsabilidade do verificador independente e dos portões do banco.py.
"""
import json, os, re, sys
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE))
import banco as B

def ler(path):
    return B.lerj(path)

def validar(pid):
    extra=ler(B.P('extraidos',pid+'.jsonl'))
    cl=ler(B.PC('classificacoes',pid+'.jsonl'))
    programa={x['codigo'] for x in B.programa()}
    por_item={str(x.get('item')):x for x in extra}
    erros=[]; vistos=set()
    for n,x in enumerate(cl,1):
        item=str(x.get('item'))
        if item in vistos: erros.append('item duplicado: '+item)
        vistos.add(item)
        if item not in por_item: erros.append('item fora da extração: '+item)
        cod=x.get('edital')
        if cod!='FORA' and cod not in programa: erros.append('código inexistente no edital: '+str(cod))
        tags=set(x.get('tags') or [])
        if not tags.issubset(B.TAGS): erros.append('tags inválidas no item '+item)
        if not x.get('nucleo_texto') and x.get('nucleo_novo'): erros.append('núcleo novo sem texto no item '+item)
    faltam=sorted(set(por_item)-vistos)
    excesso=sorted(vistos-set(por_item))
    return {'prova_id':pid,'itens_extraidos':len(extra),'itens_classificados':len(cl),'faltantes':faltam,'excedentes':excesso,'erros':erros,
            'classificacao_estrutural_ok':bool(extra and len(extra)==len(cl) and not faltam and not excesso and not erros),
            'aviso':'validacao estrutural apenas; nao substitui verificacao semantica independente'}

def main():
    args=sys.argv[1:]
    if not args:
        ids=[p['prova_id'] for p in B.provas() if p.get('estado')=='extraida']
    else: ids=args
    out=[validar(pid) for pid in ids]
    dest=B.PC('fila','validacao-estrutural.json')
    Path(dest).parent.mkdir(parents=True,exist_ok=True)
    Path(dest).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return int(any(not x['classificacao_estrutural_ok'] for x in out))

if __name__=='__main__': raise SystemExit(main())
