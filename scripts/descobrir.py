#!/usr/bin/env python3
"""Descoberta otimizada de provas Cebraspe com ITENS compatíveis com o programa do concurso ativo.
Tudo local (zero créditos do Claude). Uso (na pasta cgu-bd):
  python3 scripts/descobrir.py catalogo [--ano-min 2021] [--pausa 0.4]     baixa/atualiza o catálogo (API pública do Cebraspe) em cache
  python3 scripts/descobrir.py ranquear [--top 40]                          prior por metadados -> descoberta/candidatas.jsonl
  python3 scripts/descobrir.py varrer [--max-provas 12] [--alvo-bloco 6]    baixa em ordem, extrai itens, mede compatibilidade por ITEM, grava escopo/
  python3 scripts/descobrir.py relatorio                                    resumo (itens compatíveis por bloco do edital)
Regras: item compatível é SEMPRE preservado (escopo/ID.jsonl), mesmo se a prova tiver 1 só; a prova só é descartada
depois de medida (download é barato). A ordem de visita vem do prior de metadados para minimizar provas inúteis."""
import collections,sys,os,re,json,math,time,argparse,unicodedata,urllib.request,shutil,hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE))
import banco as B
API='https://apis.cebraspe.org.br/cebraspe/eventos/'
CDN='https://cdn.cebraspe.org.br/concursos/%s/arquivos/%s'
DESC=B.PC('descoberta'); os.makedirs(DESC,exist_ok=True)
def sa(s): return ''.join(c for c in unicodedata.normalize('NFD',s or '') if unicodedata.category(c)!='Mn').lower()
def get(url,pausa=0.4):
    rq=urllib.request.Request(url,headers={'User-Agent':B.UA,'Accept':'application/json'})
    with urllib.request.urlopen(rq,timeout=40) as r: d=r.read()
    time.sleep(pausa); return json.loads(d) if d else None
# ---------------- 1. catálogo
def catalogo(a):
    lst=get(API+'tipo/concursos/',0)
    ev=[e for g in lst for e in g['eventos']]
    ev=[e for e in ev if (e.get('eventoAno') or 0)>=a.ano_min and not e['eventoStatus'] in ('novos',)]
    cache=B.PC('descoberta','catalogo.jsonl'); feito={d['eventoURL']:d for d in B.lerj(cache)}
    t0=time.time(); n=0
    for e in ev:
        u=e['eventoURL']
        if u in feito and not a.refazer: continue
        if time.time()-t0>a.tempo: print('tempo esgotado; rode de novo para continuar'); break
        try: d=get(API+u,a.pausa)
        except Exception as x: print('falha',u,x); continue
        if d: feito[u]={k:d.get(k) for k in ('eventoURL','eventoNomeAbreviado','eventoNomeCompleto','eventoAno','eventoStatus','eventoCargos','arquivosGabarito')}; n+=1
        if n%20==0: B.escj(cache,list(feito.values()))
    B.escj(cache,list(feito.values())); print('catalogo: %d eventos em cache (%d novos); alvo %d'%(len(feito),n,len(ev)))
# ---------------- 2. pares prova+gabarito
def pares(ev):
    arq={x['nomeArquivo']:x for x in (ev.get('arquivosGabarito') or [])}
    out=[]
    for nome in arq:
        if nome.upper().startswith(('GAB','PROVA_DISC','PADRO','PADRAO')): continue
        if not nome.upper().endswith('.PDF'): continue
        g='GAB_DEFINITIVO_'+nome
        gg=next((k for k in arq if k.upper()==g.upper()),None)
        if gg: out.append((nome,gg,arq[nome].get('descricaoArquivo') or nome))
    return out
def cargo_de(nome,ev):
    """liga o arquivo ao texto do cargo pelo número (…_004_01 -> idArea 04). CG = conhecimentos gerais."""
    m=re.search(r'_(\d{3})_\d\d\.PDF$',nome.upper())
    if re.search(r'_CG\d*_',nome.upper()): return 'CG','conhecimentos gerais (bloco comum)'
    if not m: return None,''
    n=int(m.group(1))
    for c in ev.get('eventoCargos') or []:
        try:
            if int(c['idArea'])==n: return str(n),c['area']
        except ValueError: pass
    return str(n),''
