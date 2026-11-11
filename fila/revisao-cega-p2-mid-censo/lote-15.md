# Revisao cega P2 — lote 15

Classifique cada item sem consultar a previsao original. Use um codigo abaixo ou OUTRO.

## Taxonomia

- `P2·GOV 1` — Governança e responsabilidades.
- `P2·GOV 2` — Riscos e controles essenciais.
- `P2·GOV 3` — Integridade pública.
- `P2·GOV 4` — Integridade privada.
- `P2·GOV 5` — Prevenção e melhoria institucional.
- `P2·TRANSP 1` — Acesso à informação.
- `P2·TRANSP 2` — Transparência e proteção de dados.
- `P2·TRANSP 3` — Ouvidoria e proteção das pessoas.
- `P2·TRANSP 4` — Participação e melhoria de serviços.
- `P2·TRANSP 5` — Integridade da informação e comunicação.
- `P2·DIR 1` — Decisão administrativa.
- `P2·DIR 2` — Processo e garantias.
- `P2·DIR 3` — Funções de controle e melhoria da gestão.
- `P2·DIR 4` — Responsabilização em nível introdutório.
- `P2·DIR 5` — Proteção e encaminhamento.
- `P2·EVID 1` — Perguntas e fontes.
- `P2·EVID 2` — Leitura de dados e indicadores.
- `P2·EVID 3` — Inferências e erros de raciocínio.
- `P2·EVID 4` — Integridade da evidência e proteção.
- `P2·EVID 5` — Uso responsável de inteligência artificial.
- `P2·AUD 1` — Propósito, serviços e papéis.
- `P2·AUD 2` — Ciclo do trabalho.
- `P2·AUD 3` — Evidência e conclusão.
- `P2·AUD 4` — Comunicação e acompanhamento.
- `P2·AUD 5` — Integração entre funções da CGU.

## Itens

### cpnuje-2024-c21-apoio-especializado-especialidade-pr#90

Com base nas informações precedentes, julgue os itens que se seguem, a respeito das regras de modelagem e normalização de dados. Para que esteja na terceira forma normal (3FN), a relação apresentada deve ser decomposta e deve possuir, no fim do processo de normalização, um total de quatro relações. Em determinada faculdade, para controlar os dados das monitorias prestadas por alunos a seus colegas, foram criadas as tabelas Aluno, Disciplina e Monitoria por meio dos scripts SQL a seguir. CREATE TABLE Aluno ( matricula integer, nome varchar(50), cpf integer, PRIMARY KEY(matricula) ); CREATE TABLE Disciplina ( cod_disciplina integer, nome_disciplina varchar(50), PRIMARY KEY(cod_disciplina) ); CREATE TABLE Monitoria ( cod_monitoria integer, dia_da_semana char(20), numero_de_horas integer, matricula_aluno_atendido integer, matricula_aluno_monitor integer, cod_disciplina_apoiada integer, PRIMARY KEY(cod_monitoria), FOREIGN KEY (matricula_aluno_atendido) REFERENCES Aluno (matricula), FOREIGN KEY (matricula_aluno_monitor) REFERENCES Aluno (matricula), FOREIGN KEY (cod_disciplina_apoiada) REFERENCES Disciplina (cod_disciplina) ); A partir dessas informações, julgue os próximos itens.

Rótulo: `PREENCHER`

### cti-2023-c01-tecnologias-habilitadoras-area-atuac#112

Com base nas informações precedentes, julgue os próximos itens. A condutividade elétrica do dispositivo eletrônico em questão é maior que a condutividade elétrica de um dispositivo com as mesmas características estruturais, fabricado com silício (Si).

Rótulo: `PREENCHER`

### cti-2023-c02-saude-avancada-area-atuacao#53

-- CONHECIMENTO Julgue os itens seguintes, a respeito da padronização de arquivos de modelos 3D. O formato de arquivo STL (standard tesselation language) para armazenamento de dados 3D, assim como os demais tipos de formatos para o mesmo fim, possui um cabeçalho na sua versão em binário, com o total de 128 caracteres.

Rótulo: `PREENCHER`

### cti-2023-c04-tecnologias-habilitadoras-area-atuac#55

-- CONHECIMENTO Em relação aos fundamentos da nanotecnologia, julgue os itens a seguir. Um dos grandes riscos dos nanomateriais é a alta capacidade de serem absorvidos pelos seres vivos, podendo chegar à corrente sanguínea e a praticamente qualquer órgão do corpo ao serem absorvidos por contato direto com a pele, por inalação ou por ingestão.

Rótulo: `PREENCHER`

### cti-2023-c05-tecnologias-habilitadoras-area-atuac#55

-- CONHECIMENTO Com relação a ciência de dados e inteligência artificial, julgue os próximos itens. O algoritmo de classificação KNN (K Nearest Neighbors) é utilizado na inteligência artificial para reconhecimento de padrões.

Rótulo: `PREENCHER`

### cti-2023-c05-tecnologias-habilitadoras-area-atuac#56

-- CONHECIMENTO Com relação a ciência de dados e inteligência artificial, julgue os próximos itens. Na ciência de dados, as cadeias de Markov podem ser aplicadas a ferramentas de previsão do clima e de espalhamento de doenças, por exemplo.

Rótulo: `PREENCHER`

### cti-2023-c05-tecnologias-habilitadoras-area-atuac#77

Com base em obtenção, limpeza e pré-processamento de dados, julgue os próximos itens. O pré-processamento de dados deve ocorrer em bases de informações não estruturadas, com o objetivo de diminuir a quantidade de dados a serem processados.

