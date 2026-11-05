#!/usr/bin/env python3
"""CGU Treino – MVP (M1). Servidor local: Painel, Banco, Treino com progresso, Aulas.
Só biblioteca padrão. Ouve apenas em 127.0.0.1. Uso: python servidor.py [--porta 8787] [--sem-navegador]
Dados lidos ao vivo do cgu-bd (pasta acima desta). Progresso em SQLite local (+ espelho JSONL em progresso/)."""
import json, os, sqlite3, subprocess, sys, threading, time, webbrowser, argparse, re, datetime, mimetypes
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fluxo, universo, edital

APP = Path(__file__).resolve().parent
BASE = Path(os.environ.get('CGU_BASE') or APP.parent)           # cgu-bd
def conc():
    a = BASE / 'concursos' / 'ativo.txt'
    return BASE / 'concursos' / (a.read_text().strip() if a.exists() else 'cgu-affc-ti-ds')
def dbpath():
    if os.environ.get('CGU_DB'): return Path(os.environ['CGU_DB'])
    root = os.environ.get('LOCALAPPDATA') or str(Path.home() / '.local' / 'share')
    return Path(root) / 'cgu-treino' / 'treino.db'
AUL = BASE / 'aulas'
PROG = BASE / 'progresso'
LOCK = threading.Lock()

def db():
    p = dbpath(); p.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(p)); c.row_factory = sqlite3.Row
    c.execute('''CREATE TABLE IF NOT EXISTS respostas(id INTEGER PRIMARY KEY AUTOINCREMENT, k TEXT, caderno TEXT, resposta TEXT,
        correta INTEGER, pontos INTEGER, ms INTEGER, conf INTEGER, ts TEXT, nucleo TEXT, tags TEXT, edital TEXT)''')
    c.execute('CREATE TABLE IF NOT EXISTS aulas_lidas(aula TEXT PRIMARY KEY, lida INTEGER, ts TEXT)')
    return c

def lerj(f):
    f = Path(f)
    if not f.exists(): return []
    return [json.loads(l) for l in open(f, encoding='utf-8') if l.strip()]
def chave(x): return '%s#%s' % (x.get('prova_id'), x.get('item'))
def limpar(t):
    # alguns enunciados extraídos trazem a justificativa do gabarito colada; ela entregaria a resposta
    return re.split(r'\s*JUSTIFICATIVA\b', t, flags=re.I)[0].strip()
def slug(t): return t.lower().replace('·', '-').replace(' ', '-')

_cache = {}
def banco():
    f = conc() / 'banco.jsonl'
    m = f.stat().st_mtime if f.exists() else 0
    if _cache.get('m') != m:
        _cache['m'] = m; _cache['b'] = lerj(f)
        _cache['idx'] = {chave(x): x for x in _cache['b']}
    return _cache['b']
def nucleos():
    return {j['id']: j for j in lerj(conc() / 'nucleos.jsonl')}

def planos():
    out = []
    for f in sorted(AUL.glob('*/plano-real/plano.json')) + sorted(AUL.glob('*/plano.json')):
        try: out.append((f, json.loads(f.read_text(encoding='utf-8'))))
        except Exception: pass
    out += _planos_assoc()
    return out

def _res_assoc(x):
    nt = nucleos().get((x.get('nucleos') or [''])[0], {}).get('texto', '')
    return {'k': '%s#%s' % (x.get('prova_id'), x.get('item')), 'prova_id': x.get('prova_id'), 'item': x.get('item'), 'ref': x.get('ref'), 'url': x.get('url'), 'url_gab': x.get('url_gab'),
            'enunciado': x['enunciado'], 'gabarito': x.get('gabarito'), 'nivel': x.get('nivel'), 'tags': x.get('tags') or [], 'padrao': x.get('padrao'), 'edital': x.get('edital'),
            'nucleo': (x.get('nucleos') or [''])[0], 'nucleo_texto': nt}

