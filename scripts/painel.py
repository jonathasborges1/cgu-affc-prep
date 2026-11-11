#!/usr/bin/env python3
"""Painel visual do workflow (HTML dark, atualiza sozinho a cada 5 s). Abra cgu-bd/painel.html no navegador.
Mostra, por etapa: ENTRADA -> SAÍDA, gate, contagens reais, um exemplo real e o estado de cada prova. 100% local."""
import sys,os,re,json,html,collections,datetime
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE))
import banco as B
e=html.escape
def n(path): return len(B.lerj(path))
def pct(a,b): return round(100*a/b) if b else 0
prov=B.provas(); cat=B.lerj(B.PC('descoberta','catalogo.jsonl')); cand=B.lerj(B.PC('descoberta','candidatas.jsonl'))
var=[v for v in B.lerj(B.PC('descoberta','varredura.jsonl')) if 'n_itens' in v]; dups=B.lerj(B.PC('descoberta','duplicatas.jsonl'))
banco=B.rows(); prog=B.programa()
S=collections.Counter(p['estado'] for p in prov)
vistos=sum(v['n_itens'] for v in var); compat=sum(v['n_compat'] for v in var)
esc=sum(n(B.PC('escopo',p['prova_id']+'.jsonl')) for p in prov if p['estado']!='persistida')
classif=0; fora=0
for p in prov:
    for c in B.lerj(B.PC('classificacoes',p['prova_id']+'.jsonl')):
        classif+=1; fora+= str(c.get('edital')).upper()=='FORA'
verif=[p for p in prov if p.get('verificacao')]
# ---------- funil
fun=[('Catálogo Cebraspe (eventos 2021+)',len(cat)),('Provas candidatas (prova+gabarito)',len(cand)),('Provas varridas',len(var)),
     ('Itens extraídos (varridas)',vistos),('Itens compatíveis (escopo inicial)',compat),('…após remover duplicatas',compat-len(dups)),
     ('Itens classificados',classif),('…dentro do edital (não FORA)',classif-fora),('Itens no banco (persistidos)',len(banco))]
mx=max(v for _,v in fun) or 1
funil=''.join('<div class=fr><span class=fl>%s</span><div class=fb><i style="width:%.1f%%"></i></div><b>%s</b></div>'%(e(k),max(1.2,100*v/mx),v) for k,v in fun)
# ---------- provas
COR={'descoberta':'#6b7280','baixada':'#60a5fa','extraida':'#fbbf24','classificada':'#a78bfa','verificada':'#34d399','persistida':'#22c55e','bloqueada':'#ef4444'}
linhas=[]
for p in sorted(prov,key=lambda p:(B.ESTADOS.index(p['estado']) if p['estado'] in B.ESTADOS else 9,p['prova_id'])):
    pid=p['prova_id']; ne=n(B.P('extraidos',pid+'.jsonl')); nesc=n(B.PC('escopo',pid+'.jsonl')); ncl=n(B.PC('classificacoes',pid+'.jsonl'))
    v=p.get('verificacao'); vt=('%s%% / %s%% / %s%% (n=%s) %s'%(v['edital'],v['nucleo'],v['tags'],v['n'],'✔' if v['aprovada'] else '✖')) if v else '—'
    h=p.get('historico') or []; nota=(h[-1].get('nota') or '')[:60] if h else ''
    linhas.append('<tr><td>%s</td><td><span class=chip style="background:%s">%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class=nt>%s</td></tr>'%(e(pid),COR.get(p['estado'],'#999'),p['estado'],ne,nesc,ncl,e(vt),e(nota)))
# ---------- exemplo real (pega 1 item do escopo de prova qualquer, mostra enunciado -> compat -> classificação -> banco)
ex=None
for p in prov:
    for i in B.lerj(B.PC('escopo',p['prova_id']+'.jsonl')):
        ex=(p['prova_id'],i); break
    if ex: break
