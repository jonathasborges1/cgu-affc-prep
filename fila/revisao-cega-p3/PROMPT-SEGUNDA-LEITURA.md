# Segunda leitura independente — calibração P3

Revise os 120 itens de `lote-01.md` a `lote-06.md` usando somente a taxonomia exibida nos próprios lotes.

Regras:

1. Não abra `rotulos.json`, `manifesto.json`, `fila/calibracao-p3.jsonl`, `fila/calibracao-p3-revisao-agente.jsonl` nem qualquer relatório com previsões ou resultados da primeira leitura.
2. Para cada ID, atribua exatamente um código de nível 1 da taxonomia P3 ou `OUTRO`.
3. Não use o cargo ou a banca como atalho; classifique pelo conteúdo do item.
4. Em caso de conteúdo truncado ou realmente ambíguo, registre o ID separadamente em `duvidas-segunda-leitura.json`; ainda assim, não consulte a primeira leitura.
5. Grave o mapa completo em `rotulos-segunda-leitura.json`, no formato `{ "id": "P3·..." }`.
6. Ao final, confirme que há exatamente 120 IDs únicos e nenhum valor nulo.

Não altere a amostra oficial e não atualize gates de confiança. A comparação e a resolução de divergências serão feitas somente depois que esta leitura estiver concluída.
