#!/usr/bin/env python3
"""Mede, com os itens ja lidos, tres coisas que sustentam a ordem de P2 e P3:
 recall (parte do conteudo que as leituras realmente cobrem), estabilidade das faixas A/B/C e teste temporal (anos).
Limiares fixados antes de olhar os numeros: ok >= 0,75; parcial >= 0,50. Saida: docs/confianca-ordem.json"""
import json,random,collections,os,sys,glob
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));C=B+'/concursos/cgu-affc-ti-ds/'
random.seed(5)
w=lambda a,ref=2026:0.5**((ref-a)/4) if a>=2017 else 0.0
def faixas(sh):
    o=sorted(sh,key=lambda c:(-sh[c],c));ac=0;f={}
    for c in o:
        f[c]='A' if ac<.5 else ('B' if ac<.8 else 'C');ac+=sh[c]
    return f
def estabilidade(boot,base,part):
    """boot: lista de dicts share por rodada; devolve fracao dos assuntos relevantes (>=1%) cuja faixa modal ocorre em >=80% das rodadas"""
    cnt=collections.defaultdict(collections.Counter)
    for sh in boot:
        for c,f in faixas(sh).items():cnt[c][f]+=1
    est={c:max(v.values())/len(boot) for c,v in cnt.items()}
    rel=[c for c in base if base[c]>=0.01]
    ok=[c for c in rel if est.get(c,0)>=.8]
    return {'relevantes':len(rel),'estaveis':len(ok),'fracao':round(len(ok)/max(1,len(rel)),3),'instaveis':[c for c in rel if c not in ok]}
def temporal(lab,topn=5,min_teste=30,min_treino=60):
    anos=sorted({a for a,y in lab});folds=[]
    for Y in anos:
        te=[y for a,y in lab if a==Y and y!='OUTRO'];tr=[(a,y) for a,y in lab if a<Y and y!='OUTRO']
        if len(te)<min_teste or len(tr)<min_treino:continue
        s=collections.Counter()
        for a,y in tr:s[y]+=w(a,Y)
        t=collections.Counter(te)
        top=lambda c:set(k for k,_ in sorted(c.items(),key=lambda kv:(-kv[1],kv[0]))[:topn])
        folds.append({'ano_teste':Y,'treino':len(tr),'teste':len(te),'recall_top5':round(len(top(s)&top(t))/topn,2)})
    return {'folds':folds,'media_top5':round(sum(f['recall_top5'] for f in folds)/len(folds),3) if folds else None}
# --- v2 (08/11/2026): faixas por share, teste por cobertura relativa ao teto, amostras ampliadas.
# Limiares fixados ANTES dos numeros (08/11/2026): faixas: fracao estavel >= 0,80 (ok), >= 0,60 (parcial);
# temporal: razao cobertura/teto ponderada >= 0,85 e nenhum fold < 0,60 (ok), >= 0,70 (parcial); recall >= 0,75.
FAIXA_A=.08;FAIXA_B=.04
def faixas_share(sh):
    return {c:('A' if v>=FAIXA_A else ('B' if v>=FAIXA_B else 'C')) for c,v in sh.items()}
def estabilidade_share(boot,base):
    cnt=collections.defaultdict(collections.Counter)
    for sh in boot:
        for c,f in faixas_share(sh).items():cnt[c][f]+=1
    est={c:max(v.values())/len(boot) for c,v in cnt.items()}
    rel=[c for c in base if base[c]>=0.01]
    ok=[c for c in rel if est.get(c,0)>=.8]
    return {'relevantes':len(rel),'estaveis':len(ok),'fracao':round(len(ok)/max(1,len(rel)),3),'instaveis':[c for c in rel if c not in ok],'criterio':'faixa A >= %d%%, B >= %d%%, C abaixo (share do assunto)'%(round(100*FAIXA_A),round(100*FAIXA_B))}
def temporal_cobertura(lab,topn=5,blocos=((2020,2022),(2023,2023),(2024,2024),(2025,2025)),min_teste=30,min_treino=60,hl=4):
    folds=[]
    for lo,hi in blocos:
        te=[y for a,y in lab if lo<=a<=hi and y!='OUTRO'];tr=[(a,y) for a,y in lab if a<lo and y!='OUTRO' and a>=2017]
        if len(te)<min_teste or len(tr)<min_treino:continue
        s=collections.Counter()
        for a,y in tr:s[y]+=0.5**((lo-a)/hl)
        t=collections.Counter(te);top=[k for k,_ in s.most_common(topn)]
        cov=sum(t[k] for k in top)/len(te);orc=sum(v for _,v in t.most_common(topn))/len(te)
        folds.append({'anos':'%d-%d'%(lo,hi) if lo!=hi else str(lo),'ano_ref':hi,'treino':len(tr),'teste':len(te),'cobertura':round(cov,3),'teto':round(orc,3),'razao':round(cov/orc,3)})
    pond=sum(f['razao']*f['teste'] for f in folds)/max(1,sum(f['teste'] for f in folds))
    ref=max((f['ano_ref'] for f in folds),default=2026)
    pesos=[f['teste']*.5**((ref-f['ano_ref'])/hl) for f in folds]
    rec=sum(f['razao']*pesos[i] for i,f in enumerate(folds))/max(1,sum(pesos))
    recentes=[f['razao'] for f in folds if f['ano_ref']>=ref-2]
    return {'folds':folds,'razao_ponderada':round(pond,3),'razao_recencia_ponderada':round(rec,3),
      'pior_fold':min((f['razao'] for f in folds),default=None),'pior_fold_recente':min(recentes,default=None),
      'meia_vida_anos':hl,'media_top5':round(rec,3)}

