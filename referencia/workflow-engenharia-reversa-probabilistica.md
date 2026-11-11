# Workflow: tema do edital → aulas e caderno por probabilidade (04/11/2026)

Pergunta que o workflow responde: "o que eu preciso saber para ir bem na prova neste tema?". Como não sabemos o que vai cair, estudamos o que tem maior probabilidade, com base em provas anteriores do Cebraspe.

## Unidade de estudo: o núcleo
Núcleo = a ideia que um item testa (ex.: "LDO orienta a elaboração da LOA e traz as metas fiscais"). Itens diferentes repetem o mesmo núcleo com variações (C numa prova, E em outra, com troca de termo). Estudar por núcleo cobre muito mais prova do que decorar itens.

## Cálculo
- Peso do item = peso_prova × 0,5^(idade_em_anos/3).
- Score do núcleo = soma dos pesos dos seus itens. Massa do núcleo = score ÷ soma de todos os scores do tema.
- Cobertura estimada (Good–Turing) = 1 − (núcleos vistos uma única vez ÷ total de itens). É a chance estimada de um item novo do tema cair num núcleo que já conhecemos. Cobertura baixa = muita coisa ainda não vista.

## Regra de profundidade (quando parar)
1. Ensinar os núcleos em ordem de massa até acumular ~80% da massa vista.
2. Núcleos vistos só uma vez entram se forem NORMA_LITERAL, se o artigo/lei está no edital ou se são vizinhos (item 3). Não se descarta singleton enquanto a cobertura estimada for < ~70%. (No banco.py v4, o `rank` marca esses casos como ENSINAR(1x).)
3. Vizinhos: conceitos citados no texto do edital para o tópico, ou que dividem a mesma base legal/capítulo dos núcleos de alta massa. Entram com massa × 0,5 por grau de distância; parar quando a massa fica abaixo de ~3% ou a distância passa de 2.
4. Parar de minerar quando a cobertura estimada ≥ ~70% ou não houver mais provas-espelho; o que sobrar é lacuna: ensina-se pelo edital e pela base legal, sem questão (marcado como tal).
5. Teto de uma aula: ~8–10 núcleos. Mais que isso vira aula 2 (ordem de massa).

## Fluxo (simples)
1. **Consulta ao banco** (`banco.py rank`): núcleos do tópico, massa, cobertura. Suficiente? segue para 4.
2. **Mineração** (só se faltar): buscador (Chrome, em série, 1 PDF por vez) baixa prova+gabarito das provas ainda não vistas no manifesto `provas.jsonl`; extrator (script) separa itens e gabarito.
3. **Classificador/decompositor** (pode rodar em paralelo, 1 agente por prova): para cada item devolve tópico do edital (ou "fora do edital"), núcleo(s) e tags de pegadinha; marca duvidosos. O `banco.py` grava (persistência) e atualiza o manifesto. Volta ao passo 1.
4. **Plano de aula**: núcleos ordenados por massa + vizinhos + lacunas, cortados pela regra de profundidade → 1 ou mais aulas.
5. **Redação**: aula (do zero, com a forma como a banca cobra: C, E e pegadinha de cada núcleo) + caderno de até 10 itens com referência real.

## Dados
- Itens ganham o campo `nucleos` (lista de ids). Arquivo `nucleos.jsonl`: id, tópico do edital, enunciado canônico, base legal, vizinhos.
- `provas.jsonl` (manifesto): url prova, url gabarito, hash, estado (descoberta → baixada → extraída → classificada → verificada → persistida).
- Comando `banco.py rank --edital "P1·ADM 4.1"`: massa por núcleo, cobertura estimada, corte de profundidade.

## Piloto (PPA/LDO/LOA, 10 itens, 2023–2024)
8 núcleos; massa: LDO orienta LOA + metas fiscais 22%; PPA programa 20%; encadeamento PPA→LDO→LOA, limites dos Poderes e planos setoriais 11% cada; exclusividade da LOA, orçamento autorizativo e emendas 9% cada. Seis dos 10 itens são de núcleos vistos uma só vez, então a cobertura estimada é de ~40%: ainda há muita coisa não vista e a regra manda minerar mais e ensinar também os vizinhos (princípios orçamentários, créditos adicionais, metas e riscos fiscais da LRF, ciclo orçamentário).
