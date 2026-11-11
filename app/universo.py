"""Universo de provas x edital x banco. Só biblioteca padrão. Lê arquivos ao vivo."""
import json, os, re, hashlib
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(os.environ.get('CGU_BASE') or Path(__file__).resolve().parent.parent)
def conc():
    a = BASE / 'concursos' / 'ativo.txt'
    return BASE / 'concursos' / (a.read_text().strip() if a.exists() else 'cgu-affc-ti-ds')
def L(p):
    p = Path(p)
    if not p.exists(): return []
    out = []
    for l in open(p, encoding='utf-8', errors='replace'):
        l = l.strip()
        if l:
            try: out.append(json.loads(l))
            except Exception: pass
    return out
def sec(cod):  # 'P3·SEG 1.2' -> 'P3·SEG 1'
    return re.split(r'\.', str(cod), 1)[0].strip()
def codes(x):
    e = x.get('edital')
    if isinstance(e, list): return [str(i) for i in e]
    return [str(e)] if e else []

def calcular(cobertura=0.90, min_esperado=7.0):
    C = conc()
    cat = L(C / 'descoberta' / 'catalogo.jsonl'); cand = L(C / 'descoberta' / 'candidatas.jsonl')
    var = {x['prova_id']: x for x in L(C / 'descoberta' / 'varredura.jsonl') if 'n_compat' in x}
    provas = {x['prova_id']: x for x in L(C / 'provas.jsonl')}
    banco = L(C / 'banco.jsonl'); prog = L(C / 'programa.json')
    pm = {c['prova_id']: c for c in cand}

    # --- heurística: rendimento esperado de itens FORTES (casam com o edital) por faixa de prior.
    # Faixas já medidas usam a média medida; abaixo da menor faixa medida o rendimento decai 40% por faixa
    # (suposição declarada, corrigida sozinha quando novas provas dessas faixas forem varridas).
    med = defaultdict(list)
    for pid, v in var.items():
        p = v.get('prior', pm.get(pid, {}).get('prior'))
        if p is not None: med[int(p // 1)].append(v.get('n_forte', 0))
    mb = {b: sum(l) / len(l) for b, l in med.items()}
    g = sum(mb.values()) / len(mb) if mb else 10.0
    lo = min(mb) if mb else 4; hi = max(mb) if mb else 4
    def faixa_rend(b):
        if b in mb: return mb[b], 'medida'
        if b > hi: return mb[hi], 'estimada'
        return mb[lo] * (0.6 ** (lo - b)), 'estimada'
    faixa = {b: faixa_rend(b)[0] for b in range(min(0, lo), hi + 1)}
    def esperado(c):
        v = var.get(c['prova_id'])
        if v: return float(v.get('n_forte', 0)), 'medido'
        b = int(c['prior'] // 1); return faixa_rend(b)[0], 'estimado'
    linhas = []
    for c in cand:
        e, tipo = esperado(c)
        pr = provas.get(c['prova_id'])
        linhas.append({'prova_id': c['prova_id'], 'ano': c.get('ano'), 'orgao': c.get('orgao'), 'cargo': c.get('cargo'), 'prior': c['prior'],
                       'esperado': round(e, 1), 'tipo': tipo, 'estado': (pr or {}).get('estado') or ('varrida' if c['prova_id'] in var else 'descoberta')})
    linhas.sort(key=lambda r: -r['esperado'])
    tot = sum(r['esperado'] for r in linhas) or 1
    acc = 0; alvo = []
    for r in linhas:
        if r['esperado'] < min_esperado or acc / tot >= cobertura: break
        acc += r['esperado']; alvo.append(r)
    alvo_ids = {r['prova_id'] for r in alvo}

    # --- funil
    ESTADOS = ['descoberta', 'varrida', 'baixada', 'extraida', 'classificada', 'verificada', 'persistida']
    est_alvo = Counter(r['estado'] for r in alvo)
    est_prov = Counter(p.get('estado') for p in provas.values())
    urls = {x.get('url') for x in banco if x.get('url')}
    anos = Counter(e.get('eventoAno') for e in cat)
    # --- por seção do edital (nível 1): compatíveis encontrados na varredura x itens no banco
    secs = {}
    for t in prog:
        if t.get('nivel') == 1: secs[t['codigo']] = {'codigo': t['codigo'], 'prova': t['prova'], 'bloco': t['bloco_titulo'], 'topico': t['texto'], 'compat': 0, 'banco': 0}
    for pid, v in var.items():
        for k, n in (v.get('por_edital') or {}).items():
            s = sec(k)
            if s in secs: secs[s]['compat'] += n
    for x in banco:
        for k in codes(x):
            s = sec(k)
            if s in secs: secs[s]['banco'] += 1
    ped = conc() / 'edital-oficial.pdf'
    nloc = 0
    pdir = BASE / 'provas'
    if pdir.exists(): nloc = sum(1 for f in pdir.rglob('*') if f.suffix.lower() == '.pdf')
    return {
        'edital': {'pdf': ped.exists(), 'tamanho_kb': round(ped.stat().st_size / 1024) if ped.exists() else 0,
                   'sha256': hashlib.sha256(ped.read_bytes()).hexdigest()[:16] if ped.exists() else None,
                   'topicos': len(prog), 'secoes': len(secs), 'programa_md': (conc() / 'programa.md').exists(), 'regras_md': (conc() / 'regras-da-prova.md').exists(), 'lexico': (conc() / 'lexico.json').exists()},
        'funil': {'eventos': len(cat), 'anos': dict(sorted(anos.items())), 'provas_descobertas': len(cand), 'universo_alvo': len(alvo),
                  'alvo_medidas': sum(1 for r in alvo if r['tipo'] == 'medido'), 'alvo_a_varrer': sum(1 for r in alvo if r['tipo'] != 'medido'),
                  'varridas': len(var), 'em_workflow': len(provas), 'estados_workflow': dict(est_prov), 'estados_alvo': dict(est_alvo),
                  'provas_no_banco': len(urls), 'itens_no_banco': len(banco), 'pdfs_locais': nloc,
                  'massa_esperada_alvo': round(acc), 'massa_total': round(tot)},
        'heuristica': {'cobertura_massa': cobertura, 'min_esperado': min_esperado, 'rendimento_global': round(g, 1),
                       'metrica': 'itens fortes por prova', 'faixas': {str(b): {'n_medidas': len(med.get(b, [])), 'rend': round(faixa[b], 1), 'origem': faixa_rend(b)[1], 'candidatas': sum(1 for c in cand if int(c['prior'] // 1) == b)} for b in sorted(faixa) if b >= 0}},
        'secoes': sorted(secs.values(), key=lambda s: (s['prova'], s['codigo'])),
        'alvo': [dict(r, no_alvo=True, no_banco=(r['prova_id'] in {p for p, q in provas.items() if q.get('estado') == 'persistida'})) for r in alvo[:300]],
    }
