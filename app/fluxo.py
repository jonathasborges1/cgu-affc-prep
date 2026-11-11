"""Workflow (somente leitura) do CGU Treino.
O app NÃO executa nada: ele só observa o que o Claude (chat) e os scripts produzem
nas pastas do projeto — contagens por etapa, arquivos alterados e o log de execução."""
import json, os, time, datetime
from pathlib import Path

APP = Path(__file__).resolve().parent
BASE = Path(os.environ.get('CGU_BASE') or APP.parent)
def conc():
    a = BASE / 'concursos' / 'ativo.txt'
    return BASE / 'concursos' / (a.read_text().strip() if a.exists() else 'cgu-affc-ti-ds')

# (n, nome, quem executa, descrição, padrões de arquivos observados [relativos ao concurso ativo ou à raiz])
ETAPAS = [
    (1, 'Descoberta', 'script', 'Varre o catálogo do Cebraspe e ranqueia provas', ['c:descoberta/*']),
    (2, 'Download e extração', 'script', 'Baixa PDFs, extrai itens e filtra pelo edital', ['c:provas.jsonl', 'c:extraidos/*', 'c:itens/*']),
    (3, 'Escopo e duplicatas', 'script', 'Remove repetidos e monta o lote do tema', ['c:escopo/*', 'c:pacotes/*']),
    (4, 'Classificação', 'Claude', 'Agente classificador-itens', ['c:classificacoes/*', 'c:classificacao/*', 'c:classificados/*']),
    (5, 'Verificação', 'Claude', 'Agente verificador-classificacao + comparação mecânica', ['c:verificacoes/*', 'c:verificacao/*', 'c:pacotes/*-verif.md']),
    (6, 'Persistência', 'script', 'Grava itens aprovados no banco', ['c:banco.jsonl', 'c:nucleos.jsonl']),
    (7, 'Priorização', 'script', 'Cobertura, plano de núcleos e micro-aulas', ['aulas/*/plano*', 'progresso/*']),
    (8, 'Aula', 'Claude', 'Skill gerar-aula: escreve a micro-aula em HTML', ['aulas/*/*']),
]
ATIVO_SEG = 120   # etapa "ativa" se algum arquivo mudou nos últimos 2 min

def _lines(path):
    p = Path(path)
    if not p.exists(): return 0
    return sum(1 for l in open(p, encoding='utf-8', errors='replace') if l.strip())

def _glob(pat):
    base, _, g = pat.partition(':')
    root = conc() if base == 'c' else BASE
    try: return [p for p in root.glob(g) if p.is_file()]
    except Exception: return []

def _ultima(pats):
    m = 0.0; n = 0
    for pat in pats:
        for p in _glob(pat):
            n += 1
            try: m = max(m, p.stat().st_mtime)
            except OSError: pass
    return m, n

def _fmt(t):
    return datetime.datetime.fromtimestamp(t).strftime('%d/%m %H:%M:%S') if t else ''

def etapas_info():
    provas = [json.loads(l) for l in open(conc() / 'provas.jsonl', encoding='utf-8') if l.strip()] if (conc() / 'provas.jsonl').exists() else []
    est = {}
    for p in provas: est[p.get('estado', '?')] = est.get(p.get('estado', '?'), 0) + 1
    cat = _lines(conc() / 'descoberta' / 'catalogo.jsonl'); cand = _lines(conc() / 'descoberta' / 'candidatas.jsonl')
    pacotes = sorted((conc() / 'pacotes').glob('*.md')) if (conc() / 'pacotes').exists() else []
    aulas = len(list((BASE / 'aulas').glob('*/aula*'))) if (BASE / 'aulas').exists() else 0
    LT = lotes()['lotes']
    n_c = sum(1 for x in LT if 'c' in x['etapas']); n_esp = sum(1 for x in LT if x['estado'].startswith('classificado'))
    n_v = sum(1 for x in LT if x['estado'] == 'verificado'); n_rev = sum(1 for x in LT if x['estado'].startswith('reclassificado'))
    info = {
        1: '%d eventos no catálogo · %d provas candidatas' % (cat, cand),
        2: '%d provas extraídas aguardando classificação' % est.get('extraida', 0),
        3: '%d pacotes gerados' % len([p for p in pacotes if not p.name.endswith('-verif.md')]),
        4: '%d lotes classificados (%d aguardando verificação) · %d provas extraídas pendentes' % (n_c, n_esp, est.get('extraida', 0)),
        5: '%d lotes verificados · %d a reverificar · %d provas classificadas aguardando' % (n_v, n_rev, est.get('classificada', 0)),
        6: '%d provas "verificada" aguardando aplicar · %d persistidas' % (est.get('verificada', 0), est.get('persistida', 0)),
        7: 'rank e plano leem o banco ao vivo',
        8: '%d aulas geradas' % aulas,
    }
    agora = time.time(); out = []
    for n, nome, quem, desc, pats in ETAPAS:
        m, qtd = _ultima(pats)
        out.append({'n': n, 'nome': nome, 'quem': quem, 'desc': desc, 'info': info[n], 'arquivos': qtd,
                    'ultima': _fmt(m), 'idade': int(agora - m) if m else None, 'ativo': bool(m and agora - m < ATIVO_SEG)})
    return {'etapas': out, 'provas': est, 'agora': _fmt(agora)}

