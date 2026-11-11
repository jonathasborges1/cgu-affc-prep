---
name: "classificacao-itens-cebraspe"
description: "Use ao classificar itens Certo/Errado de provas do Cebraspe contra o edital CGU/AFFC: define tópico do edital, núcleo, pegadinha, nível e dúvidas, em JSONL para o banco.py."
---

# Classificação de itens Cebraspe (CGU/AFFC 2026)

Esta skill ensina a transformar um item de prova em um registro classificado do banco local. Quem a aplica é o agente `classificador-itens` (um por prova, em paralelo) ou o próprio Claude, em lotes pequenos.

## Entrada e saída
- **Entrada:** arquivo JSONL com itens já extraídos (campos `banca, orgao, cargo, ano, ref, url, url_gab, item, enunciado, gabarito`) mais três arquivos de apoio: `edital-topicos.md` (códigos do edital), `taxonomia-pegadinhas.md` (etiquetas) e `nucleos.jsonl` (núcleos já existentes, se houver). Ficam em `cgu-bd` no PC e em `claude/` no Projeto.
- **Saída:** um arquivo JSONL com **uma linha por item**, sem texto fora do JSON. Nunca altere `enunciado` nem `gabarito`.

```json
{"item":"51","edital":"P1·ADM 4.1","relevancia":"alta","nucleo_id":"n-ppa-ldo-loa-encadeamento","nucleo_novo":false,"nucleo_texto":"PPA, LDO e LOA são encadeadas: a LDO traduz o PPA em metas anuais e a LOA obedece a ambas","base_legal":"CF art. 165","padrao":"Afirmação geral de encadeamento; sem pegadinha","tags":["NORMA_LITERAL"],"nivel":"Fácil","confianca":"alta","duvida":null}
```

## Passo a passo (nesta ordem)
1. **Ler o item inteiro** e o gabarito. O gabarito vem do arquivo definitivo; se for anulado, alterado entre preliminar e definitivo ou ausente, registre em `duvida` e **não** classifique pegadinha.
2. **Mapear ao edital.** Escolha o código mais específico de `edital-topicos.md` (ex.: `P1·ADM 4.1`). Se o item só faz sentido com conteúdo que o edital não lista, use `FORA`. Se couber em dois tópicos, escolha o que traz o conceito central e cite o outro em `duvida`.
3. **Relevância:** `alta` (o enunciado é o próprio texto do tópico do edital), `media` (é vizinho: mesma base legal ou capítulo), `baixa` (tangencia o tópico), `fora`.
4. **Núcleo.** Núcleo é a **ideia única** que o item testa e que poderia aparecer como Certo ou Errado em outra prova.
   - Primeiro procure em `nucleos.jsonl` um núcleo que já expresse essa ideia. **Reutilize** (`nucleo_novo:false`).
   - Só crie um novo (`nucleo_novo:true`, id em kebab-case começando por `n-`) se nenhum existente servir.
   - Teste de granularidade: "se eu soubesse só esta ideia, acertaria o item?". Se precisar de duas ideias, o item é composto: liste dois núcleos em `nucleo_id` (lista) e marque `PARTE_CERTA_PARTE_ERRADA` se for o caso.
   - Escreva `nucleo_texto` como afirmação **verdadeira** e completa, independente de o item ser C ou E.
5. **Base legal.** Cite apenas o que o próprio enunciado, o comentário ou uma fonte conferida indicam (CF, lei, artigo). Sem certeza, deixe `null`. Não invente número de artigo.
6. **Pegadinha.** Use só as etiquetas de `taxonomia-pegadinhas.md`. Para item Errado, aponte a etiqueta que explica o erro. Para item Certo, use `NORMA_LITERAL` ou deixe sem pegadinha. `padrao` é **uma frase** dizendo o que o item testa e onde está a armadilha.
7. **Nível:** `Fácil` (norma literal, sem absoluto, uma ideia), `Médio` (troca de termo, absoluto ou inversão), `Difícil` (composto, exceção, números, ou depende de norma atualizada). É estimativa; não é dado oficial da banca.
8. **Confiança e dúvida.** `confianca`: `alta`, `media` ou `baixa`. Qualquer coisa que dependa de norma possivelmente alterada (`NORMA_DESATUALIZADA`), de texto cortado na extração ou de gabarito estranho vai em `duvida` com a razão em uma frase.

## Regras que valem sempre
- Não use conhecimento próprio para contradizer o gabarito oficial. Se o gabarito parecer inconsistente com a norma, marque `duvida`; não "corrija".
- Não crie comentário longo nem explicação de aula aqui. A classificação é curta e padronizada.
- Não classifique em lote por semelhança sem ler cada enunciado. Itens quase iguais devem repetir o mesmo `nucleo_id`, e isso é o que se quer.
- Item incompleto (corte de página, tabela quebrada): `confianca:"baixa"` e `duvida:"texto incompleto"`.
- Nunca grave no banco. Quem grava é o `banco.py`, depois da validação.

## Validação antes de devolver
- Todos os itens da entrada aparecem na saída, na mesma ordem, uma vez cada.
- Todo `edital` é um código existente ou `FORA`. Toda etiqueta existe na taxonomia.
- Todo `nucleo_id` reutilizado existe em `nucleos.jsonl`; todo novo tem `nucleo_texto`.
- O JSONL é válido (uma linha, um objeto).