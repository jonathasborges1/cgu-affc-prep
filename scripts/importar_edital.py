#!/usr/bin/env python3
"""Importa o programa (objetos de avaliação) de um edital Cebraspe em PDF para concursos/<id>/programa.json e programa.md.
Uso:  python3 scripts/importar_edital.py EDITAL.pdf --cargo 4 --saida concursos/cgu-affc-ti-ds
Roda local, sem créditos. Layout testado: Edital 1/2026 CGU-AFFC (itens 15.2.2, 15.2.3 e programa por cargo)."""
import re,sys,json,subprocess,argparse,os
P_MAP=[('ESTADO','P1','ESTADO'),('SOCIEDADE','P1','SOC'),('ÉTICA','P1','ETICA'),('ADMINISTRAÇÃO','P1','ADM'),
 ('GOVERNANÇA','P2','GOV'),('TRANSPARÊNCIA','P2','TRANSP'),('DIREITO','P2','DIR'),('EVIDÊNCIAS','P2','EVID'),('AUDITORIA','P2','AUD'),
 ('ENGENHARIA','P3','ENG'),('ARQUITETURA','P3','ARQ'),('PERSISTÊNCIA','P3','DADOS'),('DESENVOLVIMENTO SEGURO','P3','SEG')]
UP='A-ZÁÉÍÓÚÂÊÔÃÕÇ'
def blocos(txt):
    t=re.sub(r'\s+',' ',txt)
    ms=list(re.finditer(r'(?<![%s])([%s][%s ,\-–]{8,}): (?=\d)'%(UP,UP,UP),t))
    out=[]
    for i,m in enumerate(ms):
        fim=ms[i+1].start() if i+1<len(ms) else len(t)
        out.append((m.group(1).strip(),t[m.end():fim].strip()))
    return out
def proximos(L):
    p=L.split('.'); c=[L+'.1']
    for k in range(len(p),0,-1):
        q=p[:k]; q[-1]=str(int(q[-1])+1); c.append('.'.join(q))
    return c
def itens(corpo):
    res=[]; esp=['1']; pos=0; atual=None; ini=0
    for m in re.finditer(r'(?<!\S)(\d+(?:\.\d+){0,3})\.? (?=[%s])'%UP,corpo):
        n=m.group(1)
        if n in esp:
            if atual: res.append((atual,corpo[ini:m.start()].strip()))
            atual=n; ini=m.end(); esp=proximos(n)
    if atual: res.append((atual,corpo[ini:].strip()))
    return res
def main():
    a=argparse.ArgumentParser(); a.add_argument('pdf'); a.add_argument('--cargo',type=int,required=True); a.add_argument('--saida',required=True); r=a.parse_args()
    txt=subprocess.run(['pdftotext','-layout',r.pdf,'-'],capture_output=True,text=True,check=True).stdout.splitlines()
    i15=next(i for i,l in enumerate(txt) if re.match(r'^15 DOS OBJETOS',l))
    ib=next(i for i in range(i15,len(txt)) if '15.2.2 CONHECIMENTOS BÁSICOS' in txt[i])
    ic=next(i for i in range(ib,len(txt)) if '15.2.3 CONHECIMENTOS COMPLEMENTARES' in txt[i])
    ic1=next(i for i in range(ic,len(txt)) if re.match(r'^CARGO 1:',txt[i]))
    ie=next(i for i in range(ic1,len(txt)) if re.match(r'^CARGO %d:'%r.cargo,txt[i]))
    fim=next(i for i in range(ie+1,len(txt)) if re.match(r'^\s*ANEXO I\b|^CARGO \d:',txt[i]))
    cab=' '.join(txt[ie:ie+3]).strip()
    # pula o cabeçalho do cargo (até a linha que termina o nome da especialidade)
    k=ie+1
    while k<fim and not re.search(r':\s*\d',txt[k]) and not re.match(r'^[%s ,\-–]+: '%UP,txt[k]): k+=1
    regs=[('P1',txt[ib+1:ic]),('P2',txt[ic+1:ic1]),('P3',txt[k:fim])]
    out=[]; resumo=[]
    for prova,ls in regs:
        for titulo,corpo in blocos('\n'.join(ls)):
            cod=next((c for chave,pv,c in P_MAP if pv==prova and chave in titulo),None)
            if not cod: cod=re.sub(r'[^A-Z]','',titulo)[:5]
            its=itens(corpo)
            for num,tx in its:
                out.append({'codigo':'%s·%s %s'%(prova,cod,num),'prova':prova,'bloco':cod,'bloco_titulo':titulo,'num':num,'nivel':num.count('.')+1,'texto':tx})
            resumo.append((prova,cod,titulo,len([1 for n,_ in its if '.' not in n]),len(its)))
    os.makedirs(r.saida,exist_ok=True)
    with open(os.path.join(r.saida,'programa.json'),'w',encoding='utf-8') as f:
        for d in out: f.write(json.dumps(d,ensure_ascii=False)+'\n')
    with open(os.path.join(r.saida,'programa.md'),'w',encoding='utf-8') as f:
        f.write('# Programa do edital (fonte da verdade)\n\nCargo: %s\nGerado por scripts/importar_edital.py a partir do PDF oficial (item 15 do edital). Códigos no formato `PROVA·BLOCO n.m`.\n'%cab)
        cur=None
        for d in out:
            if d['bloco_titulo']!=cur:
                cur=d['bloco_titulo']; f.write('\n## %s·%s – %s\n\n'%(d['prova'],d['bloco'],cur.capitalize()))
            f.write('%s- **%s** %s\n'%('  '*(d['nivel']-1),d['num'],d['texto']))
    for p,c,t,top,tot in resumo: print('%s·%-6s grupos=%d itens=%d  %s'%(p,c,top,tot,t[:60]))
    print('total itens:',len(out))
main()
