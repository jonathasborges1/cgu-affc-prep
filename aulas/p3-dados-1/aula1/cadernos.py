import json
from html import escape as e
from pathlib import Path
D=Path(__file__).resolve().parent
css=(D.parents[1]/'_template'/'dark.css').read_text(encoding='utf-8')
R=json.loads((D/'restantes.json').read_text(encoding='utf-8'))
CAD={'2':('Caderno 2 · Modelagem relacional: chaves, integridade, normalização',[0,5,10,22,28,30,34,36,46,60]),
 '3':('Caderno 3 · Transações, concorrência e procedures',[31,33,37,40,13,25,27,23,38,21]),
 '4':('Caderno 4 · SGBD, independência de dados, NoSQL e distribuídos',[11,49,16,35,48,51,54,58,56,41])}
def limpa(t):
    for m in (' OS ESPECÍFICOS',' Com pertinência'):
        t=t.split(m)[0]
    return t.strip()
EXTRA={60:'Correto: para chegar à 1FN, elimina-se o que é aninhado ou multivalorado, deixando cada célula com valor atômico.',54:'Correto: o modelo documental estende o chave-valor porque guarda documentos inteiros, agrupados em coleções, e permite consultar pelo conteúdo.',58:'Correto: NoSQL como o MongoDB lida bem com grande volume de dados não estruturados e escala na horizontal; SQL (MySQL) é mais adequado a dados estruturados e transações ACID.',41:'Correto: transparência de distribuição, o cliente não sabe em qual servidor o dado está.',0:'Correto: restrições como integridade referencial e chaves são características do modelo relacional e evitam repetição e perda de informação.'}
nv=lambda x:{'facil':'Fácil','fácil':'Fácil','medio':'Médio','médio':'Médio','dificil':'Difícil','difícil':'Difícil'}.get(str(x.get('nivel')).lower(),x.get('nivel'))
for k,(tit,ids) in CAD.items():
    h='<div class="pg"><div class="small">P3 · Dados 1 · Aula 1 · prática</div><h1>%s</h1><p class="small">10 itens reais do Cebraspe. Julgue Certo ou Errado antes de ver o gabarito (errar desconta o mesmo que acertar: só marque com confiança).</p>'%e(tit)
    g='</div><div class="pg"><h2>Gabarito comentado</h2>'
    for n,i in enumerate(ids,1):
        x=R[i]
        h+='<div class="box"><b class="t">Questão %d</b><p>%s</p><p>%s<span class="tag">P3 · Dados 1</span><span class="tag">%s</span></p><p class="small">%s · item %s · <a href="%s">fonte oficial</a></p></div>'%(n,e(limpa(x['enunciado'])),''.join('<span class="tag">%s</span>'%e(t) for t in (x.get('tags') or [])[:2]),e(str(nv(x))),e(x['ref']),e(str(x['item'])),e(x['url']))
        c=EXTRA.get(i) or x.get('comentario') or x.get('padrao') or ''
        g+='<div class="box %s"><b class="t">Questão %d: %s</b><p>%s</p></div>'%('ok' if x['gabarito']=='C' else 'warn',n,'CERTO' if x['gabarito']=='C' else 'ERRADO',e(c))
    (D/('caderno%s.html'%k)).write_text('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>%s</style></head><body>%s%s</div></body></html>'%(css,h,g),encoding='utf-8')
print('ok')
