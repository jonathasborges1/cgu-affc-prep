#!/usr/bin/env python3
"""Associação de questões a uma aula por CONTEÚDO ensinado (não só por tema).
  associar.py aula aulas/p1-adm-4.1/aula1 [--max 10] [--gravar]
Regra: manifest.json da aula tem 'ensina' (lista de núcleos que o texto da aula realmente explica).
Questão é associável se TODOS os seus núcleos estão em 'ensina' (qualquer tema/edital).
Questões com algum núcleo fora de 'ensina' = LACUNA (aponta o que falta ensinar).
Gera cadernos de até --max itens, sem repetir questão já usada no ledger (cadernos_usados.jsonl)."""
import sys,json,argparse,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import aula as A
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('dir'); ap.add_argument('--max',type=int,default=10); ap.add_argument('--gravar',action='store_true'); ap.add_argument('--confirmar-caderno',action='store_true')
    a=ap.parse_args(); d=Path(a.dir); m=json.loads((d/'manifest.json').read_text(encoding='utf-8'))
    ens=set(m.get('ensina') or m.get('nucleos')); b=A.banco(); u=A.ledger(); nt=A.nuc_textos()
    ok=[x for x in b if x.get('nucleos') and set(x['nucleos'])<=ens and x.get('prova_id')]
    lac=[x for x in b if x.get('nucleos') and not set(x['nucleos'])<=ens and set(x['nucleos'])&ens]
    print('ensina %d núcleos | associáveis %d | já usadas %d | inéditas %d | lacuna parcial %d'%(len(ens),len(ok),sum(A.chave(x) in u for x in ok),sum(A.chave(x) not in u for x in ok),len(lac)))
    por={}
    for x in ok: por.setdefault(x['nucleos'][0],[]).append(x)
    for n,v in sorted(por.items()): print('  %-38s %d'%(n,len(v)))
    # cadernos: round-robin por núcleo para cada caderno cobrir o conteúdo todo
    novos=[x for x in ok if A.chave(x) not in u]
    filas={n:sorted([x for x in novos if x['nucleos'][0]==n],key=lambda x:-(x.get('ano') or 0)) for n in por}
    ordem=[];
    while any(filas.values()):
        for n in sorted(filas):
            if filas[n]: ordem.append(filas[n].pop(0))
    cads=[ordem[i:i+a.max] for i in range(0,len(ordem),a.max)]
    for i,c in enumerate(cads,1): print('caderno extra %d: %d itens'%(i,len(c)),[A.chave(x) for x in c])
    if a.gravar and not a.confirmar_caderno: sys.exit('RECUSADO: --gravar cria o caderno; so com --confirmar-caderno e sob pedido do aluno. Sem --gravar o comando e apenas simulacao.')
    if a.gravar:
        out={'aula':m.get('titulo'),'ensina':sorted(ens),'cadernos':[[dict(A._res(x,nt),comentario=x.get('comentario')) for x in c] for c in cads],'lacunas':[A.chave(x) for x in lac]}
        (d/'associacao.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8'); print('gravado',d/'associacao.json')
main()
