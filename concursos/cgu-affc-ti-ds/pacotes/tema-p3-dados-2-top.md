# PACOTE tema-p3-dados-2-top (20 itens)
Para cada item: edital (código de CANDIDATOS ou FORA), núcleo, tags, nível. Gabarito: C=certo E=errado.

## 1 | gab=C | cand: P3·DADOS 2.1, P3·DADOS 2.2, P3·DADOS 1.2
Em bancos NoSQL orientados a documentos, é comum o uso de estruturas aninhadas, que evitam junções e melhoram a performance de leitura. Certa empresa especializada em seguros de vida privados decidiu modernizar seu sistema de informações com a utilização de um SGBD relacional, padrão SQL. Durante a reestruturação do banco de dados, a equipe de TI definiu um modelo com tabelas tais como CLIENTE, APOLICE, BENEFICIARIO 
## 2 | gab=C | cand: P3·DADOS 2.1, P3·DADOS 2.4, P3·ARQ 2.6
Na especificação dos requisitos da contratação, compete ao integrante requisitante, com o apoio do integrante técnico, definir, entre outros, os requisitos de negócio, quando aplicáveis. JUSTIFICATIVA - Certo. Conforme a IN SGD/SEDGG/ME n.º 94/2022, “Art. 16. Na especificação dos requisitos da contratação, compete: I ao Integrante Requisitante, com apoio do Integrante Técnico, definir, quando aplicáveis, os seguintes
## 3 | gab=E | cand: P3·DADOS 2.2, P3·DADOS 2.4, P3·DADOS 2.3
No SQL, SELECT * FROM table é uma consulta de banco de dados e exibe informações da tabela do banco de dados, portanto é correto considerá-la uma mineração de dados.
## 4 | gab=E | cand: P3·DADOS 2.2, P3·DADOS 2.4, P3·DADOS 2.3
Os bancos de dados não relacionais se diferenciam dos bancos de dados relacionais por utilizarem de forma exclusiva objetos codificados com estado armazenado em um atributo estruturado, em vez de tabelas com colunas e linhas. A seguir, são apresentadas as estruturas de duas tabelas, de nomes Customers e Orders, em um banco de dados, e também um comando SQL relativo a essas tabelas. Customers CustomerID (INT) – identi
## 5 | gab=C | cand: P3·DADOS 2.3, P3·DADOS 2.4, P3·DADOS 2
No processo de análise de desempenho de um banco de dados, na análise de planos de execução é possível diagnosticar que a exclusão de índices pode levar à melhoria de desempenho do banco de dados.
## 6 | gab=C | cand: P3·DADOS 2.3, P3·DADOS 2.4, P3·DADOS 2.2
Na técnica de modificação de banco de dados adiada, a atomicidade da transação é garantida registrando-se todas as modificações do banco de dados no log, mas adiando-se a execução de todas as operações WRITE de uma transação até que a transação seja parcialmente confirmada, para transações executadas em série. OS ESPECÍFICOS -A respeito da linguagem de consulta SQL, julgue o próximo item.
## 7 | gab=C | cand: P3·DADOS 2.2, P3·DADOS 2.4, P3·DADOS 2 [texto-base: Julgue os itens seguintes, relativos à linguagem de definição de dados SQL, à linguagem de manipulação de dados SQL, à linguagem de controle de dados SQL e à linguagem de consulta de dados SQL.]
No exemplo de comando UPDATE a seguir, é utilizada a construção case, em que as atualizações nas tuplas são realizadas com um único comando, evitando-se problemas com a ordem das atualizações. UPDATE tabela SET coluna = case When predicado1 then resultado1 When predicado2 then resultado2 ... When predicado3 then resultadoN else resultadoN End; No que diz respeito a linguagens procedurais em um banco de dados SQL e a 
## 8 | gab=C | cand: P3·DADOS 2.3, P3·DADOS 2.4, P3·DADOS 2
Um exemplo de técnica bastante utilizada para a otimização do desempenho do banco de dados da empresa consiste na análise de consultas SQL, também conhecida como plano de execução.
## 9 | gab=C | cand: P3·DADOS 2.2, P1·ESTADO 5.1, P3·DADOS 2.4
A otimização de bases de dados para BI visa garantir que as consultas analíticas sejam executadas de maneira eficiente e rápida, a exemplo da indexação, que poderia ser a criação de índices nas tabelas de fatos e dimensões para acelerar a recuperação de dados; índices comuns incluem índices de colunas, índices compostos e índices bitmap.
## 10 | gab=E | cand: P3·DADOS 2.2, P3·DADOS 2.4, P3·DADOS 2
Ao escrever consultas para bancos de dados relacionais, o uso de subconsultas e tabelas aninhadas costuma apresentar melhor desempenho que o uso de JOIN.
## 11 | gab=C | cand: P3·DADOS 2.2, P3·DADOS 2.4, P3·DADOS 2.3
Filtro Bloom é uma estrutura de dados com uso eficiente de espaço que pode ser utilizada para testar se um elemento é membro de um conjunto; no entanto, os índices do filtro Bloom suportam apenas consultas de igualdade, sendo mais úteis quando uma tabela possui muitos atributos e as consultas testam combinações arbitrárias deles.
## 12 | gab=C | cand: P3·DADOS 2.2, P3·DADOS 2.4, P3·DADOS 1.8 [texto-base: Julgue os próximos itens, a respeito de linguagem de manipulação de dados (DML), de linguagem de definição de dados (DDL), de modelagem dimensional e de linguagem de consulta estruturada (SQL).]
Um esquema em estrela é um modelo multidimensional no qual os atributos das tabelas fato e dimensão podem ser usados para filtrar, agrupar e agregar os fatos. JUSTIFICATIVA - Certo. Um esquema em estrela é um modelo multidimensional que organiza os dados em um banco de dados para torná-los mais fáceis de entender e analisar. Pode ser aplicado a data warehouses, bancos de dados, data marts e outras ferramentas. O desi
## 13 | gab=C | cand: P3·DADOS 2.3, P3·DADOS 2.4, P3·DADOS 2.2
A consulta SQL a seguir cria uma view para listar o total de gastos por município e hospital, bem como agrupa os resultados por município e hospital, calcula a soma dos valores gastos e ordena os resultados, de forma decrescente, pelo maior gasto e, depois, pelo nome do município e do hospital. create view total_gastos_por_municipio as select nome_municipio as municipio, nome_hospital as hospital, sum(valor_gasto) as
## 14 | gab=C | cand: P3·DADOS 2.3, P3·DADOS 2.4, P3·DADOS 2.2
A execução da consulta SQL a seguir listará os nomes dos hospitais que tiveram gastos superiores à média geral de gastos. SELECT nome_hospital, sum(g.valor_gasto) total FROM gastos g JOIN hospital h ON g.id_hospital = h.id_hospital group by nome_hospital having sum(g.valor_gasto) > (SELECT AVG(valor_gasto) FROM gastos) ORDER BY nome_hospital as
## 15 | gab=C | cand: P3·DADOS 2.3, P3·DADOS 2.4, P3·DADOS 2.2 [texto-base: Julgue os seguintes itens, relativos a técnicas de visualização de dados em business intelligence, a data lakes e a regras de associação em mineração de dados.]
A execução da consulta SQL a seguir listará todos os processos, inclusive aqueles que ainda não têm partes associadas, e exibirá o nome das pessoas e os seus respectivos papéis nos processos em que estão envolvidas. SELECT p.numero_processo, ps.nome, pa.tipo_parte FROM Processos p LEFT JOIN Partes pa ON p.id_processo = pa.id_processo LEFT JOIN Pessoas ps ON pa.id_pessoa = ps.id_pessoa
## 16 | gab=C | cand: P3·DADOS 2.2, P3·DADOS 2.4, P3·DADOS 2
A escolha do tipo de índice é um aspecto importante para o desempenho do sistema de banco de dados: se as consultas de intervalo forem comuns, os índices de árvore B, os quais possuem uma forma de árvore balanceada, serão preferíveis aos índices de hash, os quais organizam as chaves de busca, com seus ponteiros associados em uma estrutura de arquivos hash.
## 17 | gab=C | cand: P3·DADOS 2.1, P3·DADOS 3.8, P3·DADOS 2.4 [texto-base: A respeito de arquitetura, segurança, integridade, concorrência, recuperação após falhas e gerenciamento de transições em sistemas de gerenciamento de banco de dados (SGDB), julgue os próximos itens.]
Um SGBD que implementa um sistema de log de transações segundo o princípio WAL (write-ahead logging) é capaz de garantir que, mesmo após uma falha inesperada, todas as transações confirmadas possam ser recuperadas ao estado consistente anterior à falha. JUSTIFICATIVA - Certo. O princípio do write-ahead logging (WAL) estabelece que todas as alterações feitas por uma transação sejam registradas em um log de transações 
## 18 | gab=E | cand: P3·DADOS 2.1, P3·SEG 1.1, P3·DADOS 2.4
Ao contrário do LDAP injection, em que o invasor pode inserir ou manipular consultas criadas pela aplicação, no SQL injection o invasor pode apenas inserir consultas na aplicação, que são enviadas diretamente para o banco de dados.
## 19 | gab=C | cand: P3·DADOS 2.1, P3·DADOS 2.4, P3·DADOS 2.3
Os comandos SQL, tais como SELECT, INSERT, UPDATE e DELETE, são aplicáveis em SGDBs relacionais. JUSTIFICATIVA - Certo. Esses comandos são aplicáveis e amplamente utilizados em SGBDs relacionais, pois esses sistemas compartilham a estrutura relacional e utilizam SQL como linguagem de consulta para realizar operações de manipulação e consulta de dados.
## 20 | gab=E | cand: P3·DADOS 2.1, P3·DADOS 2.4, P3·DADOS 2.3 [texto-base: Julgue os itens seguintes, relativos a linguagem de consulta estruturada (SQL), linguagem de definição de dados (DDL) e linguagem de manipulação de dados (DML).]
Os comandos SQL são instruções ou consultas usadas para interagir com um banco de dados relacional, a exemplo do comando COMMIT disponibilizado na DML para manipular dados.

