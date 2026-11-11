# PACOTE tema-p3-dados-2 (328 itens)
Para cada item: edital (código de CANDIDATOS ou FORA), núcleo, tags, nível. Gabarito: C=certo E=errado.
TEMA ALVO: P3·DADOS 2. Para cada item, use PRIMEIRO os códigos do tema alvo (lista abaixo); FORA só se nenhum código da lista toda (alvo + candidatos) tratar do assunto.

## 1 | gab=E | cand: 
Em uma consulta SQL, a cláusula FROM corresponde à seleção do predicado que envolve atributos da relação determinada pela cláusula SELECT.
## 2 | gab=C | cand: P3·DADOS 1.2, P3·DADOS 3.5
Integridade referencial, chaves e integridade de junções de relações são restrições características dos bancos de dados relacionais estabelecidas para evitar aspectos indesejáveis no manuseio de tabelas, como repetição e perda de informação.
## 3 | gab=E | cand: P2·EVID 2.1, P3·DADOS 1.6 [texto-base: Acerca das linguagens procedurais para programação de stored procedures, bem como de técnicas de otimização de consultas SQL e NoSQL, julgue os itens subsecutivos.]
A divisão de tabelas maiores em partições menores é geralmente indicada no contexto do gerenciamento de espaço de armazenamento dos bancos de dados, porém evitá-la constitui medida técnica significativa para aprimorar a otimização de consultas SQL em dados localizados de grandes tabelas.
## 4 | gab=C | cand: P3·DADOS 3.7
Os índices em um banco de dados melhoram o desempenho das operações de leitura, mas podem aumentar os custos de armazenamento e impactar negativamente as operações de escrita.
## 5 | gab=C | cand: 
Em um banco de dados federado, cada banco de dados mantém sua estrutura e gerenciamento próprios, enquanto a federação permite que os bancos sejam acessados e consultados de maneira centralizada.
## 6 | gab=E | cand: 
Os bancos de dados não relacionais se diferenciam dos bancos de dados relacionais por utilizarem de forma exclusiva objetos codificados com estado armazenado em um atributo estruturado, em vez de tabelas com colunas e linhas. A seguir, são apresentadas as estruturas de duas tabelas, de nomes Custome
## 7 | gab=E | cand: P2·EVID 2.1, P3·ENG 3.2
A cláusula ON na consulta estabelece a condição para a junção das duas tabelas, especificando que o CustomerID da tabela Customers deve corresponder ao OrderID da tabela Orders.
## 8 | gab=E | cand: 
O ADABAS permite a comunicação com outros sistemas gerenciadores de banco de dados por meio do driver ODBC, desde que essa comunicação seja exclusivamente de consultas para uma única partição. OS ESPECÍFICOS -A respeito de arquitetura e política de armazenamento de dados e engenharia de dados, julgu
## 9 | gab=C | cand: P3·ENG 2.1, P3·DADOS 1.1
A modelagem lógica de um banco de dados inclui a determinação das tabelas necessárias e suas respectivas colunas, além da especificação dos tipos de dados para cada coluna.
## 10 | gab=C | cand: P3·SEG 5.6
sobre os dados A integridade referencial é uma propriedade que garante que os valores de uma chave estrangeira em uma tabela correspondem a valores existentes na chave primária da tabela referenciada. A figura a seguir representa um projeto de banco de dados para a análise de gastos em saúde por mun
## 11 | gab=C | cand: 
A consulta SQL a seguir cria uma view para listar o total de gastos por município e hospital, bem como agrupa os resultados por município e hospital, calcula a soma dos valores gastos e ordena os resultados, de forma decrescente, pelo maior gasto e, depois, pelo nome do município e do hospital. crea
## 12 | gab=C | cand: 
A execução da consulta SQL a seguir listará os nomes dos hospitais que tiveram gastos superiores à média geral de gastos. SELECT nome_hospital, sum(g.valor_gasto) total FROM gastos g JOIN hospital h ON g.id_hospital = h.id_hospital group by nome_hospital having sum(g.valor_gasto) > (SELECT AVG(valor
## 13 | gab=E | cand: 
A seguinte consulta SQL lista os hospitais que não tiveram gastos com fisioterapia. SELECT h.nome_hospital FROM hospital h WHERE EXISTS ( SELECT 1 FROM gastos g WHERE g.id_hospital = h.id_hospital AND g.id_tipo_gasto_saude = (SELECT id_tipo_gasto_saude FROM tipo_gasto_saude WHERE nome_tipo_gasto = '
## 14 | gab=E | cand: P3·DADOS 1.2, P1·ADM 2.1
No modelo orientado a documentos, um documento é equivalente a uma tabela no modelo relacional, uma coleção é equivalente a uma linha (ou registro), um campo é equivalente a uma coluna, e um índice de documento é equivalente a um índice.
## 15 | gab=C | cand: P2·EVID 2.1, P2·AUD 1.2
Esses bancos de dados são caracterizados por armazenar e manipular dados diretamente na memória principal do sistema, proporcionando acesso mais rápido aos dados, em comparação aos bancos de dados tradicionais que utilizam armazenamento em disco.
## 16 | gab=E | cand: 
Na arquitetura cliente-servidor para aplicações móveis, a comunicação entre o cliente (aplicativo móvel) e o servidor é sempre realizada de forma que todos os dados necessários são armazenados localmente no dispositivo móvel, o que elimina a necessidade de consultas ao banco de dados do servidor.
## 17 | gab=C | cand: P1·ESTADO 5.1
A otimização de bases de dados para BI visa garantir que as consultas analíticas sejam executadas de maneira eficiente e rápida, a exemplo da indexação, que poderia ser a criação de índices nas tabelas de fatos e dimensões para acelerar a recuperação de dados; índices comuns incluem índices de colun
## 18 | gab=E | cand: 
No Hive do Apache Hadoop, as consultas são escritas em SQL; para tal, é necessário o conhecimento do MapReduce.
## 19 | gab=C | cand: P3·ENG 2.4, P1·ETICA 3.1
Considerando que a tabela seguinte descreve a quantidade de funções de dados e de transações e respectivas complexidades de um sistema, é correto afirmar que, nesse caso, o sistema possui exatamente 22 pontos de função sem fator de ajuste. função complexidade quantidade arquivo de interface externa 
## 20 | gab=C | cand: P3·DADOS 3.6, P3·DADOS 1.8
Workload, conceito que representa a demanda de aplicações a serem processadas, é utilizado para o correto dimensionamento de uma infraestrutura virtualizada. JUSTIFICATIVA - Certo. Workload constitui-se dos dados a serem processados e das instruções a serem executadas sobre estes dados. Define a qua
## 21 | gab=C | cand: P3·ARQ 2.6
Na especificação dos requisitos da contratação, compete ao integrante requisitante, com o apoio do integrante técnico, definir, entre outros, os requisitos de negócio, quando aplicáveis. JUSTIFICATIVA - Certo. Conforme a IN SGD/SEDGG/ME n.º 94/2022, “Art. 16. Na especificação dos requisitos da contr
## 22 | gab=C | cand: 
O comando cria um índice clusterizado em column1, colu column1 e column3 classificados em ordem decrescente e co JUSTIFICATIVA - Certo. O comando CREATE CLUSTERED INDE ON schema1.table1 (column1 DESC, column2 A idx_clustered na tabela table1. O índice será aplicado às col cada coluna é especificada:
## 23 | gab=E | cand: P2·AUD 1.2, P3·DADOS 1.8
Na dimensão snowflake, os dados são desnormalizados para e entanto, nessa dimensão, devido à repetição de dados, utiliza-se JUSTIFICATIVA - Errado. Na dimensão snowflake, os dados são n durante as consultas, mas economiza espaço em disco ao evitar a repe ou seja, os dados são organizados em várias t
## 24 | gab=C | cand: 
A opção de privilégio SELECT com hierarquia oferece a um us e futuras, o que simplifica a gestão de permissões no banco de JUSTIFICATIVA - Certo. O privilégio SELECT com hierarquia f
## 25 | gab=E | cand: P3·SEG 1.1
Ao contrário do LDAP injection, em que o invasor pode inserir ou manipular consultas criadas pela aplicação, no SQL injection o invasor pode apenas inserir consultas na aplicação, que são enviadas diretamente para o banco de dados.
## 26 | gab=E | cand: P3·DADOS 4.6, P3·DADOS 1.4
O armazenamento de credenciais em texto puro no banco de dados é uma prática segura, desde que o acesso ao banco de dados seja bem controlado.
## 27 | gab=E | cand: 
Em SQL, a instrução mais simples para selecionar registros de uma tabela é composta pelas cláusulas SELECT e WHERE.
## 28 | gab=C | cand: P3·DADOS 1.2
Em um banco de dados relacional, a cláusula UNIQUE deve ser aplicada a chaves alternativas, que não a chave primária, para garantir a não duplicidade da chave alternativa.
## 29 | gab=C | cand: P3·ENG 2.4, P3·DADOS 1.8 [texto-base: A respeito de IaC (infrastructure as code), integração contínua, automação e provisionamento de infraestrutura com Terraform, julgue os itens subsecutivos.]
IaC é o processo de gerenciamento e provisionamento de data centers por meio de arquivos legíveis, em que as definições de infraestrutura podem estar contidas em um arquivo de sistema de controle de versão (VCS).
## 30 | gab=C | cand: 
A execução do comando SQL mostrado a seguir disponibilizará para seleção somente os campos cod_professor e nome_professor da tabela professores a todos os usuários. GRANT SELECT (cod_professor, nome_professor) ON professores TO public;
## 31 | gab=C | cand: P3·DADOS 3.8
Considere que, em certa loja, os pedidos realizados por vendedores sejam salvos em uma tabela SQL pedidos, que as informações dos vendedores dessa loja sejam registradas na tabela vendedores e que cada um desses vendedores possua um código que é salvo na variável codigo_vendedor. Nessa situação hipo
## 32 | gab=C | cand: 
A consulta SELECT _ FROM Empregado WHERE Nome = @P OR Login = @P; é menos eficiente que a seguinte consulta. SELECT _ FROM Empregado WHERE Nome = @P UNION SELECT _ FROM Empregado WHERE Login = @P;
## 33 | gab=E | cand: 
A consulta SELECT * FROM Produtos WHERE TipoProd = ‘1’; é mais eficiente que a consulta a seguir. SELECT * FROM Produtos WHERE TipoProd = CAST (@char AS INT);
## 34 | gab=C | cand: P3·SEG 5.1, P3·DADOS 1.8
Caso conste, no modelo de dados referente ao cadastro de empregados de determinada empresa, o atributo idade do empregado, não é necessário que esse dado esteja fisicamente armazenado no banco de dados, uma vez que ele pode ser calculado com a data de nascimento em tempo de execução, o que caracteri
## 35 | gab=C | cand: P2·GOV 5.3, P2·EVID 2.2 [texto-base: Julgue os itens seguintes, relativos à linguagem de definição de dados SQL, à linguagem de manipulação de dados SQL, à linguagem de controle de dados SQL e à linguagem de consulta de dados SQL.]
A cláusula with estipula uma relação temporária cuja definição está disponível apenas à consulta em que essa cláusula ocorre.
## 36 | gab=E | cand: P2·EVID 2.1 [texto-base: Julgue os itens seguintes, relativos à linguagem de definição de dados SQL, à linguagem de manipulação de dados SQL, à linguagem de controle de dados SQL e à linguagem de consulta de dados SQL.]
Os comandos insert e delete servem, respectivamente, para inserir e deletar uma tabela no banco de dados; o comando insert permite, ainda, as restrições not null, unique e check.
## 37 | gab=C | cand:  [texto-base: Julgue os itens seguintes, relativos à linguagem de definição de dados SQL, à linguagem de manipulação de dados SQL, à linguagem de controle de dados SQL e à linguagem de consulta de dados SQL.]
No exemplo de comando UPDATE a seguir, é utilizada a construção case, em que as atualizações nas tuplas são realizadas com um único comando, evitando-se problemas com a ordem das atualizações. UPDATE tabela SET coluna = case When predicado1 then resultado1 When predicado2 then resultado2 ... When pr
## 38 | gab=C | cand: P2·DIR 2.2 [texto-base: Julgue os itens seguintes, relativos à linguagem de definição de dados SQL, à linguagem de manipulação de dados SQL, à linguagem de controle de dados SQL e à linguagem de consulta de dados SQL.]
O depurador Transact-SQL permite depurar stored procedures de forma interativa, mostrando a sequência de chamadas SQL, variáveis locais/globais, e controla pontos de interrupção e parâmetros associados a esses procedimentos.
## 39 | gab=C | cand: P2·GOV 2.2, P3·SEG 5.6
Uma medida rápida executa cálculos comuns e avançados utilizando um conjunto de comandos DAX (data analysis expressions) criados a partir dos dados de entrada fornecidos na caixa de diálogo.
## 40 | gab=C | cand: P2·EVID 2.1
Em um banco de dados relacional, as tabelas são formadas por linhas e colunas que utilizam chaves primárias ou estrangeiras para criar relações entre os dados.
## 41 | gab=E | cand: P2·EVID 1.1, P3·DADOS 3.9
Um sistema gerenciador de banco de dados resolve problemas de integridade para evitar que a mesma informação esteja duplicada em vários locais.
## 42 | gab=C | cand: P3·DADOS 4.4, P3·DADOS 1.2
Em um banco de dados relacional, uma chave primária é o conjunto de um ou mais campos utilizados para identificar um único registro na tabela.
## 43 | gab=C | cand: P2·EVID 2.2
Uma das características de um sistema gerenciador de banco de dados (SGBD) é a independência de dados, ou seja, o entendimento dos dados pelo SGBD ocorre mesmo sem uma aplicação.
## 44 | gab=E | cand: P3·SEG 5.6, P3·DADOS 1.5
As propriedades autenticidade, consistência, isolamento e durabilidade garantem confiabilidade às transações executadas em um banco de dados.
## 45 | gab=E | cand: P3·DADOS 1.5, P2·EVID 2.1
O esquema do banco de dados é alterado a cada comando de INSERT, UPDATE ou DELETE em uma de suas tabelas.
## 46 | gab=E | cand: 
Em uma consulta SQL, tuplas duplicadas são automaticamente eliminadas pelo SGBD, com o objetivo de aumentar o desempenho.
## 47 | gab=C | cand: 
Em uma tabela com 100 registros, uma consulta SQL com a cláusula WHERE pode apresentar resultados com quantidade variando de zero a 100 linhas.
## 48 | gab=E | cand: 
A SQL permite a consulta simultânea de atributos com o mesmo nome, desde que a ordem desses atributos seja a mesma da ordem das tabelas onde eles estão armazenados.
## 49 | gab=C | cand: P2·EVID 2.1, P3·DADOS 1.5
A clusterização de uma tabela consiste em ordenar fisicamente os dados, segundo um índice específico.
## 50 | gab=C | cand: P3·DADOS 1.2
Quando utilizados em operações em bancos de dados, os métodos HTTP de GET, POST, PUT e DELETE podem ser associados aos comandos CRUD de SELECT, CREATE, UPDADE e DELETE, respectivamente. JUSTIFICATIVA - Certo. Os métodos HTTP são os responsáveis por provocar alterações nos recursos identificados pela
## 51 | gab=C | cand: P3·ENG 2.5
O OLAP (online analytical processing) permite a realização de consultas analíticas complexas em grandes volumes de dados, organizados em estruturas multidimensionais, sem impactar negativamente o desempenho dos sistemas transacionais.
## 52 | gab=E | cand: P3·DADOS 1.8
Um data warehouse é projetado para suportar operações transacionais diárias, como inserções, atualizações e exclusões frequentes de dados, similarmente a um banco de dados operacional.
## 53 | gab=C | cand: 
O comando SQL a seguir cria uma visão com todos os dados dos professores e dos respectivos cursos que eles coordenam, não incluindo os cursos sem um professor com a função de coordenador. create view coordenador_curso as select * from professor p left outer join curso s on true where p.cpf_professor
## 54 | gab=E | cand: 
O comando SQL a seguir tem a sintaxe correta para obter o código dos cursos e o valor médio do salário dos professores, mas mostrando apenas aqueles cursos cuja média do salário dos seus professores é inferior a 5.000 reais. Select c.cod_curso, avg (salario) from contrato c, professor p where c.cpf_
## 55 | gab=E | cand: P1·ESTADO 5.1
A criação de índices em tabelas com alto grau de duplicidade garante um aumento na eficiência de consultas a essas tabelas.
## 56 | gab=C | cand: P3·DADOS 1.2
No processo de otimização de consultas de bancos de dados relacionais, em consultas que façam uso de ORDER_BY, a criação de índice nas colunas ORDER_BY é uma opção que pode melhorar o desempenho de tais consultas.
## 57 | gab=C | cand: 
No processo de análise de desempenho de um banco de dados, na análise de planos de execução é possível diagnosticar que a exclusão de índices pode levar à melhoria de desempenho do banco de dados.
## 58 | gab=E | cand: 
Ao escrever consultas para bancos de dados relacionais, o uso de subconsultas e tabelas aninhadas costuma apresentar melhor desempenho que o uso de JOIN.
## 59 | gab=E | cand: 
O failover em um sistema de banco de dados, sem nenhum prejuízo para a qualidade das informações consultadas, é garantido pela replicação das bases de dados em sítios distintos.
## 60 | gab=E | cand: 
Em um balanceamento de carga por transação, todas as transações de determinado cliente são enviadas para a mesma réplica do banco de dados, até que a conexão seja fechada.
## 61 | gab=C | cand: P2·AUD 1.4, P2·EVID 2.1
Uma cardinalidade N:N no modelo lógico de um banco de dados relacional gera três tabelas no modelo físico.
## 62 | gab=C | cand: P2·AUD 1.4, P2·EVID 2.1
Os índices são tabelas diferenciadas ordenadas por determinado critério e com ponteiros para a localização física das linhas.
## 63 | gab=E | cand: P2·EVID 2.1, P3·DADOS 1.5
A implementação de uma view consiste na geração de uma tabela física que consolida os dados de outras tabelas do banco de dados.
## 64 | gab=E | cand: P3·DADOS 1.5, P2·EVID 2.1
Esquema de banco de dados é um conjunto de tabelas, registros
## 65 | gab=E | cand: P2·AUD 2.2
Uma view materializada realiza consulta em tabelas do banco d
## 66 | gab=C | cand: P3·DADOS 1.2, P2·EVID 2.1
Em um banco de dados relacional, cada linha na tabela é um r atributo dos dados e cada registro, geralmente, tem um valor pa
## 67 | gab=C | cand: P3·DADOS 1.8
Um dos Vs de Big Data corresponde a velocidade, à qual é aplicada a característica ACID, que garante, entre outras coisas, a atomicidade das transações no banco de dados.
## 68 | gab=E | cand: P3·SEG 5.6, P3·ARQ 1.7
Uma role do sistema gerenciador de banco de dados faz que a lógica de negócios seja armazenada no banco de dados, podendo o código do aplicativo executar as roles em vez de atualizar diretamente as relações de banco de dados.
## 69 | gab=C | cand: 
Filtro Bloom é uma estrutura de dados com uso eficiente de espaço que pode ser utilizada para testar se um elemento é membro de um conjunto; no entanto, os índices do filtro Bloom suportam apenas consultas de igualdade, sendo mais úteis quando uma tabela possui muitos atributos e as consultas testam
## 70 | gab=E | cand: P3·DADOS 3.7, P3·DADOS 3.8 [texto-base: Acerca do governo eletrônico — ou governo digital —, da transparência da administração pública, do controle social e cidadania, e da accountability, julgue os itens subsequentes.]
Accountability é um termo utilizado para definir o processo de registro e classificação de transações financeiras realizadas de forma online.
## 71 | gab=C | cand: 
No MySQL, o InnoDB suporta transações ACID, bloqueio em nível de linha e MVCC (multi-version concurrency control) e organiza dados em um índice clustered pela chave primária.
## 72 | gab=E | cand: P3·DADOS 1.8, P2·GOV 2.2
No SQL Server, o keyset-driven cursor mantém uma cópia completa dos dados no momento em que é aberto, e qualquer alteração feita nos dados subjacentes não é refletida no cursor, tornando-o semelhante a um static cursor. id 1 2 3 departamento nome_departamento TI RH marketing funcionario id 1 2 3 4 n
## 73 | gab=E | cand: P3·SEG 5.3, P3·SEG 5.1 [texto-base: Considerando a tabela de fato apresentada inicialmente e as tabelas de dimensão a ela subsequentes, julgue os itens a seguir, referentes à modelagem dimensional de dados.]
A tabela fato_processos deveria conter informações detalhadas acerca do nome do juiz e do ano de referência, para otimizar a consulta direta, eliminando-se a necessidade de dimensões.
## 74 | gab=E | cand: 
Um aplicativo que armazene dados sensíveis criptografados em um banco de dados usando criptografia automática garante que esses dados, quando recuperados, estejam isentos de serem indevidamente capturados, mesmo que haja uma falha de injeção de SQL.
## 75 | gab=C | cand: 
Considere-se a tabela e o script SQL a seguir. Tabela: colaboradores SELECT avg(idade), sexo FROM colaboradores GROUP BY sexo O resultado da consulta SQL é avg(idade) 15 32 sexo Feminino Masculino
## 76 | gab=E | cand: P3·ENG 2.1, P3·ENG 2.5
A linguagem de manipulação de dados (DML) inclui instruções que modificam a estrutura de um banco de dados.
## 77 | gab=E | cand: 
Um índice de banco de dados é uma estrutura que deve receber um ou mais atributos de uma relação que identificam uma única tupla.
## 78 | gab=E | cand: P3·ENG 2.8, P3·ENG 2.5
O padrão adapter da visão GoF permite que uma classe de persistência seja adaptada de acordo com o banco de dados utilizado na aplicação.
## 79 | gab=C | cand: P3·DADOS 1.5, P2·EVID 2.1
Em um banco de dados distribuído com esquema federado, as tabelas do banco original são horizontalmente particionadas em tabelas-membro, sendo uma tabela-membro para cada banco de dados membro, de modo que as exibições particionadas distribuídas são usadas para que pareça haver uma cópia completa da
## 80 | gab=E | cand: P2·AUD 1.2
O resultado da consulta a seguir, que utiliza o operador UNION, não elimina os registros duplicados entre as tabelas. SELECT depto FROM emp UNION SELECT depto FROM depto;
## 81 | gab=C | cand: P2·EVID 2.1
Um banco de dados do tipo relacional é aquele composto por um conjunto de relações conhecidas como tabelas.
## 82 | gab=E | cand: P2·EVID 1.1
Quando o administrador cria uma máquina virtual com banco de dados, deve ser definido o espaço que ela irá utilizar, visto que, havendo necessidade de ampliação de espaço, uma nova máquina virtual deverá ser criada.
## 83 | gab=C | cand: P3·ENG 2.1, P3·ARQ 4.1
No LINQ to SQL, o modelo de dados de um banco de dados relacional é mapeado para um modelo de objeto expresso na linguagem de programação do desenvolvedor. No que concerne à programação avançada em PHP 5 e à utilização de frameworks de programação, julgue os itens subsecutivos.
## 84 | gab=E | cand: P2·DIR 4.2
O otimizador de consultas do SGBD é responsável por verificar se a expressão de definição de dados está de acordo com as regras de otimização da linguagem.
## 85 | gab=C | cand: P2·AUD 1.2, P3·ENG 2.1
A DCL (Data Control Language) é utilizada para controlar quem tem acesso aos objetos do banco de dados.
## 86 | gab=C | cand: P3·ENG 2.5, P3·ENG 2.1
Uma VIEW é um objeto do banco de dados, mas não possui nenhuma linha em sua estrutura, pois faz referência a linhas e colunas de outras tabelas.
## 87 | gab=C | cand: P3·SEG 4.3, P2·EVID 2.1
Ao executar um comando de SELECT em mais de uma tabela sem a cláusula WHERE, o resultado será o produto cartesiano das tabelas acessadas.
## 88 | gab=C | cand: 
A seguir, é apresentado o comando correto em SQL para se alterar o valor do salário (Salario) para o maior salário da tabela apenas para o funcionário que possui IdFuncionario igual a 1. UPDATE funcionario AS f, (SELECT max(salario) as maxsalario FROM funcionario) AS s SET f.salario = s.maxsalario W
## 89 | gab=E | cand: P2·EVID 2.1
Queries que determinam views apenas podem ser originadas de tabelas. JUSTIFICATIVA - Errado. View pode ser definida como uma tabela virtual composta por linhas e colunas de dados vindos de tabelas relacionadas em uma query (um agrupamento de SELECT, por exemplo). As linhas e colunas da view são gera
## 90 | gab=E | cand: 
Visões podem ser usadas para definir relações no esquema externo que exibem para os aplicativos as alterações feitas no esquema conceitual do banco de dados. Com pertinência à linguagem SQL, julgue o item abaixo.
## 91 | gab=E | cand: P3·SEG 1.1
Considere-se o seguinte script SQL. select   report_code,   year,   month,                   day, wind_speed, case when wind_speed>= 40 then ‘HIGH’ when wind_speed>= 30 then ‘MODERATE’ else ‘LOW’ end as wind_severity from station_data O resultado da execução do script resultará em erro, pois, caso h
## 92 | gab=E | cand: 
Em um comando SELECT, a cláusula WHERE define que o resultado da consulta é o produto cartesiano das tabelas envolvidas.
## 93 | gab=C | cand: 
Em SQL, o comando DISTINCT é utilizado para eliminar resultados repetidos em consultas a tabelas do banco de dados.
## 94 | gab=C | cand: P3·DADOS 1.4, P2·EVID 2.1
Os comandos TRUNCATE e DROP TABLE removem todas as linhas de uma tabela, porém o comando DROP TABLE exclui também a estrutura da tabela do banco de dados bem como todos os dados armazenados na tabela.
## 95 | gab=E | cand: P2·EVID 2.1
A tabela BDA_SORT _SEGMENT informa a quantidade de espaço destinado para ordenar uma consulta no SGBD Oracle.
## 96 | gab=E | cand: 
Em JDBC, o método executeUpdate() pode ser usado para realizar um update em banco de dados, caso em que esse método recebe uma expressão SQL cujos valores de retorno serão tratados por um ResultSet.
## 97 | gab=C | cand: P3·DADOS 1.9, P3·DADOS 1.4
Bancos de dados relacionais são compostos de tabelas, unidas mediante valores comuns de linha/coluna, ou chaves, sendo cada classe geográfica (camada) armazenada como uma tabela.
## 98 | gab=C | cand: 
Um índice do banco de dados é uma lista ordenada derivada dos dados em uma tabela e armazenada como uma coluna de tabela, o que dispensa onerosas varreduras de tabelas inteiras.
## 99 | gab=C | cand: 
A fim de proteger a integridade do banco de dados, as transações são atômicas, isto é, ou são completamente autorizadas no banco de dados, ou são revertidas (definitivamente não autorizadas).
## 100 | gab=E | cand: P2·AUD 1.2
A cláusula GROUP BY, do SQL, pode ser utilizada sem a presença de funções agregadas, desde que haja uma cláusula ORDER BY para organizar os resultados da consulta.
## 101 | gab=E | cand: P3·ENG 2.1
Para excluir uma tabela na linguagem SQL e liberar os recursos alocados por ela, inclusive índices e triggers associados, deve-se fazer uso do comando DELETE TABLE, pois ele remove tanto os dados quanto a estrutura da tabela.
## 102 | gab=C | cand: P2·TRANSP 4.3
Ocorre transação confirmada (commit) quando há informações suficientes no log do banco de dados para garantir que, mesmo se houver falha no sistema, as atualizações da transação serão refeitas.
## 103 | gab=C | cand: P3·ARQ 5
Auditoria de banco de dados consiste na revisão de seu log para examine de todos os acessos e operações aplicadas a ele durante determinado período.
## 104 | gab=E | cand: 
Uma instância de um banco de dados SQL compreende a organização lógica dos dados com seus atributos e seus domínios correspondentes.
## 105 | gab=C | cand: P3·ENG 2.1 [texto-base: Em relação a ferramentas de análise e avaliação de custos de projetos e a técnicas de análise e avaliação de projetos de investimentos sociais, julgue os itens seguintes.]
As três principais técnicas de avaliação de desempenho que podem ser utilizadas para avaliação de projetos de infraestrutura são a análise por envoltório de dados (DEA), o método da fronteira estocástica e o índice Malmquist.
## 106 | gab=C | cand: 
Índices em colunas frequentemente usadas em cláusulas WHERE podem melhorar significativamente a performance de consultas SQL em bancos de dados relacionais.
## 107 | gab=E | cand: P3·SEG 1.2
O índice de desempenho de prazos indica se são válidas as estimativas da quantidade de trabalho e de tempo que o trabalho consome.
## 108 | gab=E | cand: P3·DADOS 3.8
Em blockchain, ledger é um banco de dados distribuído, no qual os participantes podem inserir novas transações e alterar e excluir transações já registradas.
## 109 | gab=C | cand: P3·ARQ 1.7, P3·SEG 5.6
São objetivos do business intelligence permitir o acesso interativo e proporcionar a manipulação dos dados, fornecendo aos gerentes e analistas de negócios a capacidade de realizar a análise adequada.
## 110 | gab=C | cand: P3·ENG 2.5, P3·ENG 2.1
Pelos dados apresentados na tabela, verifica-se que o nível de instrução dos indivíduos é determinante para o seu ingresso e permanência no mercado de trabalho, por isso o menor índice de subocupação por insuficiência de horas é observado entre as pessoas com ensino superior completo.
## 111 | gab=E | cand: P3·ARQ 1.5
A normalização de dados em um banco de dados é uma técnica que organiza os dados desse banco em uma escala específica, como valores entre 0 e 1.
## 112 | gab=C | cand: P2·EVID 2.2, P1·ETICA 3.1
Na análise de pontos de função, uma consulta implícita de dados ocorre quando a aplicação apresenta dados ao usuário antes de realizar uma transação, sem que o usuário precise solicitar explicitamente os dados.
## 113 | gab=C | cand: P3·ENG 2.5
Metadados são informações estruturadas adicionais, relativas a certo conjunto de dados, que podem ser utilizadas para descrevê-lo e manipulá-lo da forma mais eficiente possível. JUSTIFICATIVA - Certo. As interfaces de metadados podem ser usadas para uma variedade de tarefas. Por exemplo, elas podem 
## 114 | gab=E | cand:  [texto-base: Julgue os próximos itens, a respeito de linguagem de manipulação de dados (DML), de linguagem de definição de dados (DDL), de modelagem dimensional e de linguagem de consulta estruturada (SQL).]
O comando SQL MODIFY é usado para atualizar dados existentes em uma tabela do banco de dados. JUSTIFICATIVA - Errado. O comando UPDATE é usado para atualizar linhas existentes em uma tabela.
## 115 | gab=C | cand: P3·DADOS 1.8 [texto-base: Julgue os próximos itens, a respeito de linguagem de manipulação de dados (DML), de linguagem de definição de dados (DDL), de modelagem dimensional e de linguagem de consulta estruturada (SQL).]
Um esquema em estrela é um modelo multidimensional no qual os atributos das tabelas fato e dimensão podem ser usados para filtrar, agrupar e agregar os fatos. JUSTIFICATIVA - Certo. Um esquema em estrela é um modelo multidimensional que organiza os dados em um banco de dados para torná-los mais fáce
## 116 | gab=C | cand:  [texto-base: Julgue os próximos itens, a respeito de linguagem de manipulação de dados (DML), de linguagem de definição de dados (DDL), de modelagem dimensional e de linguagem de consulta estruturada (SQL).]
O comando SQL SELECT FROM permite que se leia certa coluna de uma tabela. JUSTIFICATIVA - Certo. O comando SELECT FROM realizar a leitura de uma coluna de certa tabela.
## 117 | gab=C | cand:  [texto-base: Julgue os próximos itens, a respeito de linguagem de manipulação de dados (DML), de linguagem de definição de dados (DDL), de modelagem dimensional e de linguagem de consulta estruturada (SQL).]
O comando SQL DROP TABLE é usado para excluir uma tabela existente em um banco de dados. JUSTIFICATIVA - Certo. O comando DROP TABLE é usado para excluir uma tabela e todos os registros dessa tabela.
## 118 | gab=C | cand: 
No Oracle, gatilhos          podem      invocar    procedimentos armazenados. JUSTIFICATIVA - Certo. Os gatilhos são semelhantes aos procedimentos armazenados. Um gatilho armazenado no banco de dados pode incluir instruções SQL e PL/SQL para serem executadas como uma unidade e pode invocar procedime
## 119 | gab=E | cand: P3·ARQ 5.5, P3·DADOS 3.8, P3·ARQ 5.3 [texto-base: A respeito de arquitetura, segurança, integridade, concorrência, recuperação após falhas e gerenciamento de transições em sistemas de gerenciamento de banco de dados (SGDB), julgue os próximos itens.]
Se a recuperação de falhas for realizada por meio do rollback, o SGDB que utiliza log de transações retornará todas as transições, tanto as confirmadas quanto as não confirmadas, a fim de garantir que o sistema retorne ao estado anterior à falha. JUSTIFICATIVA - Errado. Em SGBDs que utilizam log de 
## 120 | gab=C | cand: P3·DADOS 3.8 [texto-base: A respeito de arquitetura, segurança, integridade, concorrência, recuperação após falhas e gerenciamento de transições em sistemas de gerenciamento de banco de dados (SGDB), julgue os próximos itens.]
Um SGBD que implementa um sistema de log de transações segundo o princípio WAL (write-ahead logging) é capaz de garantir que, mesmo após uma falha inesperada, todas as transações confirmadas possam ser recuperadas ao estado consistente anterior à falha. JUSTIFICATIVA - Certo. O princípio do write-ah
## 121 | gab=C | cand: P2·DIR 5.1, P3·DADOS 1.5
Em um sistema de banco de dados distribuído, a técnica de replicação síncrona garante que todas as cópias dos dados em diferentes      locais     estejam     sempre     atualizadas simultaneamente, eliminando qualquer possibilidade de inconsistência. JUSTIFICATIVA - Certo. A replicação síncrona em u
## 122 | gab=C | cand: 
Os comandos SQL, tais como SELECT, INSERT, UPDATE e DELETE, são aplicáveis em SGDBs relacionais. JUSTIFICATIVA - Certo. Esses comandos são aplicáveis e amplamente utilizados em SGBDs relacionais, pois esses sistemas compartilham a estrutura relacional e utilizam SQL como linguagem de consulta para r
## 123 | gab=E | cand: 
Em um banco de dados Oracle, a execução do comando SQL GRANT SELECT ON employees TO security_team; permite que o grupo de usuários security_team insira novos registros na tabela employees. JUSTIFICATIVA - Errado. A execução do referido comando apenas permitirá que o grupo de usuários security_team l
## 124 | gab=C | cand: P3·DADOS 1.8
Em Big Data, uma das propriedades ACID é a atomicidade, que garante que todas as alterações sejam efetivadas no banco de dados, sem atualização parcial da transação.
## 125 | gab=C | cand: P3·DADOS 1.8, P3·ARQ 4.1
Julgue os próximos itens, relativos à normalização de dados, à linguagem de definição de dados (DDL), a sistema gerenciador de banco de dados (SGBD) Oracle 21C e a data lake.
## 126 | gab=E | cand: P2·AUD 1.2
No JBoss EAP, XA datasource é utilizado para conexões de banco de dados que não requerem a coordenação de transações entre múltiplos recursos, proporcionando uma configuração mais simples e eficiente para transações locais.
## 127 | gab=C | cand: P3·ENG 2.4, P3·SEG 5.3
Qualquer subconjunto dos campos de uma relação pode ser uma chave de pesquisa em um arquivo de índice.
## 128 | gab=E | cand: P2·TRANSP 5.3, P2·EVID 2.1
A expressão SQL a seguir está sintaticamente correta e permite inserir dois alunos de nomes Pedro e Maria na tabela alunos. I N S E R T    V A L U E S             ( ' P e d r o ' , 'Maria') INTO alunos;
## 129 | gab=E | cand: P3·DADOS 3.8
A execução do comando a seguir corrigirá o problema que surge quando a senha do computador não está sincronizada com o banco de dados do controlador de domínio. Add-Computer -DomainName “YourDomainName” - Credential (Get-Credential) Restart-Computer
## 130 | gab=E | cand: 
A execução do código SQL a seguir retornará 10. CREATE TABLE TABELA (a integer); INSERT INTO TABELA VALUES (null); SELECT a+10 FROM TABELA;
## 131 | gab=C | cand: P2·EVID 2.1
Em um sistema de gerenciamento de banco de dados, uma tabela pode ter inúmeras chaves candidatas, mas somente uma chave primária.
## 132 | gab=E | cand: 
Considere que os comandos SQL a seguir tenham sido executados de forma bem-sucedida. CREATE TABLE TABELA_TESTE (a integer, b varchar); INSERT INTO TABELA_TESTE (a) VALUES (5); INSERT INTO TABELA_TESTE (b) VALUES ('FUB'); INSERT INTO TABELA_TESTE (a) VALUES (7); Nessa situação, o resultado da execuçã
## 133 | gab=C | cand: 
Stored procedures em PL/SQL são estruturas armazenadas diretamente no banco de dados que permitem a execução de instruções SQL pré-compiladas, o que reduz o tráfego de rede e melhora o desempenho das aplicações.
## 134 | gab=E | cand: P3·SEG 5.6, P1·ADM 1.1
O padrão MVC (model-view-controller) obriga que a visão (view) execute diretamente as operações de acesso e manipulação dos dados armazenados no banco de dados.
## 135 | gab=C | cand: P3·SEG 1.1
Caso o comando flyway migrate seja executado em um terminal de uma máquina com Flyway CLI instalado e configurado corretamente, o Flyway identificará scripts de migração que ainda não foram aplicados e os executará na ordem crescente de versão, atualizando o banco de dados com as alterações mais rec
## 136 | gab=C | cand: P2·TRANSP 4.3 [texto-base: No que se refere aos protocolos DHCP e IMAP, aos sistemas de segurança IPS, aos modelos de nuvem, ao ambiente Linux e ao Microsoft Windows Server, julgue os itens a seguir.]
Em um ambiente Oracle Database, o comando ALTER DATABASE DISMOUNT; pode ser utilizado para desmontar o banco de dados, ou seja, a execução desse comando encerraria o acesso às estruturas físicas (datafiles), mas manteria a instância ativa.
## 137 | gab=E | cand: P3·DADOS 1.7 [texto-base: No que se refere aos protocolos DHCP e IMAP, aos sistemas de segurança IPS, aos modelos de nuvem, ao ambiente Linux e ao Microsoft Windows Server, julgue os itens a seguir.]
A normalização de dados é a estratégia de criação de índices compostos para melhorar a performance das consultas em grandes volumes de dados.
## 138 | gab=C | cand: P3·DADOS 1.2
Em bancos NoSQL orientados a documentos, é comum o uso de estruturas aninhadas, que evitam junções e melhoram a performance de leitura. Certa empresa especializada em seguros de vida privados decidiu modernizar seu sistema de informações com a utilização de um SGBD relacional, padrão SQL. Durante a 
## 139 | gab=C | cand: 
Para recuperar os nomes de todos os beneficiários vinculados a apólices ativas, usa-se a DQL com cláusulas como INNER JOIN e WHERE, classificando-se tal operação como consulta de dados.
## 140 | gab=E | cand: 
O comando SELECT nome, idade FROM CLIENTE; pertence à DML, pois consulta os dados armazenados no banco para eventual tomada de decisão.
## 141 | gab=C | cand: P3·DADOS 3.1, P3·ENG 2.1
Em uma rede definida por software, o controlador SDN lida com a comunicação das aplicações, determinando o destino dos pacotes de dados e o balanceamento de carga dentro da SDN.
## 142 | gab=E | cand: P3·SEG 5.6, P3·SEG 3.3
Ao se executar o arquivo YAML descrito a seguir, será criado um deployment com uma imagem do NGINX. apiVersion: v1 kind: Service metadata: name: my-nginx-svc labels: app: nginx spec: type: LoadBalancer ports: - port: 80 selector: app: nginx No modelo de infraestrutura como código, é possível a impla
## 143 | gab=E | cand: 
Em um banco de dados, os índices são armazenados fisicamente na mesma ordem em que são definidos logicamente para permitir acesso eficiente aos dados.
## 144 | gab=C | cand: 
Se executada, a consulta a seguir retorna a contagem de clientes com mais de 18 anos de idade que realizaram transações com valores superiores a 1.000, agrupados e ordenados de forma decrescente por idade.
## 145 | gab=E | cand: P3·DADOS 1.8
Nos data warehouses, os índices de junção associam as linhas da tabela de fatos com as respectivas colunas na tabela de dimensões, o que facilita as operações de consulta e análise de dados.
## 146 | gab=C | cand: 
O banco de dados PostgreSQL possui um tratamento automático para resolver situações de deadlock, embora seja difícil prever qual das transações conflitantes será interrompida.
## 147 | gab=E | cand: 
Considere a tabela a seguir, de nome dados. id|sexo|idade| --+----+-----+ |M   |   10| |F   |   10| |M   |   11| |F   |   11| |M   |   10| Considere, ainda, que a seguinte consulta tenha sido executada. select sexo, idade, count(*) qtde from dados group by cube(sexo, idade) Nesse caso, é correto afi
## 148 | gab=C | cand: P3·ARQ 1.5, P3·ARQ 1
Entre os fatores que podem tornar uma aplicação vulnerável estão o sistema operacional, o servidor web/aplicativo, o sistema de gerenciamento de banco de dados (SGBD), as API e todos os componentes, ambientes de tempo de execução e bibliotecas.
## 149 | gab=E | cand: P3·ENG 2.1, P3·ENG 2.5
SQL é a linguagem padrão ANSI para a manipulação de bancos de dados relacionais e, por ser uma linguagem imperativa, possibilita a criação de programas completos.
## 150 | gab=C | cand: P2·EVID 1.1
No modelo relacional de banco de dados, uma relação é definida como um conjunto de tuplas e, matematicamente, os elementos de um subconjunto não têm ordem entre eles, portanto as tuplas em uma relação não têm qualquer ordem em particular. OS ESPECÍFICOS -Julgue os próximos itens, relativos a servido
## 151 | gab=C | cand: P1·ETICA 3.1
A função cursor.execute() é capaz de executar uma consulta SQL que tenha sido passada por uma string.
## 152 | gab=C | cand: 
O JPA 2.0 permite que uma lista de objetos seja ordenada na memória e, depois, que essa ordem seja implementada no banco de dados para futuras consultas.
## 153 | gab=C | cand: 
No banco de dados PostgreSQL, o comando SELECT adquire o bloqueio ACCESS SHARE nas tabelas referenciadas.
## 154 | gab=C | cand: P1·ESTADO 9.1
A taxa natural de desemprego no país em questão é de 7%, enquanto a inflação é de 6%. Em uma economia fechada, a base monetária é composta por 200 unidades monetárias de papel-moeda em poder do público e 300 unidades monetárias em reservas bancárias. A razão de reservas bancárias é de 10% e o multip
## 155 | gab=E | cand: P3·DADOS 1.6, P3·ENG 2.5 [texto-base: Julgue os itens a seguir, relativos a estruturas de concreto armado e protendido, estruturas metálicas e controle de qualidade de materiais. Na chegada de uma encomenda de concreto usinado ao local de]
Vida útil de projeto é o período em que os custos levantados para a execução de um sistema estrutural de concreto armado permanecem válidos, sendo normalmente de um ano, prazo em que os contratos de obras devem ser reajustados de acordo com índices fixados na avença.
## 156 | gab=E | cand: P3·DADOS 1.2
Em relação às linguagens de programação para banco de dados, é correto afirmar que SQL é uma linguagem de programação que se concentra no gerenciamento de bancos de dados relacionais; T-SQL é uma extensão processual usada somente no SQL Server.
## 157 | gab=E | cand: 
Uma consulta para mostrar o total de compras de um cliente, por produto, em determinado período, é SELECT c.Nome, sum(cp.Quantidade_Comprada) total_compras FROM Compras cp JOIN Clientes c ON cp.ID_Cliente = c.ID_Cliente WHERE cp.ID_Produto = c. ID_Produto;
## 158 | gab=C | cand: 
Para garantir a segurança dos dados, a empresa deve implementar as seguintes políticas de armazenamento de dados: criptografia de dados; controle de acesso; auditoria e monitoramento; política de backup; retenção de dados e segurança física. Para otimizar o desempenho do banco de dados da empresa, p
## 159 | gab=C | cand: 
Um exemplo de técnica bastante utilizada para a otimização do desempenho do banco de dados da empresa consiste na análise de consultas SQL, também conhecida como plano de execução.
## 160 | gab=E | cand: P3·DADOS 3.1, P3·ENG 2.1
A técnica de balanceamento de carga poderia ser utilizada na empresa, pois é o método ideal de distribuição da quantidade de dados nas tabelas de um banco de dados para manter a estabilidade do servidor quando o volume de dados for muito grande.
## 161 | gab=E | cand: P3·SEG 1.1, P3·SEG 5.6
CREATE TABLE cidade ( nome varchar(40), codigo int ); CREATE TABLE capital ( UF char(2) UNIQUE NOT NULL ) #XPTO (cidade); insert into capital values ('Brasília', 22, 'DF'); select * from capital; No script precedente, desenvolvido em SQL no PostgreSQL, a substituição dos caracteres #XPTO por Referen
## 162 | gab=C | cand: P3·DADOS 1.5, P3·DADOS 1.1, P3·DADOS 1 [texto-base: Em relação a extranet e intranet, bem como à arquitetura orientada a serviços, julgue os itens a seguir. WSDL é uma tecnologia que padroniza a descrição da interface de um web service, enquanto UDDI é]
A respeito de modelagem, normalização de dados e de MySQL, julgue os itens seguintes. O comando SHOW OPEN TABLES WHERE In_use > 0; é usado para exibir apenas as tabelas que estejam em uso no esquema ativo no momento da execução da consulta.
## 163 | gab=C | cand: P3·DADOS 4.6 [texto-base: Em relação a extranet e intranet, bem como à arquitetura orientada a serviços, julgue os itens a seguir. WSDL é uma tecnologia que padroniza a descrição da interface de um web service, enquanto UDDI é]
A integridade referencial garante que os valores de chaves estrangeiras correspondam aos valores válidos na tabela referenciada, mas não impede que essas chaves sejam nulas, desde que a coluna permita valores nulos.
## 164 | gab=E | cand:  [texto-base: Acerca de bancos de dados NoSQL, de banco de dados em memória e de data lake, julgue os itens subsecutivos. Um data lake funciona como uma arquitetura de armazenamento que requer que todos os dados se]
use std::sync::{Arc}; use std::thread; fn main() { let counter = Arc::new(0); let mut handles = vec![]; for _ in 0..10 { let counter_clone = Arc::clone(&counter); let handle = thread::spawn(move || { let mut num = counter_clone.lock().unwrap(); *num += 1; }); handles.push(handle); } for handle in ha
## 165 | gab=C | cand: P3·DADOS 1.4
Considere que as tabelas e o relacionamento entre elas tenham sido corretamente criados, conforme o modelo apresentado, e que os seguintes comandos tenham sido executados com sucesso. INSERT INTO Orgao VALUES (1,'TRE-SC'); INSERT INTO Orgao VALUES (2,'TRE-PR'); INSERT INTO Processo VALUES (1,'111', 
## 166 | gab=C | cand: P3·DADOS 1.4, P3·DADOS 1.8, P3·DADOS 1.2
Para lidar com as necessidades de gerenciamento de dados de Big Data, podem ser usados sistemas para armazenamento de chave-valor, mesmo sendo comum que esses sistemas tenham recursos de consulta limitados e não aceitem o uso da SQL.
## 167 | gab=E | cand: P3·DADOS 1.2
Em banco de dados, para que a integridade de uma entidade seja observada, exige-se que seja atribuído à chave primária um conteúdo que pertença a um conjunto de valores válidos dessa entidade.
## 168 | gab=E | cand: P2·EVID 2.1, P3·SEG 5.6
Se as referidas tabelas forem criadas em um banco de dados MySQL, para que seja feita uma mudança no nome do campo dia_da_semana para nome_do_dia na tabela Monitoria, será necessário executar o comando a seguir. ALTER TABLE Monitoria MODIFY COLUMN dia_da_semana TO nome_do_dia
## 169 | gab=E | cand: 
O comando SQL a seguir é capaz de listar pelo nome apenas o Aluno apoiado pela Monitoria, seguido pelo número de horas de atendimento, sendo a lista dada em ordem decrescente do número de horas e apresentada com pelo menos um registro na tabela Monitoria. SELECT a.nome, m.numero_de_horas AS nr_horas
## 170 | gab=C | cand: 
O comando SQL a seguir permite listar o nome das disciplinas que estão sendo apoiadas pela Monitoria e a respectiva quantidade de alunos atendidos em cada disciplina. SELECT nome_disciplina, COUNT(cod_disciplina_apoiada) as quantidade_de_alunos FROM Monitoria, Disciplina WHERE cod_disciplina = cod_d
## 171 | gab=C | cand: P2·AUD 1.2
Se a tabela Aluno for eliminada com o comando DROP do SQL, então, para desfazer essa eliminação utilizando o Oracle 21C, o comando a seguir deve ser executado, caso o parâmetro de inicialização RECYCLEBIN esteja definido como ON. FLASHBACK TABLE Aluno TO BEFORE DROP Em um cadastro utilizado para reg
## 172 | gab=E | cand:  [texto-base: Julgue os itens seguintes, relativos a linguagem de consulta estruturada (SQL), linguagem de definição de dados (DDL) e linguagem de manipulação de dados (DML).]
Os comandos SQL são instruções ou consultas usadas para interagir com um banco de dados relacional, a exemplo do comando COMMIT disponibilizado na DML para manipular dados.
## 173 | gab=C | cand: 
Em banco de dados, atomicidade é o critério que define os elementos que compõem uma transação completa.
## 174 | gab=C | cand: P3·DADOS 3.8
A execução do comando SELECT * FROM PESSOA LIMIT 5, 10 apresentará 10 registros da tabela PESSOA, a partir do 6.º registro dessa tabela.
## 175 | gab=C | cand: 
DCL (data control language) é responsável pelas tarefas administrativas de controle do próprio banco de dados; em SQL, comandos de GRANT, REVOKE e DENY são exemplos de comandos utilizados para esse fim.
## 176 | gab=E | cand: 
Em um banco de dados, os comandos de SELECT, UPDATE, INSERT e DELETE estão agrupados como DML (data manipulation language).
## 177 | gab=E | cand: 
O termo CRUD refere-se aos comandos de INSERT, UPDATE, SELECT e DELETE, respectivamente, em um banco de dados.
## 178 | gab=C | cand: 
Considerando que CIDADANIA seja uma tabela com as colunas NOME_PESSOA, DATA_NASCIMENTO e NOME_PAIS, a execução do comando SQL SELECT NOME_PAIS, COUNT(*)    FROM    CIDADANIA     GROUP    BY    NOME_PAIS apresentará quantas pessoas nasceram em cada PAIS.
## 179 | gab=E | cand: P3·DADOS 1.5
Na criação de esquemas de banco de dados eficientes, a normalização excessiva pode levar a um desempenho ruim em consultas complexas, e, por isso, deve ser sempre evitada.
## 180 | gab=C | cand: P2·EVID 2.1, P3·DADOS 4.4
As chaves primárias em um banco de dados relacional são usadas para identificar unicamente cada registro em uma tabela.
## 181 | gab=E | cand: P2·GOV 5.3, P2·EVID 2.2
Em uma consulta a duas tabelas, o produto cartesiano ocorrerá quando a condição de união estiver corretamente especificada.
## 182 | gab=C | cand: 
Uma transação pode incluir múltiplas operações de acesso ao banco de dados, sejam elas para consulta ou modificação.
## 183 | gab=E | cand: P1·ESTADO 6.2, P3·ENG 2.4
Os índices de uma tabela são arquivos diferenciados que contêm todas as colunas da tabela, em ordem específica.
## 184 | gab=C | cand: P3·ARQ 1.5, P3·ENG 2.1
O padrão MVC é obtido ao se colocar o componente Controller para controlar o fluxo da aplicação entre as camadas de apresentação e de manipulação de dados.
## 185 | gab=E | cand: 
A integridade dos dados em um banco de dados é automaticamente mantida, dispensando-se a implementação de medidas adicionais de controle de proteção e segurança.
## 186 | gab=C | cand: P3·DADOS 1.5
SQL é uma linguagem utilizada para declarar e acessar tabelas em um banco de dados relacional, caracterizando-se como um padrão para especificar o esquema das tabelas e o acesso aos dados.
## 187 | gab=E | cand: P3·ARQ 1.7, P2·AUD 1.4 [texto-base: •   Cada um dos itens das provas objetivas está vinculado ao com que cada um deles esteja vinculado, marque, na Folha de Res julgue o item CERTO; ou o campo designado com o código marcação de ambos os]
In the first sentence of the second paragraph, the word “jeopardize” is being used with a similar meaning as the one of enhance. A seguir, a figura I apresenta o conjunto U e três subconjuntos identificados por A, B e C, e as figuras II e III destacam subconjuntos específicos do conjunto U. Figura I
## 188 | gab=C | cand: P2·TRANSP 5.3, P3·ENG 2.8
O subconjunto destacado na figura III pode ser expresso como A ⋂B ⋃ C େ , em que B ⋃ C େ significa o complementar do conjunto (B ⋃ C) em U.
## 189 | gab=C | cand: P2·TRANSP 5.3
O subconjunto destacado na figura II pode ser expresso como C ⋂ B      A.
## 190 | gab=E | cand: P3·ARQ 1.7, P2·AUD 1 [texto-base: Julgue os itens seguintes, relacionados à lógica proposicional, considerando os símbolos lógicos comuns e as letras maiúsculas como representativas de proposições lógicas simples.]
Se P, Q e R representam proposições lógicas e as primeiras três colunas da tabela-verdade são as apresentadas a seguir, então a última coluna da tabela-verdade relacionada à expressão (P ˄ R) ˅ (Q ˄ R) apresenta valores V ou F, tomados de cima para baixo, na sequência V, F, V, V, F, F, F e F. P     
## 191 | gab=C | cand: P2·GOV 5.3, P3·DADOS 3.6
Para resultados de sondagens de simples reconhecimento com SPT, o índice de resistência à penetração é expresso como a soma do número de golpes requeridos para a segunda e terceira etapas de penetração de 15 cm, adotando-se os números obtidos nessas etapas mesmo quando a penetração não tiver sido de
## 192 | gab=E | cand: P3·ARQ 1.7, P3·SEG 5.4
O comportamento das areias sob baixos níveis de tensão é praticamente constante, independentemente do índice de vazios inicial. OS ESPECÍFICOS -Em relação a projetos e execução de barragens de terra, julgue os itens subsequentes. Para esse tipo de barragem, a construção do sistema extravasor deve se
## 193 | gab=C | cand: P3·DADOS 1.8, P3·DADOS 1.6
Uma view é baseada em um tipo de consulta executada em uma ou mais tabelas em um banco relacional; normalmente é um tipo de consulta complexa e utilizada com frequência.
## 194 | gab=E | cand: P3·DADOS 1.4, P3·ENG 2.5, P3·ENG 2.1
Um DW é projetado para armazenar dados operacionais históricos, utilizando a mesma estrutura dos dados transacionais, com o objetivo de diminuir a latência nas consultas analíticas.
## 195 | gab=C | cand:  [texto-base: Julgue os itens a seguir, que dizem respeito a coleta, tratamento, armazenamento, integração e recuperação de dados, bem como a segurança da informação.]
Uma das atividades de um administrador de banco de dados é a revogação de privilégios, realizada para cancelar certos privilégios que foram concedidos anteriormente a determinadas contas.
## 196 | gab=E | cand: 
O cursor armazena, em memória, uma única linha do comando de SELECT de uma consulta que tenha sido efetuada em tabelas do banco de dados.
## 197 | gab=C | cand: 
A linguagem de controle de dados (DCL) é um dos componentes da SQL e permite gerenciar as autorizações aos dados constantes do banco de dados.
## 198 | gab=E | cand: P3·DADOS 1.5
Os esquemas de um banco de dados dividem fisicamente as tabelas, evitando o acesso cruzado entre objetos de diferentes esquemas.
## 199 | gab=C | cand: P3·DADOS 1.2 [texto-base: 677001_01N727917 -- CONHECIMENTO No que diz respeito aos dados estruturados e não estruturados, aos bancos de dados relacionais, ao modelo de referência CRISP-DM e à modelagem preditiva, julgue os ite]
No banco de dados relacional, é permitido criar uma chave primária utilizando-se dois ou mais campos definidos como chaves estrangeiras.
## 200 | gab=C | cand: P2·EVID 2.1
O comando a seguir, além de conceder o privilégio de leitura na tabela outorga para o usuário mcom, permite também que o mcom possa conceder esse privilégio para outros usuários. GRANT SELECT ON outorga TO mcom WITH GRANT OPTION;
## 201 | gab=E | cand: 
O comando CREATE TABLE pode ser usado para realizar o backup de uma única tabela, copiando seus dados e suas definições (chaves primárias, estrangeiras, índices, entre outros); por exemplo, o comando a seguir cria o backup da tabela radcom. CREATE TABLE radcom; radcom_bkp AS SELECT * FROM
## 202 | gab=E | cand: P2·DIR 1.1, P2·TRANSP 1.2
O conceito de menor privilégio é considerado irrelevante para a definição de controle de acesso a recursos computacionais necessários para realizar uma dada tarefa.
## 203 | gab=E | cand: P3·DADOS 1.4
A atomicidade do dado garante que os efeitos de uma transação bem-sucedida sejam permanentemente armazenados no banco de dados, mesmo em caso de falhas no sistema.
## 204 | gab=E | cand: P2·EVID 2.1, P2·DIR 5.1
As tabelas de dimensão na modelagem para BI são estruturas de dados com informações agregadas e medidas específicas.
## 205 | gab=C | cand: 
Considere-se a seguinte expressão SQL. select categoria, modelo, sum(valor) from dados group by cube(categoria, modelo) Essa expressão, após executada, apresentará o resultado a seguir. categoria|modelo|sum| ---------+------+---+ | |231| 1|A | 58| 2|B | 97| 1|B | 76| 2| | 97| 1| |134| |B |173| |A | 
## 206 | gab=E | cand: 
As expressões SQL a seguir geram resultados que são equivalentes. delete from dados; drop table dados;
## 207 | gab=C | cand: P1·ADM 2.1, P3·DADOS 3.8
As expressões SQL a seguir, após serem executadas, gerarão o mesmo resultado. insert into dados values (2,'C',40); insert into dados (categoria, modelo, valor) values (2,'C',40);
## 208 | gab=E | cand: P2·AUD 1.2, P2·EVID 3.1
Em banco de dados, o recurso de programação do tipo procedimento é utilizado de forma automática e implícita sempre que ocorre um evento tal como INSERT, UPDATE ou DELETE associado à tabela.
## 209 | gab=C | cand: 
Monitorar e ajustar o desempenho do banco de dados, a fim de otimizar o tempo de resposta das consultas, é uma das técnicas para a detecção de problemas e a otimização de desempenho.
## 210 | gab=C | cand: P3·ENG 2.1, P3·ARQ 4.1
Na linguagem SQL, os comandos CREATE, ALTER e DROP são comandos de definição de dados.
## 211 | gab=E | cand: P1·ETICA 4.2, P1·ETICA 3.1
Na linguagem SQL, a função agregada para cálculo de média de um único atributo deve ser combinada com a cláusula GROUP BY.
## 212 | gab=C | cand: P1·ESTADO 4.1, P3·DADOS 1.2
Alguns bancos de dados possuem opção de replicação de tabelas, com o objetivo de desafogar o servidor principal, direcionando as consultas mais pesadas para as réplicas.
## 213 | gab=C | cand: 
A integridade referencial é uma parte essencial de qualquer banco de dados relacional, que, entre outros benefícios, facilita as consultas.
## 214 | gab=E | cand: P3·SEG 5.3, P3·DADOS 1.1
A modelagem dimensional é uma técnica de modelagem de banco de dados que usa um modelo de dados baseado em dimensões para organizar os dados, e as tabelas de dimensões são sempre as maiores tabelas do modelo dimensional.
## 215 | gab=E | cand: P3·SEG 1.1, P3·ENG 2.3, P3·ENG 2.1
Somente são possíveis os seguintes quatro tipos de JOIN em SQL, segundo o padrão ANSI: INNER JOIN, LEFT JOIN, RIGHT JOIN e CROSS JOIN.
## 216 | gab=C | cand: P2·TRANSP 1.2, P3·ENG 1.5 [texto-base: Considerando as disposições da Consolidação das Leis do Trabalho (CLT), julgue os seguintes itens, relativos a rescisão e alteração do contrato de trabalho, aviso prévio, convenções e acordos coletivo]
Nos contratos em que não esteja previsto revezamento quinzenal ou semanal de trabalho, a remuneração da hora noturna, definida como equivalente a 52 minutos e 30 segundos, deve ser superior à da diurna.
## 217 | gab=E | cand: P3·DADOS 3.1, P3·ARQ 1.7
Com base nos dados apresentados nas referidas tabelas, é correto afirmar que o índice de eficiência desse datacenter é de 48%, o que significa dizer que, de 100% da energia que é injetada, somente 48% chegam alimentando a carga em TI e o restante é consumido antes de chegar à carga de TI.
## 218 | gab=C | cand: P1·ADM 2.1, P3·ARQ 1.7 [texto-base: No que se refere à biblioteca Pandas, julgue o próximo item. 91   import pandas as pd a = [10, 78, 23] myvar = pd.Series(a, index = [“x”, “y”, “z”]) print(myvar.describe()) Caso o código em Python pre]
O resultado da execução do código Python a seguir resultará em valores diferentes para as variáveis c e d. import numpy as np a = np.array([[1,2],[3,4]]) b = np.array([[4,3],[2,1]]) c= np.dot(a,b) print(c) d=a*b print(d) 93   import numpy as np a = np.array([(1, 2), (3, 4),                 (5,   6)]
## 219 | gab=E | cand: P2·AUD 1.2, P3·ARQ 4.5, P3·ARQ 3.3
Spark é uma arquitetura de sistema operacional para trabalhar com dados organizados de forma hierárquica, utilizando-se o módulo Spark SQL, que permite consultar arquivos pelo seu conteúdo.
## 220 | gab=C | cand: 
Na técnica de modificação de banco de dados adiada, a atomicidade da transação é garantida registrando-se todas as modificações do banco de dados no log, mas adiando-se a execução de todas as operações WRITE de uma transação até que a transação seja parcialmente confirmada, para transações executada
## 221 | gab=E | cand: 
Views não inserem restrições à realização de consultas, inserções, atualizações e exclusões em tempo de execução, sendo, portanto, desnecessário traduzi-las para uma modificação nas relações reais no modelo lógico do banco de dados.
## 222 | gab=E | cand: P3·ARQ 1.7, P3·ARQ 5.1 [texto-base: Considerando a figura precedente, que representa a arquitetura de um sistema de banco de dados PostgreSQL, julgue o item seguinte, acerca do processo de administração desse banco de dados.]
O processo servidor de back-end é responsável por executar as consultas submetidas pelo cliente, realizando as etapas necessárias de execução de consulta e retornando ao processo postmaster, onde as consultas são analisadas, otimizadas e acumuladas em buffers de consultas e distribuídas ao cliente. 
## 223 | gab=C | cand: 
A escolha do tipo de índice é um aspecto importante para o desempenho do sistema de banco de dados: se as consultas de intervalo forem comuns, os índices de árvore B, os quais possuem uma forma de árvore balanceada, serão preferíveis aos índices de hash, os quais organizam as chaves de busca, com se
## 224 | gab=E | cand: P3·SEG 2.5, P2·DIR 1.1
A automação bioquímica tem como desvantagem a diminuição da segurança dos processos laboratoriais, uma vez que os métodos manuais são mais seguros que os sistemas automatizados. A dosagem de hormônios e enzimas desempenha um papel crucial no diagnóstico clínico de diversas doenças, proporcionando in
## 225 | gab=E | cand: P3·ARQ 1.7, P2·TRANSP 4.2 [texto-base: Considerando o sinal de tempo discreto              =    e ହ sabendo que a transformada Z de                é   , julgue os próximos itens. ଵ 84     =      మ      . ଵି ௓ షభ ఱ ଶ 85    ]
A região de convergência de   é || > 0. Considerem-se os cinco sinais de tempo discreto ଵ , ଶ ,  ଷ , ସ  e ହ . Considere-se, ainda, que esses sinais apresentem valores não nulos para 0 ≤  <  e valores nulos para  < 0 ou  ≥ . Considere-se, também, que a transformada de Fourier d
## 226 | gab=E | cand: P3·ARQ 1.7, P2·AUD 1.2
Se os valores a = 3, b = 4 e c = 8 forem entradas do algoritmo a seguir e o sistema no qual o algoritmo for executado utilizar números decimais com quatro casas de precisão, então a execução do referido algoritmo apresentará em tela o resultado 10.3923. sp = (a + b + c)/2; ar = sp*(sp - a)*(sp - b)*
## 227 | gab=C | cand: P3·ENG 2.1
Comandos expressos em         linguagem de definição de dados (DDL) são utilizados para criar estruturas de um banco de dados, e o seu processamento irá incluir ou alterar metadados desse mesmo banco de dados.
## 228 | gab=E | cand: 
Usando-se SQL (structured query language), é possível unir o resultado de duas instruções SELECT quaisquer, por meio do operador UNION.
## 229 | gab=E | cand: P3·DADOS 1.8, P3·DADOS 1.4
A manipulação de dados armazenados em um banco de dados é feita por meio de DML (Data Manipulation Language), linguagem na qual é possível apenas descrever os dados que se deseja acessar, sem especificar como obtê-los.
## 230 | gab=E | cand: 
No processamento de transações em um sistema de banco de dados, o uso de bloqueios (locks) tem o objetivo de garantir a propriedade da atomicidade das transações.
## 231 | gab=E | cand: P3·DADOS 1.2, P2·EVID 2.1
A transferência dos valores de IOF devidos por correntistas de bancos privados nas operações de uso de cheque especial, em que o banco envia os valores retidos diretamente à Conta Única do Tesouro Nacional, representa a etapa denominada arrecadação.
## 232 | gab=E | cand: P3·DADOS 3.8, P3·ENG 2.1 [texto-base: Julgue os itens subsequentes, relativos às especificações de serviços e à execução dos serviços de terraplenagem, pavimentação, drenagem e sinalização de uma obra rodoviária.]
A inclinação dos taludes dos cortes independe do controle tecnológico realizado durante a execução do serviço; nos cortes em altura elevada, em função do definido no projeto de engenharia, devem ser implantados patamares, com banquetas de largura mínima de 0,5 m, valetas revestidas e proteção vegeta
## 233 | gab=C | cand: P3·DADOS 1.4, P3·ARQ 1.4 [texto-base: Considerando o caso hipotético apresentado, julgue os seguintes itens, referentes à psicologia do desenvolvimento e a teorias e técnicas psicoterápicas.]
Conforme o curso esperado do desenvolvimento infantil, Beto teria aprendido a correr antes de desenvolver a habilidade de usar um lápis. JUSTIFICATIVA - Certo. É esperado, no curso do desenvolvimento típico, que as habilidades motoras grosseiras (correr, pular, saltar) antecedam as habilidades manip
## 234 | gab=C | cand: P3·ARQ 1.7, P2·DIR 4.2 [texto-base: Considerando esse caso clínico hipotético, julgue os itens a seguir, referentes ao processo de envelhecimento, a doenças crônicas e degenerativas e à saúde mental na terceira idade.]
A apresentação característica amnéstica pode ser sugestiva de síndrome de transtorno neurocognitivo, de acordo com o Manual Diagnóstico e Estatístico de Transtornos Mentais (DSM-5 TR). JUSTIFICATIVA - Certo. De acordo com o Manual Diagnóstico e Estatístico de Transtornos Mentais, na síndrome de tran
## 235 | gab=C | cand: P3·ENG 2.1, P1·ESTADO 7.1
O algoritmo do balde vazado é um método de controle de congestionamento em que um número variável de solicitações é temporariamente armazenado e organizado em uma saída de pacotes com taxa definida, em um modo de transferência assíncrona; ele é usado para implementar policiamento e modelagem de tráf
## 236 | gab=E | cand: P2·AUD 1.2
O uso de seletividade e estimativa de custos na otimização de consultas SQL consiste na modificação da representação interna de uma consulta em uma árvore de consulta com o objetivo de melhorar o seu desempenho. 678016_01N178787
## 237 | gab=C | cand: P3·DADOS 3.8, P2·GOV 4.1
Processos de armazenagem eficazes favorecem a cadeia de suprimentos, pois a perfeita execução das atividades diminui os índices de avarias, fornece registros confiáveis e possibilita o rastreamento dos produtos e o acesso a seu histórico.
## 238 | gab=C | cand: P2·EVID 2.1
A criação de tabelas e as restrições de integridade são atividades de administração de banco de dados descritas como DDL (data definition language).
## 239 | gab=C | cand: 
Em uma arquitetura do tipo banco de dados distribuídos, quando um servidor de banco de dados não tem os dados solicitados em uma consulta, ele obtém esses dados em outro servidor e devolve o resultado de forma transparente.
## 240 | gab=E | cand: 
Na arquitetura do tipo standalone, um servidor denominado backend executa consultas no banco de dados e, em seguida, retorna os resultados ao cliente.
## 241 | gab=C | cand: P3·ENG 2.1, P3·DADOS 1.4 [texto-base: 548009_01N562771 Nos itens que avaliarem conhecimentos de informática e(ou) informado o contrário, considere que todos os programas mencio proteção, de funcionamento e de uso em relação aos programas,]
A operação de definição de um banco de dados compreende especificar os tipos, as estruturas e as restrições dos dados que serão armazenados em dispositivos como discos (storage).
## 242 | gab=C | cand: P3·ARQ 1.7, P1·SOC 2.1 [texto-base: 548009_01N562771 Nos itens que avaliarem conhecimentos de informática e(ou) informado o contrário, considere que todos os programas mencio proteção, de funcionamento e de uso em relação aos programas,]
Um sistema gerenciador de banco de dados permite que sejam realizadas diversas ações no banco de dados, como, por exemplo, construir e manipular objetos.
## 243 | gab=E | cand:  [texto-base: 548009_01N562771 Nos itens que avaliarem conhecimentos de informática e(ou) informado o contrário, considere que todos os programas mencio proteção, de funcionamento e de uso em relação aos programas,]
Um banco de dados é, especificamente, um conjunto aleatório de dados não relacionados que refletem algo do mundo real.
## 244 | gab=C | cand: 
Uma das vantagens do uso da otimização automática, realizada pelos sistemas gerenciadores de banco de dados, está no fato de que os usuários não necessitam se preocupar com a melhor forma de expressar suas consultas para obter o melhor desempenho do sistema.
## 245 | gab=E | cand: 
A otimização semântica é uma das técnicas mais utilizadas para melhorar o desempenho das consultas em banco de dados; no entanto, nem toda restrição de integridade referencial pode ser usada, em princípio, nessa técnica.
## 246 | gab=C | cand: 
No processo de otimização, são usadas estatísticas do banco de dados que contribuem para a construção dos planos de consulta e para a escolha do plano mais econômico.
## 247 | gab=C | cand: P2·EVID 2.1
A indexação total de uma grande tabela com um índice B-tree tradicional pode ser custosa em termos de espaço em disco, porque os índices podem ser várias vezes maiores do que os dados na tabela.
## 248 | gab=E | cand: P2·AUD 1.4, P1·ETICA 2.2
Índices de bitmap não permitem linhas com valores NULL.
## 249 | gab=E | cand: P2·EVID 1.1, P2·EVID 2.1
Um administrador de bases de dados pode criar índices de bitmap em tabelas particionadas, e esses índices podem ser globais.
## 250 | gab=E | cand: P3·SEG 5.6
Para o processo de tuning, o PostgreSQL possui um parâmetro denominado shared_buffer, para melhoria de desempenho de entrada/saída (I/O, do inglês input/output) do banco de dados, parâmetro esse que é ajustável e fornece I/O direto aos dados, sem usar buffer de kernel.
## 251 | gab=C | cand: P3·ENG 2.1, P3·DADOS 1.4
ECM trata de conteúdos não estruturados, que não estão armazenados em tabelas de banco de dados, mas em diferentes tipos de estruturas, como celulares, arquivos, email e canais de atendimentos.
## 252 | gab=E | cand: 
No SQL, SELECT * FROM table é uma consulta de banco de dados e exibe informações da tabela do banco de dados, portanto é correto considerá-la uma mineração de dados.
## 253 | gab=E | cand: P2·AUD 1.2, P3·SEG 1.1 [texto-base: Considerando as informações apresentadas na figura precedente (captura de tela de uma sessão do SQL*Plus), relativas a comandos SQL, julgue os itens que se seguem.]
Empregada de forma correta no código em questão, pois se relaciona a um bloco anônimo de PL/SQL, a variável &numero_proc, na linha 2, não pode ser utilizada em comandos DML.
## 254 | gab=C | cand:  [texto-base: Considerando as informações apresentadas na figura precedente (captura de tela de uma sessão do SQL*Plus), relativas a comandos SQL, julgue os itens que se seguem.]
O código em tela não criará nenhum objeto no banco de dados, como, por exemplo, procedure, triggers, packages e functions.
## 255 | gab=E | cand:  [texto-base: Considerando as informações apresentadas na figura precedente (captura de tela de uma sessão do SQL*Plus), relativas a comandos SQL, julgue os itens que se seguem.]
Ao se fechar a sessão do SQL*Plus na qual foi capturada a tela em apreço, a variável definida na linha 2 persistirá no banco de dados.
## 256 | gab=E | cand: P3·DADOS 3.8
Especialmente devido à expressão na linha 11, o comando a seguir, após executado, retornará três registros. SELECT a.idsoft, a.versao, a.descricao FROM 'vsoftware' a INNER JOIN ( SELECT idsoft, MAX(versao) versao FROM 'vsoftware' GROUP BY idsoft) b ON a.idsoft = b.idsoft AND a.versao = b.versao;
## 257 | gab=C | cand: 
A execução do comando SELECT a.idsoft, a.versao, a.descricao FROM 'vsoftware' a LEFT OUTER JOIN 'vsoftware' b ON a.idsoft = b.idsoft AND a.versao < b.versao WHERE b.idsoft IS NULL; retornará os seguintes dados. idsoft       versao        descricao 1            3             adicao da tela C. 2      
## 258 | gab=E | cand: 
A execução do comando SELECT a.id FROM 'software' a where a.id not in ( SELECT b.idsoft FROM 'vsoftware' b); terá resultado idêntico à execução do comando a seguir. SELECT distinct a.id FROM 'software' a left outer join 'vsoftware' b on a.id=b.idsoft;
## 259 | gab=C | cand: 
Nas instruções seguintes, a palavra-chave IMMUTABLE indica que a função criada não pode modificar o banco de dados. CREATE FUNCTION add(integer, integer) RETURNS integer AS 'select $1 + $2;' LANGUAGE SQL IMMUTABLE RETURNS NULL ON NULL INPUT;
## 260 | gab=C | cand: P1·ETICA 5.1, P3·DADOS 1.8
Os dados nos SGBDs são organizados em blocos, em que os sistemas de suporte à decisão (DSS) e os ambientes de banco de dados de data warehouse tendem a se beneficiar de valores de tamanho de bloco maiores.
## 261 | gab=C | cand: P3·DADOS 1.8, P3·DADOS 1.4
Os blocos de dados são organizados em cabeçalho (row header) e dados (column data); a cada nova transação, o registro é armazenado como uma nova linha na tabela e, assim, um registro é armazenado em várias colunas em blocos de dados no disco.
## 262 | gab=C | cand: P3·ARQ 1.5, P3·ENG 2.5
Em sistemas desenvolvidos em Java, o objetivo do framework Hibernate é a transformação das classes para tabelas de dados, com a geração dos comandos SQL.
## 263 | gab=E | cand: 
De acordo com a definição das variáveis, o trecho de código a seguir permite uma conexão ao banco de dados em questão, sem gerar nenhum tipo de erro. . . . try { Class.forName(VAR1); conn = DriverManager.getConnection(VAR1, VAR3, VAR4); . . .
## 264 | gab=C | cand: P1·SOC 1.1, P2·AUD 2.1
A elaboração de um planejamento estratégico deve ser norteada pelos pressupostos inerentes à missão, visão e valores organizacionais, para uma melhor definição dos planos de ação direcionados ao alcance de objetivos e metas.
## 265 | gab=C | cand: 
Atomicidade da transação em um banco de dados ocorre quando todas as operações da transação são refletidas corretamente no banco de dados; ou quando nenhuma delas é refletida.
## 266 | gab=E | cand: 
Bloqueio de um banco de dados é gerado para contornar o conflito de consulta simultânea de tabelas por um usuário do aplicativo desenvolvido.
## 267 | gab=C | cand: P2·GOV 4.1
Em normalização de banco de dados, na terceira forma normal os valores em um registro que não fazem parte da chave desse registro não pertencem à tabela; em geral, sempre que o conteúdo de um grupo de campos se aplica a mais de um único registro na tabela, recomenda-se colocar esses campos em uma ta
## 268 | gab=C | cand: P1·ESTADO 4.1
O principal objetivo de um sistema de gerenciamento de banco de dados (SGDB) é retirar da aplicação cliente a responsabilidade de gerenciar o acesso, a persistência, a manipulação e a organização dos dados.
## 269 | gab=C | cand: 
Entre outras funcionalidades, uma stored procedure pode melhorar o desempenho de um banco de dados e criar tarefas agendadas; procedimentos de sistema são armazenados no banco de dados padrão do SQL Server e executam as tarefas administrativas, a partir de qualquer banco de dados.
## 270 | gab=E | cand: 
Por meio do comando SQL a seguir, é possível recuperar o nome dos pesquisadores responsáveis por projetos, seguido pelo nome de seu orientador, mas apenas os projetos orientados por Pedro. select responsavel.nome nomeresponsavel, orientador.nome nomeorientador, tituloProjeto from Pesquisador respons
## 271 | gab=C | cand: P2·AUD 1.2, P2·EVID 2.1 [texto-base: Nos itens que avaliarem conhecimentos de informática e(ou) informado o contrário, considere que todos os programas mencio proteção, de funcionamento e de uso em relação aos programas, arq -- CONHECIME]
O índice secundário é empregado quando se utiliza um campo de indexação que não seja a chave primária da tabela. tabela1 campo 0 2 3 3 4 4 6 7 tabela2 campo 5 5 7 8 8 9
## 272 | gab=E | cand: P2·DIR 1.1, P2·EVID 2.1
Considere que o comando a seguir seja executado sem erro. select campo from tabela2 where exists (select campo from tabela1) Nesse caso, o resultado será a tabela seguinte.
## 273 | gab=E | cand: P2·DIR 1.1, P2·EVID 2.1
Considere que o comando a seguir seja executado sem erro. select campo from tabela2 except select campo from tabela1 Nesse caso, o resultado obtido será a tabela seguinte.
## 274 | gab=E | cand: P2·EVID 2.1, P3·DADOS 1.5 [texto-base: Julgue os próximos itens, com relação à segurança e arquitetura de banco de dados e administração de dados e de banco de dados. O role contém as definições de permissões, privilégios e garantias de ac]
Um esquema de banco de dados pode ser definido como a representação gráfica e simbológica dos componentes de um banco de dados, seja comercial, industrial ou residencial.
## 275 | gab=E | cand: P2·EVID 2.1 [texto-base: Julgue os próximos itens, com relação à segurança e arquitetura de banco de dados e administração de dados e de banco de dados. O role contém as definições de permissões, privilégios e garantias de ac]
O comando create database aluno permite criar uma tabela de nome aluno no banco de dados.
## 276 | gab=E | cand: P2·DIR 3.4, P2·AUD 1.2
Informação pode ser definida como um conjunto de fatos diferentes relativos a uma transação e que é, geralmente, desprovida de significado; ela é considerada a matéria-prima dos sistemas de informação.
## 277 | gab=C | cand: 
Ao se criar um índice, deve-se observar, inicialmente, o seu impacto no banco de dados com relação às operações de atualização.
## 278 | gab=E | cand: P2·EVID 2.1 [texto-base: Julgue os próximos itens, com relação à engenharia de software. A atividade projeto e implementação juntamente com a validação do software são duas atividades executadas no processo de desenvolvimento]
Se as tabelas a seguir descrevem a quantidade e a complexidade das funções de dados e de transação de duas aplicações #A e #B, então a quantidade de pontos de função brutos da aplicação #A é maior que a da aplicação #B.
## 279 | gab=E | cand: 
No PostgreSQL 13 é possível obter informações das configurações correntes do SGBD por meio de consultas às suas views nativas. O comando abaixo permite obter o número máximo de conexões ativas que uma database, de nome bancodedados, pode receber. SELECT max_connections FROM pg_stat_database WHERE da
## 280 | gab=C | cand: 
A instrução SQL a seguir tem por finalidade listar os números dos advogados na OAB (advogado_oab_numero) e o total de processos (total_processos), mas somente daqueles que possuem mais de cinco processos. SELECT advogado_oab_numero, count(*) as total_processos FROM processo GROUP BY advogado_oab_num
## 281 | gab=E | cand: 
O comando RMAN> SHUTDOWN IMMEDIATE; não pode ser executado no Oracle, pois a operação de desligar o banco de dados somente é permitida por meio do SQL PLUS.
## 282 | gab=E | cand: 
SELECT é uma instrução de controle de banco de dados que permite recuperar o conteúdo de uma ou mais tabelas.
## 283 | gab=E | cand: 
Em uma consulta SQL que contém as cláusulas WHERE e HAVING, a cláusula WHERE é aplicada às linhas no conjunto de resultados. ||281FUB_013_01N943377||
## 284 | gab=C | cand: P3·ENG 2.5, P3·ENG 2.1
Em sistemas gerenciados de banco de dados, a independência dos dados refere-se à capacidade de modificar a estrutura lógica ou física do banco, sem a necessidade de uma reprogramação dos programas de aplicativos.
## 285 | gab=E | cand: P3·ARQ 4.2, P2·EVID 2.1
Uma visão representa um conjunto de informações de uma ou mais tabelas, em uma representação específica, ocupando espaço físico no banco de dados.
## 286 | gab=E | cand: P2·TRANSP 4.3, P2·TRANSP 2.1
Views são visões de tabelas de banco de dados e são armazenadas em disco, com as informações de condições e situações que necessitem de atualização constante.
## 287 | gab=C | cand: P2·AUD 4.2, P1·ESTADO 9.4 [texto-base: Acerca de técnicas de análise de desempenho e otimização de consultas, balanceamento de carga, failover e replicação de estado, julgue os itens a seguir.]
Otimizador de consulta tem por objetivo gerar um plano de avaliação de consulta que calcule o mesmo resultado da expressão analisada.
## 288 | gab=C | cand: P3·ARQ 4.1 [texto-base: Acerca de técnicas de análise de desempenho e otimização de consultas, balanceamento de carga, failover e replicação de estado, julgue os itens a seguir.]
Em um banco de dados distribuídos, a replicação aumenta o desempenho das operações de leitura e, também, a disponibilidade dos dados. OS ESPECÍFICOS -Julgue os próximos itens, a respeito de arquitetura de OLAP, data warehousing e dados multidimensionais.
## 289 | gab=E | cand: P3·DADOS 1.5
Em um banco de dados NoSQL orientado a documentos, a inexistência de um esquema impossibilita a definição de índices.
## 290 | gab=C | cand: P3·ARQ 5.4, P3·ARQ 1.3
Os Extended Events no Microsoft SQL Server são ferramentas de monitoramento e diagnóstico, que permitem rastrear eventos com baixo impacto de desempenho, com maior flexibilidade e precisão, substituindo o SQL Profile.
## 291 | gab=E | cand: P3·DADOS 1.4
No PostgreSQL, o mecanismo TOAST é essencial para armazenar eficientemente dados de grande tamanho, permitindo que o banco de dados gerencie colunas com valores extensos, como TEXT e BYTEA, sem ultrapassar o limite de 16 KB por linha.
## 292 | gab=C | cand:  [texto-base: Julgue os seguintes itens, relativos a técnicas de visualização de dados em business intelligence, a data lakes e a regras de associação em mineração de dados.]
A execução da consulta SQL a seguir listará todos os processos, inclusive aqueles que ainda não têm partes associadas, e exibirá o nome das pessoas e os seus respectivos papéis nos processos em que estão envolvidas. SELECT p.numero_processo, ps.nome, pa.tipo_parte FROM Processos p LEFT JOIN Partes p
## 293 | gab=C | cand: P3·ARQ 4.4, P3·DADOS 1.5, P3·DADOS 1.4
Em sistemas distribuídos, técnicas de análise de desempenho e otimização de consultas (tuning) envolvem particionamento de dados entre nós, uso de cache distribuído, ajuste de parâmetros de redes, avaliação de latência e análise de balanceamento de carga, com o objetivo de melhorar a eficiência gera
## 294 | gab=C | cand:  [texto-base: Em relação ao controle de qualidade dos alimentos, às boas práticas de manipulação e às análises de perigos e pontos críticos de controle, julgue os itens seguintes.]
A falta de higiene ou a manipulação incorreta de alimentos como ovos, leite cru, carne de aves, suínos e bovinos, vegetais e pescado pode causar infecção, por permitir a multiplicação da bactéria salmonella sp.
## 295 | gab=E | cand: P3·ARQ 1.7, P2·AUD 1.2, P1·ESTADO 7.1 [texto-base: Acerca dos sistemas agroflorestais, julgue os itens seguintes. O uso de sistemas agroflorestais pode causar diversos impactos na qualidade do solo, como: manutenção do teor de matéria orgânica; melhor]
O cajá-manga necessita de porta-enxerto de umbuzeiro para produzir em regiões com condições edafoclimáticas mais adversas, principalmente em áreas com precipitações inferiores a 500 mm. Para a enxertia, devem-se utilizar garfos com maiores diâmetros, ou seja, mais lignificados, uma vez que estes têm
## 296 | gab=E | cand: P2·AUD 1.3, P2·GOV 2.2
O índice de vegetação por diferença normalizada (NDVI) é calculado a partir da relação entre a refletância do infravermelho próximo (NIR) e a refletância do vermelho (RED); valores próximos de −1 indicam vegetação densa e saudável, ao passo que valores próximos de 1 indicam áreas desprovidas de vege
## 297 | gab=C | cand: P3·ARQ 1.5, P1·ETICA 2.2 [texto-base: -- CONHECIMENTO No estudo de modelagem de vulnerabilidade à desertificação de determinada região semiárida do Nordeste brasileiro, foram utilizadas as seguintes variáveis, que serão analisadas por mei]
A susceptibilidade à desertificação é inversamente proporcional aos valores de índice de vegetação.
## 298 | gab=C | cand: P1·ETICA 3.1 [texto-base: Julgue os próximos itens, considerando que os sensores imageadores podem ser classificados em sensores ópticos e de radar, dependendo da operação em faixas espectrais do visível, infravermelho próximo]
Na equação do EVI, a reflectância na faixa espectral do azul tem a função de minimizar os efeitos atmosféricos nesse índice.
## 299 | gab=C | cand: P2·AUD 2.1, P3·DADOS 3.6
O planejamento operacional de uma instituição deve gerar planos compostos pela especificação das etapas para realização das metas e estabelecer programações e cronogramas de execução. procedimentos,
## 300 | gab=C | cand: 
A principal finalidade da linguagem SQL (structured query language) em um banco de dados relacional é permitir operações como consulta, adição e exclusão de dados.
## 301 | gab=E | cand: P3·DADOS 1.8, P3·SEG 5.6
É na fase de mineração do data mining que são definidos os metadados dos dados manipulados.
## 302 | gab=C | cand: P2·TRANSP 5.2, P3·DADOS 3.9
As ferramentas de tratamento de dados oferecem recursos que contemplam tanto a limpeza e padronização de dados, com funcionalidades que incluem correções de erros e remoção de duplicatas, quanto a transformação de dados, com funcionalidades que incluem filtragem de dados, junções de tabelas, agregaç
## 303 | gab=E | cand: P2·AUD 2.3, P2·DIR 3.2 [texto-base: Julgue os itens subsecutivos, no que diz respeito às relações entre as instituições federais de ensino superior e de pesquisa científica e tecnológica e as fundações de apoio a projetos de ensino, pes]
Os planos de trabalho das fundações de apoio referentes aos projetos desenvolvidos com as instituições apoiadas devem conter, no mínimo: objeto, projeto básico, prazo de execução limitado no tempo, e resultados esperados.
## 304 | gab=C | cand: P3·DADOS 1.8, P3·DADOS 1.6
Uma VIEW é uma representação virtual de dados que se comporta como uma tabela, formada a partir de uma consulta em tabelas relacionadas.
## 305 | gab=C | cand: P3·DADOS 1.9, P3·DADOS 1.8
Um relacionamento N:N no modelo entidade-relacionamento dá origem a uma tabela associativa no modelo físico do banco de dados.
## 306 | gab=E | cand: P3·DADOS 1.4
View é uma visualização customizada de uma ou mais tabelas, com seus dados armazenados fisicamente e montada a partir da execução de uma consulta.
## 307 | gab=E | cand: P2·AUD 1.2, P2·DIR 3.2
O quadro clínico apresentado pela paciente é altamente sugestivo de osteoartrite, que acomete preferencialmente as articulações metacarpofalangianas. Um paciente de sessenta e oito anos de idade, com diagnóstico de diabetes melito do tipo 2 havia oito anos, em uso regular de metformina 2 gramas ao d
## 308 | gab=E | cand: P1·ESTADO 9.1, P2·DIR 3.4
Supondo-se que, na próxima consulta, esse paciente apresente piora clínica, com dispneia a curtas distâncias e até mesmo ao se vestir, e que seus exames laboratoriais indiquem diagnóstico inaugural de diabetes melito, o antidiabético oral de escolha deverá ser a glitazona. ||Matriz_496_RM002|| Um ho
## 309 | gab=C | cand: P3·ARQ 5.4, P3·SEG 3.3 [texto-base: Acerca da conduta em relação ao diagnóstico e tratamento da tuberculose e ao manejo das crianças e do adolescente da família em questão, julgue os próximos itens.]
O teste rápido molecular para o diagnóstico da tuberculose e resistência a rifampicina permite o diagnóstico da doença em duas horas.
## 310 | gab=C | cand: P2·GOV 2.2, P3·ARQ 1.7
Um menino com sete anos de idade foi levado a consulta médica por nunca ter obtido controle esfincteriano urinário noturno. Ele obteve controle urinário diurno com cerca de três anos de idade. Urinava cerca de seis vezes ao dia e não apresentava disúria ou urgência miccional. Nessa situação hipotéti
## 311 | gab=E | cand: P2·TRANSP 1.2, P3·ENG 1.5 [texto-base: A respeito da metodologia de orçamentação do Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil (SINAPI), julgue os itens subsequentes.]
Na definição dos custos horários dos equipamentos, são contempladas as paralisações e as reduções de produtividade oriundas das chuvas previstas no histórico pluviométrico de cada região.
## 312 | gab=C | cand: P2·AUD 2.2, P2·AUD 1.2 [texto-base: Julgue os próximos itens, relativos às especificações de serviços, ao controle de materiais e a requisitos para execução de projetos e obras de terraplanagem.]
Os ensaios de compactação e o índice de suporte Califórnia (ISC) são utilizados, por exemplo, para avaliar a capacidade de suporte e a expansão dos materiais provenientes das áreas de empréstimos que serão utilizados na execução do corpo de aterros.
## 313 | gab=C | cand: P3·ENG 1.5, P3·DADOS 4.5 [texto-base: Considerando que servidor público de determinada autarquia federal tenha solicitado ao setor técnico daquela entidade a emissão de parecer para subsidiar sua tomada de decisão, julgue os itens a segui]
A definição de servidor público, em sentido amplo, engloba os empregados públicos e servidores temporários.
## 314 | gab=C | cand: P3·ARQ 1.7
A mufla é um tipo de terminal primário que serve para garantir a deflexão do campo elétrico. R. Boylestad. Introdução à análise de circuitos. São Paulo: Prentice Hall, 2004, p. 653 (com adaptações). A figura apresentada ilustra um transformador ideal monofásico com dois secundários, em que N, E e Z 
## 315 | gab=C | cand: P3·ARQ 4.1, P2·AUD 3.2
Considerando-se que o nível de renda inicial seja igual a R$ 275 e o equilíbrio do nível de renda (Y) seja expresso por Y=                       , em que há três agentes econômicos, é correto afirmar que, com base nos dados apresentados na tabela a seguir, Y seria R$ 25 menor caso não houvesse o age
## 316 | gab=C | cand: P3·ARQ 1.7, P2·TRANSP 1.1
As variações patrimoniais devem ser reveladas pela contabilidade mesmo quando não resultem de execução orçamentária. Denomina-se mensuração o processo contábil que consiste em determinar e apresentar os valores referentes a itens do ativo e do passivo, mediante o emprego de métodos qualitativos e qu
## 317 | gab=E | cand: P3·SEG 5.3, P2·DIR 5.1
Os preços de insumos e custos de composição do SINAPI são coletados pela Caixa Econômica Federal, que realiza o tratamento dos dados e a formação dos índices, para posterior disponibilização para consultas. O estudo da geometria das tubulações é fundamental para garantir o fluxo de água nas estrutur
## 318 | gab=E | cand: P3·DADOS 3.8, P2·TRANSP 3.3 [texto-base: A respeito do ensaio realizado e do perfil apresentado do subsolo, julgue os itens a seguir, considerando que o solo acima da rocha foi classificado como argila mole e que a protuberância está a 5 m d]
A fiscalização deveria ter medido o aterro por quantidade de material transportado, mediante apropriação dos custos de transporte de solo em caminhão basculante. Durante a execução de uma obra rodoviária, a contratada pleiteou o reajuste contratual, aplicando o percentual calculado pelo índice sobre
## 319 | gab=E | cand: 
Uma visão (view) é derivada de uma ou mais relações e armazena os dados em uma tabela física do banco de dados, visando tornar ágeis as consultas.
## 320 | gab=E | cand: P2·DIR 3.3, P1·SOC 1.1
A rentabilidade da Nota do Tesouro Nacional série B Principal (NTN-B Principal) é composta por uma taxa anual pactuada no momento da compra mais a variação do Índice Nacional de Preços ao Consumidor (INPC). A respeito das competências e atribuições do Conselho Monetário Nacional (CMN), do Banco Cent
## 321 | gab=C | cand: P3·DADOS 1.9, P1·ESTADO 9.1
Uma operação de derivativo de taxa de juros entre uma entidade fechada de previdência complementar e um banco só poderá ser realizada se, entre outros requisitos, a operação ou negociação for registrada em bolsa de valores ou de mercadorias e futuros.
## 322 | gab=C | cand: P2·AUD 1.3
Uma das formas de medir o grau de eficiência com que a equipe do projeto está realizando o trabalho é avaliar o índice de desempenho de prazos, que consiste em uma medida de eficiência do cronograma expressa como a razão entre valor agregado e valor planejado.
## 323 | gab=E | cand: P3·DADOS 4.6, P1·ESTADO 9.2
A dilação do prazo de execução poderá ser feita por apostila, desde que não se extrapole a vigência contratual e não haja acréscimo de valores.
## 324 | gab=E | cand: P3·DADOS 3.8, P2·AUD 3.2
Ocorrência é a afirmação que direciona o auditor para verificar se os valores e outros dados relacionados a transações e eventos registrados foram adequadamente registrados.
## 325 | gab=C | cand: P3·SEG 5.5, P1·ADM 4.1
O relatório resumido de execução orçamentária deve conter demonstrativo específico dedicado aos restos a pagar, evidenciando-se os valores inscritos, os pagamentos realizados e o montante a pagar.
## 326 | gab=E | cand: P1·ESTADO 9.4, P1·SOC 4.1 [texto-base: •   Cada um dos itens das provas objetivas está vinculado ao com que cada um deles esteja vinculado, marque, na Folha de Res julgue o item CERTO; ou o campo designado com o código marcação de ambos os]
A proteção constitucional aos direitos dos povos originários sobre as terras que tradicionalmente ocupam está condicionada à configuração do renitente esbulho, definido como o efetivo conflito possessório, persistente até a data de promulgação da Constituição Federal de 1988, materializado por circu
## 327 | gab=E | cand: P3·DADOS 1.9, P3·ENG 2.7
Normalização de banco de dados é um conjunto de regras que visa, principalmente, à organização de um projeto de banco de dados para aumentar tanto a redundância quanto a integridade dos dados, sem interferir no desempenho.
## 328 | gab=C | cand: P1·SOC 5.1, P3·SEG 5.5 [texto-base: LEGISLAÇÃO FEDERAL E ESTADUAL DO CEARÁ ESPECÍFICA SOBRE A TEMÁTICA (LEIS, DECRETOS E DEMAIS NORMATIVAS DISPONIBILIZADAS NA INTERNET) Com base na Lei estadual n.º 18.662/2023, que apresenta o Plano Plu]
Considere que, no período de janeiro a abril de 2024, o Banco Central tenha registrado, no balanço de pagamentos do Brasil, as informações apresentadas na tabela a seguir, dadas em milhões de dólares. Nesse caso, é correto concluir que o saldo das transações correntes, no mesmo período, foi exatamen

## CÓDIGOS CANDIDATOS (texto do edital)
- P1·ADM 1.1: Administração direta e indireta; descentralização e desconcentração; agentes públicos; funções da administração pública: formulação, execução, regulação e contr
- P1·ADM 2.1: Burocracia e profissionalização; gestão orientada a resultados; participação e governança; limites e contribuições de diferentes modelos na realidade brasileira
- P1·ADM 4.1: Funções do planejamento e do orçamento; relação entre PPA, LDO e LOA; receita e despesa em nível conceitual; restrições fiscais, escolhas alocativas e sustentab
- P1·ESTADO 4.1: Fundamentos e objetivos da República; direitos fundamentais, sociais e políticos; igualdade, devido processo e limites ao exercício do poder; princípios da admi
- P1·ESTADO 5.1: Resultados socialmente relevantes; legitimidade, confiança e direitos; controle interno, externo e social em perspectiva institucional; tensões entre eficiência
- P1·ESTADO 6.2: Distinções entre corrupção, falha de gestão, conflito de interesses e ilícitos específicos; relações e diferenças entre clientelismo, patronagem, nepotismo e ca
- P1·ESTADO 7.1: Assimetrias de poder e informação, incentivos e oportunidades; relações principal-agente e problemas de ação coletiva; normas sociais, tolerância organizacional
- P1·ESTADO 9.1: Arranjos de desenvolvimento com diferentes combinações de mercado, planejamento, regulação, provisão pública e atuação empresarial do Estado; industrialização, 
- P1·ESTADO 9.2: Papel das empresas estatais no investimento de longo prazo, na infraestrutura, no financiamento e na prestação de serviços públicos.
- P1·ESTADO 9.4: Fundamentos constitucionais da atuação econômica do Estado e comparação de alternativas institucionais à luz de objetivos, evidências e resultados.
- P1·ETICA 2.2: Aplicação dos valores e deveres de conduta ética da CGU a situações de trabalho.
- P1·ETICA 3.1: Identificação de interesses privados em conflito com a função pública e medidas de prevenção, consulta e encaminhamento, nos termos dos arts. 3º a 5º, 8º e 10 d
- P1·ETICA 4.2: Distinção entre acolher uma pessoa, verificar fatos e atribuir responsabilidade.
- P1·ETICA 5.1: Coerência entre regras e práticas; ambiente organizacional e incentivos; canais de orientação e relato; papel do exemplo, da confiança e da prestação de contas.
- P1·SOC 1.1: Instituições, socialização e ação coletiva; estratificação e mobilidade social; redes, poder, discriminação e reprodução das desigualdades.
- P1·SOC 2.1: Heranças da escravidão, hierarquias sociais e construção da cidadania; transformações nas relações entre Estado e sociedade; mecanismos de inclusão e exclusão i
- P1·SOC 4.1: Relações étnico- raciais, gênero e sexualidade; pessoas com deficiência; idade; povos indígenas e comunidades tradicionais. Interseccionalidade, acessibilidade 
- P1·SOC 5.1: Pobreza, renda e proteção social; educação, saúde, saneamento e habitação como problemas públicos; sustentabilidade e vulnerabilidade climática; leitura context
- P2·AUD 1: Propósito, serviços e papéis.
- P2·AUD 1.2: Avaliação e consultoria como serviços de auditoria interna governamental; apuração de atos e fatos com indícios de ilegalidade ou irregularidade na utilização d
- P2·AUD 1.3: Finalidades e diferenças entre as três formas de atuação da SFC; relação com a gestão, correição e avaliação de políticas.
- P2·AUD 1.4: Independência, objetividade, diligência e ceticismo; papéis de gestão, supervisão e auditoria no modelo das três linhas.
- P2·AUD 2.1: Planejamento, execução, comunicação e monitoramento; finalidade de objetivos, escopo, critérios e perguntas.
- P2·AUD 2.2: Priorização por risco, materialidade e relevância social em nível conceitual; adequação do trabalho às finalidades de avaliação, consultoria ou apuração.
- P2·AUD 2.3: Apoio à melhoria da gestão com preservação da autonomia técnica e das responsabilidades de decisão e execução dos gestores.
- P2·AUD 3.2: Distinção entre sinal de risco, evidência e conclusão; necessidade de aprofundamento e proporcionalidade da afirmação.
- P2·AUD 4.2: Recomendações relacionadas a causas e riscos; distinção entre plano de ação, implementação, resultado e benefício.
- P2·DIR 1.1: Competência, finalidade, motivação, proporcionalidade e segurança jurídica; consideração das consequências e das condições de atuação.
- P2·DIR 2.2: Distinção entre procedimento investigativo e processo sancionador; proteção de direitos e necessidade de fundamentar conclusões.
- P2·DIR 3.2: Avaliação da ação governamental e apoio ao aprimoramento da gestão, da governança, dos controles e dos resultados das políticas públicas; prevenção, detecção e 
- P2·DIR 3.3: Autonomia técnica e responsabilidades dos gestores; diferenças de competências e complementaridade com o controle externo exercido pelo Congresso Nacional com o
- P2·DIR 3.4: Distinção entre avaliar a gestão, apurar fatos e aplicar sanções; cooperação e compartilhamento lícito de informações.
- P2·DIR 4.2: Finalidades e diferenças entre responsabilização de agentes públicos e de pessoas jurídicas; noções de admissibilidade, processo disciplinar, processo administr
- P2·DIR 5.1: Distinção entre acolhimento, medidas de proteção, apuração de fatos e conclusão sancionadora, especialmente diante de assédio e discriminação; finalidades e gar
- P2·EVID 1.1: Relação entre problema, pergunta e informação necessária; fontes documentais, administrativas, estatísticas e de participação social.
- P2·EVID 2.1: Interpretação de tabelas, gráficos, proporções, taxas e medidas descritivas; denominadores, qualidade e comparabilidade.
- P2·EVID 2.2: Distinção entre indicadores de percepção, experiência, denúncias, detecção e sanções na análise da corrupção; subnotificação e limites de inferência sobre sua o
- P2·EVID 3.1: Associação e causalidade; seleção e representatividade; explicações alternativas e incerteza.
- P2·GOV 2.2: Identificação de vulnerabilidades e de controles compatíveis com situações usuais, a partir dos dados fornecidos.
- P2·GOV 4.1: Finalidades dos programas de integridade e sua relação com o poder público; compromisso da direção, registros confiáveis, controles, diligência proporcional sob
- P2·GOV 5.3: Distinção entre baixa ocorrência e baixa detecção de problemas; leitura de evidências simples sobre funcionamento e resultados das medidas.
- P2·TRANSP 1.1: Transparência ativa e passiva; finalidade de pedidos e recursos; publicidade como regra e motivação das restrições.
- P2·TRANSP 1.2: Distinção conceitual entre informação classificada, sigilos previstos em lei, informação pessoal e documento preparatório; acesso parcial e comunicação clara da
- P2·TRANSP 2.1: Compatibilização entre acesso à informação e proteção de dados pessoais; finalidade, necessidade e salvaguardas.
- P2·TRANSP 3.3: Distinção entre receber um relato, apurar fatos e decidir sobre responsabilidade.
- P2·TRANSP 4.2: Recorrências em manifestações como sinais de problemas.
- P2·TRANSP 4.3: Transparência ativa, dados abertos e Portal da Transparência como meios de acesso e controle; qualidade, atualização, cobertura e limites da informação.
- P2·TRANSP 5.2: Desinformação e efeitos sobre políticas públicas; comunicação de incertezas e correção de erros.
- P2·TRANSP 5.3: Liberdade de expressão e pluralismo.
- P3·ARQ 1: Arquiteturas de aplicações.
- P3·ARQ 1.3: Desempenho, escalabilidade, segurança e custo.
- P3·ARQ 1.4: Escolha de arquitetura conforme restrições.
- P3·ARQ 1.5: Aplicações Java com Spring Framework e Spring Boot: organização de componentes, inversão de controle e injeção de dependências.
- P3·ARQ 1.7: Construção de serviços REST e separação entre apresentação, regras de negócio e acesso a dados.
- P3·ARQ 2.6: Spring Security: configuração e avaliação de mecanismos de autenticação e autorização.
- P3·ARQ 3.3: Integração entre sistemas e coordenação de operações.
- P3·ARQ 4.1: Consumo e disponibilização de serviços de dados e modelos de linguagem.
- P3·ARQ 4.2: Representações vetoriais, busca semântica e recuperação de informação para geração de respostas.
- P3·ARQ 4.4: Avaliação funcional de respostas e fontes.
- P3·ARQ 4.5: Limites de autorização, supervisão e proteção contra instruções maliciosas em conteúdo externo.
- P3·ARQ 5: Confiabilidade das aplicações.
- P3·ARQ 5.1: Contêineres, serviços de nuvem e processamento serverless como ambientes de implantação.
- P3·ARQ 5.3: Latência, disponibilidade, capacidade e tolerância a falhas.
- P3·ARQ 5.4: Diagnóstico de integrações e dependências.
- P3·ARQ 5.5: Continuidade, recuperação e degradação de serviços.
- P3·DADOS 1: Modelagem e persistência.
- P3·DADOS 1.1: Modelagem relacional, normalização e integridade.
- P3·DADOS 1.2: Bancos documentais, chave-valor e vetoriais.
- P3·DADOS 1.4: Escolha de armazenamento conforme uso.
- P3·DADOS 1.5: Transações, concorrência, consistência e evolução de esquemas.
- P3·DADOS 1.6: Persistência em Java com JPA: mapeamento de entidades e relacionamentos, ciclo de vida das entidades, contexto de persistência, consultas e transações.
- P3·DADOS 1.7: Estratégias de carregamento e seus efeitos sobre correção e desempenho.
- P3·DADOS 1.8: Spring Data JPA: repositórios, consultas e paginação.
- P3·DADOS 1.9: Integração da camada de persistência às regras de negócio.
- P3·DADOS 2: SQL e desempenho.
- P3·DADOS 2.1: Definição e manipulação de dados, controle de acesso e transações.
- P3·DADOS 2.2: Consultas com filtros, junções, agregações, subconsultas e expressões de tabela comuns.
- P3·DADOS 2.3: Índices, planos de execução, valores nulos e duplicações.
- P3·DADOS 2.4: Diagnóstico de consultas e efeitos sobre o desempenho da aplicação.
- P3·DADOS 3.1: Ingestão, transformação e carga.
- P3·DADOS 3.5: Qualidade, rastreabilidade, conciliação e repetição segura de processamento.
- P3·DADOS 3.6: Spring Batch: organização de trabalhos e etapas de processamento (jobs e steps).
- P3·DADOS 3.7: Leitura, processamento e escrita de registros.
- P3·DADOS 3.8: Controle transacional, registro do estado de execução e reinício após falhas.
- P3·DADOS 3.9: Prevenção de perdas e duplicações no reprocessamento.
- P3·DADOS 4.4: Retenção, descarte e proteção de cópias e registros.
- P3·DADOS 4.5: Compartilhamento e publicação com salvaguardas.
- P3·DADOS 4.6: Proteção de dados pessoais desde a concepção da aplicação.
- P3·ENG 1.5: Relações entre problema público, processo de trabalho e solução digital.
- P3·ENG 2.1: Linguagem Java: tipos de dados, estruturas de controle, métodos, classes e objetos.
- P3·ENG 2.3: Coleções e tipos genéricos.
- P3·ENG 2.4: Igualdade de objetos, mutabilidade, tratamento de exceções e leitura e escrita de arquivos.
- P3·ENG 2.5: Estruturas de dados, algoritmos e pseudocódigo.
- P3·ENG 2.7: Complexidade em decisões de desempenho.
- P3·ENG 2.8: Modularidade e padrões de projeto aplicados à manutenção.
- P3·ENG 3.2: Condições de corrida e sincronização.
- P3·SEG 1.1: Ameaças e vulnerabilidades em aplicações e interfaces.
- P3·SEG 1.2: Validação de entradas e controles de acesso.
- P3·SEG 2.5: Verificação de requisitos funcionais, segurança, desempenho e acessibilidade.
- P3·SEG 3.3: Automação de build, teste e implantação.
- P3·SEG 4.3: Priorização, critérios de aceitação e indicadores de resultado.
- P3·SEG 5.1: Necessidade, estudo técnico preliminar e termo de referência.
- P3·SEG 5.3: Viabilidade, dimensionamento, custo total de propriedade e pesquisa de preços.
- P3·SEG 5.4: Qualidade, níveis de serviço e entregas verificáveis.
- P3·SEG 5.5: Fiscalização e pagamento.
- P3·SEG 5.6: Propriedade intelectual, portabilidade, acesso a código e dados, dependência tecnológica e plano de saída. FLÁVIO MARQUES PROL Secretário Executivo Adjunto

## NÚCLEOS JÁ EXISTENTES (reutilize o id se for a mesma ideia)
- n-ldo-orienta-loa-metas-fiscais: A LDO orienta a elaboração da LOA e traz as metas fiscais (LRF art. 4º)
- n-ppa-programa-acoes: No PPA, programa é o conjunto de ações (orçamentárias e não orçamentárias) coordenadas; é o elo PPA–LOA
- n-encadeamento-ppa-ldo-loa: PPA, LDO e LOA são encadeadas: a LDO traduz o PPA em metas anuais e a LOA obedece a ambas
- n-ldo-limites-poderes: A LDO fixa os limites das propostas orçamentárias do Judiciário; o Executivo ajusta
- n-planos-setoriais-ppa: Planos e programas setoriais se compatibilizam com o PPA, não o contrário
- n-loa-exclusividade: A LOA não conterá dispositivo estranho à previsão da receita e fixação da despesa
- n-orcamento-autorizativo: Orçamento é autorizativo; despesas obrigatórias não podem ser contingenciadas livremente
- n-emendas-loa: Emendas à LOA exigem compatibilidade com PPA/LDO e fonte por anulação, com exclusões previstas
- n-tres-camadas-regras-negocio: Em arquitetura de três camadas a lógica de negócio fica na camada intermediária, mas validações também podem o
- n-escalabilidade-horizontal: Escalabilidade horizontal adiciona servidores para ganhar capacidade, resiliência e desempenho
- n-owasp-quebra-controle-acesso: Quebra de controle de acesso é falha de restrições sobre o que usuários autenticados podem fazer; o ataque que
- n-injecao-ldap: LDAP injection manipula consultas LDAP inserindo código malicioso na entrada, que passa a ser interpretado de 
- n-xss-alvo-usuario-navegador: XSS injeta scripts em páginas web que são executados no navegador de outros usuários; não explora execução de 
- n-csrf-acao-indesejada-sessao: CSRF induz o navegador de um usuário autenticado a enviar requisição que executa ação indesejada na aplicação 
- n-ddos-mitigacao-especifica: Mitigação eficiente de DDoS exige soluções específicas (anti-DDoS, CDN, filtragem upstream); firewall de borda
- n-requisitos-seguranca-aplicacao: Requisitos de segurança de aplicações incluem identificação de dados sensíveis, restrição de acesso, autentica
- n-owasp-top10-vs-samm: O OWASP Top 10 descreve os riscos mais críticos em aplicações web; o OWASP SAMM é um modelo de maturidade de g
- n-sqli-entrada-sem-validacao: SQL injection explora formulários e entradas que não validam ou sanitizam dados, permitindo enviar comandos ma
- n-validacao-entrada-lista-permitida: Validar entradas aceitando apenas dados conhecidamente válidos (lista de permissão) previne injeções como SQL 
- n-xss-refletido: No XSS refletido a carga útil vai na requisição, é refletida na resposta HTTP e executada no navegador da víti
- n-dos-ddos-distribuido: DDoS usa múltiplas origens distribuídas para tornar o serviço indisponível; antivírus não é suficiente para pr
- n-ataques-injecao: SQL injection, LDAP injection e XSS são ataques de injeção de código.
- n-dns-cache-poisoning-ddos: Envenenamento de cache DNS pode redirecionar tráfego e ser usado em ataques associados a DDoS.
- n-ddos-afeta-disponibilidade: A principal consequência de um ataque DDoS é a perda de disponibilidade do serviço, não de integridade dos dad
- n-phishing-engenharia-social: Phishing é engenharia social que induz a vítima a fornecer dados e pode comprometer confidencialidade, integri
- n-ransomware-backup-continuidade: Política de backup e restauração e plano de gestão de crises são medidas preventivas e reativas eficazes contr
- n-xss-tipos-refletido-armazenado-dom: XSS tem variações (refletido, armazenado e baseado em DOM) e não se limita a formulários de cadastro
- n-ssrf-sem-credenciais-admin: SSRF induz o servidor vulnerável a fazer requisições a destinos escolhidos pelo atacante, sem exigir credencia
- n-validacao-requisitos-stakeholders: Requisitos devem ser validados com os stakeholders, não apenas tecnicamente pela equipe de desenvolvimento
- n-ataques-passivos-confidencialidade: Escuta e análise de tráfego são ataques passivos contra a confidencialidade; modificação e falsificação ameaça
- n-spear-phishing-direcionado: Spear phishing é direcionado a vítima ou grupo específico com mensagem personalizada; o phishing comum é em ma
- n-vulnerabilidade-independe-ameaca: Vulnerabilidade é fragilidade explorável que existe independentemente de ameaça ativa; o risco combina ameaça 
- n-wardriving-vs-ap-spoofing: Wardriving mapeia redes sem fio circulando por uma região; access point spoofing cria ponto de acesso falso pa
- n-mitre-attack-aplicacoes: MITRE ATT&CK é base de táticas e técnicas de adversários usada em entendimento de ameaças, caça a ameaças, res
- n-xss-xxe-sao-vulnerabilidades: XSS e XXE são vulnerabilidades/ataques, não controles; boas práticas incluem validação, codificação de saída e
- n-funcoes-estado-musgrave: O setor público exerce funções alocativa (bens públicos e meritórios), distributiva e estabilizadora; a alocaç
- n-arcabouco-fiscal: O regime fiscal sustentável (LC 200/2023) limita o crescimento das despesas primárias da União, sem a vigência
- n-receita-conceitos: Receita orçamentária é a prevista na LOA; a receita se classifica (originária/derivada, corrente/capital) e a 
- n-receita-estagios-regime: A receita orçamentária é reconhecida pelo regime de caixa (arrecadação); seus estágios de execução são lançame
- n-lrf-impacto-despesa: Criar ou aumentar despesa exige estimativa de impacto no exercício e nos dois seguintes (LRF art. 16); despesa
- n-despesa-conceitos: Toda despesa orçamentária depende de autorização legislativa (dotação na LOA ou crédito adicional) e segue emp
- n-loa-tres-orcamentos: A LOA compreende o orçamento fiscal, o da seguridade social e o de investimento das estatais em que a União de
- n-classificacao-funcional: A classificação funcional (função e subfunção) agrega as áreas de atuação do setor público; a subfunção pode c
- n-creditos-adicionais: Suplementar reforça dotação existente; especial atende despesa sem dotação específica; extraordinário só para 
- n-orcamento-base-zero: No orçamento base-zero toda despesa é reavaliada e justificada a cada ciclo, sem direito adquirido ao gasto do
- n-orcamento-tradicional: O orçamento tradicional é lei que estima receita e fixa despesa, como autorização política sem foco em resulta
- n-sistema-planejamento-orcamento: No sistema federal de planejamento e orçamento, o órgão central orienta e supervisiona tecnicamente os órgãos 
- n-principios-orcamentarios: Princípios orçamentários: unidade (harmonia entre PPA, LDO e LOA), universalidade (todas as receitas e despesa
- n-divida-publica-fundada: Operação de crédito com prazo inferior a 12 meses cuja receita tenha constado do orçamento integra a dívida co