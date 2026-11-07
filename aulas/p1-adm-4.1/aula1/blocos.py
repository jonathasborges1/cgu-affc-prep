#!/usr/bin/env python3
"""Insere (idempotente) o protocolo pedagogico nos blocos A-H da Aula 1. Roda figuras.py antes. Uso: python3 blocos.py"""
import re,sys
from pathlib import Path
D=Path(__file__).resolve().parent; sys.path.insert(0,str(D.parent.parent/'_template')); sys.path.insert(0,str(D))
from pedagogia import *
import figuras
B={}
B['3.']=dict(
 prev=('A LDO traz dois anexos: Metas Fiscais e Riscos Fiscais. Aposte: um "passivo contingente" (dívida que só vira gasto se um fato acontecer, como perder uma ação judicial) entra em qual anexo?',
       'No anexo de Riscos Fiscais (LRF art. 4º, §3º). O anexo de Metas Fiscais traz as metas anuais de receitas, despesas, resultados e dívida.'),
 par=('A receita que não veio (Prefeitura fictícia de Rio Claro)',
  [('Problema','A LDO de Rio Claro fixou uma meta de resultado primário positivo de R$ 20 milhões. No fim do bimestre, a arrecadação ficou abaixo do previsto e a meta está em risco.'),
   ('Decisão','A secretária de Planejamento quer manter todas as obras. O controlador lembra que a própria LDO traz os critérios para limitar o empenho. Em até 30 dias, a prefeitura limita empenho e movimentação financeira nas despesas que podem esperar, seguindo esses critérios.'),
   ('Consequência','A meta é preservada sem corte improvisado, e a folha e a dívida seguem pagas. Se ninguém agisse, a prefeitura descumpriria a regra da LRF e da LDO.')],
  [('Meta de resultado no papel','Anexo de Metas Fiscais da LDO'),('Receita que não veio','Verificação bimestral e limitação de empenho (LRF art. 9º)'),('Regra para escolher o que adiar','Critérios fixados na LDO (LRF art. 4º, I, b)')]),
 ec=('A LDO estabelece critérios e forma de limitação de empenho.','A LOA estabelece os critérios e a forma de limitação de empenho.','Regra do jogo do ano = LDO; lista de valores = LOA. A banca troca a lei (TROCA_TERMO).'),
 chk=('Cite os dois anexos da LDO e diga em qual ficam as metas anuais e em qual ficam os passivos contingentes.',
      'Anexo de Metas Fiscais: metas anuais. Anexo de Riscos Fiscais: passivos contingentes e outros riscos. Trocar os dois é a pegadinha CONCEITO_MISTURADO.',
      'Por que a LDO precisa trazer critérios de limitação de empenho?',
      'Porque, se a receita frustrar a meta, o gestor precisa de uma regra prévia e objetiva para decidir o que adiar, em vez de cortar no improviso.',
      'Meta = onde queremos chegar; risco = o que pode nos desviar.','alta'))
B['4.']=dict(
 prev=('Uma gratificação será criada agora para ser paga todo ano, sem data para acabar. Além de estimar o impacto financeiro e declarar que cabe na LOA, o que mais a LRF exige? Aposte.',
       'Por ser despesa obrigatória de caráter continuado (mais de 2 exercícios), é preciso demonstrar que não afeta as metas fiscais e compensar com aumento permanente de receita ou redução permanente de despesa (LRF art. 17).'),
 par=('A gratificação sem conta (Secretaria de Saúde de Vila Nova)',
  [('Problema','O secretário de Saúde de Vila Nova cria uma gratificação permanente de R$ 3 milhões por ano para a enfermagem, a partir de 2027.'),
   ('Decisão','Ele manda pagar sem estimar o impacto de 2027 a 2029. A controladoria pergunta qual receita nova ou corte permanente sustenta a despesa, e ele responde: a venda de um prédio velho.'),
   ('Consequência','A despesa é considerada não autorizada, irregular e lesiva ao patrimônio público (art. 15). Venda de imóvel é receita pontual e não compensa gasto permanente. O caminho certo: estimar o impacto, declarar a adequação à LOA, ao PPA e à LDO, provar que não afeta as metas e compensar com algo permanente.')],
  [('Gratificação para sempre','Despesa obrigatória de caráter continuado (mais de 2 exercícios)'),('Estimar 2027 a 2029','Impacto no exercício de início e nos 2 seguintes (art. 16, I)'),('Venda do prédio','Receita pontual: não é compensação permanente'),('Pagar sem passos','Despesa não autorizada, irregular e lesiva (art. 15)')]),
 ec=('Compensar com aumento permanente de receita (por exemplo, nova alíquota) ou com redução permanente de despesa.','Compensar com receita pontual obtida durante a execução, como a venda de um imóvel.','O que vale é a permanência: despesa que se repete exige compensação que também se repete (DETALHE_NUMERICO e ABSOLUTO rondam este item).'),
 chk=('Liste os 3 passos da despesa obrigatória continuada e diga o que torna válida uma compensação.',
      '1) Estimativa de impacto no exercício e nos 2 seguintes. 2) Declaração do ordenador: cabe na LOA e é compatível com PPA e LDO. 3) Provar que não afeta as metas e compensar com aumento permanente de receita ou redução permanente de despesa. Compensação válida = permanente.',
      'Por que uma receita pontual não compensa uma despesa que se repete?',
      'Porque a receita entra uma vez e acaba, mas a despesa continua todo ano, abrindo um buraco permanente.',
      'Os passos 1 e 2 valem para toda despesa nova; o 3 é o extra do "continuado".','alta'))
