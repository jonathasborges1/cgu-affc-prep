# PACOTE tema-p3-dados-1-top (20 itens)
Para cada item: edital (código de CANDIDATOS ou FORA), núcleo, tags, nível. Gabarito: C=certo E=errado.

## 1 | gab=C | cand: P3·DADOS 1.2, P2·TRANSP 1.2, P2·EVID 5.2
Os bancos de dados NoSQL do tipo documento ampliam o conceito do banco de dados do tipo chave-valor, pois organizam os documentos inteiros em grupos chamados coleções.
## 2 | gab=C | cand: P3·DADOS 1.2, P3·ENG 2.1, P3·DADOS 1.4
Um banco de dados de chave-valor armazena dados como um conjunto de pares de chave-valor em que uma chave atua como identificador exclusivo. JUSTIFICATIVA - Certo. Um banco de dados de chave-valor é um tipo de banco de dados não relacional, também conhecido como banco de dados NoSQL, que usa um método simples de chave-valor para armazenar dados. Ele armazena dados como um conjunto de pares de chave-valor em que uma c
## 3 | gab=E | cand: P3·DADOS 1.2, P3·DADOS 1.4, P1·ETICA 5.1
O exemplo a seguir exibe como os dados podem ser armazenados em um banco de dados relacional do tipo chave-valor. { nome_orgao: “ANATEL”, endereco: {estado: “Distrito Federal”, cidade: “Brasília”}, numero_telefone: “55-61-1234-5678”, atuacao: [“telecomunicação”], } Nos bancos de dados NoSQL orientados a colunas, é possível organizar os dados em famílias de colunas, o que facilita o agrupamento e o acesso a informaçõe
## 4 | gab=E | cand: P3·DADOS 1.2, P3·DADOS 1.8, P3·DADOS 1.9
Uma big data não engloba dados não estruturados, mas inclui um imenso volume de dados estruturados suportado por tecnologias como o DataMining e o DataWarehouse para a obtenção de conhecimento a partir da manipulação desses dados. Os bancos de dados NoSQL não permitem a atualização de seus dados, por serem orientados a documentos e(ou) coleções. O processo de normalização provê tanto a análise de desempenho quanto a 
## 5 | gab=C | cand: P3·DADOS 1.7, P3·DADOS 1.8, P3·DADOS 1.6
Se a estratégia de carregamento for definida como Eager na relação @OneToMany entre a entidade Pedido e a entidade Item, o Hibernate automaticamente carregará todos os itens relacionados ao pedido assim que o pedido for consultado.
## 6 | gab=E | cand: P3·DADOS 1.2, P3·ENG 2.5, P3·ENG 2.1
Em que pese o fato de não serem particionáveis, os bancos de dados do tipo chave-valor, por possuírem estrutura maleável aos dados, permitem o armazenamento de objetos complexos, proporcionando escalabilidade vertical de forma mais fácil que os do tipo orientado a documento.
## 7 | gab=E | cand: P3·DADOS 1.4, P3·DADOS 1.8, P3·SEG 5.3
Considere que, em um banco de dados relacional que armazena dados a respeito de licitações, a tabela licitacoes possua os seguintes campos: id_licitacao, id_fornecedor, quantidade, preco_unitario, data_licitacao e valor_total. Considere, ainda, que esse último campo seja o resultado da multiplicação do campo quantidade pelo campo preco_unitario. Nesse caso, a tabela em questão está em conformidade com a terceira form
## 8 | gab=C | cand: P3·DADOS 1.7, P3·ENG 5.4, P2·GOV 2.2
No clean code, o princípio da responsabilidade única estabelece que uma classe deve ter uma única responsabilidade clara, evitando-se múltiplas razões para mudanças, o que melhora a coesão, a manutenibilidade e a extensibilidade do código. Em determinado banco de dados, a entidade Pedido está mapeada com uma relação @OneToMany com a entidade Item, configurada com a estratégia de carregamento Eager. A partir da situaç
## 9 | gab=E | cand: P3·DADOS 1.9, P3·ARQ 1.7, P1·ETICA 5.1
Modelos de dados lógicos fornecem maiores detalhes acerca dos conceitos e relacionamentos no domínio em consideração, indicando atributos de dados, como tipos de dados e seus respectivos comprimentos, e relacionamentos entre entidades, além de informar como será organizado e quais regras de negócios estão envolvidas.
## 10 | gab=E | cand: P3·DADOS 1.9, P3·ARQ 1.7, P3·DADOS 1.8
Na construção de um banco de dados, o modelo conceitual utiliza os requisitos de negócio, que são decompostos em entidades, atributos e relacionamentos atômicos, e aplica regras para evitar redundâncias.
## 11 | gab=E | cand: P3·DADOS 1.2, P3·DADOS 1.9, P3·DADOS 1.8
Em bancos de dados relacionais, quando uma tabela está na terceira forma normal (3FN), seus atributos dependem inteiramente da chave primária.
## 12 | gab=E | cand: P3·DADOS 1.6, P3·DADOS 1.2, P3·SEG 5.3
Dentre as dimensões do ITIL v4, os fluxos de processos e valor referem-se ao relacionamento da organização com outras entidades envolvidas no ciclo de vida dos serviços.
## 13 | gab=E | cand: P3·DADOS 1.8, P3·DADOS 1.2, P3·DADOS 1.9
O comando get clone incorpora as alterações de um repositório remoto no ramo atual. Acerca de fundamentos dos bancos de dados relacionais, normalização, diagrama entidade-relacionamento e linguagem SQL, julgue os itens a seguir.
## 14 | gab=C | cand: P3·DADOS 1.9, P3·DADOS 1.8, P3·DADOS 1.6
Considerado o conceito da solução ORM Hibernate, conclui-se que a hierarquia apresentada anteriormente está errada. O correto seria a hierarquia que se segue, uma vez que o Hibernate não se incorpora ao banco de dados relacional, mas se encontra entre a camada de acesso a dados do aplicativo Java e o banco de dados relacional. Data Access Layer Java Persistence    Hibernate Native API                  API Hibernate J
## 15 | gab=C | cand: P3·DADOS 1.2, P3·DADOS 1.9, P3·DADOS 1.8
Bancos de dados NoSQL, como MongoDB, são projetados para lidar com grandes volumes de dados não estruturados e são altamente escaláveis horizontalmente, enquanto bancos de dados SQL, como MySQL, são mais adequados para dados estruturados, suportando transações ACID.
## 16 | gab=E | cand: P3·DADOS 1.2, P3·DADOS 1.9, P3·DADOS 1.8
A principal diferença entre bancos de dados relacionais e bancos de dados NoSQL está na questão da segurança dos dados e das transações; os bancos de dados NoSql são imunes a ataques de injeção SQL.
## 17 | gab=C | cand: P3·DADOS 1.8, P3·DADOS 1.7, P3·DADOS 1.2
Extração, tratamento e carga (ETL) é o processo que coleta dados relevantes dos bancos de dados transacionais, transforma-os em um padrão e os carrega no data warehouse ou no data mart. OS ESPECÍFICOS -- No que         se refere    à    representação do diagrama entidade-relacionamento (ER) precedente, julgue os itens seguintes.
## 18 | gab=E | cand: P3·DADOS 1.9, P3·ARQ 1.7, P3·DADOS 2.1
Em uma aplicação desenvolvida em 3 camadas, a camada de dados é responsável pela guarda dos dados do repositório, cujo acesso e cuja manipulação são responsabilidades da camada de regras de negócio.
## 19 | gab=C | cand: P3·DADOS 1.5, P3·DADOS 1.9, P3·DADOS 1.8
A transformação do esquema de tabela não normalizada em um esquema relacional na primeira forma normal (1FN) consiste da eliminação das tabelas aninhadas. OS ESPECÍFICOS
## 20 | gab=C | cand: P3·DADOS 1.8, P3·DADOS 1.4, P3·DADOS 1.1 [texto-base: No que se refere aos protocolos DHCP e IMAP, aos sistemas de segurança IPS, aos modelos de nuvem, ao ambiente Linux e ao Microsoft Windows Server, julgue os itens a seguir.]
No modelo de nuvem pública, os serviços são disponibilizados para qualquer cliente, e recursos como servidores, armazenamento e aplicações são controlados pelo provedor desses serviços. OS ESPECÍFICOS -Julgue os itens seguintes, relativos à administração de banco de dados Oracle, à modelagem de dados relacional, à normalização de dados e ao data mining.

