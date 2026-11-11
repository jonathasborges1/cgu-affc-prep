# Banco de questões reais com gabarito definitivo oficial (Cebraspe), compatíveis com o edital CGU/AFFC 2026

Coletado em 02/11/2026 direto dos PDFs oficiais (texto extraído pelo Chrome com pdf.js; gabarito definitivo conferido). Itens marcados X foram anulados e ficam de fora. Cada questão tem uma única referência: o PDF da prova com o número do item.

## Fonte A: TCE-RN 2026, Analista Administrativo, TI (Desenvolvimento de Sistemas e Inteligência da Informação), Cargo 4, aplicada em 12/04/2026, Cebraspe
Prova: https://cdn.cebraspe.org.br/concursos/tce_rn_25/arquivos/D794D51B24F49D57884C4BACA10D545C9D56B8CBBB3ACBE82A0CA2B6B3DBE3E3.pdf
Gabarito definitivo: https://cdn.cebraspe.org.br/concursos/tce_rn_25/arquivos/41BEDC41DCBCC480B9306E929A88A2C23E6C4B7FD0D83DE19C629A7158A242A9.pdf
Página oficial: https://www.cebraspe.org.br/concursos/tce_rn_25

### Persistência e dados (edital Persistência 1 a 3)
- 51 [E] Bancos de dados NoSQL são projetados para garantir, por padrão, consistência forte (strong consistency), priorizando a integridade imediata dos dados em ambientes distribuídos.
- 54 [C] Em sistemas NoSQL orientados a documentos, como MongoDB, os dados são armazenados em estruturas flexíveis que permitem variação de esquema entre registros de uma mesma coleção.
- 55 [E] A ingestão de dados em streaming não é adequada para cenários que exigem alta confiabilidade, pois não permite mecanismos de tolerância a falhas ou reprocessamento de eventos.
- 56 [C] Sistemas de armazenamento distribuído, como data lakes, permitem o armazenamento de dados em seu formato bruto, favorecendo abordagens ELT em detrimento de ETL.
- 57 [C] A instrução UPDATE pode ser utilizada em conjunto com subconsultas correlacionadas para modificar dados com base em valores provenientes de outras tabelas, respeitando as restrições de integridade definidas no banco de dados.
- 58 [E] A utilização de índices compostos garante melhoria uniforme de desempenho para qualquer consulta que envolva pelo menos uma das colunas indexadas, independentemente da ordem dos atributos no índice.
- 59 [E] O particionamento de tabelas elimina a necessidade de índices secundários, pois a divisão física dos dados já garante acesso eficiente em qualquer tipo de consulta.
- 60 [E] Em ambientes de alta concorrência, a definição de restrições de chave estrangeira garante que operações de inserção e de atualização ocorram com menor custo computacional, pois o SGBD utiliza essas restrições para simplificar as verificações de consistência.
- 61 [C] A integridade referencial garante que valores de chave estrangeira em uma tabela correspondam a valores válidos de chave primária em outra tabela, evitando a existência de registros órfãos.
- 62 [C] A execução de comandos DML, como UPDATE e DELETE, sem cláusula WHERE pode resultar em operações em massa que afetam toda a tabela, podendo comprometer a integridade lógica dos dados.
- 113 [C] Consoante disposto na norma ABNT NBR ISO/IEC 27002:2022, anonimização consiste na alteração irreversível de dados pessoais de forma tal que o titular dos dados não pode mais ser identificado direta ou indiretamente; consoante o disposto na LGPD, anonimização consiste na utilização de meios técnicos por meio dos quais um dado perde a possibilidade de associação, direta ou indireta, a um indivíduo.

