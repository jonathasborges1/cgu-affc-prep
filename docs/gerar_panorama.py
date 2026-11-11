#!/usr/bin/env python3
"""Gera docs/PANORAMA-CGU-BD.pdf (dark mode). Roda local, sem custo de créditos:  python3 docs/gerar_panorama.py
PARA ATUALIZAR: edite só os blocos de DADOS abaixo (VERSAO, CHANGELOG, ETAPAS, ESTRUTURA, PENDENCIAS...) e rode de novo.
Sempre que mudar a estrutura (comandos, estados, pastas, agentes, skills), acrescente uma linha em CHANGELOG."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon

# ===================== DADOS (editar aqui) =====================
VERSAO = "v4.5"; DATA = "10/11/2026"
CHANGELOG = [
 ("10/11/2026","v4.6","Auditoria ponderada das amostras cegas estratificadas P2/P3: precisão e IC90 reproduzíveis; recall explicitamente não estimável sem amostra representativa dos descartados."),
 ("10/11/2026","v4.5","Adicionadas filas de tarefas ML locais sem aplicação automática, validação estrutural dos lotes e pendências explícitas de revisão semântica. O banco só avança pelos portões de classificação/verificação existentes."),
 ("10/11/2026","v4.4","Mineração local recursiva com blacklist por URL/hash, retomada de downloads válidos, interrupção explícita em 403/429 e gates de confiança por bloco. P2/P3 ficam provisórios até validação independente."),
 ("04/11/2026","v4.2","Pasta concursos/<id>/ com concurso.json (cargo-alvo), edital oficial, programa.json/.md (275 subitens) e regras da prova. banco.py: concurso ativo, edital lacunas/buscar, portão valida códigos contra o programa. scripts/importar_edital.py."),
 ("04/11/2026","v4.1","Download, texto, gabarito e itens passaram a rodar local (prova baixar/texto/extrair/processar). Pasta provas/ID/ guarda os PDFs. Pasta docs/ criada. Este PDF criado."),
 ("04/11/2026","v4.0","banco.py com manifesto de provas, portões, comparar, aplicar, rank e verificar-caderno. Agentes classificador e verificador. Skill de classificação."),
 ("02/11/2026","v3","Banco local inicial (75 itens), núcleos, taxonomia de pegadinhas, workflow probabilístico."),
]
# (etapa, onde roda: MAQUINA ou CLAUDE, custo, como)
ETAPAS = [
 ("Importar o edital (PDF) para programa.json","MAQUINA","zero","scripts/importar_edital.py (uma vez por edital)"),
 ("Ver subitens do programa sem questão","MAQUINA","zero","edital lacunas"),
 ("Escolher a próxima prova a minerar","CLAUDE","baixo","Lê o ranking de compatibilidade; depois 'prova add' (local)"),
 ("Baixar PDF da prova e do gabarito","MAQUINA","zero","prova processar ID (Chrome só se o site bloquear)"),
 ("Guardar PDFs, hash e origem","MAQUINA","zero","provas/ID/ + fonte.txt"),
 ("Extrair texto, gabarito e itens","MAQUINA","zero","pdftotext + extrator no banco.py"),
 ("Portão: itens = gabaritos","MAQUINA","zero","recusa avançar se não bater"),
 ("Conferir itens marcados 'revisar'","CLAUDE","baixo","só os poucos itens com código ou figura"),
 ("Classificar itens (edital, núcleo, pegadinha)","CLAUDE","ALTO","agente classificador-itens, 1 por prova"),
 ("Sortear amostra de 20%","MAQUINA","zero","prova amostra ID"),
 ("Reclassificar a amostra (checagem independente)","CLAUDE","médio","agente verificador-classificacao"),
 ("Comparar concordância e decidir","MAQUINA","zero","comparar ID (mínimos 90/80/80)"),
 ("Gravar no banco","MAQUINA","zero","aplicar ID"),
 ("Ranking, cobertura e plano da aula","MAQUINA","zero","rank --edital ..."),
 ("Escrever a aula (PDF dark mode)","CLAUDE","ALTO","explicação do zero, ilustrações, como a banca cobra"),
 ("Escolher os ids do caderno (máx. 10)","CLAUDE","baixo","a partir do banco"),
 ("Validar o caderno","MAQUINA","zero","verificar-caderno lista.json"),
 ("Atualizar este panorama (PDF)","MAQUINA","zero","python3 docs/gerar_panorama.py"),
]
ESTRUTURA = [
 ("README.md / ORQUESTRACAO.md","Entrada e roteiro que o Claude lê primeiro"),
 ("banco.py / scripts/","Programa único (Python): estado, portões, ranking, validações; importar_edital.py lê o PDF do edital"),
 ("concursos/ativo.txt","Qual concurso está em uso (troca com: banco.py concurso usar ID)"),
 ("concursos/<id>/","concurso.json (cargo-alvo), edital-oficial.pdf, programa.json/.md, regras-da-prova.md e os dados do concurso: banco, núcleos, manifesto, classificações"),
 ("provas/ID/","PDFs da prova e do gabarito, fonte.txt, prova.txt, gabarito.txt"),
 ("extraidos/ (compartilhado)","Itens extraídos de cada prova, um .jsonl por prova"),
 ("skills/","Manuais: classificação, coleta, priorização (cópia das skills da conta)"),
 ("agentes/","Instruções dos 2 agentes (classificador e verificador)"),
 ("edital-topicos.md / taxonomia-pegadinhas.md","Códigos do edital e etiquetas de pegadinha"),
 ("docs/","Manuais: ARQUIVOS, workflow-v2, portabilidade, regras do Projeto e este PANORAMA"),
 ("referencia/","Documentos históricos transcritos do Projeto"),
]
PENDENCIAS = [
 "Classificar a prova TCE-AC 2024 cargo 11 (70 itens extraídos, estado 'extraida'). Cobertura do programa hoje: 1 de 205 subitens com questão.",
 "Banco, núcleos e classificações são por concurso; provas/ e extraidos/ são compartilhados. Rank ainda usa limiares fixos no código (concurso.json guarda os valores, mas o rank não os lê).",
 "Extrator testado só no layout Cebraspe de duas colunas; outras bancas podem exigir ajuste.",
 "Itens 70 e 97 da TCE-AC marcados 'revisar' (código no enunciado).",
 "O espelho no Projeto do Claude está desatualizado em relação ao PC (a fonte correta é o PC).",
 "Limiares (70% de cobertura, 80% de massa, 90/80/80 de concordância) são regras iniciais a calibrar.",
 "Termos de uso do TEC Concursos ainda não lidos; o TEC bloqueou acessos (405/429).",
]
# ===================== fim dos DADOS =====================

BG=colors.HexColor("#0f1420"); PANEL=colors.HexColor("#182034"); TXT=colors.HexColor("#e6e9f0"); MUT=colors.HexColor("#9aa4b8")
BLUE=colors.HexColor("#6aa9ff"); GREEN=colors.HexColor("#4ade80"); AMB=colors.HexColor("#fbbf24"); LINE=colors.HexColor("#2b3550")
def S(n,**k): return ParagraphStyle(n,fontName=k.pop('fontName','Helvetica'),textColor=k.pop('textColor',TXT),**k)
body=S('b',fontSize=9.5,leading=13.5,spaceAfter=5); h1=S('h1',fontName='Helvetica-Bold',fontSize=19,leading=23,textColor=BLUE,spaceBefore=4,spaceAfter=8)
h2=S('h2',fontName='Helvetica-Bold',fontSize=12.5,leading=16,textColor=AMB,spaceBefore=8,spaceAfter=4); cell=S('c',fontSize=8.3,leading=10.6); cellb=S('cb',fontName='Helvetica-Bold',fontSize=8.3,leading=10.6)
small=S('s',fontSize=8,leading=10.5,textColor=MUT); title=S('t',fontName='Helvetica-Bold',fontSize=30,leading=36,textColor=BLUE)
def P(t,st=body): return Paragraph(t,st)
def box(txt,color=BLUE):
    t=Table([[P(txt,cell)]],colWidths=[17*cm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PANEL),('LINEBEFORE',(0,0),(0,-1),3,color),('LEFTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])); return t
def fluxo():
    d=Drawing(17*cm,5.6*cm)
    st=[("descoberta","M"),("baixada","M"),("extraida","C"),("classificada","C"),("verificada","M"),("persistida","M")]
    quem=["baixa + extrai (local)","extrai itens (local)","agente classifica","agente verifica 20%","comparar (local)","aplicar (local)"]
    w=2.5*cm; gap=0.4*cm; y=3.1*cm
    for i,(n,q) in enumerate(st):
        x=i*(w+gap); cor=GREEN if q=="M" else AMB
        d.add(Rect(x,y,w,1.5*cm,fillColor=PANEL,strokeColor=cor,strokeWidth=1.6,rx=6,ry=6))
        d.add(String(x+w/2,y+0.55*cm,n,textAnchor='middle',fontName='Helvetica-Bold',fontSize=8.6,fillColor=TXT))
        d.add(String(x+w/2,y-0.5*cm,quem[i],textAnchor='middle',fontName='Helvetica',fontSize=6.8,fillColor=cor))
        if i<5:
            xa=x+w+0.03*cm; ym=y+0.75*cm
            d.add(Line(xa,ym,xa+gap-0.1*cm,ym,strokeColor=MUT,strokeWidth=1.2))
            d.add(Polygon([xa+gap-0.1*cm,ym+0.1*cm,xa+gap-0.1*cm,ym-0.1*cm,xa+gap+0.04*cm,ym],fillColor=MUT,strokeColor=MUT))
    d.add(String(0,5.2*cm,"Estado de cada prova (manifesto provas.jsonl). Cada seta só passa por um PORTÃO no banco.py.",fontName='Helvetica',fontSize=8.2,fillColor=MUT))
    d.add(String(0,1.5*cm,"Falha em qualquer portão: o estado não avança. Verificação reprovada: a prova volta para 'extraida'.",fontSize=7.5,fontName='Helvetica',fillColor=MUT))
    d.add(Rect(0,0.3*cm,0.35*cm,0.35*cm,fillColor=GREEN,strokeColor=GREEN)); d.add(String(0.5*cm,0.36*cm,"roda na sua máquina (sem créditos)",fontSize=7.5,fontName='Helvetica',fillColor=TXT))
    d.add(Rect(6.2*cm,0.3*cm,0.35*cm,0.35*cm,fillColor=AMB,strokeColor=AMB)); d.add(String(6.7*cm,0.36*cm,"usa o Claude (créditos)",fontSize=7.5,fontName='Helvetica',fillColor=TXT))
    return d
def tabela(rows,widths,head):
    data=[[P(h,cellb) for h in head]]+[[P(str(c),cell) for c in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LINE),('ROWBACKGROUNDS',(0,1),(-1,-1),[PANEL,BG]),('GRID',(0,0),(-1,-1),0.3,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)])); return t
def page(c,doc):
    c.saveState(); c.setFillColor(BG); c.rect(0,0,A4[0],A4[1],fill=1,stroke=0); c.setFillColor(MUT); c.setFont('Helvetica',7.5)
    c.drawString(2*cm,1.1*cm,"cgu-bd | Panorama do projeto %s | %s"%(VERSAO,DATA)); c.drawRightString(A4[0]-2*cm,1.1*cm,"pág. %d"%doc.page); c.restoreState()
def main():
    out=os.path.join(os.path.dirname(os.path.abspath(__file__)),"PANORAMA-CGU-BD.pdf")
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=1.8*cm,bottomMargin=1.8*cm,title="Panorama cgu-bd",author="Jonathas / Claude")
    doc.addPageTemplates([PageTemplate(id='p',frames=[Frame(2*cm,1.8*cm,17*cm,A4[1]-3.6*cm,id='f')],onPage=page)])
    mono="<font name='Courier'>%s</font>"
    E=[Spacer(1,3*cm),P("Panorama do cgu-bd",title),Spacer(1,6),P("Banco local e workflow de engenharia reversa para o concurso CGU/AFFC 2026 (TI – Desenvolvimento de Sistemas)",S('sub',fontSize=12,leading=16,textColor=MUT)),Spacer(1,10),
       P("Versão %s | atualizado em %s"%(VERSAO,DATA),small),Spacer(1,24),
       box("<b>Ideia central.</b> O Claude não guarda o andamento na memória: o andamento fica em arquivos na sua máquina. Tudo que é mecânico (baixar, extrair, contar, comparar, ranquear, validar) roda localmente em Python e custa zero de créditos. O Claude entra só onde há julgamento: classificar itens, checar uma amostra e escrever aulas e cadernos.",BLUE),Spacer(1,8),
       box("<b>Como manter este documento.</b> Ao mudar qualquer coisa na estrutura, edite os blocos de DADOS no início de "+mono%"docs/gerar_panorama.py"+" (principalmente o CHANGELOG) e rode "+mono%"python3 docs/gerar_panorama.py"+". Gerar o PDF é local e não gasta créditos.",GREEN),PageBreak()]
    E+=[P("1. O que construímos",h1),
        P("O objetivo é descobrir <b>o que a banca mais cobra</b> em cada tema do edital e ensinar nessa ordem. Para isso montamos um banco de questões reais de provas anteriores, classificamos cada item por tema do edital, por <i>núcleo</i> (a ideia única que o item testa) e por tipo de pegadinha, e calculamos a massa de cada núcleo (peso da prova x recência). A aula ensina os núcleos até cobrir cerca de 80% da massa acumulada; o caderno usa só itens reais, com referência e URL."),
        fluxo(),Spacer(1,6),P("Peças principais",h2),
        tabela([("banco.py","Programa único. Guarda o estado, aplica os portões, ranqueia e valida. Python padrão; precisa do pdftotext (ou do pypdf) para ler PDF."),
                ("Skills (3)","Manuais em .md carregados sob demanda: classificar itens, coletar questões, priorizar temas."),
                ("Agentes (2)","Executores com instruções próprias: classificador-itens e verificador-classificacao. Não ficam registrados na conta; o Claude lê o .md e os dispara."),
                ("Arquivos .jsonl","O estado: uma linha de JSON por registro. Abrem em qualquer editor.")],[3.4*cm,13.6*cm],["Peça","Papel"]),PageBreak()]
    rows=[]
    for e,q,c,h in ETAPAS:
        col="#4ade80" if q=="MAQUINA" else "#fbbf24"
        rows.append(("<b>%s</b>"%e,"<font color='%s'><b>%s</b></font>"%(col,"Máquina" if q=="MAQUINA" else "Claude"),c,h))
    E+=[P("2. Quem faz cada etapa e quanto custa",h1),P("<b>Verde = sua máquina, zero de créditos. Amarelo = Claude.</b> A coluna de custo é qualitativa (relativa entre as etapas), não uma medida em tokens."),
        tabela(rows,[6.3*cm,2.1*cm,1.7*cm,6.9*cm],["Etapa","Onde roda","Custo","Como"]),Spacer(1,8),
        box("<b>Nota honesta.</b> Mesmo as etapas locais são disparadas pelo Claude: cada comando é uma chamada curta e devolve uma linha de resumo. A economia vem de o trabalho pesado (PDF, texto, contagens, comparações) não entrar na conversa.",AMB),PageBreak()]
    E+=[P("3. Onde a economia acontece",h1),
        tabela([("Download e leitura de PDF","Navegador do Claude e leitura do conteúdo na conversa","Download direto pela máquina; o PDF nunca entra na conversa"),
                ("Separar itens e gabarito","O Claude lia o texto e montava os itens","Extrator em Python; devolve só a contagem e os itens a revisar"),
                ("Conferir contagens, hash e cobertura","Raciocínio do Claude a cada vez","Portões no banco.py (determinísticos)"),
                ("Verificar a classificação","Reclassificar tudo","Amostra de 20% e comparação automática"),
                ("Ranking e plano da aula","Cálculo manual em prosa","rank --edital: calculado localmente"),
                ("Validar o caderno","Conferir id por id na conversa","verificar-caderno devolve APROVADO ou a lista de problemas")],[4.2*cm,6*cm,6.8*cm],["Tarefa","Antes","Agora"]),
        P("Onde os créditos ainda são gastos (e é correto que sejam)",h2),
        P("<b>1) Classificar itens</b> é o maior custo recorrente, proporcional ao número de itens. <b>2) Escrever aulas</b>, que exigem explicação do zero e material visual. <b>3) Verificar a amostra</b>, cerca de 20% do custo de uma segunda classificação. Não existe modelo local que substitua esse julgamento com a mesma qualidade."),
        P("Regras para manter o gasto baixo",h2),
        P("&bull; Passar ao agente só o <b>caminho</b> do arquivo, nunca o conteúdo.<br/>&bull; Não abrir prova.txt, exceto para consertar item sinalizado.<br/>&bull; Um agente por prova, devolvendo só a contagem e os itens com dúvida.<br/>&bull; Não reclassificar item que já está no banco.<br/>&bull; Classificar só provas compatíveis com o edital (ranking de compatibilidade).<br/>&bull; Reservar o Chrome para quando o download direto falhar."),
        P("Ideias ainda não aplicadas",h2),
        P("&bull; Definir um modelo mais leve no campo <i>model</i> do agente classificador e medir a concordância com o próprio <i>comparar</i> antes de adotar.<br/>&bull; Filtrar por palavras-chave os itens claramente fora do edital antes de classificar.<br/>&bull; Agrupar a classificação em lotes por tema."),PageBreak()]
    E+=[P("4. Estrutura de pastas e portões",h1),tabela(ESTRUTURA,[6.2*cm,10.8*cm],["Caminho","Conteúdo"]),
        P("Portões (o banco.py recusa avançar se falhar)",h2),
        tabela([("baixada","provas/ID/prova.pdf e gabarito.pdf válidos; hash gravado (ou --sem-arquivo com nota)"),
                ("extraida","itens extraídos = gabaritos (anulados fora) = linhas de extraidos/ID.jsonl"),
                ("classificada","classificacoes/ID.jsonl cobre exatamente os itens; edital e etiquetas válidos"),
                ("verificada","só por 'comparar': concordância mínima de 90% (edital), 80% (núcleo) e 80% (pegadinha)"),
                ("persistida","só por 'aplicar'")],[3*cm,14*cm],["Estado","Condição"]),
        P("Comandos mais usados",h2),
        P(mono%"prova add ..."+" cadastra a prova. "+mono%"prova processar ID"+" baixa, extrai e avança. "+mono%"prova proxima"+" mostra o que falta. "+mono%"prova amostra ID"+", "+mono%"comparar ID"+" e "+mono%"aplicar ID"+" fecham a verificação. "+mono%"rank --edital \"P3·ENG 2\""+" planeja a aula. "+mono%"verificar-caderno lista.json"+" valida o caderno. Todos começam com "+mono%"python3 banco.py"+"."),PageBreak()]
    E+=[P("5. Pendências e limites",h1)]+[P("&bull; "+x) for x in PENDENCIAS]+[Spacer(1,8),P("6. Histórico de versões",h1),tabela(CHANGELOG,[2.4*cm,1.5*cm,13.1*cm],["Data","Versão","Mudança"])]
    doc.build(E); print("ok",out)
main()
