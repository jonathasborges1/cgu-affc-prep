#!/usr/bin/env python3
"""Banco de questões CGU/AFFC v4. Fonte da verdade: arquivos de texto na pasta de dados.
Pasta de dados = variável BANCO_DIR, ou a pasta deste script. Arquivos:
  banco.jsonl      itens classificados (uma linha por item)
  nucleos.jsonl    núcleos (ideias testadas)      provas.jsonl   manifesto: estado de cada prova
  extraidos/ID.jsonl  itens extraídos     classificacoes/ID.jsonl  saída do classificador
  amostras/ID.jsonl   amostra p/ verificador      verificacoes/ID.jsonl  saída do verificador
O SQLite (FTS5) é só índice temporário (search/stats).

CONSULTA     search "termo" [--banca --ano --tema --limit --sem-padrao] | stats | mostrar ID
ITENS        add-json arq | set-padrao ID "texto" [--tags A,B] | set-nucleos ID n1,n2
NÚCLEOS      nucleo add --id n-x --edital "P1·ADM 4.1" --texto "..." [--base-legal ..]
MANIFESTO    prova add --id X --ref .. --url .. --url-gab .. --ano N [--orgao --cargo --peso]
             prova estado ID NOVO [--nota ..] [--hash ..] [--n-itens N --n-gab N]
             prova baixar ID [--local PROVA.pdf GAB.pdf] | texto ID | extrair ID | processar ID [--local ..]   (tudo local)
             prova filtrar ID --termos a,b,c   (recorte por tema: só esses itens vão ao classificador, economiza créditos)
             prova listar [--estado E] | prova proxima | prova amostra ID [--pct 20]
VERIFICAÇÃO comparar ID [--min-edital 90 --min-nucleo 80 --min-tags 80]
GRAVAÇÃO     aplicar ID        (só depois de 'verificada')
CONCURSO     concurso mostrar|listar|usar ID   (ativo em concursos/ativo.txt ou env BANCO_CONCURSO)
EDITAL       edital lacunas [--listar --bloco P3·ENG] | edital buscar TERMO   (usa concursos/<ativo>/programa.json)
PLANO        rank --edital "P1·ADM 4.1" [--ano-ref 2026]
CADERNO      verificar-caderno arq.json   (lista de ids ou de objetos {id,...})
Estados: descoberta > baixada > extraida > classificada > verificada > persistida (ou bloqueada)."""
import sqlite3,json,argparse,os,tempfile,sys,re,random,unicodedata,datetime,hashlib,shutil,subprocess,time,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); D=os.environ.get('BANCO_DIR') or HERE
P=lambda *a: os.path.join(D,*a)
def _ativo():
    v=os.environ.get('BANCO_CONCURSO')
    if v: return v
    f=P('concursos','ativo.txt')
    return open(f,encoding='utf-8').read().strip() if os.path.exists(f) else None
ATIVO=_ativo(); CONC=P('concursos',ATIVO) if ATIVO and os.path.isdir(P('concursos',ATIVO)) else D
PC=lambda *a: os.path.join(CONC,*a)   # dados do concurso ativo (banco, núcleos, manifesto, classificações)
JSONL=PC('banco.jsonl'); NUC=PC('nucleos.jsonl'); PROV=PC('provas.jsonl')
DB=os.environ.get('BANCO_DB') or os.path.join(tempfile.gettempdir(),'cgu_banco_index.db')
COLS=['fonte','banca','orgao','cargo','ano','ref','url','url_gab','item','enunciado','gabarito','comentario','tema','subtema','nivel','edital','padrao','tags']
OBRIG=['banca','ano','ref','url','url_gab','item','enunciado','gabarito','tema']
TAGS={'INVERSAO','ABSOLUTO','TROCA_TERMO','ESCOPO','CAUSA_CONSEQUENCIA','EXCECAO_OMITIDA','NORMA_LITERAL','CONCEITO_MISTURADO','PARTE_CERTA_PARTE_ERRADA','DETALHE_NUMERICO','NORMA_DESATUALIZADA'}
ESTADOS=['descoberta','baixada','extraida','classificada','verificada','persistida']
PROXIMA={'descoberta':'LOCAL: "prova processar ID" (baixa os 2 PDFs para provas/ID/, extrai texto e itens, avança sozinho se fechar). Chrome só se o download direto falhar',
 'baixada':'LOCAL: "prova processar ID" (texto + itens) ou corrigir à mão extraidos/ID.jsonl e rodar "prova estado ID extraida --n-itens N --n-gab N"',
 'extraida':'CLASSIFICADOR: disparar o agente classificador-itens -> classificacoes/ID.jsonl; depois "prova estado ID classificada"',
 'classificada':'VERIFICADOR: "prova amostra ID", disparar verificador-classificacao -> verificacoes/ID.jsonl; depois "comparar ID"',
 'verificada':'GRAVAÇÃO: "aplicar ID"','persistida':'nada (concluída)','bloqueada':'ver nota; decidir com o usuário'}
def agora(): return datetime.datetime.now().isoformat(timespec='seconds')
def lerj(path):
    if not os.path.exists(path): return []
    out=[]
    for n,l in enumerate(open(path,encoding='utf-8'),1):
        if l.strip():
            try: out.append(json.loads(l))
            except Exception as e: sys.exit('JSON inválido em %s linha %d: %s'%(path,n,e))
    return out
def escj(path,lst):
    os.makedirs(os.path.dirname(path) or '.',exist_ok=True)
    with open(path,'w',encoding='utf-8') as f:
        for d in lst: f.write(json.dumps(d,ensure_ascii=False)+'\n')
def rows():
    out=lerj(JSONL)
    for i,d in enumerate(out,1): d['id']=i
    return out