def _planos_assoc():
    """Cadernos por conteúdo ensinado: aulas/*/aulaN/associacao.json + manifest.json (cadernos 1..N)"""
    out = []
    for f in sorted(AUL.glob('*/aula*/associacao.json')):
        try:
            A = json.loads(f.read_text(encoding='utf-8')); M = json.loads((f.parent / 'manifest.json').read_text(encoding='utf-8'))
            banco(); idx = _cache['idx']; nt = nucleos()
            cads = {}
            for nome, ks in (M.get('cadernos') or {}).items():
                L = [_res_assoc(idx[k]) for k in ks if k in idx]
                if L: cads[nome] = L
            if not cads: continue
            tema = '%s · aula %s (por conteúdo)' % (M.get('tema'), M.get('aula'))
            P = {'tema': tema, 'n_itens': sum(len(v) for v in cads.values()), 'aulas': [{'k': int(M.get('aula', 1)), 'nucleos': [{'id': n, 'texto': nt.get(n, {}).get('texto', '')} for n in A['ensina']],
                 'massa': sum(len(v) for v in cads.values()), 'amostra': sum(len(v) for v in cads.values()), 'cadernos': cads}]}
            out.append((f, P))
        except Exception: pass
    return out

def comentario(q):
    v = 'Certo' if q.get('gabarito') == 'C' else 'Errado'
    p = ['Gabarito: %s.' % v]
    if q.get('nucleo_texto'): p.append('Ideia testada: ' + q['nucleo_texto'])
    if q.get('padrao'): p.append('Padrão da banca: ' + q['padrao'])
    if q.get('tags'): p.append('Etiquetas: ' + ', '.join(q['tags']))
    return ' '.join(p)

def ultimas(c):
    """última resposta por item"""
    rows = c.execute('SELECT * FROM respostas WHERE id IN (SELECT MAX(id) FROM respostas GROUP BY k)').fetchall()
    return {r['k']: r for r in rows}

# ---------- API ----------
def api_resumo():
    b = banco(); c = db()
    est = {}
    for p in lerj(conc() / 'provas.jsonl'): est[p.get('estado', '?')] = est.get(p.get('estado', '?'), 0) + 1
    sec = {}
    for x in b:
        e = str(x.get('edital', '') or '?')
        cod = edital.norm(e)
        if cod: s = re.sub(r'\.\d+.*$', '', cod)
        elif 'FORA' in e.upper(): s = 'FORA do edital'
        else: s = re.sub(r'\.\d+.*$', '', e); s = s + ' (sem tópico do edital identificado)' if s in ('P1', 'P2', 'P3') else s
        sec[s] = sec.get(s, 0) + 1
    ul = ultimas(c)
    n_ac = sum(1 for r in ul.values() if r['correta'] == 1)
    n_er = sum(1 for r in ul.values() if r['correta'] == 0)
    n_br = sum(1 for r in ul.values() if r['correta'] is None)
    log = []
    lf = BASE / 'logs' / 'execucao.log'
    if lf.exists(): log = lf.read_text(encoding='utf-8-sig', errors='replace').splitlines()[-25:]
    return {'itens': len(b), 'nucleos': len(nucleos()), 'provas': est, 'secoes': sorted(sec.items(), key=lambda t: -t[1]),
            'respondidas': len(ul), 'acertos': n_ac, 'erros': n_er, 'brancos': n_br, 'pontos': n_ac - n_er,
            'aulas_lidas': c.execute('SELECT COUNT(*) FROM aulas_lidas WHERE lida=1').fetchone()[0], 'log': log}

def api_planos():
    c = db(); ul = ultimas(c); out = []
    for f, P in planos():
        aulas = []
        for a in P['aulas']:
            cads = []
            for nome, L in a['cadernos'].items():
                feitas = sum(1 for q in L if q['k'] in ul)
                ac = sum(1 for q in L if q['k'] in ul and ul[q['k']]['correta'] == 1)
                er = sum(1 for q in L if q['k'] in ul and ul[q['k']]['correta'] == 0)
                cads.append({'nome': nome, 'total': len(L), 'feitas': feitas, 'acertos': ac, 'erros': er})
            lida = c.execute('SELECT lida FROM aulas_lidas WHERE aula=?', ('%s|%d' % (P['tema'], a['k']),)).fetchone()
            aulas.append({'k': a['k'], 'nucleos': [n['texto'] or n['id'] for n in a['nucleos']], 'massa': a['massa'], 'amostra': a['amostra'], 'cadernos': cads, 'lida': bool(lida and lida[0])})
        out.append({'id': str(f.relative_to(BASE)).replace('\\', '/'), 'tema': P['tema'], 'simulacao': P.get('simulacao'), 'n_itens': P['n_itens'], 'aulas': aulas})
    return out

