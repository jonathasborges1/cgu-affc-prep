#!/usr/bin/env python3
"""Suficiência de amostra por assunto do edital (P1/P2/P3) — decide onde ainda vale minerar provas.
Uso (na pasta cgu-bd):  python3 scripts/suficiencia.py [--nivel 1|2] [--so-minerar] [--json arq]
Critério (ver docs/criterio-suficiencia.md):
  1. ESTÁVEL  : a incerteza (90%, reamostrando PROVAS) sobre quantos itens da prova o assunto rende é <= ±1 item OU <= 35% do valor estimado.
  2. MASSA    : >= 20 itens "fortes" em >= 8 provas distintas (para dar aula com variedade).
  3. SUFICIENTE = ESTÁVEL e (MASSA ou assunto raro: no máximo ~1,5 item esperado na prova). Senão = MINERAR."""
import json,os,sys,random,argparse,glob,re
HERE=os.path.dirname(os.path.abspath(__file__)); D=os.environ.get('BANCO_DIR') or os.path.dirname(HERE)
ITENS_PROVA={'P1':40,'P2':40,'P3':90}
ALIAS_EDITAL={'P1 · Adm. pública 4.1':'P1·ADM 4.1'}
MIN_FORTE,MIN_PROVAS,TOL_ITENS,REL,RARO=20,8,1.0,0.35,1.5
ANO_REF=2026
MEIA_VIDA_ANOS=4.0
MIN_CLASSIF,COB_OK=15,0.7   # itens classificados (núcleos) para dar aula; fração das questões já cobertas por aula para considerar 'coberto'
def conc():
    a=os.path.join(D,'concursos','ativo.txt')
    if not os.path.exists(a): return os.path.join(D,'concursos','cgu-affc-ti-ds')
    with open(a,encoding='utf-8') as f: ativo=f.read().strip()
    return os.path.join(D,'concursos',ativo)
_LC={}
def lerj(f):
    """Leitura com cache por (arquivo, mtime, tamanho): só relê o que mudou. Devolve cópia rasa da lista."""
    try: st=os.stat(f)
    except OSError: return []
    ch=(st.st_mtime_ns,st.st_size); h=_LC.get(f)
    if h and h[0]==ch: return list(h[1])
    with open(f,encoding='utf-8') as arq: v=[json.loads(l) for l in arq if l.strip()]
    _LC[f]=(ch,v); return list(v)
def _pai(cod,nivel):
    pre,num=cod.rsplit(' ',1); return '%s %s'%(pre,num.split('.')[0]) if nivel==1 else cod
def _ano_prova(pid,meta):
    if meta.get('ano'): return int(meta['ano'])
    m=re.search(r'(20\d{2})',pid or '')
    return int(m.group(1)) if m else ANO_REF
def peso_prova(pid,var,cand):
    """Peso observacional: recencia e compatibilidade da prova com o alvo."""
    meta=dict(cand.get(pid) or {}); meta.update(var.get(pid) or {})
    rec=0.5**(max(0,ANO_REF-_ano_prova(pid,meta))/MEIA_VIDA_ANOS)
    prior=float(meta.get('prior') or 5.0)
    simil=max(.75,min(1.25,.75+.05*prior))
    return rec*simil
