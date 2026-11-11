# P2: como chegar a 85% de precisão na triagem (experimento de 07/11/2026)

Base: 908 itens rotulados (608 da amostra cega + 300 descartados), TF-IDF 1–2 gramas + regressão logística, validação temporal (treina em anos anteriores, testa no ano; 5 testes: 2021–2025). Scripts em tmp/p2ml/.

| Corte (prob. de ser P2) | Aceitos | Precisão | Recall |
|---|---|---|---|
| 0,5 | 98 | 82% | 49% |
| 0,6 | 64 | 86% | 34% |
| 0,7 | 45 | 87% | 24% |

- A triagem por palavras-chave acerta 13%. O classificador supervisionado passa de 85% no binário "é P2 / não é P2".
- No nível do assunto (25 classes) o acerto do 1º palpite é só 53–60% e o top-5 recupera 60%; com ~7 exemplos por assunto isso não chega a 85%.
- Negativos de P1/P3 não ajudaram.

## Caminho
1. Trocar a triagem de P2 pelo classificador (corte ≈ 0,6) para decidir "é P2".
2. Aprendizado ativo: rotular os itens que o modelo acha mais prováveis e os mais incertos entre os ~22 mil não rotulados, para subir recall e exemplos por assunto.
3. Nova amostra cega só de itens aceitos pelo classificador (≥ 300) para validar o gate de 85%.
4. Decidir se o gate de P2 é binário (pertence a P2) ou por assunto; por assunto exige muito mais rótulos.

## Correção após amostra cega nova (07/11/2026)
120 itens novos aceitos pelo classificador (prob. ≥ 0,6, nunca vistos no treino), rotulados às cegas: **57% eram de P2** (68/120), não 86%. Por faixa de probabilidade: 0,6–0,7 → 69%; 0,7–0,8 → 36%; 0,8–0,9 → 59%; ≥ 0,9 → 75% (n = 12). Retreinado com mais 100 itens rotulados (aprendizado ativo), a precisão no mesmo teste ficou em 57–67% (corte 0,8).
A validação temporal anterior foi otimista: o conjunto de teste vinha da mesma amostra pré-filtrada. Confusões principais: LGPD e direito administrativo geral parecem P2 mas não são.
Conclusão: 85% não é alcançável com o classificador e ~1.000 rótulos. Caminhos: (a) censo por leitura dos candidatos de maior probabilidade; (b) redefinir o critério de confiança da P2 para a estabilidade da ordem (largura dos intervalos), não para a precisão da triagem.
