#!/usr/bin/env python3
"""Cria lotes por tema (extraidos/tema-p2-<assunto>-<n>.jsonl) com os itens que a leitura estrita marcou como P2.
  lote_p2_positivos.py "P2·GOV 2" [--tam 25]   (lotes 'extraida'; classificar -> verificar -> aplicar)"""
import sys,json,argparse,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); sys.path.insert(0,str(Path(__file__).parent.parent))
import descobrir as D
B=D.B
ap=argparse.ArgumentParser();ap.add_argument('codigo');ap.add_argument('--tam',type=int,default=25);a=ap.parse_args()
d=B.__dict__.get('ROOT') or Path(__file__).parent.parent
J=lambda n:json.load(open(Path(d)/'tmp/p2ml'/n,encoding='utf-8'))
V2=J('lote/v2_labels.json');E=J('lote/rotulos_extra.json');Dt=J('data.json');R=J('round1.json');S=J('census.json');lc=J('lab_census.json');lg=J('lab_gate.json');lu=J('lab_unc.json')
Y=lambda k,y:V2.get(k,y)
rows=[(x,Y(x['k'],x['y'])) for x in Dt['P2']+Dt['DES']]+[(x,Y(x['k'],lg[str(i)])) for i,x in enumerate(R['gate'],1)]+[(x,Y(x['k'],lu[str(i)])) for i,x in enumerate(R['unc'],1)]+[(x,Y(x['k'],lc[str(i)])) for i,x in enumerate(S,1)]
pos={}
for x,y in rows:
    if y==a.codigo:pos[x['k']]=x
for e in E:
    if e['y']==a.codigo and e['k'] not in pos:pos[e['k']]=e
ja={(l.get('prova_origem'),str(l.get('item_orig'))) for f in Path(d,'extraidos').glob('tema-p2-*.jsonl') for l in map(json.loads,open(f,encoding='utf-8'))}
itens=[]
for k in pos:
    pid,it=k.rsplit('#',1)
    if (pid,it) in ja:continue
    ex={str(x['item']):x for x in B.lerj(B.P('extraidos',pid+'.jsonl'))}.get(it)
    if not ex or ex.get('gabarito') not in('C','E'):continue
    itens.append((pid,it,ex))
slug=re.sub(r'[^a-z0-9]+','-',a.codigo.lower().replace('p2·','')).strip('-')
n=0
for b in range(0,len(itens),a.tam):
    n+=1;pid_lote='tema-p2-%s-%d'%(slug,n);ch=itens[b:b+a.tam];js=[]
    for m,(pid,it,ex) in enumerate(ch,1):
        j=dict(ex);j.update({'item_orig':it,'prova_origem':pid,'item':str(m)});js.append(j)
    B.escj(B.P('extraidos',pid_lote+'.jsonl'),js)
    pr={'prova_id':pid_lote,'ref':'Lote P2 positivos %s (%d itens de %d provas)'%(a.codigo,len(js),len({j['prova_origem'] for j in js})),'url':'lote','url_gab':'lote','ano':2024,'orgao':'varias','cargo':a.codigo,'peso':1.0,'hash':None,'n_itens':len(js),'n_gab':len(js),'verificacao':None,'historico':[]}
    for e in('descoberta','baixada','extraida'):B.hist(pr,e,'lote de positivos P2 (leitura estrita)')
    B.prova_put(pr);print(pid_lote,len(js))
print(a.codigo,'positivos com gabarito:',len(itens),'de',len(pos))
