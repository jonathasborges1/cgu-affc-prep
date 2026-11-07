#!/usr/bin/env python3
"""Insere (idempotente) as figuras originais da Aula 1 no corpo.html. Uso: python3 figuras.py"""
import re,sys
from pathlib import Path
D=Path(__file__).resolve().parent; sys.path.insert(0,str(D.parent.parent/'_template'))
from visuais import *

from pedagogia import checagem
def T_ciclo():
    return """<h3>Ciclo orçamentário × exercício financeiro: qual é a diferença?</h3>
<p><b>Resumo em uma linha:</b> o <b>exercício financeiro</b> é o <u>período de tempo</u> em que o orçamento vale (um ano); o <b>ciclo orçamentário</b> é o <u>caminho inteiro</u> do orçamento, do primeiro rascunho até a conferência das contas (mais de um ano).</p>
<div class="box"><b class="t">Analogia: o seu ano financeiro pessoal</b>Você vive o ano de 2027 de janeiro a dezembro, gastando e recebendo: esse é o <b>exercício</b> (o "ano valendo"). Mas o <b>ciclo</b> do seu 2027 começa antes, em dezembro de 2026, quando você planeja quanto vai gastar. E só termina em 2028, quando você confere as contas e faz a declaração do imposto de renda de 2027. Planejar, viver o ano e prestar contas acontecem em momentos diferentes. O ano vivido é uma parte do caminho todo.</div>
<p><b>Passo a passo com a LOA de 2027</b> (cada passo responde a uma pergunta que a prova faz):</p>
<table><tr><th>Passo</th><th>Pergunta</th><th>Resposta</th></tr>
<tr><td>1</td><td>Em que período a LOA de 2027 vale e é executada?</td><td>De 1º de janeiro a 31 de dezembro de 2027. Isso é o <b>exercício financeiro</b>; ele coincide com o ano civil (Lei 4.320/1964, art. 34).</td></tr>
<tr><td>2</td><td>Quando o projeto dessa LOA é feito e votado?</td><td><b>Em 2026</b>, um ano antes. O Executivo envia o projeto ao Congresso até 31 de agosto (4 meses antes do fim do exercício) e o Congresso o devolve para sanção até 22 de dezembro (ADCT, art. 35, §2º, III). A <b>elaboração e a aprovação</b> acontecem fora do exercício de 2027.</td></tr>
<tr><td>3</td><td>Quando se julgam as contas de 2027?</td><td><b>Em 2028</b>, depois que o exercício terminou. O controle acompanha a execução o tempo todo, mas a prestação e o julgamento das contas do exercício vêm depois.</td></tr>
<tr><td>4</td><td>Então qual é a duração de cada um?</td><td><b>Exercício:</b> 1 ano, de 1º/1 a 31/12. <b>Ciclo da LOA de 2027:</b> começa em 2026, passa por 2027 e termina em 2028, ou seja, toca três anos civis.</td></tr>
<tr><td>5</td><td>Dentro do exercício, o que pertence a ele?</td><td>As receitas nele <b>arrecadadas</b> e as despesas nele <b>legalmente empenhadas</b> (Lei 4.320, art. 35).</td></tr></table>
<p>Repare no passo 2 e no passo 3: a primeira e a última fase do ciclo estão <u>fora</u> do exercício. Só a <b>execução</b> está inteira dentro dele. Por isso são conceitos diferentes, e não sinônimos.</p>
<div style="break-inside:avoid"><table><tr><th></th><th>Exercício financeiro</th><th>Ciclo orçamentário</th></tr>
<tr><td>O que é</td><td>Período em que o orçamento é executado</td><td>Sequência das fases: elaborar, aprovar, executar, controlar e avaliar</td></tr>
<tr><td>Duração</td><td>1 ano (1º/1 a 31/12)</td><td>Mais de 1 ano (toca 3 anos civis)</td></tr>
<tr><td>Exemplo</td><td>Exercício de 2027</td><td>Ciclo da LOA de 2027 (2026 a 2028)</td></tr>
<tr><td>De onde vem</td><td>Lei 4.320, art. 34 (coincide com o ano civil)</td><td>Conceito da doutrina; as fases vêm de várias normas (CF arts. 165 a 169 e Lei 4.320)</td></tr></table></div>"""
def F_ciclo2():
    anos=[2025,2026,2027,2028,2029];x0=130;cw=100
    b=txt(320,14,'Três ciclos acontecendo ao mesmo tempo em 2027',C['texto'],12,'middle',True)
    for i,a in enumerate(anos):
        b+=txt(x0+i*cw+cw/2-3,40,str(a),C['texto'],11.5,'middle',True)
    rot=[('LOA 2026',2026),('LOA 2027',2027),('LOA 2028',2028)]
    fases=[('Elaborar','e aprovar',C['azul'],-1),('Executar','(orçamento vale)',C['verde'],0),('Controlar','e julgar contas',C['roxo'],1)]
    for r,(nome,ano) in enumerate(rot):
        y=52+r*58
        b+=txt(8,y+29,nome,C['texto'],11,'start',True)
        for t,s,c,d in fases:
            col=anos.index(ano+d)
            b+=box(x0+col*cw,y,cw-6,48,t,s,c,ts=10.5,ss=8.5)
    cx=x0+anos.index(2027)*cw
    b+='<rect x="%s" y="46" width="%s" height="180" rx="8" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 4"/>'%(cx-3,cw,C['ambar'])
    b+=txt(cx+cw/2-3,244,'exercício financeiro 2027',C['ambar'],10.5,'middle',True)
    b+=lines(320,266,'Em 2027 convivem três ciclos: o da LOA 2026 sendo julgado, o da LOA 2027 sendo executado e o da LOA 2028 sendo elaborado.',600,C['cinza'],10,'middle')
    return fig(svg(640,288,b),'A moldura tracejada é o exercício (um ano). Cada linha é um ciclo inteiro (três anos civis). Só a faixa verde de cada linha cabe dentro do exercício a que a LOA se refere.','Figura 2b · Exercício financeiro dentro do ciclo')
