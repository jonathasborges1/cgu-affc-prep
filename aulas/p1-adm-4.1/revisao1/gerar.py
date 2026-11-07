#!/usr/bin/env python3
"""Gera caderno de revisão + resumo de véspera de P1·ADM 4.1 (dark). Fonte: banco.jsonl (itens reais). Uso: python3 gerar.py"""
import json,re,html
from pathlib import Path
D=Path(__file__).resolve().parent; BASE=D.parent.parent.parent
css=(BASE/'aulas'/'_template'/'dark.css').read_text()
sel=json.load(open(D/'selecao.json',encoding='utf-8'))
key=lambda b:(b['prova_id'],str(b['item']))
by={ (b['prova_id'],str(b['item'])):b for b in sel}
ordem=[('codevasf-2024-c01-administracao','101'),('legado-930-inpi-cc1-01','80'),('tce-ac-2024-c14-administracao','99'),
('codevasf-2024-c01-administracao','103'),('legado-958-mpo-analista-001-01','21'),('tce-sc-auditor-2021-c01-administracao','81'),
('tce-sc-auditor-2021-c01-administracao','97'),('codevasf-2024-c01-administracao','94'),
('mpo-2024-c04-desenvolvimento-sistemas-orcamentari','5'),('legado-958-mpo-analista-001-01','8')]
assert len(ordem)==10 and all(k in by for k in ordem)
def limpa(b):
    t=re.sub(r'\s+',' ',b['enunciado']).strip()
    if b['prova_id'].startswith('mpo-2024') and b['item']=='5': t=t[:t.index('orçamento federal.')+len('orçamento federal.')]
    t=t.replace(' No que diz respeito à LRF, julgue os itens que se seguem.','')
    return t
