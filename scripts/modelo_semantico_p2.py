#!/usr/bin/env python3
"""Treina e audita um classificador semantico local para a cauda de P2.

As duas amostras de teste (300 descartados auditados e 150 itens tail3) nunca
entram no treino nem na escolha do limiar. Previsoes so sao gravadas se recall
binario e acuracia top-3 de assunto passarem pelos limites predefinidos.
"""
import argparse,json,math,re
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold,cross_val_predict

BASE=Path(__file__).resolve().parent.parent;D=BASE/'tmp'/'p2ml'
def load(p,default=None):
    try:return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:return default
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def parent(y):
    m=re.match(r'(P2·\w+)\s+(\d+)',str(y or ''));return m.group(1)+' '+m.group(2) if m else str(y or 'OUTRO')
def wilson(k,n,z=1.6448536269514722):
    if not n:return [0,1]
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,c-h),min(1,c+h)]

def dataset():
    data=load(D/'data.json',{});R=load(D/'round1.json',{});S=load(D/'census.json',[]);T=load(D/'tail.json',[])
    lg=load(D/'lab_gate.json',{});lu=load(D/'lab_unc.json',{});lc=load(D/'lab_census.json',{});lt=load(D/'lab_tail.json',{})
    v2=load(D/'lote'/'v2_labels.json',{}) or {};text={}
    for x in data.get('P2',[])+data.get('DES',[])+R.get('gate',[])+R.get('unc',[])+S+T:text[x['k']]=x.get('t','')
    for x in load(D/'cand.json',[]) or []:text.setdefault(x['k'],x.get('t',''))
    lab={}
    for x in data.get('P2',[]):lab[x['k']]=parent(v2.get(x['k'],x['y']))
    for nome,rows,rot in (('gate',R.get('gate',[]),lg),('unc',R.get('unc',[]),lu)):
        for i,x in enumerate(rows,1):lab[x['k']]=parent(v2.get(x['k'],rot[str(i)]))
    for i,x in enumerate(S,1):lab[x['k']]=parent(v2.get(x['k'],lc[str(i)]))
    for i,x in enumerate(T,1):lab[x['k']]=parent(lt[str(i)])
    for x in load(D/'lote'/'rotulos_extra.json',[]) or []:lab[x['k']]=parent(v2.get(x['k'],x['y']))
    amp=load(BASE/'fila'/'p2-ampliacao-1-rotulos.json',[]) or []
    for x in amp:
        if x['fonte']=='mid3':lab[x['k']]=parent(x['y'])
    for x in load(BASE/'fila'/'p2-mid-censo-rotulos.json',[]) or []:lab[x['k']]=parent(x['y'])
    hold_a={x['k']:parent((load(BASE/'fila'/'calibracao-p2-descartados.rotulos-auditados.json',{}) or {}).get(x['k'])) for x in data.get('DES',[])}
    hold_b={x['k']:parent(x['y']) for x in amp if x['fonte']=='tail3'}
    lab={k:v for k,v in lab.items() if k in text and text[k] and k not in hold_a and k not in hold_b}
    return text,lab,hold_a,hold_b

def features():
    return FeatureUnion([
      ('w',TfidfVectorizer(ngram_range=(1,2),min_df=2,max_df=.995,sublinear_tf=True,max_features=90000,strip_accents='unicode')),
      ('c',TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),min_df=3,sublinear_tf=True,max_features=90000))])