B['5.']=dict(
 prev=('Um deputado quer financiar uma emenda com o dinheiro destinado ao pagamento da dívida pública. Aposte: pode?',
       'Não. A emenda deve indicar recursos de anulação de despesa, e a Constituição exclui pessoal e encargos, serviço da dívida e transferências tributárias constitucionais (CF art. 166, §3º, II).'),
 par=('A emenda sem fonte (Congresso fictício)',
  [('Problema','Um deputado quer R$ 5 milhões para reformar um hospital regional e apresenta emenda ao projeto de LOA.'),
   ('Decisão','Na primeira versão ele indica como fonte o saldo que sobrou em caixa no ano anterior. A comissão aponta o erro: dinheiro novo não serve de fonte para emenda. Na segunda, ele propõe cancelar a dotação de publicidade de um ministério. Também considerou tirar do serviço da dívida, mas desistiu.'),
   ('Consequência','A primeira versão não pode ser aceita, e a segunda cumpre a regra: compatível com PPA e LDO, com fonte em anulação de outra despesa permitida. O dinheiro não nasceu do nada: outra fatia perdeu.')],
  [('Cancelar a publicidade','Anulação de despesa (art. 166, §3º, II, a)'),('Não pode tirar da dívida','Exclusões: pessoal e encargos, serviço da dívida, transferências constitucionais'),('Hospital precisa estar no plano','Compatibilidade com PPA e LDO (art. 166, §3º, I)')]),
 ec=('A emenda indica como fonte a anulação de dotação de outra despesa que não seja pessoal, dívida ou transferências constitucionais.','A emenda indica como fonte o saldo que sobrou em caixa no ano anterior.','Saldo de caixa e receita extra não são fonte de emenda ao projeto de LOA (ESCOPO). Onde eles valem, você vê no Bloco E, e lá este contraste volta.'),
 chk=('Quais são as 3 despesas que não podem ser anuladas para financiar emenda?',
      'Dotações para pessoal e seus encargos, serviço da dívida e transferências tributárias constitucionais para Estados, Municípios e Distrito Federal.',
      'Por que a emenda não pode "criar" dinheiro novo?',
      'Porque a LOA é uma torta fechada: aumentar uma fatia exige tirar de outra, e só de fatias que a Constituição permite anular.',
      'P-D-T: pessoal, dívida, transferências.','média'))