def C_ciclo():
    return checagem('Sem olhar o texto: o ciclo orçamentário da LOA de 2027 começa e termina em que anos? E o exercício financeiro dela?',
      'O ciclo vai de 2026 (elaboração e aprovação) a 2028 (julgamento das contas), passando pela execução em 2027. O exercício financeiro é só 2027, de 1º de janeiro a 31 de dezembro (Lei 4.320, art. 34).',
      'Por que "ciclo orçamentário" e "exercício financeiro" não são sinônimos?',
      'Porque o exercício é só o ano em que o orçamento é executado, enquanto o ciclo inclui também a elaboração e a aprovação (antes) e o controle e o julgamento das contas (depois), e por isso dura mais de um ano.',
      'Conte os anos: antes do exercício, durante e depois.','alta')

def F_tramitacao():
    b=txt(320,16,'Como o projeto de PPA, LDO ou LOA vira lei',C['texto'],12,'middle',True)
    xs=[5,135,265,395,525];w=110
    dados=[('1 Executivo','elabora o projeto',C['azul']),('2 Comissão Mista','(CMO) parecer e emendas',C['ambar']),('3 Congresso','Câmara e Senado votam em conjunto',C['ambar']),('4 Presidente','sanciona ou veta',C['azul']),('5 Lei','publicada e em vigor',C['verde'])]
    for x,(t,s,c) in zip(xs,dados): b+=box(x,30,w,70,t,s,c)
    for x in xs[:-1]: b+=seta(x+w+1,65,x+w+19,65)
    b+=lines(320,125,'Só o Executivo propõe PPA, LDO e LOA. O Legislativo discute, emenda (dentro dos limites do Bloco C) e aprova; nunca inicia a lei.',560,C['cinza'],10,'middle')
    return fig(svg(640,150,b),'Fluxo do projeto de lei orçamentária (CF arts. 165 e 166). Pegadinha: "o Legislativo tem a iniciativa" = Errado.','Figura 1 · Da proposta à lei')
