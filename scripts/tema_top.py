"""Lote por tema com teto: pega os N itens de maior score de uma seção (para chegar à meta por seção).
Uso: python3 scripts/tema_top.py "P3·ENG 1" --n 20 --niveis forte
Mesmo efeito do 'descobrir.py tema', mas ordenado por score e limitado a N; id tema-<secao>-top."""
import sys, re, argparse, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import descobrir as D

ap = argparse.ArgumentParser()
ap.add_argument('codigo'); ap.add_argument('--n', type=int, default=20); ap.add_argument('--niveis', default='forte')
a = ap.parse_args()
B = D.B
cand = []
for p in B.provas():
    if p['estado'] in ('persistida',) or p['prova_id'].startswith('tema-'): continue
    for i in B.lerj(B.PC('escopo', p['prova_id'] + '.jsonl')):
        if B.ematch(i['compat'].get('edital_prov'), a.codigo) and i['compat']['nivel'] in a.niveis.split(','):
            cand.append((i['compat'].get('score', 0), p['prova_id'], i))
cand.sort(key=lambda t: -t[0])
seen = set(); itens = []
for sc, pid, i in cand:
    k = re.sub(r'\W+', '', (i.get('enunciado') or '').lower())[:120]
    if k in seen: continue
    seen.add(k)
    j = {kk: v for kk, v in i.items() if kk != 'compat'}
    j.update({'item_orig': i['item'], 'prova_origem': pid, 'item': str(len(itens) + 1), 'compat': i['compat']})
    itens.append(j)
    if len(itens) >= a.n: break
if not itens: sys.exit('nenhum item')
pid = 'tema-' + re.sub(r'[^a-z0-9]+', '-', D.sa(a.codigo)).strip('-') + '-top'
B.escj(B.P('extraidos', pid + '.jsonl'), [{k: v for k, v in j.items() if k != 'compat'} for j in itens])
B.escj(B.PC('escopo', pid + '.jsonl'), itens)
pr = {'prova_id': pid, 'ref': 'Lote por tema %s (top %d por score, %d provas)' % (a.codigo, len(itens), len({j['prova_origem'] for j in itens})), 'url': 'lote', 'url_gab': 'lote', 'ano': 2024, 'orgao': 'varias', 'cargo': a.codigo, 'peso': 1.0, 'hash': None, 'n_itens': len(itens), 'n_gab': len(itens), 'verificacao': None, 'historico': []}
for e in ('descoberta', 'baixada', 'extraida'): B.hist(pr, e, 'lote por tema com teto (itens de provas já baixadas)')
B.prova_put(pr)
print('lote %s: %d itens' % (pid, len(itens)))
