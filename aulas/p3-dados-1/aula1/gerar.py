#!/usr/bin/env python3
"""Gera corpo.html e manifest.json da aula P3·DADOS 1 (idempotente). Uso: python3 gerar.py"""
import sys,json,re
from pathlib import Path
from html import escape as e
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D.parents[1]/'_template'));sys.path.insert(0,str(D))
from pedagogia import *
import figuras as F
IT={}
for x in json.loads((D/'itens.json').read_text(encoding='utf-8')):
    IT[(x['prova_id'],str(x['item']))]=x
def get(pre,n):
    for (p,i),x in IT.items():
        if p.startswith(pre) and i==str(n): return x
    raise KeyError((pre,n))
def txtq(x):
    t=x['enunciado']
    t=t.split(' JUSTIFICATIVA')[0]
    if x['prova_id'].startswith('tce-ac-2024-c06') and str(x['item'])=='69': t=t.replace('sobre os dados A integridade','A integridade').split(' A figura a seguir')[0]
    return t.strip()
def nv(x): return {'medio':'Médio','médio':'Médio','facil':'Fácil','fácil':'Fácil'}.get(str(x.get('nivel')).lower(),x.get('nivel'))
def cita(x):
    return '<span class="small">%s · item %s · <a href="%s">fonte</a></span>'%(e(x['ref']),e(str(x['item'])),e(x['url']))
def banca(x,pegadinha):
    g='Certo' if x['gabarito']=='C' else 'Errado'
    cl='cert' if x['gabarito']=='C' else 'err'
    return ('<div class="box warn"><b class="t">Como a banca cobra (item real, gabarito <span class="%s">%s</span>)</b>'
            '<p>“%s”</p><p><b>Pegadinha:</b> %s</p>%s</div>')%(cl,g,e(txtq(x)),e(pegadinha),cita(x))
def tabela(cab,linhas):
    return '<table><tr>%s</tr>%s</table>'%(''.join('<th>%s</th>'%e(c) for c in cab),''.join('<tr>%s</tr>'%''.join('<td>%s</td>'%e(c) for c in l) for l in linhas))
def bloco(titulo,corpo,prev,par,ec,chk):
    return '<div class="pg">\n<h2>%s</h2>\n%s\n%s\n%s\n%s\n%s\n</div>\n'%(titulo,corpo,previsao(*prev),parabola(*par),exemplo_contra(*ec),checagem(*chk))
P=[]
P.append('''<div class="pg cover">
<div class="small">CGU · AFFC · TI – Desenvolvimento de Sistemas · Cebraspe · Edital 1/2026</div>
<h1 style="font-size:32pt;margin-top:6mm">Aula 1<br>Modelagem relacional, normalização, transações e ACID</h1>
<p style="font-size:13pt;color:#8b949e">P3 · Persistência, integração e proteção de dados – itens 1.1, 1.5 e 2.1 do edital</p>
<div class="box"><b class="t">Seção do edital</b>P3 · Persistência, integração e proteção de dados, item 1: modelagem relacional, normalização e integridade; transações, concorrência, consistência e evolução de esquemas; SQL e controle transacional.</div>
<div class="box ok"><b class="t">Como esta aula foi montada</b>De trás para frente: partiu de itens reais do Cebraspe sobre o tema (PETROBRAS 2021, FUNPRESP 2021 e 2024, SEFIN-Fortaleza 2023, MPO 2024, TCE-AC 2024, BDMG 2024, MP-TO 2024, SEPLAG-CE 2024, STM 2025, CNJ 2024 e PC-DF 2024). Você já programa em Java, então ensino pouco "o que é SQL" e muito o que a banca troca de lugar.</div>
<div class="small" style="margin-top:8mm">Cada item citado traz o link da prova oficial no site do Cebraspe, para você conferir.</div>
</div>
''')
P.append('<div class="pg">\n<h2>1. Objetivo e mapa da aula</h2>\n<p>Ao final você deve olhar um item Certo/Errado sobre banco de dados relacional e dizer: <b>qual termo foi trocado, qual propriedade está sendo testada e se há palavra absoluta</b>.</p>'
 +tabela(['Bloco','Pergunta que responde','Palavra-chave da prova'],[
 ['2. Tabelas e esquema','O que é esquema e o que é instância?','esquema × instância'],
 ['3. Chaves e integridade','Para que servem PK e FK?','integridade referencial'],
 ['4. Relacionamento N:N','Como o N:N vira tabela?','tabela associativa'],
 ['5. Normalização','O que são 1FN, 2FN e 3FN?','redundância, dependência transitiva'],
 ['6. Normalização na prática','Quando normalizar demais atrapalha?','desnormalização, "sempre"'],
 ['7. Transações e ACID','O que garante cada letra?','atomicidade'],
 ['8. Log, commit e rollback','Como o banco se recupera de falha?','REDO, UNDO'],
 ['9. Locks e deadlock','Quem cuida do isolamento?','bloqueio, ciclo de espera'],
 ['10. Stored procedures','Por que rodar lógica dentro do banco?','pré-compilada, tráfego']])
 +'<div class="box tip"><b class="t">Fora desta aula (por enquanto)</b>Os subitens do edital de JPA, Spring Data JPA, carregamento lazy/eager, cache, busca textual e bancos documentais/vetoriais ainda não têm item real no banco local. Ficam para as próximas micro-aulas, quando houver questões reais para ancorá-las.</div></div>\n')
