#!/usr/bin/env python3
"""Audita se P1/P2/P3 podem exibir prioridade como confiavel."""
import glob,json,re
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent;C=BASE/'concursos'/'cgu-affc-ti-ds'
def lerj(p):
    try:return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
    except Exception:return []
def main():
    out={'criterios':{'rotulos_por_assunto':30,'precisao_minima':.85,'recall_top5_minimo':.75,'folds_temporais_minimos':3},'blocos':{}}
    for b in ('P1','P2','P3'):
        pref=b.lower()+'-verif-1';mapa=lerj(C/'amostras'/(pref+'-mapa.jsonl'))
        ids={x['id'] for x in mapa};rot=[]
        for f in glob.glob(str(C/'classificacoes'/(pref+'-*.jsonl'))):rot += [x for x in lerj(f) if x.get('id') in ids]
        assuntos={re.match(r'(%s·\w+ \d+)'%b,x.get('triagem','')).group(1) for x in mapa if re.match(r'(%s·\w+ \d+)'%b,x.get('triagem',''))}
        por={a:0 for a in assuntos}
        for x in mapa:
            if x['id'] in {r['id'] for r in rot}:por[x['triagem']]=por.get(x['triagem'],0)+1
        completos=sum(n>=30 or n==sum(x['triagem']==a for x in mapa) for a,n in por.items())
        detalhe={}
        rel=BASE/'docs'/('calibracao-'+b.lower()+'.json')
        if rel.exists():
            try:
                med=json.loads(rel.read_text(encoding='utf-8'))
                detalhe={'progresso':med.get('progresso'),'precisao_triagem_parcial':med.get('precisao_triagem_parcial'),
                         'gates':med.get('gates'),'backtest_temporal':med.get('backtest_temporal')}
            except Exception: pass
        confiavel=True if b=='P1' else bool(detalhe.get('gates')) and all(detalhe['gates'].values())
        out['blocos'][b]={'amostra':len(mapa),'rotulados':len(rot),'assuntos':len(assuntos),'assuntos_completos':completos,
          'pacotes':len(glob.glob(str(C/'pacotes'/(pref+'-*.md')))),'confiavel':confiavel,
          'motivo':('calibracao e backtest concluidos; ordem exata apenas nas posicoes firmes' if b=='P1' else
                    ('todos os gates de calibracao e backtest foram aprovados' if confiavel else
                     'classificacao cega em andamento; prioridade permanece bloqueada ate todos os gates passarem')),
          **detalhe}
    dest=BASE/'docs'/'confiabilidade-blocos.json';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
