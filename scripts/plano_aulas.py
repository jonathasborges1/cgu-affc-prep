#!/usr/bin/env python3
"""Divide os nucleos de um assunto em aulas de ~30 min sem cortar uma ideia ao meio.
1) custo em minutos por nucleo (recorrente 2,5; unico 1,0; fixo por aula 3,0)
2) nucleos do mesmo subitem do edital e de texto parecido formam 'blocos' (nunca divididos)
3) blocos de um subitem ficam em sequencia; os cortes caem onde o elo entre blocos vizinhos e mais fraco,
   de preferencia na fronteira entre subitens do edital
4) se um bloco nao couber na tolerancia, a aula fica longa (nao se corta)."""
import json,math,re,unicodedata,collections,os
PAD={'minutos':30.0,'min_fixo':3.0,'min_recorrente':2.5,'min_unico':1.0,'tolerancia':1.25,'limiar_bloco':0.18,'peso_equilibrio':0.6}
STOP=set('de da do das dos a o as os e em um uma para por com que se na no nas nos ao aos como mais ou nao sao pode podem ser sua seu entre sobre quando cada apenas todo toda'.split())
def params(base_dir=None):
    p=dict(PAD)
    try:
        f=os.path.join(base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'concursos','cgu-affc-ti-ds','parametros-estudo.json')
        p.update((json.load(open(f,encoding='utf-8')).get('aula') or {}))
    except Exception:pass
    return p
def toks(t):
    t=unicodedata.normalize('NFD',str(t).lower());t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    return [w[:6] for w in re.findall(r'[a-z0-9]+',t) if len(w)>2 and w not in STOP]
def sim_matrix(textos):
    docs=[collections.Counter(toks(t)) for t in textos];n=len(docs);df=collections.Counter()
    for d in docs:df.update(d.keys())
    vec=[]
    for d in docs:
        v={w:(1+math.log(f))*math.log(1+n/df[w]) for w,f in d.items()};nm=math.sqrt(sum(x*x for x in v.values())) or 1
        vec.append({w:x/nm for w,x in v.items()})
    S=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            s=sum(x*vec[j].get(w,0) for w,x in vec[i].items());S[i][j]=S[j][i]=s
    return S