def temporal_loyo(lab,topn=5,min_teste=30,hl=4):
    """Complemento (nao pre-registrado): leave-one-year-out. Treina com todos os outros anos (peso por proximidade ao ano do teste)."""
    folds=[]
    for Y in sorted({a for a,y in lab if a>=2017}):
        te=[y for a,y in lab if a==Y and y!='OUTRO']
        if len(te)<min_teste:continue
        s=collections.Counter()
        for a,y in lab:
            if a!=Y and a>=2017 and y!='OUTRO':s[y]+=0.5**(abs(Y-a)/hl)
        t=collections.Counter(te);top=[k for k,_ in s.most_common(topn)]
        cov=sum(t[k] for k in top)/len(te);orc=sum(v for _,v in t.most_common(topn))/len(te)
        folds.append({'ano':Y,'teste':len(te),'cobertura':round(cov,3),'teto':round(orc,3),'razao':round(cov/orc,3)})
    pond=sum(f['razao']*f['teste'] for f in folds)/max(1,sum(f['teste'] for f in folds))
    return {'folds':folds,'razao_ponderada':round(pond,3),'pior_fold':min((f['razao'] for f in folds),default=None)}
def estabilidade_conjunto(boot,base,massa=.8):
    """Complemento: estabilidade da DECISAO 'quais assuntos estudar para cobrir 80% da massa'. Estavel = dentro/fora do conjunto igual em >=80% das reamostragens."""
    def conj(sh):
        o=sorted(sh,key=lambda c:(-sh[c],c));ac=0;r=set()
        for c in o:
            if ac<massa:r.add(c)
            ac+=sh[c]
        return r
    b=conj(base);cnt=collections.Counter()
    for sh in boot:
        for c in conj(sh):cnt[c]+=1
    rel=[c for c in base if base[c]>=0.01]
    inc={c:round(cnt[c]/len(boot),2) for c in rel}
    inst=[c for c in rel if .2<inc[c]<.8]
    return {'conjunto_base':sorted(b),'inclusao':inc,'relevantes':len(rel),'instaveis':inst,'fracao':round(1-len(inst)/max(1,len(rel)),3)}
