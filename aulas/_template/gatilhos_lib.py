"""Palavras-gatilho coloridas (verde=correta, vermelho=errada, amarelo=cuidado). Biblioteca para qualquer aula.
Uso por aula:
  1) python3 -c "import sys;sys.path.insert(0,'../../_template');import gatilhos_lib as g;g.listar('corpo.html')"   -> lista numerada (para classificar)
  2) g.gerar('corpo.html','gatilhos.json',G=[...],R=[...],A=[...])   -> grava as regras (pre+palavra+post)
  3) blocos.py chama gatilhos.aplicar(s) (wrapper da aula) a cada geracao. Idempotente. Nunca colorir o caderno (o aluno decide sozinho)."""
import re,json
from pathlib import Path
TIT={'v':'Palavra-gatilho, mas aqui a afirmação está CERTA','r':'Palavra-gatilho em afirmação ERRADA','a':'Cuidado: vale em regra, mas há exceção ou condição'}
W=r'\b(pode|podem|poderá|poderão|deve|devem|deverá|exclusivamente|exclusiv[ao]s?|apenas|somente|sempre|nunca|jamais|qualquer|quaisquer|todos|todas|toda|todo|nenhum|nenhuma|necessariamente|obrigatoriamente|unicamente|só)\b'
def _ocorrencias(s):
    s2=re.sub(r'<svg.*?</svg>',lambda m:' '*len(m.group(0)),s,flags=re.S)
    return s2,list(re.finditer(W,s2,flags=re.I))
def listar(corpo,saida='/tmp/gatilhos_lista.txt'):
    s=Path(corpo).read_text(encoding='utf-8');assert not re.search(r'<mark class="g',s),'rode listar/gerar em corpo sem cores (desfaça antes)'
    s2,ms=_ocorrencias(s);out=[]
    for i,m in enumerate(ms):
        a=max(0,m.start()-70);b=min(len(s2),m.end()+70)
        out.append('%d|%s'%(i,re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',s2[a:m.start()])+'[['+m.group(1)+']]'+re.sub(r'<[^>]+>','',s2[m.end():b]))))
    Path(saida).write_text('\n'.join(out),encoding='utf-8');print(len(out),'ocorrencias em',saida)
def gerar(corpo,saida,G=(),R=(),A=()):
    s=Path(corpo).read_text(encoding='utf-8');s2,ms=_ocorrencias(s);rules=[];av=[]
    for cls,L in (('v',G),('r',R),('a',A)):
        for i in L:
            m=ms[i];a,b=m.start(),m.end();ok=False
            for n in (22,40,60,90,140):
                pre=s[max(0,a-n):a];post=s[b:b+n]
                if s.count(pre+m.group(0)+post)==1: ok=True;break
            if not ok: av.append(i)
            rules.append({'i':i,'cls':cls,'pre':pre,'w':m.group(0),'post':post})
    Path(saida).write_text(json.dumps(rules,ensure_ascii=False,indent=0),encoding='utf-8');print(len(rules),'regras; sem ancora unica:',av)
def legenda():
    return ('<!--GAT:legenda--><div class="ped ped-prev"><b class="t">🎨 Cores das palavras-gatilho</b>'
     '<p>Palavras como <i>deve, pode, apenas, só, exclusivamente, sempre, nunca</i> são as favoritas da banca. Elas não condenam nem salvam o item sozinhas, por isso a aula as destaca:</p>'
     '<p><mark class="gv" title="%s">verde</mark> a palavra forte aparece e a afirmação está <b>Certa</b> (ex.: "Deve indicar os recursos necessários, admitidos <mark class="gv">apenas</mark> os provenientes de anulação de despesa");</p>'
     '<p><mark class="gr" title="%s">vermelho</mark> a palavra aparece em afirmação <b>Errada</b> (ex.: "o orçamento é <mark class="gr">exclusivamente</mark> autorizativo");</p>'
     '<p><mark class="ga" title="%s">amarelo</mark> <b>cuidado</b>: vale em regra, mas há exceção ou condição (ex.: "a LOA é <mark class="ga">só</mark> para prever receita e fixar despesa", com duas exceções).</p>'
     '<p class="dica">No caderno de questões nada é colorido, para você decidir sozinho. Depois do envio, o gabarito comentado traz as cores.</p></div><!--/GAT:legenda-->\n')%(TIT['v'],TIT['r'],TIT['a'])
def aplicar(s,D,antes=r'<h2>2\. '):
    s=re.sub(r'<!--GAT:legenda-->.*?<!--/GAT:legenda-->\n?','',s,flags=re.S)
    s=re.sub(r'<mark class="g[vra]"[^>]*>(.*?)</mark>',r'\1',s)
    rules=json.loads((Path(D)/'gatilhos.json').read_text(encoding='utf-8'));pos=[];falhas=[]
    for r in rules:
        alvo=r['pre']+r['w']+r['post'];n=s.count(alvo)
        if n!=1: falhas.append((r['i'],n));continue
        pos.append((s.index(alvo)+len(r['pre']),r))
    for p,r in sorted(pos,key=lambda x:-x[0]):
        w=r['w'];s=s[:p]+'<mark class="g%s" title="%s">%s</mark>'%(r['cls'],TIT[r['cls']],w)+s[p+len(w):]
    m=re.search(antes,s);s=s[:m.start()]+legenda()+s[m.start():]
    print('gatilhos marcados:',len(pos),'falhas:',falhas)
    return s
