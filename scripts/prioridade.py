#!/usr/bin/env python3
"""Modelo unico e conservador de prioridade de estudo.

Separa estabilidade da amostra, calibracao da triagem e retorno de estudo.
Contagem lexical sem rotulos nunca recebe selo de confiabilidade.
"""
import json, os, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=Path(os.environ.get('BANCO_DIR') or HERE.parent)
sys.path.insert(0,str(HERE))
import suficiencia as SU

PONTOS={'P1':1.0,'P2':1.0,'P3':2.0}
MINIMOS={'P1':8.0,'P2':12.0,'P3':54.0}
MIN_CALIBRACAO=15
ESTABILIDADE_MINIMA=.80

def _json(path,default):
    try: return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception: return default

def parametros():
    a=BASE/'concursos'/'ativo.txt'
    cid=a.read_text(encoding='utf-8').strip() if a.exists() else 'cgu-affc-ti-ds'
    return _json(BASE/'concursos'/cid/'parametros-estudo.json',{})

def calibracoes():
    """Converte a calibracao legada de P1 para um contrato unico."""
    p=dict(_json(BASE/'docs'/'precisao-triagem-p1.json',{}))
    p.update(_json(BASE/'docs'/'precisao-triagem-p2.json',{}))
    p.update(_json(BASE/'docs'/'precisao-triagem-p3.json',{}))
    out={}
    for cod,x in p.items():
        n=int(x.get('n') or 0); ac=int(x.get('no_assunto') or 0)
        pool=int(x.get('pool') or 0)
        censo=bool(pool and n>=pool)
        minimo_amostra=30 if cod.startswith(('P1·','P2·')) else 15
        cb=cod.split('·',1)[0]
        audit_bloco=_json(BASE/'docs'/('calibracao-%s.json'%cb.lower()),{})
        chave_audit=next((k for k in (audit_bloco.get('por_assunto') or {}) if k==cod),None)
        audit_topico=(audit_bloco.get('por_assunto') or {}).get(chave_audit,{})
        audit_ok=bool(audit_topico.get('completo') and int(audit_topico.get('rotulados') or 0)>=minimo_amostra)
        if cb=='P1':
            audit_ok=bool(_json(BASE/'docs'/'classificador-p1.json',{}).get('rotulos',0)>=500 and n>=minimo_amostra)
        gates=_json(BASE/'docs'/'confiabilidade-blocos.json',{}).get('blocos',{}).get(cb,{})
        gates_ok=bool(gates.get('confiavel'))
        out[cod]={'n':n,'acertos':ac,'precisao':ac/max(1,n),'precisao_ic90':x.get('ic90'),
                  'pool':pool,'censo_completo':censo,
                  'amostra_suficiente':bool(censo or audit_ok),
                  'calibracao_cego_completa':bool(audit_ok),
                  'triagem_aprovada':gates_ok,
                  'participacao':x.get('part'),'participacao_ic90':x.get('part_ic'),
                  'ordem_validada':x.get('ordem'),'faixa_validada':x.get('faixa'),
                  'posicao_ic90':x.get('rank'),'posicao_firme':bool(x.get('firme')),
                  'base_provas':244,'recall_medido':False,
                  'origem':'docs/precisao-triagem-%s.json'%cod[:2].lower()}
    return out

def _recomendar(l):
    cal=l.get('calibracao') or {}
    if not l.get('calibrado'):
        falta=max(0,MIN_CALIBRACAO-int(cal.get('n') or 0))
        motivo=('%d rotulos adicionais necessarios; ordem provisoria'%falta) if cal else 'sem amostra rotulada; ordem provisoria'
        return ('roxo','Calibrar triagem',motivo)
    if not cal.get('triagem_aprovada') and not cal.get('censo_completo'):
        return ('roxo','Prioridade provisória','amostra do tópico existe, mas a triagem ainda não passou os gates de precisão e recall')
    if not cal.get('recall_medido'):
        l['limitacao_recall']='recall ainda nao medido em itens descartados'
    if l.get('lacuna'): return ('cinza','Ensinar pela base legal','historico confirmado muito pequeno')
    if l.get('status')!='suficiente': return ('vermelho','Minerar mais provas','amostra automatica ainda instavel')
    if l.get('banco',0)<SU.MIN_CLASSIF: return ('amarelo','Classificar itens','%d de %d itens classificados'%(l.get('banco',0),SU.MIN_CLASSIF))
    c=l.get('cobertura') or {}; total=c.get('total') or 0; cob=c.get('cobertas') or 0
    if total==0 or cob/max(1,total)<SU.COB_OK: return ('verde','Pronto: criar aula','prioridade calibrada; %d itens classificados'%l.get('banco',0))
    return ('azul','Coberto: caderno e revisao','aula cobre %d/%d questoes'%(cob,total))