x=get('bdmg-2024-c02',76)
P.append(bloco('2. Tabelas, esquema e instância',
 '<p>Um banco relacional guarda tudo em <b>tabelas</b>: linhas (registros) e colunas (atributos). Pense numa planilha em que cada coluna tem tipo fixo. A pergunta que a banca adora: o que é o <i>molde</i> e o que é o <i>conteúdo</i>?</p>'+F.f_esquema()
 +'<p>O <b>esquema</b> descreve estrutura (tabelas, colunas, tipos, restrições). A <b>instância</b> é o conjunto de dados num dado momento. Também aparece o termo <b>independência de dados</b>: mudar a estrutura física (índices, disco) sem reescrever a aplicação.</p>'
 +banca(x,'Troca esquema (organização lógica) por instância (dados no momento).'),
 ('Se você inserir mais uma linha na tabela de servidores, muda o esquema, a instância ou os dois? Aposte.','Só a instância. O esquema muda apenas com comandos de definição, como ALTER TABLE.'),
 ('A coluna nova (Agência Federal de Obras, fictícia)',[('Problema','A AFO precisa registrar o e-mail institucional dos servidores. Hoje a tabela servidor tem id, nome e lotação.'),('Decisão','O DBA roda ALTER TABLE servidor ADD email. Depois o RH cadastra 200 e-mails.'),('Consequência','O ALTER mudou o esquema uma vez. Os 200 cadastros mudaram só a instância, 200 vezes.')],[('ALTER TABLE','Muda o esquema'),('Cadastro de e-mail','Muda a instância'),('Estrutura da tabela','Esquema (molde)')]),
 ('Esquema é a descrição lógica das tabelas, colunas e domínios.','Instância é a organização lógica dos dados com atributos e domínios.','Instância é a foto do conteúdo; o molde é o esquema.'),
 ('Qual a diferença entre esquema e instância, em uma frase cada?','Esquema: estrutura e restrições, muda raramente. Instância: dados de agora, muda a cada operação.','Explique por que um INSERT não altera o esquema.','Porque o INSERT só coloca conteúdo dentro do molde que já existe. Mudar o molde exigiria um comando de definição.','Molde × conteúdo.','baixa')))
