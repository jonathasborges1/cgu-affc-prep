#!/usr/bin/env python3
"""Orquestra, sem fabricar evidencias, os gates restantes da prioridade P2.

O comando e idempotente. Ele prepara a segunda leitura cega, consolida rotulos
somente quando nao ha divergencias pendentes, recalcula os relatorios e informa
o proximo bloqueio verificavel.
"""
import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
FILA=BASE/'fila';DOCS=BASE/'docs';PACOTE=FILA/'revisao-cega-p2-recall'
AMOSTRA=FILA/'calibracao-p2-descartados.jsonl'
PRIMEIRA=FILA/'calibracao-p2-descartados.rotulos.json'
SEGUNDA=PACOTE/'rotulos-segunda-leitura.json'
ADJ_PACOTE=FILA/'revisao-cega-p2-adjudicacao'
ADJ=ADJ_PACOTE/'rotulos.json'
AUDITADOS=FILA/'calibracao-p2-descartados.rotulos-auditados.json'
STATUS=DOCS/'revisao-cega-p2-recall-status.json'
AMP=FILA/'revisao-cega-p2-ampliacao-1';AMP_FINAL=FILA/'p2-ampliacao-1-rotulos.json'
MID=FILA/'revisao-cega-p2-mid-censo';MID_FINAL=FILA/'p2-mid-censo-rotulos.json'

def load(path,default=None):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return default

def dump(path,obj):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def rows(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x.strip()]

def norm_primeira(itens):
    raw=load(PRIMEIRA,{}) or {};out={}
    for i,x in enumerate(itens,1):out[x['id']]=raw.get(str(i),raw.get(x['id']))
    return out

def preparar():
    itens=rows(AMOSTRA);PACOTE.mkdir(parents=True,exist_ok=True)
    src=PACOTE/'amostra.jsonl'
    src.write_text(''.join(json.dumps(dict(x,bloco='P2'),ensure_ascii=False)+'\n' for x in itens),encoding='utf-8')
    cmd=[sys.executable,str(BASE/'scripts/revisao_cega_calibracao.py'),'preparar',str(src),'--saida',str(PACOTE),'--tamanho','20']
    subprocess.run(cmd,cwd=BASE,check=True)
    # O template padrao vira explicitamente a segunda leitura.
    template=load(PACOTE/'rotulos.json',{})
    if not SEGUNDA.exists():dump(SEGUNDA,template)
    prompt=("# Segunda leitura cega de recall P2\n\n"
      "Leia somente os arquivos `lote-01.md` a `lote-15.md`. Nao consulte previsoes, pesos, "
      "a primeira leitura nem relatorios. Para cada ID, escolha exatamente um codigo de nivel 1 "
      "da taxonomia impressa no lote ou `OUTRO`. Grave o mapa completo em "
      "`rotulos-segunda-leitura.json`.\n")
    (PACOTE/'PROMPT-SEGUNDA-LEITURA.md').write_text(prompt,encoding='utf-8')
    return {'preparado':True,'itens':len(itens),'lotes':15,'pacote':str(PACOTE)}

def completos(mapping,ids):
    return isinstance(mapping,dict) and set(mapping)==set(ids) and all(mapping.get(i) for i in ids)

def mesclar_partes(ids):
    partes=[load(PACOTE/f'rotulos-parte-{n}.json',{}) or {} for n in (1,2,3)]
    if not all(partes):return None
    unido={}
    for parte in partes:
        repetidos=set(unido)&set(parte)
        if repetidos:raise SystemExit('IDs repetidos entre partes da segunda leitura')
        unido.update(parte)
    if set(unido)!=set(ids):raise SystemExit('partes da segunda leitura nao cobrem exatamente a amostra')
    dump(SEGUNDA,unido);return unido

def mesclar_partes_dir(pacote,ids):
    partes=[load(pacote/f'rotulos-parte-{n}.json',{}) or {} for n in (1,2,3)]
    if not all(partes):return None
    unido={}
    for parte in partes:
        if set(unido)&set(parte):raise SystemExit('IDs repetidos entre partes')
        unido.update(parte)
    if set(unido)!=set(ids):raise SystemExit('partes nao cobrem exatamente a ampliacao')
    return unido