def F_ciclo():
    b=txt(320,14,'As 4 fases do ciclo orçamentário',C['texto'],12,'middle',True)
    fases=[('Elaboração','Executivo monta a proposta',C['azul']),('Aprovação','Legislativo discute e vota',C['ambar']),('Execução','arrecadar e gastar o que a LOA autoriza',C['verde']),('Controle e avaliação','interno, externo, social',C['roxo'])]
    for i,(t,s,c) in enumerate(fases): b+=box(5+i*160,24,150,60,t,s,c)
    for i in range(3): b+=seta(156+i*160,52,164+i*160,52)
    b+=txt(20,108,'O controle acompanha TODO o ciclo, não só o final',C['roxo'],10,'start',True)
    b+='<line x1="20" y1="114" x2="620" y2="114" stroke="%s" stroke-width="3"/>'%C['roxo']
    segs=[(20,215,'Ano anterior','elaboração e aprovação',C['azul']),(215,425,'EXERCÍCIO FINANCEIRO','1º de janeiro a 31 de dezembro (execução)',C['verde']),(425,620,'Ano seguinte','prestação de contas e julgamento',C['roxo'])]
    for x1,x2,t,s,c in segs:
        b+='<rect x="%s" y="126" width="%s" height="56" fill="%s22" stroke="%s"/>'%(x1,x2-x1,c,c)
        b+=txt((x1+x2)/2,146,t,c,11,'middle',True)+lines((x1+x2)/2,160,s,x2-x1-10,C['cinza'],9.5,'middle')
    b+=txt(320,204,'ciclo orçamentário (mais amplo)  ⊃  exercício financeiro (só a fase de execução)',C['texto'],10.5,'middle',True)
    return fig(svg(640,216,b),'Pegadinha: tratar "ciclo orçamentário" e "exercício financeiro" como sinônimos é Errado. O exercício coincide com o ano civil (Lei 4.320, art. 34); o ciclo engloba planejar, aprovar, executar e controlar.','Figura 2 · Ciclo orçamentário × exercício financeiro')
def F_lrf():
    b=box(5,10,130,52,'Criar ou aumentar despesa',None,C['azul'])
    b+=box(160,10,230,52,'1 Estimar o impacto','no exercício em que entra em vigor e nos 2 seguintes (art. 16, I)',C['ambar'])
    b+=box(415,10,220,52,'2 Declaração do ordenador','cabe na LOA e é compatível com PPA e LDO (art. 16, II)',C['ambar'])
    b+=seta(136,36,158,36)+seta(391,36,413,36)
    b+=seta(525,63,525,92)
    b+=losango(525,128,230,72,'Dura mais de 2 exercícios? (art. 17)',C['roxo'],10.5)
    b+=seta(410,128,352,128)+txt(382,121,'NÃO',C['verde'],9.5,'middle',True)
    b+=box(160,102,190,52,'Despesa regular','com os passos 1 e 2',C['verde'])
    b+=seta(525,164,525,196)+txt(540,184,'SIM',C['verm'],9.5,'start',True)
    b+=box(395,190,240,88,'3 Despesa obrigatória continuada','provar que não afeta as metas fiscais E compensar com aumento permanente de receita ou redução permanente de despesa',C['roxo'])
    b+=seta(395,233,352,233)
    b+=box(160,208,190,52,'Despesa regular','se os 3 passos foram cumpridos',C['verde'])
    b+='<rect x="5" y="290" width="630" height="44" rx="8" fill="#f8514922" stroke="%s" stroke-dasharray="5 4"/>'%C['verm']
    b+=lines(320,309,'Faltou algum passo? A despesa é considerada NÃO AUTORIZADA, irregular e lesiva ao patrimônio público (art. 15). Venda de imóvel não compensa: a receita é pontual, não permanente.',600,C['verm'],10,'middle')
    return fig(svg(640,344,b),'Decisão do gestor antes de assumir despesa nova. Os números "2 exercícios seguintes" e "mais de 2 exercícios" são isca de DETALHE_NUMERICO.','Figura 3 · Fluxograma da regra da LRF (arts. 15 a 17)')