x=get('tce-ac-2024-c06-gestao-dados',69)
P.append(bloco('3. Chaves e integridade referencial',
 '<p>Como saber que duas linhas são a mesma coisa? Cada tabela tem uma <b>chave primária (PK)</b>: valor único e obrigatório que identifica a linha, como o CPF identifica uma pessoa. Outra tabela aponta para ela com uma <b>chave estrangeira (FK)</b>, como um recibo que escreve o CPF do dono.</p>'+F.f_pkfk()
 +'<p><b>Integridade referencial</b>: todo valor de FK existe como PK da tabela referenciada (ou é nulo, se permitido). Se alguém apagar o fornecedor 1, o banco recusa, ou apaga junto, conforme a regra definida (restrict ou cascade).</p>'
 +banca(x,'Definição literal: FK corresponde a valor existente na PK referenciada.'),
 ('Pode haver duas linhas com a mesma PK na mesma tabela? E duas com a mesma FK? Aposte.','PK repetida, não (identifica a linha). FK repetida, sim: vários contratos podem apontar para o mesmo fornecedor.'),
 ('O contrato sem fornecedor (Ministério fictício)',[('Problema','A tabela contrato tem id_fornecedor. Alguém apagou o fornecedor 9, que ainda tinha 4 contratos.'),('Decisão','Sem FK, o banco aceita e os 4 contratos ficam órfãos. Com FK declarada, o banco bloqueia o DELETE.'),('Consequência','Relatórios de auditoria mostram contratos sem fornecedor, e ninguém sabe a quem cobrar a entrega.')],[('Contrato órfão','Violação da integridade referencial'),('FK declarada','Restrição que impede o órfão'),('id_fornecedor','Chave estrangeira apontando para a PK')]),
 ('A FK aceita apenas valores que existem na PK da tabela referenciada.','A FK aceita qualquer valor, desde que o tipo de dado seja igual ao da PK.','Tipo igual não basta: o valor precisa existir na tabela pai.'),
 ('Qual a diferença entre PK e FK quanto a repetição de valores?','PK é única na sua tabela; FK pode repetir (lado "muitos").','Por que declarar a FK no banco e não só na aplicação?','Porque o banco garante a regra para qualquer programa que o acesse, inclusive scripts e cargas manuais.','Quem aponta é a FK; quem é apontada é a PK.','média')))
x=get('funpresp-2021-c10',112)
P.append(bloco('4. Relacionamento N:N e tabela associativa',
 '<p>Um auditor participa de várias auditorias e cada auditoria tem vários auditores. Em modelo entidade-relacionamento isso é <b>N:N</b>. Mas uma coluna só guarda um valor: não dá para pôr uma lista de auditorias dentro da linha do auditor sem quebrar a 1FN. A solução é uma <b>tabela associativa</b> no meio.</p>'+F.f_nn()
 +'<p>Resumo de conversão: 1:N coloca a FK no lado N; N:N cria tabela nova com as duas FKs (juntas formam a PK); 1:1 coloca a FK em um dos lados.</p>'
 +banca(x,'Definição literal: N:N origina tabela associativa no modelo físico.'),
 ('Quantas tabelas físicas aparecem para um relacionamento N:N entre duas entidades? Aposte.','Três: as duas entidades e a tabela associativa.'),
 ('Equipes de auditoria (CGU fictícia)',[('Problema','Cada auditoria da CGU envolve várias auditoras, e cada auditora atua em várias auditorias no ano.'),('Decisão','O analista tenta pôr "auditorias" como lista dentro da linha da auditora. A consulta "quem atuou na auditoria 12?" vira busca em texto.'),('Consequência','Criou-se a tabela equipe(id_auditora, id_auditoria). Cada linha diz "esta pessoa atuou nesta auditoria", e a consulta virou um join simples.')],[('Auditora','Entidade A'),('Auditoria','Entidade B'),('Tabela equipe','Tabela associativa (duas FKs, PK composta)')]),
 ('O relacionamento N:N gera uma tabela associativa com duas chaves estrangeiras.','O relacionamento N:N é resolvido colocando uma coluna de lista na tabela de uma das entidades.','Lista numa célula viola a 1FN.'),
 ('Como se resolve um N:N no modelo físico?','Cria-se uma tabela associativa; as duas FKs juntas costumam formar a PK.','Por que não basta uma FK em um dos lados?','Porque com N:N cada linha teria de apontar para vários valores, e uma célula guarda um valor só.','N:N sempre vira tabela nova.','baixa')))