def key(d): return (d.get('url'),str(d.get('item')),d.get('enunciado'))
def nkey(t): return re.sub(r'[^a-z0-9]','',''.join(c for c in unicodedata.normalize('NFD',str(t or '')) if unicodedata.category(c)!='Mn').lower())[:160]
def salvar(lst):
    escj(JSONL,[{k:v for k,v in d.items() if k!='id'} for d in lst])
def conn():
    if os.path.exists(DB): os.remove(DB)
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.executescript(f"CREATE TABLE q(id INTEGER PRIMARY KEY,{','.join(k+(' INT' if k=='ano' else '') for k in COLS)});"
      "CREATE VIRTUAL TABLE qf USING fts5(enunciado,tema,subtema,comentario,padrao,tags,content='q',content_rowid='id',tokenize='unicode61 remove_diacritics 2');")
    for d in rows():
        v=dict(d); v['tags']=','.join(v['tags']) if isinstance(v.get('tags'),list) else v.get('tags')
        c.execute(f"INSERT INTO q(id,{','.join(COLS)}) VALUES(?,{','.join('?'*len(COLS))})",[d['id']]+[v.get(k) for k in COLS])
        c.execute("INSERT INTO qf(rowid,enunciado,tema,subtema,comentario,padrao,tags) VALUES(?,?,?,?,?,?,?)",(d['id'],*[v.get(k) for k in ('enunciado','tema','subtema','comentario','padrao','tags')]))
    c.commit(); return c
# ---------- edital: normaliza "P1 · Adm. pública 4.1" e "P1·ADM 4.1" para (p1, adm, 4.1)
def sem_acento(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if unicodedata.category(ch)!='Mn')
def ekey(s):
    s=sem_acento(str(s or '')).lower()
    m=re.search(r'p\s*([1-4])',s); prova='p'+m.group(1) if m else ''
    resto=s[m.end():] if m else s
    num=re.findall(r'\d+(?:\.\d+)*',resto); num=num[-1] if num else ''
    letras=re.sub(r'[^a-z]','',re.sub(r'\d+(?:\.\d+)*','',resto))[:3]
    return prova,letras,num
def ematch(item_edital,q):
    a,b=ekey(item_edital),ekey(q)
    if not a[0] or a[0]!=b[0]: return False
    if b[1] and a[1]!=b[1]: return False
    if not b[2]: return True
    return a[2]==b[2] or a[2].startswith(b[2]+'.')
def nucs(d):
    n=d.get('nucleos') or d.get('nucleo_id') or []
    return [n] if isinstance(n,str) else list(n)
# ---------- manifesto
def programa(): return lerj(PC('programa.json'))
def edital_valido(x):
    if str(x or '').upper()=='FORA': return True
    pr=programa()
    if not pr: return True   # sem programa carregado, não valida
    k=ekey(x); return any(ekey(d['codigo'])==k for d in pr)
def provas(): return lerj(PROV)
def prova_get(pid):
    for p in provas():
        if p['prova_id']==pid: return p
    sys.exit('prova não encontrada: %s'%pid)
def prova_put(p):
    lst=provas(); lst=[x for x in lst if x['prova_id']!=p['prova_id']]+[p]; escj(PROV,lst)
def hist(p,estado,nota=None): p.setdefault('historico',[]).append({'estado':estado,'quando':agora(),'nota':nota}); p['estado']=estado
def cmd_prova(r):
    if r.sub=='add':
        if any(x['prova_id']==r.id for x in provas()): sys.exit('já existe: %s'%r.id)
        p={'prova_id':r.id,'ref':r.ref,'url':r.url,'url_gab':r.url_gab,'ano':r.ano,'orgao':r.orgao,'cargo':r.cargo,'peso':r.peso,'hash':None,'n_itens':None,'n_gab':None,'verificacao':None,'historico':[]}
        hist(p,'descoberta'); prova_put(p); print('ok',r.id,'descoberta'); return
    if r.sub=='listar':
        for p in provas():
            if not r.estado or p['estado']==r.estado: print('%-28s %-12s itens=%s %s'%(p['prova_id'],p['estado'],p.get('n_itens'),p['ref'][:60]))
        return
    if r.sub=='proxima':
        pend=[p for p in provas() if p['estado']!='persistida']
        if not pend: print('nenhuma prova pendente no manifesto -> descobrir novas provas (ranking-compatibilidade-provas.md)'); return
        for p in pend: print('%-28s [%s] -> %s'%(p['prova_id'],p['estado'],PROXIMA[p['estado']]))
        return
    if r.sub=='amostra':
        p=prova_get(r.id); it=lerj(PC('escopo',r.id+'.jsonl')) or lerj(P('extraidos',r.id+'.jsonl'))
        if not it: sys.exit('sem extraidos/%s.jsonl'%r.id)
        n=max(3,round(len(it)*r.pct/100)); n=min(n,len(it)); rnd=random.Random(r.id)
        am=sorted(rnd.sample(range(len(it)),n)); escj(PC('amostras',r.id+'.jsonl'),[it[i] for i in am]); print('amostra',n,'de',len(it),'-> amostras/%s.jsonl'%r.id); return
    if r.sub=='estado':
        p=prova_get(r.id); novo=r.novo; atual=p['estado']
        if novo=='bloqueada': hist(p,novo,r.nota); prova_put(p); print('ok bloqueada'); return
        if novo in ('verificada','persistida'): sys.exit('"%s" só é atingido por "%s"'%(novo,'comparar' if novo=='verificada' else 'aplicar'))
        if novo not in ESTADOS: sys.exit('estado inválido')
        base=atual if atual in ESTADOS else [h['estado'] for h in p['historico'] if h['estado'] in ESTADOS][-1]
        if ESTADOS.index(novo) not in (ESTADOS.index(base),ESTADOS.index(base)+1): sys.exit('transição inválida: %s -> %s (esperado: %s)'%(atual,novo,ESTADOS[min(ESTADOS.index(base)+1,5)]))
        if novo=='baixada':
            if getattr(r,'sem_arquivo',False):
                if not r.nota: sys.exit('--sem-arquivo exige --nota explicando o motivo')
            else:
                hs=hashes_pasta(r.id)
                if not hs: sys.exit('PORTÃO: faltam provas/%s/prova.pdf e/ou gabarito.pdf válidos. Use "prova baixar %s" ou "prova baixar %s --local PROVA GAB"'%(r.id,r.id,r.id))
                p['hash']=hs
            p.setdefault('arquivos',{'pasta':'provas/'+r.id})
        if novo=='extraida':
            if r.n_itens is None or r.n_gab is None: sys.exit('informe --n-itens e --n-gab')
            if r.n_itens!=r.n_gab: sys.exit('PORTÃO: itens extraídos (%d) != gabaritos (%d)'%(r.n_itens,r.n_gab))
            ex=lerj(P('extraidos',r.id+'.jsonl'))
            if len(ex)!=r.n_itens: sys.exit('PORTÃO: extraidos/%s.jsonl tem %d linhas, esperado %d'%(r.id,len(ex),r.n_itens))
            p['n_itens']=r.n_itens; p['n_gab']=r.n_gab
        if novo=='classificada':
            alvo=lerj(PC('escopo',r.id+'.jsonl')) or lerj(P('extraidos',r.id+'.jsonl'))
            ex={str(d['item']) for d in alvo}; cl=lerj(PC('classificacoes',r.id+'.jsonl'))
            if len(cl)!=len(ex) or {str(d['item']) for d in cl}!=ex: sys.exit('PORTÃO: classificacoes/%s.jsonl não cobre exatamente os %d itens do escopo (%s)'%(r.id,len(ex),'recorte por tema' if os.path.exists(PC('escopo',r.id+'.jsonl')) else 'prova inteira'))
            ruim=[d['item'] for d in cl if not d.get('edital') or not edital_valido(d.get('edital')) or any(t not in TAGS for t in d.get('tags') or [])]
            if ruim: sys.exit('PORTÃO: itens sem edital, com código fora do programa ou com etiqueta inválida: %s'%ruim)
        hist(p,novo,r.nota); prova_put(p); print('ok',r.id,atual,'->',novo)