def preparar_ampliacao():
    cand=load(BASE/'tmp/p2ml/cand.json',[]) or [];usados=set()
    D=load(BASE/'tmp/p2ml/data.json',{}) or {}
    for x in D.get('P2',[])+D.get('DES',[]):usados.add(x['k'])
    for nome in ('round1.json','census.json','tail.json'):
        obj=load(BASE/'tmp/p2ml'/nome,{})
        if isinstance(obj,list):usados.update(x['k'] for x in obj)
        elif isinstance(obj,dict):
            for v in obj.values():
                if isinstance(v,list):usados.update(x['k'] for x in v if isinstance(x,dict) and x.get('k'))
    for x in load(BASE/'tmp/p2ml/lote/rotulos_extra.json',[]) or []:usados.add(x['k'])
    mid=[x for x in cand if x['k'] not in usados and .3<=float(x['p'])<.6]
    tail=[x for x in cand if x['k'] not in usados and float(x['p'])<.3]
    rng=random.Random(20261110);sel=[]
    for fonte,pool,n in (('mid3',mid,150),('tail3',tail,150)):
        for x in rng.sample(pool,min(n,len(pool))):
            sel.append({'id':x['k'],'bloco':'P2','fonte':fonte,'ano':x['ano'],'enunciado':x['t']})
    AMP.mkdir(parents=True,exist_ok=True);src=AMP/'amostra.jsonl'
    src.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sel),encoding='utf-8')
    manifesto=load(AMP/'manifesto.json',{}) or {}
    if manifesto.get('ids')!=[x['id'] for x in sel]:
        subprocess.run([sys.executable,str(BASE/'scripts/revisao_cega_calibracao.py'),'preparar',str(src),
          '--saida',str(AMP),'--tamanho','20'],cwd=BASE,check=True)
    return {'preparada':True,'itens':len(sel),'mid':sum(x['fonte']=='mid3' for x in sel),'tail':sum(x['fonte']=='tail3' for x in sel),'pacote':str(AMP)}

def consolidar_ampliacao():
    itens=rows(AMP/'amostra.jsonl');ids=[x['id'] for x in itens];rot=mesclar_partes_dir(AMP,ids)
    if not rot:return {'concluida':False,'bloqueio':'rotulagem_ampliacao_incompleta','itens':len(ids)}
    out=[{'k':x['id'],'ano':x['ano'],'fonte':x['fonte'],'y':rot[x['id']]} for x in itens]
    dump(AMP_FINAL,out)
    return {'concluida':True,'itens':len(out),'positivos':sum(x['y']!='OUTRO' for x in out),'arquivo':str(AMP_FINAL)}

