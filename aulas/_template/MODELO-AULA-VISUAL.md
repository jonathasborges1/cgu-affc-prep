# Modelo visual de aula (v3)

Regra: toda aula nova tem **pelo menos 1 figura original por bloco** e o texto só vem depois que o leitor "viu" a ideia.

## Roteiro didático obrigatório por bloco

1. **Cenário/parábola curta**: personagem ou órgão → problema → decisão → consequência.
2. **Tradução**: diga explicitamente o que cada elemento representa no conceito técnico.
3. **Previsão**: peça ao aluno que decida ou explique antes de revelar a regra.
4. **Formalização**: apresente a norma, definição, fórmula ou classificação.
5. **Contraste de banca**: Certo × Errado e a pegadinha provável.
6. **Recuperação ativa**: uma pergunta sem consulta, com resposta curta recolhida em `<details>`.

Marcação obrigatória no HTML: o cenário usa `data-didatica="cenario"` ou classe `ped-par`; a pausa usa `data-didatica="recuperacao"` ou classe `ped-chk`. O `manifest.json` recebe `"didatica_v2": true` para ativar o gate do renderizador.

## Qual figura para qual conteúdo (helpers em `aulas/_template/visuais.py`)
| Conteúdo | Figura |
|---|---|
| Sequência / tramitação | linha de caixas com setas (`box` + `seta`) |
| Ciclo ou período no tempo | faixas coloridas sobre uma linha do tempo |
| Regra com condições (se… então…) | fluxograma com `losango` e caixa final "faltou passo" |
| Tipos parecidos que a banca troca | 3 cards lado a lado: quando / instrumento / recursos / vigência |
| Hierarquia (A contém B) | caixas encadeadas + exemplo concreto |
| Espectro (mais/menos) | régua com faixas e setas |
| Técnica de prova | raio-X do item (partes, palavra absoluta, veredito) + 4 detectores |
| Decisão sob incerteza | régua de confiança com saldo esperado |
| Fechamento da aula | mapa mental de 1 página |

## Regras
- Figuras são **desenhadas por nós** (SVG inline, paleta `C`). Não embutir imagens da web (direitos autorais); fontes consultadas entram só como texto.
- Cada figura tem legenda `fig(svg, legenda, titulo)`, com a pegadinha da banca quando houver.
- Contraste alto no tema escuro, texto ≥ 9 pt, nada fora da caixa: conferir cada figura em PNG antes de entregar.
- Gerar via `figuras.py` na pasta da aula (idempotente, marcadores `<!--FIG:nome-->`), nunca colar SVG à mão no corpo.
- Âncoras: a figura entra imediatamente antes do cabeçalho que a usa.
- Depois de gerar: renderizar PDF, olhar páginas das figuras, subir `manifest.versao`.
- O caderno interativo não muda com as figuras (casa itens pelo enunciado).