# ---------- arquivos locais: baixar, texto, extrair (tudo local, sem gastar créditos do Claude) ----------
UA='cgu-bd/4 (estudo pessoal; contato do usuario)'
def pdir(pid): return P('provas',pid)
def eh_pdf(path):
    try:
        with open(path,'rb') as f: return f.read(5)==b'%PDF-'
    except OSError: return False
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def hashes_pasta(pid):
    a,b=os.path.join(pdir(pid),'prova.pdf'),os.path.join(pdir(pid),'gabarito.pdf')
    if eh_pdf(a) and eh_pdf(b): return {'prova':sha(a),'gabarito':sha(b)}
    return None
def baixa(url,dest,pausa):
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    tmp=dest+'.part'
    # Falhas de CDN/DNS não podem bloquear uma rodada inteira de mineração.
    # Permite ajuste por ambiente, mantendo um limite conservador por arquivo.
    timeout=float(os.environ.get('CGU_DOWNLOAD_TIMEOUT','20'))
    with urllib.request.urlopen(req,timeout=timeout) as rsp, open(tmp,'wb') as f: shutil.copyfileobj(rsp,f)
    if not eh_pdf(tmp): os.remove(tmp); sys.exit('o conteúdo baixado não é PDF: %s'%url)
    os.replace(tmp,dest); time.sleep(pausa)
def pdf_texto(pdf,saida,layout=False):
    if shutil.which('pdftotext'):
        subprocess.run(['pdftotext']+(['-layout'] if layout else [])+[pdf,saida],check=True)
    else:
        from pypdf import PdfReader
        open(saida,'w',encoding='utf-8').write('\n'.join((pg.extract_text() or '') for pg in PdfReader(pdf).pages))
def pdf_texto_colunas(pdf,saida,layout=False):
    """Provas em 2 colunas: lê cada página coluna esquerda e depois direita (evita números de item soltos)."""
    info=subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout
    n=int(re.search(r'Pages:\s+(\d+)',info).group(1)); w=float(re.search(r'Page size:\s+([\d.]+)',info).group(1))
    h=float(re.search(r'x\s+([\d.]+)',info.split('Page size:')[1]).group(1)); out=[]
    for pg in range(1,n+1):
        for x in (0,w/2):
            out.append(subprocess.run(['pdftotext']+(['-layout'] if layout else [])+['-f',str(pg),'-l',str(pg),'-x',str(int(x)),'-y','0','-W',str(int(w/2)),'-H',str(int(h)),pdf,'-'],capture_output=True,text=True).stdout)
    open(saida,'w',encoding='utf-8').write('\n'.join(out))
def texto_melhor(pid,gab):
    """Gera prova.txt pelo método que extrai TODOS os itens do gabarito COM enunciado (>=25 caracteres).
    Métodos: normal, colunas, colunas+layout. Contar itens não basta: item de enunciado vazio é perda silenciosa."""
    d=pdir(pid); pdf=os.path.join(d,'prova.pdf'); dest=os.path.join(d,'prova.txt')
    metodos=[('normal',lambda a,b:pdf_texto(a,b)),('colunas',lambda a,b:pdf_texto_colunas(a,b)),('col-layout',lambda a,b:pdf_texto_colunas(a,b,True))]
    melhor=None
    for nome,fn in metodos:
        fn(pdf,dest); v=extrair_itens(open(dest,encoding='utf-8').read(),gab)
        bons=sum(1 for x in v.values() if len(x['enunciado'])>=25)
        if melhor is None or bons>melhor[2]: melhor=(v,nome,bons)
        if bons>=len(gab): break
    dict(metodos)[melhor[1]](pdf,dest)
    return melhor[0],melhor[1]
