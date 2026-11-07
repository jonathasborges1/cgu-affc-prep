# Protocolo pedagógico de aula (v4)

Além do modelo visual (`MODELO-AULA-VISUAL.md`), todo BLOCO CONCEITUAL da aula segue esta sequência. É gate: aula sem ela não está pronta.

| # | Etapa | Componente (`aulas/_template/pedagogia.py`) | Onde |
|---|---|---|---|
| 1 | Aposta (previsão) antes da explicação; resposta recolhida | `previsao(q, a)` | logo após o título do bloco |
| 2 | Analogia cotidiana curta | texto do bloco ("Ideia intuitiva") | início |
| 3 | Cenário no setor público: personagem/órgão + problema → decisão → consequência | `parabola(titulo, cena, mapa)` | fim do bloco |
| 4 | Tabela "na história × no conceito formal" | dentro de `parabola` | fim |
| 5 | Exemplo correto + contraexemplo (item Certo × item Errado) | `exemplo_contra(certo, errado, porque)` | fim |
| 6 | Pegadinha real da banca (tag da taxonomia) | caixa "Pegadinha" do bloco + `porque` | durante/fim |
| 7 | Recuperação sem olhar o texto + autoexplicação com resposta-modelo | `checagem(q, a, explique, modelo, dica, ajuda)` | fim |

## Regras
- Cenário usa órgão do setor público (prefeitura, ministério, tribunal, autarquia) com nome fictício; nunca só analogia familiar. Fatos legais citados com artigo.
- Redução gradual da ajuda: `ajuda` = alta (com dica) nos primeiros blocos, média, baixa, nenhuma nos últimos (sem dica).
- Respostas ficam em `<details>` (recolhidas no app). `scripts/render_aula.py` abre todas para o PDF.
- Cenário e checagem não repetem item do caderno; o caderno continua sendo a última etapa.
- Aula com mais de ~8 blocos: dividir em microaulas (o limite do fluxo é ≤5 núcleos).
- Gerar sempre por script idempotente (`figuras.py` + `blocos.py`): `python3 blocos.py` roda as figuras e depois o protocolo.
- Pendente (próximas melhorias do app): revisão espaçada integrada à aula e aula adaptada aos erros individuais.

## Glossário de siglas (tooltip)
- O app mostra, ao passar o mouse (ou tocar) em qualquer sigla, o nome completo e uma definição curta. Vale para texto e para os textos dentro das figuras.
- Fonte: `aulas/_template/glossario.json` (siglas de todo o projeto: orçamento, órgãos, pegadinhas, TI) + `aulas/<aula>/glossario.json` opcional (siglas só daquela aula). Formato: `"SIGLA": {"nome": "...", "def": "..."}`. O arquivo da aula sobrescreve o geral.
- Regra de criação: ao escrever uma aula, toda sigla nova entra no glossário (geral se reaproveitável, da aula se específica). Sigla ambígua traz os dois sentidos ("MP"). Não inventar nome: se não houver certeza, usar descrição genérica.
- O PDF não tem tooltip; siglas importantes devem ser explicadas por extenso na primeira vez que aparecem no texto.

## Palavras-gatilho coloridas
- Palavras como pode, deve, apenas, só, exclusivamente, sempre, nunca ganham cor: **verde** (palavra forte em afirmação Certa), **vermelho** (em afirmação Errada), **amarelo** (cuidado: vale em regra, com exceção ou condição). Uma legenda aparece no início da aula.
- Nunca colorir o caderno de questões (o aluno decide sozinho); o gabarito comentado pode ter cores.
- Colorir só afirmações sobre o conteúdo (norma, regra, item de exemplo); não colorir instruções ("só depois de apostar") nem expressões idiomáticas de analogia.
- Procedimento (`aulas/_template/gatilhos_lib.py`): `listar` gera a lista numerada de ocorrências; classifique cada uma; `gerar` grava `gatilhos.json` da aula; o `blocos.py` chama `gatilhos.aplicar(s)` ao final. Idempotente.

## Regra de ordem dos termos (v5)
Nenhum termo técnico pode aparecer antes do bloco que o define (aluno parte do zero). Quando o contraste envolve dois conceitos de blocos diferentes:
1. No primeiro bloco, use só o que já foi ensinado. Se um termo futuro for inevitável, use **termo-ponte**: `<span class="ponte" title="Adiantado: o Bloco X ensina">termo</span>` com mini-definição visível na mesma frase (o PDF não tem tooltip) e remissão ao bloco.
2. No bloco onde o segundo conceito é ensinado, inclua a caixa **🔁 Retomada** (`pedagogia.retomada(...)`: tabela comparativa + exemplo × contraexemplo + pegadinha com questão real).
3. Cada aula tem `termos.json` (termo, regex, bloco que define). `blocos.py` roda `ordem_termos.verificar(D)` e deve imprimir **0** termos usados antes de definidos (seções isentas: mapa, resumo, caderno, gabarito).
