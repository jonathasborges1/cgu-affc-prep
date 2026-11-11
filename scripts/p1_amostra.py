#!/usr/bin/env python3
"""Amostra CEGA para medir o acerto da triagem em P1: n itens fortes por assunto (aleatorio com semente), sem mostrar ao classificador o codigo da triagem.
  p1_amostra.py [--n 30] [--seed 11] [--lote 50] [--prefixo p1-verif] [--rodada 1] [--bloco P1]
Gera pacotes/<prefixo>-<rodada>-<k>.md (para o agente) e amostras/<prefixo>-<rodada>-mapa.jsonl (gabarito da triagem, NAO mostrar ao agente).
Itens ja amostrados em rodadas anteriores sao excluidos."""
import sys,json,random,argparse,glob,os,re,collections
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); C=os.path.join(D,'concursos','cgu-affc-ti-ds')
def lj(f): return [json.loads(l) for l in open(f,encoding='utf-8') if l.strip()] if os.path.exists(f) else []
ap=argparse.ArgumentParser(); ap.add_argument('--n',type=int,default=30); ap.add_argument('--seed',type=int,default=11); ap.add_argument('--lote',type=int,default=50)
ap.add_argument('--prefixo',default='p1-verif'); ap.add_argument('--rodada',type=int,default=1); ap.add_argument('--bloco',default='P1'); ap.add_argument('--so',default='')
a=ap.parse_args()
prog=lj(os.path.join(C,'programa.json')); nm={}
for x in prog:
    m=re.match(r'(%s·\w+ \d+)(\.\d+)?'%a.bloco,x['codigo'])
    if m: nm.setdefault(m.group(1),[]).append((x['codigo'],x['texto']))
dup={x['prova_id']+'#'+str(x['item']) for x in lj(os.path.join(C,'descoberta','duplicatas.jsonl'))}
var={v['prova_id'] for v in lj(os.path.join(C,'descoberta','varredura.jsonl')) if 'n_itens' in v}
ja=set()
for f in glob.glob(os.path.join(C,'amostras',a.prefixo+'-*-mapa.jsonl')):
    for r in lj(f): ja.add(r['prova_id']+'#'+str(r['item']))
vis=set(); pool=collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(C,'escopo','*.jsonl'))):
    if os.path.basename(f).startswith('tema-'): continue
    for e in lj(f):
        c=e.get('compat') or {}; k=e['prova_id']+'#'+str(e['item'])
        if k in dup or k in vis or e['prova_id'] not in var or c.get('nivel')!='forte': continue
        m=re.match(r'(%s·\w+ \d+)'%a.bloco,c.get('edital_prov') or '')
        if not m: continue
        vis.add(k)
        if k not in ja: pool[m.group(1)].append(e)
rnd=random.Random(a.seed*100+a.rodada); sel=[]
for ass,L in pool.items():
    if a.so and ass not in a.so.split(','): continue
    por=collections.defaultdict(list)
    for e in L: por[e['prova_id']].append(e)
    for v in por.values(): rnd.shuffle(v)
    provas=list(por); rnd.shuffle(provas); out=[]; r=0
    while len(out)<a.n and any(len(por[p])>r for p in provas):
        for p in provas:
            if len(por[p])>r and len(out)<a.n: out.append(por[p][r])
        r+=1
    sel+=[(ass,e) for e in out]
rnd.shuffle(sel)
os.makedirs(os.path.join(C,'amostras'),exist_ok=True); os.makedirs(os.path.join(C,'pacotes'),exist_ok=True)
mapa=[]; blocos=[sel[i:i+a.lote] for i in range(0,len(sel),a.lote)]
cod=['## CÓDIGOS (escolha UM por item; dentro de cada assunto estão os subitens do edital)']
for ass in sorted(nm,key=lambda s:(s.split(' ')[0],int(s.split(' ')[-1]))):
    cod.append('- **%s**: %s'%(ass,' | '.join('%s %s'%(c.split(' ')[-1],t[:170]) for c,t in nm[ass])))
for k,b in enumerate(blocos,1):
    out=['# PACOTE %s-%d-%d (%d itens): pertinência ao edital de %s'%(a.prefixo,a.rodada,k,len(b),a.bloco),'',
         'Tarefa: para cada item, diga a QUAL assunto do edital abaixo ele pertence (ou OUTRO se nenhum conteúdo listado no edital de %s trata do tema; pertencer a Português, TI, Direito de outra área, medicina, engenharia etc. é OUTRO).'%a.bloco,
         'Relevância: alta = o item cobra exatamente o conteúdo listado; media = vizinho/parcial; baixa = só tangencia; fora = não trata.','']+cod+['','## ITENS']
    for j,(ass,e) in enumerate(b,1):
        iid='v%d-%d-%02d'%(a.rodada,k,j); mapa.append({'id':iid,'prova_id':e['prova_id'],'item':e['item'],'triagem':ass,'edital_prov':e['compat']['edital_prov'],'score':e['compat']['score'],'gabarito':e.get('gabarito'),'pacote':'%s-%d-%d'%(a.prefixo,a.rodada,k)})
        ctx=(' [texto-base: '+e['contexto'][:160].replace('\n',' ')+']') if len(e.get('contexto',''))>150 else ''
        out.append('### %s | gab=%s%s\n%s'%(iid,e.get('gabarito'),ctx,re.sub(r'\s+',' ',e['enunciado'])[:480]))
    open(os.path.join(C,'pacotes','%s-%d-%d.md'%(a.prefixo,a.rodada,k)),'w',encoding='utf-8').write('\n'.join(out))
open(os.path.join(C,'amostras','%s-%d-mapa.jsonl'%(a.prefixo,a.rodada)),'w',encoding='utf-8').write(''.join(json.dumps(m,ensure_ascii=False)+'\n' for m in mapa))
cnt=collections.Counter(m['triagem'] for m in mapa); print(len(mapa),'itens em',len(blocos),'pacotes; por assunto:',dict(sorted(cnt.items())))