def _score(l,dom,p):
    bloco=l['prova']; d=max(0.0,min(1.0,float(dom.get(l['codigo'],0) or 0)))
    cfg=(p.get('topicos') or {}).get(l['codigo'],{})
    horas=max(.25,float(cfg.get('horas') or p.get('horas_padrao') or 1.0))
    disc=float(cfg.get('fator_discursiva') or (p.get('fator_discursiva') or {}).get(bloco,1.0))
    minimo=MINIMOS[bloco]/(SU.ITENS_PROVA[bloco]*PONTOS[bloco])
    boost=1+max(0,minimo-d)*float(p.get('forca_minimo',2.0))
    ganho=l['itens_esperados']*PONTOS[bloco]*(1-d)*disc*boost
    return {'dominio':d,'horas_estimadas':horas,
            'horas_origem':'configurada' if 'horas' in cfg else 'padrao',
            'pontos_item':PONTOS[bloco],'fator_discursiva':disc,
            'fator_minimo':boost,'ganho_bruto':ganho,'score_estudo':ganho/horas}

def priorizar(nivel=1,cobertura=None,dominio=None,base=None):
    r=base or SU.calcular(nivel,cobertura); cal=calibracoes(); p=parametros(); dom=dominio or {}
    por_bloco={b:[] for b in SU.ITENS_PROVA}
    for original in r['linhas']:
        l=dict(original); c=cal.get(l['codigo']); l['calibracao']=c
        l['calibrado']=bool(c and c.get('amostra_suficiente') and (c.get('calibracao_cego_completa') or c.get('censo_completo')) and c.get('triagem_aprovada'))
        if c and c.get('participacao') is not None:
            l['share_bruto']=l['share']; l['share']=float(c['participacao'])
            ic=c.get('participacao_ic90') or [l['share'],l['share']]
            l['lo'],l['hi']=map(float,ic); l['fonte_estimativa']='calibracao_manual'
        else:
            l['fonte_estimativa']='triagem_ponderada_provisoria'
        l['itens_esperados']=l['share']*SU.ITENS_PROVA[l['prova']]
        l['esp']=l['itens_esperados']; l['esp_lo']=l['lo']*SU.ITENS_PROVA[l['prova']]; l['esp_hi']=l['hi']*SU.ITENS_PROVA[l['prova']]
        l.update(_score(l,dom,p))
        # Para decisao, usa o piso do IC90. A media continua exposta como incidencia.
        piso=max(0.0,l['esp_lo'])*l['pontos_item']*(1-l['dominio'])*l['fator_discursiva']*l['fator_minimo']/l['horas_estimadas']
        l['score_conservador']=piso
        pc=(c or {}).get('posicao_ic90') or [l.get('ordem',0)]*3
        l['posicao_ic90']=pc
        # P2/P3 posicoes vieram de triagem com baixa precisao; nao as declaramos exatas ate haver auditoria propria.
        l['ordem_exata_confiavel']=bool((c or {}).get('posicao_firme') and l['prova']=='P1')
        l['posicao_exibida']=str((c or {}).get('ordem_validada')) if l['ordem_exata_confiavel'] else ('%s–%s'%(pc[0],pc[-1]) if c and c.get('posicao_ic90') and l['prova']=='P1' else 'provisoria')
        por_bloco[l['prova']].append(l)
    linhas=[]
    for bloco,L in por_bloco.items():
        def chave_ordem(x):
            c=x.get('calibracao') or {}; firme=x.get('ordem_exata_confiavel') and (c.get('ordem_validada') or 999)<=3
            return (0,c.get('ordem_validada')) if firme else (1,-x['score_conservador'],-x['score_estudo'],-x['share'],x['codigo'])
        L.sort(key=chave_ordem); acum=0
        for i,l in enumerate(L,1):
            l['ordem_estudo']=i; l['ordem']=i
            if l['prova']=='P1':
                med=(l.get('calibracao') or {}).get('ordem_validada') or i
                l['grupo_prioridade']='A essencial' if l['ordem_exata_confiavel'] and med<=3 else ('B alta' if med<=12 else ('C media' if med<=18 else 'D baixa'))
            elif l['prova']=='P2' and l.get('calibrado'):
                med=(l.get('calibracao') or {}).get('ordem_validada') or i
                l['grupo_prioridade']='A essencial' if med<=2 else ('B alta' if med<=7 else ('C media' if med<=10 else 'D baixa'))
            elif l['prova']=='P3' and l.get('calibrado'):
                med=(l.get('calibracao') or {}).get('ordem_validada') or i
                l['grupo_prioridade']='A essencial' if med<=4 else ('B alta' if med<=10 else ('C media' if med<=15 else 'D baixa'))
            else: l['grupo_prioridade']='provisoria'
            l['faixa']='A' if acum<.5 else ('B' if acum<.8 else 'C'); acum+=l['share']
            if (l.get('calibracao') or {}).get('faixa_validada'):
                l['faixa_incidencia']=l['calibracao']['faixa_validada']
            l['cor'],l['acao'],l['motivo']=_recomendar(l); linhas.append(l)
    r=dict(r); r['linhas']=linhas; total=len(linhas); ok=sum(1 for l in linhas if l['calibrado'])
    r['modelo']='prioridade-v2'; r['rotulo_estimativa']='incidencia estimada (nao probabilidade)'
    audit=_json(BASE/'docs'/'rotulos-p1-descartados.json',{})
    rec=audit.get('resumo') or {}
    recall_global=False  # auditoria existente cobre P1 e nao deve ser apresentada como recall dos demais blocos
    p1=[l for l in linhas if l['prova']=='P1']; p1ok=sum(l['calibrado'] for l in p1)
    evid=_json(BASE/'docs'/'confianca-ordem.json',{})
    conf_blocos=_json(BASE/'docs'/'confiabilidade-blocos.json',{}).get('blocos',{})
    r['calibracao']={'topicos_calibrados':ok,'topicos_total':total,'cobertura':ok/max(1,total),
                     'recall_medido':recall_global,'amostra_descartados':rec,'confiavel_para_ordem_global':False,
                     'P1':{'calibrados':p1ok,'total':len(p1),'ordem_por_faixas_confiavel':bool(conf_blocos.get('P1',{}).get('confiavel')),
                           'ordem_exata_confiavel':sum(l['ordem_exata_confiavel'] for l in p1)}}
    for bloco, itens in por_bloco.items():
        if bloco == 'P1': continue
        okb = sum(l['calibrado'] for l in itens)
        r['calibracao'][bloco] = {
            'calibrados': okb, 'total': len(itens),
            'ordem_por_faixas_confiavel': bool(conf_blocos.get(bloco,{}).get('confiavel')) and _ordem_faixas_confiavel(bloco,evid),
            'ordem_exata_confiavel': sum(l['ordem_exata_confiavel'] for l in itens),
            'motivo': 'Falta validar amostra rotulada, descartados e estabilidade das posicoes.'}
    r['formula_score']='itens_esperados * pontos_item * (1-dominio) * fator_discursiva * fator_minimo / horas'
    return r

