---
name: coleta-questoes-concurso
description: Use ao coletar provas e itens do Cebraspe para o banco local, somente pelo CDN oficial, respeitando ritmo e parada.
---
# Coleta de questões (somente CDN oficial do Cebraspe)
Não use TEC Concursos nem outro site que proíba robôs/IA/automação. Não inspecione APIs deles.

Fluxo (scripts do projeto, nesta ordem):
1. `python scripts/descobrir.py catalogo` – lista eventos do CDN (cache em descoberta/).
2. `python scripts/descobrir.py ranquear` – pontua provas por compatibilidade com o edital.
3. `python scripts/descobrir.py varrer --tempo 150 --max-provas 10 --alvo-total 6000 --ganho-min 0` – baixa PDFs, extrai itens, filtra por edital.
4. `python scripts/descobrir.py dedupe` – remove repetidos.
5. `python scripts/descobrir.py tema "<seção>" --id <lote>` e `pacote <lote>` – prepara o lote para classificação.

Regras: pausa entre requisições, parar em erro 403/429, sem paralelismo agressivo, registrar em logs/execucao.log. Itens sem gabarito oficial ou com extração duvidosa vão para dúvida e não entram no banco.