x1=get('mpo-2024-cg-bloco-comum',86);x2=get('seplag-ce-2024-x',40);x3=get('petrobras-ns-2021-c06',53)
P.append(bloco('5. Normalização: 1FN, 2FN e 3FN',
 '<p><b>Normalizar</b> é reorganizar as tabelas para que cada fato seja guardado <b>em um só lugar</b>. Ideia intuitiva: se o endereço de um fornecedor aparece em 500 linhas e ele muda de endereço, você corrige 500 vezes e erra algumas. Normalizar evita essa <i>redundância</i> e as <b>anomalias</b> de inserção, alteração e exclusão.</p>'+F.f_formas()
 +'<p><b>Dedução em passos.</b> (1) Célula com "Ana, Bruno" no campo equipe: lista dentro da célula, viola a 1FN. (2) Tabela com chave (id_pedido, id_item) e coluna nome_item, que depende só do id_item: dependência parcial, viola a 2FN. (3) Tabela licitação com quantidade, preço e valor_total = quantidade × preço: valor_total depende de atributos não-chave, dependência transitiva, viola a 3FN.</p>'
 +banca(x1,'Normalização de esquema confundida com escalonamento de valores (0 a 1).')+banca(x2,'Normalização reduz redundância; o item diz aumentar.')+banca(x3,'Definição literal de 3FN (não-chave depende só da chave).')
 +'<p><b>Caso TCE-AC 2024, item 65 (no caderno):</b> o campo calculado valor_total fica na tabela e a banca diz que está em 3FN. Está errado: ele é derivado de colunas não-chave.</p>',
 ('Uma tabela guarda código do município e nome do município em toda linha de gasto. Qual forma normal ela viola? Aposte.','3FN: o nome depende do código do município (atributo não-chave), não da chave da linha de gasto.'),
 ('O município repetido (Controladoria fictícia)',[('Problema','A tabela gasto_saude repete "Manaus" e "AM" em milhares de linhas.'),('Decisão','O nome de Manaus muda de grafia numa carga. Parte das linhas fica com a grafia antiga.'),('Consequência','Relatório por município soma duas vezes a mesma cidade. A correção é criar a tabela municipio e deixar só o código em gasto_saude.')],[('Nome repetido','Redundância'),('Grafia diferente','Anomalia de alteração'),('Tabela municipio','Resultado da normalização (3FN)')]),
 ('Normalizar reduz a redundância e organiza dados em tabelas relacionadas.','Normalizar é converter valores para uma escala entre 0 e 1.','Normalização de esquema não é normalização estatística.'),
 ('O que cada forma normal proíbe: 1FN, 2FN e 3FN?','1FN: valor não atômico/grupo repetido. 2FN: dependência parcial da chave composta. 3FN: dependência transitiva entre não-chaves.','Por que valor_total = quantidade × preço viola a 3FN?','Porque depende de colunas não-chave, que já determinam o valor. Guardá-lo duplica informação e pode ficar inconsistente.','Chave, chave toda, só a chave.','alta')))
x=get('funpresp-exe-2024-c08',74)
P.append(bloco('6. Normalização na prática: o outro lado',
 '<p>Normalizar muito tem custo: uma consulta que precisava de 1 tabela passa a juntar (JOIN) 8. Em relatórios pesados isso pode ficar lento. Por isso existe a <b>desnormalização</b>: duplicar dados de propósito para ganhar leitura, aceitando o custo de manter a cópia coerente.</p>'
 +tabela(['','Mais normalizado','Mais desnormalizado'],[['Redundância','Baixa','Alta'],['Escrita/atualização','Simples e segura','Mais cara, risco de inconsistência'],['Leitura/relatório','Mais JOINs','Menos JOINs, mais rápida'],['Uso típico','Sistemas transacionais','Consultas analíticas, relatórios']])
 +banca(x,'"Deve ser sempre evitada" é palavra absoluta; o problema real existe, mas o dever não é absoluto.'),
 ('Um relatório mensal faz JOIN de 8 tabelas e demora 40 s. Duplicar uma coluna na tabela principal é sempre errado? Aposte.','Não. É uma decisão consciente (desnormalização) com custo de manter a consistência.'),
 ('O painel lento (Tribunal fictício)',[('Problema','O painel de gastos de um tribunal junta 8 tabelas e demora 40 segundos.'),('Decisão','A equipe cria uma tabela resumo atualizada à noite. O sistema de lançamentos continua normalizado.'),('Consequência','O painel responde em 2 segundos. Há atraso de um dia nos números, aceito conscientemente.')],[('Tabela resumo','Desnormalização'),('Sistema de lançamentos','Esquema normalizado'),('Atraso de um dia','Custo da redundância')]),
 ('A normalização excessiva pode prejudicar consultas complexas, e a desnormalização pode ser uma escolha justificada.','A normalização excessiva deve ser sempre evitada.','"Sempre" e "nunca" são sinais de alerta na prova.'),
 ('Cite um ganho e um custo de desnormalizar.','Ganho: menos JOINs e leitura mais rápida. Custo: redundância e risco de inconsistência.','Por que "sempre evitar" está errado?','Porque normalizar é a regra para dados transacionais; evitar sempre ignoraria o projeto que pesa vantagens e custos.','Pergunta: o que o item pede, regra ou decisão de projeto?','média')))