### Engenharia de software, arquitetura e entrega
- 63 [C] No catálogo GoF, o padrão de criação Singleton garante que haja somente uma instância para cada classe, com um único ponto de acesso a ela.
- 100 [E] No padrão de projeto abstract factory, a inclusão de uma nova categoria de objeto em uma família de produtos já existente prescinde da alteração da interface da fábrica abstrata e de suas subclasses concretas.
- 97 [C] Diferentemente das arquiteturas tradicionais de N camadas, a arquitetura de microsserviços se baseia na descentralização da gestão de dados, em que cada serviço deve, idealmente, possuir sua própria base de dados, de forma a garantir a independência de implantação e o baixo acoplamento.
- 98 [E] A adoção de uma estratégia de camadas fechadas (closed layers) permite que a camada de apresentação acesse diretamente os serviços da camada de dados quando houver necessidade de otimização de performance, desde que a camada de negócio permaneça inalterada.
- 99 [C] No padrão arquitetural MVC (model-view-controller), o componente controller atua como um intermediário que interpreta as entradas enviadas pelo usuário e coordena as atualizações necessárias no model, de forma a permitir que a lógica de negócio e o estado dos dados permaneçam independentes da interface de apresentação.
- 101 [C] No que se refere ao desenvolvimento de soluções mobile baseadas em padrões W3C, a arquitetura de uma PWA (progressive web app) utiliza service workers para atuar como um proxy de rede programável de forma a permitir que o usuário mobile acesse funcionalidades críticas da aplicação mesmo em cenários de latência elevada ou ausência de conectividade.
- 102 [E] O framework gRPC adota o formato JSON como padrão nativo de serialização de dados, o que assegura a interoperabilidade direta com navegadores web.
- 103 [C] Nas arquiteturas cloud native, o isolamento provido pelo uso de containers permite que falhas em serviços individuais sejam mitigadas pela substituição automática das instâncias comprometidas.
- 67 [E] Um dos objetivos do método Kanban é colocar a maior quantidade possível de itens em andamento, aumentando a capacidade de entrega do time de desenvolvimento.
- 68 [C] A metodologia Scrum determina que a duração de uma sprint é inalterável, mesmo que todos os itens previstos ainda não estejam finalizados.
- 69 [C] De acordo com o conceito INVEST, as histórias de usuário devem ser independentes, negociáveis, pequenas e testáveis.
- 72 [E] Throughput e Velocity são duas métricas de software que identificam a quantidade absoluta de itens entregues em determinado período de tempo.
- 73 [C] O processo de deployment blue/green utiliza dois ambientes de produção com as mesmas configurações, o que permite um método de implantação de baixo risco.
- 74 [C] Sob o mesmo namespace, diversos contêineres Docker podem ser executados e interagir entre si, com compartilhamento local de dados.
- 110 [C] Considere que as fases que compõem o processo de elaboração de certo plano diretor de TIC (PDTIC) sejam preparação, diagnóstico e planejamento. Considere, ainda, que se pretenda realizar a análise dos ambientes interno e externo da TIC por meio do método SWOT. Nesse caso, a atividade pretendida deve ser executada na fase de diagnóstico e, para o ambiente interno, podem ser analisados a qualidade dos processos e serviços providos e o nível de satisfação dos usuários com os serviços prestados.

### Contratação de TI (edital Entrega 5)
- 114 [E] Ao final do contrato, os módulos implementados serão de propriedade da empresa contratada, que poderá repassar, mediante compensação financeira, os direitos de propriedade intelectual para o contratante.
- 115 [C] Na administração estadual, o gestor de contrato pode ser auxiliado, no cumprimento das atribuições do cargo, por recursos terceirizados.
- 116 [E] A menos que esteja expresso de forma diferente no edital, os testes e demais provas exigidos por normas técnicas são de responsabilidade do contratante, quando entidade pública.
- 117 [C] Estão entre os critérios de julgamento no modelo de licitação por concorrência: menor preço, melhor técnica, maior retorno econômico.
- 118 [E] Para fins de obtenção de preço estimado, a Instrução Normativa SEGES/ME n.º 65/2021 estipula como único método o cálculo da média a partir de um conjunto de três ou mais preços.
- 119 [C] Nos termos da Instrução Normativa SGD/ME n.º 94/2022, na renovação de centro de dados, deve-se priorizar a contratação de serviços em nuvem. (conferir se a norma ainda está em vigor antes de usar)

### IA, parcial (mais para P2 5.x do edital)
94 [C] MLOps (testes, monitoramento, re-treinamento); 95 [C] mitigação de viés; 96 [E] interpretabilidade de árvore de decisão x redes profundas (item completo no PDF).

## Fonte B: TCU 2026, Auditor Federal de Controle Externo, Auditoria de TI, aplicada em 22/02/2026, Cebraspe (itens 101 a 200)
Prova (específicos): https://cdn.cebraspe.org.br/concursos/TCU_25_AUFC/arquivos/9546624AF77A5D0A72692C2ACF3725FAF5033C9A8889BFC43D6665194D880172.pdf
Gabarito definitivo (específicos): https://cdn.cebraspe.org.br/concursos/TCU_25_AUFC/arquivos/D599023DB31F3467DB9CC03BE3D58BFE91CD7351624DDF045C0FDB71B3569A51.pdf
Página oficial: https://www.cebraspe.org.br/concursos/tcu_25_aufc
Numeração do caderno oficial (difere da do QConcursos). Itens anulados nesse bloco: 101, 103, 105, 106, 122, 126, 129, 130, 165, 190, 192, 193.