def achar_plano(pid):
    for f, P in planos():
        if str(f.relative_to(BASE)).replace('\\', '/') == pid: return P
def api_caderno(q):
    P = achar_plano(q['plano'][0]); k = int(q['aula'][0]); nome = q['caderno'][0]
    if not P: return {'erro': 'plano não encontrado'}
    c = db(); ul = ultimas(c)
    for a in P['aulas']:
        if a['k'] == k and nome in a['cadernos']:
            itens = []
            for x in a['cadernos'][nome]:
                y = {kk: x[kk] for kk in ('k', 'enunciado', 'nivel', 'tags', 'ref', 'url', 'url_gab', 'item', 'nucleo', 'nucleo_texto', 'edital')}; y['enunciado'] = limpar(y['enunciado'])
                y['tags_visiveis'] = False
                r = ul.get(x['k'])
                if r:
                    y['anterior'] = {'resposta': r['resposta'], 'correta': r['correta'], 'gabarito': x['gabarito'], 'comentario': comentario(x)}
                itens.append(y)
            return {'tema': P['tema'], 'aula': k, 'caderno': nome, 'itens': itens}
    return {'erro': 'caderno não encontrado'}

def gabarito_de(k, plano_id=None):
    banco()
    x = _cache['idx'].get(k)
    if x:
        nt = nucleos().get((x.get('nucleos') or [''])[0], {}).get('texto', '')
        return {'gabarito': x.get('gabarito'), 'padrao': x.get('padrao'), 'tags': x.get('tags') or [], 'nucleo': (x.get('nucleos') or [''])[0], 'nucleo_texto': nt, 'edital': x.get('edital')}
    for f, P in planos():              # itens de planos simulados não estão no banco real
        for a in P['aulas']:
            for L in a['cadernos'].values():
                for q in L:
                    if q['k'] == k: return {'gabarito': q['gabarito'], 'padrao': q.get('padrao'), 'tags': q.get('tags') or [], 'nucleo': q.get('nucleo'), 'nucleo_texto': q.get('nucleo_texto'), 'edital': q.get('edital')}

def api_resposta(d):
    g = gabarito_de(d['k'])
    if not g: return {'erro': 'item desconhecido'}
    r = d['resposta']
    correta = None if r == 'B' else (1 if r == g['gabarito'] else 0)
    pontos = 0 if r == 'B' else (1 if correta else -1)
    ts = datetime.datetime.now().isoformat(timespec='seconds')
    with LOCK:
        c = db()
        c.execute('INSERT INTO respostas(k,caderno,resposta,correta,pontos,ms,conf,ts,nucleo,tags,edital) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                  (d['k'], d.get('caderno', ''), r, correta, pontos, d.get('ms'), d.get('conf'), ts, g['nucleo'], json.dumps(g['tags'], ensure_ascii=False), g['edital']))
        c.commit(); c.close()
        PROG.mkdir(exist_ok=True)
        with open(PROG / 'respostas.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': ts, 'k': d['k'], 'caderno': d.get('caderno'), 'resposta': r, 'correta': correta, 'pontos': pontos, 'ms': d.get('ms'), 'conf': d.get('conf'), 'nucleo': g['nucleo'], 'tags': g['tags'], 'edital': g['edital']}, ensure_ascii=False) + '\n')
    return {'correta': correta, 'pontos': pontos, 'gabarito': g['gabarito'], 'comentario': comentario(g)}

