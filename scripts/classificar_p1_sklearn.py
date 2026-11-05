#!/usr/bin/env python3
"""Classificador discriminativo de P1 com validacao temporal e rejeicao."""
import collections,json,re,sys
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
BASE=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(BASE/'scripts'))
import classificar_p1_local as D

def modelo():
    return Pipeline([('tfidf',TfidfVectorizer(strip_accents='unicode',lowercase=True,ngram_range=(1,2),min_df=2,max_features=60000,sublinear_tf=True)),
                     ('clf',LinearSVC(C=.8,class_weight='balanced'))])
def pred(m,textos):
    dec=m.decision_function(textos);classes=m.named_steps['clf'].classes_
    if dec.ndim==1:dec=np.column_stack([-dec,dec])
    ix=np.argsort(dec,axis=1)[:,::-1];ys=classes[ix[:,0]];marg=dec[np.arange(len(ix)),ix[:,0]]-dec[np.arange(len(ix)),ix[:,1]]
    top=[[str(classes[j]) for j in row[:3]] for row in ix]
    return ys,marg,top
def validar(L):
    out=[]
    for a in sorted({x['ano'] for x in L if x['ano']}):
        tr=[x for x in L if x['ano'] and x['ano']<a];te=[x for x in L if x['ano']==a]
        if len(tr)<100 or len(te)<15:continue
        m=modelo().fit([x['text'] for x in tr],[x['y'] for x in tr]);ys,ms,tops=pred(m,[x['text'] for x in te])
        out += [{'ano':a,'real':x['y'],'pred':str(y),'margin':float(mg),'top3':tp,'triagem':x['triagem']} for x,y,mg,tp in zip(te,ys,ms,tops)]
    curvas=[]
    for lim in [0,.05,.1,.15,.2,.25,.3,.4,.5,.6,.8,1.0,1.25,1.5]:
        A=[x for x in out if x['margin']>=lim and x['pred']==x['triagem']];n=len(A);ok=sum(x['real']==x['pred'] for x in A)
        curvas.append({'limiar':lim,'aceitos':n,'cobertura':n/max(1,len(out)),'precisao':ok/max(1,n),'top3':sum(x['real'] in x['top3'] for x in A)/max(1,n)})
    eleg=[x for x in curvas if x['aceitos']>=30 and x['precisao']>=.85]
    return out,curvas,(min(eleg,key=lambda x:x['limiar']) if eleg else None)
def validar_binario(L):
    out=[]
    for a in sorted({x['ano'] for x in L if x['ano']}):
        tr=[x for x in L if x['ano'] and x['ano']<a];te=[x for x in L if x['ano']==a]
        if len(tr)<100 or len(te)<15:continue
        m=modelo().fit([x['text'] for x in tr],['OUTRO' if x['y']=='OUTRO' else 'P1' for x in tr])
        dec=m.decision_function([x['text'] for x in te]);classes=list(m.named_steps['clf'].classes_);sgn=1 if classes[1]=='P1' else -1
        out += [{'real':x['y']!='OUTRO','score':float(z)*sgn} for x,z in zip(te,dec)]
    curvas=[]
    for lim in [0,.1,.2,.3,.4,.5,.6,.8,1,1.25,1.5,2]:
        A=[x for x in out if x['score']>=lim];n=len(A);ok=sum(x['real'] for x in A)
        curvas.append({'limiar':lim,'aceitos':n,'precisao':ok/max(1,n),'cobertura_positivos':ok/max(1,sum(x['real'] for x in out))})
    eleg=[x for x in curvas if x['aceitos']>=30 and x['precisao']>=.9]
    candidatos=[x for x in curvas if x['aceitos']>=30 and x['precisao']>=.85]
    return curvas,(min(eleg,key=lambda x:x['limiar']) if eleg else None),(min(candidatos,key=lambda x:x['limiar']) if candidatos else None)
def main():
    idx,todos=D.indice_textos();L=D.rotulos(idx);cv,curvas,esc=validar(L);curvas_bin,esc_bin,cand_bin=validar_binario(L)
    triagem={}
    for f in sorted((D.C/'escopo').glob('*.jsonl')):
        if f.name.startswith('tema-'):continue
        for z in D.lerj(f):
            c=z.get('compat') or {};cod=c.get('edital_prov') or '';mt=re.match(r'(P1·\w+ \d+)',cod)
            if c.get('nivel')=='forte' and mt:triagem[D.chave(z.get('prova_id') or f.stem,z.get('item'))]=mt.group(1)
    m=modelo().fit([x['text'] for x in L],[x['y'] for x in L]);ys,ms,tops=pred(m,[x['texto_modelo'] for x in todos])
    mb=modelo().fit([x['text'] for x in L],['OUTRO' if x['y']=='OUTRO' else 'P1' for x in L]);db=mb.decision_function([x['texto_modelo'] for x in todos]);cb=list(mb.named_steps['clf'].classes_);db=db*(1 if cb[1]=='P1' else -1)
    vistos=set();auto=[];rev=[]
    provaveis=[]
    for x,y,mg,tp,bs in zip(todos,ys,ms,tops,db):
        nk=re.sub(r'\W','',D.norm(x.get('enunciado')))
        if not nk or nk in vistos:continue
        vistos.add(nk);tr=triagem.get(x['chave'],'NAO_RECUPERADO');aceita=bool(esc and mg>=esc['limiar'] and str(y)==tr)
        r={'prova_id':x['prova_id'],'item':x.get('item'),'ano':D.ano(x['prova_id']),'codigo':str(y),'codigo_triagem':tr,'margem':round(float(mg),4),'top3':tp,
           'score_p1':round(float(bs),4),'enunciado':x.get('enunciado'),'gabarito':x.get('gabarito'),'auto':aceita,'modelo':'p1-tfidf-svm-v1'}
        (auto if aceita else rev).append(r)
        if tr=='NAO_RECUPERADO' and cand_bin and bs>=cand_bin['limiar']:provaveis.append(dict(r,candidato_apenas=True))
    auto.sort(key=lambda x:(x['codigo']=='OUTRO',-x['margem']));rev.sort(key=lambda x:-x['margem'])
    outdir=D.C/'classificacoes-auto';outdir.mkdir(exist_ok=True)
    (outdir/'p1.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in auto),encoding='utf-8')
    (BASE/'fila'/'revisao-p1.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rev),encoding='utf-8')
    provaveis.sort(key=lambda x:-x['score_p1']);(BASE/'fila'/'revisao-p1-provaveis.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in provaveis),encoding='utf-8')
    rel=[x for x in auto if x['codigo']!='OUTRO'];res={'modelo':'p1-tfidf-svm-v1','rotulos':len(L),'itens_unicos':len(vistos),'validacao_temporal':{'n':len(cv),'curvas':curvas,'escolhido':esc},
      'detector_p1':{'curvas':curvas_bin,'auto_escolhido':esc_bin,'candidato_revisao':cand_bin,'descartados_provaveis_p1':len(provaveis)},
      'auto_total':len(auto),'auto_p1':len(rel),'auto_outro':len(auto)-len(rel),'revisao':len(rev),'por_topico':dict(collections.Counter(x['codigo'] for x in rel)),
      'gate':'precisao >= 85%, >=30 aceitos no holdout e concordancia SVM+triagem'}
    (BASE/'docs'/'classificador-p1.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(res,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