def calcular(nivel=1,cob=None,B=300,seed=7):
    nivel=2 if int(nivel)==2 else 1; d=conc(); prog=lerj(os.path.join(d,'programa.json')); info={x['codigo']:x for x in prog}
    var={v['prova_id']:v for v in lerj(os.path.join(d,'descoberta','varredura.jsonl')) if 'n_itens' in v}
    cand={v['prova_id']:v for v in lerj(os.path.join(d,'descoberta','candidatas.jsonl'))}
    dup={x['prova_id']+'#'+str(x['item']) for x in lerj(os.path.join(d,'descoberta','duplicatas.jsonl'))}
    ndup={}
    for k in dup: p=k.rsplit('#',1)[0]; ndup[p]=ndup.get(p,0)+1
    tam={p:max(1,v['n_itens']-ndup.get(p,0)) for p,v in var.items()}
    forte={}; fraco={}; vistos=set(); pesos={p:peso_prova(p,var,cand) for p in var}
    for f in sorted(glob.glob(os.path.join(d,'escopo','*.jsonl'))):
        if os.path.basename(f).startswith('tema-'): continue      # recortes por tema não são amostra aleatória das provas
        for e in lerj(f):
            k=e['prova_id']+'#'+str(e['item'])
            if k in dup or k in vistos or e['prova_id'] not in tam or not isinstance(e.get('compat'),dict) or ' ' not in str(e['compat'].get('edital_prov') or ''): continue
            vistos.add(k); c=_pai(e['compat']['edital_prov'],nivel)
            alvo=forte if e['compat'].get('nivel')=='forte' else fraco
            alvo.setdefault(c,{}); alvo[c][e['prova_id']]=alvo[c].get(e['prova_id'],0)+1
    provas=sorted(tam); rnd=random.Random(seed); cods=[]
    for x in prog:
        c=_pai(x['codigo'],nivel)
        if c not in cods and x['prova'] in ITENS_PROVA: cods.append(c)
    bl=lambda c: c.split('·')[0]
    am={c:[] for c in cods}
    for _ in range(B):
        ep=[provas[rnd.randrange(len(provas))] for _ in provas]; cnt={}
        for p in ep: cnt[p]=cnt.get(p,0)+1       # mesma soma de antes, agrupada por prova sorteada (só itera as provas que têm item do assunto)
        soma={c:sum(n*pesos.get(p,1)*cnt.get(p,0) for p,n in forte.get(c,{}).items()) for c in cods}; tot={}
        for c in cods: tot[bl(c)]=tot.get(bl(c),0)+soma[c]
        for c in cods: am[c].append(soma[c]/tot[bl(c)] if tot[bl(c)] else 0)
    pc=lambda v,q: sorted(v)[min(len(v)-1,int(q*len(v)))]
    ben={}
    for x in lerj(os.path.join(d,'banco.jsonl')):
        ed=ALIAS_EDITAL.get(x.get('edital'),x.get('edital') or '')
        if ed and ed!='FORA' and ' ' in ed and x.get('nucleos'): ben[_pai(ed,nivel)]=ben.get(_pai(ed,nivel),0)+1
    tf={}
    for c in cods: tf[bl(c)]=tf.get(bl(c),0)+sum(n*pesos.get(p,1) for p,n in forte.get(c,{}).items())
    L=[]
    for c in cods:
        b=bl(c); nf=sum(forte.get(c,{}).values()); np_=len(forte.get(c,{})); n_=ITENS_PROVA[b]
        massa_pond=sum(n*pesos.get(p,1) for p,n in forte.get(c,{}).items())
        sh=massa_pond/tf[b] if tf[b] else 0; lo=pc(am[c],.05); hi=pc(am[c],.95)
        conf='alta' if nf>=15 and np_>=8 else ('média' if nf>=6 and np_>=4 else 'baixa')
        x=info.get(c) or next((y for y in prog if _pai(y['codigo'],nivel)==c),{})
        meia=(hi-lo)/2*n_; estavel=meia<=TOL_ITENS or (sh*n_>0 and meia/(sh*n_)<=REL); massa=nf>=MIN_FORTE and np_>=MIN_PROVAS; raro=hi*n_<RARO
        L.append({'codigo':c,'prova':b,'bloco':x.get('bloco'),'bloco_titulo':x.get('bloco_titulo'),'texto':x.get('texto'),'forte':nf,'massa_ponderada':massa_pond,'fraco':sum(fraco.get(c,{}).values()),
                  'provas':np_,'share':sh,'lo':lo,'hi':hi,'esp':sh*n_,'esp_lo':lo*n_,'esp_hi':hi*n_,'meia':meia,'conf':conf,'banco':ben.get(c,0),'cobertura':(cob or {}).get(c),
                  'estavel':estavel,'massa':massa,'raro':raro,'lacuna':nf<3,'status':'suficiente' if estavel and (massa or raro) else 'minerar'})
    for b in ITENS_PROVA:
        S=sorted([l for l in L if l['prova']==b],key=lambda l:(-l['share'],-l['provas'],l['codigo'])); ac=0
        for i,l in enumerate(S):
            l['ordem']=i+1; l['faixa']='A' if ac<.5 else ('B' if ac<.8 else 'C'); ac+=l['share']
            if l['forte']==0: l['faixa']='C'
    L.sort(key=lambda l:(l['prova'],l['ordem']))
    for l in L: l['cor'],l['acao'],l['motivo']=recomendar(l)
    return {'nivel':nivel,'n_provas':len(provas),'n_itens_varridos':sum(tam.values()),'n_forte':sum(sum(x.values()) for x in forte.values()),'itens_prova':ITENS_PROVA,
            'modelo_fonte':{'ano_ref':ANO_REF,'meia_vida_anos':MEIA_VIDA_ANOS,'similaridade':'0.75 + 0.05 * prior, limitada a 0.75..1.25'},
            'criterio':{'min_forte':MIN_FORTE,'min_provas':MIN_PROVAS,'tol_itens':TOL_ITENS,'rel':REL,'raro':RARO},'linhas':L}
