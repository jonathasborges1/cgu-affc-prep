#!/usr/bin/env python3
"""Painel de prioridade: funil de dados, material por assunto, semaforo de aula e confianca da ordem.
Tudo derivado de arquivos do banco; limiares ficam em LIM e sao descritos no modal da tela."""
import json,glob,os,time,collections
import plano_aulas as PA
HERE=os.path.dirname(os.path.abspath(__file__));B=os.environ.get('BANCO_DIR') or os.path.dirname(HERE)
C=B+'/concursos/cgu-affc-ti-ds/'
LIM={'classif_ok':20,'classif_parcial':10,'nuc_ok':6,'nuc_parcial':3,'lidos_ok':30,'lidos_parcial':15,'sobe_posicoes':3}
ALIAS={'P1 · Adm. pública 4.1':'P1·ADM 4.1'}
# itens lidos que nao saem de arquivo unico (fonte: docs/ordem-p2.md e docs/rotulos-p1-descartados.json)
LIDOS_FIXO={'P1':680,'P2':1939}
_c={}
_RC={}
def rd(p):
    """Leitura com cache por (arquivo, mtime, tamanho); só relê o que mudou."""
    try:st=os.stat(p)
    except OSError:return []
    ch=(st.st_mtime_ns,st.st_size);h=_RC.get(p)
    if h and h[0]==ch:return list(h[1])
    try:v=[json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]
    except OSError:return []
    _RC[p]=(ch,v);return list(v)
_NC={}
def nlin(p):
    try:st=os.stat(p)
    except OSError:return 0
    ch=(st.st_mtime_ns,st.st_size);h=_NC.get(p)
    if h and h[0]==ch:return h[1]
    n=sum(1 for l in open(p,encoding='utf-8') if l.strip());_NC[p]=(ch,n);return n
def nuclear_ids(value):
    """Normaliza IDs de núcleos, aceitando listas antigas aninhadas e JSON serializado."""
    if isinstance(value,str):
        s=value.strip()
        if not s:return
        try:
            parsed=json.loads(s)
        except Exception:
            try: parsed=json.loads(s.replace("'", '"'))
            except Exception: yield s
            else: yield from nuclear_ids(parsed)
        else:
            yield from nuclear_ids(parsed)
    elif isinstance(value,(list,tuple,set)):
        for item in value: yield from nuclear_ids(item)
    elif isinstance(value,dict):
        ident=value.get('id') or value.get('nucleo_id')
        if ident is not None: yield from nuclear_ids(ident)
def js(p,d=None):
    try:return json.load(open(p,encoding='utf-8'))
    except Exception:return d
def cod1(ed):
    ed=ALIAS.get(ed,ed or '')
    if ' ' not in ed or not ed[:2] in('P1','P2','P3'):return None
    pre,num=ed.rsplit(' ',1);return '%s %s'%(pre,num.split('.')[0])
def base():
    if _c.get('t',0)>time.time()-60:return _c['v']
    provas=rd(C+'provas.jsonl');ext=0;nex=0
    for f in glob.glob(B+'/extraidos/*.jsonl'):
        nex+=1;ext+=nlin(f)
    forte=collections.Counter()
    for f in glob.glob(C+'escopo/*.jsonl'):
        if os.path.basename(f).startswith('tema-'):continue
        for r in rd(f):
            c=r.get('compat');c=c if isinstance(c,dict) else {}
            if c.get('nivel')=='forte':forte[str(c.get('edital_prov',''))[:2]]+=1
    bq=rd(C+'banco.jsonl');nuc={n['id']:n for n in rd(C+'nucleos.jsonl')}
    cl=collections.Counter();sem=collections.Counter();nq=collections.defaultdict(lambda:collections.defaultdict(set))
    for x in bq:
        ed=x.get('edital') or ''
        if ed=='FORA':continue
        c=cod1(ed)
        if not c:sem[ed[:2] if ed[:2] in('P1','P2','P3') else '?']+=1;continue
        cl[c]+=1
        ns=x.get('nucleos') or []
        for n in set(nuclear_ids(ns)):
            nq[c][n].add(x.get('prova_id') or x.get('ref'))
    # Classificações que já foram produzidas, mas ainda não passaram pelo portão
    # independente. Elas não entram no banco nem nos contadores de cobertura.
    pend=collections.Counter();pend_nuc=collections.defaultdict(set)
    estados={p.get('prova_id'):p.get('estado') for p in provas}
    for f in glob.glob(C+'classificacoes/*.jsonl'):
        pid=os.path.basename(f)[:-6]
        if estados.get(pid)!='classificada':continue
        for x in rd(f):
            ed=x.get('edital') or ''
            c=cod1(ed)
            if not c:continue
            pend[c]+=1
            if x.get('nucleo_id'):pend_nuc[c].add(x['nucleo_id'])
    v={'provas':provas,'extraidas':ext,'arq_ext':nex,'forte':forte,'cl':cl,'sem':sem,'nq':nq,'nuc':nuc,
       'pend':pend,'pend_nuc':pend_nuc,'banco_total':sum(cl.values())+sum(sem.values())}
    _c.update(t=time.time(),v=v);return v
