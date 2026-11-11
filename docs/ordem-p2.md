# Ordem de prioridade da P2 (versão de 07/11/2026)

Base: amostra cega p2-verif-1 (679 itens, 25 assuntos, 14 pacotes), rotulada em 07/11/2026 por um único rotulador (Claude), sem acesso à previsão da triagem. Itens de provas de 2016 ou antes pesam zero; os demais pesam com meia-vida de 4 anos. Estimador estratificado: cada estrato da triagem é reponderado pela sua massa no acervo e redistribuído pelos assuntos reais rotulados. IC90 por bootstrap (500 reamostragens por estrato).

## Resultado dos gates (docs/calibracao-p2.json)
- Amostra completa: sim. Sem duplicados: sim.
- Precisão da triagem por palavras-chave: 13,3% (90 de 679). Mínimo exigido: 85%. NÃO passou.
- Backtest temporal: 1 fold (mín. 3), recall top-5 de 38% (mín. 75%). NÃO passou.
- Consequência: o app continua marcando a P2 como provisória. Esta ordem é a melhor estimativa com rótulos, não uma ordem calibrada pelos gates do projeto.
- Só 210 dos 679 itens (31%) pertencem de fato ao programa de P2.

## Ordem
| # | Assunto | Parcela estimada | IC90 | Posição (p5–p95) | Faixa |
|---|---|---|---|---|---|
| 1 | P2·DIR 3 | 12.9% | 7.7–19.5% | 1–6 | A |
| 2 | P2·GOV 2 | 12.9% | 7.9–18.6% | 1–5 | A |
| 3 | P2·TRANSP 1 | 8.0% | 4.5–12.2% | 2–10 | B |
| 4 | P2·TRANSP 2 | 7.8% | 4.5–11.9% | 2–10 | B |
| 5 | P2·DIR 1 | 7.7% | 3.2–11.8% | 2–11 | B |
| 6 | P2·AUD 1 | 7.7% | 3.5–12.4% | 2–11 | B |
| 7 | P2·TRANSP 4 | 7.7% | 3.6–11.7% | 2–11 | B |
| 8 | P2·GOV 1 | 6.6% | 4.0–9.4% | 3–10 | B |
| 9 | P2·DIR 4 | 5.2% | 1.8–8.9% | 4–15 | C |
| 10 | P2·AUD 2 | 4.8% | 1.8–8.4% | 4–15 | C |
| 11 | P2·EVID 3 | 3.0% | 1.3–5.1% | 9–17 | C |
| 12 | P2·EVID 5 | 3.0% | 1.2–5.2% | 9–17 | C |
| 13 | P2·AUD 3 | 2.9% | 1.4–5.2% | 9–17 | C |
| 14 | P2·DIR 2 | 2.1% | 0.4–4.1% | 10–19 | D |
| 15 | P2·AUD 4 | 2.0% | 0.7–4.0% | 10–18 | D |
| 16 | P2·EVID 2 | 1.8% | 0.5–3.4% | 11–19 | D |
| 17 | P2·TRANSP 5 | 1.5% | 0.7–2.3% | 13–19 | D |
| 18 | P2·GOV 3 | 1.2% | 0.0–2.4% | 13–24 | D |
| 19 | P2·TRANSP 3 | 0.6% | 0.0–1.2% | 16–24 | D |
| 20 | P2·AUD 5 | 0.2% | 0.0–0.7% | 18–23 | E |
| 21 | P2·EVID 1 | 0.2% | 0.0–0.5% | 19–23 | E |
| 22 | P2·GOV 5 | 0.0% | 0.0–0.0% | 20–22 | E |
| 23 | P2·GOV 4 | 0.0% | 0.0–0.0% | 21–23 | E |
| 24 | P2·EVID 4 | 0.0% | 0.0–0.0% | 23–24 | E |
| 25 | P2·DIR 5 | 0.0% | 0.0–0.0% | 25–25 | E |

## Como ler
- A (DIR 3, GOV 2): firmes no topo; entram em qualquer cenário.
- B (TRANSP 1, TRANSP 2, DIR 1, AUD 1, TRANSP 4, GOV 1): posições 3 a 8 se sobrepõem; tratar como bloco, ordem interna é só desempate.
- C e D: ordem relativa razoável, mas com IC largo.
- E (AUD 5, EVID 1, GOV 4, GOV 5, EVID 4, DIR 5): sem evidência nas provas antigas. O edital de 2026 é novo e lista esses temas; zero no histórico não é zero em 2026. Estudar pela base legal e não montar caderno sem questão real.