def api_progresso():
    c = db(); ul = ultimas(c)
    por_n = {}; por_t = {}
    for r in ul.values():
        n = por_n.setdefault(r['nucleo'] or '?', {'ac': 0, 'er': 0, 'br': 0})
        key = 'ac' if r['correta'] == 1 else ('er' if r['correta'] == 0 else 'br')
        n[key] += 1
        for t in json.loads(r['tags'] or '[]'):
            tt = por_t.setdefault(t, {'ac': 0, 'er': 0, 'br': 0}); tt[key] += 1
    nt = nucleos()
    nuc = [{'id': k, 'texto': nt.get(k, {}).get('texto', k), **v} for k, v in por_n.items()]
    nuc.sort(key=lambda z: (-(z['er'] + z['br']), z['id']))
    tags = [{'tag': k, **v} for k, v in por_t.items()]
    tags.sort(key=lambda z: -z['er'])
    erros = [r['k'] for r in ul.values() if r['correta'] == 0]
    hist = c.execute("SELECT substr(ts,1,10) d, COUNT(*) n, SUM(pontos) p FROM respostas GROUP BY d ORDER BY d DESC LIMIT 14").fetchall()
    return {'nucleos': nuc, 'tags': tags, 'fila_refazer': len(erros), 'dias': [dict(h) for h in hist]}

def api_refazer():
    c = db(); ul = ultimas(c); ks = [k for k, r in ul.items() if r['correta'] == 0][:10]
    itens = []
    for f, P in planos():
        for a in P['aulas']:
            for L in a['cadernos'].values():
                for q in L:
                    if q['k'] in ks and all(i['k'] != q['k'] for i in itens):
                        itens.append({**{kk: q[kk] for kk in ('k', 'enunciado', 'nivel', 'tags', 'ref', 'url', 'url_gab', 'item', 'nucleo', 'nucleo_texto', 'edital')}, 'enunciado': limpar(q['enunciado'])})
    return {'tema': 'Refazer erros', 'aula': 0, 'caderno': 'R', 'itens': itens}

def api_banco(q):
    b = banco(); t = (q.get('q', [''])[0]).lower(); ed = q.get('edital', [''])[0]; tag = q.get('tag', [''])[0]; nv = q.get('nivel', [''])[0].lower()
    r = []
    for x in b:
        if t and t not in x['enunciado'].lower() and t not in ' '.join(x.get('nucleos') or []).lower(): continue
        if ed and not str(x.get('edital', '')).startswith(ed): continue
        if tag and tag not in (x.get('tags') or []): continue
        if nv and nv not in str(x.get('nivel', '')).lower().replace('á', 'a').replace('é', 'e'): continue
        r.append({'k': chave(x), 'enunciado': limpar(x['enunciado']), 'gabarito': x.get('gabarito'), 'nivel': x.get('nivel'), 'tags': x.get('tags') or [], 'edital': x.get('edital'), 'ref': x.get('ref'), 'url': x.get('url'), 'nucleo': (x.get('nucleos') or [''])[0], 'padrao': x.get('padrao')})
        if len(r) >= 100: break
    return {'total_filtrado': len(r), 'itens': r}

def api_aulas():
    c = db(); ul = ultimas(c); nt = nucleos(); out = []
    for m in sorted(AUL.glob('*/aula*/manifest.json')):
        j = json.loads(m.read_text(encoding='utf-8')); d = m.parent
        lida = c.execute('SELECT lida FROM aulas_lidas WHERE aula=?', ('aula|%s' % j.get('titulo', d.name),)).fetchone()
        tit = j.get('titulo') or d.name
        curto = re.sub(r'\s*\([^)]*\)\s*$', '', re.sub(r'^Aula\s*\d+\s*[–-]\s*', '', tit))
        pid = (d / 'associacao.json'); pid = str(pid.relative_to(BASE)).replace('\\', '/') if pid.exists() else None
        cads = []
        for nome, ks in sorted((j.get('cadernos') or {}).items()):
            f = sum(1 for k in ks if k in ul); ac = sum(1 for k in ks if k in ul and ul[k]['correta'] == 1); er = sum(1 for k in ks if k in ul and ul[k]['correta'] == 0)
            cads.append({'nome': nome, 'total': len(ks), 'feitas': f, 'acertos': ac, 'erros': er, 'pdf': (d / ('caderno%s.pdf' % nome)).exists(), 'plano': pid})
        nuc = [(nt.get(n, {}).get('texto') or n) for n in (j.get('ensina') or j.get('nucleos') or [])]
        out.append({'titulo': tit, 'curto': curto, 'num': j.get('aula'), 'versao': j.get('versao'), 'tema': j['tema'], 'dir': str(d.relative_to(AUL)).replace('\\', '/'), 'data': j['data'],
                    'pdf': (d / 'aula.pdf').exists(), 'cadernos_pdf': sorted(p.stem for p in d.glob('caderno*.pdf')), 'cadernos': cads, 'nucleos': nuc, 'lida': bool(lida and lida[0]), 'chave_lida': 'aula|%s' % tit})
    return out

