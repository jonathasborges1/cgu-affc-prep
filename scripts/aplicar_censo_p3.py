#!/usr/bin/env python3
"""Aplica o censo assistido por ML (docs/censo-ml-p3.json) a ordem de P3 usada pelo app.
Faz backup (docs/_bak_pre_censo/), atualiza docs/precisao-triagem-p3.json (part/faixa/rank/ordem por assunto), docs/recall-triagem-p3.json
(ordem_com_oculto, recall, ocultas) e docs/confianca-ordem.json['P3'] (testes contados com os numeros novos)."""
import json,os,shutil
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));D=B+'/docs/'
os.makedirs(D+'_bak_pre_censo',exist_ok=True)
for f in ('precisao-triagem-p3.json','recall-triagem-p3.json','confianca-ordem.json'):
    if not os.path.exists(D+'_bak_pre_censo/'+f):shutil.copy(D+f,D+'_bak_pre_censo/'+f)
c=json.load(open(D+'censo-ml-p3.json'));P=json.load(open(D+'precisao-triagem-p3.json'));R=json.load(open(D+'recall-triagem-p3.json'))
acum=0
for i,x in enumerate(c['ordem'],1):
    a=x['assunto']
    if a in P:
        P[a].update({'part':x['part'],'part_ic':x['ic90'],'ordem':i,'acum':round(acum+x['part'],4),'faixa':x['faixa'],'firme':x['rank_ic90'][0]==x['rank_ic90'][1],'rank':[x['rank_ic90'][0],round((x['rank_ic90'][0]+x['rank_ic90'][1])/2),x['rank_ic90'][1]],'estab_faixa':x['estab_faixa'],'fonte_part':'censo-ml'})
    acum+=x['part']
R.update({'ordem_com_oculto':[x['assunto'] for x in c['ordem']],'recall_estimado':c['recall_conhecidas'],'p3_oculto_estimado':c['ocultas_p3'][1],'p3_oculto_ic90':[c['ocultas_p3'][0],c['ocultas_p3'][2]],'fonte':'censo-ml (docs/censo-ml-p3.json)'})
json.dump(P,open(D+'precisao-triagem-p3.json','w'),ensure_ascii=False,indent=1);json.dump(R,open(D+'recall-triagem-p3.json','w'),ensure_ascii=False,indent=1)
v=c['v2'];C=json.load(open(D+'confianca-ordem.json'))
C['P3']={'versao':2,'recall_leitura':c['recall_localizado'],
 'recall_obs':'parte das P3 conhecidas (pool da triagem + itens lidos no topo da fila e nos sorteios) sobre o total estimado; as escondidas nao lidas vem de modelo local calibrado em amostra estratificada (docs/censo-ml-p3.json). Aceite sem leitura so se o modelo tiver precisao>=90% (limite inferior) na amostra.',
 'amostras':c['conhecidas'],'faixas':v['faixas'],'faixas_acum':v['faixas_acum'],'temporal':v['temporal'],'temporal_loyo':v['temporal_loyo'],'conjunto80':v['conjunto80'],'aceite_modelo':c.get('aceite_modelo')}
json.dump(C,open(D+'confianca-ordem.json','w'),ensure_ascii=False,indent=1)
print('ok recall',C['P3']['recall_leitura'],'faixas',v['faixas']['estaveis'],'/',v['faixas']['relevantes'],'temporal',v['temporal']['razao_ponderada'],v['temporal']['pior_fold'])