## CÓDIGOS CANDIDATOS (texto do edital)
- P1·ETICA 5.1: Coerência entre regras e práticas; ambiente organizacional e incentivos; canais de orientação e relato; papel do exemplo, da confiança e da prestação de contas.
- P2·EVID 5.2: Erros, conteúdo não sustentado, vieses e efeitos sobre grupos; proteção de informações, supervisão, rastreabilidade e contestação.
- P2·GOV 2.2: Identificação de vulnerabilidades e de controles compatíveis com situações usuais, a partir dos dados fornecidos.
- P2·TRANSP 1.2: Distinção conceitual entre informação classificada, sigilos previstos em lei, informação pessoal e documento preparatório; acesso parcial e comunicação clara da
- P3·ARQ 1.7: Construção de serviços REST e separação entre apresentação, regras de negócio e acesso a dados.
- P3·DADOS 1.1: Modelagem relacional, normalização e integridade.
- P3·DADOS 1.2: Bancos documentais, chave-valor e vetoriais.
- P3·DADOS 1.4: Escolha de armazenamento conforme uso.
- P3·DADOS 1.5: Transações, concorrência, consistência e evolução de esquemas.
- P3·DADOS 1.6: Persistência em Java com JPA: mapeamento de entidades e relacionamentos, ciclo de vida das entidades, contexto de persistência, consultas e transações.
- P3·DADOS 1.7: Estratégias de carregamento e seus efeitos sobre correção e desempenho.
- P3·DADOS 1.8: Spring Data JPA: repositórios, consultas e paginação.
- P3·DADOS 1.9: Integração da camada de persistência às regras de negócio.
- P3·DADOS 2.1: Definição e manipulação de dados, controle de acesso e transações.
- P3·ENG 2.1: Linguagem Java: tipos de dados, estruturas de controle, métodos, classes e objetos.
- P3·ENG 2.5: Estruturas de dados, algoritmos e pseudocódigo.
- P3·ENG 5.4: Impactos das mudanças e das falhas sobre a continuidade e a qualidade dos serviços.
- P3·SEG 5.3: Viabilidade, dimensionamento, custo total de propriedade e pesquisa de preços.

