# cgu-bd: banco local de questões CGU/AFFC (v4)

Comece por `ORQUESTRACAO.md` (roteiro) e `docs/ARQUIVOS.md` (mapa de formatos e locais).

- `concursos/<id>/`: **um concurso por pasta** (concurso.json com o cargo-alvo, edital-oficial.pdf, programa.json/.md, regras-da-prova.md) e os dados dele: `banco.jsonl`, `nucleos.jsonl`, `provas.jsonl`, `classificacoes/`. O ativo está em `concursos/ativo.txt`.
- `provas/` e `extraidos/`: PDFs e itens extraídos, compartilhados entre concursos.
- `banco.py`: único programa. Não editar os .jsonl à mão (só Python 3).
- `scripts/importar_edital.py`: importa o programa de um edital Cebraspe em PDF para `programa.json`.
- `edital-topicos.md` (índice resumido; a fonte da verdade é `concursos/<ativo>/programa.md`) e `taxonomia-pegadinhas.md` (etiquetas de pegadinha).
- `docs/tec/tec-cadernos.json`, `docs/tec/plano-filtros-tec.md`: cadernos já criados no TEC e filtros planejados (consultar antes de criar outro).
- `skills/`, `agentes/`: instruções para o Claude e para os agentes.
- `docs/`: manuais (workflow, portabilidade, regras do Projeto) e `PANORAMA-CGU-BD.pdf` (gerado por `docs/gerar_panorama.py`; atualizar a cada mudança).
- `referencia/`: documentos históricos do Projeto.

Provas: `python3 banco.py prova add ...` e depois `prova processar ID` (baixa PDFs para `provas/ID/`, extrai texto e itens, tudo local).

Uso: `python3 banco.py stats` · `python3 banco.py search "oauth" --limit 5` · `python3 banco.py rank --edital "P3·ENG 2"` · `python3 banco.py prova proxima`

Importação exige: banca, ano, ref, url, url_gab, item, enunciado, gabarito (C/E), tema. Sem referência real e gabarito oficial, o item é rejeitado.
