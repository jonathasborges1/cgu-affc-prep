# Modelo de prioridade v2

## O que o numero significa

O app exibe **incidencia estimada**, nunca "probabilidade de cair". Uma frequencia historica so passa a calibrada quando e comparada com itens lidos e rotulados. Estabilidade do bootstrap e calibracao sao gates diferentes.

O indice de estudo e:

```
itens_esperados * pontos_por_item * (1 - dominio)
* fator_discursiva * fator_minimo / horas_estimadas
```

- `itens_esperados`: participacao calibrada quando existe; caso contrario, triagem ponderada e explicitamente provisoria.
- `pontos_por_item`: P1=1, P2=1, P3=2.
- `dominio`: ganho liquido suavizado nas respostas C/E. Cinquenta por cento de acerto equivale a zero, pois um erro anula um acerto.
- `fator_minimo`: protege contra eliminacao em P1, P2 e P3.
- `horas_estimadas`: configuravel em `concursos/<ativo>/parametros-estudo.json`; o default de 1 h fica identificado como default.

## Gates de confianca

1. Fonte oficial e extracao valida.
2. Amostra automatica estavel, reamostrando provas.
3. Pelo menos 15 rotulos humanos/independentes por assunto para estimar precisao.
4. Itens descartados amostrados para medir recall.
5. Backtest temporal com volume minimo.

Sem os gates 3 e 4, a ordem aparece como provisoria e a acao e `Calibrar triagem`. O sistema nao recomenda aula com base somente em casamento lexical.

Em P1, um topico com menos de 15 rotulos tambem e considerado calibrado quando todos os candidatos do seu universo foram lidos (censo completo). A decisao usa o limite inferior do IC90, nao apenas a media. Posicao exata so e mostrada para os tres assuntos cuja posicao ficou firme; os demais aparecem como intervalo e grupo de prioridade.

## Peso das provas

As provas nao contam mais igualmente. A massa e ponderada por meia-vida de quatro anos e pela compatibilidade calculada na descoberta, limitada para nao dominar o conjunto. Esses parametros sao heuristicas transparentes e so devem ser ajustados depois de backtests suficientes.

## Calibracao e backtest

```
python scripts/calibrar_triagem.py amostrar --bloco P2 --n 120 --saida fila/calibracao-p2.jsonl
python scripts/calibrar_triagem.py avaliar fila/calibracao-p2.jsonl --saida docs/calibracao-p2.json
python scripts/backtest_prioridade.py
python -m unittest discover -s tests -v
```

O arquivo de amostra contem recuperados e descartados, com peso amostral. `codigo_real` deve ser preenchido sem consultar a previsao. Assim o modelo mede precisao e recall, nao apenas acerto entre itens que o filtro decidiu mostrar.

## Limite atual

P1 possui calibracao manual. P2 e P3 permanecem provisoriamente ordenados ate a revisao das amostras. Esse limite agora e parte do contrato do backend, nao apenas um aviso visual.
