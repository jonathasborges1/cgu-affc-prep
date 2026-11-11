#!/usr/bin/env python3
"""Cache de aulas do workflow CGU-AFFC.
  aula.py status "P3·SEG 1"      -> o que existe e se está em dia (local, zero crédito)
  aula.py registrar DIR --tema "P3·SEG 1" --aula 1 --nucleos n-a,n-b --itens 993_TCE_AC_008_01:87,...  (grava manifest.json e usa o ledger)
  aula.py proximos "P3·SEG 1" [--n 10] -> itens ainda não usados em cadernos (para o próximo caderno)
Regra: status 'em dia' => entregar o PDF salvo, sem gerar nada."""
import sys,json,hashlib,argparse,datetime
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
AUL=BASE/'aulas'
def conc():
    a=BASE/'concursos'/'ativo.txt'
    return BASE/'concursos'/(a.read_text().strip() if a.exists() else 'cgu-affc-ti-ds')
import os
def banco(): return [json.loads(l) for l in open(os.environ.get('AULA_BANCO') or conc()/'banco.jsonl',encoding='utf-8') if l.strip()]
def nuc_textos():
    f=os.environ.get('AULA_NUCLEOS') or str(conc()/'nucleos.jsonl')
    return {j['id']:j.get('texto','') for j in (json.loads(l) for l in open(f,encoding='utf-8') if l.strip())} if Path(f).exists() else {}
def slug(t): return t.lower().replace('·','-').replace(' ','-')
def chave(x): return '%s#%s'%(x.get('prova_id'),x.get('item'))
def estado(nucleos,b):
    e={n:sorted('%s|%s'%(chave(x),x.get('gabarito')) for x in b if n in (x.get('nucleos') or [])) for n in nucleos}
    h=hashlib.sha1(json.dumps(e,sort_keys=True).encode()).hexdigest()[:12]
    return e,h
def ledger():
    f=AUL/'cadernos_usados.jsonl'
    return {json.loads(l)['k'] for l in open(f,encoding='utf-8')} if f.exists() else set()
def cmd_status(a):
    b=banco(); d=AUL/slug(a.tema); achou=False
    if not d.exists(): print('nenhuma aula de',a.tema,'-> gerar (workflow: etapas 7+8; 1-6 só se cobertura < 70%)'); return
    for m in sorted(d.glob('aula*/manifest.json')):
        j=json.loads(m.read_text()); achou=True
        e,h=estado(j['nucleos'],b); ant=j['estado']
        novos={n:len(e[n])-len(ant.get(n,[])) for n in e if len(e[n])!=len(ant.get(n,[]))}
        pdf=m.parent/'aula.pdf'
        print('%s v%s (%s, origem=%s): %s | PDF %s'%(m.parent.name,j.get('versao',1),j['data'],j['origem'],'EM DIA' if h==j['hash'] else 'DESATUALIZADA','ok' if pdf.exists() else 'ausente'))
        if h!=j['hash']: print('  mudanças por núcleo (itens a mais):',novos or 'gabarito/itens trocados')
        print('  itens no caderno:',len(j['caderno']),'| núcleos:',len(j['nucleos']))
    if not achou: print('pasta existe mas sem manifest')
def _trava(a,cmd):
    if not getattr(a,'confirmar_caderno',False):
        sys.exit('RECUSADO: "%s" materializa caderno (e/ou grava no ledger). Cadernos so sao criados sob pedido explicito do aluno, um por vez. Use --confirmar-caderno quando ele pedir. Para ver se o tema esta pronto sem criar nada: aula.py preparar "<tema>"'%cmd)