x1=get('petrobras-ns-2021-c05',108);x2=get('mp-to-servidor-2024-c01',67)
P.append(bloco('7. Transações e propriedades ACID',
 '<p>Uma <b>transação</b> é um grupo de operações tratado como uma unidade. Exemplo: transferir R$ 100 da conta A para a B são dois UPDATEs. Se o primeiro roda e o segundo falha, o dinheiro some. A transação evita isso com as quatro propriedades ACID.</p>'+F.f_acid()
 +tabela(['Letra','Propriedade','Pergunta que responde'],[['A','Atomicidade','Tudo foi feito ou nada foi feito?'],['C','Consistência','As regras (chaves, restrições) continuam valendo?'],['I','Isolamento','Uma transação interfere em outra em andamento?'],['D','Durabilidade','Depois do commit, sobrevive a uma queda?']])
 +banca(x1,'Definição literal de atomicidade (tudo ou nada).')+banca(x2,'A sigla é Atomicidade, não "autenticidade".'),
 ('Na transferência, o débito rodou e o crédito falhou. Qual propriedade manda desfazer o débito? Aposte.','Atomicidade: a transação inteira é revertida (rollback).'),
 ('A transferência interrompida (Fundo fictício)',[('Problema','O sistema do fundo debita R$ 100 da conta A e cai antes de creditar a conta B.'),('Decisão','Como as duas operações estavam na mesma transação, o banco desfaz o débito ao reiniciar.'),('Consequência','A conta A volta ao saldo original. Sem transação, R$ 100 teriam desaparecido.')],[('Débito + crédito','Uma transação'),('Desfazer o débito','Atomicidade (rollback)'),('Saldo volta ao correto','Consistência preservada')]),
 ('A atomicidade garante que todas as operações da transação sejam refletidas ou nenhuma delas.','A atomicidade garante que transações simultâneas não se enxerguem.','Isso é isolamento, não atomicidade.'),
 ('Diga o que cada letra de ACID protege, em uma frase.','A: tudo ou nada. C: estado válido para estado válido. I: concorrência sem interferência. D: confirmado sobrevive a falha.','Por que a transação é necessária na transferência bancária?','Porque são dois UPDATEs que precisam acontecer juntos; separados, uma falha entre eles perde dinheiro.','Troca de palavra na sigla = pegadinha clássica.','baixa')))
x1=get('bdmg-2024-c02',73);x2=get('pc-df-adm-2024',67)
P.append(bloco('8. Log de transações, commit e rollback',
 '<p>Como o banco cumpre atomicidade e durabilidade se pode cair a qualquer momento? Ele anota tudo num <b>log de transações</b> antes de mexer nos dados (o princípio WAL, write-ahead logging). Depois da queda, lê o log e arruma.</p>'+F.f_log()
 +tabela(['Operação','O que faz','Aplica-se a'],[['REDO (refazer)','Reaplica as mudanças','Transações confirmadas cujos dados podem não ter ido ao disco'],['UNDO (desfazer) / rollback','Desfaz as mudanças','Transações não confirmadas']])
 +banca(x1,'Commit pressupõe log suficiente para refazer após falha (durabilidade).')+banca(x2,'Rollback desfaz as não confirmadas; as confirmadas são refeitas, não desfeitas.'),
 ('Após uma queda, o banco desfaz as transações confirmadas, as não confirmadas ou ambas? Aposte.','Desfaz só as não confirmadas; as confirmadas são refeitas se necessário.'),
 ('A queda de energia (Datacenter fictício)',[('Problema','Faltou luz no datacenter do órgão no meio da atualização de 10 mil cadastros. Uma transação já tinha commit; outra, não.'),('Decisão','Ao subir, o banco lê o log: refaz a que tinha commit e desfaz a outra.'),('Consequência','O cadastro volta consistente: nenhuma alteração pela metade e nenhuma confirmada perdida.')],[('Transação com commit','Candidata a REDO'),('Transação sem commit','Candidata a UNDO (rollback)'),('Log gravado antes','Write-ahead logging')]),
 ('No rollback, o SGBD desfaz as transações não confirmadas.','No rollback, o SGBD desfaz todas as transações, confirmadas ou não.','Desfazer confirmadas contradiz a durabilidade.'),
 ('O que o commit promete e como o log ajuda?','Promete durabilidade: o log tem informação suficiente para refazer a transação após falha.','Por que o log é gravado antes dos dados?','Para que, se a queda ocorrer entre as duas gravações, ainda haja registro do que refazer ou desfazer.','C = refaz; sem C = desfaz.','alta')))
