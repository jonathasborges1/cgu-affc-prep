#!/usr/bin/env python3
"""CGU Treino – MVP (M1). Servidor local: Painel, Banco, Treino com progresso, Aulas.
Só biblioteca padrão. Ouve apenas em 127.0.0.1. Uso: python servidor.py [--porta 8787] [--sem-navegador]
Dados lidos ao vivo do cgu-bd (pasta acima desta). Progresso em SQLite local (+ espelho JSONL em progresso/)."""
import threading
import json, html as html_mod, os, sqlite3, subprocess, sys, threading, time, webbrowser, argparse, re, datetime, mimetypes
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
_PRIORIDADE_CACHE = {}

_forcar_calculo = {'on': False}
_PRI_LOCK = threading.Lock()
def _prioridade_bg(nivel):
    if not _PRI_LOCK.acquire(blocking=False): return
    def _w():
        _forcar_calculo['on'] = True
        try: api_prioridade(nivel)
        except Exception: pass
        finally: _forcar_calculo['on'] = False; _PRI_LOCK.release()
    threading.Thread(target=_w, daemon=True).start()

_MT = {}
def _recarregar_se_mudou(mod):
    """Recarrega o módulo só se o arquivo mudou (preserva os caches de leitura entre chamadas)."""
    import importlib
    try: m = os.stat(mod.__file__).st_mtime_ns
    except Exception: return
    if _MT.get(mod.__name__) not in (None, m): importlib.reload(mod)
    _MT[mod.__name__] = m
_PAINEL_PRIORIDADE_CACHE = {'ts': 0, 'value': None}

def db():
    p = dbpath(); p.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(p)); c.row_factory = sqlite3.Row
    c.execute('''CREATE TABLE IF NOT EXISTS respostas(id INTEGER PRIMARY KEY AUTOINCREMENT, k TEXT, caderno TEXT, resposta TEXT,
        correta INTEGER, pontos INTEGER, ms INTEGER, conf INTEGER, ts TEXT, nucleo TEXT, tags TEXT, edital TEXT)''')
    c.execute('CREATE TABLE IF NOT EXISTS aulas_lidas(aula TEXT PRIMARY KEY, lida INTEGER, ts TEXT)')
    # Migração aditiva: preserva todo o histórico das versões anteriores.
    cols = {r[1] for r in c.execute('PRAGMA table_info(respostas)').fetchall()}
    for nome, tipo in (('motivo', 'TEXT'), ('motivo_detalhe', 'TEXT'), ('revisao_em', 'TEXT'), ('intervalo', 'INTEGER')):
        if nome not in cols: c.execute('ALTER TABLE respostas ADD COLUMN %s %s' % (nome, tipo))
    c.execute('CREATE TABLE IF NOT EXISTS config(chave TEXT PRIMARY KEY, valor TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS ultimo_acesso(id INTEGER PRIMARY KEY CHECK(id=1), url TEXT, titulo TEXT, ts TEXT)')
    # Erros e brancos antigos continuam visíveis na nova fila adaptativa.
    c.execute("UPDATE respostas SET revisao_em=substr(ts,1,10), intervalo=1 WHERE revisao_em IS NULL AND correta IS NOT 1")
    c.commit()
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

MOTIVOS = {
    'nao_leu': 'Não li/estudei este conteúdo',
    'nao_aprendeu': 'Li, mas não aprendi ou não entendi',
    'esqueceu': 'Já tinha estudado, mas esqueci',
    'interpretacao': 'Interpretei o enunciado de outra forma',
    'regra': 'Não conhecia a regra',
    'confusao': 'Confundi conceitos',
    'excecao': 'Não percebi uma exceção',
    'palavra': 'Caí em palavra-chave/absoluta',
    'atencao': 'Erro de atenção',
    'chute': 'Chutei ou acertei sem segurança',
    'outro': 'Outro motivo / não consegui identificar',
}

GUIAS_DIAGNOSTICO = {
    'nao_leu': ('Primeiro contato com o conteúdo', 'Estude primeiro o núcleo indicado. Depois, feche a aula e tente explicar a regra com suas palavras antes de conferir o comentário.', 'Faça uma questão diferente deste núcleo na revisão de amanhã.'),
    'nao_aprendeu': ('Reforço para aprender de verdade', 'Volte à explicação do núcleo, compare a regra com o comentário desta questão e explique em voz própria por que o gabarito está correto. Se ainda não conseguir, repita a leitura em blocos menores.', 'Depois do estudo, teste a compreensão com uma questão diferente na revisão de amanhã.'),
    'esqueceu': ('Recuperação de memória', 'Antes de abrir a aula, tente escrever ou falar tudo o que lembra sobre o núcleo. Só então confira o trecho e complete o que faltou; isso ajuda a recuperar a memória sem reler tudo.', 'A revisão adaptativa programará uma questão diferente para amanhã.'),
    'interpretacao': ('Leitura guiada do enunciado', 'Releia o enunciado e separe sujeito, afirmação e condição. Compare cada parte com o comentário e identifique onde sua interpretação mudou o sentido.', 'Na próxima questão, reescreva a afirmação em uma frase simples antes de julgar.'),
    'regra': ('Aprendizagem da regra', 'Estude o núcleo indicado e transforme a regra em um exemplo e um contraexemplo. Compare ambos com a justificativa do gabarito.', 'Faça uma questão diferente deste núcleo na revisão de amanhã.'),
    'confusao': ('Diferencie os conceitos', 'Abra o conteúdo indicado e monte uma comparação: conceito A, conceito B e o critério que os separa. Explique por que a questão pertence a um deles.', 'Na revisão, pratique uma questão que exija escolher entre conceitos próximos.'),
    'excecao': ('Reforce a exceção', 'Volte ao trecho indicado e localize a regra geral, a condição e a exceção. Destaque a palavra do enunciado que ativa ou afasta a exceção.', 'Na próxima questão, confira explicitamente condições e ressalvas antes de responder.'),
    'palavra': ('Treino de palavras decisivas', 'Releia o enunciado procurando termos absolutos, quantificadores, negações e limites. Confira se a regra realmente sustenta esse alcance.', 'Na revisão, destaque a palavra que mais altera o julgamento antes de marcar.'),
    'atencao': ('Estratégia contra desatenção', 'Não precisa reler a aula inteira agora. Refaça o julgamento mais devagar: sublinhe sujeito, negação, quantificador e exceções; depois confira cada trecho com o comentário.', 'Pratique outra questão e só finalize após uma conferência de 10 segundos.'),
    'chute': ('Transforme o chute em conhecimento recuperável', 'Estude o núcleo indicado e tente recuperar a regra sem olhar. Em seguida, explique por que uma alternativa de julgamento está certa e a outra não.', 'Na próxima tentativa, registre confiança baixa/média/alta para ajustar o ritmo de revisão.'),
    'outro': ('Plano de recuperação direcionado', 'Use o comentário para localizar a lacuna e estude o núcleo indicado. Se o motivo não estiver claro, anote o que dificultou a questão para ajustar a próxima recomendação.', 'A revisão adaptativa verificará o mesmo núcleo com uma questão diferente.'),
}

def recomendacao_diagnostico(k, motivo, detalhe=''):
    titulo, orientacao, proximo = GUIAS_DIAGNOSTICO.get(motivo, GUIAS_DIAGNOSTICO['outro'])
    material = api_recomendacao_aula({'k': [k]}) if k else {'aulas': [], 'nucleo_texto': ''}
    return {'titulo': titulo, 'orientacao': orientacao, 'proximo_passo': proximo,
            'detalhe_aluno': detalhe, 'nucleo_texto': material.get('nucleo_texto'),
            'aulas': material.get('aulas') or [], 'sem_aula': not bool(material.get('aulas'))}

def intervalo_revisao(correta, conf, acertos_anteriores=0):
    """Intervalo simples e explicável; confiança baixa impede falso domínio."""
    if correta != 1: return 1
    if not conf or conf <= 1: return 2
    if conf == 2: return 7
    return 30 if acertos_anteriores >= 2 else 15

def _somar_dias(iso, dias):
    base = datetime.date.fromisoformat(iso[:10])
    return (base + datetime.timedelta(days=dias)).isoformat()