ALIAS_EDITAL = {'P1 · Adm. pública 4.1': 'P1·ADM 4.1'}
MIN_MINIAULA = 6      # mini-aula só vale a pena com pelo menos este nº de questões ainda não cobertas
MAX_NUC_PACK = 5      # núcleos por mini-aula

def api_doc():
    """Números vivos para a aba 'Como funciona' e constantes das heurísticas."""
    import sys as _s
    _s.path.insert(0, str(BASE / 'scripts'))
    import importlib, suficiencia as SU; importlib.reload(SU)
    d = conc(); desc = d / 'descoberta'
    var = [v for v in lerj(desc / 'varredura.jsonl') if 'n_itens' in v]
    b = banco(); cls = [x for x in b if x.get('nucleos') and x.get('edital') != 'FORA']
    mans = [json.loads(m.read_text(encoding='utf-8')) for m in sorted(AUL.glob('*/aula*/manifest.json'))]
    return {'eventos': len(lerj(desc / 'catalogo.jsonl')), 'candidatas': len(lerj(desc / 'candidatas.jsonl')), 'provas_varridas': len(var),
            'itens_extraidos': sum(v['n_itens'] for v in var), 'itens_compat': sum(v['n_compat'] for v in var), 'itens_fortes': sum(v['n_forte'] for v in var),
            'banco_total': len(b), 'banco_classificados': len(cls), 'nucleos': len(nucleos()), 'aulas': len(mans),
            'cadernos': sum(len(m.get('cadernos') or {}) for m in mans), 'itens_em_cadernos': len({k for m in mans for ks in (m.get('cadernos') or {}).values() for k in ks}),
            'k': {'min_forte': SU.MIN_FORTE, 'min_provas': SU.MIN_PROVAS, 'tol_itens': SU.TOL_ITENS, 'rel': SU.REL, 'raro': SU.RARO, 'min_classif': SU.MIN_CLASSIF, 'cob_ok': SU.COB_OK,
                  'min_miniaula': MIN_MINIAULA, 'max_nuc_pack': MAX_NUC_PACK}}

def api_prioridade(nivel=1):
    """Prioridade e suficiência de amostra por assunto (cálculo em scripts/suficiencia.py)."""
    import sys as _s
    _s.path.insert(0, str(BASE / 'scripts'))
    import importlib, suficiencia as SU, prioridade as PR
    importlib.reload(SU); importlib.reload(PR)
    nivel = 2 if int(nivel) == 2 else 1
    try: cob = api_cobertura()
    except Exception: cob = []
    r0 = SU.calcular(nivel); cobr = {}
    for t in cob:
        for l in r0['linhas']:
            c = l['codigo']
            if c == t['tema'] or t['tema'].startswith(c + '.') or c.startswith(t['tema'] + '.'):
                r = cobr.setdefault(c, {'aulas': 0, 'cobertas': 0, 'total': 0, 'tema': t['tema']})
                r['aulas'] += t['aulas']; r['cobertas'] += t['cobertas']; r['total'] += t['total']
    stats = {}
    cdb = db()
    for x in ultimas(cdb).values():
        ed = ALIAS_EDITAL.get(x['edital'], x['edital'] or '')
        if ed == 'FORA' or ' ' not in ed: continue
        try: cod = SU._pai(ed, nivel)
        except Exception: continue
        s = stats.setdefault(cod, [0, 0]); s[1] += 1
        if x['correta'] == 1: s[0] += 1
    cdb.close()
    # Em C/E, 50% de acerto tem ganho liquido zero. Beta(1,1) evita extremos com poucas respostas.
    dominio = {cod: max(0.0, min(1.0, 2*((ac+1)/(n+2))-1)) for cod,(ac,n) in stats.items()}
    for l in r0['linhas']: l['cobertura'] = cobr.get(l['codigo'])
    out = PR.priorizar(nivel, dominio=dominio, base=r0)
    try: prec = json.loads((BASE / 'docs' / 'precisao-triagem-p1.json').read_text(encoding='utf-8'))
    except Exception: prec = {}
    for l in out['linhas']: l['prec'] = prec.get(l['codigo'])
    out['dominio_amostras'] = {k: {'acertos':v[0], 'tentativas':v[1], 'dominio':dominio[k]} for k,v in stats.items()}
    return out

