#!/usr/bin/env python3
"""Estima participacao de cada assunto de P3 a partir de itens lidos (rotulos cegos).
Estratos = assunto previsto pela triagem lexical (nivel forte). Pos-estratificacao + bootstrap.
Saida: docs/precisao-triagem-p3.json e docs/recall-triagem-p3.json"""
import json,glob,os,random,collections,sys
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));C=B+'/concursos/cgu-affc-ti-ds/'
rd=lambda p:[json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]
# pools (forte) e pool de descartados
pool=collections.Counter();npool=0
for f in glob.glob(C+'escopo/*.jsonl'):
    pid=os.path.basename(f)[:-6]
    if pid.startswith('tema-'):continue
    rows=rd(f);fo=0
    for r in rows:
        c=r.get('compat');c=c if isinstance(c,dict) else {}
        if c.get('nivel')=='forte' and str(c.get('edital_prov','')).startswith('P3'):
            pool[c['edital_prov'].split('.')[0]]+=1;fo+=1
    if fo:
        e=B+'/extraidos/'+pid+'.jsonl'
        if os.path.exists(e): npool+=sum(1 for l in open(e,encoding='utf-8') if l.strip())-len(rows)
lab={}  # (prova,item)->(estrato,codigo)
# 221 originais
mp={m['id']:m for m in rd(C+'amostras/p3-verif-1-mapa.jsonl')}
for f in glob.glob(C+'classificacoes/p3-verif-1-*.jsonl'):
    for x in rd(f):
        m=mp[x['id']];lab[(m['prova_id'],str(m['item']))]=(m['triagem'],x['codigo'])
# 308 novos (sobrescrevem duplicatas) e 110 descartados
T=json.load(open(B+'/tmp/p3ext/tudo.json'));L=T['L'];nao=[]
for m in T['M']:
    c=L[m['id']]['codigo']
    if m['tipo']=='forte':lab[(m['prova_id'],str(m['item']))]=(m['triagem'],c)
    else:nao.append(c)
# censo DADOS 2 (lote classificado)
es=rd(C+'escopo/tema-p3-dados-2.jsonl');cl={str(x['item']):x for x in rd(C+'classificacoes/tema-p3-dados-2.jsonl')}
for r in es:
    c=r.get('compat');c=c if isinstance(c,dict) else {}
    if c.get('nivel')!='forte':continue
    e=cl[str(r['item'])]['edital'];cod=e.split('.')[0] if e.startswith('P3·') else 'OUTRO'
    lab[(r['prova_origem'],str(r['item_orig']))]=('P3·DADOS 2',cod)
# amostras por estrato
S=collections.defaultdict(list)
for (p,i),(s,c) in lab.items():S[s].append(c)
S['P3·DADOS 2']=[c for (p,i),(s,c) in lab.items() if s=='P3·DADOS 2']
ass=sorted(pool)
def est(S):
    real={a:0.0 for a in ass}
    for s in ass:
        n=len(S[s])
        if not n:continue
        for c in S[s]:
            if c in real:real[c]+=pool[s]/n
    return real
base=est(S);tot=sum(base.values());R=2000;random.seed(7)
bs=[];bp=collections.defaultdict(list);bpart=collections.defaultdict(list);boot=[]
for _ in range(R):
    S2={s:([random.choice(S[s]) for _ in S[s]] if len(S[s])<pool[s] else list(S[s])) for s in ass}
    r=est(S2);t=sum(r.values()) or 1
    order=sorted(ass,key=lambda a:-r[a]);rk={a:i+1 for i,a in enumerate(order)}
    boot.append({a:r[a]/t for a in ass})
    for a in ass:bpart[a].append(r[a]/t);bp[a].append(rk[a])
    for s in ass:
        n=len(S2[s]);bs.append((s,sum(c==s for c in S2[s])/max(1,n)))
pc=lambda v,q:sorted(v)[int(q*(len(v)-1))]
ordem=sorted(ass,key=lambda a:-base[a]);out={};acum=0
for k,a in enumerate(ordem,1):
    n=len(S[a]);ac=sum(c==a for c in S[a]);prec=[p for s,p in bs if s==a]
    census=n>=pool[a];part=base[a]/tot
    rk=[pc(bp[a],.05),pc(bp[a],.5),pc(bp[a],.95)]
    out[a]={'pool':pool[a],'n':n,'no_assunto':ac,'ic90':[round(ac/n,3)]*2 if census else [round(pc(prec,.05),3),round(pc(prec,.95),3)],
      'real':round(base[a],1),'part':round(part,4),'part_ic':[round(pc(bpart[a],.05),4),round(pc(bpart[a],.95),4)],
      'rank':rk,'ordem':k,'acum':round(acum+part,4),'faixa':'A' if acum<.5 else ('B' if acum<.8 else 'C'),
      'firme':rk[2]-rk[0]<=2,'amostrado':True,'censo':census}
    acum+=part
json.dump(out,open(B+'/docs/precisao-triagem-p3.json','w'),ensure_ascii=False,indent=1)
# recall
hid=collections.Counter(c for c in nao if c!='OUTRO');h=sum(hid.values());nn=len(nao)
oculto=h/nn*npool;rec=tot/(tot+oculto)
# ordem com oculto distribuido
alt={a:base[a]+hid[a]/nn*npool for a in ass};ta=sum(alt.values())
ordalt=sorted(ass,key=lambda a:-alt[a])
rc={'pool_forte':sum(pool.values()),'pool_descartados':npool,'descartados_lidos':nn,'com_p3':h,
 'taxa_oculta':round(h/nn,4),'p3_oculto_estimado':round(oculto),'p3_recuperado_estimado':round(tot),'recall_estimado':round(rec,3),
 'ordem_com_oculto':ordalt,'ordem_sem_oculto':ordem,'itens_lidos_total':sum(len(v) for v in S.values())+nn,
 'fraco_contexto_amostrados':False}
json.dump(rc,open(B+'/docs/recall-triagem-p3.json','w'),ensure_ascii=False,indent=1)
print('itens lidos forte',sum(len(v) for v in S.values()),'real total',round(tot))
for a in ordem:
    o=out[a];print(o['ordem'],a,'pool',o['pool'],'n',o['n'],'prec',o['no_assunto'],'/',o['n'],'real',o['real'],'part',o['part'],o['part_ic'],'rank',o['rank'],o['faixa'],'firme' if o['firme'] else '','censo' if o['censo'] else '')
print(json.dumps(rc,ensure_ascii=False))
print('precisao global',sum(o['no_assunto'] for o in out.values())/sum(o['n'] for o in out.values()))

# confianca da ordem (faixas estaveis e teste por ano)
import re;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import confianca_ordem as CO
yr=lambda p:int(re.search(r'(20\d{2})',p).group(1)) if re.search(r'(20\d{2})',p) else 0
labA=[(yr(p),c) for (p,i),(s_,c) in lab.items()]
CO.salvar('P3',{'recall_leitura':round(rec,3),'recall_obs':'parte do conteúdo de P3 localizada pela triagem (o restante, fora dela, só é estimado por amostra)','faixas':CO.estabilidade(boot,{a:base[a]/tot for a in ass},None),'temporal':CO.temporal(labA)})
