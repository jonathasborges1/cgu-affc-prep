#!/usr/bin/env python3
"""Audita se P1/P2/P3 podem exibir prioridade como confiavel."""
import glob,json,re
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent;C=BASE/'concursos'/'cgu-affc-ti-ds'
def lerj(p):
    try:return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
    except Exception:return []
def ler_json(p):
    try:return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:return {}
def main():
    out={'criterios':{'rotulos_por_assunto':30,'estabilidade_faixas_fixas_minima':.80,
         'temporal_recencia_ponderado_minimo':.85,'pior_periodo_recente_minimo':.70,
         'margem_maxima_amostra_cauda_90':.04},'blocos':{}}
    ordem=ler_json(BASE/'docs'/'confianca-ordem.json')
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
        if b=='P1':
            confiavel=True
        else:
            ev=ordem.get(b,{}) if isinstance(ordem,dict) else {}
            faixa=ev.get('faixas') or {};temp=ev.get('temporal') or {};am=ev.get('amostragem_probabilistica') or {}
            gates={'amostra_completa':bool((detalhe.get('gates') or {}).get('amostra_completa')),
              'sem_duplicados':bool((detalhe.get('gates') or {}).get('sem_duplicados')),
              'estabilidade_faixas_fixas_0_80':float(faixa.get('fracao') or 0)>=.80,
              'temporal_recencia_ponderado_0_85':float(temp.get('razao_recencia_ponderada') or 0)>=.85,
              'pior_periodo_recente_0_70':temp.get('pior_fold_recente') is not None and float(temp['pior_fold_recente'])>=.70,
              'amostragem_probabilistica_aprovada':bool(am.get('aprovada') and am.get('sem_imputacao_modelo'))}
            detalhe['gates_ordem']=gates
            detalhe['precisao_triagem_informativa']=detalhe.get('precisao_triagem_parcial')
            confiavel=all(gates.values())
        out['blocos'][b]={'amostra':len(mapa),'rotulados':len(rot),'assuntos':len(assuntos),'assuntos_completos':completos,
          'pacotes':len(glob.glob(str(C/'pacotes'/(pref+'-*.md')))),'confiavel':confiavel,
          'motivo':('calibracao e backtest concluidos; ordem exata apenas nas posicoes firmes' if b=='P1' else
                    ('todos os gates de calibracao e backtest foram aprovados' if confiavel else
                     'classificacao cega em andamento; prioridade permanece bloqueada ate todos os gates passarem')),
          **detalhe}
    dest=BASE/'docs'/'confiabilidade-blocos.json';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