def api_cobertura():
    """Por tema com aula: quantas questões existem no banco, quantas as aulas abordam e o que falta (em mini-aulas sugeridas)."""
    b = [x for x in banco() if x.get('nucleos') and x.get('edital') != 'FORA']; nt = nucleos(); out = []
    try: metas = json.loads((AUL / 'metas.json').read_text(encoding='utf-8'))
    except Exception: metas = {}
    por = {}
    for m in sorted(AUL.glob('*/aula*/manifest.json')):
        j = json.loads(m.read_text(encoding='utf-8')); por.setdefault(j['tema'], []).append(j)
    for tema, ms in por.items():
        ens = set(); [ens.update(j.get('ensina') or j.get('nucleos') or []) for j in ms]
        it = [x for x in b if ALIAS_EDITAL.get(x['edital'], x['edital']).startswith(tema)]
        cob = [x for x in it if set(x['nucleos']) <= ens]; desc = [x for x in it if not set(x['nucleos']) <= ens]
        cont = {}
        for x in desc:
            for n in x['nucleos']: cont[n] = cont.get(n, 0) + 1
        ordem = sorted(cont, key=lambda n: (-cont[n], n)); packs = []; cur = []; q = 0
        for n in ordem:
            cur.append(n); q += cont[n]
            if q >= MIN_MINIAULA or len(cur) >= MAX_NUC_PACK: packs.append((cur, q)); cur = []; q = 0
        if cur:
            if packs and q < MIN_MINIAULA and len(packs[-1][0]) + len(cur) <= MAX_NUC_PACK + 2: packs[-1] = (packs[-1][0] + cur, packs[-1][1] + q)
            else: packs.append((cur, q))
        n_aulas = len(ms)
        out.append({'tema': tema, 'total': len(it), 'cobertas': len(cob), 'descobertas': len(desc), 'aulas': n_aulas, 'meta': metas.get(tema), 'minimo': MIN_MINIAULA,
                    'nucleos_total': len({n for x in it for n in x['nucleos']}), 'nucleos_cobertos': len({n for x in cob for n in x['nucleos']}),
                    'minis': [{'nome': 'Mini-aula %d' % (n_aulas + i + 1), 'questoes': qq, 'vale': qq >= MIN_MINIAULA, 'nucleos': [{'id': n, 'texto': nt.get(n, {}).get('texto') or n, 'q': cont[n]} for n in ns]} for i, (ns, qq) in enumerate(packs)]})
    return out

def api_marcar_lida(d):
    with LOCK:
        c = db(); c.execute('INSERT OR REPLACE INTO aulas_lidas VALUES(?,?,?)', (d['aula'], 1 if d.get('lida', True) else 0, datetime.datetime.now().isoformat(timespec='seconds'))); c.commit(); c.close()
    return {'ok': True}

def api_gerar_plano(d):
    """NAO cria aula nem caderno. Confere a estrutura-base (somente leitura) e registra o pedido do aluno na fila."""
    tema = d.get('tema', 'P3·SEG 1')
    r = subprocess.run([sys.executable, str(BASE / 'scripts' / 'aula.py'), 'preparar', tema], capture_output=True, text=True, cwd=str(BASE), timeout=120)
    try: pr = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: pr = {'erro': (r.stdout + r.stderr)[-800:]}
    if d.get('pedir') and pr.get('estrutura_base_ok'):
        (BASE / 'fila').mkdir(exist_ok=True)
        with open(BASE / 'fila' / 'pedidos_aula.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': datetime.datetime.now().isoformat(timespec='seconds'), 'tema': tema, 'etapa': 'aula', 'estado': 'aguardando Claude'}, ensure_ascii=False) + '\n')
        pr['pedido_registrado'] = True
    pr['saida'] = ('Estrutura-base %s: %s itens classificados, %s micro-aulas possiveis. Nada foi criado. %s' % ('OK' if pr.get('estrutura_base_ok') else 'INCOMPLETA', pr.get('itens_classificados'), pr.get('micro_aulas_possiveis'), ('Pedido de aula registrado.' if pr.get('pedido_registrado') else 'Peca a aula ao Claude quando quiser estudar este tema; o caderno so e criado depois, sob novo pedido.')))
    pr['ok'] = r.returncode == 0
    return pr