B['6.']=dict(
 prev=('Uma empresa deposita caução para participar de uma licitação. Aposte: esse dinheiro é receita orçamentária?',
       'Não. Entra no caixa, mas não é do governo: será devolvido. É ingresso extraorçamentário.'),
 par=('Duas entradas no caixa (Prefeitura de Rio Claro)',
  [('Problema','Na mesma semana, o caixa de Rio Claro recebeu R$ 2 milhões de IPTU e R$ 500 mil de caução de um licitante.'),
   ('Decisão','O contador quer tratar tudo como receita do mês e liberar R$ 2,5 milhões em gastos. O controlador separa as duas entradas.'),
   ('Consequência','Só os R$ 2 milhões são receita orçamentária. Contar a caução como receita faria a prefeitura gastar um dinheiro que terá de devolver.')],
  [('IPTU','Receita orçamentária corrente, tributária (derivada)'),('Caução','Ingresso extraorçamentário (devolvível)'),('Dinheiro que entra no caixa','Arrecadação, um dos estágios da receita')]),
 ec=('Receita orçamentária é aquela prevista na lei orçamentária anual.','Receita orçamentária é toda entrada de dinheiro no caixa do governo, inclusive cauções.','Entrar no caixa não basta: o que define é a previsão na LOA e o dinheiro ser do ente (ABSOLUTO: "toda").'),
 chk=('Dê um exemplo de receita orçamentária e outro de extraorçamentária. A venda de um imóvel público é receita corrente ou de capital?',
      'Orçamentária: imposto. Extraorçamentária: caução. A venda de imóvel é receita de capital (alienação de bens).',
      'Por que contar a caução como receita seria perigoso?',
      'Porque faria o governo achar que tem dinheiro para gastar quando terá de devolvê-lo.',
      'Pergunte: esse dinheiro é do governo ou está só de passagem?','média'))
B['7.']=dict(
 ret=('emenda ao projeto de LOA × crédito adicional',
  'No Bloco C você viu que a emenda só aceita anular despesa e que o dinheiro "novo" fica de fora. Agora que você conhece o crédito adicional, dá para fechar o contraste: são dois momentos diferentes da vida do orçamento.',
  'Emenda ao projeto de LOA (Bloco C)','Crédito adicional (este bloco)',
  [('Quando','Enquanto o Congresso ainda vota o projeto da LOA','Depois que a LOA foi aprovada e está sendo executada'),
   ('Fontes aceitas (suplementar e especial)','Só anulação de despesa (excluídos pessoal, dívida e transferências)','Superávit financeiro do ano anterior, excesso de arrecadação, anulação de dotações e operações de crédito (Lei 4.320, art. 43)')],
  'Um crédito suplementar aberto com o superávit financeiro do exercício anterior.',
  'Uma emenda ao projeto de LOA que indica o superávit financeiro do exercício anterior como fonte.',
  'É a pegadinha do Bloco C vista do outro lado: a banca pega uma fonte do crédito adicional e a atribui à emenda (ESCOPO). Item real nessa linha: Cebraspe, MPO 2024, cargo 4 (caderno 958_MPO_ANALISTA_004), gabarito Errado. https://cdn.cebraspe.org.br/concursos/MPO_24/arquivos/958_MPO_ANALISTA_004_01.PDF'),
 prev=('Uma enchente destrói pontes e o governo precisa de recursos imediatos que não estão na LOA. Aposte: que crédito adicional e por qual instrumento?',
       'Crédito extraordinário, para despesa urgente e imprevisível (guerra, comoção interna, calamidade pública), aberto por medida provisória na União (CF art. 167, §3º).'),
 par=('Três contas estouradas em um ano (Ministério fictício)',
  [('Problema','O ministério gastou todos os R$ 10 milhões da merenda em setembro (a dotação existe, mas acabou). Em março criou um programa novo sem linha no orçamento. Em junho, uma enchente exigiu socorro imediato.'),
   ('Decisão','Para cada caso ele pede um crédito diferente: reforçar a linha da merenda, abrir uma linha para o programa novo e agir já na enchente.'),
   ('Consequência','Merenda: suplementar, por lei autorizativa, com fonte indicada. Programa novo: especial, por lei específica, com fonte indicada. Enchente: extraordinário, por MP, sem exigir fonte prévia indicada.')],
  [('Reforçar linha existente','Crédito suplementar'),('Criar linha nova','Crédito especial'),('Emergência imprevisível','Crédito extraordinário'),('De onde vem o dinheiro','Lei 4.320, art. 43: superávit financeiro, excesso de arrecadação, anulação de dotações, operações de crédito')]),
 ec=('Crédito especial é aberto para despesa sem dotação orçamentária específica.','Crédito suplementar é aberto para despesas urgentes e imprevisíveis, como as decorrentes de calamidade pública.','Urgência e imprevisibilidade pertencem ao extraordinário; a banca troca o nome do tipo (TROCA_TERMO).'),
 chk=('Complete: suplementar ___, especial ___, extraordinário ___. Cite duas das quatro fontes do art. 43.',
      'Suplementar reforça dotação existente; especial cria dotação nova; extraordinário atende urgência imprevisível. Fontes: superávit financeiro, excesso de arrecadação, anulação de dotações, operações de crédito.',
      'Por que o extraordinário dispensa a espera por uma lei comum?',
      'Porque a emergência não pode esperar o trâmite de uma lei ordinária; a medida provisória permite agir de imediato.',
      None,'baixa'))
