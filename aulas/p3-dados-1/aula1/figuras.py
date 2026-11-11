"""Figuras originais da aula P3·DADOS 1 (SVG dark)."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'_template'))
from visuais import *
def grade(x,y,cols,rows,cw,c='#58a6ff',rh=18,destaque=None):
    o='';n=len(cols);W=sum(cw)
    o+='<rect x="%s" y="%s" width="%s" height="%s" fill="%s22" stroke="%s"/>'%(x,y,W,rh,c,c)
    cx=x
    for i,t in enumerate(cols):
        o+=txt(cx+4,y+13,t,c,9.5,'start',True);cx+=cw[i]
    for r,row in enumerate(rows):
        yy=y+rh*(r+1);col='#f85149' if destaque==r else '#e6edf3'
        o+='<rect x="%s" y="%s" width="%s" height="%s" fill="#0d1117" stroke="#30363d"/>'%(x,yy,W,rh)
        cx=x
        for i,t in enumerate(row):
            o+=txt(cx+4,yy+13,t,col,9.5);cx+=cw[i]
    return o
def f_esquema():
    b=box(10,8,200,26,'ESQUEMA = o molde','',c='#a371f7',ts=12)
    b+=grade(10,40,['coluna','tipo'],[['id_servidor','inteiro'],['nome','texto'],['lotacao','texto']],[110,90],'#a371f7')
    b+=lines(10,118,'Muda só com ALTER TABLE. Muda pouco, é decisão de projeto.',200,'#8b949e',9.5)
    b+=box(250,8,380,26,'INSTÂNCIA = o conteúdo de hoje','',c='#58a6ff',ts=12)
    b+=grade(250,40,['id_servidor','nome','lotacao'],[['101','Ana','CGU/DF'],['102','Bruno','CGU/AM'],['103','Carla','CGU/SP']],[110,140,130])
    b+=lines(250,118,'Muda a cada INSERT, UPDATE ou DELETE. Uma foto do banco neste instante.',380,'#8b949e',9.5)
    b+=seta(212,60,248,60,'#8b949e')
    return fig(svg(640,135,b),'O molde (esquema) e a foto do conteúdo (instância). A banca troca um pelo outro.','Esquema × instância')
def f_pkfk():
    b=txt(10,14,'fornecedor (pai)',C['azul'],11,'start',True)+grade(10,20,['id_fornecedor (PK)','nome'],[['1','Alfa Ltda'],['2','Beta SA']],[130,110])
    b+=txt(330,14,'licitacao (filha)',C['verde'],11,'start',True)+grade(330,20,['id_licitacao (PK)','id_fornecedor (FK)'],[['10','1'],['11','2'],['12','9']],[110,130],C['verde'],destaque=2)
    b+=seta(328,56,252,50,C['azul'],azul=True)+seta(328,74,252,68,C['azul'],azul=True)
    b+=seta(328,92,252,92,C['verm'],tracejado=True)
    b+=txt(290,118,'FK 9 não existe na PK de fornecedor: registro órfão. Violaria a integridade referencial.',C['verm'],10,'middle')
    return fig(svg(640,130,b),'A chave estrangeira só pode apontar para um valor que exista na chave primária da tabela pai.','PK, FK e integridade referencial')
def f_nn():
    b=box(10,20,150,44,'auditor','PK id_auditor',c=C['azul'])+box(240,6,170,72,'auditor_auditoria','PK composta (id_auditor, id_auditoria) + 2 FKs',c=C['ambar'])+box(490,20,140,44,'auditoria','PK id_auditoria',c=C['verde'])
    b+=seta(162,42,238,42,C['azul'],azul=True)+seta(488,42,412,42,C['verde'])
    b+=chip(168,24,60,16,'1 : N',C['azul'],9)+chip(424,24,60,16,'N : 1',C['verde'],9)
    b+=lines(10,100,'No modelo conceitual: auditor N:N auditoria (um auditor participa de várias auditorias e cada auditoria tem vários auditores). No modelo físico, o N:N vira uma tabela no meio.',620,'#8b949e',10)
    return fig(svg(640,125,b),'Relacionamento N:N origina tabela associativa com duas chaves estrangeiras.','Do N:N à tabela associativa')
def f_formas():
    b=''
    xs=[10,225,440]
    t=[('1FN','Valores atômicos','Sem lista dentro da célula, sem grupo repetido','#58a6ff'),('2FN','1FN + sem dependência parcial','Só importa com chave composta: todo atributo depende da chave INTEIRA','#3fb950'),('3FN','2FN + sem dependência transitiva','Atributo não-chave não depende de outro não-chave. "Depende da chave, da chave toda e só da chave"','#d29922')]
    for i,(a,b2,c,col) in enumerate(t):
        b+=box(xs[i],10,190,100,a+' · '+b2,c,c=col,ts=11,ss=9.5)
    b+=seta(202,60,223,60,'#8b949e')+seta(417,60,438,60,'#8b949e')
    b+=txt(320,134,'Cada degrau contém o anterior. Objetivo: reduzir redundância e evitar anomalias de inserção, alteração e exclusão.',C['cinza'],10,'middle')
    return fig(svg(640,148,b),'Escada das formas normais: cada forma exige a anterior.','1FN, 2FN e 3FN')
def f_acid():
    b=''
    d=[('A','Atomicidade','Tudo ou nada',C['azul']),('C','Consistência','Banco sai de um estado válido para outro válido',C['verde']),('I','Isolamento','Uma transação não vê o meio da outra',C['ambar']),('D','Durabilidade','Confirmada, sobrevive a falha',C['roxo'])]
    for i,(l,n,s,c) in enumerate(d):
        x=10+i*157
        b+='<rect x="%s" y="8" width="148" height="104" rx="8" fill="#161b22" stroke="%s"/>'%(x,c)+txt(x+74,48,l,c,34,'middle',True)+txt(x+74,68,n,c,11.5,'middle',True)+lines(x+74,84,s,134,'#8b949e',9,'middle')
    return fig(svg(640,120,b),'ACID: A de Atomicidade (não "autenticidade"). Trocar a palavra da sigla é pegadinha recorrente.','As quatro propriedades de uma transação')
def f_log():
    b=''
    b+='<line x1="20" y1="45" x2="620" y2="45" stroke="#30363d" stroke-width="3"/>'
    ev=[(60,'T1 escreve no log',C['azul']),(200,'T1 COMMIT',C['verde']),(330,'T2 escreve no log',C['ambar']),(470,'💥 falha',C['verm'])]
    for x,t,c in ev:
        b+='<circle cx="%s" cy="45" r="6" fill="%s"/>'%(x,c)+txt(x,28,t,c,10,'middle',True)
    b+=box(380,70,230,56,'Recuperação','T1 confirmada: REDO (refaz). T2 sem commit: UNDO (desfaz).',c=C['roxo'],ts=11)
    b+=lines(20,84,'Regra do WAL: o log vai ao disco ANTES dos dados. Por isso o commit só vale quando já há log suficiente para refazer.',340,'#8b949e',10)
    b+=seta(470,52,490,68,C['verm'],tracejado=True)
    return fig(svg(640,135,b),'Linha do tempo de uma falha: o log decide quem é refeito e quem é desfeito.','Log, commit, REDO e UNDO')
def f_dead():
    b=box(20,10,150,34,'Transação T1','tem lock em A',c=C['azul'])+box(470,10,150,34,'Transação T2','tem lock em B',c=C['verde'])
    b+=box(20,100,150,30,'Recurso A',None,c=C['cinza'])+box(470,100,150,30,'Recurso B',None,c=C['cinza'])
    b+=seta(95,46,95,98,C['azul'],azul=True)+seta(545,46,545,98,C['verde'])
    b+=seta(172,26,468,110,C['azul'],tracejado=True,azul=True)+seta(468,26,172,110,C['verde'],tracejado=True)
    b+=txt(320,72,'espera um pelo outro',C['verm'],11,'middle',True)+txt(320,88,'DEADLOCK (ciclo de espera)',C['verm'],10,'middle')
    return fig(svg(640,142,b),'Linhas cheias: lock já obtido. Tracejadas: lock pedido. O SGBD detecta o ciclo e aborta uma das transações.','Deadlock')
def f_proc():
    b=txt(10,14,'Sem procedure',C['verm'],11,'start',True)+box(10,22,90,34,'Aplicação',None,c=C['azul'])+box(250,22,90,34,'Banco',None,c=C['cinza'])
    for i,y in enumerate((30,40,50)): b+=seta(102,y,248,y,C['verm'])
    b+=txt(175,70,'3 viagens de rede',C['verm'],10,'middle')
    b+=txt(380,14,'Com stored procedure',C['verde'],11,'start',True)+box(380,22,90,34,'Aplicação',None,c=C['azul'])+box(560,22,70,34,'Banco',None,c=C['cinza'])
    b+=seta(472,40,558,40,C['verde'])+txt(515,70,'1 chamada',C['verde'],10,'middle')
    return fig(svg(640,82,b),'A lógica roda dentro do banco, já compilada: menos tráfego de rede.','Stored procedure')
