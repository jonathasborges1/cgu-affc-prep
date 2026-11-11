# Fluxo: tema alvo → banco local → padrão Cebraspe → aula

(Versão v3 do fluxo, mantida como referência. O fluxo atual está em `ORQUESTRACAO.md` e `docs/workflow-v2.md`; o banco.py atual é o v4.)

Objetivo: não consultar TEC/Cebraspe de forma repetida. Tudo que for coletado vai para o banco local; as aulas consultam o banco primeiro.

## Onde fica o banco
- Banco principal, no PC do Jonathas: `C:\Users\jonathas.000\Documents\provas\CGU-AFFC-Auditor-Fiscal-Financas-Controle\cgu-bd\`.
- Acesso: pelo app desktop, com a pasta conectada à sessão (aparece em `$HOME/mnt/jonathas.000/...` no device_bash). Só funciona com o app aberto e o PC ligado.
- SQLite NÃO pode ficar nessa pasta ("disk I/O error"). O banco.py reconstrói um índice FTS5 temporário (pasta temporária da máquina, ou `BANCO_DB`) a cada execução, a partir do JSONL.
- Gravar na pasta pelo device_bash: `device_commit_files` não sobrescreve arquivo existente de forma confiável. Método que funciona: commitar com outro nome (ex.: `_stage_x`) e depois `cp -f` para o destino; alternativa: `echo <base64> | base64 -d > arquivo`. Apagar exige `device_request_delete_permission`.

## Comandos do banco.py v3 (o v4 acrescenta nucleo, prova, comparar, aplicar, rank, verificar-caderno; ver ORQUESTRACAO.md)
`search "termo" [--banca --ano --tema --limit --sem-padrao]`, `stats`, `add-json arq.jsonl` (valida campos obrigatórios, gabarito C/E, ignora duplicadas por url+item+enunciado), `set-padrao ID "texto" --tags TAG1,TAG2` (tags da taxonomia), `mostrar ID`.
Campos: fonte, banca, orgao, cargo, ano, ref, url, url_gab, item, enunciado, gabarito, comentario, tema, subtema, nivel, edital, padrao, tags.

## Estado do banco em 04/11/2026
- 75 itens: 10 de PPA/LDO/LOA (com padrão e tags), 32 do TCE-RN 2026 e 33 do TCU 2026 (oficiais, sem nivel/comentário/padrão ainda).
- Ainda não importados: TCE-AC 2024, MPO 2024 (docs do Projeto) e itens do TCU truncados.
- TEC: caderno 107753370 (620 itens PPA/LDO/LOA, não resolvidos) lido até ~525; sessão ainda sob 429 no último teste.

## Passo a passo para um tema novo
1. Buscar no banco (`search`). Se houver pelo menos ~20 itens do tema, não ir às plataformas.
2. Se faltar: Cebraspe primeiro (PDFs oficiais no CDN, gabarito definitivo, ver `metodo-coleta-cebraspe-chrome.md`), depois TEC.
3. No TEC: um filtro por tema, nome `CGU-AAAA-MM-Bloco-Tema`; conferir `docs/tec/tec-cadernos.json` antes de criar; preferir "não resolvidas".
4. Gravar cada item no banco com gabarito conferido (url_gab).
5. Ler os itens do tema e preencher `padrao` + `tags` (taxonomia de pegadinhas) com `set-padrao`.
6. Montar a aula de trás para frente: pegadinhas e pontos mais cobrados definem a ênfase; depois analogia, dedução e figuras.
7. Caderno final: no máximo 10 itens, um link por item, gabarito comentado.

## Regras do TEC
Ver `heuristicas-coleta-tec-concursos.md` (ler antes de qualquer consulta). Os números de ritmo ali (8 s, 30 itens, 2 h) são hipóteses prudentes, não limites confirmados do TEC; os termos de uso ainda não foram lidos.