### Dados e integração
- 113 [C] Arquivos do tipo CSV podem ser utilizados para representar informações de tabelas, incluindo os rótulos de suas colunas.
- 114 [E] No serviço REST, para que o servidor responda adequadamente, ele precisa armazenar o estado da sessão do cliente entre suas requisições.
- 115 [E] Bancos de dados relacionais utilizam tabelas bidimensionais, e o MongoDB representa os dados em formato JSON ou XML.
- 116 [C] PolyBase é a ferramenta que permite ao Microsoft SQL Server consultar fontes externas como se os dados estivessem armazenados localmente.
- 117 [C] Como data warehouse é não volátil, a etapa intermediária do ETL deve efetuar todos os tratamentos necessários nos dados para melhorar a sua qualidade.
- 118 [C] A construção de um data mesh parte do princípio de propriedade de domínio, conforme o qual as equipes de cada domínio assumem a responsabilidade por seus dados.
- 119 [E] O pipeline de CI/CD consiste em duas etapas sequenciais: implantação rápida em produção e posterior integração com os demais serviços.
- 120 [E] Data warehouse e data lake armazenam dados em seu formato original, porém o data lake, diferentemente do data warehouse, acessa bases externas a uma organização.

### Arquitetura, APIs e identidade
- 127 [E] Em um Service Mesh, a implementação das CCC (cross cutting concerns) permanece a cargo de cada microsserviço, cabendo ao control plane redistribuí-las aos proxies.
- 128 [E] A decodificação de um JWT envolve transformar o header e o payload em um formato compacto e seguro para URLs, de maneira a permitir que qualquer pessoa leia essas partes sem precisar de uma chave.
- 138 [E] Em uma arquitetura corporativa que adota SSO via SAML 2.0, o authorization server do fluxo OAuth2 atua como identity provider responsável pela emissão das assertions SAML utilizadas no processo de autenticação entre o usuário e o service provider.
- 143 [C] Em um sistema corporativo, a exigência de senha e de código gerado por aplicativo autenticador atende aos requisitos de múltiplos fatores de autenticação, pois combina um fator de conhecimento e um fator de posse.
- 142 [E] A validação de segurança realizada no cliente é suficiente para eliminar os riscos de injeção em aplicações web baseadas em APIs REST, desde que o tráfego esteja protegido por TLS.
- 148 [C] Em ambientes de nuvem pública, a configuração de controles de acesso baseada em princípio de privilégio mínimo no nível dos serviços gerenciados contribui para reduzir superfícies de ataque.
- 153 [E] Na arquitetura Zero Trust, usuários conectados por VPN corporativa são tratados como confiáveis por padrão, uma vez que, nesse modelo, a confiança é eliminada independentemente da origem da conexão, incluído o perímetro da rede interna, exigindo-se autenticação contínua e validação de acesso a cada recurso.
- 154 [E] O modelo RBAC não é eficaz para a implementação do princípio do menor privilégio, pois suas funções tendem a conceder permissões amplas e não limitam o acesso somente ao necessário para tarefas específicas, o que compromete a segurança em ambientes de computação em nuvem.
- 159 [E] O AWS IAM (Identity and Access Management) restringe o controle de permissões a configurações gerais aplicadas de maneira uniforme a todos os usuários, sem oferecer mecanismos para detalhamento de acesso por recurso ou por entidade específica.

### Segurança, privacidade e dados
- 139 [E] A adoção de privacidade por padrão em um serviço digital legitima que as configurações iniciais favoreçam a coleta ampliada de dados, desde que os mecanismos de segurança por padrão estejam habilitados para proteger essas informações.
- 141 [C] Em arquiteturas corporativas, o uso combinado de um proxy e de um SIEM tem potencial para ampliar a capacidade de detecção de atividades anômalas (texto completo no PDF).
- 144 [E] O uso de um SIEM devidamente configurado para correlação em tempo real elimina a necessidade de mecanismos de prevenção de um IPS, já que os eventos consolidados permitem bloquear as atividades maliciosas diretamente a partir da análise centralizada.
- 149 [C] Em um sistema que utiliza assinatura digital para garantir integridade e autenticidade de documentos, é adequado que a proteção dos dados em trânsito seja apoiada por protocolos como o TLS, enquanto a proteção dos dados em repouso seja realizada por criptografia simétrica.
- 162 [C] O uso de computação em nuvem no governo federal deve obedecer à Lei Geral de Proteção de Dados Pessoais (LGPD), com garantia dos direitos fundamentais de titularidade, guarda de registros das operações de tratamento e adoção de responsabilidades compartilhadas entre órgãos e provedores.

