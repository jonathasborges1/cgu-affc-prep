---
name: gerar-aula
description: Gera uma micro-aula (HTML dark do zero + caderno de até 10 itens reais) para um tema do edital CGU/AFFC a partir do plano de núcleos e do banco; consulta o cache antes.
---
# Gerar micro-aula
1. `python scripts/aula.py status "<tema>"` – se EM DIA, não regenere; informe o caminho. Se DESATUALIZADA, atualize só o caderno.
2. Leia o plano (`aulas/<tema>/plano-real/plano.json`) e escolha a micro-aula pedida (≤5 núcleos).
3. Para cada núcleo, leia os itens do banco (`concursos/<ativo>/banco.jsonl`) e escreva em `aulas/<tema>/aulaN/corpo.html`: objetivo e mapa; explicação do zero com analogia; exemplos crescentes; "como a banca cobra" (Certo, Errado, pegadinha do tipo da taxonomia); resumo de revisão. Use as classes de `aulas/_template/dark.css`. Não invente questões.
4. Caderno: só itens do banco, ≤10, não usados no ledger; cada um com tags, nível, referência (banca, órgão, cargo, ano), URL da fonte e gabarito comentado.
5. Grave `manifest.json` e registre: `python scripts/aula.py registrar aulas/<tema>/aulaN --tema "<tema>" --aula N --versao 1 --titulo "..." --nucleos ... --itens prova:item,...`.
6. PDF: `python scripts/render_aula.py aulas/<tema>/aulaN` (requer playwright).