def F_creditos():
    cards=[('SUPLEMENTAR',C['verde'],'A dotação existe, mas é insuficiente (reforço)','Lei autorizativa; pode vir na própria LOA (exceção; ver Bloco H)','Indicar a fonte (art. 43)','Só no exercício em que foi aberto'),
           ('ESPECIAL',C['ambar'],'Não existe dotação específica (ex.: órgão novo)','Lei específica','Indicar a fonte (art. 43)','Pode ser reaberto se autorizado nos 4 últimos meses (CF 167 §2º)'),
           ('EXTRAORDINÁRIO',C['verm'],'Despesa urgente e imprevisível: guerra, comoção interna, calamidade','Medida provisória (União)','Sem indicação prévia exigida','Pode ser reaberto (CF 167 §2º)')]
    b=''
    rot=['QUANDO','INSTRUMENTO','RECURSOS','VIGÊNCIA']
    for i,(t,c,*vals) in enumerate(cards):
        x=5+i*213;w=205
        b+='<rect x="%s" y="6" width="%s" height="290" rx="8" fill="#161b22" stroke="%s"/><rect x="%s" y="6" width="%s" height="30" rx="8" fill="%s33"/>'%(x,w,c,x,w,c)
        b+=txt(x+w/2,26,t,c,12.5,'middle',True)
        for j,v in enumerate(vals):
            y=52+j*61
            b+=txt(x+10,y,rot[j],C['cinza'],8.5,'start',True)+lines(x+10,y+13,v,w-20,C['texto'],10)
            if j<3: b+='<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#30363d"/>'%(x+8,y+49,x+w-8,y+49)
    b+=txt(320,318,'Fontes para abrir suplementar e especial (Lei 4.320, art. 43)',C['texto'],10.5,'middle',True)
    for i,f in enumerate(['Superávit financeiro','Excesso de arrecadação','Anulação de dotações','Operações de crédito']):
        b+=chip(5+i*160,326,150,26,f,C['azul'],9.5)
    return fig(svg(640,360,b),'Truque de memória: SUPLEMENTAR reforça o que já existe; ESPECIAL cria linha nova; EXTRAORDINÁRIO é a emergência. A banca troca o nome do tipo (TROCA_TERMO).','Figura 4 · Os três créditos adicionais lado a lado')
def F_programa():
    b=txt(320,14,'Exemplo didático: da função à ação',C['texto'],12,'middle',True)
    b+=box(5,56,118,66,'Função 10','Saúde (maior agregação)',C['cinza'])+box(143,56,118,66,'Subfunção 301','Atenção básica',C['cinza'])
    b+=box(281,50,128,78,'PROGRAMA','"Saúde da família" (aparece no PPA e reaparece na LOA)',C['ambar'])
    b+=seta(124,89,141,89)+seta(262,89,279,89)
    acoes=[('Projeto','construir uma nova UBS (começo, meio e fim)',C['verde']),('Atividade','manter as UBS funcionando (contínua)',C['azul']),('Operação especial','pagar sentença judicial (não gera produto)',C['roxo'])]
    for i,(t,s,c) in enumerate(acoes):
        y=24+i*62;b+=box(445,y,190,52,t,s,c);b+=seta(410,89,443,y+26)
    b+=lines(160,170,'"Projeto" é só UM tipo de ação. O elo entre PPA e LOA é o PROGRAMA.',300,C['ambar'],10,'middle')
    return fig(svg(640,196,b),'Estrutura programática: função → subfunção → programa → ação. Item que diga "a LOA se integra ao PPA por meio dos projetos" é Errado (TROCA_TERMO).','Figura 5 · Programa e ações, com exemplo')