def gab_parse(txt):
    """Lê a tabela 'Item n n n / Gabarito C E ...' do gabarito do Cebraspe. Retorna {item:'C'|'E'|'ANULADO'}."""
    out={}; itens=None
    for ln in txt.splitlines():
        t=ln.split()
        if not t: continue
        if t[0]=='Item' and all(x.isdigit() for x in t[1:]): itens=[int(x) for x in t[1:]]
        elif t[0]=='Gabarito' and itens:
            vals=t[1:]
            for n,v in zip(itens,vals):
                if n>0: out[n]=v if v in ('C','E') else 'ANULADO'
            itens=None
    return out
RUIDO=re.compile(r'CEBRASPE|^Espa[cç]o livre|^\*+ ?FIM|^\s*[–-]\s*\d+\s*[–-]\s*$')
CABEC=re.compile(r'^-- ?CONHECIMENTOS [^-]+-+\s*')
PREAMB=re.compile(r'^(Julgue|Considerando|Em rela|A respeito|Tendo como|No que se refere|Com base|Acerca|Com rela|Quanto|Conforme|Para responder|Com refer|Texto|Em conformidade|Segundo|De acordo)')
def extrair_itens(txt,gab):
    esperados=sorted(gab); vistos={}; atual=None; pre=[]; ctx=''; buf=[]
    def fecha():
        nonlocal ctx
        if atual is None: return
        ls=[l for l in buf]; corte=None
        for i in range(1,len(ls)):
            bloco=' '.join(ls[i:i+3])
            if PREAMB.match(ls[i]) and re.search(r'julgue|assinale|considere',bloco,re.I): corte=i; break
        corpo=ls if corte is None else ls[:corte]
        novo_ctx=None if corte is None else ' '.join(ls[corte:])
        fig=[]
        if not re.search(r'c[oó]digo|script|programa',' '.join(corpo[:2]),re.I):
            fig=[l for l in corpo if re.match(r'^</?[A-Za-z!?]|^\w+=“|/>\s*$',l)]; corpo=[l for l in corpo if l not in fig]
        vistos[atual]={'item':atual,'contexto':ctx,'enunciado':' '.join(corpo).strip(),'figura':' '.join(fig)}
        if novo_ctx: ctx=novo_ctx
    pend=list(esperados)
    for ln in txt.splitlines():
        ln=CABEC.sub('',ln.strip())
        if not ln or RUIDO.search(ln): continue
        m=re.match(r'^(\d{1,3})(?:\s+(\S.*))?$',ln)
        if m and ((m.group(2) and m.group(2)[0].isupper() and int(m.group(1)) in pend[:25]) or (not m.group(2) and pend and int(m.group(1))==pend[0])):
            n=int(m.group(1)); fecha()
            if atual is None and pre: ctx=' '.join(pre)
            atual=n; buf=[m.group(2)] if m.group(2) else []; pend=[x for x in pend if x!=n]; continue
        if atual is None: pre.append(ln)
        else: buf.append(ln)
    fecha()
    return vistos