def atividade(janela_min=30, limite=25):
    """Arquivos alterados recentemente nas pastas do projeto + final do log de execução."""
    corte = time.time() - janela_min * 60; achados = []
    for raiz in (conc(), BASE / 'aulas', BASE / 'progresso', BASE / 'logs'):
        if not raiz.exists(): continue
        try:
            for p in raiz.rglob('*'):
                if p.is_file():
                    try:
                        mt = p.stat().st_mtime
                    except OSError: continue
                    if mt >= corte: achados.append((mt, p))
        except Exception: pass
    achados.sort(key=lambda x: -x[0])
    arqs = [{'quando': _fmt(mt), 'arquivo': str(p.relative_to(BASE)).replace('\\', '/'), 'kb': round(p.stat().st_size / 1024, 1)} for mt, p in achados[:limite]]
    log = []; lf = BASE / 'logs' / 'execucao.log'
    if lf.exists(): log = lf.read_text(encoding='utf-8-sig', errors='replace').splitlines()[-60:]
    return {'arquivos': arqs, 'log': log, 'janela_min': janela_min}


# ---------------------------------------------------------------- lotes por tema
def _prog(lote):
    """Progresso do lote em itens: classificados e verificados contra o total do escopo."""
    c = conc()
    def n(sub, nome):
        p = c / sub / (nome + '.jsonl')
        return _lines(p) if p.exists() and p.stat().st_size < 5000000 else None
    E = n('escopo', lote); Cn = n('classificacoes', lote) or 0; PR = n('classificacoes', lote + '-pendentes-revisao') or 0; V = n('verificacoes', lote) or 0
    tot = E or (Cn + PR) or None
    if not tot: return None
    return {'total': tot, 'classificados': Cn + PR, 'aprovados': Cn, 'em_revisao': PR, 'verificados': V}