## NÚCLEOS JÁ EXISTENTES (reutilize o id se for a mesma ideia)
- n-tres-camadas-regras-negocio: Em arquitetura de três camadas a lógica de negócio fica na camada intermediária, mas validações também podem o
- n-integridade-referencial-fk-pk: Integridade referencial garante que os valores de uma chave estrangeira correspondam a valores existentes na c
- n-bd-federado-distribuido: Em banco federado cada banco mantém estrutura e gestão próprias e a federação permite acesso e consulta centra
- n-nosql-nao-exclusivo-documentos: Bancos não relacionais incluem vários modelos (documento, chave-valor, colunar, grafo); não se resumem a objet
- n-modelagem-logica-tabelas-colunas: A modelagem lógica define tabelas, colunas e tipos de dados de cada coluna, independentemente do SGBD físico
- n-nosql-documento-vs-relacional: No modelo de documentos, coleção equivale a tabela e documento equivale a linha (registro), campo equivale a c
- n-banco-em-memoria: Bancos em memória armazenam e processam dados na memória principal, com acesso mais rápido que bancos baseados
- n-pf: Pontos de função brutos dependem da quantidade e da complexidade das funções de dados e de transação de cada a
- n-select-privilegio-hierarquia: Privilégio SELECT concedido em nível hierárquico (esquema/banco) abrange objetos existentes e futuros, simplif
- n-unique-chave-alternativa: A restrição UNIQUE garante unicidade de chaves alternativas (candidatas que não são a chave primária)
- n-grant-select-coluna: GRANT SELECT em colunas específicas ON tabela TO PUBLIC concede leitura apenas àquelas colunas a todos os usuá
- n-atributo-derivado: Atributo derivado é calculado a partir de outro (idade a partir da data de nascimento) e não precisa ser armaz
- n-dml-nao-altera-esquema: Comandos DML (INSERT, UPDATE, DELETE) alteram os dados, não o esquema do banco; alterar o esquema é função de 
- n-update-case: UPDATE com CASE aplica atualizações condicionais em um único comando, evitando problemas de ordem entre múltip
- n-depurador-tsql: O depurador Transact-SQL permite depurar stored procedures interativamente, com pilha de chamadas, variáveis, 
- n-tabelas-linhas-colunas-chaves: Em bancos relacionais, tabelas (relações) são compostas por linhas (registros/tuplas) e colunas (atributos), l
- n-sgbd-controla-redundancia: O SGBD controla redundância e integridade por meio de restrições, mas não elimina automaticamente toda duplica
- n-chave-primaria-identifica-registro: Chave primária é o conjunto de um ou mais atributos que identifica unicamente cada registro da tabela
- n-independencia-de-dados: Independência de dados: o SGBD mantém a descrição dos dados (metadados) separada das aplicações, que não preci
- n-acid-propriedades: ACID: Atomicidade, Consistência, Isolamento e Durabilidade garantem a confiabilidade das transações
- n-relacionamento-nn-tabela-associativa: Relacionamento N:N no modelo lógico gera tabela associativa, totalizando três tabelas no modelo físico (duas e
- n-view-virtual: View é tabela virtual definida por consulta; não armazena dados fisicamente (exceto visão materializada) e é r
- n-esquema-banco-definicao: Esquema de banco de dados é a descrição da estrutura (tabelas, colunas, relacionamentos, restrições), distinta
- n-view-vs-view-materializada: View é consulta armazenada que não guarda dados fisicamente; view materializada armazena fisicamente o resulta
- n-transacao-atomicidade-acid: Atomicidade (ACID): a transação é efetivada por completo ou revertida, sem atualização parcial
- n-role-controle-acesso-vs-stored-procedure: Role agrupa privilégios para controle de acesso; lógica de negócio no banco é implementada por stored procedur
- n-innodb-acid-mvcc-clustered: O InnoDB do MySQL suporta transações ACID, bloqueio em nível de linha e MVCC e organiza os dados em índice clu
- n-keyset-cursor-vs-static: Cursor keyset-driven fixa o conjunto de chaves e reflete alterações nos valores das linhas; o cursor estático 
- n-dcl-grant-revoke-deny: DCL controla autorizações e privilégios de acesso por GRANT (conceder), REVOKE (revogar) e DENY (negar, em alg
- n-sql-update-subconsulta-max: UPDATE pode atribuir a uma coluna o resultado de subconsulta com agregação (MAX), restrito pelo WHERE às linha
- n-view-esquema-externo-independencia-logica: Visões definem esquemas externos e isolam as aplicações das mudanças do esquema conceitual (independência lógi
- n-sql-drop-table-vs-truncate-delete-table: DROP TABLE exclui tabela inteira (estrutura, dados e objetos associados); TRUNCATE só esvazia mantendo a estru
- n-jdbc-executeupdate-vs-resultset: No JDBC, executeUpdate() recebe comando SQL de atualização e retorna a contagem de linhas afetadas, não um Res
- n-log-wal-redo-undo-recuperacao: Com log de transações (WAL), após falha as transações confirmadas são refeitas e as não confirmadas desfeitas 
- n-normalizacao-vs-escala-indice-composto: Normalização organiza tabelas para reduzir redundância e anomalias; não é escalonamento de valores nem criação
- n-apf-consulta-implicita: Em pontos de função, consulta implícita ocorre quando a aplicação apresenta dados sem solicitação explícita do
- n-metadados-descrevem-dados: Metadados são informações estruturadas que descrevem os dados e permitem manipulá-los com eficiência
- n-sql-update-altera-linhas-modify-inexistente: UPDATE é o comando SQL que altera linhas existentes; MODIFY não é comando de atualização de dados
- n-oracle-trigger-invoca-procedure: Gatilhos (triggers) do Oracle podem invocar procedimentos armazenados e são disparados implicitamente
- n-replicacao-sincrona-consistencia: Replicação síncrona aplica a transação em todas as réplicas antes de concluí-la, mantendo consistência forte e
- n-sql-comandos-em-sgbd-relacional: SELECT, INSERT, UPDATE e DELETE são comandos SQL aplicáveis em SGBDs relacionais
- n-sql-grant-select-somente-leitura: GRANT SELECT concede apenas permissão de leitura; inserir registros exige o privilégio INSERT
- n-xa-datasource-transacao-distribuida: XA datasource serve a transações distribuídas coordenadas entre múltiplos recursos; transações locais usam dat
- n-sql-insert-into-values-sintaxe: A sintaxe de inserção é INSERT INTO tabela VALUES (...) ; a ordem INSERT VALUES ... INTO é inválida e uma list
- n-chave-candidata-varias-primaria-unica: Uma tabela pode ter várias chaves candidatas, mas somente uma chave primária
- n-stored-procedure-precompilada-reduz-trafego: Stored procedures são armazenadas no banco, pré-compiladas, e reduzem tráfego de rede melhorando o desempenho
- n-mvc-view-nao-acessa-dados-model: No MVC o acesso e a manipulação de dados cabem ao model; a view apenas apresenta, sem obrigação de acessar o b
- n-nosql-documental-aninhamento-evita-juncao: Em NoSQL documental o aninhamento de estruturas evita junções e melhora a leitura
- n-sql-select-juncao-where-dql-vs-dml: Consultas SELECT (inclusive com INNER JOIN e WHERE) são DQL (consulta de dados), distintas da DML (INSERT, UPD
- n-postgresql-deadlock-deteccao-automatica: O PostgreSQL detecta deadlock automaticamente e aborta uma das transações, sendo difícil prever qual
- n-sql-declarativa-nao-imperativa: SQL é linguagem padrão ANSI declarativa para bancos relacionais; não é imperativa para criar programas complet
- n-relacao-conjunto-tuplas-sem-ordem: No modelo relacional, relação é conjunto de tuplas e, por ser conjunto, não há ordem entre elas
- n-python-cursor-execute-string-sql: cursor.execute() executa consulta SQL passada como string em bibliotecas de acesso a banco em Python
- n-jpa-ordercolumn-persiste-ordem-lista: O JPA 2.0 permite manter a ordem de listas de objetos no banco (OrderColumn)
- n-postgresql-select-access-share: No PostgreSQL, SELECT adquire o bloqueio ACCESS SHARE nas tabelas referenciadas
- n-tsql-extensao-sql-server-sybase: T-SQL é extensão procedural da linguagem SQL usada no SQL Server (e também no Sybase)
- n-sql-references-insert-colunas-incompativeis: Chave estrangeira em CREATE TABLE usa REFERENCES; INSERT com mais valores que colunas gera erro
- n-integridade-referencial-fk-admite-null: Integridade referencial exige que a chave estrangeira corresponda a valor existente na tabela referenciada, ma
- n-chave-valor-consulta-limitada: Bancos chave-valor atendem Big Data com bom desempenho, mas costumam ter recursos de consulta limitados e norm
- n-integridade-entidade-pk-nao-nula: Integridade de entidade exige que a chave primária seja única e nunca nula; pertencer a um domínio de valores 
- n-alter-table-renomear-coluna: Renomear coluna usa ALTER TABLE ... RENAME COLUMN antigo TO novo (ou CHANGE no MySQL); MODIFY COLUMN altera ti
- n-oracle-flashback-before-drop: No Oracle, com RECYCLEBIN em ON, FLASHBACK TABLE nome TO BEFORE DROP recupera tabela removida com DROP
- n-tcl-commit-rollback: COMMIT e ROLLBACK são comandos de controle de transação (TCL), não de DML, que reúne INSERT, UPDATE e DELETE
- n-crud-create-read-update-delete: CRUD = Create, Read, Update, Delete, correspondendo a INSERT, SELECT, UPDATE e DELETE nessa ordem
- n-normalizacao-excessiva-desnormalizacao: Normalização excessiva pode prejudicar consultas complexas (muitas junções), mas não deve ser 'sempre' evitada
- n-transacao-multiplas-operacoes: Uma transação agrupa uma ou mais operações de leitura e/ou escrita no banco como unidade lógica
- n-mvc-controller-fluxo: No MVC, o Controller coordena o fluxo entre a camada de apresentação (View) e o modelo/dados, separando respon
- n-integridade-nao-dispensa-controles: Integridade de dados depende de restrições, transações e controles de segurança/proteção; não é mantida automa
- n-sql-linguagem-padrao-ddl-dml: SQL é a linguagem padrão dos bancos relacionais para definir esquema (DDL) e acessar dados (DML/consulta)
- n-esquema-agrupamento-logico: Esquema é agrupamento lógico de objetos do banco (namespace); não divide fisicamente tabelas nem impede acesso
- n-pk-composta-por-chaves-estrangeiras: Uma chave primária pode ser composta por duas ou mais colunas, inclusive colunas que são chaves estrangeiras (
- n-grant-option-repassa-privilegio: GRANT ... WITH GRANT OPTION concede o privilégio e permite ao beneficiário repassá-lo a outros usuários
- n-ctas-nao-copia-constraints-indices: CREATE TABLE ... AS SELECT copia estrutura e dados, mas geralmente não replica chaves, constraints e índices d
- n-durabilidade-persistencia-commit: Durabilidade garante que efeitos de transação confirmada persistam mesmo com falhas; atomicidade é tudo-ou-nad
- n-insert-com-sem-lista-colunas: INSERT sem lista de colunas segue a ordem da tabela; com lista, mapeia por nome. Se a lista cobre as colunas n
- n-trigger-vs-procedimento: Trigger (gatilho) dispara automaticamente em eventos INSERT/UPDATE/DELETE; stored procedure é chamada explicit
- n-ddl-define-estruturas-metadados: DDL cria e altera estruturas, tipos e restrições do banco, e seu processamento atualiza o catálogo de metadado
- n-modificacao-adiada-log-write: Na modificação adiada, as alterações vão ao log e os WRITEs só são executados após a confirmação parcial da tr
- n-view-atualizacao-traduzida-relacoes-base: Operações sobre views precisam ser traduzidas para as tabelas base e podem sofrer restrições, sobretudo em atu
- n-pseudocodigo-heron-area-negativa: Em pseudocódigo, rastreie os valores: com lados 3, 4 e 8 o produto de Heron é negativo e o algoritmo exibe a m
- n-dml-procedural-e-declarativa: DML pode ser procedural (especifica como obter os dados) ou declarativa/não procedural; SQL é declarativa, mas
- n-locks-isolamento: Bloqueios (locks) controlam concorrência e garantem isolamento, não atomicidade
- n-bd-distribuido-transparencia-consulta: Em banco de dados distribuído, quando um servidor não tem os dados solicitados, obtém-nos de outro servidor e 
- n-sgbd-construir-manipular: O SGBD permite definir, construir, manipular e compartilhar bancos de dados
- n-banco-dados-conjunto-coerente: Banco de dados é um conjunto lógico e coerente de dados relacionados, que representa aspectos do mundo real
- n-sqlplus-var: No SQL*Plus, variáveis de substituição (&var) podem ser usadas em comandos SQL, inclusive DML; bloco anônimo P
- n-pg-immutable: No PostgreSQL, função marcada IMMUTABLE não modifica o banco e retorna sempre o mesmo resultado para os mesmos
- n-orm-hibernate: Hibernate é framework ORM em Java que mapeia classes a tabelas e gera os comandos SQL
- n-jdbc-driver-url: Em JDBC, Class.forName recebe o nome da classe do driver e DriverManager.getConnection recebe a URL de conexão
- n-3fn: Na 3FN, atributos não-chave dependem apenas da chave; grupos de campos que se repetem para vários registros vã
- n-sgbd: O SGBD retira da aplicação cliente a responsabilidade de gerenciar acesso, persistência, manipulação e organiz
- n-create-db: CREATE DATABASE cria um banco de dados; tabelas são criadas com CREATE TABLE
- n-select-ddl: SELECT é comando de consulta (DQL/DML), não de controle; comandos de controle de acesso são GRANT e REVOKE (DC
- n-replicacao: A replicação em banco distribuído melhora o desempenho de leitura e a disponibilidade dos dados
- n-nosql-idx: Bancos NoSQL documentais, mesmo sem esquema fixo, permitem definir índices sobre campos dos documentos
- n-pg-toast: TOAST do PostgreSQL armazena valores grandes fora da linha principal (compressão e tabela auxiliar), permitind
- n-norm: A normalização reduz a redundância e melhora a integridade dos dados, podendo impactar o desempenho (mais junç