# prior de metadados (palavras no texto do cargo / órgão). Pesos iniciais: calibráveis.
PRIOR=[(r'tecnologia da informacao|\bti\b|sistemas|desenvolvimento|informatica|analista de sistemas|dados|seguranca da informacao',3.0),
       (r'desenvolvimento de sistemas|sistemas de informacao|software|sistemas de informação',1.5),
       (r'controle|auditor|fiscal|controladoria|tribunal de contas|tce|tcu|cgu',2.5),
       (r'planejamento|orcamento|gestao publica|administracao|governanca|integridade',1.5),
       (r'ministerio|agencia|autarquia|instituto|banco|tribunal|senado|camara|cgdf|df\b',0.5)]
def prior(ev,cargo_txt,nome):
    t=sa(cargo_txt+' '+(ev.get('eventoNomeCompleto') or '')+' '+(ev.get('eventoNomeAbreviado') or ''))
    s=sum(w for rx,w in PRIOR if re.search(rx,t))
    ano=ev.get('eventoAno') or 2000; s+=max(0,(ano-2020))*0.35          # recência
    if cargo_txt=='conhecimentos gerais (bloco comum)': s+=1.5           # CG cobre P1/P2 de uma vez
    if re.search(r'especialidade: geral|\bgeral\b',t) and 'tecnologia' not in t: s-=0.5
    return round(s,2)
def slug_area(txt):
    """'CARGO 6: ANALISTA DE TI – ÁREA: GESTÃO DE DADOS' -> 'gestao-dados'"""
    m=re.search(r'(?:area|especialidade|enfase|perfil|area de atuacao)[^:\u2013-]*[:\u2013-]+\s*(.+)',sa(txt))
    base=m.group(1) if m else (sa(txt).split(':',1)[-1])
    ws=[w for w in re.findall(r'[a-z0-9]+',base) if w not in ('de','da','do','das','dos','e','em','a','o','para','com')]
    return '-'.join(ws[:4])[:36].strip('-')
def novo_pid(ev,nome,cid,ctxt):
    org='-'.join(w for w in sa(ev['eventoURL']).split('_') if not re.fullmatch(r'\d{2}',w))
    org=re.sub(r'[^a-z0-9-]','-',org).strip('-')
    c='cg' if cid=='CG' else ('c%02d'%int(cid) if cid else 'x')
    sl='bloco-comum' if cid=='CG' else slug_area(ctxt)
    return '-'.join(x for x in (org,str(ev.get('eventoAno')),c,sl) if x)
def ranquear(a):
    cat=B.lerj(B.PC('descoberta','catalogo.jsonl')); cand=[]
    ja={p['prova_id'] for p in B.provas()}
    for ev in cat:
        for nome,gab,desc in pares(ev):
            cid,ctxt=cargo_de(nome,ev)
            pid_antigo=sa(ev['eventoURL']).replace('_','-')+'-'+re.sub(r'[^a-z0-9]','',sa(nome[:-4]))[-12:]
            pid=novo_pid(ev,nome,cid,ctxt or desc)
            cand.append({'prova_id':pid,'evento':ev['eventoURL'],'ano':ev.get('eventoAno'),'orgao':ev.get('eventoNomeAbreviado'),
                         'cargo':ctxt or desc,'arquivo':nome,'arquivo_gab':gab,'prior':prior(ev,ctxt or desc,nome),'visitada':pid in ja,'pid_antigo':pid_antigo})
    cand.sort(key=lambda c:-c['prior']); B.escj(B.PC('descoberta','candidatas.jsonl'),cand)
    print('%d provas candidatas (pares prova+gabarito). Topo do ranking:'%len(cand))
    for c in cand[:a.top]: print('%5.2f %s %s | %s'%(c['prior'],c['ano'],c['orgao'],c['cargo'][:80]))
# ---------------- 3. compatibilidade por item (BM25 local contra programa.json)
STOP=set(sa('a o as os um uma de do da dos das em no na nos nas por para com sem sob sobre entre e ou que se ao aos à às pelo pela pelos pelas como mais menos ser estar ter sua seu suas seus este esta isso essa esse mesmo cada outro outra quando onde qual quais apenas sempre nunca todo toda todos todas segundo acerca julgue item itens seguinte seguintes proposto considerando forma sendo pode podem deve devem caso assim ainda tambem entao ja nao sim sao foi sera ha pois porem entretanto portanto contudo').split())
def toks(s):
    out=[]
    for w in re.findall(r'[a-z0-9]+',sa(s)):
        if w in STOP or len(w)<3: continue
        out.append(w[:6] if len(w)>6 else w)           # radical grosseiro (6 letras)
    return out