### Entrega, DevSecOps e qualidade
- 132 [C] No DevSecOps, a execução de varreduras automatizadas de segurança é premissa fundamental do pipeline de desenvolvimento e deve ocorrer de forma integrada e contínua ao longo de todo o ciclo de entrega.
- 135 [C] A linguagem Java, ao implementar o conceito de nest, permite o acesso a membros private entre nestmates nativamente pela máquina virtual, dispensando o uso de métodos sintéticos.
- 155 [C] FinOps combina pessoas, processos e tecnologias para fornecer visibilidade de custos em nuvem (texto completo no PDF).
- 156 [C] CI/CD combina integração contínua com testes, entrega e implantação automatizados (texto completo no PDF).
- Itens 133, 134, 136 dependem de código ou configuração (GitHub Actions, Grafana, SonarQube): pegar o enunciado completo no PDF antes de usar.

### Nuvem e contêineres
- 151 [E] Docker e Kubernetes são software intercambiáveis em qualquer ambiente, pois ambos criam, executam e orquestram contêineres de forma idêntica.
- 152 [C] Em arquiteturas serverless, operam servidores físicos, porém a gestão da infraestrutura é abstraída dos desenvolvedores (texto completo no PDF).
- 157 [E] A alta disponibilidade em ambientes de nuvem é obtida suficientemente com o uso de múltiplas zonas de disponibilidade dentro de um mesmo data center, sem necessidade de replicação geográfica de dados ou de componentes de sistema.
- 158 [C] No armazenamento orientado a objetos, cada informação é organizada como uma unidade autônoma acompanhada de metadados, sendo tal abordagem indicada para grandes volumes de dados não estruturados, como imagens, vídeos, logs e backups.
- 160 [C] Arquiteturas multicloud caracterizam-se pelo uso simultâneo de serviços de nuvens públicas de diferentes provedores, o que permite maior flexibilidade operacional e reduz a dependência de um único fornecedor.
- 161 [E] A estratégia lift and shift envolve a reescrita completa das aplicações antes da migração, de modo a serem explorados integralmente os recursos nativos da nuvem, e prioriza a modernização antes da transferência do ambiente.
- 124 [E] Na arquitetura PaaS, o provedor é o responsável pelos recursos de sistema operacional e pelas aplicações. (texto completo no PDF)
- 125 [C] No fluxo padrão do Serverless Framework Dashboard CI/CD, as branch deployments permitem que cada commit em uma branch configurada do repositório GitHub seja implantado automaticamente em um stage associado.

### Contratação de TI
- 177 [E] O estudo técnico preliminar pode substituir o termo de referência na contratação de alguns tipos de serviços que envolvam soluções de TI.
- 178 [E] A etapa inicial do processo de contratação de soluções de TI na administração pública consiste na elaboração do termo de referência.
- 179 [C] Denomina-se fábrica de software um modelo de contratação com foco na produção contínua de sistemas e normalmente remunerado por ponto de função.
- 180 [C] No que se refere à contratação sob demanda de software, os direitos patrimoniais do código-fonte desenvolvido devem ser cedidos à administração pública.

### IA, encaixe parcial (P2 5.x e Arquitetura 4)
163 [C] explicabilidade; 164 [C] discriminação algorítmica; 166 [E] emergência em multiagentes; 167 [C] NER supervisionado; 168 [E] transformers e pré-processamento; 169 [C] multiagentes; 170 [E] Word2Vec; 171 [E] orquestração em MLOps; 172 [C] MLOps; 173 [C] versionamento e rollback de modelos; 174 [E] reforço não supervisionado; 175 [C] reforço x supervisionado; 176 [E] dispensar validação.

## Fonte C: TCE-AC 2024 (já usada no Caderno 1)
Ver `triagem-tce-ac-2024.md`.

## Como o Cebraspe publica (para repetir a coleta em outras provas)
- Página: https://www.cebraspe.org.br/concursos/<slug> (TCU: tcu_25_aufc; TRF6 2025: trf6_24; DATAPREV 2023: DATAPREV_23; TCE-RN: tce_rn_25; TCE-AC: tce_ac_24). Os links dos PDFs aparecem na página e apontam para cdn.cebraspe.org.br/concursos/<SLUG>/arquivos/<hash>.pdf.
- O Chrome não entrega o texto de PDF. Funciona abrir uma página 403 do mesmo domínio e extrair com pdf.js (jsdelivr) via fetch.

## Impacto no plano de cadernos
Os 4 grupos de questões reais com gabarito (TCE-AC 2024, TCE-RN 2026, TCU 2026, QConcursos parcial) já sustentam cadernos para: interfaces e acessibilidade; arquitetura e padrões; identidade e acesso; SQL e modelagem; dados e ETL/NoSQL; segurança e criptografia; entrega e DevSecOps; nuvem e contêineres; Scrum/Kanban e produto; contratação de TI; IA parcial. Faltam referências para Spring Security, Spring Data JPA, Spring Batch, RAG e vetores, idempotência.
