"""Visão do conteúdo programático x questões do banco. Só biblioteca padrão."""
import re, unicodedata, json, ast
from collections import defaultdict, Counter
from universo import conc, L, BASE

BL = [('estado', 'ESTADO'), ('soc', 'SOC'), ('etic', 'ETICA'), ('adm', 'ADM'), ('gov', 'GOV'), ('transp', 'TRANSP'), ('dir', 'DIR'), ('evid', 'EVID'), ('aud', 'AUD'), ('eng', 'ENG'), ('arq', 'ARQ'), ('dad', 'DADOS'), ('seg', 'SEG')]
def sa(s): return ''.join(c for c in unicodedata.normalize('NFD', str(s or '')) if unicodedata.category(c) != 'Mn').lower()
def norm(cod):
    """'P1 · Adm. pública 4.1' / 'P3·SEG 1.2' -> 'P3·SEG 1.2'; None se não der para mapear."""
    s = sa(cod).strip()
    m = re.match(r'^(p[123])\s*·?\s*([a-z][a-z .\-]*?)\s*(\d+(?:\.\d+)*)?$', s)
    if not m: return None
    nome, num = m.group(2).strip(), m.group(3)
    for k, v in BL:
        if nome.startswith(k):
            return '%s·%s%s' % (m.group(1).upper(), v, (' ' + num) if num else '')
    return None
def lista(v):
    if isinstance(v, list): return v
    if isinstance(v, str) and v.startswith('['):
        try: return ast.literal_eval(v)
        except Exception: return []
    return [v] if v else []
def sob(cod, t): return cod == t or (cod or '').startswith(t + '.')

def dados():
    C = conc()
    prog = L(C / 'programa.json'); banco = L(C / 'banco.jsonl'); nuc = {n['id']: n for n in L(C / 'nucleos.jsonl')}
    var = L(C / 'descoberta' / 'varredura.jsonl')
    return C, prog, banco, nuc, var

def arvore():
    C, prog, banco, nuc, var = dados()
    cb = Counter(); sem = {'sem_codigo': 0, 'fora': 0}
    for x in banco:
        c = norm(x.get('edital'))
        if c: cb[c] += 1
        elif 'FORA' in str(x.get('edital')).upper(): sem['fora'] += 1
        else: sem['sem_codigo'] += 1
    cc = Counter()
    for v in var:
        for k, n in (v.get('por_edital') or {}).items():
            c = norm(k) or k
            cc[c] += n
    out = []
    for t in prog:
        cod = t['codigo']
        nb = sum(n for c, n in cb.items() if sob(c, cod)); nc = sum(n for c, n in cc.items() if sob(c, cod))
        nn = sum(1 for n in nuc.values() if sob(norm(n.get('edital')) or '', cod))
        out.append({'codigo': cod, 'prova': t['prova'], 'bloco': t['bloco'], 'bloco_titulo': t['bloco_titulo'], 'num': t['num'], 'nivel': t['nivel'], 'texto': t['texto'], 'banco': nb, 'compat': nc, 'nucleos': nn})
    tot_ext = sum(v.get('n_itens', 0) for v in var); comp = sum(v.get('n_compat', 0) for v in var); forte = sum(v.get('n_forte', 0) for v in var)
    try: cj = json.load(open(C / 'concurso.json', encoding='utf-8'))
    except Exception: cj = {}
    return {'concurso': {k: cj.get(k) for k in ('orgao', 'edital', 'banca', 'cargo', 'prova', 'provas_objetivas', 'prova_discursiva', 'pagina_oficial')}, 'topicos': out, 'sem': sem, 'classificacao': {
        'provas_varridas': len(var), 'itens_extraidos': tot_ext, 'compativeis': comp, 'fortes': forte,
        'no_banco': len(banco), 'com_tags': sum(1 for x in banco if lista(x.get('tags'))), 'com_nucleo': sum(1 for x in banco if lista(x.get('nucleos'))),
        'sem_codigo_edital': sem['sem_codigo'], 'fora_do_edital': sem['fora'], 'nucleos': len(nuc)}}

def itens(cod):
    C, prog, banco, nuc, var = dados()
    res = []
    for x in banco:
        c = norm(x.get('edital'))
        if c and sob(c, cod):
            enun = re.split(r'\s*JUSTIFICATIVA\b', x.get('enunciado', ''), flags=re.I)[0].strip()
            res.append({'ref': x.get('ref'), 'url': x.get('url'), 'item': x.get('item'), 'enunciado': enun, 'gabarito': x.get('gabarito'), 'nivel': x.get('nivel'),
                        'tags': lista(x.get('tags')), 'nucleos': [nuc.get(n, {}).get('texto', n) for n in lista(x.get('nucleos'))], 'codigo': c})
    nn = [{'id': n['id'], 'texto': n['texto'], 'edital': n.get('edital')} for n in nuc.values() if sob(norm(n.get('edital')) or '', cod)]
    return {'codigo': cod, 'itens': res, 'nucleos': nn}


def cap(s): s = str(s or ''); return s[:1] + s[1:].lower()
def tit(s): return re.sub(r'\.\s*$', '', str(s or '')).strip()

def nomes():
    """raw/código -> {'r': 'Bloco › 4 Título', 'c': '4 Título'} na nomenclatura do edital."""
    C, prog, banco, nuc, var = dados()
    por = {t['codigo']: t for t in prog}
    def mk(t): return {'r': '%s › %s %s' % (cap(t['bloco_titulo']), t['num'], tit(t['texto'])), 'c': '%s %s' % (t['num'], tit(t['texto']))}
    out = {k: mk(t) for k, t in por.items()}
    raws = {str(x.get('edital') or '') for x in banco} | {str(n.get('edital') or '') for n in nuc.values()}
    for r in raws:
        if not r or r in out: continue
        c = norm(r)
        if c and c in out: out[r] = out[c]
        elif 'FORA' in r.upper(): out[r] = {'r': 'Fora do edital', 'c': 'Fora do edital'}
        elif re.fullmatch(r'P[123]', r.strip()): out[r] = {'r': r + ' (sem tópico do edital identificado)', 'c': r + ' (sem tópico)'}
    out['FORA do edital'] = {'r': 'Fora do edital', 'c': 'Fora do edital'}
    return out