x1=get('sefin-fortaleza-ce-2023',129);x2=get('cnj-2024-c02',62)
P.append(bloco('9. Concorrência: locks, isolamento e deadlock',
 '<p>Vários usuários mexem no mesmo dado ao mesmo tempo. Sem controle, um lê o valor que o outro está a meio caminho de mudar. O banco usa <b>bloqueios (locks)</b> para organizar a fila. Isso é <b>isolamento</b>, a letra I.</p>'
 +'<p><b>Deadlock</b>: T1 segura A e quer B; T2 segura B e quer A. Ninguém avança. SGBDs como o PostgreSQL detectam o ciclo e abortam uma das transações, e não dá para prever qual.</p>'+F.f_dead()
 +banca(x1,'Locks garantem isolamento, não atomicidade (trocou a letra do ACID).')+banca(x2,'O PostgreSQL detecta o deadlock e aborta uma transação (tratamento automático).'),
 ('Dois servidores editam o mesmo cadastro ao mesmo tempo. Quem evita que um sobrescreva o outro às cegas? Aposte.','O controle de concorrência (locks): é isolamento.'),
 ('A fila no mesmo cadastro (Autarquia fictícia)',[('Problema','Duas analistas atualizam o limite do mesmo contrato ao mesmo tempo.'),('Decisão','A primeira obtém o lock da linha. A segunda espera até o commit da primeira.'),('Consequência','Nenhuma sobrescreve a outra sem ver. Se cada uma segurasse uma linha e pedisse a da outra, haveria deadlock e o banco abortaria uma delas.')],[('Lock da linha','Mecanismo de isolamento'),('Espera da segunda analista','Serialização do acesso'),('Uma segura A e quer B, a outra B e quer A','Deadlock')]),
 ('Bloqueios (locks) servem ao isolamento entre transações concorrentes.','Bloqueios (locks) têm o objetivo de garantir a atomicidade.','Atomicidade é tudo ou nada (log/rollback); lock é isolamento.'),
 ('Que letra do ACID os locks protegem? E o que é deadlock?','Isolamento. Deadlock: transações em ciclo de espera por recursos uma da outra.','Como o banco resolve um deadlock?','Detecta o ciclo e aborta uma das transações, liberando seus locks para a outra seguir.','Lock = Isolamento.','média')))
x=get('stm-2025-c03',66)
P.append(bloco('10. Stored procedures',
 '<p>Uma <b>stored procedure</b> é um bloco de código guardado dentro do banco (em PL/SQL, PL/pgSQL, T-SQL) e chamado pelo nome. Pense numa receita pendurada na cozinha: em vez de ditar cada passo por telefone, você diz "faça a receita 7". Menos conversa, menos tráfego.</p>'+F.f_proc()
 +'<ul><li><b>Vantagens:</b> menos tráfego de rede, plano de execução já preparado, regra centralizada, permissão por procedimento.</li><li><b>Custos:</b> lógica de negócio presa ao fornecedor do banco, teste e versionamento mais difíceis.</li><li><b>Gatilho (trigger), termo-ponte:</b> código que o banco dispara sozinho quando ocorre um INSERT/UPDATE/DELETE; a procedure, ao contrário, é chamada por quem quer.</li></ul>'
 +banca(x,'Definição conforme literatura: pré-compiladas, menos tráfego, melhor desempenho.'),
 ('Uma regra de cálculo precisa de 3 consultas e 2 gravações. Onde ela gera menos tráfego de rede: na aplicação ou numa procedure? Aposte.','Na procedure: tudo roda no banco com uma só chamada.'),
 ('O fechamento mensal (Prefeitura fictícia)',[('Problema','O fechamento mensal executa 5 passos que, pela aplicação, geram 5 idas e vindas à rede.'),('Decisão','A equipe cria a procedure fechar_mes(mes) e a aplicação chama uma vez.'),('Consequência','O fechamento cai de 12 s para 3 s. Em compensação, o código fica preso ao SGBD escolhido.')],[('fechar_mes(mes)','Stored procedure'),('Uma só chamada','Redução de tráfego'),('Preso ao SGBD','Custo/dependência de fornecedor')]),
 ('A stored procedure é armazenada no banco e pode reduzir o tráfego de rede.','A stored procedure roda na aplicação e aumenta o tráfego de rede.','Quem roda "dentro do banco" é a procedure.'),
 ('Cite uma vantagem e um custo das stored procedures.','Vantagem: menos tráfego e desempenho. Custo: dependência do SGBD e versionamento mais difícil.','Qual a diferença entre procedure e trigger?','Procedure é chamada explicitamente; trigger é disparada automaticamente por um evento de dados.','Procedure: eu chamo. Trigger: o evento chama.','baixa')))
