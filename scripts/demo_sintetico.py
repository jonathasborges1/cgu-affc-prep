#!/usr/bin/env python3
"""Gera um banco SIMULADO (500 itens fictícios) para demonstrar aula.py plano/relatorio. Uso: python3 demo_sintetico.py DIR"""
import json,random,sys
from pathlib import Path
random.seed(7)
d=Path(sys.argv[1]); d.mkdir(parents=True,exist_ok=True)
conceitos=['CSRF','XSS','SQL injection','LDAP injection','DDoS','SSRF','XXE','IDOR','JWT','OAuth 2.0','CORS','CSP','TLS','SAST','DAST','SCA','WAF','Fuzzing','Hardening','MFA','Gestão de segredos','Log e monitoramento','Controle de acesso','Desserialização']
aspectos=['definição','defesa','troca de pilar (CIA)']
nucs=[]
for c in conceitos:
    for a in aspectos: nucs.append((c,a))
nucs=nucs[:70]
codigos=['P3·SEG 1.1']*30+['P3·SEG 1.2']*14+['P3·SEG 1.3']*8+['P3·SEG 1.4']*10+['P3·SEG 1.6']*8
tags=['INVERSAO','ABSOLUTO','TROCA_TERMO','ESCOPO','CAUSA_CONSEQUENCIA','EXCECAO_OMITIDA','NORMA_LITERAL','CONCEITO_MISTURADO','PARTE_CERTA_PARTE_ERRADA']
pesos=[1/(i+1)**0.9 for i in range(70)]; tot=sum(pesos); alvo=[max(1,round(500*p/tot)) for p in pesos]
while sum(alvo)>500: alvo[alvo.index(max(alvo))]-=1
while sum(alvo)<500: alvo[0]+=1
provas=['SIM-ORGAO-A-%d'%i for i in range(1,16)]
itens=[];nid=[]
for i,((c,a),n) in enumerate(zip(nucs,alvo)):
    nuc='n-sim-%02d-%s'%(i+1,c.lower().replace(' ','-').replace('.','')) ; texto='%s: %s (ideia simulada %d)'%(c,a,i+1); nid.append({'id':nuc,'texto':texto,'edital':codigos[i]})
    for j in range(n):
        gab=random.choice('CE'); tg=[] if gab=='C' and random.random()<.7 else random.sample(tags,random.choice([1,1,2]))
        niv=random.choice(['facil','medio','medio','dificil']); pr=random.choice(provas)
        itens.append({'prova_id':pr,'banca':'Cebraspe','ref':'[SIMULADO] Cebraspe %s %d'%(pr,random.randint(2016,2025)),'ano':random.randint(2016,2025),'url':'https://exemplo.invalid/sim/%s.pdf'%pr,'url_gab':'https://exemplo.invalid/sim/GAB_%s.pdf'%pr,'item':random.randint(1,120),'enunciado':'[SIMULADO] Afirmação %d sobre %s – aspecto: %s.'%(j+1,c,a),'gabarito':gab,'nivel':niv,'tags':tg,'padrao':('Padrão simulado: '+tg[0].lower().replace('_',' ')) if tg else 'Definição correta (simulado).','edital':codigos[i],'nucleos':[nuc]})
(d/'banco.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in itens),encoding='utf-8')
(d/'nucleos.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in nid),encoding='utf-8')
print(len(itens),'itens simulados,',len(nid),'núcleos')
