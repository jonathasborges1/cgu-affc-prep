#!/usr/bin/env python3
"""Gera amostra cega reproduzivel, estratificada e sem repetir a auditoria anterior.

Uso: python scripts/gerar_amostra_cega_v2.py [--n 60] [--seed 20261109]
Os rótulos da triagem ficam somente nos manifestos privados.
"""
import argparse
import hashlib
import json
import random
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONC = ROOT / 'concursos' / 'cgu-affc-ti-ds'
FILA = ROOT / 'fila'


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def norm(text):
    text = unicodedata.normalize('NFKD', str(text or '').lower())
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return re.sub(r'\W+', ' ', text).strip()


def pool(bloco):
    extracted = {}
    for path in (ROOT / 'extraidos').glob('*.jsonl'):
        for item in read_jsonl(path):
            extracted[(item.get('prova_id'), str(item.get('item')))] = item
    candidates = {}
    for path in sorted((CONC / 'amostras').glob(f'{bloco.lower()}-verif-1-mapa.jsonl')):
        for row in read_jsonl(path):
            key = (row.get('prova_id'), str(row.get('item')))
            item = extracted.get(key)
            if item and len(norm(item.get('enunciado'))) >= 35:
                row = dict(row)
                row['_item'] = item
                # Um mesmo item pode aparecer em mais de um arquivo de amostra.
                if key not in candidates or float(row.get('score') or 0) > float(candidates[key].get('score') or 0):
                    candidates[key] = row
    return list(candidates.values())


def previous_keys(bloco):
    keys, texts = set(), set()
    path = FILA / f'verificacao-cega-{bloco.lower()}.jsonl'
    if path.exists():
        for row in read_jsonl(path):
            keys.add((row.get('prova_id'), str(row.get('item'))))
            texts.add(norm(row.get('enunciado')))
    return keys, texts


def generate(bloco, n, seed):
    all_rows = pool(bloco)
    excluded_keys, excluded_texts = previous_keys(bloco)
    seen_texts = set()
    rows = []
    for row in all_rows:
        item = row['_item']
        key = (row.get('prova_id'), str(row.get('item')))
        text = norm(item.get('enunciado'))
        if key in excluded_keys or text in excluded_texts or text in seen_texts:
            continue
        seen_texts.add(text)
        rows.append(row)
    rows.sort(key=lambda x: (float(x.get('score') or 0), x.get('prova_id') or '', str(x.get('item'))))
    strata = [rows[i * len(rows) // 3:(i + 1) * len(rows) // 3] for i in range(3)]
    rng = random.Random(seed + (2 if bloco == 'P2' else 3))
    target = min(n, len(rows))
    base, rem = divmod(target, 3)
    quotas = [base + (i < rem) for i in range(3)]
    selected = []
    for i, group in enumerate(strata):
        take = min(quotas[i], len(group))
        selected.extend((x, ('baixo', 'medio', 'alto')[i]) for x in rng.sample(group, take))
        quotas[i] -= take
    # Redistribui cotas quando algum estrato não tem população suficiente.
    for i, group in enumerate(strata):
        if not quotas[i]:
            continue
        already = {x.get('id') for x, _ in selected}
        spare = [x for x in group if x.get('id') not in already]
        take = min(quotas[i], len(spare))
        selected.extend((x, ('baixo', 'medio', 'alto')[i]) for x in rng.sample(spare, take))
    selected.sort(key=lambda pair: (('baixo', 'medio', 'alto').index(pair[1]), pair[0].get('id', '')))

    programa = read_jsonl(CONC / 'programa.json')
    codigos = sorted({x['codigo'] for x in programa if x.get('prova') == bloco})
    public, private = [], []
    for row, stratum in selected:
        item = row['_item']
        ident = f"cego-v2-{bloco.lower()}-{len(public) + 1:03d}"
        public.append({
            'id': ident, 'prova_id': row.get('prova_id'), 'item': row.get('item'),
            'gabarito': row.get('gabarito'), 'enunciado': item.get('enunciado', ''),
            'referencia': item.get('ref'), 'url': item.get('url'), 'codigos_candidatos': codigos,
        })
        private.append({
            'id': ident, 'origem': row.get('id'), 'estrato': stratum,
            'score_original': row.get('score'), 'triagem': row.get('triagem'),
            'edital_prov': row.get('edital_prov'),
        })
    pop = {name: len(group) for name, group in zip(('baixo', 'medio', 'alto'), strata)}
    sample_counts = {name: sum(x['estrato'] == name for x in private) for name in pop}
    stem = f'verificacao-cega-v2-{bloco.lower()}'
    (FILA / f'{stem}.jsonl').write_text('\n'.join(json.dumps(x, ensure_ascii=False) for x in public) + ('\n' if public else ''), encoding='utf-8')
    manifest = {
        'bloco': bloco, 'n': len(public), 'status': 'aguarda_classificacao_semantica',
        'metodo': 'deduplicacao por item e texto normalizado; sorteio sem reposicao dentro de tercis de score',
        'semente': seed, 'populacao_elegivel': len(rows),
        'populacao_por_estrato': pop, 'amostra_por_estrato': sample_counts,
        'peso_expansao_por_estrato': {k: (round(pop[k] / sample_counts[k], 6) if sample_counts[k] else None) for k in pop},
        'excluidos_auditoria_anterior': len(excluded_keys), 'rotulos_ocultos': private,
    }
    (FILA / f'{stem}-manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{bloco}: {len(public)} itens; população elegível={len(rows)}; estratos={sample_counts}; semente={seed}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=60)
    parser.add_argument('--seed', type=int, default=20261109)
    args = parser.parse_args()
    for block in ('P2', 'P3'):
        generate(block, args.n, args.seed)
