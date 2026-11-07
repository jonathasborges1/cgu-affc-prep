"""Verificador de ordem de termos: nenhum termo tecnico pode aparecer antes do bloco que o define.
Uso: python3 ordem_termos.py <pasta-da-aula>   (le corpo.html e termos.json da aula)
termos.json: {"isentas":["1","11","12","13","14"],"termos":[{"nome":"credito adicional","pat":"regex","def":7}]}
Excecoes: secoes isentas (mapa, revisao, caderno) e termos-ponte (<span class="ponte">...</span>), que trazem mini-definicao inline."""
import re,json,sys
from pathlib import Path
def verificar(pasta,mostrar=True):
    D=Path(pasta);s=(D/'corpo.html').read_text(encoding='utf-8');cfg=json.loads((D/'termos.json').read_text(encoding='utf-8'))
    s=re.sub(r'<span class="ponte"[^>]*>.*?</span>','',s,flags=re.S)
    hs=list(re.finditer(r'<h2[^>]*>(\d+)\. ',s));achados=[]
    for i,h in enumerate(hs):
        n=h.group(1)
        if n in cfg.get('isentas',[]): continue
        corpo=s[h.start():hs[i+1].start() if i+1<len(hs) else len(s)]
        txt=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',corpo))
        for t in cfg['termos']:
            if int(n)<int(t['def']):
                for m in re.finditer(t['pat'],txt,flags=re.I):
                    achados.append((n,t['nome'],t['def'],txt[max(0,m.start()-45):m.end()+45]))
    if mostrar:
        for n,t,d,c in achados: print('secao %s usa "%s" (definido na %s): ...%s...'%(n,t,d,c))
        print('termos usados antes de definidos:',len(achados))
    return achados
if __name__=='__main__': verificar(sys.argv[1])