def bin_metrics(model,X,y,threshold):
    s=model.decision_function(X);pred=s>=threshold;truth=np.array(y)=='P2';tp=int(np.sum(pred&truth));fn=int(np.sum(~pred&truth));fp=int(np.sum(pred&~truth))
    rec=tp/max(1,tp+fn);prec=tp/max(1,tp+fp)
    return {'n':len(y),'positivos':int(np.sum(truth)),'aceitos':int(np.sum(pred)),'tp':tp,'fn':fn,'fp':fp,
      'recall':rec,'recall_ic90':wilson(tp,tp+fn),'precisao':prec}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('acao',choices=('avaliar','predizer'));a=ap.parse_args()
    text,lab,h1,h2=dataset();keys=list(lab);docs=[text[k] for k in keys];yb=np.array(['P2' if lab[k]!='OUTRO' else 'OUTRO' for k in keys])
    vec=features();X=vec.fit_transform(docs);cv=StratifiedKFold(5,shuffle=True,random_state=20261110)
    base=LinearSVC(class_weight='balanced',C=.7);oof=cross_val_predict(base,X,yb,cv=cv,method='decision_function')
    truth=yb=='P2';candidatos=sorted(set(float(x) for x in np.quantile(oof,np.linspace(0,.8,161))))
    valid=[]
    for th in candidatos:
        pred=oof>=th;tp=int(np.sum(pred&truth));lo=wilson(tp,int(np.sum(truth)))[0]
        if lo>=.90:valid.append((th,int(np.sum(pred))))
    threshold=max(valid,key=lambda z:z[0])[0] if valid else float(np.min(oof)-1e-6)
    base.fit(X,yb)
    out={'treino':{'n':len(keys),'positivos':int(np.sum(truth)),'limiar_predefinido_por_oof':threshold,
      'oof':bin_metrics(type('M',(),{'decision_function':lambda self,x:oof})(),X,yb,threshold)},'holdouts':{}}
    for nome,H in (('descartados_auditados',h1),('tail3',h2)):
        kk=[k for k in H if k in text and text[k]];XX=vec.transform([text[k] for k in kk]);yy=['P2' if H[k]!='OUTRO' else 'OUTRO' for k in kk]
        out['holdouts'][nome]=bin_metrics(base,XX,yy,threshold)
    pos=[k for k in keys if lab[k]!='OUTRO'];ym=np.array([lab[k] for k in pos]);multi=LinearSVC(class_weight='balanced',C=.5);multi.fit(vec.transform([text[k] for k in pos]),ym)
    for nome,H in (('descartados_auditados',h1),('tail3',h2)):
        kk=[k for k in H if H[k]!='OUTRO' and k in text and text[k]]
        if not kk:continue
        sc=multi.decision_function(vec.transform([text[k] for k in kk]));classes=multi.classes_;top=np.argsort(sc,axis=1)[:,-3:]
        real=np.array([H[k] for k in kk]);p1=classes[top[:,-1]];ok3=np.array([real[i] in classes[top[i]] for i in range(len(real))])
        out['holdouts'][nome]['assunto_top1']=float(np.mean(p1==real));out['holdouts'][nome]['assunto_top3']=float(np.mean(ok3));out['holdouts'][nome]['assunto_top3_ic90']=wilson(int(np.sum(ok3)),len(ok3))
    out['gates']={'recall_binario_holdouts':all(x['recall_ic90'][0]>=.75 for x in out['holdouts'].values()),
      'assunto_top3_holdouts':all(x.get('assunto_top3_ic90',[0])[0]>=.70 for x in out['holdouts'].values())}
    out['aprovado']=all(out['gates'].values());dump(BASE/'docs'/'modelo-semantico-p2.json',out)
    if a.acao=='predizer' and out['aprovado']:
        usados=set(lab)|set(h1)|set(h2);cand=[x for x in load(D/'cand.json',[]) if x['k'] not in usados]
        XX=vec.transform([x['t'] for x in cand]);accept=base.decision_function(XX)>=threshold;pm=multi.predict(XX)
        pred=[{'k':x['k'],'ano':x['ano'],'y':parent(pm[i]) if accept[i] else 'OUTRO','revisao':'modelo_semantico_auditado'} for i,x in enumerate(cand)]
        dump(BASE/'fila'/'p2-cauda-modelo-auditado.json',pred);out['previsoes_gravadas']=len(pred)
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