class Indice:
    def lex(s,cod):
        return ' '.join(v for k,v in s.L.items() if cod==k or cod.startswith(k+'.') or (cod.startswith(k) and not cod[len(k)].isdigit() and cod[len(k)]!='.' and False))
    def __init__(s,prog):
        s.L={}
        try: s.L=json.load(open(B.PC('lexico.json'),encoding='utf-8'))
        except OSError: pass
        s.docs=[]; s.cod=[]
        for d in prog:
            if d['nivel']<2 and d['num'].count('.')==0 and not d['num'].isdigit(): continue
            txt=d['texto']+' '+(d.get('bloco_titulo') or '')+' '+s.lex(d['codigo'])
            s.docs.append(toks(txt)); s.cod.append(d['codigo'])
        s.N=len(s.docs); s.df={}
        for dd in s.docs:
            for t in set(dd): s.df[t]=s.df.get(t,0)+1
        s.avg=sum(map(len,s.docs))/max(1,s.N)
    def idf(s,t): return math.log(1+(s.N-s.df.get(t,0)+0.5)/(s.df.get(t,0)+0.5))
    def score(s,q):
        qs=set(toks(q)); melhor=(0,None,[])
        for dd,c in zip(s.docs,s.cod):
            tf={};
            for t in dd: tf[t]=tf.get(t,0)+1
            sc=0; hit=[]
            for t in qs:
                if t in tf:
                    f=tf[t]; sc+=s.idf(t)*f*2.2/(f+1.2*(0.25+0.75*len(dd)/s.avg)); hit.append(t)
            if sc>melhor[0]: melhor=(sc,c,hit)
        return melhor
def compat_itens(itens,ind,forte,fraco):
    """marca cada item: forte/fraco/nao; expande para o mesmo contexto (itens que dividem texto-base)."""
    res={}
    for it in itens:
        sc,cod,hit=ind.score(it['enunciado'])
        nivel='forte' if sc>=forte and len(hit)>=2 else ('fraco' if sc>=fraco and len(hit)>=2 else 'nao')
        res[it['item']]={'score':round(sc,2),'edital_prov':cod,'termos':hit[:6],'nivel':nivel}
    ctx={}
    for it in itens: ctx.setdefault(it.get('contexto') or '',[]).append(it['item'])
    for c,ids in ctx.items():
        if len(c)>150 and len(ids)>1 and any(res[i]['nivel']=='forte' for i in ids):
            for i in ids:
                if res[i]['nivel']=='nao': res[i]['nivel']='contexto'
    return res
