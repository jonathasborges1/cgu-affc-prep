#!/usr/bin/env python3
"""Mineração guiada pela suficiência: varre provas candidatas (CDN oficial do Cebraspe) em rodadas e para quando
todos os assuntos estiverem 'suficiente' (scripts/suficiencia.py) ou quando houver rendimento decrescente.
Uso: python3 scripts/minerar.py [--max-provas 200] [--rodada 6] [--pausa 3] [--tempo-total 3000]
Regras: um PDF por vez, pausa >= 3 s entre downloads, parar no primeiro erro de bloqueio (403/429)."""
import os,sys,time,json,argparse,types
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); sys.path.insert(0,os.path.dirname(HERE))
import banco as B, descobrir as D, suficiencia as S

def bloqueado():
    """Rejeita a conclusão se as amostras cegas do classificador ainda não passaram seus gates."""
    p=__import__('prioridade')
    out=p.priorizar(1)
    return [b for b in ('P1','P2','P3') if not out.get('calibracao',{}).get(b,{}).get('ordem_por_faixas_confiavel',False)]

def fila_humana():
    """Pendências que exigem julgamento semântico e não podem ser resolvidas pelo laço local."""
    saida=[]
    for p in B.provas():
        if p.get('estado')=='extraida':
            saida.append({'prova_id':p['prova_id'],'etapa':'classificacao_semantica','acao':'classificar e validar estruturalmente','comando':'python scripts/validar_lotes.py '+p['prova_id']})
        elif p.get('estado')=='classificada':
            saida.append({'prova_id':p['prova_id'],'etapa':'verificacao_independente','acao':'sortear amostra, verificar sem ver classificação e comparar','comando':'python banco.py prova amostra '+p['prova_id']})
        elif p.get('estado')=='verificada':
            saida.append({'prova_id':p['prova_id'],'etapa':'persistencia','acao':'aplicar somente se aprovada','comando':'python banco.py aplicar '+p['prova_id']})
    path=B.PC('fila','automacao-pendencias.json')
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,'w',encoding='utf-8') as f: json.dump({'pendencias':saida,'blocos_sem_ordem_confiavel':bloqueado()},f,ensure_ascii=False,indent=2)
    return saida

def rodar_local():
    """Atualiza ML e filas locais; nenhuma classificação automática é aplicada ao banco."""
    import subprocess
    tarefas=[]
    for cmd in ([sys.executable,os.path.join(HERE,'classificar_p1_sklearn.py')],
                [sys.executable,os.path.join(HERE,'ml_triagem.py'),'tudo']):
        if time.monotonic()>=rodar_local.deadline:
            tarefas.append({'comando':os.path.basename(cmd[1]),'erro':'orçamento de tempo do ciclo esgotado'});continue
        try:
            r=subprocess.run(cmd,cwd=os.path.dirname(HERE),capture_output=True,text=True,timeout=max(1,min(1800,rodar_local.deadline-time.monotonic())))
            tarefas.append({'comando':os.path.basename(cmd[1]),'returncode':r.returncode,'resumo':r.stdout[-1200:],'erro':r.stderr[-500:] if r.returncode else ''})
        except Exception as e: tarefas.append({'comando':os.path.basename(cmd[1]),'erro':str(e)})
    path=B.PC('fila','automacao-local.json')
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,'w',encoding='utf-8') as f: json.dump({'tarefas':tarefas,'auto_aplicacao_banco':False},f,ensure_ascii=False,indent=2)
    return tarefas
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--max-provas',type=int,default=200); ap.add_argument('--rodada',type=int,default=6)
    ap.add_argument('--pausa',type=float,default=3.0); ap.add_argument('--tempo-total',type=int,default=3000); ap.add_argument('--paciencia',type=int,default=5)
    a=ap.parse_args(); orig=B.baixa
    rodar_local.deadline=time.monotonic()+a.tempo_total
    B.baixa=lambda url,dest,pausa: orig(url,dest,max(pausa,a.pausa))
    t0=time.time(); feitas=0; hist=[]
    def foto():
        r=S.calcular(1); L=r['linhas']; mi=[l for l in L if l['status']=='minerar']
        return {'n_prov':r['n_provas'],'minerar':len(mi),'forte_min':sum(l['forte'] for l in mi),'cods':sorted(l['codigo'] for l in mi)}
    f0=foto(); hist.append(f0); print('início: %d provas, %d assuntos a minerar'%(f0['n_prov'],f0['minerar']),flush=True)
    while feitas<a.max_provas and time.time()-t0<a.tempo_total:
        if hist[-1]['minerar']==0:
            pend=bloqueado()
            if pend: print('PARADA: amostra estável, mas ordem ainda sem validação independente nos blocos:',', '.join(pend))
            else: print('PARADA: todos os assuntos suficientes e ordem validada')
            break
        n_antes=hist[-1]['n_prov']
        try:
            import subprocess
            subprocess.run([sys.executable,os.path.join(HERE,'descobrir.py'),'catalogo'],check=True)
            subprocess.run([sys.executable,os.path.join(HERE,'descobrir.py'),'ranquear'],check=True)
        except SystemExit as x:
            print('PARADA: descoberta/catálogo falhou:',x); break
        except Exception as x:
            print('PARADA: descoberta/catálogo falhou:',x); break
        ns=types.SimpleNamespace(max_provas=a.rodada,tempo=170,forte=10.0,fraco=8.0,ganho_min=-1,alvo_total=10**9)
        try:
            D.varrer(ns)
        except SystemExit as x:
            print('PARADA (erro/bloqueio):',x); break
        except Exception as x:
            print('PARADA: falha inesperada na varredura; estado salvo para retomada:',x); break
        f=foto(); novas=f['n_prov']-n_antes; feitas+=max(novas,0); hist.append(f)
        print('rodada: +%d provas (total %d) | a minerar %d | fortes nos a-minerar %d'%(novas,f['n_prov'],f['minerar'],f['forte_min']),flush=True)
        if novas<=0: print('PARADA: sem provas novas (candidatas esgotadas ou falhas)'); break
        if len(hist)>a.paciencia:
            h=hist[-1-a.paciencia]
            if f['minerar']>=h['minerar'] and f['forte_min']<=h['forte_min']*1.05+1: print('PARADA: rendimento decrescente (sem avanço em %d rodadas)'%a.paciencia); break
    pend=bloqueado(); humana=fila_humana(); local=rodar_local()
    print('fim: %d provas novas; a minerar: %s; blocos sem validação: %s; pendências semânticas: %d; tarefas ML locais: %d'%(feitas,hist[-1]['cods'],','.join(pend) or 'nenhum',len(humana),len(local)))
if __name__=='__main__': main()
