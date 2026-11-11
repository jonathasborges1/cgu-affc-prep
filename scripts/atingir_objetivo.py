#!/usr/bin/env python3
"""Orquestrador de uma invocação para perseguir a prioridade confiável recursivamente.

Uma invocação pode repetir ciclos locais/coleta; nunca declara sucesso por ter
terminado. Gates sem evidência ou etapas humanas/rede indisponíveis ficam no
relatório docs/objetivo-status.json.
"""
import argparse, datetime, json, os, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts')); sys.path.insert(0,str(ROOT))
import banco as B

def run(cmd,timeout,cwd=ROOT):
    try:
        p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=max(1,timeout))
        return {'comando':' '.join(map(str,cmd)),'returncode':p.returncode,'stdout':p.stdout[-2500:],'stderr':p.stderr[-1200:]}
    except Exception as e:return {'comando':' '.join(map(str,cmd)),'returncode':None,'erro':str(e)}

def confidence():
    import prioridade as P
    r=P.priorizar(1); blocks={}
    for b in ('P1','P2','P3'):
        z=r.get('calibracao',{}).get(b,{})
        blocks[b]={'assuntos_calibrados':z.get('calibrados'),'assuntos_total':z.get('total'),
                   'ordem_por_faixas_confiavel':bool(z.get('ordem_por_faixas_confiavel')),
                   'ordem_exata_confiavel':z.get('ordem_exata_confiavel',0)}
    return blocks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prompt',default='PROMPT_EXECUCAO_1_ITERACAO.md');ap.add_argument('--max-ciclos',type=int,default=4)
    ap.add_argument('--max-provas',type=int,default=12);ap.add_argument('--tempo-total',type=int,default=600);ap.add_argument('--pausa',type=float,default=5)
    a=ap.parse_args();start=time.monotonic();deadline=start+a.tempo_total
    prompt=ROOT/a.prompt
    if not prompt.exists():raise SystemExit('prompt operacional não encontrado: '+str(prompt))
    report={'inicio':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),'concurso':os.path.basename(B.CONC),
            'prompt':str(prompt.relative_to(ROOT)),'ciclos':[],'objetivo_atingido':False,'bloqueios':[]}
    for cycle in range(1,a.max_ciclos+1):
        if time.monotonic()>=deadline:report['bloqueios'].append('orçamento de tempo esgotado');break
        entry={'ciclo':cycle,'tarefas':[]}
        entry['tarefas'].append(run([sys.executable,str(ROOT/'scripts/auditar_prioridade_cega.py')],deadline-time.monotonic()))
        cat=run([sys.executable,str(ROOT/'scripts/descobrir.py'),'catalogo','--tempo',str(max(1,int(min(90,deadline-time.monotonic()))))],deadline-time.monotonic())
        entry['tarefas'].append(cat)
        if cat.get('returncode')==0:
            entry['tarefas'].append(run([sys.executable,str(ROOT/'scripts/descobrir.py'),'ranquear'],deadline-time.monotonic()))
            entry['tarefas'].append(run([sys.executable,str(ROOT/'scripts/descobrir.py'),'varrer','--max-provas',str(max(1,a.max_provas//a.max_ciclos)),'--tempo',str(max(1,int(min(150,deadline-time.monotonic())))),'--forte','10','--fraco','8','--ganho-min','-1','--alvo-total','1000000'],deadline-time.monotonic()))
        else:
            detalhe=(cat.get('stderr') or cat.get('erro') or 'erro sem detalhe')[-400:]
            dns=('getaddrinfo failed' in detalhe.lower() or 'could not resolve host' in detalhe.lower()
                 or 'name or service not known' in detalhe.lower())
            if dns:
                report['bloqueios'].append('DNS/saída de rede indisponível no processo restrito; a correção é liberar HTTPS para este processo ou executar a coleta em contexto com rede autorizada. O DNS global do Windows não deve ser alterado. Detalhe: '+detalhe)
            else:
                report['bloqueios'].append('descoberta online indisponível: '+detalhe)
        for cmd in ([ROOT/'scripts/classificar_p1_sklearn.py'],[ROOT/'scripts/ml_triagem.py','validar'],[ROOT/'scripts/ml_triagem.py','recall']):
            if time.monotonic()>=deadline:break
            entry['tarefas'].append(run([sys.executable,*map(str,cmd)],deadline-time.monotonic()))
        entry['confianca']=confidence();report['ciclos'].append(entry)
        if all(entry['confianca'][b]['ordem_por_faixas_confiavel'] for b in ('P1','P2','P3')):
            report['objetivo_atingido']=True;break
        if cat.get('returncode')!=0 or time.monotonic()>=deadline:break
    report['confianca_final']=confidence()
    report['provas_novas']=sum(1 for p in B.provas() if any(h.get('etapa')=='extraida' and 'descobrir.py' in str(h.get('nota')) for h in p.get('historico',[])))
    report['pendencias_semanticas']=[{'prova_id':p['prova_id'],'estado':p['estado'],'proximo':'classificação semântica/verificação independente exige revisão dedicada'} for p in B.provas() if p.get('estado') in ('extraida','classificada','verificada')]
    if not report['objetivo_atingido']:
        for b,x in report['confianca_final'].items():
            if not x['ordem_por_faixas_confiavel']:report['bloqueios'].append(f'{b}: gates de confiança da ordem ainda não aprovados')
    report['fim']=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    report['observacao']='O orquestrador concluiu a invocação. Isto não equivale a atingir o objetivo quando objetivo_atingido=false.'
    dest=ROOT/'docs/objetivo-status.json';dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'relatorio':str(dest),'objetivo_atingido':report['objetivo_atingido'],'ciclos':len(report['ciclos']),'confianca':report['confianca_final'],'bloqueios':report['bloqueios']},ensure_ascii=False,indent=2))
    return 0 if report['objetivo_atingido'] else 2
if __name__=='__main__':raise SystemExit(main())
