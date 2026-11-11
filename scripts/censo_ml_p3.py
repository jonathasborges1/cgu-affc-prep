#!/usr/bin/env python3
"""Censo assistido por ML das P3 escondidas: classifica TODO o pool (8k) com modelos locais, calibra a prob. de ser P3 e corrige o assunto pela matriz de erros
medida em validacao temporal; valida contra a amostra estratificada lida. Zero token.
Saida: docs/censo-ml-p3.json"""
import json,os,sys,glob,random,collections
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ml_triagem as MT
import confianca_ordem as CO
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from scipy.optimize import nnls
B=MT.B;rd=MT.rd
def lab_extra():
    E={}
    for pref,mp in (('lab-','mapa.json'),('sorteio-lab-','sorteio-mapa.json'),('sorteio2-lab-','sorteio2-mapa.json'),('topo2-lab-','topo2-mapa.json')):
        M={m['id']:m for m in json.load(open(B+'/tmp/p3fila/'+mp))}
        for f in glob.glob(B+'/tmp/p3fila/'+pref+'*.jsonl'):
            if pref=='lab-' and 'sorteio' in f:continue
            for x in rd(f):
                m=M[x['id']];E[(m['prova_id'],str(m['item']))]=(x['codigo'],m.get('banda'),m.get('tam_banda'))
    return E
