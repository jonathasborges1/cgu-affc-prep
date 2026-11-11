# Estratégia de mineração e priorização de temas (definida em 04/11/2026)

## 1. Qual fonte é mais leve e mais segura
| Fonte | Requisições por ~100 itens | API pública? | Risco de bloqueio | Veredito |
|---|---|---|---|---|
| PDFs oficiais no CDN do Cebraspe (prova + GAB_DEFINITIVO) | 2 | Não há API, mas são arquivos estáticos públicos | Baixo (robots.txt do www libera tudo; o do CDN não existe) | **Fonte principal** |
| TEC / QConcursos (tela ou rota interna) | 100 (uma por questão) ou ~5 pela impressão do caderno | Não há API pública documentada; rota interna da tela | Alto (já bloqueou em 02–04/11) | Só apoio: achar temas, ler comentário de professor |
| Páginas de listas de provas (PCI Concursos, estudegratis) | 1 por prova | Não | Baixo, mas são só índices de PDFs | Útil para descobrir quais provas existem |

Conclusão: uma prova inteira vem em 2 arquivos. Isso é ~50 vezes menos requisições do que ler questão por questão em plataforma, e é o canal que o próprio Cebraspe usa para divulgar provas e gabaritos. Não existe API oficial de questões.

Cuidados que continuam valendo no CDN: um arquivo por vez, ≥ ~5 s entre downloads, nunca baixar o mesmo PDF duas vezes (cache no banco: url_gab já guardada), parar ao primeiro erro 429/403. Os termos do Cebraspe não foram lidos; uso é pessoal, para estudo, sem republicar as provas.

## 2. Pipeline (poucas requisições, tudo local depois)
1. Lista de provas-alvo = `ranking-compatibilidade-provas.md` (16 provas) + novas que surgirem. Cada uma = 2 PDFs (prova e gabarito definitivo). Total inicial ≈ 32 downloads.
2. Download e extração de texto com pdf.js pelo Chrome (ver `metodo-coleta-cebraspe-chrome.md`), um PDF por vez, gravando no banco logo depois.
3. Parsing local: separar itens por número, ligar ao gabarito por posição, `add-json` (valida e deduplica).
4. Classificar cada item em bloco/tópico do edital e subtema (tema, subtema). Itens sem tópico do edital ficam marcados como "fora do edital".
5. Rodar o ranking (seção 3) e só então decidir o que aprofundar no TEC (comentários) para os temas do topo.

## 3. Heurísticas de prioridade de tema
Pontuação por tópico do edital: **score = Σ (peso_prova × peso_recência) por item** que cai no tópico, ajustada pelos fatores abaixo.
1. **Frequência** (sua ideia): mais itens do tópico nas provas-espelho = mais prioridade.
2. **Recência** (sua ideia): peso_recência = 0,5^(idade_em_anos / 3). Prova de 2026 vale 1,0; de 2023, ~0,5; de 2020, ~0,25. O edital da CGU 2026 é novo e a banca mudou o estilo, então 2025–2026 pesa mais.
3. **Compatibilidade da prova**: peso_prova vem do ranking de compatibilidade (cargo/área parecidos e formato Certo/Errado pesam mais; múltipla escolha pesa menos).
4. **Peso no edital**: cada item de P3 vale 2 pontos; tópicos com mais subitens no edital (ex.: Spring, JPA, OAuth) recebem fator maior. O edital é a única verdade: tópico do edital sem nenhuma questão não é "irrelevante", é **lacuna**.
5. **Lacuna com risco**: tópico explícito no edital e com 0–2 itens históricos (Spring Security, Spring Batch, RAG/agentes) entra numa fila própria: ensinar com questões vizinhas (outras bancas só como conteúdo) e dar peso para a chance de a CGU cobrar o que é novo.
6. **Emergentes**: tópico que só aparece em 2025–2026 (IA, nuvem, DevSecOps) sobe, porque a tendência é de alta.
7. **Reciclagem de assertivas**: itens quase iguais em provas diferentes (mesma ideia, redação parecida) mostram o que a banca reaproveita; contam como um único "núcleo" com bônus de recorrência.
8. **Dificuldade real** (opcional, só se vier do TEC sem esforço extra): taxa de acerto baixa indica pegadinha frequente; sobe o tópico na revisão, não na coleta.
9. **Custo-benefício para o Jonathas**: Java e APIs ele já domina. Para estudo, desce o tópico que ele domina e sobe o que é novo para ele; para coleta de questões, a prioridade segue o score.
10. **Cobertura mínima**: antes de aprofundar um tema, garantir ≥ ~20 itens ou esgotar as provas-espelho; sem isso, a aula por engenharia reversa fica fraca.

## 4. Próximos passos
- Piloto: baixar prova e gabarito de 1–2 provas do topo do ranking (ex.: TCE-AC 2024, cargo 11) e medir quantos itens entram por requisição.
- Acrescentar ao `banco.py` um comando `rank` que aplique as heurísticas 1–4 aos itens já classificados. (Feito no banco.py v4.)
