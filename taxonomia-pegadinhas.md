# Taxonomia de pegadinhas (Cebraspe, itens Certo/Errado)

Usar estas etiquetas no campo `tags` (comando `set-padrao ID "texto" --tags A,B`). O campo `padrao` explica em uma frase o que o item testa.

| Etiqueta | O que é | Como reconhecer |
|---|---|---|
| INVERSAO | Troca de sentido da relação (quem depende de quem, causa e efeito) | "A se adapta a B" quando a norma diz o contrário |
| ABSOLUTO | Palavra absoluta que torna o item falso | sempre, nunca, apenas, somente, exclusivamente, qualquer, garante, elimina |
| TROCA_TERMO | Um termo técnico substituído por outro parecido | projeto × programa, autenticação × autorização, ETL × ELT |
| ESCOPO | Generaliza ou restringe além do que a regra permite | "todos", "em qualquer caso", ou limita a um caso só |
| CAUSA_CONSEQUENCIA | Relação de causa e efeito invertida ou inventada | "como X, então Y" sem ligação real |
| EXCECAO_OMITIDA | Regra correta, mas ignora a exceção prevista | "pode, desde que..." sem a vedação legal |
| NORMA_LITERAL | Cópia ou paráfrase fiel de um artigo ou definição | geralmente Certo; erro só por troca de uma palavra |
| CONCEITO_MISTURADO | Atribui a um instituto o conteúdo de outro | metas fiscais no PPA, OAuth como autenticação |
| PARTE_CERTA_PARTE_ERRADA | Item composto com uma metade verdadeira e outra falsa | duas afirmações ligadas por "e", "o que", "pois" |
| DETALHE_NUMERICO | Prazo, percentual ou quantidade alterados | datas, limites, quantidades |
| NORMA_DESATUALIZADA | Item depende de norma revogada ou alterada | conferir vigência antes de usar |

## Técnica de leitura (separar o item em partes)
1. Sublinhar palavras absolutas.
2. Dividir em afirmações; basta uma falsa para o item ser Errado.
3. Checar a direção das relações (quem depende de quem).
4. Procurar a exceção que a norma prevê.
5. Em caso de dúvida real, lembrar que o erro desconta o mesmo que o acerto vale.