exemplo=''
if ex:
    pid,i=ex; c={str(x['item']):x for x in B.lerj(B.PC('classificacoes',pid+'.jsonl'))}.get(str(i['item']))
    exemplo='<div class=ex><b>Exemplo real</b> — %s, item %s (gabarito %s)<br><i>enunciado:</i> %s<br><i>etapa 1 (compatibilidade):</i> <code>%s</code><br><i>etapa 4 (classificação):</i> <code>%s</code></div>'%(e(pid),i['item'],i.get('gabarito'),e(i['enunciado'][:260]),e(json.dumps(i['compat'],ensure_ascii=False)),e(json.dumps({k:c.get(k) for k in ('edital','nucleo_id','tags','nivel')},ensure_ascii=False)) if c else 'ainda não classificado')
# ---------- etapas (entrada -> saída -> gate)
ET=[('1','Descoberta','catálogo da API Cebraspe + programa.json + lexico.json','provas/ID/ (PDF) e escopo/ID.jsonl (itens compatíveis)','pares prova+gabarito; item compatível sempre preservado','%d provas varridas · %d itens vistos · %d compatíveis (%d%%) · %d duplicatas'%(len(var),vistos,compat,pct(compat,vistos),len(dups))),
    ('2','Baixada','URLs do CDN','prova.pdf + gabarito.pdf com hash','os dois são PDFs válidos','%d provas com PDF íntegro'%sum(1 for p in prov if B.hashes_pasta(p['prova_id']))),
    ('3','Extraída','prova.pdf + gabarito.pdf','extraidos/ID.jsonl (item, contexto, enunciado, gabarito)','nº de itens = nº do gabarito; enunciado ≥25 caracteres','%d provas · vazios: %d'%(len(prov),sum(1 for p in prov for i in B.lerj(B.P('extraidos',p['prova_id']+'.jsonl')) if len(i['enunciado'])<25))),
    ('4','Classificada','pacotes/ID.md (itens + 3 códigos candidatos)','classificacoes/ID.jsonl (edital, núcleo, tags, nível)','cobre exatamente o escopo; códigos e tags válidos','%d itens classificados · %d FORA (%d%%)'%(classif,fora,pct(fora,classif))),
    ('5','Verificada','pacote sem as respostas do classificador','verificacoes/ID.jsonl → comparar','edital ≥90% · núcleo ≥80% · pegadinha ≥80%','%d provas verificadas · %d aprovadas'%(len(verif),sum(1 for p in verif if p['verificacao']['aprovada']))),
    ('6','Persistida','classificação aprovada','banco.jsonl + nucleos.jsonl','sem duplicata (url+item ou texto igual)','%d itens no banco · %d núcleos'%(len(banco),n(B.NUC))),
    ('7','Priorização','banco.jsonl','rank: núcleos ENSINAR, cobertura Good-Turing, lacunas','cobertura ≥70% para liberar a aula','ver cobertura por tema abaixo'),
    ('8','Material de estudo','núcleos priorizados do tema','aula PDF dark + caderno (≤10 questões reais)','questão real + URL','(não executada)')]
etapas=''.join('<div class=et><div class=en>%s</div><div><b>%s</b><br><small>ENTRA: %s<br>SAI: %s<br>GATE: %s</small><div class=ct>%s</div></div></div>'%x for x in ET)
# ---------- cobertura por seção do edital (banco x escopo pendente)
bc=collections.Counter(); pc=collections.Counter()
def sec(c): m=re.match(r'(P\d·\w+ \d+)',c or ''); return m.group(1) if m else (c or '?')
for d in banco: bc[sec(d.get('edital'))]+=1
for p in prov:
    if p['estado']!='persistida':
        for i in B.lerj(B.PC('escopo',p['prova_id']+'.jsonl')): pc[sec(i['compat']['edital_prov'])]+=1