P.append('<div class="pg">\n<h2>11. Como a banca cobra e a técnica Certo/Errado</h2>'
 +tabela(['Padrão da pegadinha','Exemplo desta aula','Como reagir'],[
 ['Troca de termo na sigla','ACID com "autenticidade"','Reconstrua a sigla de cabeça'],
 ['Troca de propriedade','Locks "garantem atomicidade"','Lock = isolamento; log = atomicidade/durabilidade'],
 ['Troca de conceito parecido','Normalização = escala 0 a 1','Normalização de esquema ≠ de valores'],
 ['Inversão','Normalização "aumenta" a redundância','Pergunte: o sentido do verbo está certo?'],
 ['Absoluto','"Deve ser sempre evitada"','Procure a exceção'],
 ['Esquema × instância','Instância = organização lógica','Esquema = molde; instância = conteúdo']])
 +'<div class="box ok"><b class="t">Quando arriscar</b>Se o item errado desconta o mesmo que o certo ganha, o palpite cego tem valor esperado zero. Só vale marcar quando você consegue apontar o termo trocado, ou quando tem mais de 50% de confiança. Item com “sempre/nunca/apenas” e conceito que você não domina: deixe em branco. Se a dúvida é de redação e você reconhece o conceito, arrisque.</div>'
 +'<div class="box"><b class="t">Dividir o item em partes</b>Leia: sujeito (o que é?), verbo (faz o quê?), complemento (para quê?). A pegadinha costuma estar em uma só dessas três partes. Em "locks têm o objetivo de garantir a atomicidade", sujeito e verbo estão certos; o erro está no complemento.</div></div>\n')
P.append('<div class="pg">\n<h2>12. Resumo de revisão</h2><ul>'
 +''.join('<li>%s</li>'%s for s in [
 '<b>Esquema</b> = molde (estrutura, muda pouco). <b>Instância</b> = conteúdo de agora.',
 '<b>PK</b>: única e obrigatória. <b>FK</b>: pode repetir e precisa existir na PK da tabela pai (integridade referencial).',
 '<b>N:N</b> vira tabela associativa com duas FKs.',
 '<b>1FN</b>: atômico. <b>2FN</b>: sem dependência parcial. <b>3FN</b>: sem dependência transitiva. Normalizar reduz redundância; não é escala 0–1.',
 '<b>Desnormalizar</b> é decisão de projeto (leitura mais rápida, custo de consistência). “Sempre evitar” é absoluto.',
 '<b>ACID</b>: Atomicidade, Consistência, Isolamento, Durabilidade. A não é “autenticidade”.',
 '<b>Log (WAL)</b> antes dos dados. <b>Commit</b> confirmado: REDO. <b>Sem commit</b>: UNDO/rollback.',
 '<b>Locks</b> = isolamento. <b>Deadlock</b> = ciclo de espera; o SGBD aborta uma.',
 '<b>Stored procedure</b>: pré-compilada no banco, menos tráfego; trigger dispara sozinho.'])+'</ul></div>\n')