def preparar_mid_censo():
    cand=load(BASE/'tmp/p2ml/cand.json',[]) or [];usados=set()
    for p in (BASE/'tmp/p2ml/data.json',):
        D=load(p,{}) or {};usados.update(x['k'] for x in D.get('P2',[])+D.get('DES',[]))
    for nome in ('round1.json','census.json','tail.json'):
        obj=load(BASE/'tmp/p2ml'/nome,{})
        if isinstance(obj,list):usados.update(x['k'] for x in obj)
        elif isinstance(obj,dict):
            for v in obj.values():
                if isinstance(v,list):usados.update(x['k'] for x in v if isinstance(x,dict) and x.get('k'))
    usados.update(x['k'] for x in load(BASE/'tmp/p2ml/lote/rotulos_extra.json',[]) or [])
    usados.update(x['k'] for x in load(AMP_FINAL,[]) or [])
    sel=[{'id':x['k'],'bloco':'P2','fonte':'mid4','ano':x['ano'],'enunciado':x['t']}
         for x in cand if x['k'] not in usados and .3<=float(x['p'])<.6]
    MID.mkdir(parents=True,exist_ok=True);src=MID/'amostra.jsonl'
    src.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sel),encoding='utf-8')
    manifesto=load(MID/'manifesto.json',{}) or {}
    if manifesto.get('ids')!=[x['id'] for x in sel]:
        subprocess.run([sys.executable,str(BASE/'scripts/revisao_cega_calibracao.py'),'preparar',str(src),
          '--saida',str(MID),'--tamanho','20'],cwd=BASE,check=True)
    return {'preparado':True,'itens':len(sel),'lotes':(len(sel)+19)//20,'pacote':str(MID)}

def consolidar_mid_censo():
    itens=rows(MID/'amostra.jsonl');ids=[x['id'] for x in itens];partes=[]
    for n in range(1,7):
        p=load(MID/f'rotulos-parte-{n}.json',{}) or {}
        if not p:return {'concluida':False,'bloqueio':'rotulagem_mid_censo_incompleta','parte_pendente':n,'itens':len(ids)}
        partes.append(p)
    unido={}
    for p in partes:
        if set(unido)&set(p):raise SystemExit('IDs repetidos nas partes do censo intermediario')
        unido.update(p)
    if set(unido)!=set(ids):raise SystemExit('partes do censo intermediario nao cobrem exatamente a amostra')
    out=[{'k':x['id'],'ano':x['ano'],'fonte':'mid4','y':unido[x['id']]} for x in itens];dump(MID_FINAL,out)
    return {'concluida':True,'itens':len(out),'positivos':sum(x['y']!='OUTRO' for x in out),'arquivo':str(MID_FINAL)}

def consolidar():
    itens=rows(AMOSTRA);ids=[x['id'] for x in itens];a=norm_primeira(itens);b=mesclar_partes(ids) or load(SEGUNDA,{}) or {}
    if not completos(b,ids):
        return {'concluida':False,'bloqueio':'segunda_leitura_incompleta','preenchidos':sum(bool(b.get(i)) for i in ids),'itens':len(ids)}
    dif=[i for i in ids if a.get(i)!=b.get(i)]
    if dif:
        adj=load(ADJ,{}) or {}
        if set(adj)!=set(dif) or any(not adj.get(i) for i in dif):
            dump(PACOTE/'divergencias.json',{i:{'primeira':a.get(i),'segunda':b.get(i)} for i in dif})
            ADJ_PACOTE.mkdir(parents=True,exist_ok=True)
            fonte=ADJ_PACOTE/'amostra.jsonl';por_id={x['id']:x for x in itens}
            fonte.write_text(''.join(json.dumps(dict(por_id[i],bloco='P2'),ensure_ascii=False)+'\n' for i in dif),encoding='utf-8')
            manifesto=load(ADJ_PACOTE/'manifesto.json',{}) or {}
            if manifesto.get('ids')!=dif:
                subprocess.run([sys.executable,str(BASE/'scripts/revisao_cega_calibracao.py'),'preparar',str(fonte),
                  '--saida',str(ADJ_PACOTE),'--tamanho','20'],cwd=BASE,check=True)
            return {'concluida':False,'bloqueio':'adjudicacao_pendente','divergencias':len(dif),'arquivo':str(ADJ)}
    else:adj={}
    final={i:(adj[i] if i in dif else b[i]) for i in ids};dump(AUDITADOS,final)
    concord=sum(a.get(i)==b.get(i) for i in ids)/len(ids)
    st={'concluida':True,'itens':len(ids),'concordancia':round(concord,4),'divergencias':len(dif),
        'divergencias_pendentes':0,'rotulos_auditados':str(AUDITADOS.relative_to(BASE))}
    dump(STATUS,st);return st

def run(script,*args):
    return subprocess.run([sys.executable,str(BASE/'scripts'/script),*args],cwd=BASE,check=True,capture_output=True,text=True).stdout.strip()

def recalcular():
    saidas={}
    for script in ('confianca_ordem.py','confiabilidade_blocos.py'):
        saidas[script]=run(script)[-1000:]
    run('prioridade.py','--json',str(DOCS/'prioridade-atual.json'))
    publicar_ordem()
    return saidas

def publicar_ordem():
    e=(load(DOCS/'confianca-ordem.json',{}) or {}).get('P2',{});shares=e.get('share') or {};ics=e.get('ic90') or {}
    ordem=[]
    for pos,(codigo,share) in enumerate(sorted(shares.items(),key=lambda x:(-x[1],x[0])),1):
        ordem.append({'posicao_estimada':pos,'codigo':codigo,'participacao':share,'ic90':ics.get(codigo),
          'faixa_por_participacao':'A' if share>=.08 else ('B' if share>=.04 else 'C')})
    d=diagnostico();out={'status':'confiavel_por_faixas' if d['objetivo_atingido'] else 'provisoria','alta_confianca':d['objetivo_atingido'],
      'metodo':'amostra estratificada ponderada, segunda leitura cega, adjudicacao e bootstrap',
      'gates':d['gates'],'valores_gates':d['valores'],'ordem':ordem,
      'aviso':'A ordem por faixas esta certificada; posicoes exatas continuam informativas, nao certificadas.' if d['objetivo_atingido'] else 'Nao usar posicoes exatas como certificadas enquanto os gates nao passarem.'}
    dump(DOCS/'ordem-p2-auditada.json',out);return out

def diagnostico():
    e=(load(DOCS/'confianca-ordem.json',{}) or {}).get('P2',{})
    c=(load(DOCS/'confiabilidade-blocos.json',{}) or {}).get('blocos',{}).get('P2',{})
    f=e.get('faixas') or {};t=e.get('temporal') or {};r=e.get('recall_auditoria') or {};am=e.get('amostragem_probabilistica') or {}
    gates={'amostra_completa':bool((c.get('gates') or {}).get('amostra_completa')),
      'sem_duplicados':bool((c.get('gates') or {}).get('sem_duplicados')),
      'estabilidade_faixas_fixas_0_80':float(f.get('fracao') or 0)>=.80,
      'temporal_recencia_ponderado_0_85':float(t.get('razao_recencia_ponderada') or 0)>=.85,
      'pior_periodo_recente_0_70':t.get('pior_fold_recente') is not None and float(t['pior_fold_recente'])>=.70,
      'amostragem_probabilistica_aprovada':bool(am.get('aprovada') and am.get('sem_imputacao_modelo'))}
    objetivo=all(gates.values());mid_censo=MID_FINAL.exists()
    out={'objetivo_atingido':objetivo,'gates':gates,
      'valores':{'estabilidade':f.get('fracao'),'instaveis':f.get('instaveis'),'temporal_recente':t.get('razao_recencia_ponderada'),
      'temporal_todos_periodos':t.get('razao_ponderada'),'pior_periodo_recente':t.get('pior_fold_recente'),
      'pior_periodo_historico':t.get('pior_fold'),'folds':len(t.get('folds') or []),'recall_lido_diagnostico':e.get('recall_leitura'),
      'amostra_cauda':am.get('cauda_amostra'),'margem_maxima_90':am.get('margem_maxima_90')},'confiavel_publicado':bool(c.get('confiavel'))}
    if mid_censo and not objetivo:
        out['parada_segura']={'ativa':True,'motivo':'censo da faixa intermediaria concluido; a cauda restante e grande e os gates empiricos reprovaram',
          'cauda_itens':13163,'alternativas':['classificar uma parcela substancial da cauda com nova auditoria independente',
          'desenvolver classificador semantico e valida-lo em amostra cega antes de imputar rotulos',
          'alterar o criterio somente por decisao metodologica explicita, nunca automaticamente']}
    return out

def continuar(max_ciclos=4):
    historico=[]
    preparar()
    for _ in range(max_ciclos):
        cons=consolidar();historico.append({'consolidacao':cons})
        recalcular();d=diagnostico();historico[-1]['diagnostico']=d
        if d['objetivo_atingido'] or not cons.get('concluida'):break
        if not (d['gates']['estabilidade_faixas_fixas_0_80'] and d['gates']['temporal_recencia_ponderado_0_85']):
            preparar_ampliacao();amp=consolidar_ampliacao();historico[-1]['ampliacao']=amp
            if not amp.get('concluida'):break
            recalcular();historico[-1]['diagnostico_apos_ampliacao']=diagnostico()
            if historico[-1]['diagnostico_apos_ampliacao']['objetivo_atingido']:break
        if not MID_FINAL.exists():
            preparar_mid_censo();mid=consolidar_mid_censo();historico[-1]['mid_censo']=mid
            if not mid.get('concluida'):break
            recalcular();historico[-1]['diagnostico_apos_mid_censo']=diagnostico()
        # Sem nova evidencia, repetir produziria o mesmo resultado.
        break
    out={'historico':historico,'final':diagnostico()};dump(DOCS/'finalizacao-p2-status.json',out);return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('acao',choices=('preparar','consolidar','preparar-ampliacao','consolidar-ampliacao','preparar-mid-censo','consolidar-mid-censo','recalcular','status','continuar'));ap.add_argument('--max-ciclos',type=int,default=4);a=ap.parse_args()
    if a.acao=='preparar':out=preparar()
    elif a.acao=='consolidar':out=consolidar()
    elif a.acao=='preparar-ampliacao':out=preparar_ampliacao()
    elif a.acao=='consolidar-ampliacao':out=consolidar_ampliacao()
    elif a.acao=='preparar-mid-censo':out=preparar_mid_censo()
    elif a.acao=='consolidar-mid-censo':out=consolidar_mid_censo()
    elif a.acao=='recalcular':out=recalcular()
    elif a.acao=='status':out=diagnostico()
    else:out=continuar(a.max_ciclos)
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