tit={d['codigo']:d['texto'] for d in prog}; secs=sorted(set(bc)|set(pc),key=lambda k:-(bc[k]+pc[k]))[:12]
cob=''.join('<tr><td>%s</td><td>%s</td><td><div class=fb><i class=g style="width:%d%%"></i><i class=y style="width:%d%%"></i></div></td><td>%d</td><td>%d</td></tr>'%(e(k),e(tit.get(k,'')[:50]),min(100,bc[k]*5),min(100-min(100,bc[k]*5),pc[k]*5),bc[k],pc[k]) for k in secs)
log=''
try: log=e(''.join(open(B.P('logs','execucao.log'),encoding='utf-8-sig').readlines()[-22:]))
except OSError: pass
agora=datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
doc='''<!doctype html><html lang=pt-br><head><meta charset=utf-8><meta http-equiv=refresh content=5><title>Painel CGU-BD</title><style>
body{background:#0f1117;color:#e5e7eb;font:14px/1.45 Segoe UI,system-ui,sans-serif;margin:0;padding:22px 28px}h1{margin:0 0 4px;font-size:22px}h2{margin:26px 0 10px;font-size:16px;color:#93c5fd;border-bottom:1px solid #263041;padding-bottom:4px}
.sub{color:#9ca3af;font-size:12px}.fr{display:flex;align-items:center;gap:10px;margin:3px 0}.fl{width:280px;color:#cbd5e1}.fb{flex:1;background:#1b2130;border-radius:4px;height:14px;display:flex;overflow:hidden}.fb i{background:#3b82f6;display:block}.fb i.g{background:#22c55e}.fb i.y{background:#fbbf24}.fr b{width:70px;text-align:right}
table{border-collapse:collapse;width:100%%;font-size:13px}th{text-align:left;color:#9ca3af;font-weight:600;border-bottom:1px solid #263041;padding:5px 8px}td{padding:5px 8px;border-bottom:1px solid #1b2130}.nt{color:#9ca3af}
.chip{padding:2px 8px;border-radius:10px;color:#0b0d12;font-weight:600;font-size:12px}.et{display:flex;gap:12px;background:#151a26;border:1px solid #232c3d;border-radius:8px;padding:10px 12px;margin:6px 0}.en{font-size:22px;font-weight:700;color:#60a5fa;width:26px}
.et small{color:#9ca3af}.ct{margin-top:4px;color:#86efac;font-weight:600}.ex{background:#151a26;border-left:3px solid #60a5fa;padding:10px 14px;margin:10px 0;border-radius:4px}code{color:#fcd34d;font-size:12px}
pre{background:#0b0d12;border:1px solid #232c3d;border-radius:6px;padding:10px;color:#a7f3d0;font-size:12px;overflow:auto}.leg span{margin-right:14px}
</style></head><body><h1>Painel do workflow CGU-BD</h1><div class=sub>Concurso: %s · atualizado %s · esta página se recarrega a cada 5 s</div>
<h2>Funil (o que entra e o que sobra em cada passo)</h2>%s
<h2>Etapas: entrada → saída → gate → situação real</h2>%s%s
<h2>Provas e estado</h2><table><tr><th>prova</th><th>estado</th><th>extraídos</th><th>escopo</th><th>classif.</th><th>verificação (edital/núcleo/pegadinha)</th><th>última nota</th></tr>%s</table>
<h2>Cobertura por seção do edital</h2><div class=leg><span style="color:#22c55e">■ já no banco</span><span style="color:#fbbf24">■ pendente no escopo</span></div><table><tr><th>seção</th><th>tema</th><th>progresso</th><th>banco</th><th>pendente</th></tr>%s</table>
<h2>Últimas linhas do log</h2><pre>%s</pre></body></html>'''%(e(os.path.basename(B.CONC)),agora,funil,etapas,exemplo,''.join(linhas),cob,log)
out=B.P('painel.html'); open(out,'w',encoding='utf-8').write(doc); print('painel:',out)