nivel={'dificil':'difícil','difícil':'difícil','medio':'médio','médio':'médio','facil':'fácil','fácil':'fácil'}
SUB={('codevasf-2024-c01-administracao','101'):'Classificação funcional: função e subfunção',
('legado-930-inpi-cc1-01','80'):'Orçamento autorizativo × despesas obrigatórias',
('tce-ac-2024-c14-administracao','99'):'Sistema federal de planejamento e orçamento: órgãos central, setoriais e específicos',
('codevasf-2024-c01-administracao','103'):'Créditos adicionais: suplementar × especial',
('legado-958-mpo-analista-001-01','21'):'LDO orienta a elaboração da LOA e traz as metas fiscais',
('tce-sc-auditor-2021-c01-administracao','81'):'Princípios orçamentários: universalidade',
('tce-sc-auditor-2021-c01-administracao','97'):'LRF: dívida pública fundada (prazo de 12 meses)',
('codevasf-2024-c01-administracao','94'):'LOA: totalidade e os três orçamentos',
('mpo-2024-c04-desenvolvimento-sistemas-orcamentari','5'):'Arcabouço fiscal (LC 200/2023): vigência',
('legado-958-mpo-analista-001-01','8'):'Elo PPA–LOA: programa × projeto'}
COM={
('codevasf-2024-c01-administracao','101'):('C','Cópia fiel da definição: <b>função</b> = maior nível de agregação, ligada à missão institucional do órgão; <b>subfunção</b> = área da despesa em que a ação é executada. Sem palavra absoluta nem troca de termo. Item de leitura direta (NORMA_LITERAL): quem conhece a hierarquia função → subfunção → programa → ação marca Certo sem medo.'),
('legado-930-inpi-cc1-01','80'):('E','A segunda parte está certa: a limitação de empenho (contingenciamento) segue critérios da LDO para cumprir metas fiscais (LRF, art. 9º). O erro é <b>"exclusivamente"</b> autorizativo: há despesas obrigatórias (pessoal, benefícios legais, dívida) e emendas de execução obrigatória que não se contingenciam livremente. Parte certa + palavra absoluta = Errado (ABSOLUTO, PARTE_CERTA_PARTE_ERRADA).'),
('tce-ac-2024-c14-administracao','99'):('C','É a regra do sistema federal (Lei 10.180/2001): o órgão central orienta e supervisiona setoriais e específicos, <b>sem prejuízo</b> da subordinação ao órgão em que estão integrados. Pegadinha clássica do assunto é trocar as definições (dizer que setoriais são "vinculados ou subordinados ao central", que é o conceito de específicos); aqui nada foi trocado (NORMA_LITERAL).'),
('codevasf-2024-c01-administracao','103'):('E','Órgão novo, inexistente na LOA, não tem dotação alguma. <b>Suplementar</b> só reforça dotação que já existe; despesa sem dotação específica pede crédito <b>especial</b> (lei específica). Trocar o tipo de crédito é a pegadinha TROCA_TERMO.'),
('legado-958-mpo-analista-001-01','21'):('C','A LDO orienta a elaboração da LOA (CF, art. 165, §2º) e traz as metas fiscais (LRF, art. 4º). A expressão "exercício em vigor" é imprecisa, pois a LDO é feita no ano anterior ao do orçamento, mas o gabarito definitivo manteve Certo: o que o item cobra é a relação LDO → LOA. Lição: quando o núcleo está certo, não derrube o item por um detalhe de redação.'),
('tce-sc-auditor-2021-c01-administracao','81'):('E','A primeira parte define bem a universalidade (todas as receitas e despesas previstas na LOA). O erro está na consequência inventada: a cobrança de tributo <b>não</b> depende da previsão na LOA. Quem autoriza exigir tributo é a lei que o institui (legalidade tributária, CF art. 150, I), com as anterioridades; a antiga anualidade tributária não vale mais (CAUSA_CONSEQUENCIA).'),
('tce-sc-auditor-2021-c01-administracao','97'):('C','Pela LRF, a dívida pública consolidada (fundada) inclui operações de crédito com prazo superior a 12 meses; as de prazo menor só entram se a receita tiver constado do orçamento (art. 29, §3º). Aqui o prazo é de nove meses, mas a receita estava prevista na LOA: a operação entra no cálculo. O item parece "armadilha de prazo", mas a exceção do §3º o torna Certo (DETALHE_NUMERICO).'),
('codevasf-2024-c01-administracao','94'):('E','A totalidade manda incluir todas as receitas e despesas em um único orçamento. Os três orçamentos (fiscal, da seguridade social e de investimento das estatais) são <b>partes de uma só LOA</b>, não leis separadas; logo a LOA segue a totalidade. O item nega o princípio com uma causa inventada (INVERSAO, CAUSA_CONSEQUENCIA).'),
('mpo-2024-c04-desenvolvimento-sistemas-orcamentari','5'):('E','A estrutura da frase está certa (limites globais, a cada exercício, para despesas primárias), mas o número foi inventado: o regime da LC 200/2023 não "vigora por quarenta exercícios". Regra de prova: quando um item certo ganha um número específico que você não reconhece, desconfie (DETALHE_NUMERICO).'),
('legado-958-mpo-analista-001-01','8'):('E','O elo entre PPA e LOA é o <b>programa</b>: o programa do PPA reaparece na LOA detalhado em ações. "Projeto" é só um tipo de ação orçamentária (ao lado de atividade e operação especial). Troca de termo (TROCA_TERMO). Observação: o Cebraspe não publica justificativa; esta é a leitura mais coerente com o gabarito definitivo (Errado).')}
def cert(g): return '<span class="cert">Certo</span>' if g=='C' else '<span class="err">Errado</span>'
qs=[];gs=[]
for n,k in enumerate(ordem,1):
    b=by[k];g=b['gabarito'];assert g==COM[k][0],k
    tags=''.join('<span class="tag">%s</span>'%t for t in ['P1·ADM 4.1',SUB[k]]+b['nucleos']+b['tags']+[nivel[b['nivel'].lower()]])
    ref=html.escape(re.sub(r'\s+',' ',b['ref']))
    qs.append('<div class="q"><span class="tag">%d</span>%s<p>%s</p><div class="meta">Ref.: %s<br>Prova: %s<br>Gab.: %s</div></div>'%(n,tags,html.escape(limpa(b)),ref,b['url'],b['url_gab']))
    gs.append('<p><b>%d — %s.</b> %s</p>'%(n,cert(g),COM[k][1]))
