---
name: "priorizacao-temas-banca"
description: "Use para decidir quais temas do edital minerar e estudar primeiro, ranqueando por frequência, recência e compatibilidade das provas anteriores da banca."
---

# Priorização de temas por incidência (CGU/AFFC e similares)

Usar antes de escolher o próximo tema a minerar ou ensinar. Ler no Projeto: `claude/estrategia-mineracao-e-priorizacao.md`, `claude/ranking-compatibilidade-provas.md` e o banco local (`banco.py stats`).

## Fonte primeiro
- Preferir PDFs oficiais no CDN do Cebraspe (prova + gabarito definitivo): 2 arquivos por prova, sem API. Um arquivo por vez, ≥ ~5 s entre downloads, nunca repetir o mesmo PDF, parar no primeiro 429/403.
- Plataformas (TEC, QConcursos) só como apoio e seguindo `coleta-questoes-concurso`.

## Cálculo
score(tópico do edital) = soma, sobre os itens do tópico, de peso_prova × peso_recência.
- peso_recência = 0,5^(idade_em_anos/3).
- peso_prova: vem do ranking de compatibilidade (cargo/área parecidos e formato Certo/Errado pesam mais).
- Ajustar por: número de subitens do tópico no edital e pontos do bloco (P3 vale 2 por item).

## Regras extras
1. Tópico explícito no edital com 0–2 itens históricos é lacuna de risco, não irrelevante: entra em fila própria e se ensina com questões vizinhas (outras bancas só como conteúdo).
2. Tópicos emergentes (só em 2025–2026) sobem.
3. Assertivas quase iguais em provas diferentes formam um núcleo recorrente: bônus.
4. Taxa de acerto baixa (se vier sem custo extra) indica pegadinha; sobe na revisão.
5. Para estudo, descer o que o usuário já domina (Java, APIs) e subir o que é novo; para coleta, seguir o score.
6. Antes de aprofundar um tema, garantir ~20 itens ou esgotar as provas-espelho.
7. Edital é a única verdade do que ensinar; itens sem tópico ficam marcados como fora do edital.