def recomendar(l):
    """Semáforo de maturidade: 3 perguntas em ordem. Devolve cor, ação e motivo (texto curto)."""
    c=l.get('cobertura') or {}; tot=c.get('total') or 0; cob=c.get('cobertas') or 0; fr=cob/tot if tot else 0
    if l['lacuna']: return ('cinza','Ensinar pela base legal','só %d item(ns) forte(s) em %d provas: não há histórico a minerar'%(l['forte'],l['provas']))
    if l['status']!='suficiente':
        why=[]
        if not l['estavel']: why.append('incerteza de ±%.1f itens'%l['meia'])
        if not l['massa'] and not l['raro']:
            if l['forte']<MIN_FORTE: why.append('%d de %d itens fortes'%(l['forte'],MIN_FORTE))
            if l['provas']<MIN_PROVAS: why.append('%d de %d provas'%(l['provas'],MIN_PROVAS))
        return ('vermelho','Minerar mais provas','; '.join(why) or 'amostra insuficiente')
    if l['banco']<MIN_CLASSIF: return ('amarelo','Classificar itens','amostra suficiente, mas só %d de %d itens classificados no banco (triagem tem %d fortes)'%(l['banco'],MIN_CLASSIF,l['forte']))
    if tot==0 or fr<COB_OK: return ('verde','Pronto: criar aula','%d itens classificados%s'%(l['banco'],(' · %d questões sem aula'%(tot-cob)) if tot else ' · nenhuma aula ainda'))
    return ('azul','Coberto: caderno e revisão','aula cobre %d/%d questões'%(cob,tot))
def resumo(r):
    out=[]
    for b in ITENS_PROVA:
        L=[l for l in r['linhas'] if l['prova']==b]; m=[l for l in L if l['status']=='minerar']
        out.append('%s: %d assuntos, %d suficientes, %d a minerar'%(b,len(L),len(L)-len(m),len(m)))
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--nivel',type=int,default=1); ap.add_argument('--so-minerar',action='store_true'); ap.add_argument('--json')
    a=ap.parse_args(); r=calcular(a.nivel)
    print('provas varridas %d | itens %d | fortes %d'%(r['n_provas'],r['n_itens_varridos'],r['n_forte']))
    for t in resumo(r): print(' ',t)
    for l in r['linhas']:
        if a.so_minerar and l['status']!='minerar': continue
        print('%s %-16s forte=%3d provas=%2d part=%5.1f%% ±%.1f itens esp=%.1f %s%s%s %s'%(l['faixa'],l['codigo'],l['forte'],l['provas'],100*l['share'],l['meia'],l['esp'],
              'E' if l['estavel'] else '-','M' if l['massa'] else '-','R' if l['raro'] else '-',l['status'].upper()+(' (lacuna)' if l['lacuna'] else '')))
    if a.json: json.dump(r,open(a.json,'w',encoding='utf-8'),ensure_ascii=False)