def lotes():
    """Uma linha por lote (tema-* ou prova) com as 4 fases e a hora de cada arquivo."""
    c = conc(); d = {}
    def add(sub, chave, suf=None):
        pasta = c / sub
        if not pasta.exists(): return
        for p in pasta.iterdir():
            if not p.is_file(): continue
            n = p.name
            if sub == 'pacotes':
                if n.endswith('-verif.md'): d.setdefault(n[:-9], {})['pv'] = p
                elif n.endswith('.md'): d.setdefault(n[:-3], {})['p'] = p
            elif n.endswith('.jsonl'):
                nome = n[:-6]
                if chave == 'e' and not nome.startswith('tema-'): continue
                if chave == 'c' and nome.endswith('-pendentes-revisao'):
                    d.setdefault(nome[:-18], {})['pr'] = p; continue
                d.setdefault(nome, {})[chave] = p
    add('escopo', 'e'); add('pacotes', 'p'); add('classificacoes', 'c'); add('verificacoes', 'v')
    agora = time.time(); out = []
    for nome, f in d.items():
        et = {}
        for k, p in f.items():
            try: st = p.stat()
            except OSError: continue
            et[k] = {'t': st.st_mtime, 'quando': _fmt(st.st_mtime), 'kb': round(st.st_size / 1024, 1),
                     'linhas': _lines(p) if k in ('e', 'c', 'v', 'pr') and st.st_size < 5000000 else None}
        if not et: continue
        c_, v_, p_, e_ = et.get('c'), et.get('v'), et.get('p'), et.get('e')
        if v_ and c_ and v_['t'] >= c_['t']: est, cor = 'verificado', 'ok'
        elif v_ and c_: est, cor = 'reclassificado: reverificar', 'aviso'
        elif c_: est, cor = 'classificado: aguarda verificação', 'rodando'
        elif p_: est, cor = 'pacote pronto: aguarda classificação', 'rodando'
        elif e_: est, cor = 'escopo pronto', 'rodando'
        else: est, cor = 'verificação sem classificação', 'aviso'
        prog = _prog(nome)
        if prog and prog['em_revisao'] and est == 'verificado': est, cor = 'verificado · %d em revisão' % prog['em_revisao'], 'aviso'
        ult = max(x['t'] for x in et.values())
        out.append({'lote': nome, 'tema': nome.startswith('tema-'), 'estado': est, 'cor': cor, 'etapas': et,
                    'prog': prog, 'ultima': _fmt(ult), 't': ult, 'idade': int(agora - ult), 'ativo': agora - ult < ATIVO_SEG})
    out.sort(key=lambda x: -x['t'])
    return {'lotes': out[:40], 'total': len(out), 'agora': _fmt(agora)}

# ---------------------------------------------------------------- eventos (log dinâmico)
import threading, re as _re
LOGS = BASE / 'logs'
EVT = LOGS / 'eventos.jsonl'
_lock = threading.Lock()
_MAPA = {'descoberta': 1, 'provas.jsonl': 2, 'extraidos': 2, 'itens': 2, 'escopo': 3, 'pacotes': 3,
         'classificacoes': 4, 'classificacao': 4, 'classificados': 4, 'verificacoes': 5, 'verificacao': 5,
         'banco.jsonl': 6, 'nucleos.jsonl': 6}

def _nivel(t):
    s = str(t).lower()
    if _re.search(r'\berro\b|falha|traceback|exception|negado', s): return 'erro'
    if _re.search(r'parada|pulada|aviso|desatualizada|incompleta|reverificar', s): return 'aviso'
    if _re.search(r'conclu|pronto|gravado|persistid|terminou: ok|\bok\b', s): return 'ok'
    return 'info'

def registrar(msg, etapa=None, nivel=None, fonte='app', lote=None, feito=None, total=None, t=None):
    """Acrescenta um evento em logs/eventos.jsonl (uma linha JSON). Usado pelo app, pelos scripts e pelo Claude."""
    t = t or time.time()
    ev = {'t': round(t, 2), 'h': datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S'), 'etapa': etapa,
          'nivel': nivel or _nivel(msg), 'fonte': fonte, 'msg': str(msg).replace('\n', ' ')[:300]}
    if lote: ev['lote'] = lote
    if feito is not None: ev['feito'] = feito
    if total is not None: ev['total'] = total
    with _lock:
        LOGS.mkdir(exist_ok=True)
        with open(EVT, 'a', encoding='utf-8') as f: f.write(json.dumps(ev, ensure_ascii=False) + '\n')

def eventos(desde=0, limite=400):
    """Eventos novos a partir do deslocamento em bytes `desde`. Devolve o próximo deslocamento."""
    if not EVT.exists(): return {'eventos': [], 'prox': 0, 'reinicio': False}
    tam = EVT.stat().st_size; reinicio = False; meio = False
    if desde > tam: desde = 0; reinicio = True
    if desde == 0 and tam > 200000: desde = tam - 200000; meio = True
    with open(EVT, 'rb') as f:
        f.seek(desde); b = f.read()
    i = b.rfind(b'\n')
    if i < 0: return {'eventos': [], 'prox': desde, 'reinicio': reinicio}
    linhas = b[:i + 1].split(b'\n')[:-1]
    if meio and linhas: linhas = linhas[1:]
    evs = []
    for l in linhas[-limite:]:
        try: evs.append(json.loads(l.decode('utf-8', 'replace')))
        except Exception: pass
    return {'eventos': evs, 'prox': desde + i + 1, 'reinicio': reinicio}

