# Auditoria cega da triagem — P2 e P3

Data: 2026-11-09

## Método

Classifiquei semanticamente os enunciados dos pacotes `verificacao-cega-p2.jsonl` (55 itens) e `verificacao-cega-p3.jsonl` (58 itens), sem consultar os rótulos privados antes de salvar as anotações independentes. Usei `edital`, `fora_edital` e `ambiguidade`; itens só foram aceitos quando a correspondência com um subitem estava sustentada pelo conteúdo do enunciado. Em seguida comparei as anotações com `edital_prov` e com os estratos de score do manifesto.

As anotações por item estão em `verificacao-cega-p2-rotulos-independentes.jsonl` e `verificacao-cega-p3-rotulos-independentes.jsonl`.

## Resultado

| Bloco | Amostra | Dentro do edital | Ambíguos | Fora do edital | Subitem idêntico ao palpite original entre os aceitos |
|---|---:|---:|---:|---:|---:|
| P2 | 55 | 17 (30,9%) | 2 (3,6%) | 36 (65,5%) | 9/17 (52,9%) |
| P3 | 58 | 39 (67,2%) | 1 (1,7%) | 18 (31,0%) | 16/39 (41,0%) |

### Resultado por estrato de score

| Bloco | Estrato baixo | Estrato médio | Estrato alto |
|---|---:|---:|---:|
| P2 | 4/19 dentro; 14 fora; 1 ambíguo | 5/18 dentro; 13 fora | 8/18 dentro; 9 fora; 1 ambíguo |
| P3 | 7/18 dentro; 10 fora; 1 ambíguo | 13/20 dentro; 7 fora | 19/20 dentro; 1 fora |

## Interpretação e limites

- **P2 não passa nesta triagem:** cerca de dois terços da amostra não sustentam vínculo com o conteúdo programático; até o estrato alto só teve 8 de 18 itens aceitos. Não usar o lote atual para alimentar frequência/prioridade sem nova classificação.
- **P3 mostra separação útil por score:** o estrato alto teve 19/20 itens dentro do edital, mas os estratos baixo e médio ainda têm contaminação relevante. Isso é um sinal promissor para filtrar itens de score alto, não uma aprovação da base inteira.
- A amostra foi montada por ordenação determinística do score e seleção de trechos baixo/médio/alto, não por sorteio aleatório dentro dos estratos. Logo, as proporções não são estimativas imparciais para todo o banco.
- Esta foi uma revisão semântica independente do rótulo original, mas ainda é uma única revisão automatizada. Os desacordos de subitem (P2: 8; P3: 23) precisam de adjudicação humana ou segunda revisão independente antes de recalibrar o classificador.
- Nenhum dado do banco principal foi alterado. A comparação não foi tratada como aprovação de aplicação.

## Próximo passo recomendado

Corrigir a formação da fila para sortear amostras aleatórias reprodutíveis dentro de cada estrato, registrar exemplos negativos explícitos para P2, e revisar os casos de desacordo com segunda anotação independente. Só então recalcular precisão/recall e decidir limiares separados para P2 e P3. Para P3, manter score alto em quarentena como candidato promissor; para P2, bloquear aplicação automática até recalibrar.

## Rodada cega aleatória v2 (2026-11-09)

Corrigi o gerador para sortear sem reposição dentro de tercis de score, com semente `20261109`, deduplicação por chave do item e texto normalizado e exclusão dos itens da primeira rodada. A rodada contém 60 itens de cada bloco; nenhum item se repete entre a rodada anterior e a v2. Os pesos de expansão e contagens da população estão nos manifestos v2.

| Bloco | Dentro do edital | Ambíguos | Fora do edital | Concordância exata do subitem entre aceitos |
|---|---:|---:|---:|---:|
| P2 | 22/60 (36,7%) | 1/60 | 37/60 | 5/22 (22,7%) |
| P3 | 48/60 (80,0%) | 2/60 | 10/60 | 14/48 (29,2%) |

P2 por score baixo/médio/alto: 7/20, 6/20, 9/20 dentro do edital. P3: 15/20, 17/20, 16/20. Portanto, a alta taxa observada no estrato alto da primeira amostra de P3 não se repetiu (16/20 nesta rodada).

Esta rodada é uma amostra aleatória estratificada do **pool de itens já selecionados pelo mapa de triagem**, não de todas as questões extraídas. Ela mede a precisão dentro desse pool, não o recall da busca. Os resultados continuam abaixo da meta de precisão ≥90%, e o acerto exato do subitem também é baixo. As anotações foram feitas sem consultar os palpites, mas ainda por uma única revisão automatizada; não substituem adjudicação independente humana.

Arquivos v2: `verificacao-cega-v2-p2.jsonl`, `verificacao-cega-v2-p2-manifesto.json`, `verificacao-cega-v2-p2-rotulos-independentes.jsonl` e correspondentes P3. O script de geração é `scripts/gerar_amostra_cega_v2.py`.

## Atualização operacional

Corrigida a leitura de IDs de núcleos aninhados que derrubava `scripts/painel_prioridade.py`. O painel agora calcula e exibe os blocos: P1 alta, P2 média, P3 média; a ordem global continua explicitamente não confiável. Versão do app atualizada de 0.0.103 para 0.0.104. A execução local do painel terminou sem erro após a correção. O banco de questões não foi alterado.

## Diagnóstico do objetivo completo

- O app lê 159 registros no manifesto de provas (155 em `extraida`, 4 em `persistida`). A descoberta local de conteúdo reporta 344 provas varridas, 22.434 itens e 4.991 candidatos lexicais fortes; são contadores de etapas diferentes e não devem ser somados como se fossem provas aprovadas.
- `scripts/suficiencia.py` estima volume suficiente para P1 (24/24 temas) e P2 (25/25), mas ainda recomenda mineração para P3·DADOS 4 e P3·ENG 3. **Suficiência de volume não equivale a classificação correta.**
- O relatório canônico `docs/confiabilidade-blocos.json` mantém P1 aprovado e P2/P3 reprovados: precisão parcial 13,3% em P2 e 52,0% em P3; backtest top‑5 de 0,38 e 0,30, cada um com apenas um fold temporal nos gates de classificação.
- Em `docs/confianca-ordem.json`, P2 tem recall estimado 0,83 e estabilidade de faixa 0,667, mas só dois folds temporais; P3 tem recall estimado 0,539. Assim, a classificação e a captura de questões ainda impedem a confiança alta da ordem global, mesmo quando o volume parece suficiente.
- O pipeline local tem 155 provas extraídas aguardando classificação no manifesto. Não classifiquei nem apliquei essas provas em lote: fazer isso antes de corrigir/validar o classificador propagaria falsos positivos ao banco.

## Portão atual

A ordem global de alta confiança **não foi atingida**. P1 aparece como alta no painel segundo o critério atualmente registrado; P2 e P3 aparecem como média. Para promover qualquer bloco a alta confiança ainda são necessários: validação humana independente das novas amostras cegas, amostras de itens descartados para recall por bloco, melhoria da precisão/subitem do classificador e backtest temporal com pelo menos três folds válidos. Só então se deve processar as provas pendentes e atualizar a ordem. As aulas e cadernos continuam utilizáveis como materiais de estudo, mas não devem ser interpretados como evidência de que a prioridade global está validada.
