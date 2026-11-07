"""Biblioteca de componentes visuais para aulas (SVG inline, dark). Importe em figuras.py da aula.
Regras de uso estão em aulas/_template/MODELO-AULA-VISUAL.md. Todas as figuras são ORIGINAIS (nada copiado da web)."""
import html
C={'azul':'#58a6ff','verde':'#3fb950','ambar':'#d29922','verm':'#f85149','roxo':'#a371f7','cinza':'#8b949e','fundo':'#161b22','fundo2':'#0d1117','linha':'#30363d','texto':'#e6edf3'}
def esc(s): return html.escape(str(s),quote=False)
def wrap(s,w,size):
    mx=max(4,int(w/(0.60*size)));out=[];cur=''
    for p in str(s).split():
        if cur and len(cur)+1+len(p)>mx: out.append(cur);cur=p
        else: cur=(cur+' '+p).strip()
    if cur: out.append(cur)
    return out
def svg(w,h,body):
    return ('<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg"><defs>'
     '<marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#8b949e"/></marker>'
     '<marker id="arb" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#58a6ff"/></marker></defs>%s</svg>'%(w,h,body))
def txt(x,y,s,c='#e6edf3',size=11,anchor='start',bold=False):
    return '<text x="%s" y="%s" fill="%s" font-size="%s" text-anchor="%s"%s>%s</text>'%(x,y,c,size,anchor,' font-weight="bold"' if bold else '',esc(s))
def lines(x,y,s,w,c='#8b949e',size=10,anchor='start',lh=None,bold=False):
    lh=lh or size+3;o=[]
    for i,l in enumerate(wrap(s,w,size)): o.append(txt(x,y+i*lh,l,c,size,anchor,bold))
    return ''.join(o)
def box(x,y,w,h,titulo,sub=None,c='#58a6ff',fill='#161b22',ts=12,ss=9.5):
    o='<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="%s" stroke="%s"/>'%(x,y,w,h,fill,c)
    tl=wrap(titulo,w-10,ts);ty=y+(ts+6 if not sub else ts+5)
    for i,l in enumerate(tl): o+=txt(x+w/2,ty+i*(ts+2),l,c,ts,'middle',True)
    if sub: o+=lines(x+w/2,ty+len(tl)*(ts+2)+1,sub,w-12,'#8b949e',ss,'middle')
    return o
def seta(x1,y1,x2,y2,c='#8b949e',tracejado=False,azul=False):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.6"%s marker-end="url(#%s)"/>'%(x1,y1,x2,y2,c,' stroke-dasharray="5 4"' if tracejado else '','arb' if azul else 'ar')
def losango(cx,cy,w,h,s,c='#d29922',size=10):
    o='<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="#161b22" stroke="%s"/>'%(cx,cy-h/2,cx+w/2,cy,cx,cy+h/2,cx-w/2,cy,c)
    L=wrap(s,w*0.62,size);y0=cy-(len(L)-1)*(size+2)/2+size/3
    for i,l in enumerate(L): o+=txt(cx,y0+i*(size+2),l,c,size,'middle',True)
    return o
def chip(x,y,w,h,s,c='#58a6ff',size=10):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s22" stroke="%s"/>'%(x,y,w,h,h/2,c,c)+txt(x+w/2,y+h/2+size/3,s,c,size,'middle',True)
def fig(svg_str,legenda,titulo=None):
    t='<div style="font-size:9.5pt;color:#8b949e;margin:3mm 0 1mm">🖼 <b>%s</b></div>'%esc(titulo) if titulo else ''
    return '<div style="break-inside:avoid;margin:3mm 0;background:#0d1117;border:1px solid #30363d;border-radius:2mm;padding:2mm 3mm">%s%s<div class="cap">%s</div></div>'%(t,svg_str,esc(legenda))