def _snap():
    s = {}
    for raiz, tag in ((conc(), 'c'), (BASE / 'aulas', 'b'), (BASE / 'progresso', 'b')):
        if not raiz.exists(): continue
        try:
            for p in raiz.rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts:
                    try: st = p.stat(); s[p] = (st.st_mtime, st.st_size, tag)
                    except OSError: pass
        except Exception: pass
    return s

def _etapa_de(p, tag):
    root = conc() if tag == 'c' else BASE
    try: rel = p.relative_to(root).as_posix()
    except ValueError: return None, None, None
    top = rel.split('/')[0]
    if tag == 'c':
        if rel.endswith('-verif.md'): return 5, rel, p.name[:-9]
        lote = p.stem if top in ('escopo', 'pacotes', 'classificacoes', 'verificacoes') else None
        if lote and lote.endswith('-pendentes-revisao'): lote = lote[:-18]
        return _MAPA.get(top), rel, lote
    return (8 if top == 'aulas' else 7 if top == 'progresso' else None), rel, None

def _semear():
    """Primeira execução: traz as últimas linhas do execucao.log para o fluxo de eventos."""
    lf = LOGS / 'execucao.log'
    if EVT.exists() or not lf.exists(): return
    mt = lf.stat().st_mtime
    for l in [x for x in lf.read_text(encoding='utf-8-sig', errors='replace').splitlines() if x.strip()][-40:]:
        registrar(l, fonte='log', t=mt)

def _vigia_eventos():
    snap = _snap(); ult = {}; lf = LOGS / 'execucao.log'
    off = lf.stat().st_size if lf.exists() else 0; t_rot = 0
    while True:
        time.sleep(2)
        try:
            agora = time.time(); nov = _snap()
            for p, (mt, sz, tag) in nov.items():
                ant = snap.get(p)
                if ant and ant[0] == mt and ant[1] == sz: continue
                if agora - ult.get(p, 0) < 4: continue          # agrupa rajadas do mesmo arquivo
                ult[p] = agora
                etapa, rel, lote = _etapa_de(p, tag)
                if not rel: snap[p] = (mt, sz, tag); continue
                d = (sz - (ant[1] if ant else 0)) / 1024
                txt = '%s %s (%+.1f KB' % (rel, 'criado' if not ant else 'alterado', d)
                if p.suffix == '.jsonl' and sz < 5000000: txt += ', %d linhas' % _lines(p)
                feito = total = None
                if lote and etapa in (4, 5) and tag == 'c':
                    g = _prog(lote)
                    if g: total = g['total']; feito = g['classificados'] if etapa == 4 else g['verificados']
                registrar(txt + ')', etapa=etapa, nivel='info', fonte='app', lote=lote, feito=feito, total=total)
                snap[p] = (mt, sz, tag)
            for p in [q for q in snap if q not in nov]:
                etapa, rel, lote = _etapa_de(p, snap[p][2])
                if rel: registrar('%s removido' % rel, etapa=etapa, nivel='aviso', fonte='app', lote=lote)
                del snap[p]
            if lf.exists():                                       # acompanha o que os scripts escrevem no execucao.log
                tam = lf.stat().st_size
                if tam < off: off = 0
                if tam > off:
                    with open(lf, 'rb') as f: f.seek(off); novo = f.read()
                    off = tam
                    for l in novo.decode('utf-8-sig', 'replace').splitlines():
                        if l.strip(): registrar(l, fonte='log')
            if agora - t_rot > 120 and EVT.exists() and EVT.stat().st_size > 2000000:   # rodízio do arquivo de eventos
                t_rot = agora
                with _lock:
                    ls = EVT.read_text(encoding='utf-8', errors='replace').splitlines()[-1500:]
                    tmp = EVT.with_suffix('.tmp'); tmp.write_text('\n'.join(ls) + '\n', encoding='utf-8'); tmp.replace(EVT)
        except Exception:
            pass

def iniciar_eventos():
    try: _semear()
    except Exception: pass
    try:
        v = (APP / 'versao.txt').read_text(encoding='utf-8').strip()
    except Exception: v = '?'
    registrar('app iniciado (v%s): acompanhando arquivos do projeto e o execucao.log' % v, fonte='app', nivel='info')
    threading.Thread(target=_vigia_eventos, daemon=True).start()