def pagina_aula(rel):
    d = (AUL / rel).resolve()
    if AUL.resolve() not in d.parents: return None
    corpo = d / 'corpo.html'
    if not corpo.exists(): return None
    css = (AUL / '_template' / 'dark.css').read_text(encoding='utf-8')
    titulo = json.loads((d / 'manifest.json').read_text(encoding='utf-8')).get('titulo', 'Aula')
    extra = '''html,body{background:#0f1419}.pg{max-width:880px;margin:0 auto 24px;padding:24px 22px}.cover{height:auto!important}
    #lida{position:fixed;right:16px;bottom:16px;background:#238636;color:#fff;border:0;border-radius:8px;padding:10px 16px;font:600 14px sans-serif;cursor:pointer}'''
    js = '''<button id="lida">Marcar aula como lida</button><script>
    document.getElementById('lida').onclick=async()=>{await fetch('/api/aula-lida',{method:'POST',body:JSON.stringify({aula:'aula|%s',lida:true})});document.getElementById('lida').textContent='Lida ✔'}</script>''' % titulo.replace("'", "\\'")
    return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>%s</title><style>%s%s</style></head><body>%s%s</body></html>' % (titulo, css, extra, corpo.read_text(encoding='utf-8'), js)

def _sair(reiniciar):
    def go():
        time.sleep(0.6)
        if reiniciar and os.environ.get('CGU_LOOP') == '1': os._exit(3)   # o iniciar.bat reabre o servidor na MESMA janela
        if reiniciar:
            args = [sys.executable, str(Path(__file__).resolve())] + [a for a in sys.argv[1:] if a != '--sem-navegador'] + ['--sem-navegador']
            code = 'import time,subprocess,sys;time.sleep(1.5);subprocess.Popen(sys.argv[1:]' + (',creationflags=0x10' if os.name == 'nt' else ',start_new_session=True') + ')'
            subprocess.Popen([sys.executable, '-c', code] + args, **({'creationflags': 0x08000000} if os.name == 'nt' else {'start_new_session': True}))
        os._exit(0)
    threading.Thread(target=go, daemon=True).start()
    return {'ok': True, 'reiniciando': reiniciar}

def _num():
    try: return (APP / 'versao.txt').read_text(encoding='utf-8').strip()
    except Exception: return '?'
def _versao():
    h = [_num()]
    for f in sorted(APP.glob('*.py')) + [APP / 'index.html']:
        try: st = f.stat(); h.append('%s:%d:%d' % (f.name, st.st_mtime_ns, st.st_size))
        except Exception: pass
    return '|'.join(h)