def _item_treino(k):
    """Formato único usado por cadernos normais e pela revisão adaptativa."""
    banco(); x = _cache['idx'].get(k)
    if x:
        y = _res_assoc(x)
        y['enunciado'] = limpar(y['enunciado']); y['tags_visiveis'] = False
        return y
    for _f, P in planos():
        for a in P['aulas']:
            for L in a['cadernos'].values():
                for q in L:
                    if q['k'] == k:
                        return {**q, 'enunciado': limpar(q['enunciado']), 'tags_visiveis': False}
    return None

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
        anteriores = c.execute('SELECT correta FROM respostas WHERE nucleo=? ORDER BY id DESC LIMIT 2', (g['nucleo'],)).fetchall()
        sequencia = sum(1 for x in anteriores if x['correta'] == 1)
        intervalo = intervalo_revisao(correta, d.get('conf'), sequencia)
        revisao_em = _somar_dias(ts, intervalo)
        cur = c.execute('''INSERT INTO respostas(k,caderno,resposta,correta,pontos,ms,conf,ts,nucleo,tags,edital,revisao_em,intervalo)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (d['k'], d.get('caderno', ''), r, correta, pontos, d.get('ms'), d.get('conf'), ts, g['nucleo'], json.dumps(g['tags'], ensure_ascii=False), g['edital'], revisao_em, intervalo))
        resposta_id = cur.lastrowid
        c.commit(); c.close()
        PROG.mkdir(exist_ok=True)
        with open(PROG / 'respostas.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': ts, 'id': resposta_id, 'k': d['k'], 'caderno': d.get('caderno'), 'resposta': r, 'correta': correta, 'pontos': pontos, 'ms': d.get('ms'), 'conf': d.get('conf'), 'nucleo': g['nucleo'], 'tags': g['tags'], 'edital': g['edital'], 'revisao_em': revisao_em, 'intervalo': intervalo}, ensure_ascii=False) + '\n')
    return {'id': resposta_id, 'correta': correta, 'pontos': pontos, 'gabarito': g['gabarito'], 'comentario': comentario(g), 'nucleo': g['nucleo'], 'nucleo_texto': g.get('nucleo_texto') or g['nucleo'], 'revisao_em': revisao_em, 'intervalo': intervalo}

def api_diagnostico(d):
    motivo = d.get('motivo')
    if motivo not in MOTIVOS: return {'erro': 'motivo inválido'}
    detalhe = str(d.get('detalhe') or '').strip()[:500]
    with LOCK:
        c = db(); row = c.execute('SELECT id,k,nucleo FROM respostas WHERE id=?', (d.get('id'),)).fetchone()
        if not row:
            c.close()
            return {'erro': 'resposta não encontrada'}
        c.execute('UPDATE respostas SET motivo=?,motivo_detalhe=? WHERE id=?', (motivo, detalhe or None, row['id'])); c.commit(); c.close()
        PROG.mkdir(exist_ok=True)
        with open(PROG / 'respostas.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': datetime.datetime.now().isoformat(timespec='seconds'), 'tipo': 'diagnostico', 'id': row['id'], 'k': row['k'], 'nucleo': row['nucleo'], 'motivo': motivo, 'detalhe': detalhe or None}, ensure_ascii=False) + '\n')
    return {'ok': True, 'motivo': motivo, 'rotulo': MOTIVOS[motivo], 'recomendacao': recomendacao_diagnostico(row['k'], motivo, detalhe)}

def api_revisao_adaptativa():
    c = db(); hoje = datetime.date.today().isoformat(); ul = ultimas(c)
    rows = c.execute('''SELECT * FROM respostas WHERE nucleo IS NOT NULL AND id IN
        (SELECT MAX(id) FROM respostas WHERE nucleo IS NOT NULL GROUP BY nucleo)
        ORDER BY COALESCE(revisao_em,'9999-12-31'), id''').fetchall()
    devidas = [r for r in rows if r['revisao_em'] and r['revisao_em'] <= hoje]
    proximas = [r for r in rows if r['revisao_em'] and r['revisao_em'] > hoje]
    itens = []
    for r in devidas[:10]:
        # Prefere uma questão ainda não respondida do mesmo núcleo: mede transferência,
        # em vez de apenas decorar o gabarito do item anterior.
        cand = []
        for x in banco():
            if r['nucleo'] in (x.get('nucleos') or []): cand.append(chave(x))
        k = next((k for k in cand if k != r['k'] and k not in ul), r['k'])
        item = _item_treino(k)
        if item and all(x['k'] != item['k'] for x in itens): itens.append(item)
    c.close()
    return {'tema': 'Revisão adaptativa', 'aula': 0, 'caderno': 'Hoje', 'itens': itens,
            'devidas': len(devidas), 'proximas_7d': sum(1 for r in proximas if r['revisao_em'] <= _somar_dias(hoje, 7)),
            'proxima_data': proximas[0]['revisao_em'] if proximas else None}

def api_prontidao():
    c = db(); ul = ultimas(c)
    try: concurso = json.loads((conc() / 'concurso.json').read_text(encoding='utf-8'))
    except Exception: concurso = {}
    data = ((concurso.get('prova') or {}).get('data'))
    hoje = datetime.date.today(); prova = datetime.date.fromisoformat(data) if data else hoje
    dias = max(0, (prova - hoje).days)
    mans = []
    for m in sorted(AUL.glob('*/aula*/manifest.json')):
        try: mans.append(json.loads(m.read_text(encoding='utf-8')))
        except Exception: pass
    total_aulas = len(mans)
    lidas = c.execute('SELECT COUNT(*) FROM aulas_lidas WHERE lida=1').fetchone()[0]
    ks = {k for man in mans for vals in (man.get('cadernos') or {}).values() for k in vals}
    pend_q = sum(1 for k in ks if k not in ul)
    devidas = api_revisao_adaptativa()['devidas']
    # Estimativa transparente: 30 min/aula, 2 min/questão e 2 min/revisão.
    horas = round(max(0, total_aulas-lidas)*.5 + pend_q/30 + devidas/30, 1)
    semanas = max(dias/7, 1/7); necessarias = round(horas/semanas, 1)
    row = c.execute("SELECT valor FROM config WHERE chave='horas_semana'").fetchone()
    disponiveis = float(row['valor']) if row else 10.0
    status = 'viável' if necessarias <= disponiveis else ('apertado' if necessarias <= disponiveis*1.2 else 'insuficiente')
    c.close()
    return {'data_prova': data, 'dias': dias, 'aulas_total': total_aulas, 'aulas_lidas': min(lidas,total_aulas),
            'questoes_pendentes': pend_q, 'revisoes_devidas': devidas, 'horas_estimadas': horas,
            'horas_semana_necessarias': necessarias, 'horas_semana_disponiveis': disponiveis, 'status': status,
            'escopo': 'material já criado',
            'criterio': '30 min por aula não lida + 2 min por questão pendente ou revisão devida',
            'aviso': 'Este cálculo considera somente as aulas e os cadernos já criados. Lacunas do edital ainda sem material aparecem na aba Prioridade e não entram nesta estimativa.'}

def api_config(d):
    try: horas = max(1, min(80, float(d.get('horas_semana'))))
    except Exception: return {'erro': 'horas por semana inválidas'}
    c = db(); c.execute("INSERT INTO config(chave,valor) VALUES('horas_semana',?) ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor", (str(horas),)); c.commit(); c.close()
    return {'ok': True, 'horas_semana': horas}

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
    motivos = [{'motivo': MOTIVOS.get(r['motivo'], r['motivo']), 'n': r['n']} for r in c.execute(
        "SELECT motivo,COUNT(*) n FROM respostas WHERE motivo IS NOT NULL GROUP BY motivo ORDER BY n DESC").fetchall()]
    adapt = api_revisao_adaptativa()
    return {'nucleos': nuc, 'tags': tags, 'fila_refazer': len(erros), 'dias': [dict(h) for h in hist],
            'motivos': motivos, 'revisoes_devidas': adapt['devidas'], 'revisoes_7d': adapt['proximas_7d'], 'proxima_revisao': adapt['proxima_data']}

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

def api_revisoes():
    """Cadernos de revisão e resumos de véspera já gerados (aulas/<tema>/revisao*/)."""
    out = []
    for m in sorted(AUL.glob('*/revisao*/manifest.json')):
        try: j = json.loads(m.read_text(encoding='utf-8'))
        except Exception: continue
        d = m.parent
        out.append({'tema': j.get('tema'), 'dir': str(d.relative_to(AUL)).replace('\\', '/'), 'data': j.get('data'),
                    'caderno': (d / 'caderno-revisao.pdf').exists(), 'resumo': (d / 'resumo-vespera.pdf').exists()})
    return out

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
    try: nivel = 2 if int(nivel) == 2 else 1
    except Exception: nivel = 1
    agora = time.time(); cached = _PRIORIDADE_CACHE.get(nivel)
    if cached and agora - cached[0] < 30: return cached[1]
    if cached and not _forcar_calculo.get('on'):    # dado velho: responde na hora e atualiza em segundo plano
        _prioridade_bg(nivel); return cached[1]
    import sys as _s
    _s.path.insert(0, str(BASE / 'scripts'))
    import importlib, suficiencia as SU, prioridade as PR
    _recarregar_se_mudou(SU); _recarregar_se_mudou(PR)
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
    prec = {}
    for _f in ('p1', 'p2', 'p3'):
        try: prec.update(json.loads((BASE / 'docs' / ('precisao-triagem-%s.json' % _f)).read_text(encoding='utf-8')))
        except Exception: pass
    for l in out['linhas']: l['prec'] = prec.get(l['codigo'])
    out['dominio_amostras'] = {k: {'acertos':v[0], 'tentativas':v[1], 'dominio':dominio[k]} for k,v in stats.items()}
    try: out['classificador_p1'] = json.loads((BASE / 'docs' / 'classificador-p1.json').read_text(encoding='utf-8'))
    except Exception: out['classificador_p1'] = None
    try: out['ordem_p2'] = json.loads((BASE / 'docs' / 'ordem-p2-faixas.json').read_text(encoding='utf-8'))
    except Exception: out['ordem_p2'] = None
    try: out['confiabilidade_blocos'] = json.loads((BASE / 'docs' / 'confiabilidade-blocos.json').read_text(encoding='utf-8'))
    except Exception: out['confiabilidade_blocos'] = None
    _PRIORIDADE_CACHE[nivel] = (time.time(), out)
    return out

def api_painel_prioridade_calc():
    """Funil de dados, material por assunto, semaforo de aula e confianca da ordem (scripts/painel_prioridade.py)."""
    if _PAINEL_PRIORIDADE_CACHE['value'] is not None and time.time() - _PAINEL_PRIORIDADE_CACHE['ts'] < 30:
        return _PAINEL_PRIORIDADE_CACHE['value']
    import sys as _s, importlib
    _s.path.insert(0, str(BASE / 'scripts'))
    import painel_prioridade as PP
    _recarregar_se_mudou(PP); PP._c.clear()
    value = PP.montar(api_prioridade(1))
    _PAINEL_PRIORIDADE_CACHE.update(ts=time.time(), value=value)
    try: (BASE / 'docs' / '.cache-painel-prioridade.json').write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    except Exception: pass
    return value

api_painel_prioridade = api_painel_prioridade_calc
_PAINEL_LOCK = threading.Lock()
def _painel_atualizar_bg():
    """Recalcula o painel em segundo plano (no máximo uma vez por vez)."""
    if not _PAINEL_LOCK.acquire(blocking=False): return
    def _w():
        try: api_painel_prioridade_calc()
        except Exception: pass
        finally: _PAINEL_LOCK.release()
    threading.Thread(target=_w, daemon=True).start()

def api_painel_prioridade_rapido():
    """Responde na hora com o último painel calculado (memória ou disco) e atualiza em segundo plano quando passou de 30 s.
    Só a primeira vez, sem nenhum cálculo anterior, espera o cálculo."""
    v = _PAINEL_PRIORIDADE_CACHE['value']
    if v is None:
        try:
            v = json.loads((BASE / 'docs' / '.cache-painel-prioridade.json').read_text(encoding='utf-8'))
            _PAINEL_PRIORIDADE_CACHE.update(ts=0, value=v)
        except Exception: v = None
    if v is None: return api_painel_prioridade_calc()
    if time.time() - _PAINEL_PRIORIDADE_CACHE['ts'] >= 30: _painel_atualizar_bg()
    return v

def api_tec_indice():
    p = BASE / 'docs' / 'tecconcursos-cgu-2026-indice.json'
    try: return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: return {'erro': 'índice externo ainda não persistido', 'detalhe': str(e)}

def api_tec_cadernos():
    p = BASE / 'docs' / 'tec-cadernos.json'
    try: return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: return {'erro': 'docs/tec-cadernos.json ausente', 'detalhe': str(e)}

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

def api_aula_estado(q):
    """Retorna as respostas já registradas para todos os itens de uma aula (para restaurar o estado ao recarregar)."""
    dir_aula = q.get('dir', [''])[0]
    if not dir_aula:
        return {'erro': 'dir obrigatório'}
    # Coleta todas as chaves dos cadernos desta aula
    aula_path = AUL / dir_aula
    ks = set()
    for assoc in aula_path.glob('associacao.json'):
        try:
            a = json.loads(assoc.read_text(encoding='utf-8'))
            for cad_itens in a.values():
                for item in cad_itens:
                    ks.add(item if isinstance(item, str) else item.get('k', ''))
        except Exception:
            pass
    # Lê o manifest para pegar as chaves dos cadernos pela estrutura do plano
    man_path = aula_path / 'manifest.json'
    cadernos_set = set()
    if man_path.exists():
        try:
            man = json.loads(man_path.read_text(encoding='utf-8'))
            for a in man.get('aulas', [man]):
                for cad_nome, cad_itens in a.get('cadernos', {}).items():
                    cadernos_set.add(cad_nome)
                    for item in cad_itens:
                        ks.add(item if isinstance(item, str) else item.get('k', ''))
        except Exception:
            pass
    if not ks:
        # Tenta via plano
        for f, P in planos():
            # Verifica se este plano pertence a esta aula pelo dir
            try:
                rel = str(f.parent.relative_to(AUL)).replace('\\', '/')
            except Exception:
                continue
            if rel.startswith(dir_aula.split('/')[0]):
                for a in P.get('aulas', []):
                    for cad_nome, cad_itens in a.get('cadernos', {}).items():
                        cadernos_set.add(cad_nome)
                        for item in cad_itens:
                            ks.add(item if isinstance(item, str) else item.get('k', ''))
    if not ks:
        return {'feitos': {}, 'respostas': {}}
    c = db()
    # Pega a última resposta de cada item
    rows = c.execute(
        'SELECT k, caderno, resposta, correta, id, motivo, motivo_detalhe FROM respostas WHERE k IN (%s) ORDER BY id' % ','.join('?' * len(ks)),
        list(ks)
    ).fetchall()
    c.close()
    # Por caderno: quais itens foram respondidos e todos foram enviados?
    por_caderno = {}
    respostas = {}
    for r in rows:
        respostas[r['k']] = {'resposta': r['resposta'], 'correta': r['correta'], 'id': r['id'], 'motivo': r['motivo'], 'motivo_detalhe': r['motivo_detalhe']}
        cad = r['caderno'] or ''
        por_caderno.setdefault(cad, set()).add(r['k'])
    # Um caderno é considerado "feito" se pelo menos 1 item foi respondido nele
    feitos = {cad: list(ks_cad) for cad, ks_cad in por_caderno.items() if cad}
    return {'feitos': feitos, 'respostas': respostas}

def api_recomendacao_aula(q):
    """Dado um k de item, retorna aulas que ensinam o núcleo daquele item.
    Retorna lista de {titulo, curto, dir, url_aula, url_pdf, num, tema, topico_edital, nucleos_ensinados}.
    Se o núcleo não tiver aula ainda, retorna lista vazia com sugestao de tópico.
    """
    k = (q.get('k') or [''])[0]
    if not k:
        return {'erro': 'k obrigatório', 'aulas': []}

    # Encontra o item no banco para pegar núcleo e edital
    g = gabarito_de(k)
    if not g:
        return {'erro': 'item não encontrado', 'aulas': []}

    nucleo_id = g.get('nucleo') or ''
    edital_cod = g.get('edital') or ''
    nt = nucleos()
    nucleo_texto = (nt.get(nucleo_id) or {}).get('texto') or nucleo_id

    # Varre manifests de aulas para achar quais ensinam este núcleo
    out = []
    seen = set()
    for man_path in sorted(AUL.glob('*/aula*/manifest.json')):
        try:
            j = json.loads(man_path.read_text(encoding='utf-8'))
        except Exception:
            continue
        ensina = set(j.get('ensina') or j.get('nucleos') or [])
        if nucleo_id not in ensina:
            continue
        d_aula = man_path.parent
        rel = str(d_aula.relative_to(AUL)).replace('\\', '/')
        if rel in seen:
            continue
        seen.add(rel)
        tit = j.get('titulo') or d_aula.name
        curto = re.sub(r'\s*\([^)]*\)\s*$', '', re.sub(r'^Aula\s*\d+\s*[–-]\s*', '', tit))
        nuc_textos = [(nt.get(n, {}).get('texto') or n) for n in ensina]
        out.append({
            'titulo': tit,
            'curto': curto,
            'num': j.get('aula'),
            'tema': j.get('tema', ''),
            'dir': rel,
            'url_aula': '/aula/' + '/'.join(rel.split('/')),
            'url_pdf': '/aula-pdf/' + '/'.join(rel.split('/')) if (d_aula / 'aula.pdf').exists() else None,
            'nucleos_ensinados': nuc_textos,
        })

    return {
        'nucleo_id': nucleo_id,
        'nucleo_texto': nucleo_texto,
        'edital': edital_cod,
        'aulas': out,
        'sem_aula': len(out) == 0,
    }

def api_registrar_acesso(d):
    """Salva o último URL/título acessado para permitir retomada."""
    url = d.get('url', '')
    titulo = d.get('titulo', '')
    if not url:
        return {'erro': 'url obrigatório'}
    ts = datetime.datetime.now().isoformat(timespec='seconds')
    with LOCK:
        c = db()
        c.execute('INSERT OR REPLACE INTO ultimo_acesso(id, url, titulo, ts) VALUES(1,?,?,?)', (url, titulo, ts))
        c.commit(); c.close()
    return {'ok': True}

def api_retomar():
    """Retorna o último local acessado pelo usuário."""
    c = db()
    row = c.execute('SELECT url, titulo, ts FROM ultimo_acesso WHERE id=1').fetchone()
    c.close()
    if not row:
        return {'url': None, 'titulo': None, 'ts': None}
    return {'url': row['url'], 'titulo': row['titulo'], 'ts': row['ts']}

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

def _txt(h): return re.sub(r'\W+', '', html_mod.unescape(re.sub(r'<[^>]+>', '', h))).lower()

def _interativo(corpo, man):
    """Torna interativos os itens do caderno que aparecem no corpo da aula: casa cada bloco com o item do banco pelo enunciado
    (nada do gabarito vai para a página antes do envio)."""
    banco(); idx = _cache['idx']; por = {}
    for nome, ks in (man.get('cadernos') or {}).items():
        for k in ks: por.setdefault(k, str(nome))
    for k in man.get('itens') or []: por.setdefault(k, 'revisao')
    pref = {}
    for k, nome in por.items():
        x = idx.get(k)
        if x: pref[_txt(limpar(x['enunciado']))[:70]] = (nome, k)
    achados = []
    def rep(m):
        b = m.group(0); p = re.search(r'<p>(.*?)</p>', b, re.S)
        if not p: return b
        hit = pref.get(_txt(p.group(1))[:70])
        if not hit: return b
        nome, k = hit; achados.append(k); n = len(achados)
        bt = '<div class="resp" data-n="%d"><button type="button" data-r="C">Certo</button><button type="button" data-r="E">Errado</button><button type="button" data-r="B">Em branco</button></div><div class="fb"></div>' % n
        b = b.replace('<div class="q">', '<div class="q" data-k="%s" data-c="%s" data-n="%d">' % (html_mod.escape(k, True), html_mod.escape(nome, True), n), 1)
        return b.replace('<div class="meta">', bt + '<div class="meta">', 1)
    corpo = re.sub(r'<div class="q">.*?</div></div>', rep, corpo, flags=re.S)
    if not achados: return corpo, {}
    com = {}
    m = re.search(r'<div class="pg"([^>]*)>(\s*)<h2>([^<]*Gabarito comentado[^<]*)</h2>', corpo)
    if m:
        sec = corpo[m.start():]
        for pm in re.finditer(r'<p><b>(\d+)\s*[—–-]\s*<span class="(?:cert|err)">(?:Certo|Errado)</span>\.</b>(.*?)</p>', sec, re.S):
            n = int(pm.group(1))
            if 1 <= n <= len(achados): com[achados[n - 1]] = pm.group(2).strip()
        corpo = corpo[:m.start()] + '<div class="pg" id="gabsec"%s style="display:none">%s<h2>%s</h2>' % (m.group(1), m.group(2), m.group(3)) + corpo[m.end():]
    return corpo, com

TOC_JS = r'''<nav id="toc" aria-label="Índice da aula"><div class="tt"><span>Índice da aula</span><button id="tocx" title="Recolher">‹</button></div><div class="pb"><i></i></div><div class="pc"></div><div id="toclist"></div></nav><button id="tocbtn">☰ Índice</button><script>
(function(){
var KEY='toc:'+location.pathname,vistos={};try{vistos=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
var H=[].slice.call(document.querySelectorAll('h2,h3')).filter(function(h){return !h.closest('.q,.ped,.box,.barra')});
var cur=null,itens=[],list=document.getElementById('toclist');
H.forEach(function(h,i){h.id=h.id||'sec-'+i;var l2=h.tagName==='H3';var a=document.createElement('a');a.className=l2?'l2':'l1';a.textContent=h.textContent.replace(/^\s*\d+\.\s*/,function(m){return m});a.href='#'+h.id;a.dataset.i=i;
  a.onclick=function(ev){ev.preventDefault();h.scrollIntoView({behavior:'smooth',block:'start'});if(innerWidth<=1180)fechar()};
  list.appendChild(a);itens.push({h:h,a:a,pai:l2?cur:null,l2:l2});if(!l2)cur=itens[itens.length-1]});
var body=document.body;
function abrir(){body.classList.add('toc-on');body.classList.remove('toc-off')}
function fechar(){body.classList.remove('toc-on');body.classList.add('toc-off')}
(innerWidth>1180)?abrir():fechar();
document.getElementById('tocx').onclick=fechar;document.getElementById('tocbtn').onclick=abrir;
var tick=false;
function atualiza(){tick=false;var y=innerHeight*0.28,ativo=0;
  itens.forEach(function(it,i){var oc=it.h.offsetParent===null;it.a.classList.toggle('oculto',oc);if(!oc&&it.h.getBoundingClientRect().top<=y)ativo=i});
  var A=itens[ativo],paiA=A.l2?A.pai:A;
  itens.forEach(function(it,i){var on=(i===ativo);it.a.classList.toggle('ativo',on);
    if(it.l2)it.a.classList.toggle('vis',it.pai===paiA);
    if(i<ativo&&!it.l2&&!vistos[it.h.id]){vistos[it.h.id]=1}
    it.a.classList.toggle('visto',!it.l2&&!!vistos[it.h.id]&&it!==paiA);it.a.classList.toggle('atual',it===paiA&&!on)});
  try{localStorage.setItem(KEY,JSON.stringify(vistos))}catch(e){}
  var max=document.documentElement.scrollHeight-innerHeight,p=max>0?Math.min(100,Math.round(100*scrollY/max)):0;
  document.querySelector('#toc .pb i').style.width=p+'%';
  var n1=itens.filter(function(i){return !i.l2&&!i.a.classList.contains('oculto')});
  document.querySelector('#toc .pc').textContent=p+'% da aula · seção '+(n1.indexOf(paiA)+1)+' de '+n1.length;
  var ac=document.querySelector('#toc a.ativo');if(ac){var r=ac.getBoundingClientRect(),t=document.getElementById('toc').getBoundingClientRect();if(r.top<t.top+40||r.bottom>t.bottom-20)ac.scrollIntoView({block:'center'})}}
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(atualiza)}},{passive:true});addEventListener('resize',atualiza);atualiza();
})();</script>'''

GLOS_JS = r'''<div id="sgtip" role="tooltip"></div><script>
(function(){
var G=__GLOS__,keys=Object.keys(G).sort(function(a,b){return b.length-a.length});if(!keys.length)return;
function esc(k){return k.replace(/[.*+?^${}()|[\]\\\/-]/g,'\\$&')}
var re=new RegExp('(^|[^A-Za-z0-9_À-ÿ])('+keys.map(esc).join('|')+')(?![A-Za-z0-9_À-ÿ])','g');
var tip=document.getElementById('sgtip');
function skip(n){for(var e=n.parentNode;e&&e!==document.body;e=e.parentNode){var t=e.tagName;if(t==='SCRIPT'||t==='STYLE'||t==='svg'||t==='SVG'||t==='TEXTAREA'||e.id==='toc'||e.id==='sgtip'||e.id==='tocbtn'||e.classList&&(e.classList.contains('sg')||e.classList.contains('versao-aula')||e.classList.contains('barra')))return true}return false}
var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null),nodes=[],n;while(n=w.nextNode()){if(n.nodeValue.trim()&&!skip(n))nodes.push(n)}
nodes.forEach(function(n){var t=n.nodeValue;re.lastIndex=0;if(!re.test(t))return;re.lastIndex=0;var f=document.createDocumentFragment(),i=0,m;
  while((m=re.exec(t))){var ini=m.index+m[1].length;f.appendChild(document.createTextNode(t.slice(i,ini)));var s=document.createElement('span');s.className='sg';s.dataset.g=m[2];s.tabIndex=0;s.textContent=m[2];f.appendChild(s);i=ini+m[2].length}
  f.appendChild(document.createTextNode(t.slice(i)));n.parentNode.replaceChild(f,n)});
document.querySelectorAll('svg text').forEach(function(t){re.lastIndex=0;var x=' '+t.textContent,ks=[],m;while((m=re.exec(x)))ks.push(m[2]);if(ks.length){t.classList.add('sgv');t.dataset.g=ks.filter(function(k,i){return ks.indexOf(k)===i}).join('|')}});
function html(ks){return ks.map(function(k){var g=G[k];return '<div class="sgi"><b>'+k+'</b> · '+g.nome+(g.def?'<div class="sgd">'+g.def+'</div>':'')+'</div>'}).join('')}
function mostra(el){var ks=(el.dataset.g||'').split('|').filter(function(k){return G[k]});if(!ks.length)return;tip.innerHTML=html(ks);tip.style.display='block';
  var r=el.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight,x=Math.max(8,Math.min(r.left+r.width/2-tw/2,innerWidth-tw-8)),y=r.top-th-8;if(y<8)y=r.bottom+8;tip.style.left=x+'px';tip.style.top=y+'px'}
function esconde(){tip.style.display='none'}
document.addEventListener('mouseover',function(e){var el=e.target.closest&&e.target.closest('.sg,svg text.sgv');if(el)mostra(el)});
document.addEventListener('mouseout',function(e){var el=e.target.closest&&e.target.closest('.sg,svg text.sgv');if(el)esconde()});
document.addEventListener('focusin',function(e){if(e.target.classList&&e.target.classList.contains('sg'))mostra(e.target)});
document.addEventListener('focusout',esconde);addEventListener('scroll',esconde,{passive:true});
document.addEventListener('click',function(e){var el=e.target.closest&&e.target.closest('.sg');if(el){mostra(el)}else if(!e.target.closest('#sgtip'))esconde()});
})();</script>'''

def pagina_aula(rel, modo='teoria', caderno=None, acao=''):
    d = (AUL / rel).resolve()
    if AUL.resolve() not in d.parents: return None
    corpo = d / 'corpo.html'
    if not corpo.exists(): return None
    css = (AUL / '_template' / 'dark.css').read_text(encoding='utf-8')
    man = json.loads((d / 'manifest.json').read_text(encoding='utf-8')); titulo = man.get('titulo', 'Aula')
    numero = man.get('aula') or re.sub(r'\D', '', d.name) or '?'
    versao = man.get('versao', 1)
    versao_app = (APP / 'versao.txt').read_text(encoding='utf-8').strip()
    identificacao = 'App v%s · Aula %s · conteúdo v%s' % (versao_app, numero, versao)
    titulo_doc = '%s · App v%s · conteúdo v%s' % (titulo, versao_app, versao)
    fonte = corpo.read_text(encoding='utf-8')
    divisao = re.search(r'(?:<div class="pg"[^>]*>\s*)?<h2>[^<]*Caderno de quest[õo]es[^<]*</h2>', fonte, re.I)
    if divisao:
        fonte = fonte[divisao.start():] if modo == 'questoes' else fonte[:divisao.start()]
        if not divisao.group(0).startswith('<div'):
            fonte = '<div class="pg">' + fonte if modo == 'questoes' else fonte + '</div>'
    corpo_h, com = _interativo(fonte, man)
    cads = man.get('cadernos') or {}
    if modo == 'questoes' and cads:
        destino_cad = '/aula/' + str(rel).strip('/') + '?modo=questoes'
        esc = lambda v: html_mod.escape(str(v), quote=True)
        if caderno is not None and caderno not in cads:
            return None
        banco()
        historico = ultimas(db())
        # Abrir um caderno com histórico leva à consulta do mesmo retrato
        # usado pelos cartões; nova tentativa é sempre uma ação explícita.
        if caderno is not None and not acao and any(k in historico for k in cads[caderno]):
            acao = 'consultar'
        cards = []
        for nome, chaves in cads.items():
            feitas = sum(k in historico for k in chaves)
            acertos = sum(k in historico and historico[k]['correta'] == 1 for k in chaves)
            erros = sum(k in historico and historico[k]['correta'] == 0 for k in chaves)
            brancos = feitas - acertos - erros
            total = len(chaves)
            percentual = round(100 * feitas / total) if total else 0
            status = 'Não iniciado' if not feitas else ('Concluído' if feitas == total else 'Em andamento')
            rotulo_acao = 'Refazer' if feitas and feitas == total else ('Continuar' if feitas else 'Começar')
            link = destino_cad + '&caderno=' + esc(nome)
            consulta = '<p><a href="%s&acao=consultar">Consultar respostas e gabarito comentado</a> · <a href="%s&acao=refazer">Refazer caderno</a></p>' % (link, link) if feitas else ''
            pdf = '<a href="/aula-pdf/%s/caderno%s.pdf">PDF</a>' % (esc(str(rel).strip('/')), esc(nome)) if (d / ('caderno%s.pdf' % nome)).exists() else ''
            cards.append('<section class="caderno-progresso" style="padding:16px;border:1px solid #30363d;border-radius:10px;margin:12px 0"><h3>Caderno %s%s</h3><p><b>%s</b> · %s de %s questões respondidas (%s%%)</p><progress value="%s" max="%s" aria-label="Progresso do caderno %s" style="width:100%%;accent-color:#3fb950"></progress><p><span style="color:#3fb950">%s acertos</span> · <span style="color:#f85149">%s erros</span> · %s em branco · <b>%s pendentes</b></p><a href="%s">%s caderno %s →</a> %s</section>' % (esc(nome), ' · selecionado' if nome == caderno else '', status, feitas, total, percentual, feitas, max(total, 1), esc(nome), acertos, erros, brancos, total - feitas, link, rotulo_acao, esc(nome), pdf))
            cards[-1] += consulta
        chaves_aula = {k for ks in cads.values() for k in ks}
        total_feitas = sum(k in historico for k in chaves_aula)
        lista = '<div class="pg"><h2>Cadernos desta aula</h2><p><b>Progresso da aula: %s de %s questões respondidas.</b></p><p class="small">Considera a última resposta registrada em cada questão, inclusive em outros treinos. Em branco conta como respondida.</p>' % (total_feitas, len(chaves_aula)) + ''.join(cards) + '</div>'
        corpo_h, com = lista, {}
        if caderno is not None:
            questoes = []
            selecionadas = cads[caderno]
            ac = sum(k in historico and historico[k]['correta'] == 1 for k in selecionadas)
            er = sum(k in historico and historico[k]['correta'] == 0 for k in selecionadas)
            resumo_consulta = '<p role="status"><b>Resultado registrado: %s acerto%s · %s erro%s</b></p>' % (ac, '' if ac == 1 else 's', er, '' if er == 1 else 's') if acao == 'consultar' else ''
            for n, k in enumerate(cads[caderno], 1):
                x = _cache['idx'].get(k)
                if not x:
                    questoes.append('<p>Questão %s indisponível no banco.</p>' % n)
                    continue
                com[k] = comentario(x)
                if acao == 'consultar':
                    anterior = historico.get(k)
                    resultado = ('Você acertou' if anterior['correta'] == 1 else 'Você errou' if anterior['correta'] == 0 else 'Em branco') if anterior else 'Ainda não respondida'
                    resposta = {'C': 'Certo', 'E': 'Errado', 'B': 'Em branco'}.get(anterior['resposta'], 'Em branco') if anterior else '—'
                    gab = 'Certo' if x['gabarito'] == 'C' else 'Errado'
                    classe_resultado = 'resultado-correto' if anterior and anterior['correta'] == 1 else ('resultado-errado' if anterior and anterior['correta'] == 0 else ('resultado-branco' if anterior else 'resultado-pendente'))
                    questoes.append('<section class="q %s"><h3>Questão %s · %s</h3><p>%s</p><p>Sua resposta: <b>%s</b> · Gabarito: <b>%s</b></p><div><b>Gabarito comentado</b><p>%s</p></div></section>' % (classe_resultado, n, resultado, esc(limpar(x['enunciado'])), resposta, gab, esc(com[k])))
                    continue
                questoes.append('<div class="q" data-k="%s" data-c="%s" data-n="%s"><span class="tag">%s</span><p>%s</p><div class="resp"><button type="button" data-r="C">Certo</button><button type="button" data-r="E">Errado</button><button type="button" data-r="B">Em branco</button></div><div class="fb"></div><div class="rec-aula"></div></div>' % (esc(k), esc(caderno), n, n, esc(limpar(x['enunciado']))))
            corpo_h = '<div class="pg"><p><a href="%s">← Todos os cadernos</a></p><h2>Caderno %s</h2>%s%s</div>' % (esc(destino_cad), esc(caderno), resumo_consulta, ''.join(questoes)) + lista
    if divisao or cads:
        destino = '/aula/' + str(rel).strip('/')
        destino = html_mod.escape(destino, True)
        teoria_ativa = ' aria-current="page"' if modo != 'questoes' else ''
        questoes_ativas = ' aria-current="page"' if modo == 'questoes' else ''
        navegacao = ('<nav class="material-nav" aria-label="Material da aula">'
                     '<a href="%s"%s>📖 Aula teórica</a>'
                     '<a href="%s?modo=questoes"%s>✍ Caderno de questões</a></nav>'
                     % (destino, teoria_ativa, destino, questoes_ativas))
        proximo = (destino, 'Voltar à aula teórica') if modo == 'questoes' else (destino + '?modo=questoes', 'Praticar no caderno de questões →')
        corpo_h = navegacao + corpo_h + '<div class="material-proximo"><a href="%s">%s</a></div>' % proximo
        titulo_doc = ('Caderno de questões · ' if modo == 'questoes' else '') + titulo_doc
    # A rota limpa termina em "aulaN" sem barra final. Nesse caso, um src
    # relativo como "sketches/x.png" subiria para a pasta do tema. Reescreva
    # apenas esses caminhos na versão servida pelo navegador; o corpo.html
    # continua relativo para que o renderizador local do PDF funcione.
    aula_url = '/aula/' + str(rel).strip('/') + '/'
    corpo_h = corpo_h.replace('src="sketches/', 'src="' + aula_url + 'sketches/')
    glos = {}
    for gf in (AUL / '_template' / 'glossario.json', d / 'glossario.json'):
        try: glos.update(json.loads(gf.read_text(encoding='utf-8')))
        except Exception: pass
    glos_js = GLOS_JS.replace('__GLOS__', json.dumps(glos, ensure_ascii=False).replace('</', '<\\/'))
    extra = '''html,body{background:#0f1419}.pg{max-width:880px;margin:0 auto 24px;padding:24px 22px}.cover{height:auto!important}
    body{padding-bottom:90px}
    .material-nav{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:8px;padding:8px;background:#161b22;border:1px solid #58a6ff;border-radius:12px;box-shadow:0 4px 20px #0009;max-width:calc(100vw - 24px);box-sizing:border-box}
    .material-nav a,.material-proximo a{display:block;background:#21262d;color:#fff;text-decoration:none;padding:12px 16px;border-radius:8px;font:600 14px/1.4 sans-serif;text-align:center}
    .material-nav a[aria-current="page"]{background:#1f6feb}
    .material-nav a:hover,.material-proximo a:hover{background:#238636}
    .material-nav a:focus-visible,.material-proximo a:focus-visible{outline:3px solid #fff;outline-offset:2px}
    .material-proximo{max-width:880px;margin:24px auto;padding:0 22px}.material-proximo a{background:#238636}
    #lida{position:fixed;right:16px;top:12px;background:#238636;color:#fff;border:0;border-radius:8px;padding:10px 16px;font:600 14px sans-serif;cursor:pointer;z-index:5}
    .versao-aula{position:fixed;left:16px;top:12px;z-index:5;background:#1f6feb;color:#fff;border:1px solid #58a6ff;border-radius:8px;padding:8px 12px;font:700 13px sans-serif;box-shadow:0 4px 16px #0008}

    h2,h3{scroll-margin-top:18px}
    #toc{position:fixed;left:0;top:54px;bottom:0;width:262px;overflow-y:auto;background:#0d1117;border-right:1px solid #30363d;padding:10px 8px 24px;z-index:4;font:13px/1.35 sans-serif;transition:transform .2s}
    #toc .tt{display:flex;align-items:center;justify-content:space-between;color:#8b949e;font:700 11px sans-serif;letter-spacing:.06em;text-transform:uppercase;margin:0 4px 6px}
    #toc .tt button{background:none;border:1px solid #30363d;color:#8b949e;border-radius:6px;cursor:pointer;padding:2px 8px;font-size:12px}
    #toc .pb{height:4px;background:#21262d;border-radius:2px;margin:0 4px 10px;overflow:hidden}#toc .pb i{display:block;height:100%;width:0;background:#3fb950;transition:width .15s}
    #toc .pc{color:#8b949e;font-size:11px;margin:0 4px 8px}
    #toc a{display:block;color:#c9d1d9;text-decoration:none;border-radius:6px;padding:5px 8px;margin:1px 0;border-left:3px solid transparent;cursor:pointer}
    #toc a:hover{background:#161b22}#toc a.l2{padding-left:20px;font-size:12px;color:#8b949e;display:none}#toc a.l2.vis{display:block}
    #toc a.ativo{background:#1f6feb26;border-left-color:#58a6ff;color:#fff;font-weight:700}#toc a.l2.ativo{font-weight:600}
    #toc a.atual{color:#fff;font-weight:700;border-left-color:#58a6ff}
    #toc a.oculto{display:none!important}
    #toc a.visto::after{content:" ✓";color:#3fb950;font-weight:700}
    #tocbtn{position:fixed;left:16px;top:54px;z-index:5;background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:8px;padding:7px 11px;font:700 13px sans-serif;cursor:pointer;display:none}
    body.toc-on{padding-left:262px}body.toc-off #toc{transform:translateX(-270px)}body.toc-off #tocbtn{display:block}
    @media(max-width:1180px){body.toc-on{padding-left:0}body.toc-on #toc{box-shadow:6px 0 24px #000c}}
    .resp{display:flex;gap:8px;margin:8px 0}.resp button{flex:1;background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:8px;padding:9px 6px;font:600 14px sans-serif;cursor:pointer}
    .resp button:hover{border-color:#58a6ff}.resp button.on{background:#1f6feb;border-color:#58a6ff;color:#fff}.resp button.on[data-r=B]{background:#6e7681;border-color:#8b949e}
    .q.ok{border-color:#3fb950!important}.q.no{border-color:#f85149!important}.fb{display:none;margin-top:8px;padding:8px 10px;border-radius:6px;background:#0d1117;font-size:13px;line-height:1.5}
    /* Cores do título indicam o resultado registrado, sem confundir o tema padrão verde dos h3 com acerto. */
    .q.ok>h3,.q.resultado-correto>h3{color:#3fb950!important}
    .q.no>h3,.q.resultado-errado>h3{color:#f85149!important}
    .q.resultado-branco>h3{color:#d29922!important}
    .q.resultado-pendente>h3{color:#e6edf3!important}
    .diag-aula{border-left:4px solid #d29922!important}.diag-aula .chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
    .diag-aula .chip{background:#21262d;color:#c9d1d9;border:1px solid #484f58;border-radius:14px;padding:5px 11px;cursor:pointer}
    .diag-aula .chip:hover,.diag-aula .chip.on{background:#1f6feb;color:#fff;border-color:#58a6ff}
    .diag-aula .diag-detalhe{background:#0d1117;color:#e6edf3;border:1px solid #30363d;border-radius:6px;padding:8px;font:inherit}
    /* O resultado do caderno fica no fluxo normal: não pode cobrir as últimas questões. */
    .barra{position:relative;z-index:1;background:#161b22;border:1px solid #58a6ff;border-radius:10px;padding:12px 14px;margin:14px 0;box-shadow:0 4px 18px #0006}
    .barra button{background:#238636;color:#fff;border:0;border-radius:8px;padding:10px 18px;font:700 14px sans-serif;cursor:pointer}.barra button.s{background:#21262d;border:1px solid #30363d}.barra button:disabled{opacity:.5;cursor:not-allowed}
    .res{margin-top:10px;font-size:14px;line-height:1.6}.res .g{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0}.res .g span{background:#0d1117;border-radius:8px;padding:8px 14px;font-size:13px}.res .g b{font-size:22px;display:block}
    .sg{border-bottom:1px dotted #6e7681;cursor:help;text-decoration:none}.sg:hover,.sg:focus{border-bottom-color:#58a6ff;color:#79c0ff;outline:0;background:#1f6feb22}
    svg text.sgv{cursor:help}
    #sgtip{position:fixed;display:none;z-index:50;max-width:360px;background:#0d1117;border:1px solid #58a6ff;border-radius:8px;padding:9px 12px;color:#e6edf3;font:13px/1.4 sans-serif;box-shadow:0 8px 28px #000c;pointer-events:none}
    #sgtip .sgi+.sgi{border-top:1px solid #30363d;margin-top:6px;padding-top:6px}#sgtip b{color:#58a6ff}#sgtip .sgd{color:#8b949e;font-size:12px;margin-top:2px}
    /* +2px em toda a hierarquia de texto da aula (somente na tela; o PDF segue o dark.css) */
    body{font-size:14.67px}h1{font-size:35.3px}h2{font-size:22px}h3{font-size:17.33px}
    table{font-size:14.8px}code,.c{font-size:14.53px}pre{font-size:14px}.cap{font-size:13.47px}.tag{font-size:13.07px}.meta{font-size:13.2px}.small{font-size:14px}
    .cover h1{font-size:44.7px!important}.cover p{font-size:19.3px!important}
    .ped b.t{font-size:15.6px}.ped summary,.ped table,.ped .dica{font-size:14px}.ped .ajuda{font-size:12.67px}
    .fb{font-size:15px!important}.res{font-size:16px}.res .g span{font-size:15px}.resp button{font-size:16px}
    body.toc-on{padding-left:262px}body.toc-off #toc{transform:translateX(-270px)}
    @media(max-width:1180px){body.toc-on{padding-left:0}}'''
    js = '''<button id="lida">Marcar aula como lida</button><script>
    // Registra acesso para permitir retomada
    (function(){const url=location.pathname;const titulo=document.title.split(' · ')[0];fetch('/api/registrar-acesso',{method:'POST',body:JSON.stringify({url,titulo})}).catch(()=>{});})();
    document.getElementById('lida').onclick=async()=>{await fetch('/api/aula-lida',{method:'POST',body:JSON.stringify({aula:'aula|%s',lida:true})});document.getElementById('lida').textContent='Lida ✔'};
    const COM=%s;const MOTIVOS=%s;
    function escapeDiag(s){return String(s||'').replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
    function blocoDiagnostico(id,k,branco){
      const titulo=branco?'O que impediu a resposta?':'O que mais contribuiu para o erro?';
      const botoes=MOTIVOS.map(function(x){return '<button type="button" class="chip" data-motivo="'+escapeDiag(x[0])+'">'+escapeDiag(x[1])+'</button>'}).join('');
      const html='<div class="diag-aula q" id="diag-aula-'+id+'" style="margin-top:10px"><b>'+titulo+'</b><p class="muted">Escolha a causa para receber uma orientação e um conteúdo adequados. A resposta fica salva no histórico.</p><div class="chips">'+botoes+'</div><textarea class="diag-detalhe" rows="2" maxlength="500" placeholder="Se quiser, conte um pouco mais (opcional)" style="width:100%;box-sizing:border-box;margin-top:6px"></textarea><div class="diag-status muted"></div><div class="diag-recomendacao"></div></div>';
      setTimeout(function(){const w=document.getElementById('diag-aula-'+id);if(w)w.querySelectorAll('[data-motivo]').forEach(function(b){b.onclick=function(){diagnosticarAula(id,k,b.dataset.motivo,b)}})},0);
      return html
    }
    async function diagnosticarAula(id,k,motivo,el){
      const w=el.closest('.diag-aula'),st=w.querySelector('.diag-status'),dest=w.querySelector('.diag-recomendacao');st.textContent='Registrando e preparando a recomendação…';
      try{const r=await(await fetch('/api/diagnostico',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id,k:k,motivo:motivo,detalhe:w.querySelector('.diag-detalhe').value})})).json();if(r.erro){st.textContent=r.erro;return}
        w.querySelectorAll('[data-motivo]').forEach(function(b){b.classList.toggle('on',b===el)});st.textContent='Registrado: '+r.rotulo+' ✔';const x=r.recomendacao||{},aulas=x.aulas||[];
        const links=aulas.map(function(a){return '<p><a href="'+escapeDiag(a.url_aula)+'" target="_blank">📖 Abrir aula '+(a.num||'')+': '+escapeDiag(a.curto||a.titulo)+'</a>'+(a.url_pdf?' · <a href="'+escapeDiag(a.url_pdf)+'" target="_blank">PDF</a>':'')+'</p>'}).join('');
        dest.innerHTML='<div class="q" style="margin-top:8px;border-color:#58a6ff"><b>'+escapeDiag(x.titulo||'Próximo passo recomendado')+'</b><p>'+escapeDiag(x.orientacao||'')+'</p><p><b>Depois:</b> '+escapeDiag(x.proximo_passo||'')+'</p><p class="muted">Núcleo: '+escapeDiag(x.nucleo_texto||k)+'</p>'+(links||'<p class="muted">Ainda não há aula associada a este núcleo. Consulte a aba Aulas para localizar ou solicitar esse conteúdo.</p>')+'</div>'
      }catch(e){st.textContent='Não consegui salvar o diagnóstico. Tente novamente.'}
    }
    (function(){
    const Q=[...document.querySelectorAll('.q[data-k]')];if(!Q.length)return;const grupos={};Q.forEach(q=>(grupos[q.dataset.c]=grupos[q.dataset.c]||[]).push(q));
    const t0={};const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
    Q.forEach(q=>q.querySelectorAll('.resp button').forEach(b=>b.onclick=()=>{
      if(q.dataset.feito)return;
      const desmarcar=b.classList.contains('on');
      q.querySelectorAll('.resp button').forEach(x=>x.classList.remove('on'));
      if(desmarcar)delete q.dataset.r;
      else{b.classList.add('on');q.dataset.r=b.dataset.r;t0[q.dataset.c]=t0[q.dataset.c]||Date.now()}
      cont(q.dataset.c)
    }));
    function cont(c){const L=grupos[c],n=L.filter(q=>q.dataset.r).length;const bar=document.getElementById('bar-'+c);bar.querySelector('.cnt').textContent=n+' de '+L.length+' marcadas (as demais vão como em branco)'}
    Object.keys(grupos).forEach(c=>{const L=grupos[c],ult=L[L.length-1],bar=document.createElement('div');bar.className='barra';bar.id='bar-'+c;
      bar.innerHTML='<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap"><b>Caderno '+esc(c)+'</b><span class="cnt" style="color:#8b949e;font-size:13px"></span><span style="flex:1"></span><button class="env">Enviar prova</button></div><div class="res"></div>';
      ult.after(bar);cont(c);bar.querySelector('.env').onclick=()=>enviar(c,bar)});
    async function enviar(c,bar){const L=grupos[c];const btn=bar.querySelector('.env');btn.disabled=true;btn.textContent='Enviando…';const ms=Math.round((Date.now()-(t0[c]||Date.now()))/Math.max(1,L.length));let A=0,E=0,B=0;const acertou=[],errou=[],falhas=[];
      for(const q of L){const r=q.dataset.r||'B';let o;try{o=await (await fetch('/api/resposta',{method:'POST',body:JSON.stringify({k:q.dataset.k,resposta:r,ms:ms,caderno:c})})).json()}catch(e){o={erro:String(e)}}
        if(o.erro){falhas.push(q.dataset.n);continue}q.dataset.feito='1';q.querySelectorAll('.resp button').forEach(x=>x.disabled=true);
        const fb=q.querySelector('.fb');const g=o.gabarito==='C'?'Certo':'Errado',v=r==='C'?'Certo':r==='E'?'Errado':'em branco';
        if(o.correta===1){A++;q.classList.add('ok');acertou.push(o.nucleo_texto)}else if(o.correta===0){E++;q.classList.add('no');errou.push({n:q.dataset.n,t:o.nucleo_texto})}else B++;
        const cor=o.correta===1?'#3fb950':o.correta===0?'#f85149':'#8b949e';
        fb.style.display='block';fb.style.borderLeft='4px solid '+cor;fb.innerHTML='<b style="color:'+cor+'">'+(o.correta===1?'Você acertou':o.correta===0?'Você errou':'Em branco')+'</b> · você marcou: '+v+' · gabarito: <b>'+g+'</b><div style="margin-top:4px">'+(COM[q.dataset.k]||esc(o.comentario||''))+'</div>'+(o.correta===1?'':blocoDiagnostico(o.id,q.dataset.k,o.correta===null));
      const gs=document.getElementById('gabsec');if(gs)gs.style.display='block';
      const saldo=A-E;const res=bar.querySelector('.res');
      const fortes=[...new Set(acertou)],fracos=[...new Set(errou.map(x=>x.t))];
      res.innerHTML='<div class="g"><span style="color:#3fb950"><b>'+A+'</b>acertos</span><span style="color:#f85149"><b>'+E+'</b>erros</span><span style="color:#8b949e"><b>'+B+'</b>em branco</span><span><b style="color:'+(saldo>=0?'#58a6ff':'#f85149')+'">'+(saldo>0?'+':'')+saldo+'</b>saldo (erro anula acerto)</span><span><b>'+Math.round(100*A/L.length)+'%%</b>de acerto</span></div>'
       +(fracos.length?'<div><b style="color:#f85149">Onde você errou (revise):</b><ul style="margin:4px 0 4px 18px">'+errou.map(x=>'<li>Item '+x.n+': '+esc(x.t)+'</li>').join('')+'</ul></div>':'<div style="color:#3fb950"><b>Nenhum erro neste caderno.</b></div>')
       +(fortes.length?'<div><b style="color:#3fb950">Onde você foi bem:</b> '+fortes.map(esc).join('; ')+'</div>':'')
       +(falhas.length?'<div style="color:#d29922">Não consegui registrar os itens '+falhas.join(', ')+'. Confira se o app está rodando e envie de novo.</div>':'<div class="muted" style="color:#8b949e;margin-top:6px">Progresso registrado: veja na aba <a href="/#progresso" target="_blank" style="color:#58a6ff">Progresso</a>. O gabarito comentado da aula foi liberado mais abaixo.</div>')
       +'<div style="margin-top:8px"><button class="s" onclick="location.reload()">Refazer caderno</button></div>';
      btn.style.display='none';bar.scrollIntoView({block:'center',behavior:'smooth'})}

    async function carregarRecAula(k,el){
      try{
        const d=await(await fetch('/api/recomendacao-aula?k='+encodeURIComponent(k))).json();
        if(!d||!d.aulas)return;
        if(d.aulas.length===0){
          el.innerHTML='<div style="margin-top:8px;padding:10px 14px;border-left:3px solid #d29922;background:#1a1f26;border-radius:6px;font-size:13px"><b style="color:#d29922">📚 Revisar:</b> <span style="color:#8b949e">Nenhuma aula disponível para este tema ainda.</span></div>';
          el.style.display='block';return;
        }
        const nt=d.nucleo_texto||'';
        const links=d.aulas.map(a=>{
          const pdf=a.url_pdf?'<a href="'+a.url_pdf+'" target="_blank" style="color:#8b949e;font-size:12px;text-decoration:none;border:1px solid #30363d;padding:3px 8px;border-radius:5px">📄 PDF</a>':'';
          return '<div style="display:flex;align-items:center;gap:8px;margin-top:6px"><a href="'+a.url_aula+'" style="color:#58a6ff;font-size:13px;text-decoration:none">📖 '+(a.curto||a.titulo)+'</a>'+pdf+'</div>';
        }).join('');
        el.innerHTML='<div style="margin-top:8px;padding:10px 14px;border-left:3px solid #58a6ff;background:#0d1117;border-radius:6px"><div style="font-size:11px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Revisar conteúdo</div><div style="font-size:13px;color:#e6edf3;font-weight:600">'+nt+'</div>'+links+'</div>';
        el.style.display='block';
      }catch(e){}
    }
    })();
    // Restaurar cadernos já enviados ao recarregar a página
    (async function(){
      if(new URLSearchParams(location.search).get('acao')==='refazer')return;
      try{
        const dir=location.pathname.replace(/^\\/aula\\//,'').replace(/\\/$/,'');
        if(!dir)return;
        const st=await (await fetch('/api/aula-estado?dir='+encodeURIComponent(dir))).json();
        if(!st||!st.respostas)return;
        const resp=st.respostas;const feitos=st.feitos||{};
        // Para cada caderno que tem respostas, restaura as questões e mostra resultado resumido
        const Q=[...document.querySelectorAll('.q[data-k]')];if(!Q.length)return;
        const grupos={};Q.forEach(q=>(grupos[q.dataset.c]=grupos[q.dataset.c]||[]).push(q));
        const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
        for(const [c,ks] of Object.entries(feitos)){
          const L=grupos[c];if(!L||!L.length)continue;
          // Verifica se este caderno tem pelo menos 1 resposta registrada
          const temResp=L.some(q=>resp[q.dataset.k]);if(!temResp)continue;
          let A=0,E=0,B=0;
          L.forEach(q=>{
            const r=resp[q.dataset.k];if(!r)return;
            q.dataset.feito='1';q.dataset.r=r.resposta;
            q.querySelectorAll('.resp button').forEach(x=>{x.disabled=true;if(x.dataset.r===r.resposta)x.classList.add('on')});
            const fb=q.querySelector('.fb');if(!fb)return;
            const cor=r.correta===1?'#3fb950':r.correta===0?'#f85149':'#8b949e';
            const v=r.resposta==='C'?'Certo':r.resposta==='E'?'Errado':'em branco';
            fb.style.display='block';fb.style.borderLeft='4px solid '+cor;
            fb.innerHTML='<b style="color:'+cor+'">'+(r.correta===1?'Você acertou':r.correta===0?'Você errou':'Em branco')+'</b> · você marcou: '+v+(r.correta===1?'':(r.motivo?'<div class="muted">Motivo informado: '+esc((MOTIVOS.find(function(x){return x[0]===r.motivo})||[])[1]||r.motivo)+'</div>':blocoDiagnostico(r.id,q.dataset.k,r.correta===null)));
            if(r.correta===1)A++;else if(r.correta===0)E++;else B++;
            if(r.correta===1)q.classList.add('ok');else if(r.correta===0)q.classList.add('no');
          });
          // Adicionar barra de resultado restaurada
          const ult=L[L.length-1];
          if(!document.getElementById('bar-'+c)){
            const bar=document.createElement('div');bar.className='barra';bar.id='bar-'+c;
            const saldo=A-E;
            bar.innerHTML='<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap"><b>Caderno '+esc(c)+'</b><span style="color:#58a6ff;font-size:13px">↩ Resultado restaurado</span><span style="flex:1"></span></div>'
              +'<div class="res"><div class="g"><span style="color:#3fb950"><b>'+A+'</b>acertos</span><span style="color:#f85149"><b>'+E+'</b>erros</span><span style="color:#8b949e"><b>'+B+'</b>em branco</span><span><b style="color:'+(saldo>=0?'#58a6ff':'#f85149')+'">'+(saldo>0?'+':'')+saldo+'</b>saldo</span></div>'
              +'<div style="margin-top:8px;display:flex;gap:8px"><button class="s" onclick="location.reload()">Refazer</button>'
              +'<a href="/#progresso" style="display:inline-block;padding:9px 14px;background:#21262d;border:1px solid #30363d;border-radius:8px;color:#58a6ff;font:600 13px sans-serif;text-decoration:none">Ver progresso ↗</a>'
              +'</div></div>';
            ult.after(bar);
          }
        }
        // Avisa quantos cadernos foram restaurados
        const nFeitos=Object.keys(feitos).filter(c=>grupos[c]&&grupos[c].some(q=>resp[q.dataset.k])).length;
        if(nFeitos>0){
          const aviso=document.createElement('div');aviso.id='aviso-restauracao';
          aviso.style.cssText='background:#1f6feb22;border:1px solid #58a6ff55;border-radius:8px;padding:10px 14px;margin:12px 0;font-size:13px;color:#8b949e';
          aviso.innerHTML='↩ <b style="color:#58a6ff">'+nFeitos+(nFeitos>1?' cadernos já foram':' caderno já foi')+' restaurado'+(nFeitos>1?'s':'')+' do seu histórico.</b> Para refazer, clique em "Refazer" abaixo de cada caderno.';
          const primQ=document.querySelector('.q[data-k]');
          if(primQ){
            // Subir até filho direto de div.pg
            let el=primQ;while(el.parentNode&&el.parentNode.className!=='pg'&&el.parentNode.tagName!=='BODY')el=el.parentNode;
            const pgCont=el.parentNode;
            // Usar setTimeout para garantir que seja inserido após todos os scripts síncronos
            setTimeout(()=>{if(!document.getElementById('aviso-restauracao'))pgCont.insertBefore(aviso,el);},50);
          }
        }
      }catch(e){console.warn('Restauração falhou:',e)}
    })();
    </script>''' % (titulo.replace("'", "\\'"), json.dumps(com, ensure_ascii=False).replace('</', '<\\/'), json.dumps(list(MOTIVOS.items()), ensure_ascii=False).replace('</', '<\\/'))
    etiqueta = '<div class="versao-aula" aria-label="Versões do aplicativo e da aula">%s</div>' % html_mod.escape(identificacao)
    return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>%s</title><style>%s%s</style></head><body>%s%s%s</body></html>' % (html_mod.escape(titulo_doc), css, extra, etiqueta, corpo_h, js + TOC_JS + glos_js)

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
            rel = unquote(p[len('/aula/'):]).strip('/')
            # Aulas podem carregar imagens didáticas relativas à sua própria pasta.
            # Sirva somente arquivos de imagem dentro de AUL; o restante continua
            # seguindo para a rota HTML da aula.
            if rel.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                f = (AUL / rel).resolve()
                if AUL.resolve() in f.parents and f.exists() and f.is_file():
                    cts = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}
                    return self._b(f.read_bytes(), cts.get(f.suffix.lower(), 'application/octet-stream'))
                return self._j({'erro': 'imagem não encontrada'}, 404)
            q['dir'] = [rel]; p = '/aula'
        try:
            if p == '/': return self._b((APP / 'index.html').read_bytes(), 'text/html; charset=utf-8')
            if p == '/api/resumo': return self._j(api_resumo())
            if p == '/api/planos': return self._j(api_planos())
            if p == '/api/caderno': return self._j(api_refazer() if q.get('caderno', [''])[0] == 'R' else api_caderno(q))
            if p == '/api/progresso': return self._j(api_progresso())
            if p == '/api/revisao-adaptativa': return self._j(api_revisao_adaptativa())
            if p == '/api/prontidao': return self._j(api_prontidao())
            if p == '/api/banco': return self._j(api_banco(q))
            if p == '/api/aulas': return self._j(api_aulas())
            if p == '/api/cobertura': return self._j(api_cobertura())
            if p == '/api/revisoes': return self._j(api_revisoes())
            if p == '/api/doc': return self._j(api_doc())
            if p == '/api/painel-prioridade': return self._j(api_painel_prioridade_rapido())
            if p == '/api/prioridade': return self._j(api_prioridade(q.get('nivel', ['1'])[0]))
            if p == '/api/workflow': return self._j(fluxo.etapas_info())
            if p == '/api/atividade': return self._j(fluxo.atividade())
            if p == '/api/lotes': return self._j(fluxo.lotes())
            if p == '/api/eventos': return self._j(fluxo.eventos(int((q.get('desde') or ['0'])[0] or 0)))
            if p == '/api/nomes': return self._j(edital.nomes())
            if p == '/api/versao': return self._j({'v': _versao(), 'versao': _num()})
            if p == '/api/edital': return self._j(edital.arvore())
            if p == '/api/edital-itens': return self._j(edital.itens(q['cod'][0]))
            if p == '/api/tec-indice': return self._j(api_tec_indice())
            if p == '/api/tec-cadernos': return self._j(api_tec_cadernos())
            if p == '/api/universo': return self._j(universo.calcular())
            if p == '/api/aula-estado': return self._j(api_aula_estado(q))
            if p == '/api/recomendacao-aula': return self._j(api_recomendacao_aula(q))
            if p == '/api/retomar': return self._j(api_retomar())
            if p == '/aula':
                h = pagina_aula(q['dir'][0], q.get('modo', ['teoria'])[0], q.get('caderno', [None])[0], q.get('acao', [''])[0])
                return self._b(h.encode('utf-8'), 'text/html; charset=utf-8') if h else self._j({'erro': 'aula não encontrada'}, 404)
            if p == '/aula-pdf':
                arq = q.get('arq', ['aula.pdf'])[0]
                if not re.fullmatch(r'(aula|caderno\d+|caderno-revisao|resumo-vespera)\.pdf', arq): arq = 'aula.pdf'
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
            if p == '/api/diagnostico': return self._j(api_diagnostico(d))
            if p == '/api/config': return self._j(api_config(d))
            if p == '/api/aula-lida': return self._j(api_marcar_lida(d))
            if p == '/api/registrar-acesso': return self._j(api_registrar_acesso(d))
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
    try: _painel_atualizar_bg()   # aquece o painel em segundo plano; a aba abre com o último resultado salvo
    except Exception: pass
    try: srv.serve_forever()
    except KeyboardInterrupt: print('\nencerrado')