## Limites
- Rotulador único; sem revisão independente.
- Recall dos itens descartados pela triagem não foi medido.
- A parcela soma 100% dos itens de P2 recuperados, não dos 40 itens da prova.

## Revisão final (07/11/2026) — com amostra dos descartados

Rotulagem cega de 300 itens descartados pela triagem (ano ≥ 2017, universo 15.946): só 16 eram P2 (5,3%). Estimativa ponderada por recência, combinada com o estrato recuperado (sensibilidade à precisão do recuperado: 7%, 13% e 20%):

| Ordem | Assunto | Share combinado (~) |
|---|---|---|
| 1 | DIR 3 (controle, CGU/TCU) | 24–26% |
| 2 | TRANSP 1 (acesso à informação) | 18–20% |
| 3 | AUD 2 (ciclo, risco/materialidade) | 11–12% |
| 4 | TRANSP 4 (participação, portal) | ~10% |
| 5 | GOV 1 (governança) | ~9–10% |
| 6 | GOV 2 (riscos e controles) | 8–9% |
| 7 | EVID 5 (IA responsável) | 7% |
| 8+ | DIR 1, TRANSP 2, AUD 1, DIR 4, EVID 3 | ≤ 4% cada |

Estável nas duas estimativas: DIR 3, GOV 2 e TRANSP 1 no topo. Subiram com os descartados: AUD 2, TRANSP 4, EVID 5. Caíram: TRANSP 2, AUD 1, DIR 4.
Limites: apenas 16 acertos nos descartados (IC largo); rótulos do próprio avaliador; gates de precisão ≥ 0,85, 3 folds e recall top-5 ≥ 0,75 NÃO passam com a triagem lexical atual. Ordem de trabalho, não certificada.

## Ordem de trabalho fechada (bootstrap 2000x, combinando recuperados + descartados)
Faixa 1 (estudar primeiro): DIR 3 (rank 1–5), TRANSP 1 (1–7)
Faixa 2 (indistinguíveis entre si, estudar em bloco): TRANSP 4, AUD 2, GOV 1, GOV 2 (todos p5–p95 dentro de 1–11)
Faixa 3: EVID 5 (2–16, incerta), DIR 1
Faixa 4: TRANSP 2, AUD 1, DIR 4
Faixa 5: EVID 3, AUD 3, DIR 2, AUD 4, EVID 2 e demais

## Versão final (07/11/2026, v0.0.57) — censo por leitura
Base: 1.939 itens lidos e rotulados (todos os 931 de maior probabilidade do classificador, mais as amostras anteriores) + estimativa por amostra para o restante (100 itens na faixa 0,3–0,6 e 75 abaixo de 0,3). Peso por recência (meia-vida 4 anos; provas ≤ 2016 = 0). Bootstrap de 2000 rodadas.

| # | Assunto | Parcela | Posição (p5–mediana–p95) |
|---|---|---|---|
| 1 | DIR 3 | 18.9% | 1–1–2 |
| 2 | GOV 2 | 18.3% | 1–2–4 |
| 3 | GOV 1 | 11.6% | 2–3–5 |
| 4 | TRANSP 4 | 9.2% | 3–4–7 |
| 5 | DIR 1 | 6.9% | 3–5–11 |
| 6 | TRANSP 1 | 5.9% | 5–6–8 |
| 7 | AUD 1 | 5.8% | 5–6–8 |
| 8 | AUD 2 | 4.7% | 6–8–10 |
| 9 | DIR 4 | 3.5% | 5–10–15 |
| 10 | TRANSP 2 | 3.5% | 8–10–11 |
| 11 | AUD 3 | 3.4% | 8–10–11 |
| 12 | GOV 3 | 2.2% | 10–12–13 |
| 13 | AUD 4 | 1.8% | 11–13–14 |
| 14 | EVID 5 | 1.2% | 13–14–16 |

DIR 3 é firme (1–2). GOV 2, GOV 1 e TRANSP 4 formam o grupo seguinte. Sem evidência no histórico: DIR 5, EVID 4, GOV 4, GOV 5 (estudar pela base legal). Os gates de precisão da triagem por palavras (≥ 85%) seguem sem passar: 13%.