gabs=''.join(c[0] for c in [COM[k] for k in ordem])
cad='''<style>.pg{page-break-after:auto}.cover{page-break-after:always}.q{break-inside:avoid;background:#161b22;border:1px solid #30363d;border-radius:2mm;padding:3mm 4mm;margin:3mm 0}.q p{margin:2mm 0}.meta{font-size:7.6pt;color:#8b949e;word-break:break-all}.tag{display:inline-block;background:#21262d;color:#79c0ff;border-radius:1.5mm;padding:0 2mm;margin:0 1.5mm 1mm 0;font-size:7.8pt}.cert{color:#3fb950;font-weight:bold}.err{color:#f85149;font-weight:bold}.small{font-size:8.6pt;color:#8b949e}</style>
<div class="pg cover"><div class="small">CGU · AFFC · TI – Desenvolvimento de Sistemas · Cebraspe · Edital 1/2026</div>
<h1 style="font-size:28pt;margin-top:6mm">Caderno de revisão<br>P1·ADM 4.1 – Planejamento e orçamento</h1>
<p style="font-size:12.5pt;color:#8b949e">10 itens reais do Cebraspe para revisar o que as Aulas 1, 2 e 3 ensinaram</p>
<div class="box"><b class="t">Seção do edital</b>P1 · Administração pública e fundamentos de políticas públicas — item 4.1: funções do planejamento e do orçamento; relação entre PPA, LDO e LOA; receita e despesa em nível conceitual; restrições fiscais, escolhas alocativas e sustentabilidade das ações.</div>
<div class="box tip"><b class="t">Como usar</b>Estes itens já foram vistos nas aulas; aqui servem de <b>revisão</b>, escolhidos entre os de maior pegadinha. Julgue cada um <b>antes</b> de ler o gabarito. Cinco são de nível médio e cinco difíceis. Errar custa o mesmo que acertar: marque só se sua confiança passar de 50%; senão, deixe em branco.</div>
<div class="box ok"><b class="t">Regra deste caderno</b>Todo item vem de uma prova real do Cebraspe, com link da prova e do gabarito definitivo no CDN oficial. Nenhuma questão foi inventada. Em dois itens o texto extraído do PDF foi aparado só para tirar resíduos de diagramação (cabeçalho do bloco); o enunciado do item não foi alterado.</div></div>
<div class="pg"><h2>Caderno de questões</h2><p class="small">Julgue Certo ou Errado. Cada item traz tags de tema e subtema, núcleo, pegadinha, nível, referência e URL da prova oficial; o gabarito definitivo está na URL indicada em "Gab.".</p>'''+''.join(qs)+'''</div>
<div class="pg" style="page-break-before:always"><h2>Gabarito comentado</h2><p class="small">Gabarito definitivo do Cebraspe: <b>'''+' · '.join('%d-%s'%(i+1,c) for i,c in enumerate(gabs))+'''</b>. O Cebraspe não publica justificativa dos itens; os comentários apoiam-se na Constituição (arts. 150, 165 e 166), na LRF, na Lei 4.320/1964 e nas aulas 1 a 3.</p>'''+''.join(gs)+'''
<div class="box tip"><b class="t">Seu placar</b>Conte acertos (A), erros (E) e brancos. Saldo = A − E. Abaixo de 6 acertos em 10, volte ao resumo de véspera e revise os blocos dos itens que errou: itens 2, 4, 5, 8 e 10 = Aula 1; itens 1, 3, 7 e 9 = Aula 2; item 6 = Aula 3.</div></div>'''
res_svg='''<svg viewBox="0 0 640 150" width="100%"><defs><marker id="m" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#58a6ff"/></marker></defs>
<rect x="10" y="20" width="170" height="50" rx="8" fill="#161b22" stroke="#58a6ff"/><text x="95" y="42" fill="#58a6ff" text-anchor="middle" font-size="14" font-weight="bold">PPA · 4 anos</text><text x="95" y="60" fill="#8b949e" text-anchor="middle" font-size="10">"para onde vamos?"</text>
<rect x="235" y="20" width="170" height="50" rx="8" fill="#161b22" stroke="#d29922"/><text x="320" y="42" fill="#d29922" text-anchor="middle" font-size="14" font-weight="bold">LDO · 1 ano</text><text x="320" y="60" fill="#8b949e" text-anchor="middle" font-size="10">"prioridades e regras"</text>
<rect x="460" y="20" width="170" height="50" rx="8" fill="#161b22" stroke="#3fb950"/><text x="545" y="42" fill="#3fb950" text-anchor="middle" font-size="14" font-weight="bold">LOA · 1 ano</text><text x="545" y="60" fill="#8b949e" text-anchor="middle" font-size="10">"quanto entra e sai"</text>
<line x1="180" y1="45" x2="233" y2="45" stroke="#58a6ff" marker-end="url(#m)"/><line x1="405" y1="45" x2="458" y2="45" stroke="#58a6ff" marker-end="url(#m)"/>
<text x="206" y="38" fill="#8b949e" text-anchor="middle" font-size="9">orienta</text><text x="431" y="38" fill="#8b949e" text-anchor="middle" font-size="9">orienta</text>
<rect x="10" y="100" width="170" height="38" rx="8" fill="#161b22" stroke="#f85149"/><text x="95" y="123" fill="#f85149" text-anchor="middle" font-size="11">planos setoriais</text>
<line x1="95" y1="100" x2="95" y2="72" stroke="#f85149" marker-end="url(#m)"/><text x="108" y="90" fill="#f85149" font-size="9">se encaixam no PPA (nunca o contrário)</text>
<text x="545" y="108" fill="#3fb950" text-anchor="middle" font-size="10">3 orçamentos numa só LOA:</text><text x="545" y="124" fill="#8b949e" text-anchor="middle" font-size="10">fiscal · seguridade · investimento</text></svg>'''
T=lambda rows,h:'<table><tr>%s</tr>%s</table>'%(''.join('<th>%s</th>'%x for x in h),''.join('<tr>%s</tr>'%''.join('<td>%s</td>'%c for c in r) for r in rows))
resumo='''<style>.pg{page-break-after:auto}.cover{page-break-after:always}.small{font-size:8.6pt;color:#8b949e}.cert{color:#3fb950;font-weight:bold}.err{color:#f85149;font-weight:bold}td,th{vertical-align:top}</style>
<div class="pg"><div class="small">CGU · AFFC · TI – Desenvolvimento de Sistemas · Cebraspe · Edital 1/2026</div>
<h1 style="font-size:24pt;margin-top:3mm">Resumo de véspera<br>P1·ADM 4.1 – Planejamento e orçamento</h1>
<p class="small">Para reler em 15 minutos. Consolida as Aulas 1, 2 e 3. Se algo aqui parecer estranho, volte à aula do bloco indicado entre colchetes.</p>
<h2>1. A cadeia que explica quase tudo</h2>'''+res_svg+'''
<div class="box"><b class="t">Regra de ouro [A1]</b>Ninguém gasta sem estar na LOA; a LOA obedece à LDO; a LDO caminha para o PPA. <b>Planos setoriais se adaptam ao PPA, nunca o contrário</b> (CF art. 165, §4º). Seta invertida = INVERSAO = suspeita de Errado.</div>
'''+T([['PPA','4 anos (2º ano do mandato até o 1º do seguinte)','Diretrizes, objetivos e metas; programas de duração continuada','Programa (elo com a LOA)'],
['LDO','1 ano','Metas e prioridades; orienta a LOA; legislação tributária; agências de fomento; limitação de empenho; anexos de metas e de riscos fiscais','Limita as propostas de todos os Poderes (CF 99 §4º: Executivo ajusta)'],
['LOA','1 ano','Orçamento fiscal + seguridade social + investimento das estatais','Exclusividade e totalidade; autorizativo']],['Lei','Horizonte','Conteúdo','Gancho de prova'])+'''
<h3>Datas clássicas [A1] (ADCT art. 35, §2º)</h3>'''+T([['PPA','31 de agosto (1º ano do mandato)','22 de dezembro'],['LDO','15 de abril','17 de julho'],['LOA','31 de agosto','22 de dezembro']],['Projeto','Enviado ao Congresso até','Devolvido para sanção até'])+'''
<h2>2. Blocos, regras e pegadinhas</h2>'''+T([
['LDO e metas [A1]','Anexo de <b>metas</b> fiscais ≠ anexo de <b>riscos</b> fiscais (passivos contingentes). Limites (pessoal etc.) são da LRF, não metas da LDO.','CONCEITO_MISTURADO, ABSOLUTO'],
['Despesa nova (LRF 16 e 17) [A1]','Estimativa de impacto no exercício e nos 2 seguintes. Obrigatória continuada (&gt; 2 exercícios): não afetar metas e compensar com <b>aumento permanente de receita ou redução permanente de despesa</b>. Venda de imóvel não serve.','"de forma exclusiva", momento da compensação, números'],
['Emendas à LOA [A1]','Compatíveis com PPA e LDO; recurso <b>só por anulação de despesa</b> (exceto pessoal, dívida, transferências). Erros/omissões = hipótese de cabimento, não fonte.','ESCOPO, TROCA_TERMO'],
['Receita [A1, A3]','Orçamentária = prevista na LOA. Corrente × capital; originária × derivada. Estágios: lançamento, arrecadação, recolhimento; previsão é planejamento. Regime orçamentário = <b>arrecadação</b>, que não coincide "necessariamente" com o fato gerador.','TROCA_TERMO, ABSOLUTO'],
['Créditos adicionais [A1]','<b>Suplementar</b> reforça dotação existente; <b>especial</b> = sem dotação específica (órgão novo), lei específica; <b>extraordinário</b> = urgente e imprevisível, por MP. Fontes: superávit, excesso de arrecadação, anulação, operações de crédito.','TROCA_TERMO'],
['PPA [A1]','Elo com a LOA = <b>programa</b> (ações orçamentárias e não orçamentárias). Ações: projeto, atividade, operação especial.','TROCA_TERMO'],
['LOA [A1]','Exclusividade: só receita e despesa, exceto créditos suplementares e operações de crédito (inclusive ARO). Autorizativo, mas <b>nunca "exclusivamente"</b>: obrigatórias e emendas impositivas.','ABSOLUTO + PARTE_CERTA'],
['Sistema e arcabouço [A2]','Central orienta e supervisiona; <b>setorial</b> = dentro dos Ministérios; <b>específico</b> = vinculado/subordinado ao central. LC 200/2023: limite global de despesas primárias; crescimento real = 70% do da receita, piso 0,6% e teto 2,5%; 50% se a meta primária do ano anterior falhar. <b>Sem "quarenta exercícios".</b>','TROCA_TERMO, DETALHE_NUMERICO'],
['Classificação funcional e despesa [A2]','Função = maior agregação (missão do órgão); subfunção = área da despesa; função ≠ programa. Sem dotação ou crédito adicional não há despesa nem contratação; empenho → liquidação → pagamento.','CAUSA_CONSEQUENCIA'],
['Dívida consolidada [A2]','&gt; 12 meses entra; ≤ 12 meses só entra se a receita constou do orçamento (LRF art. 29, §3º).','DETALHE_NUMERICO'],
['Funções do Estado e modelos [A3]','Alocativa (bens públicos e meritórios), distributiva (renda), estabilizadora (emprego, preços). Alocação nunca "exclusivamente" por orçamento. Tradicional = autorização política; programa = objetivos e metas; base zero = tudo reexaminado, sem direito adquirido.','ABSOLUTO'],
['Princípios [A3]','Unidade (harmonia PPA/LDO/LOA), universalidade (tudo na LOA), exclusividade. A LOA <b>não condiciona</b> a cobrança de tributo: quem institui é a lei (CF 150, I).','CAUSA_CONSEQUENCIA']],['Bloco','O que precisa estar na ponta da língua','Pegadinha típica'])+'''
<h2>3. Técnica de prova Certo/Errado</h2>
<div class="box tip"><b class="t">Cinco passos para cada item</b>1) Grife a palavra absoluta (exclusivamente, sempre, necessariamente, apenas). 2) Separe o item em partes; uma parte falsa derruba o item inteiro. 3) Pergunte "de qual lei é isso?" (PPA, LDO ou LOA). 4) Olhe os números e prazos (12 meses, dois exercícios, 70%, 0,6% a 2,5%, 4 anos). 5) Procure a seta invertida e a consequência inventada ("por isso", "de modo que").</div>
<div class="box warn"><b class="t">Quando marcar</b>Saldo esperado por item = 2p − 1 (p = sua chance de acertar). Só compensa marcar com confiança acima de 50%. Em 10 itens com 60% de confiança, o esperado é 6 acertos e 4 erros: saldo +2. Com 40%, saldo −2: deixe em branco.</div>
<h2>4. Checklist de véspera</h2>
<div class="box ok">☐ Digo de cabeça: PPA 4 anos, LDO e LOA 1 ano.<br>☐ Sei o que cada lei traz e quem orienta quem.<br>☐ Sei as regras da LRF: três exercícios, compensação permanente, 12 meses na dívida.<br>☐ Sei trocar mentalmente suplementar × especial × extraordinário.<br>☐ Sei que o elo PPA–LOA é programa, não projeto.<br>☐ Desconfio de "exclusivamente", "necessariamente" e de números que eu não reconheço.<br>☐ Refiz o caderno de revisão e li o gabarito comentado.</div></div>'''
def doc(t,c): return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>'%(t,css,c)
(D/'caderno-revisao.html').write_text(doc('Caderno de revisão P1·ADM 4.1',cad),encoding='utf-8')
(D/'resumo-vespera.html').write_text(doc('Resumo de véspera P1·ADM 4.1',resumo),encoding='utf-8')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br=p.chromium.launch()
    for n in ('caderno-revisao','resumo-vespera'):
        pg=br.new_page();pg.goto('file://'+str((D/(n+'.html')).resolve()))
        pg.pdf(path=str(D/(n+'.pdf')),prefer_css_page_size=True,print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'});print('ok',n)
    br.close()
json.dump({'tema':'P1·ADM 4.1','tipo':'revisao','data':'2026-11-05','itens':['%s#%s'%k for k in ordem],'gabarito':gabs,'nota':'itens reaproveitados das aulas 1-3 (revisao); nao registrado no ledger de aulas'},open(D/'manifest.json','w'),ensure_ascii=False,indent=1)