def F_autorizativo():
    b=txt(320,14,'Quanto o gestor pode cortar? O orçamento não é igual para todas as despesas',C['texto'],11.5,'middle',True)
    segs=[(10,210,'Obrigatórias',C['verm'],'pessoal, benefícios previstos em lei, dívida','não se contingenciam livremente (LRF art. 9º, §2º)'),
          (210,380,'Emendas impositivas',C['ambar'],'individuais e de bancada','têm execução obrigatória'),
          (380,630,'Discricionárias',C['verde'],'o resto: custeio e investimentos a critério do gestor','podem sofrer limitação de empenho para cumprir a meta da LDO')]
    for x1,x2,t,c,a,s in segs:
        b+='<rect x="%s" y="30" width="%s" height="40" fill="%s33" stroke="%s"/>'%(x1,x2-x1,c,c)+txt((x1+x2)/2,55,t,c,11.5,'middle',True)
        b+=lines((x1+x2)/2,88,a,x2-x1-14,C['texto'],9.5,'middle')+lines((x1+x2)/2,118,s,x2-x1-14,C['cinza'],9.5,'middle')
    b+=seta(380,150,40,150,C['verm'])+txt(210,168,'menos espaço para contingenciar',C['verm'],9.5,'middle')
    b+=seta(220,150,610,150,C['verde'])+txt(430,168,'mais espaço para contingenciar',C['verde'],9.5,'middle')
    b+='<rect x="120" y="182" width="400" height="34" rx="8" fill="#f8514922" stroke="%s"/>'%C['verm']+txt(320,203,'"exclusivamente autorizativo" = palavra absoluta → item Errado',C['verm'],10.5,'middle',True)
    return fig(svg(640,226,b),'A LOA autoriza o gasto, mas não o torna obrigatório em todos os casos. Dica de prova: ache a palavra absoluta antes de olhar o resto do item.','Figura 6 · Autorizativo, mas nem tudo se corta')
def F_raiox():
    def cw(t,size=10.5): return int(len(t)*size*0.62+18)
    b=txt(320,14,'Raio-X de um item: leia por partes',C['texto'],12,'middle',True)
    p1=[('O orçamento é',C['cinza']),('exclusivamente',C['verm']),('autorizativo,',C['cinza'])]
    x=10;xs=[]
    for t,c in p1:
        w=cw(t);b+=chip(x,56,w,28,t,c,10.5);xs.append((x,w));x+=w+8
    xa,wa=xs[1]
    b+=lines(xa+wa/2,32,'palavra ABSOLUTA',160,C['verm'],9.5,'middle',bold=True)+seta(xa+wa/2,38,xa+wa/2,54,C['verm'])
    t4='o que permite contingenciar para cumprir a meta da LDO';w4=cw(t4)
    b+=chip(10,96,w4,28,t4,C['verde'],10.5)
    b+=seta(10+w4+6,110,10+w4+24,110,C['verde'])+lines(10+w4+30,110,'parte certa (LRF art. 9º)',630-(10+w4+30),C['verde'],9.5,'start',bold=True)
    yv=142
    b+='<rect x="10" y="%s" width="620" height="38" rx="8" fill="#f8514922" stroke="%s"/>'%(yv,C['verm'])+lines(320,yv+16,'Veredito: ERRADO. Uma parte falsa basta; o Cebraspe não aproveita "meio certo".',590,C['verm'],10.5,'middle',bold=True)
    ys=yv+58;b+=txt(320,ys,'Quatro detectores para ligar a cada item',C['texto'],10.5,'middle',True)
    dets=[('ABSOLUTO','sempre, nunca, exclusivamente',C['verm']),('TROCA_TERMO','programa × projeto',C['ambar']),('INVERSAO','seta ao contrário',C['roxo']),('NÚMERO','prazo ou % inventado',C['azul'])]
    for i,(t,s_,c) in enumerate(dets): b+=box(10+i*157,ys+10,150,50,t,s_,c,ts=10.5,ss=9)
    return fig(svg(640,ys+70,b),'Técnica: (1) grife a palavra absoluta, (2) separe em partes, (3) pergunte de qual lei é o assunto, (4) confira números, (5) procure seta invertida.','Figura 7 · Dissecando um item Certo/Errado')
def F_regua():
    b=txt(320,14,'Quando marcar e quando deixar em branco (10 itens com a mesma confiança)',C['texto'],11.5,'middle',True)
    b+='<rect x="20" y="30" width="300" height="34" fill="#f8514933" stroke="%s"/><rect x="320" y="30" width="300" height="34" fill="#3fb95033" stroke="%s"/>'%(C['verm'],C['verde'])
    b+=txt(170,52,'deixe em branco',C['verm'],11,'middle',True)+txt(470,52,'marque',C['verde'],11,'middle',True)
    for p,s in [(30,'-4'),(40,'-2'),(50,'0'),(60,'+2'),(70,'+4'),(90,'+8')]:
        x=20+6*p;b+='<line x1="%s" y1="64" x2="%s" y2="74" stroke="%s"/>'%(x,x,C['cinza'])+txt(x,88,'%d%%'%p,C['texto'],10,'middle',True)+txt(x,104,s,C['verde'] if p>50 else C['verm'] if p<50 else C['ambar'],11,'middle',True)
    b+=txt(8,104,'saldo',C['cinza'],9,'start')+txt(8,88,'confiança',C['cinza'],9,'start')
    b+=lines(320,128,'Saldo esperado em 10 itens = 10 × (2p − 1). Acima de 50% o chute compensa; abaixo, perde.',600,C['cinza'],10,'middle')
    return fig(svg(640,148,b),'Cada erro anula um acerto. Com 50% de confiança o saldo esperado é zero: tanto faz. Só marque quando acreditar mais em "acertei" do que em "errei".','Figura 8 · Régua de decisão')