def _ordem_faixas_confiavel(bloco,evidencias):
    """Confiança em faixas só quando estabilidade, teste temporal e auditoria de recall sustentam o bloco."""
    e=evidencias.get(bloco) or {}
    faixa=e.get('faixas') or {}
    temporal=e.get('temporal') or {}
    amostra=e.get('amostragem_probabilistica') or {}
    est=float(faixa.get('fracao') or 0)
    razao=float(temporal.get('razao_recencia_ponderada') or 0)
    pior=temporal.get('pior_fold_recente')
    return bool(est>=ESTABILIDADE_MINIMA and razao>=.85 and pior is not None and float(pior)>=.70
                and amostra.get('aprovada') and amostra.get('sem_imputacao_modelo'))

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--nivel',type=int,default=1); ap.add_argument('--json'); a=ap.parse_args()
    out=priorizar(a.nivel)
    for bloco in SU.ITENS_PROVA:
        print('\n'+bloco)
        for l in [x for x in out['linhas'] if x['prova']==bloco][:10]:
            print('%2d %-18s score=%6.2f itens=%4.1f %-22s %s'%(l['ordem'],l['codigo'],l['score_estudo'],l['itens_esperados'],l['acao'],l['fonte_estimativa']))
    if a.json: Path(a.json).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
