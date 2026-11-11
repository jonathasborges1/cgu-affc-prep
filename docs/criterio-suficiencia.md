# Critério de suficiência de amostra (definido em 05/11/2026)

Pergunta: já minerei provas suficientes para ensinar este assunto e saber o quanto ele pesa?
Código: `scripts/suficiencia.py` (cálculo), `scripts/minerar.py` (laço de mineração), aba **Prioridade** do app.

Unidade: assunto do edital (nível 1) dentro de P1, P2 ou P3. Só entram itens "fortes" da triagem por termos, sem duplicatas entre cargos da mesma prova e sem os recortes `escopo/tema-*` (não são amostra das provas).

Assunto = **suficiente** quando:
1. **Estável**: o intervalo de 90% (reamostrando provas, 300 vezes) para "quantos itens da prova o assunto rende" tem meia-largura <= 1 item OU <= 35% do valor estimado.
2. **Massa** (>= 20 itens fortes em >= 8 provas) OU **raro** (limite superior < 1,5 item esperado na prova).
Caso contrário: **minerar**. Com < 3 itens fortes o assunto é marcado **lacuna** (ensinar pela base legal).

Parada da mineração: todos suficientes, ou rendimento decrescente (5 rodadas de 6 provas sem reduzir os assuntos a minerar nem somar itens fortes neles), ou limite de tempo/provas.
Cuidados: 1 PDF por vez, pausa >= 3 s, parar em 403/429; só o CDN oficial do Cebraspe.
Limites: limiares são regras iniciais; a triagem é por termos (precisão ~40% em ADM 4: 37 confirmados de ~86); provas são de outros cargos; participação não é previsão.

## Semáforo de maturidade (v0.0.30): 3 perguntas em ordem
1. Amostra de provas suficiente? Não -> vermelho: minerar mais provas.
2. >= 15 itens classificados em núcleos no banco? Não -> amarelo: classificar itens.
3. A aula cobre >= 70% das questões do assunto? Não -> verde: criar aula (ou mini-aula); sim -> azul: caderno e revisão.
Assunto com < 3 itens fortes (lacuna) -> cinza: ensinar pela base legal. Constantes em `scripts/suficiencia.py` (MIN_CLASSIF, COB_OK).
O app (aba Prioridade) mostra a ação e um botão "copiar pedido" com o texto pronto para colar no chat.

## Calibração e confiança da ordem (v1)
- Um tópico de P1/P2 tem amostra suficiente com censo ou 30 rótulos; P3 usa censo ou 15 rótulos devido ao tamanho menor dos lotes cegos existentes. A regra mede apenas suficiência para estimar o tópico, não acurácia da triagem. Precisão/recall e estabilidade continuam gates separados.
- Censo pequeno é suficiente para calibrar a triagem do universo observado, mas não prova estabilidade da ordem histórica nem do desempenho em provas futuras.
- A ordem por faixas do bloco só recebe confiança quando há evidência publicada de estabilidade acumulada >= 0,80, teste temporal ponderado >= 0,85, pior período >= 0,70 e auditoria de recall com limite inferior de 90% >= 0,75. Campo de auditoria ausente significa confiança não demonstrada.
- Ordem exata de tópico exige o indicador `firme` validado na fonte de calibração. Uma faixa confiável não implica posições exatas confiáveis.
- `recall_medido` só pode ser verdadeiro mediante registro de auditoria correspondente; não é inferido do código P1/P2/P3.
- A varredura mantém URLs visitadas e hashes SHA-256 de PDFs presentes no acervo. Bloqueio HTTP interrompe a rodada; erros transitórios não são marcados como concluídos, e PDFs válidos já baixados são reaproveitados.
- O laço de mineração atualiza catálogo e ranking antes de cada rodada. Ele não declara a meta atingida enquanto os gates de confiança publicados para os blocos estiverem reprovados.
- `scripts/validar_lotes.py` verifica localmente se uma classificação cobre exatamente os itens extraídos e usa códigos/tags válidos. Esse portão é estrutural; não substitui leitura semântica independente, comparação de concordância nem autorização de persistência.
- `scripts/minerar.py` grava `concursos/<ativo>/fila/automacao-pendencias.json` com os próximos passos que exigem julgamento humano. Prova em estado extraída/classificada/verificada nunca é avançada automaticamente pelo laço.
- `scripts/auditar_prioridade_cega.py` pondera os rótulos independentes da amostra estratificada v2. Como ela foi sorteada apenas entre itens recuperados, informa precisão, mas declara recall não estimável; recall requer amostra probabilística dos descartados.

## Confiança da ordem P2 por inferência estratificada (v3, 10/11/2026)

- Quando o universo não é censado, a participação é estimada por amostra aleatória estratificada; não se exige ler 75% da população, pois isso confundiria fração censada com precisão da inferência.
- A faixa intermediária deve estar integralmente lida. A cauda deve ter amostra probabilística suficiente para margem máxima teórica de 4 pontos percentuais no IC90 (n mínimo 423), além de bootstrap por assunto.
- As faixas de prioridade são fixas por participação: A >= 8%, B >= 4%, C abaixo. A confiança exige estabilidade de faixa >= 80% dos assuntos relevantes.
- O backtest usa a mesma meia-vida de quatro anos do modelo de incidência. Exige razão temporal ponderada por recência >= 0,85 e pior período entre os três anos mais recentes >= 0,70. Períodos antigos continuam publicados como diagnóstico de mudança estrutural.
- Previsões automáticas só podem ser imputadas se passarem auditoria fora da amostra. O classificador de `docs/modelo-semantico-p2.json` reprovou e, por isso, nenhuma previsão dele integra a ordem.
