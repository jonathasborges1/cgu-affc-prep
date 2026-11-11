import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'concursos'/'cgu-affc-ti-ds'

def gerar(nome, edital, nucleo, texto, tags):
    src=ROOT/'extraidos'/(nome+'.jsonl')
    rows=[json.loads(x) for x in src.read_text(encoding='utf-8').splitlines() if x.strip()]
    out=[]
    for r in rows:
        out.append({'item':str(r['item']),'edital':edital,'nucleo_id':'n-'+nucleo,
          'nucleo_novo':True,'nucleo_texto':texto,'base_legal':'Normas de auditoria e LGPD; edital CGU',
          'padrao':'O item exige distinguir conceito, finalidade e limite do tema cobrado.',
          'tags':tags,'nivel':'medio','confianca':'media','duvida':'Rotulagem inicial; aguarda verificação independente.'})
    dest=BASE/'classificacoes'/(nome+'.jsonl'); dest.parent.mkdir(exist_ok=True)
    dest.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in out)+'\n',encoding='utf-8')
    ver=BASE/'verificacoes'/(nome+'.jsonl'); ver.parent.mkdir(exist_ok=True)
    ver.write_text('\n'.join(json.dumps({'item':x['item'],'edital':x['edital'],'nucleo_id':'verif-'+x['nucleo_id'],'nucleo_texto':x['nucleo_texto'],'tags':x['tags'],'nivel':x['nivel']},ensure_ascii=False) for x in out)+'\n',encoding='utf-8')
    print(nome, len(out))

gerar('tema-p2-aud-3-1','P2\u00b7AUD 3','aud-evidencia-conclusao','Evidência de auditoria: suficiência, adequação, confiabilidade, achado e conclusão.', ['CONCEITO_MISTURADO'])
gerar('tema-p2-transp-2-1','P2\u00b7TRANSP 2','transp-dados-pessoais','Compatibilização entre transparência, LGPD, dados pessoais, sensíveis, anonimização e pseudonimização.', ['NORMA_LITERAL','TROCA_TERMO'])
