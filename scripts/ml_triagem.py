#!/usr/bin/env python3
"""ML local (zero token) para triagem de P3: detector P3-x-fora + classificador de assunto.
Uso (na raiz do projeto cgu-bd):
  python scripts/ml_triagem.py validar   # folds temporais (treina em anos < Y, testa em Y) -> docs/ml-triagem-p3.json
  python scripts/ml_triagem.py fila      # treina com tudo e ordena o pool de descartadas -> docs/ml-fila-p3.json
  python scripts/ml_triagem.py recall    # estima P3 escondidas no pool (calibra nas descartadas lidas)
  python scripts/ml_triagem.py tudo      # os tres
Aceite automatico so vale com margem >= limiar medido; tudo marcado origem='ml' e NAO entra em caderno sem auditoria."""
import json,glob,os,re,sys,collections,random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));C=B+'/concursos/cgu-affc-ti-ds/'
rd=lambda p:[json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]
yr=lambda p:int(re.search(r'(20\d{2})',p).group(1)) if re.search(r'(20\d{2})',p) else 0
SEED=7

def texto(x):return ' '.join(filter(None,[x.get('contexto'),x.get('enunciado')]))
def carregar():
    txt={}
    for f in glob.glob(B+'/extraidos/*.jsonl'):
        pid=os.path.basename(f)[:-6]
        for x in rd(f):txt[(pid,str(x.get('item')))]=texto(x)
    lab={};mp={m['id']:m for m in rd(C+'amostras/p3-verif-1-mapa.jsonl')}
    for f in glob.glob(C+'classificacoes/p3-verif-1-*.jsonl'):
        for x in rd(f):m=mp[x['id']];lab[(m['prova_id'],str(m['item']))]=x['codigo']
    T=json.load(open(B+'/tmp/p3ext/tudo.json'));nao=set()
    for m in T['M']:
        k=(m['prova_id'],str(m['item']));lab[k]=T['L'][m['id']]['codigo']
        if m['tipo']=='nao':nao.add(k)
    cl={str(x['item']):x for x in rd(C+'classificacoes/tema-p3-dados-2.jsonl')}
    for r in rd(C+'escopo/tema-p3-dados-2.jsonl'):
        c=r.get('compat');c=c if isinstance(c,dict) else {}
        if c.get('nivel')=='forte':
            e=cl[str(r['item'])]['edital'];lab[(r['prova_origem'],str(r['item_orig']))]=e.split('.')[0] if e.startswith('P3·') else 'OUTRO'
    return txt,lab,nao
def pool_descartadas(txt,lab):
    """itens extraidos, sem triagem forte, em provas que tem P3 (mesma definicao do precisao_p3.py)"""
    out=[]
    for f in glob.glob(C+'escopo/*.jsonl'):
        pid=os.path.basename(f)[:-6]
        if pid.startswith('tema-'):continue
        rows=rd(f);vistos={str(r.get('item')) for r in rows};fo=0
        for r in rows:
            c=r.get('compat');c=c if isinstance(c,dict) else {}
            if c.get('nivel')=='forte' and str(c.get('edital_prov','')).startswith('P3'):fo+=1
        if not fo:continue
        for (p,i),t in txt.items():
            if p==pid and i not in vistos:out.append((p,i))
    return out
def vet():return TfidfVectorizer(strip_accents='unicode',lowercase=True,ngram_range=(1,2),min_df=2,sublinear_tf=True,max_features=60000)
def det():return Pipeline([('v',vet()),('c',LogisticRegression(C=4,class_weight='balanced',max_iter=800))])
def cls():return Pipeline([('v',vet()),('c',LinearSVC(C=1,class_weight='balanced'))])
def dataset(txt,lab):return [(yr(k[0]),k,txt[k],y) for k,y in lab.items() if k in txt and len(txt[k])>20]

def validar(L):
    P=[x for x in L if x[3]!='OUTRO'];res=[];out=[];folds=[]
    for a in sorted({x[0] for x in L}):
        tr=[x for x in P if x[0]<a];te=[x for x in P if x[0]==a]
        if len(tr)>=120 and len(te)>=20:
            m=cls().fit([x[2] for x in tr],[x[3] for x in tr]);d=m.decision_function([x[2] for x in te]);cs=m.named_steps['c'].classes_
            ix=np.argsort(d,axis=1)[:,::-1]
            for x,r,dd in zip(te,ix,d):res.append((a,x[3]==cs[r[0]],x[3] in [cs[j] for j in r[:3]],dd[r[0]]-dd[r[1]]))
            folds.append(a)
        tr=[x for x in L if x[0]<a];te=[x for x in L if x[0]==a]
        if len(tr)>=150 and len(te)>=30:
            m=det().fit([x[2] for x in tr],[x[3]!='OUTRO' for x in tr]);p=m.predict_proba([x[2] for x in te])[:,1]
            out+=[(a,x[3]!='OUTRO',pp) for x,pp in zip(te,p)]
    r={'anos_assunto':folds,'n_assunto':len(res),'top1':float(np.mean([x[1] for x in res])),'top3':float(np.mean([x[2] for x in res])),'margem':[]}
    for lim in (0,.2,.3,.4,.5,.6,.8):
        s=[x for x in res if x[3]>=lim]
        if s:r['margem'].append({'lim':lim,'cobertura':len(s)/len(res),'precisao':float(np.mean([x[1] for x in s]))})
    y=np.array([o[1] for o in out]);s=np.array([o[2] for o in out])
    r['detector']={'n':len(out),'auc':float(roc_auc_score(y,s)),'cortes':[]}
    for lim in (.3,.4,.5,.6,.7,.8,.9):
        k=s>=lim
        if k.any():r['detector']['cortes'].append({'p':lim,'aceita':float(k.mean()),'precisao':float(y[k].mean()),'recall':float((y&k).sum()/max(1,y.sum()))})
    # limiar de auto-aceite = menor margem com precisao >= 0.92 (e ao menos 5% de cobertura)
    ok=[m for m in r['margem'] if m['precisao']>=.92 and m['cobertura']>=.05]
    r['limiar_auto_aceite_margem']=min([m['lim'] for m in ok]) if ok else None
    os.makedirs(B+'/docs',exist_ok=True);json.dump(r,open(B+'/docs/ml-triagem-p3.json','w'),ensure_ascii=False,indent=1)
    print('assunto: n=%d top1=%.2f top3=%.2f'%(r['n_assunto'],r['top1'],r['top3']))
    for m in r['margem']:print('  margem>=%.1f cobertura %.2f precisao %.2f'%(m['lim'],m['cobertura'],m['precisao']))
    print('detector: n=%d AUC=%.3f'%(r['detector']['n'],r['detector']['auc']))
    for c in r['detector']['cortes']:print('  p>=%.1f aceita %.2f precisao %.2f recall %.2f'%(c['p'],c['aceita'],c['precisao'],c['recall']))
    print('limiar auto-aceite (margem):',r['limiar_auto_aceite_margem'])
    return r