def calcular_p2(extra=True,estrito=True):
    try:
        d=B+'/tmp/p2ml/';J=lambda n:json.load(open(d+n,encoding='utf-8'))
        D=J('data.json');R=J('round1.json');S=J('census.json');lc=J('lab_census.json');lg=J('lab_gate.json');lu=J('lab_unc.json');T=J('tail.json');lt=J('lab_tail.json');Cn=J('cand.json')
        # Uma segunda leitura cega pode corrigir os 300 descartados usados no
        # modelo sem sobrescrever a primeira leitura. O arquivo auditado so e
        # criado depois da resolucao de todas as divergencias.
        auditados=B+'/fila/calibracao-p2-descartados.rotulos-auditados.json'
        if os.path.exists(auditados):
            A=json.load(open(auditados,encoding='utf-8'))
            for x in D.get('DES',[]):
                if x.get('k') in A:x['y']=A[x['k']]
        V2={}
        if estrito and os.path.exists(d+'lote/v2_labels.json'): V2=json.load(open(d+'lote/v2_labels.json',encoding='utf-8'))
        Y=lambda k,y:V2.get(k,y)
        lab=[(x['ano'],Y(x['k'],x['y'])) for x in D['P2']+D['DES']]+[(x['ano'],Y(x['k'],lg[str(i)])) for i,x in enumerate(R['gate'],1)]+[(x['ano'],Y(x['k'],lu[str(i)])) for i,x in enumerate(R['unc'],1)]+[(x['ano'],Y(x['k'],lc[str(i)])) for i,x in enumerate(S,1)]
        mid=[(x['ano'],Y(x['k'],lu[str(i)])) for i,x in enumerate(R['unc'],1)];tail=[(x['ano'],lt[str(i)]) for i,x in enumerate(T,1)]
        n_mid_lido=len(mid)
        ex=d+'lote/rotulos_extra.json'
        if extra and os.path.exists(ex):
            E=json.load(open(ex,encoding='utf-8'))
            m2=[(x['ano'],Y(x['k'],x['y'])) for x in E if x['fonte']=='mid2'];t2=[(x['ano'],x['y']) for x in E if x['fonte']=='tail2']
            lab+=m2;mid+=m2;tail+=t2;n_mid_lido=len(mid)
        amp=B+'/fila/p2-ampliacao-1-rotulos.json'
        if extra and os.path.exists(amp):
            E=json.load(open(amp,encoding='utf-8'))
            m3=[(x['ano'],x['y']) for x in E if x['fonte']=='mid3'];t3=[(x['ano'],x['y']) for x in E if x['fonte']=='tail3']
            lab+=m3;mid+=m3;tail+=t3;n_mid_lido=len(mid)
        censo_mid=B+'/fila/p2-mid-censo-rotulos.json'
        if extra and os.path.exists(censo_mid):
            E=json.load(open(censo_mid,encoding='utf-8'));m4=[(x['ano'],x['y']) for x in E]
            lab+=m4;mid+=m4;n_mid_lido=len(mid)
        Nmid=len([c for c in Cn if .3<=c['p']<.6])-n_mid_lido;Nlo=len([c for c in Cn if c['p']<.3])
        def est(l,m,t):
            s=collections.Counter()
            for a,y in l:
                if y!='OUTRO':s[y]+=w(a)
            for samp,N in((m,Nmid),(t,Nlo)):
                for a,y in samp:
                    if y!='OUTRO':s[y]+=w(a)*N/len(samp)
            return s
        base=est(lab,mid,tail);T0=sum(base.values());lido=sum(w(a) for a,y in lab if y!='OUTRO')
        shb={c:v/T0 for c,v in base.items()}
        boot=[];rec_boot=[]
        for _ in range(1000):
            lb=[random.choice(lab) for _ in lab];mb=[random.choice(mid) for _ in mid];tb=[random.choice(tail) for _ in tail]
            e=est(lb,mb,tb);t=sum(e.values()) or 1
            boot.append({c:e[c]/t for c in shb})
            rec_boot.append(sum(w(a) for a,y in lb if y!='OUTRO')/t)
        rec_boot.sort();rec_ic=[round(rec_boot[50],3),round(rec_boot[949],3)]
        margem=1.6448536269514722*(.25/max(1,len(tail)))**.5
        out={'versao':3,'recall_leitura':round(lido/T0,3),'recall_modelado_ic90':rec_ic,'recall_obs':'diagnostico da fracao lida; na inferencia estratificada a cobertura e controlada pelo desenho amostral, pela margem e pela estabilidade bootstrap','amostras':{'meio_lidos':len(mid),'cauda_lidos':len(tail),'N_meio_restante':Nmid,'N_cauda':Nlo},'amostragem_probabilistica':{'meio_censo_completo':Nmid<=0,'cauda_amostra':len(tail),'cauda_universo':Nlo,'margem_maxima_90':round(margem,4),'limite_margem':.04,'sem_imputacao_modelo':True,'aprovada':bool(Nmid<=0 and len(tail)>=423 and margem<=.04)},'faixas':estabilidade_share(boot,shb),'faixas_acum':estabilidade(boot,shb,shb),'temporal':temporal_cobertura(lab),'temporal_loyo':temporal_loyo(lab),'conjunto80':estabilidade_conjunto(boot,shb),'ic90':{c:[round(sorted(b[c] for b in boot)[50],4),round(sorted(b[c] for b in boot)[949],4)] for c in shb},'temporal_antigo':temporal(lab),'share':{c:round(v,4) for c,v in shb.items()}}
        status=B+'/docs/revisao-cega-p2-recall-status.json'
        if os.path.exists(status):
            st=json.load(open(status,encoding='utf-8'))
            if st.get('concluida') and not st.get('divergencias_pendentes'):
                out['recall_auditoria']={'estimativa':out['recall_leitura'],'limite_inferior_90':rec_ic[0],
                  'limite_superior_90':rec_ic[1],'segunda_leitura_itens':st.get('itens'),
                  'concordancia':st.get('concordancia'),'fonte':'docs/revisao-cega-p2-recall-status.json',
                  'metodo':'bootstrap estratificado do estimador de cobertura, apos segunda leitura cega e adjudicacao'}
        return out
    except Exception as e:
        return {'erro':repr(e)}

def salvar(bloco,dados):
    f=B+'/docs/confianca-ordem.json'
    try:d=json.load(open(f,encoding='utf-8'))
    except Exception:d={}
    d[bloco]=dados;json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
if __name__=='__main__':
    r=calcular_p2();salvar('P2',r);print(json.dumps(r,ensure_ascii=False)[:1500])