def nucleos_de(v,c):
    ids=set(n for n,x in v['nuc'].items() if cod1(x.get('edital'))==c)|set(v['nq'][c])
    top=[]
    for n in ids:
        q=len(v['nq'][c].get(n,()));t=(v['nuc'].get(n) or {}).get('texto','')
        top.append({'id':n,'texto':t,'provas':q})
    top.sort(key=lambda a:(-a['provas'],a['id']))
    return len(ids),sum(1 for a in top if a['provas']>=2),top[:8]
def plano_de(v,c,P):
    ids=set(n for n,x in v['nuc'].items() if cod1(x.get('edital'))==c)|set(v['nq'][c])
    nucs=[{'id':i,'texto':(v['nuc'].get(i) or {}).get('texto',''),'provas':len(v['nq'][c].get(i,())),'edital':(v['nuc'].get(i) or {}).get('edital','')} for i in sorted(ids)]
    r=PA.planejar(nucs,P);r.pop('params',None)
    for a in r['aulas']:a.pop('nucleos',None)
    return r
def nivel3(x,ok,par):return 'ok' if x>=ok else ('parcial' if x>=par else 'falta')
def montar(out):
    """out = retorno de api_prioridade(1)."""
    v=base();rec=js(B+'/docs/recall-triagem-p3.json',{}) or {}
    fila=js(B+'/fila/classificacao-p2-dir-3.json',{}) or {}
    # Fila da rodada de confiança: mantém a recomendação da interface sincronizada
    # com os lotes AUD 3/TRANSP 2 após a classificação e aplicação.
    conf=js(B+'/fila/classificacao-p2-confianca-rodada.json',{}) or {}
    fila['temas']=conf.get('temas',{})
    fila['status_confiança']=conf.get('status')
    programa=rd(C+'programa.json')
    edital_n1=collections.Counter(x.get('prova') for x in programa if x.get('nivel')==1)
    edital_detalhes=collections.Counter(x.get('prova') for x in programa if (x.get('nivel') or 0)>1)
    cb=(js(B+'/docs/confiabilidade-blocos.json',{}) or {}).get('blocos',{})
    pos0={a:i+1 for i,a in enumerate(rec.get('ordem_sem_oculto',[]))};pos1={a:i+1 for i,a in enumerate(rec.get('ordem_com_oculto',[]))}
    PAP=PA.params(B);linhas=[];por_bloco=collections.defaultdict(list)
    for l in out['linhas']:
        c=l['codigo'];cal=l.get('calibracao') or {}
        ncl=v['cl'].get(c,0);nn,nrec,top=nucleos_de(v,c);np=int(v['pend'].get(c,0));nnp=len(v['pend_nuc'].get(c,set()))
        n=int(cal.get('n') or 0);cen=bool(cal.get('censo_completo'))
        k1=nivel3(ncl,LIM['classif_ok'],LIM['classif_parcial']);k2=nivel3(nn,LIM['nuc_ok'],LIM['nuc_parcial'])
        k3='ok' if (n>=LIM['lidos_ok'] or cen) else ('parcial' if n>=LIM['lidos_parcial'] else 'falta')
        g=(l.get('grupo_prioridade') or 'provisoria')[0]  # A,B,C,D,p
        sobe=bool(c.startswith('P3·') and c in pos0 and c in pos1 and pos0[c]-pos1[c]>=LIM['sobe_posicoes'])
        prio='alta' if g in 'AB' else ('media' if g=='C' else ('baixa' if g=='D' else 'indef'))
        if sobe and prio in('baixa','media'):prio='media_sobe'
        confiavel=bool((cb.get(l['prova']) or {}).get('confiavel'))
        if not confiavel:
            cor,tit,mot='amarelo','Ordem provisória','Os dados ajudam a estimar incidência, mas a auditoria independente deste bloco ainda não passou todos os critérios.'
            ped='Conclua a validação cega de %s: precisão, recall e backtest temporal; depois atualize docs/confiabilidade-blocos.json.'%l['prova']
        elif k3=='falta' or prio=='indef':
            cor,tit,mot='amarelo','Ordem ainda não medida','Poucos itens lidos: a posição deste assunto é só um palpite.'
            ped='Rotule às cegas mais itens "fortes" de %s (meta: %d lidos).'%(c,LIM['lidos_ok'])
        elif k1=='falta' or k2=='falta':
            if prio in('alta','media','media_sobe'):
                if np:
                    cor,tit,mot='amarelo','Aguardando verificação independente','%d itens e %d núcleos já classificados aguardam verificação; no banco há %d itens e %d núcleos.'%(np,nnp,ncl,nn)
                    ped='Os pacotes oficiais de %s já foram classificados inicialmente (%d itens, %d núcleos). Faça agora a verificação independente, compare com os limiares de edital ≥90%%, núcleo ≥80%% e pegadinha ≥80%% e, somente se aprovado, aplique ao banco. Ao terminar, informe quantos itens e núcleos foram aprovados.'%(c,np,nnp)
                else:
                    cor,tit,mot='vermelho','Ainda não: falta material','Assunto importante, mas só %d questões classificadas e %d núcleos.'%(ncl,nn)
                    if c=='P2·DIR 3':
                        ped='Próximo passo: classifique agora os pacotes oficiais de P2·DIR 3. Leia concursos/cgu-affc-ti-ds/pacotes/tema-p2-dir-3-1.md e tema-p2-dir-3-2.md; para cada item registre edital, núcleo, pegadinha e nível. Depois faça a verificação independente e só então aplique ao banco. Ao terminar, informe quantos itens e núcleos foram aprovados.'
                    else:
                        ped='Próximo passo: classifique os itens oficiais do assunto %s. Depois faça a verificação independente e só então aplique ao banco. Ao terminar, informe quantos itens e núcleos foram aprovados.'%c
            else:
                cor,tit,mot='cinza','Pode esperar','Baixa prioridade e pouco material: deixe para depois dos assuntos A e B.';ped=''
        elif k1=='parcial' or k2=='parcial':
            cor,tit,mot='amarelo','Dá para começar, falta completar','%d questões e %d núcleos: a aula sai, mas com cobertura parcial.'%(ncl,nn)
            ped='Classifique mais itens do assunto %s até chegar a %d questões e %d núcleos.'%(c,LIM['classif_ok'],LIM['nuc_ok'])
        elif prio=='alta':
            cor,tit,mot='verde','Criar aula agora','Alta prioridade, %d questões classificadas, %d núcleos.'%(ncl,nn);ped='Recomendação para %s: 1) gere a aula com `python scripts/gerar_aula.py "%s" --aula 1 --confirmar`; 2) valide o PDF e leia a aula; 3) somente se quiser treinar, gere o caderno com `python scripts/gerar_caderno.py "%s" --aula 1 --max 10 --confirmar`. Não gere o caderno junto com a aula.'%(c,c,c)
        elif prio=='media_sobe':
            cor,tit,mot='amarelo','Criar depois dos A/B (pode subir)','Hoje está no meio da ordem, mas a triagem pode estar escondendo questões deste assunto.';ped='Crie a aula de %s depois dos assuntos A e B.'%c
        elif prio=='media':
            cor,tit,mot='amarelo','Criar depois dos A/B','Prioridade média; material suficiente.';ped='Crie a aula de %s depois dos assuntos A e B.'%c
        else:
            cor,tit,mot='cinza','Pode esperar','Baixa incidência medida; material suficiente se sobrar tempo.';ped=''
        r={'codigo':c,'nome':(l.get('texto') or ''),'prova':l['prova'],'ordem':l.get('posicao_exibida') or l.get('ordem'),
           'grupo':l.get('grupo_prioridade'),'faixa':l.get('faixa'),'part':(cal.get('participacao')),'part_ic':cal.get('participacao_ic90'),
           'rank':cal.get('posicao_ic90'),'firme':bool(cal.get('posicao_firme') and l['prova']=='P1'),'lidos':n,'pool':int(cal.get('pool') or 0),'censo':cen,
           'precisao':(cal.get('acertos')/n if n else None),'classif':ncl,'nucleos':nn,'nuc_rec':nrec,'top_nucleos':top,'pendentes_verificacao':np,'nucleos_pendentes_verificacao':nnp,
           'k':{'material':k1,'nucleos':k2,'leitura':k3,'prioridade':prio},'pode_subir':sobe,
           'plano':plano_de(v,c,PAP),'cor':cor,'titulo':tit,'motivo':mot,'pedido':ped,'esp':l.get('itens_esperados')}
        linhas.append(r);por_bloco[l['prova']].append(r)
    blocos={}
    for b,rs in por_bloco.items():
        lidos_forte=sum(r['lidos'] for r in rs)
        lidos=lidos_forte+(rec.get('descartados_lidos',0) if b=='P3' else 0) if b=='P3' else LIDOS_FIXO.get(b,lidos_forte)
        nfirme=sum(r['firme'] for r in rs);nlid=sum(1 for r in rs if r['k']['leitura']=='ok')
        g=(cb.get(b) or {}).get('gates') or {}
        recall=rec.get('recall_estimado') if b=='P3' else None
        cf=(js(B+'/docs/confianca-ordem.json',{}) or {}).get(b)
        block_conf=bool((cb.get(b) or {}).get('confiavel'))
        if cf and not cf.get('erro'):
            nv=lambda x,ok=.75,par=.5:'ok' if x>=ok else ('parcial' if x>=par else 'falta')
            fx=cf['faixas'];tm=cf['temporal'];fo=tm.get('folds') or []
            pond=sum(f.get('recall_top5',0)*f['teste'] for f in fo)/max(1,sum(f['teste'] for f in fo)) if fo else 0
            if cf.get('versao')==2:
                rz=tm.get('razao_recencia_ponderada',tm['razao_ponderada']);pf=tm.get('pior_fold_recente',tm['pior_fold'])
                ts='ok' if rz>=.85 and pf>=.70 else ('parcial' if rz>=.70 and pf>=.60 else 'falta')
            else:
                ts='falta' if len(fo)<3 or tm.get('media_top5') is None else nv(tm['media_top5'])
            prec=sum((r['precisao'] or 0)*r['lidos'] for r in rs)/max(1,sum(r['lidos'] for r in rs))
            checks=[
             {'k':'leitura','t':'Questões lidas por assunto','s':'ok' if nlid==len(rs) else ('parcial' if nlid>=len(rs)/2 else 'falta'),'d':'%d de %d assuntos com ≥%d lidas (ou todas lidas)'%(nlid,len(rs),LIM['lidos_ok'])},
             {'k':'recall','t':'Amostragem probabilística','s':'ok' if (cf.get('amostragem_probabilistica') or {}).get('aprovada') else 'falta','d':('cauda n=%d; margem máxima IC90 %.1f%% (limite 4%%)'%((cf.get('amostragem_probabilistica') or {}).get('cauda_amostra',0),100*(cf.get('amostragem_probabilistica') or {}).get('margem_maxima_90',1)))},
             {'k':'faixas','t':'Faixas A/B/C estáveis','s':nv(fx['fracao'],.8,.6 if cf.get('versao')==2 else .5),'d':'%d de %d assuntos relevantes (≥1%%) ficam na mesma faixa em 80%% das reamostragens (meta ≥80%%)'%(fx['estaveis'],fx['relevantes'])},
             {'k':'temporal','t':'Teste em anos diferentes','s':ts,'d':('%d testes; cobertura relativa %d%% (pior período: %d%%; metas: média ≥85%% e nenhum período <70%%)'%(len(fo),round(100*tm['razao_ponderada']),round(100*tm['pior_fold']))) if cf.get('versao')==2 else '%d testes; a ordem de anos anteriores acerta em média %d%% dos 5 primeiros do ano seguinte (%d%% ponderando pelo tamanho do teste; meta ≥75%%)'%(len(fo),round(100*(tm.get('media_top5') or 0)),round(100*pond))},
             {'k':'firmes','t':'Posições exatas firmes','s':'ok' if nfirme>=len(rs)*.6 else ('parcial' if nfirme>=2 else 'falta'),'d':'%d de %d assuntos mantêm a posição exata ao reamostrar. Informativo: o estudo usa faixas'%(nfirme,len(rs)),'info':True},
             {'k':'precisao','t':'Acerto da triagem por palavras','s':'ok' if prec>=.85 else 'falta','d':'medido %d%% (meta 85%%). Informativo: mede esforço de leitura, não a correção da ordem, que vem das questões lidas'%round(100*prec),'info':True}]
            C_=[c_ for c_ in checks if not c_.get('info')];S_={c_['k']:c_['s'] for c_ in C_}
            niv='alto' if block_conf and all(x=='ok' for x in S_.values()) else ('medio' if S_['leitura']=='ok' and S_['recall']!='falta' and S_['faixas']!='falta' else 'baixo')
            ok=sum(x=='ok' for x in S_.values());ntot=len(C_);instaveis=fx.get('instaveis') or []
        else:
            checks=[
             {'k':'leitura','t':'Questões lidas por assunto','s':'ok' if nlid==len(rs) else ('parcial' if nlid>=len(rs)/2 else 'falta'),'d':'%d de %d assuntos com ≥%d lidas (ou todas lidas)'%(nlid,len(rs),LIM['lidos_ok'])},
             {'k':'firmes','t':'Posições firmes','s':'ok' if nfirme>=len(rs)*.6 else ('parcial' if nfirme>=2 else 'falta'),'d':'%d de %d assuntos mantêm a posição ao reamostrar'%(nfirme,len(rs))},
             {'k':'recall','t':'Recall (o que a triagem deixa escapar)','s':('ok' if recall and recall>=.75 else ('falta' if recall is not None else 'parcial')),'d':('~%d%% do conteúdo é encontrado (meta ≥75%%)'%round(100*recall)) if recall is not None else 'medido em amostra de descartados (ver tabela técnica)'},
             {'k':'precisao','t':'Acerto da triagem por palavras','s':'ok' if g.get('precisao_minima_0_85') else 'falta','d':'meta ≥85%'+(('; medido %d%%'%round(100*sum((r['precisao'] or 0)*r['lidos'] for r in rs)/max(1,sum(r['lidos'] for r in rs)))) if b in('P2','P3') else '')},
             {'k':'temporal','t':'Teste em anos diferentes','s':'ok' if g.get('tres_folds_temporais') else 'falta','d':'meta: 3 testes; hoje %d'%len(((cb.get(b) or {}).get('backtest_temporal') or {}).get('folds',[]))},
            ]
            if b=='P1' and (cb.get(b) or {}).get('confiavel'):
                for c_ in checks:
                    if c_['k'] in('precisao','temporal'):c_['s']='ok';c_['d']='calibração e backtest concluídos'
            ok=sum(c_['s']=='ok' for c_ in checks)
            niv='alto' if ok==len(checks) else ('medio' if checks[0]['s']=='ok' and checks[2]['s']!='parcial' and nfirme>=2 else 'baixo')
            if b=='P1' and (cb.get(b) or {}).get('confiavel'):niv='alto' if checks[0]['s']=='ok' else 'medio'
            ntot=len(checks);instaveis=[]
        blocos[b]={'nivel':niv,'checks':checks,'testes_ok':ok,'testes_total':ntot,'faixas_instaveis':instaveis,'lidos':lidos,'assuntos':len(rs),
                   'forte':v['forte'].get(b,0),'classif':sum(r['classif'] for r in rs),'nucleos':sum(r['nucleos'] for r in rs),
                   'edital_temas':edital_n1.get(b,0),'edital_detalhes':edital_detalhes.get(b,0),
                   'temas_com_material':sum(r['classif']>0 for r in rs),'temas_sem_material':sum(r['classif']==0 for r in rs),
                   'verde':sum(r['cor']=='verde' for r in rs),'amarelo':sum(r['cor']=='amarelo' for r in rs),'vermelho':sum(r['cor']=='vermelho' for r in rs),'cinza':sum(r['cor']=='cinza' for r in rs)}
    pr=v['provas'];est=collections.Counter(p.get('estado') for p in pr)
    return {'funil':{'provas':len(pr),'provas_extraidas':est.get('extraida',0)+est.get('persistida',0),'provas_persistidas':est.get('persistida',0),
            'questoes':v['extraidas'],'banco_total':v['banco_total'],'sem_assunto':dict(v['sem']),'nucleos':len(v['nuc']),
            'forte':dict(v['forte'])},'blocos':blocos,'linhas':linhas,'limites':LIM,'plano_params':PAP,
            'fila_p2':fila,
            'recall':{k:rec.get(k) for k in('recall_estimado','taxa_oculta','p3_oculto_estimado','descartados_lidos','com_p3','fraco_contexto_amostrados')} if rec else None}
if __name__=='__main__':
    import sys;sys.path.insert(0,HERE);import prioridade as P,suficiencia as SU
    o=P.priorizar(1);r=montar(o)
    print(json.dumps(r['funil'],ensure_ascii=False));
    for b,x in r['blocos'].items():print(b,x['nivel'],{k:x[k] for k in('lidos','forte','classif','nucleos','verde','amarelo','vermelho','cinza')})
    for l in r['linhas']:
        if l['prova']=='P3':print(l['ordem'],l['codigo'],l['classif'],l['nucleos'],l['nuc_rec'],l['k'],l['cor'],l['titulo'],'SOBE' if l['pode_subir'] else '')