def F_mapa():
    b='<ellipse cx="320" cy="160" rx="82" ry="36" fill="#58a6ff22" stroke="%s"/>'%C['azul']+txt(320,155,'ORÇAMENTO',C['azul'],12,'middle',True)+txt(320,171,'PÚBLICO · Aula 1',C['azul'],10,'middle',True)
    esq=[('PPA','4 anos; programas e metas; o elo com a LOA é o programa',C['azul']),('LDO','prioridades e regras do ano; metas e riscos; limita os Poderes',C['ambar']),('LOA','3 orçamentos numa lei; exclusividade; autorizativa',C['verde'])]
    dir_=[('LRF e despesa nova','impacto em 3 exercícios; compensação permanente',C['roxo']),('Emendas','só anulação de despesa; compatíveis com PPA e LDO',C['verm']),('Receita','orçamentária = prevista na LOA; estágios',C['azul']),('Créditos adicionais','suplementar, especial, extraordinário',C['ambar'])]
    for i,(t,s,c) in enumerate(esq):
        y=14+i*100;b+=box(5,y,200,72,t,s,c);b+='<line x1="205" y1="%s" x2="240" y2="160" stroke="%s" stroke-dasharray="4 4"/>'%(y+36,c)
    for i,(t,s,c) in enumerate(dir_):
        y=4+i*76;b+=box(435,y,200,62,t,s,c);b+='<line x1="435" y1="%s" x2="400" y2="160" stroke="%s" stroke-dasharray="4 4"/>'%(y+31,c)
    return fig(svg(640,312,b),'Cola de uma página: se você consegue explicar cada caixa em uma frase, domina a Aula 1.','Figura 9 · Mapa mental da Aula 1')
FIGS=[('tramitacao',F_tramitacao,r'<h2>3\. Bloco A'),('ciclotxt',T_ciclo,r'<h2>3\. Bloco A'),('ciclo',F_ciclo,r'<h2>3\. Bloco A'),('ciclo2',F_ciclo2,r'<h2>3\. Bloco A'),('ciclochk',C_ciclo,r'<h2>3\. Bloco A'),('lrf',F_lrf,r'<h2>5\. Bloco C'),('creditos',F_creditos,r'<h2>8\. Bloco F'),
      ('programa',F_programa,r'<div class="box ok"><b class="t">Detalhe que a banca usa'),('autorizativo',F_autorizativo,r'<h2>11\. Como a banca'),('raiox',F_raiox,r'<h3>Quando vale arriscar'),
      ('regua',F_regua,r'<h2>12\. Resumo'),('mapa',F_mapa,r'<h2>13\. Caderno')]
def main():
    p=D/'corpo.html';s=p.read_text(encoding='utf-8')
    s=re.sub(r'<!--FIG:(\w+)-->.*?<!--/FIG:\1-->','',s,flags=re.S)
    for nome,fn,anc in FIGS:
        m=re.search(anc,s);assert m,nome
        # h2 abre uma <div class="pg"> antes? inserimos logo antes do cabeçalho
        s=s[:m.start()]+'<!--FIG:%s-->%s<!--/FIG:%s-->\n'%(nome,fn(),nome)+s[m.start():]
    s=s.replace('Aula 1 · v2','Aula 1 · v3',1)
    p.write_text(s,encoding='utf-8');print('figuras inseridas:',len(FIGS))
if __name__=='__main__': main()
