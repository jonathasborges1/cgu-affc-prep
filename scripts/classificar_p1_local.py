#!/usr/bin/env python3
"""Classifica P1 localmente com Naive Bayes e rejeicao por baixa confianca.

Treina nos 650 rotulos cegos, valida por ano e so aceita automaticamente o
subconjunto cujo limiar atingiu a precisao minima. Todo o resto vai para revisao.
"""
import collections, glob, json, math, random, re, unicodedata
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent; C=BASE/'concursos'/'cgu-affc-ti-ds'
def lerj(p):
    try:return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
    except Exception:return []
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',str(s or '').lower()) if unicodedata.category(c)!='Mn')
def tokens(s):
    w=[x for x in re.findall(r'[a-z]{3,}',norm(s)) if x not in {'para','como','uma','que','dos','das','com','por','ser','sao','seja','sobre','entre','mais','deve','podem','item'}]
    return w+['%s_%s'%(a,b) for a,b in zip(w,w[1:])]
def ano(pid):
    m=re.search(r'(20\d{2})',pid or '');return int(m.group(1)) if m else 0
def chave(pid,item):return str(pid)+'#'+str(item)

class NB:
    def fit(self,L):
        self.cls=collections.Counter();self.cnt=collections.defaultdict(collections.Counter);self.tot=collections.Counter();self.vocab=set()
        for text,y in L:
            self.cls[y]+=1
            for t in tokens(text):self.cnt[y][t]+=1;self.tot[y]+=1;self.vocab.add(t)
        return self
    def scores(self,text):
        ts=collections.Counter(tokens(text));N=sum(self.cls.values());V=max(1,len(self.vocab));out={}
        for y,n in self.cls.items():
            z=math.log((n+1)/(N+len(self.cls)))
            den=self.tot[y]+V
            for t,k in ts.items():z+=k*math.log((self.cnt[y][t]+1)/den)
            out[y]=z
        return out
    def pred(self,text):
        s=self.scores(text);o=sorted(s,key=s.get,reverse=True);m=s[o[0]]-s[o[1]] if len(o)>1 else 99
        return o[0],m,o[:3]

def indice_textos():
    idx={};todos=[]
    for f in sorted((BASE/'extraidos').glob('*.jsonl')):
        pid=f.stem
        for x in lerj(f):
            k=chave(pid,x.get('item'));text=' '.join(filter(None,[x.get('contexto'),x.get('enunciado')]))
            r=dict(x,prova_id=pid,chave=k,texto_modelo=text);idx[k]=r;todos.append(r)
    return idx,todos
def rotulos(idx):
    mapa={x['id']:x for x in lerj(C/'amostras'/'p1-verif-1-mapa.jsonl')};lab={}
    for f in sorted((C/'classificacoes').glob('p1-verif-1-*.jsonl')):
        for x in lerj(f):lab[x['id']]=x
    out=[]
    for iid,m in mapa.items():
        x=lab.get(iid);it=idx.get(chave(m['prova_id'],m['item']))
        if x and it:out.append({'id':iid,'pid':m['prova_id'],'ano':ano(m['prova_id']),'text':it['texto_modelo'],'y':x['codigo'],'triagem':m['triagem']})
    # Amostra de descartados, rotulada sem consultar a previsao.
    sup=json.loads((BASE/'docs'/'rotulos-p1-descartados.json').read_text(encoding='utf-8'))['rotulos']
    for x in lerj(BASE/'fila'/'calibracao-p1-complemento.jsonl'):
        out.append({'id':x['id'],'pid':x['prova_id'],'ano':ano(x['prova_id']),'text':x['enunciado'],'y':sup[x['id']],'triagem':'NAO_RECUPERADO'})
    return out
def cv(L):
    pred=[]
    for a in sorted({x['ano'] for x in L if x['ano']}):
        tr=[x for x in L if x['ano'] and x['ano']<a];te=[x for x in L if x['ano']==a]
        if len(tr)<100 or len(te)<15:continue
        m=NB().fit([(x['text'],x['y']) for x in tr])
        for x in te:
            y,margin,top=m.pred(x['text']);pred.append({'ano':a,'real':x['y'],'pred':y,'margin':margin,'top3':top,'triagem':x['triagem']})
    curvas=[]
    for lim in [0,1,2,3,4,5,6,8,10,12,15,20]:
        A=[x for x in pred if x['margin']>=lim and x['pred']==x['triagem']];ok=sum(x['real']==x['pred'] for x in A)
        curvas.append({'limiar':lim,'aceitos':len(A),'cobertura':len(A)/max(1,len(pred)),'precisao':ok/max(1,len(A)),
                       'top3':sum(x['real'] in x['top3'] for x in A)/max(1,len(A))})
    eleg=[x for x in curvas if x['aceitos']>=30 and x['precisao']>=.85]
    escolhido=min(eleg,key=lambda x:x['limiar']) if eleg else None
    return pred,curvas,escolhido
def main():
    idx,todos=indice_textos();L=rotulos(idx);pred,curvas,esc=cv(L);modelo=NB().fit([(x['text'],x['y']) for x in L])
    triagem={}
    for f in sorted((C/'escopo').glob('*.jsonl')):
        if f.name.startswith('tema-'):continue
        for z in lerj(f):
            c=z.get('compat') or {}; cod=c.get('edital_prov') or ''
            if c.get('nivel')=='forte' and cod.startswith('P1·'):
                m=re.match(r'(P1·\w+ \d+)',cod)
                if m:triagem[chave(z.get('prova_id') or f.stem,z.get('item'))]=m.group(1)
    vistos=set();auto=[];rev=[]
    for x in todos:
        nk=re.sub(r'\W','',norm(x['enunciado']))
        if not nk or nk in vistos:continue
        vistos.add(nk);y,margin,top=modelo.pred(x['texto_modelo'])
        tr=triagem.get(x['chave'],'NAO_RECUPERADO');aceita=bool(esc and margin>=esc['limiar'] and y==tr)
        r={'prova_id':x['prova_id'],'item':x.get('item'),'ano':ano(x['prova_id']),'codigo':y,'codigo_triagem':tr,'margem':round(margin,3),'top3':top,
           'enunciado':x.get('enunciado'),'gabarito':x.get('gabarito'),'auto':aceita,'modelo':'p1-nb-lexico-v2'}
        (auto if r['auto'] else rev).append(r)
    # OUTRO de alta confianca nao precisa entrar no banco de P1, mas fica no resultado auditavel.
    auto.sort(key=lambda x:(x['codigo']=='OUTRO',-x['margem']));rev.sort(key=lambda x:-x['margem'])
    outdir=C/'classificacoes-auto';outdir.mkdir(exist_ok=True)
    (outdir/'p1.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in auto),encoding='utf-8')
    (BASE/'fila'/'revisao-p1.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rev),encoding='utf-8')
    rel=[x for x in auto if x['codigo']!='OUTRO'];cnt=collections.Counter(x['codigo'] for x in rel)
    resumo={'modelo':'p1-nb-lexico-v2','rotulos':len(L),'itens_unicos':len(vistos),'validacao_temporal':{'n':len(pred),'curvas':curvas,'escolhido':esc},
            'auto_total':len(auto),'auto_p1':len(rel),'auto_outro':len(auto)-len(rel),'revisao':len(rev),'por_topico':dict(cnt),
            'regra':'auto somente se margem >= limiar escolhido em holdout temporal'}
    (BASE/'docs'/'classificador-p1.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(resumo,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