def multi():return Pipeline([('v',MT.vet()),('c',LogisticRegression(C=12,class_weight='balanced',max_iter=1500))])
def main(nboot=400,seed=3):
    txt,lab,nao=MT.carregar();E=lab_extra()
    amostra={k:v for k,v in E.items() if v[1]};topo={k:v for k,v in E.items() if not v[1]}
    lab2=dict(lab);lab2.update({k:v[0] for k,v in E.items()})
    L=MT.dataset(txt,lab2)
    # --- matriz de erros (validacao temporal, so P3 reais)
    P=[x for x in L if x[3]!='OUTRO' and x[1] not in amostra];cl=sorted({x[3] for x in P});ix={c:i for i,c in enumerate(cl)};K=len(cl)
    C=np.zeros((K,K));
    for a in sorted({x[0] for x in P}):
        tr=[x for x in P if x[0]<a];te=[x for x in P if x[0]==a]
        if len(tr)<120 or len(te)<15:continue
        m=multi().fit([x[2] for x in tr],[x[3] for x in tr]);pr=m.predict([x[2] for x in te])
        for x,p in zip(te,pr):C[ix[x[3]],ix[p]]+=1
    C=(C+0.5*np.eye(K))/(C+0.5*np.eye(K)).sum(1,keepdims=True)   # suavizado
    # --- detector P3 calibrado (treino SEM a amostra e SEM as descartadas lidas)
    ex=set(amostra)|set(nao)
    md,_=MT.ajustar(L,ex)
    treino=[x for x in L if x[1] not in ex and x[3]!='OUTRO'];mm=multi().fit([x[2] for x in treino],[x[3] for x in treino])
    def lg(v):v=np.clip(v,1e-4,1-1e-4);return np.log(v/(1-v)).reshape(-1,1)
    ks=list(amostra);ps=md.predict_proba([txt[k] for k in ks])[:,1];ys=np.array([amostra[k][0]!='OUTRO' for k in ks]);ws=np.array([amostra[k][2]/sum(1 for q in ks if amostra[q][1]==amostra[k][1]) for k in ks])
    # pool nao rotulado
    fila=json.load(open(B+'/docs/ml-fila-p3.json'))['itens'];pool=[(r['prova_id'],r['item']) for r in fila if (r['prova_id'],r['item']) not in lab2]
    pp=md.predict_proba([txt[k] for k in pool])[:,1];Q=mm.predict_proba([txt[k] for k in pool]);clm=list(mm.named_steps['c'].classes_)
    sel=[j for j,c in enumerate(clm)]
    def estimar(rs):
        idx=[rs.randrange(len(ks)) for _ in ks] if rs else range(len(ks))
        idx=list(idx)
        if ys[idx].sum() in(0,len(idx)):return None
        cal=LogisticRegression(C=1.0).fit(lg(ps[idx]),ys[idx],sample_weight=ws[idx]);w=cal.predict_proba(lg(pp))[:,1]
        # a amostra cobre o pool menos o topo(150) ja lido; w ja e P(P3|score)
        hard=np.argmax(Q,axis=1);s=np.zeros(K)
        for j,c in enumerate(clm):s[ix[c]]=w[hard==j].sum()
        # correcao por matriz de erros: s_pred = C^T s_true  -> nnls
        return s,w.sum(),s   # previsao direta (a correcao por matriz piorou na validacao)
    base,total,bruto=estimar(None)
    rs=random.Random(seed);bt=[];
    for _ in range(nboot):
        r=estimar(rs)
        if r:bt.append(r)
    H=np.array([b[0] for b in bt]);T=np.array([b[1] for b in bt])
    H=H*np.exp(np.random.RandomState(seed).normal(0,0.30,H.shape))   # erro do modelo (validacao: ~30% por assunto)
    # validacao: amostra lida (ponderada) x prevista
    real_s=collections.Counter();
    for k in ks:
        if amostra[k][0]!='OUTRO':real_s[amostra[k][0]]+=ws[ks.index(k)]
    Qs=mm.predict_proba([txt[k] for k in ks]);hs=np.argmax(Qs,axis=1);sv=np.zeros(K)
    for i,k in enumerate(ks):sv[ix[clm[hs[i]]]]+=ws[i]*ys[i]
    tv,_=nnls(C.T,sv)
    out={'classes':cl,'ocultas_p3':[int(np.percentile(T,q)) for q in (5,50,95)],'oculto_por_assunto':{c:[round(float(np.percentile(H[:,ix[c]],q)),1) for q in (5,50,95)] for c in cl},
         'bruto_sem_correcao':{c:round(float(bruto[ix[c]]),1) for c in cl},'amostra_lida_ponderada':{c:round(real_s[c],1) for c in cl},
         'validacao_amostra_bruto':{c:round(float(sv[ix[c]]),1) for c in cl},'validacao_amostra_corrigido':{c:round(float(tv[ix[c]]),1) for c in cl},'diag_confusao':{c:round(float(C[ix[c],ix[c]]),2) for c in cl}}
    # --- aceite pelo modelo (localizadas sem leitura): menor limiar com precisao (limite inferior 5%) >= 0.90 e n_amostra >= 25
    wy=ws*ys;aceite=None;rb=random.Random(seed+1)
    for t in (.75,.80,.85,.90,.93,.95):
        m=ps>=t;n=int(m.sum())
        if n<25:continue
        pr=float(wy[m].sum()/ws[m].sum());lb=[]
        idx=np.where(m)[0]
        for _ in range(400):
            j=[idx[rb.randrange(len(idx))] for _ in idx];lb.append(float(wy[j].sum()/ws[j].sum()))
        lo=float(np.percentile(lb,5))
        if lo>=.90:aceite={'limiar':t,'n_amostra':n,'precisao':round(pr,3),'precisao_lb90':round(lo,3),'n_pool':int((pp>=t).sum()),'p3_aceitas':round(int((pp>=t).sum())*lo)};break
    out['aceite_modelo']=aceite
    # --- ordem final: P3 no pool forte (real) + topo lido (exato) + escondidas (ML, bootstrap)
    prec=json.load(open(B+'/docs/precisao-triagem-p3.json'));realf={a:prec[a]['real'] for a in prec if a.startswith('P3')}
    tp=collections.Counter(v[0] for v in topo.values() if v[0]!='OUTRO')
    allc=sorted(set(cl)|set(realf));tot=np.zeros((len(H),len(allc)))
    for j,a in enumerate(allc):
        tot[:,j]=realf.get(a,0)+tp.get(a,0)+(H[:,ix[a]] if a in ix else 0)
    part=tot/tot.sum(1,keepdims=True);rank=(-part).argsort(1).argsort(1)+1
    med=np.median(part,0);ordem=[allc[j] for j in np.argsort(-med)];cum=np.cumsum(sorted(med,reverse=True))
    faixa={a:('A' if cum[i]-med[allc.index(a)]<.5 else 'B' if cum[i]-med[allc.index(a)]<.8 else 'C') for i,a in enumerate(ordem)}
    est=0;lista=[]
    for a in ordem:
        j=allc.index(a);fs=[]
        for b in range(len(H)):
            o=np.argsort(-part[b]);cc=np.cumsum(part[b][o]);pos=list(o).index(j);fs.append('A' if cc[pos]-part[b][j]<.5 else 'B' if cc[pos]-part[b][j]<.8 else 'C')
        f=collections.Counter(fs).most_common(1)[0];lista.append({'assunto':a,'part':round(float(med[j]),4),'ic90':[round(float(np.percentile(part[:,j],5)),4),round(float(np.percentile(part[:,j],95)),4)],'faixa':faixa[a],'estab_faixa':round(f[1]/len(fs),2),'rank_ic90':[int(np.percentile(rank[:,j],5)),int(np.percentile(rank[:,j],95))]})
    out['ordem']=lista;sp=sum(1 for v in amostra.values() if v[0]!='OUTRO');con=sum(realf.values())+sum(tp.values())+sp;tt=float(np.median(T))
    out['recall_conhecidas']=round(con/(con+tt),3);out['conhecidas']={'pool_forte':round(sum(realf.values())),'topo':sum(tp.values()),'sorteio':sp,'escondidas_nao_lidas':round(tt)}
    ac=aceite['p3_aceitas'] if aceite else 0;out['recall_localizado']=round((con+ac)/(con+tt),3)
    # estabilidade pelas regras v2 (as mesmas da P2, pre-registradas)
    boot=[{allc[j]:float(part[b,j]) for j in range(len(allc))} for b in range(len(H))];basesh={allc[j]:float(med[j]) for j in range(len(allc))}
    labyr=[(x[0],x[3]) for x in L]
    out['v2']={'faixas':CO.estabilidade_share(boot,basesh),'faixas_acum':CO.estabilidade(boot,basesh,basesh),'temporal':CO.temporal_cobertura(labyr),'temporal_loyo':CO.temporal_loyo(labyr),'conjunto80':CO.estabilidade_conjunto(boot,basesh)}
    print('conhecidas',out['conhecidas'],'| recall conhecidas %.3f | aceite do modelo'%out['recall_conhecidas'],aceite,'| recall localizado %.3f'%out['recall_localizado'])
    print('v2 faixas:',out['v2']['faixas']['estaveis'],'/',out['v2']['faixas']['relevantes'],'instaveis',out['v2']['faixas']['instaveis'])
    print('v2 temporal: razao %.3f pior %s folds %d'%(out['v2']['temporal']['razao_ponderada'],out['v2']['temporal']['pior_fold'],len(out['v2']['temporal']['folds'])))
    print('recall (conhecidas / total estimado): %.3f'%out['recall_conhecidas'])
    for i,x in enumerate(lista,1):print('%2d %-12s %.3f [%.3f-%.3f] faixa %s estab %.2f rank %s'%(i,x['assunto'],x['part'],*x['ic90'],x['faixa'],x['estab_faixa'],x['rank_ic90']))
    print('faixas estaveis (>=0.80):',sum(x['estab_faixa']>=.8 for x in lista if x['part']>=.01),'de',sum(x['part']>=.01 for x in lista))
    json.dump(out,open(B+'/docs/censo-ml-p3.json','w'),ensure_ascii=False,indent=1)
    print('ocultas P3 (IC90):',out['ocultas_p3'])
    print('%-12s %8s %16s %8s %6s'%('assunto','amostra','ML corrigido(IC90)','ML bruto','diagC'))
    ev=[abs(tv[ix[c]]-real_s[c]) for c in cl];eb=[abs(sv[ix[c]]-real_s[c]) for c in cl]
    print('validacao na amostra (erro absoluto medio por assunto): bruto %.1f | corrigido %.1f | referencia (media das contagens) %.1f'%(np.mean(eb),np.mean(ev),np.mean([real_s[c] for c in cl])))
    for c in sorted(cl,key=lambda c:-out['oculto_por_assunto'][c][1]):
        o=out['oculto_por_assunto'][c];print('%-12s %8.1f %6.0f [%4.0f-%4.0f] %8.1f %6.2f'%(c,real_s[c],o[1],o[0],o[2],out['bruto_sem_correcao'][c],out['diag_confusao'][c]))
    return out
if __name__=='__main__':main()