def ajustar(L,excl=()):
    ex=set(excl);D=[x for x in L if x[1] not in ex];P=[x for x in D if x[3]!='OUTRO']
    md=det().fit([x[2] for x in D],[x[3]!='OUTRO' for x in D]);mc=cls().fit([x[2] for x in P],[x[3] for x in P])
    return md,mc
def pontuar(md,mc,textos):
    p=md.predict_proba(textos)[:,1];d=mc.decision_function(textos);cs=mc.named_steps['c'].classes_;ix=np.argsort(d,axis=1)[:,::-1]
    return p,[([str(cs[j]) for j in r[:3]],float(dd[r[0]]-dd[r[1]])) for r,dd in zip(ix,d)]

def fila(L,txt,lab,nao):
    md,mc=ajustar(L,nao)  # sem as descartadas lidas, para poder calibrar nelas
    pool=[k for k in pool_descartadas(txt,lab) if k not in lab]
    p,top=pontuar(md,mc,[txt[k] for k in pool]);o=np.argsort(-p)
    rows=[{'prova_id':pool[i][0],'item':pool[i][1],'p_p3':round(float(p[i]),4),'assuntos':top[i][0],'margem':round(top[i][1],3),'trecho':txt[pool[i]][:160]} for i in o]
    json.dump({'n':len(rows),'itens':rows},open(B+'/docs/ml-fila-p3.json','w'),ensure_ascii=False)
    print('fila: %d itens do pool ordenados por P(P3); top 5:'%len(rows))
    for r in rows[:5]:print('  %.2f %s #%s %s'%(r['p_p3'],r['prova_id'],r['item'],r['assuntos'][0]))
    return pool,p
def recall(L,txt,lab,nao):
    nao=[k for k in nao if k in txt]
    md,mc=ajustar(L,nao);p110=md.predict_proba([txt[k] for k in nao])[:,1];y=np.array([lab[k]!='OUTRO' for k in nao])
    print('descartadas lidas: %d, com P3: %d (%.1f%%), AUC=%.3f'%(len(nao),y.sum(),100*y.mean(),roc_auc_score(y,p110)))
    pool=[k for k in pool_descartadas(txt,lab) if k not in lab];pp=md.predict_proba([txt[k] for k in pool])[:,1]
    # calibracao Platt (logit de p -> y) nas descartadas lidas, com bootstrap
    lg=lambda v:np.log(np.clip(v,1e-4,1-1e-4)/(1-np.clip(v,1e-4,1-1e-4))).reshape(-1,1);rng=random.Random(SEED);est=[]
    for _ in range(300):
        ix=[rng.randrange(len(nao)) for _ in nao]
        if y[ix].sum() in (0,len(ix)):continue
        c=LogisticRegression(C=1.0).fit(lg(p110[ix]),y[ix]);est.append(c.predict_proba(lg(pp))[:,1].sum())
    c=LogisticRegression(C=1.0).fit(lg(p110),y);pt=c.predict_proba(lg(pp))[:,1].sum()
    amostral=y.mean()*len(pool)
    pc=lambda a,q:float(np.percentile(a,q))
    r={'pool':len(pool),'lidas':len(nao),'p3_lidas':int(y.sum()),'estimativa_amostral':round(float(amostral)),'estimativa_modelo':round(float(pt)),'ic90_modelo':[round(pc(est,5)),round(pc(est,95))],
       'auc_lidas':float(roc_auc_score(y,p110)),'aviso':'so 110 lidas e ~16 positivos: tratar como ordem de grandeza; nao substitui leitura'}
    json.dump(r,open(B+'/docs/ml-recall-p3.json','w'),ensure_ascii=False,indent=1)
    print('P3 escondidas no pool de %d: amostral %d | modelo calibrado %d (IC90 %d-%d)'%(len(pool),r['estimativa_amostral'],r['estimativa_modelo'],*r['ic90_modelo']))
    return r

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'tudo'
    txt,lab,nao=carregar();L=dataset(txt,lab)
    print('rotulados com texto:',len(L),'| P3:',sum(x[3]!='OUTRO' for x in L),'| classes:',len({x[3] for x in L if x[3]!='OUTRO'}))
    if cmd in('validar','tudo'):validar(L)
    if cmd in('fila','tudo'):fila(L,txt,lab,nao)
    if cmd in('recall','tudo'):recall(L,txt,lab,nao)
