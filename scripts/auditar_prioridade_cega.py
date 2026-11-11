#!/usr/bin/env python3
"""Avalia auditorias cegas estratificadas já rotuladas para P2/P3.

Calcula precisão/recall do filtro de compatibilidade nos tercis de score,
intervalos bootstrap por item e um resumo reproduzível por bloco. Não altera
rótulos nem o banco de questões.
"""
import json, random, re
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
def readj(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def readl(p): return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def parent(c):
    if not c: return None
    m=re.match(r'^(P[23]·[^ ]+ \d+)',str(c))
    return m.group(1) if m else None
def percentile(xs,p):
    xs=sorted(xs); return xs[min(len(xs)-1,int(p*(len(xs)-1)))]
def evaluate(block,boot=4000):
    stem=f'verificacao-cega-v2-{block.lower()}'
    manifest=readj(BASE/'fila'/f'{stem}-manifesto.json')
    labels={x['id']:x for x in readl(BASE/'fila'/f'{stem}-rotulos-independentes.jsonl')}
    public={x['id']:x for x in readl(BASE/'fila'/f'{stem}.jsonl')}
    hidden={x['id']:x for x in manifest['rotulos_ocultos']}
    prog=readl(BASE/'concursos/cgu-affc-ti-ds/programa.json')
    valid={x['codigo'] for x in prog}
    rows=[]; errors=[]
    for ident,h in hidden.items():
        lab=labels.get(ident); item=public.get(ident)
        if lab is None or item is None: continue
        if lab.get('decisao')=='edital': real=parent(lab.get('codigo'))
        elif lab.get('decisao')=='fora_edital': real=None
        else: real='AMBIGUO'
        if lab.get('codigo') and lab['codigo'] not in valid: errors.append({'id':ident,'erro':'codigo inexistente','codigo':lab['codigo']})
        if not lab.get('justificativa') or len(lab.get('justificativa',''))<25: errors.append({'id':ident,'erro':'justificativa curta/ausente'})
        rows.append({'id':ident,'estrato':h['estrato'],'pred':parent(h.get('triagem')),'real':real,'amb':real=='AMBIGUO',
                     'conf':lab.get('confianca'),'human_code':lab.get('codigo'),'hidden_code':h.get('edital_prov')})
    strata={}
    for s in ('baixo','medio','alto'):
        r=[x for x in rows if x['estrato']==s and not x['amb']]
        w=float(manifest['peso_expansao_por_estrato'][s] or 0)
        tp=sum(w for x in r if x['pred']==x['real'] and x['real'] is not None)
        fp=sum(w for x in r if x['pred'] is not None and x['pred']!=x['real'])
        strata[s]={'n':len(r),'peso':w,'tp':tp,'fp':fp,'precisao':tp/max(1e-12,tp+fp)}
    tp=sum(x['tp'] for x in strata.values());fp=sum(x['fp'] for x in strata.values())
    precision=tp/max(1e-12,tp+fp)
    rng=random.Random(20261110+(2 if block=='P2' else 3));bs_p=[];bs_r=[]
    for _ in range(boot):
        a=b=0
        for s in ('baixo','medio','alto'):
            rr=[x for x in rows if x['estrato']==s and not x['amb']]
            w=strata[s]['peso']
            if not rr: continue
            draw=[rng.choice(rr) for _ in rr]
            a+=sum(w for x in draw if x['pred']==x['real'] and x['real'] is not None)
            b+=sum(w for x in draw if x['pred'] is not None and x['pred']!=x['real'])
        bs_p.append(a/max(1e-12,a+b))
    out={'bloco':block,'metodo':'auditoria cega estratificada por tercil de score, ponderada pelo inverso da fração amostral',
         'n_manifesto':manifest['n'],'n_rotulado':len(rows),'n_ambiguo':sum(x['amb'] for x in rows),'erros_integridade':errors,
         'por_estrato':strata,'precisao_ponderada':precision,'precisao_ic90':[percentile(bs_p,.05),percentile(bs_p,.95)],
         'recall_ponderado':None,'recall_ic90':None,'recall_status':'nao_estimavel: amostra v2 foi retirada do conjunto recuperado; nao inclui sorteio representativo dos descartados',
         'regra':'sem confiança alta automática nesta auditoria; intervalo e divergências permanecem visíveis',
         'amostra_ids':len(rows)}
    return out
def main():
    out={b:evaluate(b) for b in ('P2','P3')}
    dest=BASE/'docs'/'auditoria-cega-prioridade.json'
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({b:{k:v for k,v in x.items() if k!='por_estrato'} for b,x in out.items()},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
