# Método de coleta de provas oficiais do Cebraspe via Chrome (testado em 02/11/2026)

## Resultado do teste
Com o Claude in Chrome, a coleta melhora muito: dá para ler o texto dos PDFs oficiais (prova e gabarito definitivo) e conferir cada item pelo número. Sem o Chrome (WebSearch/WebFetch), o conteúdo vinha parafraseado ou truncado, e o shell não alcança o CDN.

## Passo a passo
1. Selecionar o navegador (havia 2 Chromes conectados; foi usado o "Browser 2").
2. Abrir `https://www.cebraspe.org.br/concursos/<SLUG>` (ex.: MPO_24, SEFAZ_CE_21) e usar `find` com o nome do link ("PROVA OBJETIVA - CARGO 4") para obter o `href` do PDF.
3. Abrir uma página 404 do CDN (`https://cdn.cebraspe.org.br/concursos/<SLUG>/arquivos/x_nao_existe.txt`) para ter um contexto de JavaScript na mesma origem. No viewer de PDF nativo e na página www o `javascript_tool` falha ou trava.
4. Nessa página, carregar pdf.js (jsdelivr, pdfjs-dist 3.11.174), fazer `fetch` do PDF e extrair o texto. O gabarito definitivo vem como linhas "61 62 ... / E C E ..." e dá para mapear por posição.
5. Procurar por palavras-chave (segregação, linhas de defesa, agente de contratação, fiscal, ETP...) e cruzar item × gabarito.

## Padrões de nome de arquivo (úteis para varrer em lote)
- MPO 2024: `958_MPO_ANALISTA_CG1_01.PDF`, `958_MPO_ANALISTA_00N_01.PDF` (N = cargo 1 a 8) e gabarito `GAB_DEFINITIVO_<mesmo nome>.PDF`.
- SEFAZ-CE 2021: prova `MATRIZ_598_SEFAZ_00N.PDF`; gabarito `GAB_DEFINITIVO_MATRIZ_598_SEFAZ_00N_00_PAG_5.PDF` (nome irregular, pegar pelo link da página).
- Cada concurso tem seu padrão; sempre confirmar pelo link na página do concurso.

## Limites encontrados
- O `javascript_tool` falhou na página www ("Cannot access a chrome-extension URL") e houve travamento de screenshot; o contorno foi usar `find`/`get_page_text` na página e rodar o JS na página 404 do CDN.
- A lista de PDFs da página www é montada dinamicamente; o HTML bruto não traz os links.
- Itens com texto colado a outros itens exigem checar o trecho antes de usar.

## Achados desta coleta (todos com gabarito definitivo oficial)
- MPO 2024, Conhecimentos Gerais: item 29 (vinculação ao edital obriga ambos) = C; item 30 ("Um dos princípios básicos de licitações é a segregação de funções") = C.
- MPO 2024, Cargo 7 (Gestão de Contratos de TI): item 94 (requisitante e área técnica no ETP não podem ser cumulados, "sob pena" de ofensa à segregação) = E; item 58 (assessoria jurídica e controle interno do órgão como 3ª linha de defesa) = E. Esta prova é a melhor prova-espelho achada para o bloco 5 da P3 (contratação e fiscalização).
- SEFAZ-CE 2021, Cargo 4 (Auditor Fiscal de TI): item 99 (segregação de funções, conceito) = C.