B['8.']=dict(
 prev=('O elo entre o PPA e a LOA é o projeto ou o programa? Aposte.',
       'O programa. Projeto é só um dos tipos de ação dentro do programa (os outros são atividade e operação especial).'),
 par=('O plano que não cabia no PPA (Prefeitura de Rio Claro)',
  [('Problema','A Secretaria de Mobilidade aprova um plano setorial com metas duas vezes maiores que as do PPA 2026–2029.'),
   ('Decisão','O dirigente diz que "o plano manda e o PPA se ajusta". O Planejamento responde que planos setoriais devem ser elaborados em consonância com o PPA (CF art. 165, §4º) e propõe duas saídas: reduzir as metas do plano ao PPA ou, se forem essenciais, enviar projeto de lei para alterar o PPA.'),
   ('Consequência','A hierarquia se preserva: o plano se ajusta ao PPA, e não o contrário. Meta sem lastro no PPA ficaria sem programa na LOA e sem dotação.')],
  [('PPA','Lei de médio prazo (4 anos), com programas e metas'),('Plano setorial','Se ajusta ao PPA'),('Mudar o PPA','Exige lei'),('Programa','Elo entre PPA e LOA')]),
 ec=('LOA e PPA se conectam pelos programas; as ações (projeto, atividade, operação especial) detalham cada programa.','A LOA se integra ao PPA por meio dos projetos.','Projeto é só um tipo de ação; o elo é o programa (TROCA_TERMO).'),
 chk=('Ordene da maior para a menor agregação: ação, função, programa, subfunção. Cite os três tipos de ação.',
      'Função → subfunção → programa → ação. Ações: projeto, atividade, operação especial.',
      'Por que um plano setorial não pode "mandar" no PPA?',
      'Porque a Constituição exige que planos setoriais sejam elaborados em consonância com o PPA, que é a lei de médio prazo de toda a administração.',
      None,'baixa'))
B['9.']=dict(
 prev=('Um tribunal federal envia ao Executivo uma proposta orçamentária acima do limite da LDO. Aposte: o Executivo rejeita a proposta ou a ajusta?',
       'Ajusta, para consolidar a proposta única (CF art. 99, §4º). O limite vem da LDO.'),
 par=('O condomínio dos Poderes (União fictícia)',
  [('Problema','Um tribunal federal manda a proposta com valor acima do limite fixado pela LDO.'),
   ('Decisão','O Executivo, que consolida o projeto de lei orçamentária, faz os ajustes necessários para encaixar a proposta nos limites e envia um único projeto ao Congresso.'),
   ('Consequência','O orçamento continua único e consistente com a LDO, em vez de cada Poder impor o seu valor.')],
  [('Limite combinado em assembleia','LDO fixa os limites (CF art. 99, §1º)'),('Síndico consolida as contas','Executivo consolida a proposta única'),('Pedido acima do limite','Ajuste pelo Executivo (art. 99, §4º)')]),
 ec=('O Judiciário elabora sua proposta orçamentária dentro dos limites estipulados na LDO.','A LDO define exclusivamente regras para as despesas do Executivo e do Legislativo.','Palavra absoluta ("exclusivamente") + omissão do Judiciário, do MP e da Defensoria (ABSOLUTO).'),
 chk=('Quem fixa os limites da proposta de cada Poder e quem consolida o projeto? Que outros órgãos também enviam proposta própria?',
      'A LDO fixa os limites e o Executivo consolida. Legislativo, Judiciário, Ministério Público e Defensoria propõem dentro desses limites.',
      'Por que existe um orçamento só, mesmo com vários Poderes?',
      'Porque há uma única lei orçamentária; cada Poder propõe a sua parte, mas o Executivo consolida tudo num projeto só.',
      None,'baixa'))