def cmd_registrar(a):
    _trava(a,'registrar')
    b=banco(); d=Path(a.dir); n=a.nucleos.split(',')
    e,h=estado(n,b); cad=[]
    for p in a.itens.split(','):
        arq,it=p.split(':'); xs=[x for x in b if x.get('url','').endswith(arq) and str(x.get('item'))==it]
        if not xs: sys.exit('item não achado: '+p)
        cad.append(chave(xs[0]))
    m={'tema':a.tema,'aula':a.aula,'versao':a.versao,'titulo':a.titulo,'origem':'workflow','data':str(datetime.date.today()),'nucleos':n,'estado':e,'hash':h,'caderno':cad}
    d.mkdir(parents=True,exist_ok=True); (d/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=1))
    lf=AUL/'cadernos_usados.jsonl'; usados=ledger()
    with open(lf,'a',encoding='utf-8') as f:
        for k in cad:
            if k not in usados: f.write(json.dumps({'k':k,'tema':a.tema,'aula':a.aula})+'\n')
    print('manifest gravado; hash',h,'; caderno',len(cad),'itens no ledger')
def cmd_proximos(a):
    b=banco(); u=ledger(); r=[x for x in b if str(x.get('edital','')).startswith(a.tema) and chave(x) not in u]
    print(len(r),'itens inéditos para caderno de',a.tema)
    for x in r[:a.n]: print(' ',chave(x),x.get('gabarito'),x.get('nivel'),'|',(x.get('nucleos') or [''])[0],'|',x['enunciado'][:80])

from collections import Counter,defaultdict
def _it(b,tema): return [x for x in b if str(x.get('edital','')).startswith(tema) and x.get('nucleos')]
def _niv(x): return str(x.get('nivel','')).lower().replace('á','a').replace('é','e')
def _limpo(x): return x.get('gabarito')=='C' and not x.get('tags')
def selecionar(cands,cota):
    sel=[];tags=set();nivs=set();provas=set()
    rest=sorted(cands,key=lambda x:-(x.get('ano') or 0))
    ini=[x for x in rest if _limpo(x)]
    if ini: rest.remove(ini[0]); sel.append(ini[0])
    def nov(x): return 2*len(set(x.get('tags') or [])-tags)+(_niv(x) not in nivs)+(x.get('prova_id') not in provas)+(x.get('gabarito') not in {y.get('gabarito') for y in sel})*0.5
    for y in sel: tags|=set(y.get('tags') or []);nivs.add(_niv(y));provas.add(y.get('prova_id'))
    while rest and len(sel)<cota:
        rest.sort(key=lambda x:-nov(x)); x=rest[0]
        if sel and nov(x)==0: break   # saturação: nada novo (pegadinha, nível, prova)
        rest.pop(0); sel.append(x); tags|=set(x.get('tags') or []);nivs.add(_niv(x));provas.add(x.get('prova_id'))
    return sel,rest
def _res(x,nt):
    return {'k':chave(x),'prova_id':x.get('prova_id'),'item':x.get('item'),'ref':x.get('ref'),'url':x.get('url'),'url_gab':x.get('url_gab'),'ano':x.get('ano'),
     'enunciado':x['enunciado'],'gabarito':x.get('gabarito'),'nivel':x.get('nivel'),'tags':x.get('tags') or [],'padrao':x.get('padrao'),'edital':x.get('edital'),'nucleo':(x['nucleos'] or [''])[0],'nucleo_texto':nt.get((x['nucleos'] or [''])[0],'')}