def cmd_arquivos(r):
    pid=r.id; p=prova_get(pid); d=pdir(pid); os.makedirs(d,exist_ok=True)
    if r.sub=='baixar':
        a,b=os.path.join(d,'prova.pdf'),os.path.join(d,'gabarito.pdf')
        if r.local:
            for src,dst in zip(r.local,(a,b)):
                if not eh_pdf(src): sys.exit('não é PDF: %s'%src)
                shutil.copyfile(src,dst)
            origem='copiado de arquivos locais: %s | %s'%tuple(r.local)
        else:
            if not (p.get('url') and p.get('url_gab')): sys.exit('manifesto sem url/url_gab')
            baixa(p['url'],a,r.pausa); baixa(p['url_gab'],b,r.pausa)
            origem='baixado de %s e %s'%(p['url'],p['url_gab'])
        open(os.path.join(d,'fonte.txt'),'w',encoding='utf-8').write('%s\nquando: %s\n'%(origem,agora()))
        print('ok provas/%s/ prova.pdf %d KB, gabarito.pdf %d KB'%(pid,os.path.getsize(a)//1024,os.path.getsize(b)//1024)); return
    if r.sub=='texto':
        if not hashes_pasta(pid): sys.exit('sem PDFs em provas/%s/'%pid)
        pdf_texto(os.path.join(d,'prova.pdf'),os.path.join(d,'prova.txt')); pdf_texto(os.path.join(d,'gabarito.pdf'),os.path.join(d,'gabarito.txt'),layout=True)
        print('ok texto extraído (prova.txt, gabarito.txt)'); return
    if r.sub=='extrair':
        tp,tg=os.path.join(d,'prova.txt'),os.path.join(d,'gabarito.txt')
        if not (os.path.exists(tp) and os.path.exists(tg)): sys.exit('rode "prova texto %s" antes'%pid)
        gab=gab_parse(open(tg,encoding='utf-8').read())
        if not gab: sys.exit('não consegui ler a tabela do gabarito (formato diferente); revisar gabarito.txt')
        vistos=extrair_itens(open(tp,encoding='utf-8').read(),gab)
        faltam=[n for n in sorted(gab) if n not in vistos]; anul=[n for n in sorted(gab) if gab[n]=='ANULADO']
        linhas=[]
        for n in sorted(vistos):
            v=vistos[n]; g=gab[n]
            sus=bool(re.search(r'[<>{};]|\bexample\b',v['enunciado'])) or len(v['enunciado'])<25
            linhas.append({'prova_id':pid,'banca':'Cebraspe','orgao':p.get('orgao'),'cargo':p.get('cargo'),'ano':p['ano'],'ref':p['ref'],'url':p['url'],'url_gab':p['url_gab'],
                           'item':n,'enunciado':v['enunciado'],'contexto':v['contexto'],'figura':v.get('figura',''),'gabarito':g,'revisar':sus})
        linhas=[l for l in linhas if l['gabarito']!='ANULADO']
        escj(P('extraidos',pid+'.jsonl'),linhas)
        rev=[l['item'] for l in linhas if l['revisar']]
        print('extraidos/%s.jsonl: %d itens (gabarito: %d; anulados: %s; não localizados no texto: %s; revisar à mão: %s)'%(pid,len(linhas),len(gab),anul or '-',faltam or '-',rev or '-'))
        if faltam: print('PORTÃO vai falhar até corrigir os não localizados (ver provas/%s/prova.txt)'%pid)
        return
    if r.sub=='filtrar':
        ex=lerj(P('extraidos',pid+'.jsonl'))
        if not ex: sys.exit('sem extraidos/%s.jsonl'%pid)
        ter=[sem_acento(t).lower().strip() for t in r.termos.split(',') if t.strip()]
        def hit(d):
            tx=sem_acento(d['enunciado']+' '+d.get('contexto','')).lower()
            return any((re.search(r'\b'+re.escape(t)+r'\b',tx) if len(t)<=4 else t in tx) for t in ter)
        acert={d['item'] for d in ex if hit(d)}
        ctxs={d['contexto'] for d in ex if d['item'] in acert and d.get('contexto')}
        sel=[d for d in ex if d['item'] in acert or (d.get('contexto') in ctxs)]
        escj(PC('escopo',pid+'.jsonl'),sel)
        print('escopo: %d de %d itens (%d com termo + %d do mesmo bloco de comando) -> escopo/%s.jsonl'%(len(sel),len(ex),len(acert),len(sel)-len(acert),pid)); return
    if r.sub=='processar':
        ns=lambda **k: argparse.Namespace(**dict(dict(sub='baixar',id=pid,local=None,pausa=6.0),**k))
        if p['estado']=='descoberta':
            cmd_arquivos(ns(local=r.local))
            cmd_prova(argparse.Namespace(sub='estado',id=pid,novo='baixada',nota=None,hash=None,n_itens=None,n_gab=None,sem_arquivo=False))
        cmd_arquivos(ns(sub='texto')); cmd_arquivos(ns(sub='extrair'))
        ex=lerj(P('extraidos',pid+'.jsonl')); gab=gab_parse(open(os.path.join(d,'gabarito.txt'),encoding='utf-8').read())
        n_gab=len([1 for v in gab.values() if v!='ANULADO'])
        if len(ex)==n_gab:
            cmd_prova(argparse.Namespace(sub='estado',id=pid,novo='extraida',nota=None,hash=None,n_itens=len(ex),n_gab=n_gab,sem_arquivo=False))
        else: print('parou em "baixada": itens %d != gabaritos %d; revisar à mão'%(len(ex),n_gab))
        return

def cmd_concurso(r):
    base=P('concursos')
    if r.sub=='listar':
        for n in sorted(os.listdir(base)) if os.path.isdir(base) else []:
            if os.path.isdir(os.path.join(base,n)): print(('* ' if n==ATIVO else '  ')+n)
        return
    if r.sub=='usar':
        if not os.path.isdir(os.path.join(base,r.id)): sys.exit('concurso não encontrado: %s'%r.id)
        open(os.path.join(base,'ativo.txt'),'w',encoding='utf-8').write(r.id+'\n'); print('ativo:',r.id); return
    f=os.path.join(CONC,'concurso.json')
    if not os.path.exists(f): sys.exit('nenhum concurso ativo (concursos/ativo.txt)')
    c=json.load(open(f,encoding='utf-8')); pr=programa()
    print('%s | %s | %s'%(c['id'],c['edital'],c['banca'])); print('cargo %s: %s – %s'%(c['cargo']['numero'],c['cargo']['nome'],c['cargo']['especialidade']))
    print('prova: %s | programa: %d subitens'%(c['prova']['data'],len(pr)))
def cmd_edital(r):
    pr=programa()
    if not pr: sys.exit('sem programa.json no concurso ativo')
    if r.sub=='buscar':
        q=sem_acento(r.termo).lower()
        for d in pr:
            if q in sem_acento(d['texto']).lower() or q in sem_acento(d['codigo']).lower(): print('%-14s %s'%(d['codigo'],d['texto'][:110]))
        return
    folhas=[d for d in pr if not any(o['codigo'].startswith(d['codigo']+'.') for o in pr)]
    cont={}
    for it in rows():
        k=ekey(it.get('edital')); cont[k]=cont.get(k,0)+1
    por={}
    for d in folhas:
        b=d['prova']+'·'+d['bloco']; n=cont.get(ekey(d['codigo']),0); por.setdefault(b,[]).append((d,n))
    tot=cob=0
    for b,l in por.items():
        c=len([1 for _,n in l if n]); tot+=len(l); cob+=c
        print('%-10s %2d/%2d subitens com questão'%(b,c,len(l)))
        if r.listar and (not r.bloco or r.bloco.lower() in b.lower()):
            for d,n in l:
                if not n: print('    sem questão: %-14s %s'%(d['codigo'],d['texto'][:80]))
    print('TOTAL %d/%d (%.0f%%)'%(cob,tot,100*cob/max(tot,1)))

def sim_texto(x,y):
    """Núcleos de execuções independentes têm ids diferentes: compara o TEXTO (Jaccard de radicais de 5 letras)."""
    f=lambda t:{w[:5] for w in re.findall(r'[a-z0-9]+',sem_acento(str(t or '')).lower()) if len(w)>3}
    a,b=f(x),f(y); return len(a&b)/len(a|b) if a and b else 0.0
def cmd_comparar(r):
    p=prova_get(r.id)
    if p['estado']!='classificada': sys.exit('prova está em "%s"; comparar exige "classificada"'%p['estado'])
    cl={str(d['item']):d for d in lerj(PC('classificacoes',r.id+'.jsonl'))}; ve=lerj(PC('verificacoes',r.id+'.jsonl'))
    if not ve: sys.exit('sem verificacoes/%s.jsonl'%r.id)
    n=ok_e=ok_n=ok_t=0; desac=[]
    for v in ve:
        c=cl.get(str(v['item']))
        if not c: continue
        n+=1; e=ematch(c.get('edital'),v.get('edital')) or ematch(v.get('edital'),c.get('edital')) or (str(c.get('edital')).upper()=='FORA'==str(v.get('edital')).upper())
        a,b=set(nucs(c)),set(nucs(v)); nn=(not a and not b) or bool(a&b) or sim_texto(c.get('nucleo_texto'),v.get('nucleo_texto'))>=0.3
        ta,tb=set(c.get('tags') or []),set(v.get('tags') or []); tt=(not ta and not tb) or bool(ta&tb)
        ok_e+=e; ok_n+=nn; ok_t+=tt
        if not (e and nn and tt): desac.append({'item':v['item'],'edital':[c.get('edital'),v.get('edital')],'nucleo':[sorted(a),sorted(b)],'sim':round(sim_texto(c.get('nucleo_texto'),v.get('nucleo_texto')),2),'tags':[sorted(ta),sorted(tb)]})
    if n==0: sys.exit('nenhum item da verificação casa com a classificação')
    pe,pn,pt=100*ok_e/n,100*ok_n/n,100*ok_t/n
    aprov=pe>=r.min_edital and pn>=r.min_nucleo and pt>=r.min_tags
    p['verificacao']={'n':n,'edital':round(pe,1),'nucleo':round(pn,1),'tags':round(pt,1),'aprovada':aprov,'desacordos':[d['item'] for d in desac]}
    print('amostra=%d  edital=%.0f%% (min %d)  núcleo=%.0f%% (min %d)  pegadinha=%.0f%% (min %d)'%(n,pe,r.min_edital,pn,r.min_nucleo,pt,r.min_tags))
    for d in desac: print('  desacordo item %s: %s'%(d['item'],json.dumps(d,ensure_ascii=False)))
    if aprov: hist(p,'verificada','concordância ok'); print('APROVADA -> verificada. Próximo: aplicar',r.id)
    else: hist(p,'extraida','verificação reprovada; reclassificar com os desacordos como exemplos'); print('REPROVADA -> volta a "extraida": reclassificar a prova inteira');
    prova_put(p)
def cmd_aplicar(r):
    p=prova_get(r.id)
    if p['estado']!='verificada': sys.exit('prova está em "%s"; aplicar exige "verificada"'%p['estado'])
    ex={str(d['item']):d for d in lerj(P('extraidos',r.id+'.jsonl'))}; cl=lerj(PC('classificacoes',r.id+'.jsonl'))
    have={key(d) for d in rows()}; havn={nkey(d.get('enunciado')) for d in rows()}; nuc={x['id'] for x in lerj(NUC)}; novosn=[]; ins=rej=dup=0; saida=[]
    for c in cl:
        e=ex.get(str(c['item']))
        if not e: rej+=1; continue
        d=dict(e); ids=nucs(c)
        if d.get('item_orig'): d['item']=str(d.pop('item_orig')); d.pop('prova_origem',None)   # lote por tema: devolve o nº real do item
        d.update({'fonte':'oficial-'+r.id,'edital':c['edital'],'tema':c['edital'],'subtema':c.get('nucleo_texto'),'nivel':c.get('nivel'),'padrao':c.get('padrao'),'tags':c.get('tags') or [],'nucleos':ids,'peso_prova':p.get('peso',1.0)})
        if c.get('duvida'): d['duvida']=c['duvida']
        if c.get('base_legal'): d['base_legal']=c['base_legal']
        falta=[k for k in OBRIG if not d.get(k)]
        if falta or d.get('gabarito') not in ('C','E'): rej+=1; print('rejeitado item %s (faltam/gabarito): %s'%(c['item'],falta)); continue
        if key(d) in have or nkey(d.get('enunciado')) in havn: dup+=1; continue   # mesma questão em outro cargo/prova
        saida.append(d); have.add(key(d)); havn.add(nkey(d.get('enunciado'))); ins+=1
        for i in ids:
            if i not in nuc and c.get('nucleo_novo'): nuc.add(i); novosn.append({'id':i,'edital':c['edital'],'texto':c.get('nucleo_texto'),'base_legal':c.get('base_legal'),'origem':r.id})
    if saida:
        with open(JSONL,'a',encoding='utf-8') as f:
            for d in saida: f.write(json.dumps(d,ensure_ascii=False)+'\n')
    if novosn:
        with open(NUC,'a',encoding='utf-8') as f:
            for n in novosn: f.write(json.dumps(n,ensure_ascii=False)+'\n')
    hist(p,'persistida','inseridos=%d duplicados=%d rejeitados=%d núcleos novos=%d'%(ins,dup,rej,len(novosn))); prova_put(p)
    print('inseridos',ins,'duplicados',dup,'rejeitados',rej,'núcleos novos',len(novosn),'-> persistida')
# ---------- rank
def cmd_rank(r):
    items=[d for d in rows() if ematch(d.get('edital'),r.edital)]
    if not items: print('nenhum item com edital ~ "%s" no banco -> MINERAR'%r.edital); return
    sem=[d for d in items if not nucs(d)]; com=[d for d in items if nucs(d)]
    tx={x['id']:x for x in lerj(NUC)}; sc={}; cnt={}; tg={}
    for d in com:
        w=float(d.get('peso_prova') or 1.0)*0.5**((r.ano_ref-int(d['ano']))/3); ns=nucs(d)
        for n in ns: sc[n]=sc.get(n,0)+w/len(ns); cnt[n]=cnt.get(n,0)+1; tg.setdefault(n,set()).update(d.get('tags') or [])
    tot=sum(sc.values()) or 1; N=len(com); n1=sum(1 for n in cnt if cnt[n]==1); cob=1-n1/N if N else 0
    print('Tema "%s": %d itens no banco (%d com núcleo, %d sem núcleo), %d núcleos'%(r.edital,len(items),N,len(sem),len(cnt)))
    print('Cobertura estimada (Good-Turing) = %.0f%%  [núcleos vistos 1 vez: %d de %d itens]'%(100*cob,n1,N))
    cum=0; ordem=sorted(sc,key=lambda n:-sc[n]); aula=1; k=0
    print('\n%-3s %-6s %-5s %-6s %-9s %s'%('#','massa','itens','acum','decisão','núcleo'))
    for i,n in enumerate(ordem,1):
        m=sc[n]/tot; antes=cum; cum+=m
        if antes<0.80: dec='ENSINAR'
        elif cnt[n]==1 and cob<0.70: dec='ENSINAR(1x)'
        else: dec='opcional'
        if dec.startswith('ENSINAR'):
            k+=1
            if k>10: aula+=1; k=1
        print('%-3d %4.0f%%  %-5d %4.0f%%  %-9s %s%s'%(i,100*m,cnt[n],100*cum,dec+('' if not dec.startswith('ENSINAR') else ' a%d'%aula),(tx.get(n,{}).get('texto') or n)[:80],'' if n in tx else '  [núcleo sem cadastro]'))
    pend=[p for p in provas() if p['estado']!='persistida']
    print('\nRECOMENDAÇÃO:',end=' ')
    if sem: print('%d itens sem núcleo: classificar antes de decidir.'%len(sem))
    elif cob<0.70: print('cobertura < 70%%: MINERAR mais (%s); núcleos vistos 1 vez entram no plano (ENSINAR(1x)) e o que o edital pede sem questão vira lacuna.'%('%d provas pendentes no manifesto'%len(pend) if pend else 'manifesto sem provas pendentes: descobrir novas provas'))
    else: print('cobertura >= 70%%: PODE ENSINAR (%d aula(s)).'%aula)
# ---------- caderno
def cmd_caderno(r):
    spec=json.load(open(r.arq,encoding='utf-8')); bank={d['id']:d for d in rows()}; err=[]
    if not isinstance(spec,list): sys.exit('o arquivo deve ser uma lista JSON de ids ou de objetos {"id":..}')
    if len(spec)>10: err.append('caderno tem %d questões (máximo 10)'%len(spec))
    vistos=set()
    for s in spec:
        i=s if isinstance(s,int) else s.get('id'); d=bank.get(i)
        if d is None: err.append('id %s não existe no banco'%i); continue
        if i in vistos: err.append('id %s repetido'%i)
        vistos.add(i)
        for k in ('ref','url','url_gab','tema','nivel','gabarito','enunciado'):
            if not d.get(k): err.append('#%s sem %s'%(i,k))
        if not str(d.get('url','')).startswith('http'): err.append('#%s url inválida'%i)
        if d.get('gabarito') not in ('C','E'): err.append('#%s gabarito inválido'%i)
        if d.get('duvida'): err.append('#%s marcado com dúvida: %s'%(i,d['duvida']))
        if isinstance(s,dict):
            for k in ('enunciado','gabarito','url'):
                if k in s and s[k]!=d.get(k): err.append('#%s: %s do caderno difere do banco'%(i,k))
    print('caderno: %d questões'%len(spec)); [print('  ERRO:',e) for e in err]
    print('APROVADO' if not err else 'REPROVADO (%d problemas)'%len(err)); sys.exit(1 if err else 0)
def main():
    a=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter); s=a.add_subparsers(dest='cmd')
    p=s.add_parser('search'); p.add_argument('termo'); p.add_argument('--banca'); p.add_argument('--ano',type=int); p.add_argument('--tema'); p.add_argument('--limit',type=int,default=15); p.add_argument('--sem-padrao',action='store_true')
    s.add_parser('stats'); p=s.add_parser('add-json'); p.add_argument('arq')
    p=s.add_parser('set-padrao'); p.add_argument('id',type=int); p.add_argument('texto'); p.add_argument('--tags',default='')
    p=s.add_parser('set-nucleos'); p.add_argument('id',type=int); p.add_argument('nucleos')
    p=s.add_parser('mostrar'); p.add_argument('id',type=int)
    p=s.add_parser('nucleo'); ns=p.add_subparsers(dest='sub'); q=ns.add_parser('add'); q.add_argument('--id',required=True); q.add_argument('--edital',required=True); q.add_argument('--texto',required=True); q.add_argument('--base-legal')
    p=s.add_parser('prova'); ps=p.add_subparsers(dest='sub')
    q=ps.add_parser('add'); [q.add_argument('--'+k) for k in ('id','ref','url','url-gab')]; q.add_argument('--ano',type=int,required=True); q.add_argument('--orgao'); q.add_argument('--cargo'); q.add_argument('--peso',type=float,default=1.0)
    q=ps.add_parser('estado'); q.add_argument('id'); q.add_argument('novo'); q.add_argument('--nota'); q.add_argument('--hash'); q.add_argument('--n-itens',type=int); q.add_argument('--n-gab',type=int); q.add_argument('--sem-arquivo',action='store_true')
    q=ps.add_parser('baixar'); q.add_argument('id'); q.add_argument('--local',nargs=2,metavar=('PROVA','GAB')); q.add_argument('--pausa',type=float,default=6.0)
    q=ps.add_parser('texto'); q.add_argument('id'); q=ps.add_parser('extrair'); q.add_argument('id')
    q=ps.add_parser('filtrar'); q.add_argument('id'); q.add_argument('--termos',required=True,help='termos separados por vírgula (sem acento, minúsculas tanto faz)')
    q=ps.add_parser('processar'); q.add_argument('id'); q.add_argument('--local',nargs=2,metavar=('PROVA','GAB'))
    q=ps.add_parser('listar'); q.add_argument('--estado'); ps.add_parser('proxima'); q=ps.add_parser('amostra'); q.add_argument('id'); q.add_argument('--pct',type=int,default=20)
    p=s.add_parser('concurso'); cs=p.add_subparsers(dest='sub'); cs.add_parser('mostrar'); cs.add_parser('listar'); q=cs.add_parser('usar'); q.add_argument('id')
    p=s.add_parser('edital'); es=p.add_subparsers(dest='sub'); q=es.add_parser('lacunas'); q.add_argument('--listar',action='store_true'); q.add_argument('--bloco'); q=es.add_parser('buscar'); q.add_argument('termo')
    p=s.add_parser('comparar'); p.add_argument('id'); p.add_argument('--min-edital',type=int,default=90); p.add_argument('--min-nucleo',type=int,default=80); p.add_argument('--min-tags',type=int,default=80)
    p=s.add_parser('aplicar'); p.add_argument('id')
    p=s.add_parser('rank'); p.add_argument('--edital',required=True); p.add_argument('--ano-ref',type=int,default=datetime.date.today().year)
    p=s.add_parser('verificar-caderno'); p.add_argument('arq')
    r=a.parse_args()
    if not r.cmd: a.print_help(); return
    if r.cmd=='prova':
        if r.sub=='add': r.url_gab=r.url_gab;
        if r.sub=='estado': r.id=r.id
        if r.sub in ('baixar','texto','extrair','filtrar','processar'): return cmd_arquivos(r)
        return cmd_prova(r)
    if r.cmd=='concurso': return cmd_concurso(r)
    if r.cmd=='edital': return cmd_edital(r)
    if r.cmd=='comparar': return cmd_comparar(r)
    if r.cmd=='aplicar': return cmd_aplicar(r)
    if r.cmd=='rank': return cmd_rank(r)
    if r.cmd=='verificar-caderno': return cmd_caderno(r)
    if r.cmd=='nucleo':
        if lerj(NUC) and any(x['id']==r.id for x in lerj(NUC)): sys.exit('núcleo já existe')
        with open(NUC,'a',encoding='utf-8') as f: f.write(json.dumps({'id':r.id,'edital':r.edital,'texto':r.texto,'base_legal':r.base_legal},ensure_ascii=False)+'\n')
        print('ok',r.id); return
    if r.cmd=='add-json':
        have={key(d) for d in rows()}; havn={nkey(d.get('enunciado')) for d in rows()}; n=rej=0
        with open(JSONL,'a',encoding='utf-8') as f:
            for l in open(r.arq,encoding='utf-8'):
                if not l.strip(): continue
                d=json.loads(l); d.pop('id',None)
                falta=[k for k in OBRIG if not d.get(k)]
                if falta: rej+=1; print('rejeitada (faltam %s): %s'%(','.join(falta),str(d.get('ref'))[:80])); continue
                if d['gabarito'] not in ('C','E'): rej+=1; print('rejeitada (gabarito deve ser C ou E):',d.get('ref')); continue
                if key(d) in have: continue
                f.write(json.dumps(d,ensure_ascii=False)+'\n'); have.add(key(d)); n+=1
        print('inseridas',n,'rejeitadas',rej); return
    if r.cmd=='set-padrao':
        lst=rows(); tg=[t for t in r.tags.split(',') if t]
        ruim=[t for t in tg if t not in TAGS]
        if ruim: sys.exit('tags inválidas: %s (válidas: %s)'%(ruim,sorted(TAGS)))
        for d in lst:
            if d['id']==r.id: d['padrao']=r.texto; d['tags']=tg; salvar(lst); print('ok',r.id); return
        sys.exit('id não encontrado')
    if r.cmd=='set-nucleos':
        lst=rows(); ids=[x for x in r.nucleos.split(',') if x]; cad={x['id'] for x in lerj(NUC)}
        ruim=[x for x in ids if x not in cad]
        if ruim: sys.exit('núcleos não cadastrados (use "nucleo add"): %s'%ruim)
        for d in lst:
            if d['id']==r.id: d['nucleos']=ids; salvar(lst); print('ok',r.id); return
        sys.exit('id não encontrado')
    if r.cmd=='mostrar':
        for d in rows():
            if d['id']==r.id: print(json.dumps(d,ensure_ascii=False,indent=1)); return
        sys.exit('id não encontrado')
    c=conn()
    if r.cmd=='stats':
        print('Por fonte:');[print(' ',dict(x)) for x in c.execute("SELECT fonte,COUNT(*) n FROM q GROUP BY fonte")]
        print('Por tema:');[print(' ',dict(x)) for x in c.execute("SELECT tema,COUNT(*) n,SUM(padrao IS NOT NULL) com_padrao FROM q GROUP BY tema ORDER BY n DESC")]
        print('total',c.execute("SELECT COUNT(*) FROM q").fetchone()[0])
    elif r.cmd=='search':
        q="SELECT q.* FROM qf JOIN q ON q.id=qf.rowid WHERE qf MATCH ?"; ps=[r.termo]
        if r.banca: q+=" AND banca=?"; ps.append(r.banca)
        if r.ano: q+=" AND ano>=?"; ps.append(r.ano)
        if r.tema: q+=" AND q.tema LIKE ?"; ps.append('%'+r.tema+'%')
        if r.sem_padrao: q+=" AND q.padrao IS NULL"
        q+=" ORDER BY rank LIMIT ?"; ps.append(r.limit)
        for row in c.execute(q,ps): print(f"#{row['id']} [{row['gabarito']}] {row['ref']}\n  {row['tema']} › {row['subtema']}\n  {row['enunciado'][:220]}\n  {row['url']}\n")
if __name__=='__main__': main()