def varrer(a):
    prog=B.programa(); ind=Indice(prog)
    cand=B.lerj(B.PC('descoberta','candidatas.jsonl'))
    cfg=B.lerj(B.PC('descoberta','varredura.jsonl')); visto={c['prova_id']:c for c in cfg}
    # Blacklist persistente: identidade por URLs e hashes evita repetir PDFs entre concursos/IDs.
    provas_locais=B.provas(); urls={u for p in provas_locais for u in (p.get('url'),p.get('url_gab')) if u}
    hashes={h for p in provas_locais for h in (p.get('hash') or {}).values() if h}
    raiz_provas=os.path.dirname(os.path.dirname(B.PC('descoberta','x')))
    for root,dirs,files in os.walk(raiz_provas):
        dirs[:]=[x for x in dirs if x not in {'.git','__pycache__'}]
        if 'prova.pdf' in files and 'gabarito.pdf' in files:
            for nome in ('prova.pdf','gabarito.pdf'):
                f=os.path.join(root,nome)
                if B.eh_pdf(f): hashes.add(B.sha(f))
    for p in provas_locais:
        hs=B.hashes_pasta(p['prova_id'])
        if hs: hashes.update(hs.values())
    t0=time.time(); ganho_hist=[]
    cob={}                                           # edital provável -> nº itens compatíveis já reunidos
    for c in cfg:
        for k,v in (c.get('por_edital') or {}).items(): cob[k]=cob.get(k,0)+v
    feitas=0
    for c in cand:
        if c['prova_id'] in visto: continue
        if feitas>=a.max_provas: print('parada: máximo de provas desta rodada'); break
        if time.time()-t0>a.tempo: print('parada: tempo da chamada (rode de novo, continua de onde parou)'); break
        pid=c['prova_id']; d=B.pdir(pid); os.makedirs(d,exist_ok=True)
        urlp=CDN%(c['evento'],c['arquivo']); urlg=CDN%(c['evento'],c['arquivo_gab'])
        if urlp in urls or urlg in urls:
            visto[pid]={'prova_id':pid,'pulada':'duplicata_url'}; B.escj(B.PC('descoberta','varredura.jsonl'),list(visto.values())); print('pulada (URL já registrada):',pid); continue
        # Se já existem PDFs para este candidato, valide e registre os hashes antes de reutilizar.
        for nome,url in (('prova.pdf',urlp),('gabarito.pdf',urlg)):
            local=os.path.join(d,nome)
            if B.eh_pdf(local):
                h=B.sha(local)
                if h in hashes:
                    visto[pid]={'prova_id':pid,'pulada':'duplicata_hash'}; B.escj(B.PC('descoberta','varredura.jsonl'),list(visto.values())); print('pulada (hash já registrado):',pid); shutil.rmtree(d,ignore_errors=True); break
                hashes.add(h)
        if pid in visto: continue
        # Reaproveita downloads parciais válidos; nunca baixa o mesmo PDF de novo.
        if not B.eh_pdf(os.path.join(d,'prova.pdf')) or not B.eh_pdf(os.path.join(d,'gabarito.pdf')):
            if any(B.eh_pdf(os.path.join(d,n)) for n in ('prova.pdf','gabarito.pdf')):
                hashes.discard(B.sha(os.path.join(d,'prova.pdf'))) if B.eh_pdf(os.path.join(d,'prova.pdf')) else None
                hashes.discard(B.sha(os.path.join(d,'gabarito.pdf'))) if B.eh_pdf(os.path.join(d,'gabarito.pdf')) else None
        try:
            if not B.eh_pdf(os.path.join(d,'gabarito.pdf')): B.baixa(urlg,os.path.join(d,'gabarito.pdf'),0.4)
            B.pdf_texto(os.path.join(d,'gabarito.pdf'),os.path.join(d,'gabarito.txt'),layout=True)
            gtxt=open(os.path.join(d,'gabarito.txt'),encoding='utf-8').read()
            if not B.gab_parse(gtxt):          # gabarito sem tabela Item/Gabarito C-E: prova de múltipla escolha (ou formato novo)
                mot='multipla_escolha' if re.search(r'^Quest[aã]o\s+\d+',gtxt,re.M) else 'gabarito_ilegivel'
                print('pulada (%s): %s'%(mot,pid)); visto[pid]={'prova_id':pid,'pulada':mot,'cargo':c['cargo']}; shutil.rmtree(d,ignore_errors=True)
                B.escj(B.PC('descoberta','varredura.jsonl'),list(visto.values())); continue
            if not B.eh_pdf(os.path.join(d,'prova.pdf')): B.baixa(urlp,os.path.join(d,'prova.pdf'),0.4)
            B.pdf_texto(os.path.join(d,'gabarito.pdf'),os.path.join(d,'gabarito.txt'),layout=True)
            gab=B.gab_parse(open(os.path.join(d,'gabarito.txt'),encoding='utf-8').read())
            vistos,metodo=B.texto_melhor(pid,gab)
        except BaseException as x:
            msg=str(x); print('falha',pid,msg[:80])
            if re.search(r'403|429|forbidden|too many requests',msg,re.I):
                sys.exit('BLOQUEIO CDN detectado; interrompendo varredura sem contornar: '+msg[:120])
            # Falha transitória não vira item visitado e pode ser retomada na próxima rodada.
            visto.pop(pid,None); B.escj(B.PC('descoberta','varredura.jsonl'),list(visto.values())); shutil.rmtree(d,ignore_errors=True); continue
        itens=[dict(v,gabarito=gab.get(v['item'])) for v in sorted(vistos.values(),key=lambda v:v['item'])]
        comp=compat_itens(itens,ind,a.forte,a.fraco)
        ok=[i for i in itens if comp[i['item']]['nivel']!='nao' and gab.get(i['item'])!='ANULADO']
        por={}
        for i in ok:
            k=(comp[i['item']]['edital_prov'] or '').split(' ')[0]+' '+(comp[i['item']]['edital_prov'] or '').split('·')[-1].split(' ')[0]
            por[comp[i['item']]['edital_prov']]=por.get(comp[i['item']]['edital_prov'],0)+1
        reg={'prova_id':pid,'n_itens':len(itens),'n_gab':len(gab),'n_compat':len(ok),
             'n_forte':sum(1 for i in ok if comp[i['item']]['nivel']=='forte'),'por_edital':por,'prior':c['prior'],'cargo':c['cargo'],'extracao_incompleta':len(itens)<len(gab),'metodo_texto':metodo,'n_vazios':sum(1 for i in itens if len(i['enunciado'])<25)}
        feitas+=1
        # grava SEMPRE o que for compatível (nem que seja 1 item); só descarta os arquivos pesados se 0
        if ok:
            ref='Cebraspe %s %s · %s'%(c['orgao'],c['ano'],c['cargo'])
            lst=[x for x in B.provas() if x['prova_id']!=pid]
            p={'prova_id':pid,'ref':ref,'url':CDN%(c['evento'],c['arquivo']),'url_gab':CDN%(c['evento'],c['arquivo_gab']),'ano':c['ano'],
               'orgao':c['orgao'],'cargo':c['cargo'],'peso':1.0,'hash':B.hashes_pasta(pid),'n_itens':len(itens),'n_gab':len(gab),'verificacao':None,'historico':[]}
            for e in ('descoberta','baixada'): B.hist(p,e,'descobrir.py')
            B.prova_put(p)
            urls.update((urlp,urlg)); hashes.update((p.get('hash') or {}).values())
            full=[dict({'prova_id':pid,'banca':'Cebraspe','orgao':c['orgao'],'cargo':c['cargo'],'ano':c['ano'],'ref':ref,'url':p['url'],'url_gab':p['url_gab']},**i) for i in itens]
            B.escj(B.P('extraidos',pid+'.jsonl'),full); B.hist(p,'extraida','descobrir.py: %d itens, %d compatíveis'%(len(itens),len(ok))); B.prova_put(p)
            B.escj(B.PC('escopo',pid+'.jsonl'),[dict(i,compat=comp[i['item']]) for i in full if i['item'] in {o['item'] for o in ok}])
            for k,v in por.items(): cob[k]=cob.get(k,0)+v
        else:
            shutil.rmtree(d,ignore_errors=True)       # 0 itens compatíveis: nada a preservar
        visto[pid]=reg; B.escj(B.PC('descoberta','varredura.jsonl'),list(visto.values()))
        print('%-34s itens=%3d/%3d compat=%2d (fortes %2d) prior=%.1f%s | %s'%(pid,len(itens),len(gab),len(ok),reg['n_forte'],c['prior'],(' EXTRACAO INCOMPLETA' if reg['extracao_incompleta'] else '')+' ['+metodo+']',c['cargo'][:44]))
        ganho_hist.append(len(ok))
        if len(ganho_hist)>=4 and sum(ganho_hist[-4:])<=a.ganho_min: print('parada: ganho marginal baixo nas últimas 4 provas'); break
        if sum(cob.values())>=a.alvo_total: print('parada: alvo total de itens compatíveis atingido (%d)'%sum(cob.values())); break
