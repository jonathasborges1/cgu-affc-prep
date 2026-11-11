#!/usr/bin/env python3
"""Converte o texto OCR de um caderno impresso do TEC (PDF salvo pelo usuário) em itens (uma prova-lote por 25 itens).
  tec_pdf_para_itens.py <pasta_ocr> --prefixo tec-p2-aud --tema "P2·AUD" [--tam 25]
Só texto de arquivo local já baixado pelo usuário; não acessa o site."""
import re,sys,json,glob,argparse,unicodedata
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); sys.path.insert(0,str(Path(__file__).parent.parent))
import descobrir as D
B=D.B
ap=argparse.ArgumentParser();ap.add_argument('pasta');ap.add_argument('--prefixo',required=True);ap.add_argument('--tema',required=True);ap.add_argument('--tam',type=int,default=25);ap.add_argument('--seco',action='store_true');a=ap.parse_args()
def _limpa(t):
    # remove cabeçalho/rodapé de página (a questão pode atravessar a quebra de página)
    return '\n'.join(l for l in t.split('\n') if not re.match(r'^\s*\d{2}/\d{2}/\d{4}, \d{2}:\d{2}\s+Caderno',l) and 'cadernos/' not in l and not re.search(r'imprimir\s+\d+/\d+\s*$',l))
txt='\n'.join(_limpa(open(f,encoding='utf-8').read()) for f in sorted(glob.glob(a.pasta+'/p-*.txt')))
# gabarito: bloco final "N) Certo/Errado/Anulada"
i=txt.rfind('1) ');gab={}
for n,g in re.findall(r'(\d+)\)\s*(Certo|Errado|Anulada)',txt[txt.find('Gabarito') if 'Gabarito' in txt else 0:]): gab[int(n)]={'Certo':'C','Errado':'E','Anulada':'ANUL'}[g]
# se o rótulo "Gabarito" não existir, usa o último trecho com ≥150 pares
pares=re.findall(r'(\d+)\)\s*(Certo|Errado|Anulada)',txt)
if len(gab)<150:
    gab={};ult=pares[-200:] if len(pares)>=200 else pares
    for n,g in ult: gab[int(n)]={'Certo':'C','Errado':'E','Anulada':'ANUL'}[g]
# itens: começam em uma linha com url tecconcursos .../questoes/<id>
blocos=re.split(r'\n[^\n]*?tecconcursos\.com\.br/questoes/\s*(\d+)[^\n]*\n',txt)
itens=[]
for k in range(1,len(blocos),2):
    qid=blocos[k];corpo=blocos[k+1]
    corpo=re.split(r'\n\s*Certo\s*\n\s*Errado',corpo)[0]
    linhas=[l.strip() for l in corpo.split('\n') if l.strip()]
    if len(linhas)<3:continue
    ref=linhas[0];assunto=linhas[1];resto=' '.join(linhas[2:])
    m=re.match(r'(\d+)\)\s*(.*)',resto,re.S)
    if not m:continue
    num=int(m.group(1));enun=re.sub(r'\s+',' ',m.group(2)).strip()
    mm=re.match(r'(.+?)\s*\((.+?)\)\s*-\s*(.+?)/(\d{4})\s*$',ref)
    banca=mm.group(1) if mm else ref;ano=int(mm.group(4)) if mm else None
    itens.append({'num':num,'qid':qid,'ref':ref,'assunto':assunto,'enunciado':enun,'banca':banca,'ano':ano,'cargo':mm.group(3) if mm else None,'orgao':mm.group(2) if mm else None})
print('itens lidos',len(itens),'gabaritos',len(gab),'anuladas',sum(1 for v in gab.values() if v=='ANUL'))
nums=[x['num'] for x in itens];print('numeração ok' if nums==sorted(nums) and len(set(nums))==len(nums) else 'ATENÇÃO numeração',min(nums),max(nums),'faltam',[n for n in range(1,201) if n not in set(nums)][:30])
norm=lambda s:re.sub(r'\W+','',unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode())
have={norm(d.get('enunciado') or '')[:160] for d in B.rows()}
for f in glob.glob(str(B.P('extraidos','*.jsonl'))):
    for l in open(f,encoding='utf-8'):
        try:have.add(norm(json.loads(l).get('enunciado') or '')[:160])
        except Exception:pass
ok=[];dup=0;anul=0;sem=0
for x in itens:
    g=gab.get(x['num'])
    if g is None:sem+=1;continue
    if g=='ANUL':anul+=1;continue
    if norm(x['enunciado'])[:160] in have:dup+=1;continue
    x['gabarito']=g;ok.append(x)
print('novos',len(ok),'duplicados',dup,'anuladas',anul,'sem gabarito',sem)
ok.sort(key=lambda x:(x['assunto'],x['num']))   # lotes por assunto, para núcleos consistentes
if a.seco:sys.exit()
n=0
for b in range(0,len(ok),a.tam):
    n+=1;pid='%s-%d'%(a.prefixo,n);js=[]
    for m,x in enumerate(ok[b:b+a.tam],1):
        js.append({'prova_id':pid,'banca':x['banca'].replace('CEBRASPE (CESPE)','Cebraspe') if x['banca'].startswith('CEBRASPE') else x['banca'],'orgao':x['orgao'],'cargo':x['cargo'],'ano':x['ano'],'ref':'%s · TEC Concursos questão %s'%(x['ref'],x['qid']),'url':'https://www.tecconcursos.com.br/questoes/'+x['qid'],'url_gab':'https://www.tecconcursos.com.br/questoes/'+x['qid'],'item':str(m),'item_orig':str(x['num']),'prova_origem':'tec-'+x['qid'],'enunciado':x['enunciado'],'gabarito':x['gabarito'],'assunto_tec':x['assunto'],'fonte':'tec-caderno-impresso'})
    B.escj(B.P('extraidos',pid+'.jsonl'),js)
    pr={'prova_id':pid,'ref':'Lote %s (%d itens do caderno impresso do TEC)'%(a.tema,len(js)),'url':'lote','url_gab':'lote','ano':2025,'orgao':'varias','cargo':a.tema,'peso':1.0,'hash':None,'n_itens':len(js),'n_gab':len(js),'verificacao':None,'historico':[]}
    for e in('descoberta','baixada','extraida'):B.hist(pr,e,'caderno impresso TEC (OCR local)')
    B.prova_put(pr);print(pid,len(js))