def cmd_plano(a):
    _trava(a,'plano')
    b=banco(); it=_it(b,a.tema); nt=nuc_textos(); usados=ledger()
    cont=Counter();ed=defaultdict(Counter)
    for x in it:
        for n in x['nucleos']: cont[n]+=1; ed[n][x['edital']]+=1
    grp=defaultdict(list)
    for n in cont: grp[ed[n].most_common(1)[0][0]].append(n)
    ordem=sorted(grp,key=lambda g:-sum(cont[n] for n in grp[g]))
    flat=[n for g in ordem for n in sorted(grp[g],key=lambda n:-cont[n])]
    blocos=[flat[i:i+a.max_nucleos] for i in range(0,len(flat),a.max_nucleos)]
    if len(blocos)>1 and len(blocos[-1])<=2: blocos[-2]+=blocos.pop()
    alvo=max(1,round(a.fracao*len(it))); N=len(it)
    aulas=[];prev=[]
    for k,ns in enumerate(blocos,1):
        info=[];S=[];R=[]
        for n in ns:
            c=[x for x in it if n in x['nucleos']]
            cota=min(a.teto,max(1,round(len(c)/N*alvo)))
            sel,rest=selecionar(c,cota); S+=sel; R+=rest
            info.append({'id':n,'texto':nt.get(n,''),'edital':ed[n].most_common(1)[0][0],'massa':len(c),'cota':cota,'amostra':[chave(x) for x in sel],'reserva':[chave(x) for x in rest],'saturou':len(sel)<cota})
        A=[x for x in S if _limpo(x) or _niv(x)=='facil']; Bk=[x for x in S if x not in A]
        C=R+[x for x in prev]
        def chunks(L,nome):
            L=[x for x in L if chave(x) not in usados]
            return {('%s%d'%(nome,i//10+1)):[_res(x,nt) for x in L[i:i+10]] for i in range(0,len(L),10)}
        cad={}; cad.update(chunks(A,'A')); cad.update(chunks(Bk,'B')); cad.update(chunks(sorted(C,key=lambda x:-(x.get('ano') or 0))[:20],'C'))
        aulas.append({'k':k,'nucleos':info,'massa':sum(i['massa'] for i in info),'amostra':len(S),'reserva':len(R),'cadernos':cad})
        prev=S
    out={'tema':a.tema,'n_itens':N,'n_nucleos':len(cont),'alvo_amostra':alvo,'fracao':a.fracao,'teto':a.teto,'max_nucleos':a.max_nucleos,'simulacao':bool(os.environ.get('AULA_SIMULACAO')),'aulas':aulas}
    d=Path(a.saida) if a.saida else AUL/slug(a.tema); d.mkdir(parents=True,exist_ok=True)
    (d/'plano.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
    print('%d itens | %d núcleos | %d micro-aulas | amostra %d (%.0f%%) | reserva %d'%(N,len(cont),len(aulas),sum(x['amostra'] for x in aulas),100*sum(x['amostra'] for x in aulas)/N,sum(x['reserva'] for x in aulas)))
    for x in aulas: print('  micro-aula %d: %d núcleos, %d itens no banco, amostra %d, cadernos %s'%(x['k'],len(x['nucleos']),x['massa'],x['amostra'],','.join('%s(%d)'%(k,len(v)) for k,v in x['cadernos'].items())))
def comentario(q):
    v='Certo' if q['gabarito']=='C' else 'Errado'
    p=['<b>Gabarito: %s.</b>'%v]
    if q.get('nucleo_texto'): p.append('Ideia testada: '+q['nucleo_texto'])
    if q.get('padrao'): p.append('Padrão da banca: '+q['padrao'])
    if q.get('tags'): p.append('Etiquetas: '+', '.join(q['tags']))
    return ' '.join(p)
def cmd_relatorio(a):
    d=Path(a.dir); P=json.loads((d/'plano.json').read_text(encoding='utf-8')); H=__import__('html').escape
    def barras(n):
        m=max(1,n['massa']); return '<div class="bar"><i class="m" style="width:%d%%"></i></div><div class="bar"><i class="s" style="width:%d%%"></i></div>'%(100,100*len(n['amostra'])//m)
    css=open(Path(__file__).resolve().parent.parent/'aulas'/'_template'/'relatorio.css',encoding='utf-8').read() if (Path(__file__).resolve().parent.parent/'aulas'/'_template'/'relatorio.css').exists() else ''
    o=['<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Plano de micro-aulas – %s</title><style>%s</style></head><body><div class="w">'%(H(P['tema']),css)]
    if P['simulacao']: o.append('<div class="sim"><b>SIMULAÇÃO.</b> Os itens, núcleos, provas e links deste relatório são fictícios e servem só para mostrar como o plano funciona. Nada aqui entra no banco nem no caderno real.</div>')
    am=sum(x['amostra'] for x in P['aulas']); rs=sum(x['reserva'] for x in P['aulas'])
    o.append('<h1>%s</h1><p class="sub">Plano de micro-aulas e trilha de treino</p>'%H(P['tema']))
    o.append('<div class="cards"><div><b>%d</b>itens no banco</div><div><b>%d</b>núcleos (ideias testadas)</div><div><b>%d</b>micro-aulas</div><div><b>%d</b>itens de treino (%.0f%%)</div><div><b>%d</b>na reserva</div></div>'%(P['n_itens'],P['n_nucleos'],len(P['aulas']),am,100*am/max(1,P['n_itens']),rs))
    o.append('<h2>Como ler</h2><ol class="how"><li><b>Dividir:</b> os núcleos são agrupados por seção do edital e ordenados pela massa de questões (as ideias mais cobradas vêm primeiro). Cada micro-aula leva até <b>%d núcleos</b> para caber em ~30 min.</li><li><b>Amostrar:</b> cada núcleo recebe uma cota proporcional à massa (mínimo 1, máximo <b>%d</b>). Escolho primeiro uma definição limpa e depois itens que trazem pegadinha, nível ou prova diferentes. Quando o próximo item não traz nada novo, o núcleo <b>satura</b> e o resto vai para a reserva.</li><li><b>Treinar:</b> A = definições e itens fáceis; B = pegadinhas; C = mistura com micro-aulas anteriores e reserva. Cada caderno tem no máximo 10 itens.</li><li><b>Gabarito comentado:</b> montado automaticamente com a ideia testada, o padrão da banca e as etiquetas já gravados no banco (sem gastar tokens).</li></ol>'%(P['max_nucleos'],P['teto']))
    o.append('<h2>Visão geral</h2><table><tr><th>Micro-aula</th><th>Núcleos</th><th>Itens no banco</th><th>Amostra</th><th>Reserva</th><th>Cadernos</th></tr>')
    for x in P['aulas']: o.append('<tr><td><a href="#a%d">%d</a></td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%s</td></tr>'%(x['k'],x['k'],len(x['nucleos']),x['massa'],x['amostra'],x['reserva'],H(', '.join('%s (%d)'%(k,len(v)) for k,v in x['cadernos'].items()))))
    o.append('</table>')
    for x in P['aulas']:
        op=' open' if x['k']<=a.abrir else ''
        o.append('<details id="a%d"%s><summary>Micro-aula %d · %d núcleos · %d itens no banco → %d de treino</summary>'%(x['k'],op,x['k'],len(x['nucleos']),x['massa'],x['amostra']))
        o.append('<table><tr><th>Núcleo</th><th>Edital</th><th>Massa</th><th style="width:34%">Banco vs amostra</th><th>Cota</th><th>Status</th></tr>')
        for n in x['nucleos']:
            o.append('<tr><td>%s</td><td>%s</td><td>%d</td><td><div class="bar"><i class="m" style="width:%d%%"></i></div><div class="bar"><i class="s" style="width:%d%%"></i></div></td><td>%d</td><td>%s</td></tr>'%(H(n['texto'] or n['id']),H(n['edital']),n['massa'],100,100*len(n['amostra'])//max(1,n['massa']),n['cota'],'saturou com %d'%len(n['amostra']) if n['saturou'] else 'cota completa (%d)'%len(n['amostra'])))
        o.append('</table><p class="leg"><i class="m"></i> itens no banco &nbsp; <i class="s"></i> itens na amostra</p>')
        for nome,L in x['cadernos'].items():
            tipo={'A':'definições e itens fáceis','B':'pegadinhas','C':'mistura e revisão'}[nome[0]]
            o.append('<h3>Caderno %d%s · %s · %d itens</h3>'%(x['k'],nome,tipo,len(L)))
            for i,q in enumerate(L,1):
                o.append('<div class="q"><div class="tg"><span>%d</span><span>%s</span><span>%s</span>%s</div><p>%s</p><div class="meta">Ref.: %s · item %s<br>Prova: %s<br>Gab.: %s</div><details class="g"><summary>Ver gabarito comentado</summary><p>%s</p></details></div>'%(i,H(q['nucleo_texto'][:60] or q['nucleo']),H(str(q['nivel'])),''.join('<span class="t">%s</span>'%H(t) for t in q['tags']),H(q['enunciado']),H(str(q['ref'])),H(str(q['item'])),H(str(q['url'])),H(str(q['url_gab'])),comentario(q)))
        o.append('</details>')
    o.append('</div></body></html>')
    (d/'relatorio.html').write_text('\n'.join(o),encoding='utf-8'); print('gravado',d/'relatorio.html')


def cmd_preparar(a):
    """Prontidao: confere a estrutura-base (itens classificados, nucleos, aulas, itens ineditos). NAO grava nada."""
    b=banco(); it=_it(b,a.tema); u=ledger(); d=AUL/slug(a.tema)
    nuc=Counter(n for x in it for n in x['nucleos'])
    ineditos=[x for x in it if chave(x) not in u]
    aulas=[]
    for m in sorted(d.glob('aula*/manifest.json')) if d.exists() else []:
        j=json.loads(m.read_text(encoding='utf-8')); aulas.append({'aula':m.parent.name,'pdf':(m.parent/'aula.pdf').exists(),'cadernos_pdf':sorted(p.stem for p in m.parent.glob('caderno*.pdf'))})
    micro=-(-len(nuc)//a.max_nucleos) if nuc else 0
    pronto=len(it)>=3 and len(nuc)>=1
    out={'tema':a.tema,'itens_classificados':len(it),'nucleos':len(nuc),'micro_aulas_possiveis':micro,'itens_ineditos':len(ineditos),'aulas_existentes':aulas,
         'estrutura_base_ok':pronto,'proximo_passo':('pedir a aula (o caderno so depois da aula, sob pedido)' if pronto else 'classificar mais itens deste tema'),'gravou':False}
    print(json.dumps(out,ensure_ascii=False))
def _main():
    ap=argparse.ArgumentParser(); s=ap.add_subparsers(dest='c',required=True)
    p=s.add_parser('status'); p.add_argument('tema'); p.set_defaults(f=cmd_status)
    p=s.add_parser('registrar'); p.add_argument('dir'); p.add_argument('--tema',required=True); p.add_argument('--aula',type=int,required=True); p.add_argument('--versao',type=int,default=1); p.add_argument('--titulo',default='Aula'); p.add_argument('--confirmar-caderno',action='store_true'); p.add_argument('--nucleos',required=True); p.add_argument('--itens',required=True); p.set_defaults(f=cmd_registrar)
    p=s.add_parser('proximos'); p.add_argument('tema'); p.add_argument('--n',type=int,default=10); p.set_defaults(f=cmd_proximos)
    p=s.add_parser('plano'); p.add_argument('tema'); p.add_argument('--max-nucleos',type=int,default=5); p.add_argument('--fracao',type=float,default=0.28); p.add_argument('--teto',type=int,default=6); p.add_argument('--saida'); p.add_argument('--confirmar-caderno',action='store_true'); p.set_defaults(f=cmd_plano)
    p=s.add_parser('preparar'); p.add_argument('tema'); p.add_argument('--max-nucleos',type=int,default=5); p.set_defaults(f=cmd_preparar)
    p=s.add_parser('relatorio'); p.add_argument('dir'); p.add_argument('--abrir',type=int,default=1); p.set_defaults(f=cmd_relatorio)
    a=ap.parse_args(); a.f(a)
if __name__=="__main__": _main()