def pacote(a):
    """Pacote compacto p/ classificador/verificador: itens do escopo + 3 códigos candidatos do edital (+ núcleos existentes do tema)."""
    prog=B.programa(); ind=Indice(prog); txt={d['codigo']:d['texto'] for d in prog}
    it=B.lerj(B.PC('escopo',a.id+'.jsonl')) or B.lerj(B.P('extraidos',a.id+'.jsonl'))
    if a.itens: it=[i for i in it if str(i['item']) in a.itens.split(',')]
    nuc=B.lerj(B.NUC); cods={}
    out=['# PACOTE %s (%d itens)'%(a.id,len(it)),'Para cada item: edital (código de CANDIDATOS ou FORA), núcleo, tags, nível. Gabarito: C=certo E=errado.','']
    for i in it:
        sc=[]
        for dd,c in zip(ind.docs,ind.cod):
            qs=set(toks(i['enunciado'])); s=sum(ind.idf(w) for w in qs if w in dd)
            sc.append((s,c))
        top=[c for s,c in sorted(sc,reverse=True)[:3] if s>0]
        for c in top: cods[c]=txt[c]
        if a.alvo: top=[c for c in top if not B.ematch(c,a.alvo)]+[]; top=[c for c in txt if B.ematch(c,a.alvo) and c.count('.')>0 and sc and False]+top
        ctx=(' [texto-base: '+i['contexto'][:200]+']') if len(i.get('contexto',''))>150 else ''
        out.append('## %s | gab=%s | cand: %s%s\n%s'%(i['item'],i.get('gabarito'),', '.join(top),ctx,i['enunciado'][:a.max]))
    if a.alvo:
        for c in txt:
            if B.ematch(c,a.alvo): cods[c]=txt[c]
        out.insert(2,'TEMA ALVO: %s. Para cada item, use PRIMEIRO os códigos do tema alvo (lista abaixo); FORA só se nenhum código da lista toda (alvo + candidatos) tratar do assunto.'%a.alvo)
    out+=['','## CÓDIGOS CANDIDATOS (texto do edital)']+['- %s: %s'%(c,v[:160]) for c,v in sorted(cods.items())]
    if not a.sem_nucleos:
        out+=['','## NÚCLEOS JÁ EXISTENTES (reutilize o id se for a mesma ideia)']+['- %s: %s'%(n['id'],(n.get('texto') or '')[:110]) for n in nuc if any(ekey_ok(n.get('edital'),c) for c in cods)]
    s='\n'.join(out); os.makedirs(B.PC('pacotes'),exist_ok=True); open(B.PC('pacotes',a.id+('-verif' if a.sem_nucleos else '')+'.md'),'w',encoding='utf-8').write(s)
    print('pacote: %d itens, %d caracteres (~%d tokens)'%(len(it),len(s),len(s)//4))
def ekey_ok(a,b): return B.ekey(a)==B.ekey(b)
def reextrair(a):
    """Reprocessa (local, sem rede) as provas ainda não classificadas com o extrator atual; recalcula escopo."""
    ind=Indice(B.programa()); n=0
    for p in B.provas():
        pid=p['prova_id']
        if p['estado'] in ('persistida','classificada','verificada') or not os.path.exists(B.pdir(pid)+'/gabarito.txt'): continue
        gab=B.gab_parse(open(B.pdir(pid)+'/gabarito.txt',encoding='utf-8').read())
        vistos,metodo=B.texto_melhor(pid,gab); ex0=B.lerj(B.P('extraidos',pid+'.jsonl'))
        meta={k:ex0[0][k] for k in ('prova_id','banca','orgao','cargo','ano','ref','url','url_gab') if k in ex0[0]} if ex0 else {}
        itens=[dict(meta,**dict(v,gabarito=gab.get(v['item']))) for v in sorted(vistos.values(),key=lambda v:v['item'])]
        comp=compat_itens(itens,ind,a.forte,a.fraco); ok=[i for i in itens if comp[i['item']]['nivel']!='nao' and gab.get(i['item'])!='ANULADO']
        B.escj(B.P('extraidos',pid+'.jsonl'),itens); B.escj(B.PC('escopo',pid+'.jsonl'),[dict(i,compat=comp[i['item']]) for i in ok])
        vz=sum(1 for i in itens if len(i['enunciado'])<25); n+=1
        print('%-52s itens=%d/%d vazios=%d compat=%d [%s]'%(pid[:52],len(itens),len(gab),vz,len(ok),metodo))
    print(n,'provas reprocessadas')
def dedupe(a):
    """Remove dos escopos a questão repetida em outro cargo (mesmo concurso) ou já presente no banco; guarda rastro em duplicatas.jsonl."""
    vistos={B.nkey(d.get('enunciado')):'banco' for d in B.rows()}; rastro=[]; tot=0
    for p in B.provas():
        pid=p['prova_id']
        if p['estado'] in ('persistida','classificada','verificada'): continue
        esc=B.lerj(B.PC('escopo',pid+'.jsonl')); novo=[]
        for i in esc:
            k=B.nkey(i['enunciado'])
            if k in vistos: rastro.append({'prova_id':pid,'item':i['item'],'igual_a':vistos[k]}); tot+=1
            else: vistos[k]=pid+'#'+str(i['item']); novo.append(i)
        B.escj(B.PC('escopo',pid+'.jsonl'),novo)
        print('%-52s escopo %d -> %d'%(pid[:52],len(esc),len(novo)))
    B.escj(B.PC('descoberta','duplicatas.jsonl'),rastro); print('duplicatas removidas:',tot)
def tema(a):
    """Lote por TEMA: junta os itens do escopo de todas as provas pendentes que caem na seção do edital (ex.: 'P3·SEG 1')
    numa prova-lote (id tema-...), que atravessa classificar -> verificar -> aplicar como qualquer prova."""
    pid=a.id or 'tema-'+re.sub(r'[^a-z0-9]+','-',sa(a.codigo)).strip('-'); itens=[]; n=0
    for p in B.provas():
        if p['estado'] in ('persistida',) or p['prova_id'].startswith('tema-'): continue
        for i in B.lerj(B.PC('escopo',p['prova_id']+'.jsonl')):
            if B.ematch(i['compat'].get('edital_prov'),a.codigo) and i['compat']['nivel'] in a.niveis.split(','):
                n+=1; j={k:v for k,v in i.items() if k!='compat'}; j.update({'item_orig':i['item'],'prova_origem':p['prova_id'],'item':str(n),'compat':i['compat']}); itens.append(j)
    if not itens: sys.exit('nenhum item')
    B.escj(B.P('extraidos',pid+'.jsonl'),[{k:v for k,v in j.items() if k!='compat'} for j in itens]); B.escj(B.PC('escopo',pid+'.jsonl'),itens)
    lst=[x for x in B.provas() if x['prova_id']!=pid]
    pr={'prova_id':pid,'ref':'Lote por tema %s (itens de %d provas)'%(a.codigo,len({j['prova_origem'] for j in itens})),'url':'lote','url_gab':'lote','ano':2024,'orgao':'varias','cargo':a.codigo,'peso':1.0,'hash':None,'n_itens':len(itens),'n_gab':len(itens),'verificacao':None,'historico':[]}
    for e in ('descoberta','baixada','extraida'): B.hist(pr,e,'lote por tema (itens vindos de provas já baixadas)')
    B.prova_put(pr); print('lote %s: %d itens de %d provas'%(pid,len(itens),len({j['prova_origem'] for j in itens})))
    for k,v in collections.Counter(j['prova_origem'][:34] for j in itens).most_common(): print('  %3d  %s'%(v,k))
def relatorio(a):
    v=[x for x in B.lerj(B.PC('descoberta','varredura.jsonl')) if 'n_itens' in x]
    tot=sum(x['n_itens'] for x in v); ok=sum(x['n_compat'] for x in v)
    print('provas varridas: %d | itens vistos: %d | compatíveis preservados: %d (%.0f%%)'%(len(v),tot,ok,100*ok/max(1,tot)))
    cob={}
    for x in v:
        for k,n in x['por_edital'].items(): cob[k]=cob.get(k,0)+n
    for k,n in sorted(cob.items(),key=lambda kv:-kv[1])[:25]: print('%4d  %s'%(n,k))
    for x in sorted(v,key=lambda x:-x['n_compat'])[:15]: print('  %-34s %3d/%3d prior=%.1f %s'%(x['prova_id'],x['n_compat'],x['n_itens'],x['prior'],x['cargo'][:48]))
if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    c=sp.add_parser('catalogo'); c.add_argument('--ano-min',type=int,default=2021); c.add_argument('--pausa',type=float,default=0.4); c.add_argument('--tempo',type=int,default=150); c.add_argument('--refazer',action='store_true')
    r=sp.add_parser('ranquear'); r.add_argument('--top',type=int,default=40)
    v=sp.add_parser('varrer'); v.add_argument('--max-provas',type=int,default=12); v.add_argument('--tempo',type=int,default=150)
    v.add_argument('--forte',type=float,default=10.0); v.add_argument('--fraco',type=float,default=8.0)
    v.add_argument('--ganho-min',type=int,default=2); v.add_argument('--alvo-total',type=int,default=300)
    k=sp.add_parser('pacote'); k.add_argument('id'); k.add_argument('--itens'); k.add_argument('--max',type=int,default=420); k.add_argument('--sem-nucleos',action='store_true'); k.add_argument('--alvo')
    rx=sp.add_parser('reextrair'); rx.add_argument('--forte',type=float,default=10.0); rx.add_argument('--fraco',type=float,default=8.0)
    sp.add_parser('dedupe'); tm=sp.add_parser('tema'); tm.add_argument('codigo'); tm.add_argument('--id'); tm.add_argument('--niveis',default='forte,fraco,contexto')
    sp.add_parser('relatorio')
    a=ap.parse_args(); {'catalogo':catalogo,'ranquear':ranquear,'varrer':varrer,'relatorio':relatorio,'pacote':pacote,'reextrair':reextrair,'dedupe':dedupe,'tema':tema}[a.cmd](a)