Q=[('petrobras-ns-2021-c05',108,'Transações / ACID','Atomicidade'),('mp-to-servidor-2024-c01',67,'Transações / ACID','Sigla ACID'),('sefin-fortaleza-ce-2023',129,'Concorrência','Locks e isolamento'),('mpo-2024-cg-bloco-comum',86,'Modelagem relacional','Normalização de esquema'),('seplag-ce-2024-x',40,'Modelagem relacional','Normalização e redundância'),('funpresp-exe-2024-c08',74,'Modelagem relacional','Normalização excessiva'),('tce-ac-2024-c06-gestao-dados',65,'Modelagem relacional','3FN e campo derivado'),('funpresp-2021-c10',112,'Modelagem relacional','N:N e tabela associativa'),('bdmg-2024-c02',73,'Transações / ACID','Commit e log'),('pc-df-adm-2024',67,'Transações / ACID','Rollback e recuperação')]
GC={
 ('petrobras-ns-2021-c05',108):'Definição literal de atomicidade: ou todas as operações são refletidas, ou nenhuma.',
 ('mp-to-servidor-2024-c01',67):'A sigla ACID é Atomicidade, Consistência, Isolamento e Durabilidade. “Autenticidade” é troca de termo.',
 ('sefin-fortaleza-ce-2023',129):'Locks controlam concorrência, ou seja, isolamento. Atomicidade é garantida por log e rollback.',
 ('mpo-2024-cg-bloco-comum',86):'Normalização de banco organiza tabelas para reduzir redundância; escala de 0 a 1 é normalização de valores.',
 ('seplag-ce-2024-x',40):'Normalização busca reduzir a redundância (não aumentar) e proteger a integridade; efeitos sobre desempenho existem.',
 ('funpresp-exe-2024-c08',74):'O risco de desempenho existe, mas “deve ser sempre evitada” é absoluto: desnormalizar é decisão de projeto.',
 ('tce-ac-2024-c06-gestao-dados',65):'valor_total é calculado a partir de colunas não-chave: dependência transitiva e redundância. Viola a 3FN.',
 ('funpresp-2021-c10',112):'Relacionamento N:N no modelo físico vira tabela associativa com as chaves das duas entidades.',
 ('bdmg-2024-c02',73):'Commit pressupõe log suficiente para refazer as atualizações após falha (durabilidade, REDO).',
 ('pc-df-adm-2024',67):'O rollback desfaz só as não confirmadas; as confirmadas permanecem (e podem ser refeitas via log).'}
P.append('<div class="pg">\n<h2>13. Caderno de questões – Aula 1</h2><p class="small">10 itens reais do Cebraspe. Julgue Certo ou Errado antes de ver o gabarito. Cada item traz o link da prova oficial.</p>')
for n,(pre,it,t,st) in enumerate(Q,1):
    x=get(pre,it)
    P.append('<div class="box"><b class="t">Questão %d</b><p>%s</p><p><span class="tag">%s</span><span class="tag">%s</span><span class="tag">P3 · Dados 1</span><span class="tag">%s</span></p><p class="small">%s · item %s · <a href="%s">fonte oficial</a></p></div>'%(n,e(txtq(x)),e(t),e(st),e(str(nv(x))),e(x['ref']),e(str(x['item'])),e(x['url'])))
P.append('</div>\n<div class="pg">\n<h2>14. Gabarito comentado</h2>')
for n,(pre,it,t,st) in enumerate(Q,1):
    x=get(pre,it);g=x['gabarito']
    P.append('<div class="box %s"><b class="t">Questão %d: %s</b><p>%s</p></div>'%('ok' if g=='C' else 'warn',n,'CERTO' if g=='C' else 'ERRADO',e(GC[(pre,it)])))
P.append('</div>\n')
(D/'corpo.html').write_text('\n'.join(P),encoding='utf-8')
(D/'manifest.json').write_text(json.dumps({'tema':'P3·DADOS 1','aula':1,'versao':1,'didatica_v2':True,'titulo':'Aula 1 – Modelagem relacional, normalização, transações e ACID (P3·DADOS 1)','origem':'engenharia-reversa','data':'2026-11-08','caderno':['%s#%s'%(get(p,i)['prova_id'],i) for p,i,_,_ in Q]},ensure_ascii=False,indent=1),encoding='utf-8')
print('ok',len(P))