def planejar(nucs,P=None):
    """nucs: lista de {'id','texto','provas','edital'}  (edital com subitem, ex. 'P3·DADOS 2.2')."""
    P=P or params();n=len(nucs)
    if n==0:return {'n_aulas':0,'minutos_total':0,'aulas':[],'params':P}
    orc=P['minutos']-P['min_fixo'];tol=P['tolerancia']
    custo=[P['min_recorrente'] if x['provas']>=2 else P['min_unico'] for x in nucs]
    S=sim_matrix([x['texto'] or x['id'] for x in nucs])
    def subnum(e):
        m=re.search(r'(\d+)\.(\d+)\s*$',e or '');return (int(m.group(1)),int(m.group(2))) if m else (0,0)
    # blocos: agrupamento hierarquico (ligacao media) dentro do mesmo subitem, limitado ao orcamento
    cl=[[i] for i in range(n)]
    def cc(c):return sum(custo[i] for i in c)
    def sm(a,b):return sum(S[i][j] for i in a for j in b)/(len(a)*len(b))
    while True:
        best=(0,None,None)
        for x in range(len(cl)):
            for y in range(x+1,len(cl)):
                if subnum(nucs[cl[x][0]]['edital'])!=subnum(nucs[cl[y][0]]['edital']):continue
                if cc(cl[x])+cc(cl[y])>orc:continue
                s=sm(cl[x],cl[y])
                if s>best[0]:best=(s,x,y)
        if best[0]<P['limiar_bloco']:break
        _,x,y=best;cl[x]=cl[x]+cl[y];del cl[y]
    # ordem: por subitem; dentro dele, encadeia blocos parecidos (vizinho mais proximo), comecando pelo mais cobrado
    por=collections.defaultdict(list)
    for c in cl:por[subnum(nucs[c[0]]['edital'])].append(c)
    seq=[]
    for k in sorted(por):
        rest=sorted(por[k],key=lambda c:-sum(nucs[i]['provas'] for i in c));cur=rest.pop(0);seq.append(cur)
        while rest:
            nx=max(rest,key=lambda c:sm(cur,c));rest.remove(nx);seq.append(nx);cur=nx
    m=len(seq);bc=[cc(c) for c in seq];tot=sum(bc)
    # penalidade de cortar entre bloco i e i+1: elo (similaridade) + 1 se for o mesmo subitem (fronteira de subitem sai de graca)
    pen=[]
    for i in range(m-1):
        mesmo=subnum(nucs[seq[i][0]]['edital'])==subnum(nucs[seq[i+1][0]]['edital'])
        pen.append((sm(seq[i],seq[i+1])+(0.5 if mesmo else 0.0)))
    pre=[0]
    for c in bc:pre.append(pre[-1]+c)
    def dividir(K):
        alvo=tot/K;INF=1e18;dp=[[INF]*(m+1) for _ in range(K+1)];bk=[[0]*(m+1) for _ in range(K+1)];dp[0][0]=0
        for k in range(1,K+1):
            for j in range(k,m+1):
                for i in range(k-1,j):
                    if dp[k-1][i]>=INF:continue
                    c=pre[j]-pre[i]
                    if c>orc*tol and j-i>1:continue
                    v=dp[k-1][i]+P['peso_equilibrio']*((c-alvo)/orc)**2+(pen[i-1] if i>0 else 0)
                    if v<dp[k][j]:dp[k][j]=v;bk[k][j]=i
        return dp,bk
    K0=max(1,math.ceil(tot/orc))
    for K in range(K0,min(m,K0+3)+1):
        dp,bk=dividir(K)
        if dp[K][m]<1e17:break
    else:
        K=min(m,K0);dp,bk=dividir(K)
    cuts=[];j=m
    for k in range(K,0,-1):cuts.append((bk[k][j],j));j=bk[k][j]
    cuts.reverse();aulas=[]
    for a,(i,j) in enumerate(cuts,1):
        ids=[x for c in seq[i:j] for x in c];ns=[nucs[x] for x in ids];c=pre[j]-pre[i]
        subs=sorted({subnum(x['edital']) for x in ns})
        top=lambda cb:max(cb,key=lambda x:(nucs[x]['provas'],-x))
        corte=None
        if j<m:
            mesmo=subnum(nucs[seq[j-1][0]]['edital'])==subnum(nucs[seq[j][0]]['edital'])
            corte='fronteira de subitem' if not mesmo else 'entre blocos com pouca ligação'
        aulas.append({'n':a,'subitens':['%d.%d'%s for s in subs if s!=(0,0)],'n_nucleos':len(ids),'n_rec':sum(1 for x in ns if x['provas']>=2),
          'min':round(c+P['min_fixo'],1),'longa':c>orc*tol,'topicos':[(nucs[top(cb)]['texto'] or nucs[top(cb)]['id'])[:90] for cb in seq[i:j]][:4],'blocos':j-i,
          'nucleos':[nucs[x]['id'] for x in ids],'corte_depois':corte})
    return {'n_aulas':len(aulas),'minutos_total':round(tot+P['min_fixo']*len(aulas),1),'n_nucleos':n,'n_blocos':m,'aulas':aulas,
            'por_aula_alvo':round(orc),'params':P}
if __name__=='__main__':
    import sys;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import painel_prioridade as PP
    v=PP.base()
    for c in sys.argv[1:] or ['P3·DADOS 2','P3·SEG 1','P3·DADOS 1']:
        ids=set(n for n,x in v['nuc'].items() if PP.cod1(x.get('edital'))==c)|set(v['nq'][c])
        nucs=[{'id':i,'texto':(v['nuc'].get(i) or {}).get('texto',''),'provas':len(v['nq'][c].get(i,())),'edital':(v['nuc'].get(i) or {}).get('edital','')} for i in sorted(ids)]
        r=planejar(nucs);print('==',c,r['n_nucleos'],'nucleos',r['n_blocos'],'blocos',r['n_aulas'],'aulas',r['minutos_total'],'min')
        for a in r['aulas']:print(' aula',a['n'],a['subitens'],a['n_nucleos'],'nuc',a['n_rec'],'rec',a['min'],'min','LONGA' if a['longa'] else '','| corte:',a['corte_depois']);[print('    -',t[:80]) for t in a['topicos'][:3]]