## CÓDIGOS CANDIDATOS (texto do edital)
- P1·ESTADO 5.1: Resultados socialmente relevantes; legitimidade, confiança e direitos; controle interno, externo e social em perspectiva institucional; tensões entre eficiência
- P3·ARQ 2.6: Spring Security: configuração e avaliação de mecanismos de autenticação e autorização.
- P3·DADOS 1.2: Bancos documentais, chave-valor e vetoriais.
- P3·DADOS 1.8: Spring Data JPA: repositórios, consultas e paginação.
- P3·DADOS 2: SQL e desempenho.
- P3·DADOS 2.1: Definição e manipulação de dados, controle de acesso e transações.
- P3·DADOS 2.2: Consultas com filtros, junções, agregações, subconsultas e expressões de tabela comuns.
- P3·DADOS 2.3: Índices, planos de execução, valores nulos e duplicações.
- P3·DADOS 2.4: Diagnóstico de consultas e efeitos sobre o desempenho da aplicação.
- P3·DADOS 3.8: Controle transacional, registro do estado de execução e reinício após falhas.
- P3·SEG 1.1: Ameaças e vulnerabilidades em aplicações e interfaces.

## NÚCLEOS JÁ EXISTENTES (reutilize o id se for a mesma ideia)
- n-owasp-quebra-controle-acesso: Quebra de controle de acesso é falha de restrições sobre o que usuários autenticados podem fazer; o ataque que
- n-injecao-ldap: LDAP injection manipula consultas LDAP inserindo código malicioso na entrada, que passa a ser interpretado de 
- n-xss-alvo-usuario-navegador: XSS injeta scripts em páginas web que são executados no navegador de outros usuários; não explora execução de 
- n-csrf-acao-indesejada-sessao: CSRF induz o navegador de um usuário autenticado a enviar requisição que executa ação indesejada na aplicação 
- n-ddos-mitigacao-especifica: Mitigação eficiente de DDoS exige soluções específicas (anti-DDoS, CDN, filtragem upstream); firewall de borda
- n-owasp-top10-vs-samm: O OWASP Top 10 descreve os riscos mais críticos em aplicações web; o OWASP SAMM é um modelo de maturidade de g
- n-sqli-entrada-sem-validacao: SQL injection explora formulários e entradas que não validam ou sanitizam dados, permitindo enviar comandos ma
- n-xss-refletido: No XSS refletido a carga útil vai na requisição, é refletida na resposta HTTP e executada no navegador da víti
- n-dos-ddos-distribuido: DDoS usa múltiplas origens distribuídas para tornar o serviço indisponível; antivírus não é suficiente para pr
- n-ataques-injecao: SQL injection, LDAP injection e XSS são ataques de injeção de código.
- n-dns-cache-poisoning-ddos: Envenenamento de cache DNS pode redirecionar tráfego e ser usado em ataques associados a DDoS.
- n-ddos-afeta-disponibilidade: A principal consequência de um ataque DDoS é a perda de disponibilidade do serviço, não de integridade dos dad
- n-phishing-engenharia-social: Phishing é engenharia social que induz a vítima a fornecer dados e pode comprometer confidencialidade, integri
- n-xss-tipos-refletido-armazenado-dom: XSS tem variações (refletido, armazenado e baseado em DOM) e não se limita a formulários de cadastro
- n-ssrf-sem-credenciais-admin: SSRF induz o servidor vulnerável a fazer requisições a destinos escolhidos pelo atacante, sem exigir credencia
- n-ataques-passivos-confidencialidade: Escuta e análise de tráfego são ataques passivos contra a confidencialidade; modificação e falsificação ameaça
- n-spear-phishing-direcionado: Spear phishing é direcionado a vítima ou grupo específico com mensagem personalizada; o phishing comum é em ma
- n-vulnerabilidade-independe-ameaca: Vulnerabilidade é fragilidade explorável que existe independentemente de ameaça ativa; o risco combina ameaça 
- n-wardriving-vs-ap-spoofing: Wardriving mapeia redes sem fio circulando por uma região; access point spoofing cria ponto de acesso falso pa
- n-mitre-attack-aplicacoes: MITRE ATT&CK é base de táticas e técnicas de adversários usada em entendimento de ameaças, caça a ameaças, res
- n-xss-xxe-sao-vulnerabilidades: XSS e XXE são vulnerabilidades/ataques, não controles; boas práticas incluem validação, codificação de saída e
- n-sql-from-relacao-where-predicado: Em SQL, a cláusula FROM indica as relações (tabelas) consultadas, SELECT define as colunas projetadas e WHERE 
- n-particionamento-tabelas-desempenho: Particionar tabelas grandes em partições menores melhora a gestão de armazenamento e pode melhorar o desempenh
- n-indices-leitura-vs-escrita: Índices aceleram leituras, mas consomem armazenamento e encarecem inserções, atualizações e exclusões
- n-nosql-nao-exclusivo-documentos: Bancos não relacionais incluem vários modelos (documento, chave-valor, colunar, grafo); não se resumem a objet
- n-left-join-on-chaves: A cláusula ON define a condição de junção, comparando a chave estrangeira com a chave primária correspondente 
- n-view-group-by-order-by: Uma view armazena uma consulta nomeada; com JOIN, GROUP BY, SUM e ORDER BY (inclusive por posição da coluna) l
- n-having-subconsulta-media: HAVING filtra grupos após a agregação e pode comparar SUM com subconsulta escalar (AVG geral), listando grupos
- n-exists-vs-not-exists: EXISTS retorna linhas para as quais a subconsulta encontra correspondência; para listar quem não tem registros
- n-nosql-documento-vs-relacional: No modelo de documentos, coleção equivale a tabela e documento equivale a linha (registro), campo equivale a c
- n-indices-bi-tabelas-fato-dimensao: Em bases para BI, índices (colunas, compostos, bitmap) em tabelas de fatos e dimensões aceleram consultas anal
- n-indice-clusterizado-ordem-fisica: Índice clusterizado (ou clusterização de tabela) ordena fisicamente os dados segundo as colunas do índice, com
- n-select-privilegio-hierarquia: Privilégio SELECT concedido em nível hierárquico (esquema/banco) abrange objetos existentes e futuros, simplif
- n-sql-select-from-le-coluna: SELECT ... FROM lê colunas de uma tabela
- n-grant-select-coluna: GRANT SELECT em colunas específicas ON tabela TO PUBLIC concede leitura apenas àquelas colunas a todos os usuá
- n-delete-not-exists-correlacionada: DELETE com NOT EXISTS e subconsulta correlacionada remove registros sem correspondência na outra tabela (regis
- n-or-vs-union-desempenho: Em colunas indexadas distintas, substituir OR por UNION de duas consultas pode ser mais eficiente por permitir
- n-conversao-tipo-where-indice: Conversão de tipo aplicada a coluna ou parâmetro no WHERE pode inibir o uso de índice e afetar desempenho; com
- n-cte-with-escopo-consulta: A cláusula WITH (CTE) define relação temporária disponível apenas à consulta em que ocorre
- n-dml-nao-altera-esquema: Comandos DML (INSERT, UPDATE, DELETE) alteram os dados, não o esquema do banco; alterar o esquema é função de 
- n-update-case: UPDATE com CASE aplica atualizações condicionais em um único comando, evitando problemas de ordem entre múltip
- n-sql-distinct-elimina-duplicatas: DISTINCT elimina linhas repetidas no resultado de uma consulta
- n-where-filtra-linhas: A cláusula WHERE filtra linhas, podendo retornar de zero ao total de linhas da tabela
- n-colunas-mesmo-nome-qualificar: Atributos de mesmo nome em tabelas distintas devem ser qualificados com a tabela/alias na consulta para evitar
- n-left-join-on-true-where: LEFT OUTER JOIN com ON TRUE seguido de WHERE na chave equivale a junção interna, excluindo linhas sem correspo
- n-indice-nao-garante-ganho: Índice não garante ganho de desempenho: colunas de baixa seletividade (muita duplicidade) rendem pouco, e índi
- n-indice-coluna-where-melhora-consulta: Índices em colunas usadas em WHERE e junções podem melhorar significativamente o desempenho de consultas, ao c
- n-remover-indice-melhora-escrita: A análise de planos de execução pode revelar índices não usados cuja exclusão melhora o desempenho, sobretudo 
- n-subconsulta-vs-join: Subconsultas e tabelas aninhadas não costumam superar JOIN em desempenho; o otimizador geralmente favorece JOI
- n-indice-estrutura-ponteiros: Índice é estrutura auxiliar ordenada por um critério, com ponteiros para a localização física das linhas; não 
- n-view-virtual: View é tabela virtual definida por consulta; não armazena dados fisicamente (exceto visão materializada) e é r
- n-view-vs-view-materializada: View é consulta armazenada que não guarda dados fisicamente; view materializada armazena fisicamente o resulta
- n-role-controle-acesso-vs-stored-procedure: Role agrupa privilégios para controle de acesso; lógica de negócio no banco é implementada por stored procedur
- n-bloom-filter-igualdade: Filtro Bloom é estrutura probabilística eficiente em espaço que testa pertinência a conjunto, suportando consu
- n-dml-select-agrupamento-avg: Consulta com AVG e GROUP BY retorna uma linha por grupo com a média do atributo
- n-indice-chave-pesquisa-qualquer-subconjunto: Qualquer subconjunto dos campos de uma relação pode servir de chave de pesquisa de um índice
- n-sql-union-elimina-duplicatas: UNION elimina linhas duplicadas do resultado; UNION ALL as mantém
- n-otimizador: O otimizador de consultas gera um plano de execução equivalente (mesmo resultado) à expressão original, escolh
- n-dcl-grant-revoke-deny: DCL controla autorizações e privilégios de acesso por GRANT (conceder), REVOKE (revogar) e DENY (negar, em alg
- n-sql-produto-cartesiano-sem-juncao: SELECT sobre mais de uma tabela sem condição de junção/WHERE gera produto cartesiano; a cláusula WHERE restrin
- n-sql-update-subconsulta-max: UPDATE pode atribuir a uma coluna o resultado de subconsulta com agregação (MAX), restrito pelo WHERE às linha
- n-sql-case-when-ordem-avaliacao: CASE avalia as condições em ordem e retorna o resultado da primeira verdadeira, sem erro por faixas abertas; v
- n-sql-drop-table-vs-truncate-delete-table: DROP TABLE exclui tabela inteira (estrutura, dados e objetos associados); TRUNCATE só esvazia mantendo a estru
- n-oracle-v-sort-segment-espaco-ordenacao: O espaço de ordenação no Oracle é informado por visões dinâmicas de desempenho, como V$SORT_SEGMENT
- n-sql-group-by-sem-agregada: GROUP BY pode ser usado sem funções agregadas; ORDER BY não é condição para isso
- n-sql-update-altera-linhas-modify-inexistente: UPDATE é o comando SQL que altera linhas existentes; MODIFY não é comando de atualização de dados
- n-sql-comandos-em-sgbd-relacional: SELECT, INSERT, UPDATE e DELETE são comandos SQL aplicáveis em SGBDs relacionais
- n-sql-grant-select-somente-leitura: GRANT SELECT concede apenas permissão de leitura; inserir registros exige o privilégio INSERT
- n-sql-insert-into-values-sintaxe: A sintaxe de inserção é INSERT INTO tabela VALUES (...) ; a ordem INSERT VALUES ... INTO é inválida e uma list
- n-sql-null-aritmetica-resulta-null: Expressão aritmética com NULL resulta em NULL, não no valor do outro operando
- n-sql-count-avg-ignoram-null: COUNT(coluna) e AVG ignoram valores NULL; COUNT(*) conta todas as linhas
- n-nosql-documental-aninhamento-evita-juncao: Em NoSQL documental o aninhamento de estruturas evita junções e melhora a leitura
- n-sql-select-juncao-where-dql-vs-dml: Consultas SELECT (inclusive com INNER JOIN e WHERE) são DQL (consulta de dados), distintas da DML (INSERT, UPD
- n-indice-ordem-fisica-independe-logica: A organização física do índice (ordenada por chave de busca) independe da ordem lógica em que é definido e da 
- n-group-by-count-por-grupo: SELECT col, COUNT(*) ... GROUP BY col retorna a quantidade de linhas de cada valor de col
- n-sql-group-by-cube-subtotais: GROUP BY CUBE gera agregações para todas as combinações das colunas (subtotais e total geral), não só os grupo
- n-owasp-fatores-vulnerabilidade-so-sgbd-bibliotecas: Fatores de vulnerabilidade incluem SO, servidor web, SGBD, APIs, bibliotecas e ambientes de execução
- n-sql-declarativa-nao-imperativa: SQL é linguagem padrão ANSI declarativa para bancos relacionais; não é imperativa para criar programas complet
- n-tsql-extensao-sql-server-sybase: T-SQL é extensão procedural da linguagem SQL usada no SQL Server (e também no Sybase)
- n-sql-group-by-colunas-nao-agregadas-juncao: Em consulta agregada, colunas não agregadas devem constar no GROUP BY e a condição de junção deve relacionar a
- n-plano-execucao-tecnica-otimizacao: Analisar o plano de execução das consultas SQL é técnica usual de otimização de desempenho do banco
- n-sql-references-insert-colunas-incompativeis: Chave estrangeira em CREATE TABLE usa REFERENCES; INSERT com mais valores que colunas gera erro
- n-mysql-show-open-tables-in-use: No MySQL, SHOW OPEN TABLES WHERE In_use > 0 lista as tabelas em uso
- n-right-join-count-coluna: RIGHT JOIN preserva todas as linhas da tabela da direita (com NULL na esquerda sem correspondência); COUNT(col
- n-chave-valor-consulta-limitada: Bancos chave-valor atendem Big Data com bom desempenho, mas costumam ter recursos de consulta limitados e norm
- n-alter-table-renomear-coluna: Renomear coluna usa ALTER TABLE ... RENAME COLUMN antigo TO novo (ou CHANGE no MySQL); MODIFY COLUMN altera ti
- n-left-join-preserva-tabela-esquerda: LEFT JOIN preserva todas as linhas da tabela da esquerda, mesmo sem correspondência na direita; para listar só
- n-join-implicito-group-by-contagem: Junção por WHERE entre tabelas combinada com GROUP BY e COUNT retorna a quantidade de registros relacionados p
- n-oracle-flashback-before-drop: No Oracle, com RECYCLEBIN em ON, FLASHBACK TABLE nome TO BEFORE DROP recupera tabela removida com DROP
- n-tcl-commit-rollback: COMMIT e ROLLBACK são comandos de controle de transação (TCL), não de DML, que reúne INSERT, UPDATE e DELETE
- n-limit-offset-mysql: No MySQL, LIMIT a, b pula a linhas (offset) e retorna b registros
- n-crud-create-read-update-delete: CRUD = Create, Read, Update, Delete, correspondendo a INSERT, SELECT, UPDATE e DELETE nessa ordem
- n-sql-linguagem-padrao-ddl-dml: SQL é a linguagem padrão dos bancos relacionais para definir esquema (DDL) e acessar dados (DML/consulta)
- n-cursor-percorre-resultado-linha-a-linha: Cursor mantém o conjunto de linhas de uma consulta e permite percorrê-lo linha a linha; não guarda uma única l
- n-grant-option-repassa-privilegio: GRANT ... WITH GRANT OPTION concede o privilégio e permite ao beneficiário repassá-lo a outros usuários
- n-ctas-nao-copia-constraints-indices: CREATE TABLE ... AS SELECT copia estrutura e dados, mas geralmente não replica chaves, constraints e índices d
- n-insert-com-sem-lista-colunas: INSERT sem lista de colunas segue a ordem da tabela; com lista, mapeia por nome. Se a lista cobre as colunas n
- n-monitoramento-ajuste-desempenho-bd: Monitorar e ajustar o banco (consultas, índices, estatísticas) reduz tempo de resposta e ajuda a detectar prob
- n-ddl-define-estruturas-metadados: DDL cria e altera estruturas, tipos e restrições do banco, e seu processamento atualiza o catálogo de metadado
- n-agregacao-sem-group-by: Funções de agregação como AVG funcionam sem GROUP BY (resultado único); GROUP BY só agrupa por colunas
- n-replicas-leitura-desafogam-principal: Réplicas de leitura desafogam o servidor principal ao receber consultas pesadas
- n-tipos-de-join-ansi: O padrão SQL tem também FULL OUTER JOIN (além de INNER, LEFT, RIGHT e CROSS) e NATURAL JOIN; a lista não é lim
- n-view-atualizacao-traduzida-relacoes-base: Operações sobre views precisam ser traduzidas para as tabelas base e podem sofrer restrições, sobretudo em atu
- n-indice-btree-vs-hash-intervalo: Índice B-tree é preferível ao hash em consultas por intervalo, pois mantém as chaves ordenadas; hash serve a i
- n-union-colunas-compativeis: UNION exige SELECTs com o mesmo número de colunas e tipos compatíveis; não une quaisquer consultas
- n-dml-procedural-e-declarativa: DML pode ser procedural (especifica como obter os dados) ou declarativa/não procedural; SQL é declarativa, mas
- n-otimizacao-heuristica-vs-custo: Otimização heurística reescreve a árvore de consulta por regras; a baseada em custo usa seletividade e estimat
- n-otimizacao-semantica-restricoes: Otimização semântica usa restrições de integridade para reescrever consultas, e em princípio qualquer restriçã
- n-estatisticas-plano-consulta: O otimizador usa estatísticas do banco para estimar custos e escolher o plano de consulta mais econômico
- n-bitmap-null: Índices bitmap (Oracle) indexam linhas com valores NULL, ao contrário dos índices B-tree, que em geral não inc
- n-bitmap-part: Em tabelas particionadas no Oracle, índices bitmap só podem ser locais, não globais
- n-pg-shared: No PostgreSQL, shared_buffers define a memória de cache do SGBD, mas o banco ainda usa o cache de página do si
- n-select-mineracao: SELECT é consulta que recupera dados armazenados; não é mineração de dados, que busca padrões e conhecimento n
- n-sqlplus-var: No SQL*Plus, variáveis de substituição (&var) podem ser usadas em comandos SQL, inclusive DML; bloco anônimo P
- n-maior-grupo: A linha de maior valor por grupo (ex.: última versão) obtém-se com join com subconsulta MAX/GROUP BY ou com LE
- n-notin-leftjoin: NOT IN (subconsulta) e LEFT JOIN com DISTINCT não são equivalentes: o LEFT JOIN devolve também as linhas com c
- n-pg-immutable: No PostgreSQL, função marcada IMMUTABLE não modifica o banco e retorna sempre o mesmo resultado para os mesmos
- n-bloco-dss: Sistemas de apoio à decisão e data warehouse, com leitura sequencial de grandes volumes, tendem a se beneficia
- n-oracle-bloco: No Oracle, o bloco de dados tem cabeçalho e área de dados, e as linhas das tabelas são armazenadas em colunas 
- n-autojoin: Autojunção exige aliases distintos e colunas qualificadas por alias nas condições de junção e de filtro; condi
- n-idx-secundario: Índice secundário é usado quando o campo indexado não é a chave primária da tabela
- n-except: EXCEPT retorna as linhas da primeira consulta ausentes na segunda e elimina duplicatas
- n-create-db: CREATE DATABASE cria um banco de dados; tabelas são criadas com CREATE TABLE
- n-pg-maxconn: No PostgreSQL, max_connections é parâmetro global do servidor, consultado com SHOW max_connections ou pg_setti
- n-where-having: WHERE filtra linhas antes do agrupamento; HAVING filtra grupos após a agregação (ex.: HAVING COUNT(*) > 5)
- n-select-ddl: SELECT é comando de consulta (DQL/DML), não de controle; comandos de controle de acesso são GRANT e REVOKE (DC
- n-nosql-idx: Bancos NoSQL documentais, mesmo sem esquema fixo, permitem definir índices sobre campos dos documentos
- n-sqlserver-xe: Extended Events do SQL Server é mecanismo leve e flexível de monitoramento e diagnóstico que substitui o SQL P
- n-tuning-dist: Em sistemas distribuídos, o tuning envolve particionamento entre nós, cache distribuído, ajuste de rede, latên