B['10.']=dict(
 prev=('A LOA pode trazer um artigo autorizando reajuste de salários do funcionalismo? Aposte.',
       'Não. Pelo princípio da exclusividade (CF art. 165, §8º), a LOA trata de previsão de receita e fixação de despesa. Exceções: autorização para créditos suplementares e para operações de crédito, inclusive por antecipação de receita (ARO).'),
 par=('A obra que não saiu (Prefeitura de Rio Claro)',
  [('Problema','A LOA reservou R$ 10 milhões para pavimentar ruas, mas em maio a receita caiu e a meta de resultado ficou em risco.'),
   ('Decisão','O secretário insiste: "está na LOA, é obrigação". O Planejamento aplica a limitação de empenho nas despesas discricionárias, adia a obra e mantém folha e dívida.'),
   ('Consequência','A obra espera. A LOA autoriza o gasto, mas isso não o torna obrigatório em todos os casos: despesas obrigatórias e emendas impositivas têm tratamento diferente.')],
  [('Está na LOA','Caráter autorizativo (com exceções)'),('Adiar a obra','Limitação de empenho em despesa discricionária (LRF art. 9º)'),('Folha e dívida seguem','Despesas obrigatórias não são contingenciadas livremente (art. 9º, §2º)')]),
 ec=('A LOA pode conter autorização para abrir créditos suplementares, exceção ao princípio da exclusividade.','O orçamento é exclusivamente autorizativo, o que permite contingenciar qualquer despesa.','"Exclusivamente" e "qualquer": palavras absolutas que derrubam o item (ABSOLUTO).'),
 chk=('Quais os três orçamentos que compõem a LOA e quais as duas exceções à exclusividade?',
      'Orçamento fiscal, da seguridade social e de investimento das estatais. Exceções: autorização para créditos suplementares e para operações de crédito (inclusive ARO).',
      'Por que "exclusivamente autorizativo" é uma palavra-armadilha?',
      'Porque ignora que há despesas obrigatórias e emendas impositivas que não se cortam livremente; palavra absoluta costuma tornar o item Errado.',
      None,'nenhuma'))
GUIA=('<div class="ped ped-prev"><b class="t">🧭 Como usar cada bloco desta aula</b>'
 '<p>1) <b>Aposte</b> antes de ler. 2) Leia a explicação e a analogia. 3) Veja o <b>cenário no setor público</b> e a tabela que liga a história ao conceito. '
 '4) Compare o <b>exemplo certo e o errado</b>. 5) <b>Recupere sem olhar</b> e explique com suas palavras antes de abrir a resposta. '
 'A ajuda diminui ao longo da aula (alta → nenhuma): nos últimos blocos você responde sem dica.</p><p>Um termo com <span class="ponte">sublinhado pontilhado</span> é adiantado: aparece só como ponte e é ensinado de verdade no bloco indicado. Lá o contraste volta, em uma caixa 🔁 Retomada.</p></div>')
def main():
    figuras.main()
    p=D/'corpo.html';s=p.read_text(encoding='utf-8')
    s=re.sub(r'<!--PED:[\w.]+-->.*?<!--/PED:[\w.]+-->\n?','',s,flags=re.S)
    hs=list(re.finditer(r'<h2>(\d+)\. ',s));pos={}
    for i,m in enumerate(hs): pos[m.group(1)+'.']=(m.start(),m.end(),hs[i+1].start() if i+1<len(hs) else len(s))
    for k in sorted(B,key=lambda x:-int(x[:-1])):
        a,e_,nx=pos[k];b=B[k]
        # fim do bloco: antes do proximo h2 (e do seu pg-break eventual)
        fim=('<!--PED:%sfim-->'%k+exemplo_contra(*b['ec'])+(retomada(*b['ret']) if 'ret' in b else '')+parabola(*b['par'])+checagem(b['chk'][0],b['chk'][1],b['chk'][2],b['chk'][3],b['chk'][4],b['chk'][5])+'<!--/PED:%sfim-->\n'%k)
        s=s[:nx]+fim+s[nx:]
        # previsao: logo apos o fim do </h2>
        h2end=s.index('</h2>',a)+5
        s=s[:h2end]+'<!--PED:%sini-->'%k+previsao(*b['prev'])+'<!--/PED:%sini-->'%k+s[h2end:]
    nx2=pos['2.'][0]
    s=s[:nx2]+'<!--PED:guia-->'+GUIA+'<!--/PED:guia-->\n'+s[nx2:]
    import gatilhos; s=gatilhos.aplicar(s)
    s=re.sub(r'Aula 1 · v\d+','Aula 1 · v7',s,count=1)
    p.write_text(s,encoding='utf-8')
    import ordem_termos;ordem_termos.verificar(D)
    print('protocolo inserido:',len(B),'blocos')
if __name__=='__main__': main()
