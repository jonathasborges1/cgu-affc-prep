"""Componentes pedagogicos (v4). Cada bloco conceitual usa: previsao, parabola, exemplo_contra, checagem.
As respostas ficam em <details> (recolhidas no app; o render do PDF abre todas)."""
from html import escape as e
def previsao(q,a):
    return '<div class="ped ped-prev"><b class="t">🎯 Antes de ler: faça a sua aposta</b><p>%s</p><details><summary>Ver a resposta (só depois de apostar)</summary><p>%s</p></details></div>'%(e(q),e(a))
def parabola(titulo,cena,mapa):
    c=''.join('<p class="cena"><i>%s.</i> %s</p>'%(e(r),e(t)) for r,t in cena)
    m=''.join('<tr><td>%s</td><td>%s</td></tr>'%(e(h),e(k)) for h,k in mapa)
    return '<div class="ped ped-par"><b class="t">📖 Cenário no setor público: %s</b>%s<table><tr><th>Na história</th><th>No conceito formal</th></tr>%s</table></div>'%(e(titulo),c,m)
def exemplo_contra(certo,errado,porque):
    return '<div class="ped ped-ec"><b class="t">✔ Exemplo × ✘ Contraexemplo</b><p><span class="cert">Certo:</span> %s</p><p><span class="err">Errado:</span> %s</p><p class="dica">%s</p></div>'%(e(certo),e(errado),e(porque))
def checagem(q,a,explique,modelo,dica=None,ajuda='média'):
    d='<p class="dica">Dica: %s</p>'%e(dica) if dica else ''
    return ('<div class="ped ped-chk"><b class="t">🧠 Recupere sem olhar o texto <span class="ajuda">ajuda: %s</span></b><p>%s</p>%s'
            '<details><summary>Conferir</summary><p>%s</p></details>'
            '<p style="margin-top:2mm"><b>Explique com suas palavras.</b> %s</p>'
            '<details><summary>Ver uma resposta-modelo</summary><p>%s</p></details></div>')%(e(ajuda),e(q),d,e(a),e(explique),e(modelo))

def retomada(titulo,intro,ca,cb,linhas,certo,errado,dica):
    """Retomada: volta a um bloco anterior quando o segundo termo do contraste so foi ensinado agora."""
    r=''.join('<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>'%(e(a),e(x),e(y)) for a,x,y in linhas)
    return ('<div class="ped ped-ret"><b class="t">🔁 Retomada do Bloco C: %s</b><p>%s</p><table><tr><th></th><th>%s</th><th>%s</th></tr>%s</table>'
            '<p><span class="cert">Certo:</span> %s</p><p><span class="err">Errado:</span> %s</p><p class="dica">%s</p></div>')%(e(titulo),e(intro),e(ca),e(cb),r,e(certo),e(errado),e(dica))