def _vigia():
    # reinicia sozinho quando algum .py do app muda (e espera o arquivo parar de mudar)
    base = {f.name: f.stat().st_mtime_ns for f in APP.glob('*.py')}
    while True:
        time.sleep(2)
        try:
            now = {f.name: f.stat().st_mtime_ns for f in APP.glob('*.py')}
            if now != base:
                time.sleep(1.5)
                if now == {f.name: f.stat().st_mtime_ns for f in APP.glob('*.py')}:
                    try: compile(open(APP / 'servidor.py', encoding='utf-8').read(), 'servidor.py', 'exec')
                    except SyntaxError as e: print('mudança ignorada (erro de sintaxe):', e); base = now; continue
                    print('Código atualizado: reiniciando…'); _sair(True); return
                base = {f.name: f.stat().st_mtime_ns for f in APP.glob('*.py')}
        except Exception: pass

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _j(self, o, code=200):
        b = json.dumps(o, ensure_ascii=False).encode('utf-8')
        self.send_response(code); self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def _b(self, b, ct, code=200):
        self.send_response(code); self.send_header('Content-Type', ct); self.send_header('Cache-Control', 'no-store'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query); p = u.path
        # URLs limpas: /aula/<pasta>/<aulaN>  e  /aula-pdf/<pasta>/<aulaN>[/<arquivo>.pdf]  (as antigas ?dir= continuam valendo)
        if p.startswith('/aula-pdf/'):
            seg = unquote(p[len('/aula-pdf/'):]).strip('/')
            if seg.lower().endswith('.pdf') and '/' in seg: seg, arq = seg.rsplit('/', 1); q['arq'] = [arq]
            q['dir'] = [seg]; p = '/aula-pdf'
        elif p.startswith('/aula/'):
            q['dir'] = [unquote(p[len('/aula/'):]).strip('/')]; p = '/aula'
        try:
            if p == '/': return self._b((APP / 'index.html').read_bytes(), 'text/html; charset=utf-8')
            if p == '/api/resumo': return self._j(api_resumo())
            if p == '/api/planos': return self._j(api_planos())
            if p == '/api/caderno': return self._j(api_refazer() if q.get('caderno', [''])[0] == 'R' else api_caderno(q))
            if p == '/api/progresso': return self._j(api_progresso())
            if p == '/api/banco': return self._j(api_banco(q))
            if p == '/api/aulas': return self._j(api_aulas())
            if p == '/api/cobertura': return self._j(api_cobertura())
            if p == '/api/doc': return self._j(api_doc())
            if p == '/api/prioridade': return self._j(api_prioridade(q.get('nivel', ['1'])[0]))
            if p == '/api/workflow': return self._j(fluxo.etapas_info())
            if p == '/api/atividade': return self._j(fluxo.atividade())
            if p == '/api/lotes': return self._j(fluxo.lotes())
            if p == '/api/eventos': return self._j(fluxo.eventos(int((q.get('desde') or ['0'])[0] or 0)))
            if p == '/api/nomes': return self._j(edital.nomes())
            if p == '/api/versao': return self._j({'v': _versao(), 'versao': _num()})
            if p == '/api/edital': return self._j(edital.arvore())
            if p == '/api/edital-itens': return self._j(edital.itens(q['cod'][0]))
            if p == '/api/universo': return self._j(universo.calcular())
            if p == '/aula':
                h = pagina_aula(q['dir'][0])
                return self._b(h.encode('utf-8'), 'text/html; charset=utf-8') if h else self._j({'erro': 'aula não encontrada'}, 404)
            if p == '/aula-pdf':
                arq = q.get('arq', ['aula.pdf'])[0]
                if not re.fullmatch(r'(aula|caderno\d+)\.pdf', arq): arq = 'aula.pdf'
                f = (AUL / q['dir'][0] / arq).resolve()
                if AUL.resolve() in f.parents and f.exists(): return self._b(f.read_bytes(), 'application/pdf')
            self._j({'erro': 'não encontrado'}, 404)
        except Exception as e:
            self._j({'erro': str(e)}, 500)
    def do_POST(self):
        try:
            d = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
            p = urlparse(self.path).path
            if p == '/api/resposta': return self._j(api_resposta(d))
            if p == '/api/aula-lida': return self._j(api_marcar_lida(d))
            if p == '/api/gerar-plano': return self._j(api_gerar_plano(d))
            if p == '/api/reiniciar': return self._j(_sair(True))
            if p == '/api/encerrar': return self._j(_sair(False))
            self._j({'erro': 'não encontrado'}, 404)
        except Exception as e:
            self._j({'erro': str(e)}, 500)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--porta', type=int, default=8787); ap.add_argument('--sem-navegador', action='store_true'); a = ap.parse_args()
    srv = ThreadingHTTPServer(('127.0.0.1', a.porta), H)
    url = 'http://127.0.0.1:%d' % a.porta
    print('CGU Treino rodando em', url, '\nBanco de dados:', dbpath(), '\nPasta cgu-bd:', BASE, '\nCtrl+C para encerrar.')
    threading.Thread(target=_vigia, daemon=True).start()
    fluxo.iniciar_eventos()
    if not a.sem_navegador: threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print('\nencerrado')