Rótulo: `PREENCHER`

### cti-2023-c05-tecnologias-habilitadoras-area-atuac#79

Com base em obtenção, limpeza e pré-processamento de dados, julgue os próximos itens. A normalização de um conjunto de dados tem como objetivo representar todos os valores desse conjunto em uma escala de 0 a 1.

Rótulo: `PREENCHER`

### cti-2023-c05-tecnologias-habilitadoras-area-atuac#103

Julgue os itens a seguir que tratam de extração e representação de conhecimento. Se um algoritmo induzir hipóteses que apresentam baixa taxa de acerto mesmo no conjunto de treino, então as hipóteses estão superajustadas aos dados.

Rótulo: `PREENCHER`

### cti-2023-c06-tecnologias-habilitadoras-area-atuac#111

No que se refere à análise e à mineração de dados, julgue os próximos itens. A mineração de dados pode ser entendida como um subconjunto da análise de dados, pois é usada para descobrir padrões ocultos em conjuntos de dados brutos, enquanto o enfoque da análise de dados se encontra no exame dos conjuntos de dados para a obtenção de conclusões precisas.

Rótulo: `PREENCHER`

### cti-2023-c06-tecnologias-habilitadoras-area-atuac#114

No que se refere à análise e à mineração de dados, julgue os próximos itens. A tarefa de agrupamento de dados consiste na análise de conjuntos de dados em que estão presentes apenas as descrições dos dados e pode até mesmo resolver problemas de detecção de desvios.

Rótulo: `PREENCHER`

### cti-2023-c06-tecnologias-habilitadoras-area-atuac#119

No que se refere à análise exploratória de dados e ao pré-processamento de dados, julgue os próximos itens. A análise multivariada com gráficos, um dos tipos primários de análise exploratória de dados, faz uso de imagens para exibir a relação entre duas ou mais variáveis.

Rótulo: `PREENCHER`

### cti-2023-c07-saude-avancada-area-atuacao#54

-- CONHECIMENTO Acerca dos conceitos relacionados a laboratórios abertos multiusuários (LAMU), julgue os itens a seguir. Os LAMU são proibidos por lei de auferir receitas próprias.

Rótulo: `PREENCHER`

### cti-2023-c08-saude-avancada-area-atuacao#108

No que se refere a automação e controle de processos, julgue os itens a seguir. Em uma edificação, os atuadores, utilizados em automação e controle de processos, são dispositivos geralmente usados para controlar a iluminação de ambientes, por meio da detecção automática de radiação infravermelha emitida pelo corpo humano.

Rótulo: `PREENCHER`

### cti-2023-c09-tecnologias-habilitadoras-area-atuac#78

Julgue os próximos itens, a respeito da gestão de segurança da informação. Para a identificação de ameaças à segurança da informação, recomenda-se a realização de avaliações de risco regularmente.

Rótulo: `PREENCHER`

### cti-2023-c09-tecnologias-habilitadoras-area-atuac#80

Julgue os próximos itens, a respeito da gestão de segurança da informação. As organizações devem, obrigatoriamente, implementar recursos criptográficos para proteger dados pessoais em todos os sistemas.

Rótulo: `PREENCHER`

### dataprev-2023-c02-advocacia#51

89300201590493 No que diz respeito às normas programáticas, aos direitos políticos e ao mandado de segurança, julgue os itens que se seguem. Em casos de manifesta ilegalidade da ação estatal, o mandado de segurança pode tutelar direitos protegidos pela ação de habeas corpus. Em relação ao tratamento constitucional da União e do Poder Legislativo, julgue os itens a seguir. Por ser a Câmara dos Deputados casa legislativa de representação popular, existe proporcionalidade rígida e precisa na relação entre o voto dos eleitores em cada estado e o número de deputados que esses votos elegem.

Rótulo: `PREENCHER`

### dataprev-2023-c02-advocacia#52

89300201590493 No que diz respeito às normas programáticas, aos direitos políticos e ao mandado de segurança, julgue os itens que se seguem. Em casos de manifesta ilegalidade da ação estatal, o mandado de segurança pode tutelar direitos protegidos pela ação de habeas corpus. Normas constitucionais programáticas são normas jurídicas, não exortações retóricas, e possuem eficácia, ainda que de modo diferente de outras normas constitucionais.

Rótulo: `PREENCHER`

### dataprev-2023-c02-advocacia#53

89300201590493 No que diz respeito às normas programáticas, aos direitos políticos e ao mandado de segurança, julgue os itens que se seguem. Em casos de manifesta ilegalidade da ação estatal, o mandado de segurança pode tutelar direitos protegidos pela ação de habeas corpus. Os direitos políticos, que incidem na formação das maiorias parlamentares, mantêm alguma tensão com os direitos fundamentais, porquanto estes limitam o funcionamento parlamentar.

Rótulo: `PREENCHER`

### dataprev-2023-c02-advocacia#54

89300201590493 No que diz respeito às normas programáticas, aos direitos políticos e ao mandado de segurança, julgue os itens que se seguem. Em casos de manifesta ilegalidade da ação estatal, o mandado de segurança pode tutelar direitos protegidos pela ação de habeas corpus. Julgue os itens seguintes, relativos ao regime de precatórios e ao Ministério Público. De acordo com a interpretação prevalecente acerca das funções do Ministério Público na área penal, esse órgão tanto pode reunir elementos de prova por meio de inquérito policial quanto realizar investigações criminais diretamente.

Rótulo: `PREENCHER`
