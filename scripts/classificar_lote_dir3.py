#!/usr/bin/env python3
"""Gera a primeira rotulagem humana-assistida do lote oficial P2·DIR 3.
Não aplica ao banco: a etapa seguinte exige verificação independente."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'concursos'/'cgu-affc-ti-ds'/'classificacoes'

MAP1={
1:('P2·DIR 3.1','controle-interno-finalidades',['NORMA_LITERAL']),2:('P2·DIR 3.1','controle-externo-tribunais-contas',['CONCEITO_MISTURADO']),3:('P2·DIR 3.2','controle-jurisdicional-administracao',['CONCEITO_MISTURADO']),4:('P2·DIR 3.1','prestacao-contas-controle',['INVERSAO']),5:('P2·DIR 3.4','controle-externo-sancoes',['NORMA_LITERAL']),6:('P2·DIR 3.1','prestacao-contas-controle',['EXCECAO_OMITIDA']),7:('P2·DIR 3.2','controle-administrativo-peticao',['NORMA_LITERAL']),8:('P2·DIR 3.1','controle-interno-externo-social',['CONCEITO_MISTURADO']),9:('P2·DIR 3.1','controle-interno-finalidades',['NORMA_LITERAL']),10:('P2·DIR 3.1','controle-interno-finalidades',['NORMA_LITERAL']),11:('P2·DIR 3.1','fiscalizacao-lrf-controle',['NORMA_LITERAL']),12:('P2·DIR 3.2','controle-social',['CONCEITO_MISTURADO']),13:('P2·DIR 3.2','controle-social',['TROCA_TERMO']),14:('P2·DIR 3.1','apoio-controle-externo',['NORMA_LITERAL']),15:('P2·DIR 3.1','controle-externo-tribunais-contas',['NORMA_LITERAL']),16:('P2·DIR 3.1','controle-legislativo-executivo',['NORMA_LITERAL']),17:('P2·DIR 3.1','controle-interno-cgu-recursos',['NORMA_LITERAL']),18:('P2·DIR 3.1','controle-externo-tribunais-contas',['NORMA_LITERAL']),19:('P2·DIR 3.1','controle-interno-externo-social',['ABSOLUTO']),20:('P2·DIR 3.3','autonomia-controle-externo',['CONCEITO_MISTURADO']),21:('P2·DIR 3.3','autonomia-controle-externo',['CONCEITO_MISTURADO']),22:('P2·DIR 3.1','controle-interno-finalidades',['EXCECAO_OMITIDA']),23:('P2·DIR 3.3','autonomia-controle-externo',['INVERSAO']),24:('P2·DIR 3.2','auditoria-controle-gestao',['NORMA_LITERAL']),25:('P2·DIR 3.2','controle-gestao-resultados',['NORMA_LITERAL'])}
MAP2={1:('P2·DIR 3.2','controle-social',['NORMA_LITERAL']),2:('P2·DIR 3.1','controle-recursos-publicos',['EXCECAO_OMITIDA']),3:('P2·DIR 3.2','controle-social',['NORMA_LITERAL']),4:('P2·DIR 3.2','controle-social',['CONCEITO_MISTURADO']),5:('P2·DIR 3.3','autonomia-controle-externo',['CONCEITO_MISTURADO']),6:('P2·DIR 3.3','autonomia-controle-externo',['CONCEITO_MISTURADO']),7:('P2·DIR 3.1','sistema-controle-interno-integrado',['INVERSAO']),8:('P2·DIR 3.1','sistema-controle-interno-integrado',['NORMA_LITERAL']),9:('P2·DIR 3.1','controle-interno-finalidades',['EXCECAO_OMITIDA']),10:('P2·DIR 3.1','controle-interno-finalidades',['CONCEITO_MISTURADO']),11:('P2·DIR 3.1','controle-recursos-publicos',['EXCECAO_OMITIDA'])}

def gerar(nome, mapa):
    src=ROOT/'extraidos'/nome
    rows=[json.loads(x) for x in src.read_text(encoding='utf-8').splitlines() if x.strip()]
    out=[]
    for x in rows:
        item=int(x['item']); edital,nuc,tags=mapa[item]
        out.append({'item':str(item),'edital':edital,'nucleo_id':'n-dir3-'+nuc,'nucleo_novo':True,
          'nucleo_texto':nuc.replace('-',' ').capitalize()+'.','base_legal':'CF art. 70 a 74',
          'padrao':'O item explora a distinção e as finalidades dos controles público interno, externo e social.',
          'tags':tags,'nivel':'medio','confianca':'media','duvida':'Rotulagem inicial; aguarda verificação independente.'})
    dest=OUT/nome.replace('tema-p2-','tema-p2-').replace('.jsonl','.jsonl')
    dest.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in out)+'\n',encoding='utf-8')
    return len(out)

if __name__=='__main__':
    print('lote1',gerar('tema-p2-dir-3-1.jsonl',MAP1))
    print('lote2',gerar('tema-p2-dir-3-2.jsonl',MAP2))
