# Mapa de provas anteriores x edital CGU/AFFC 2026 (TI – Desenvolvimento de Sistemas), versão 2

Atualizado em 02/11/2026. Esta versão substitui a primeira e incorpora a verificação feita pelo Chrome (QConcursos aberto de verdade, enunciados lidos). Itens marcados como "lido" tiveram o enunciado e a banca conferidos na página. Itens "só pela busca" não foram abertos.

## Conclusão
- Não existe prova anterior da CGU feita pelo Cebraspe. A CGU 2022 (TI) foi da FGV, múltipla escolha. Serve para conteúdo, não para estilo.
- Melhor prova espelho de P3: TCU 2026, Auditor de Controle Externo, TI (Cebraspe, 22/02/2026). Mais perto do estilo atual, mas é auditoria de TI com pouca coisa de Java.
- Melhor fonte para Java, Spring e JPA: o banco de questões do QConcursos filtrado só por Cebraspe (ver "Como filtrar").
- Lacunas confirmadas: nenhuma questão Cebraspe sobre Spring Security, Spring Data JPA ou Spring Batch nas páginas conferidas.

## Como filtrar só Cebraspe no QConcursos
Acrescentar `?examining_board_ids%5B%5D=2` ao endereço de qualquer página de assunto. A busca por palavra-chave na URL (`q=`) é ignorada e não deve ser usada.
- Frameworks Java (176 questões Cebraspe): https://www.qconcursos.com/questoes-de-concursos/disciplinas/tecnologia-da-informacao-programacao/frameworks-java/questoes?examining_board_ids%5B%5D=2
- Frameworks em Engenharia de Software (23 questões Cebraspe): https://www.qconcursos.com/questoes-de-concursos/disciplinas/tecnologia-da-informacao-engenharia-de-software/frameworks/questoes?examining_board_ids%5B%5D=2
- Gerência de Transações (112 questões Cebraspe): https://www.qconcursos.com/questoes-de-concursos/questoes?discipline_ids%5B%5D=96&examining_board_ids%5B%5D=2&subject_ids%5B%5D=277

Atenção: nos resultados de busca na web, o texto da questão e a etiqueta da banca às vezes vêm trocados. Um exemplo real: uma questão de Spring Data JPA com `@Transactional` apareceu ligada à Prefeitura de Porto Velho 2026, mas essa questão (Q4228222) é sobre ACID/durabilidade. Só aceitar atribuição depois de abrir a questão.

## P3: questões Cebraspe lidas, com link direto
Prefixo dos links: https://www.qconcursos.com/questoes-de-concursos/questoes/

| Código | Prova | Tema | Hash do link |
|---|---|---|---|
| Q2274715 | DATAPREV 2023, Analista TI, Arquitetura e Engenharia Tecnológica | Spring Boot: `spring init` cria projeto | 7e51c037-67 |
| Q2274716 | idem | Spring Boot: pré-requisito é ter Java instalado | 7e54b670-67 |
| Q2274717 | idem | Spring Boot: GraalVM native images | 7e580b37-67 |
| Q2281773 | TBG 2023, Desenvolvimento de Software | Spring: `@RestController` | b66246e5-72 |
| Q2281776 | TBG 2023, Desenvolvimento de Software | Hibernate como camada entre aplicação e banco | b66eccaf-72 |
| Q2226513 | SERPRO 2023, Analista, Tecnologia | Hibernate 6.2 e bloqueio otimista x pessimista | 37ba1e3a-2e |
| Q3468198 | FUB 2025, Técnico TI | `EntityManager.persist()` e contexto de persistência | 1cf907b0-5a |
| Q2341104 | TC-DF 2023, Auditor, TI, Sistemas de TI | Hibernate gera SQL em tempo de compilação? | 6d67d684-b1 |
| Q3409353 | STM 2025, Analista, Suporte em TI | Hibernate Envers | 3bd3ed91-46 |
| Q3167218 | TRF6 2025, Analista, Governança e Gestão de TI | Hibernate Envers e Flyway | 88ca9df9-db |
| Q2378415 | INPI 2024, Analista, Gestão de TI e desenvolvimento de sistemas | Envers x identidade (SSO) | a0b29391-d4 |
| Q3104127 | STJ 2024, Analista, Análise de Sistemas | JUnit `@EnabledOnOs` | 1bafed69-b6 |
| Q2133223 | CNMP 2023, Analista, TIC, Desenvolvimento de Sistemas | JUnit e ordem de execução | 17a4a6ab-e6 |
| Q1814479 | PG-DF 2021, Analista de Sistema, Desenvolvimento | JUnit 5 e Spring Framework | 60f9cd67-16 |
| Q4248439 | SEPLAG-AL 2026, Análise de Sistemas | React: estado e `setItens` (front-end, não é Spring) | 9c2c4bf6-9c |

Lidas na lista, sem link direto coletado ainda (o código basta para achar na página filtrada):
- Q4234281, UNEAL 2026, Análise de Sistemas: autoconfiguração do Spring Boot (única questão Spring Boot de 2026 do Cebraspe que achei).
- Q3258087, TRT-10 2025, TI: Vue.js e Virtual DOM.
- Q3111784, TSE 2024, TI: Zuul e Spring Cloud (borda e roteamento de microsserviços).
- Q2532047, CNJ 2024, Programação de Sistemas: JPA 2.0 e ordenação.
- Q3167137, TRF6 2025, Analista, Análise de Sistemas: JPA 2.0 e `OptimisticLockException`.

Só pela busca (não abertas): OAuth 2 e JWT no BANRISUL 2022 (Q64); OpenID Connect no STM 2025 e TCE-AC 2024; Vue.js no BANRISUL 2022 e TCE-AC 2024 (PDF oficial, item 51, aberto antes); microsserviços e mensageria no BANRISUL 2025 (PDF oficial).

## P3: TCU 2026, Auditor de Controle Externo, TI (Cebraspe, 200 itens C/E)
Lista de questões (20 por página): https://www.qconcursos.com/questoes-de-concursos/provas/cespe-cebraspe-2026-tcu-auditor-federal-de-controle-externo-area-de-controle-externo-orientacao-auditoria-de-tecnologia-da-informacao/questoes?page=6 (trocar o número: 6 = itens 101-120, 7 = 121-140, 8 = 141-160, 9 = 161-180).
A numeração do QConcursos pode diferir da do caderno oficial. Use o código Q39065xx como referência. Os gabaritos não foram coletados.
Distribuição: Engenharia de Software 25, Direito Administrativo 21, Português 20, Segurança 17, Governança de TI 17, Sistemas Operacionais 14, Arquitetura de Software 7, Banco de Dados 5, Programação 3.

| Itens (códigos) | Tema | Onde cai no edital |
|---|---|---|
| 113, 114 (Q3906549, Q3906550) | CSV com rótulos de colunas; REST e estado de sessão no servidor | Persistência 3.4; Arquitetura 1.7 |
| 115 a 120 (Q3906551 a Q3906556) | Relacional x MongoDB, PolyBase, ETL e data warehouse, data mesh, data lake, CI/CD | Persistência 1.2, 3.1 a 3.3 |
| 127 (Q3906563) | Service mesh e preocupações transversais | Arquitetura 1.1 e 1.2 |
| 128, 129 (Q3906564, Q3906565) | JWT é só codificado, não cifrado; versionamento de API por data (anulada) | Arquitetura 2.1 e 2.4 |
| 130 a 134 (Q3906566 a Q3906570) | Docker multi-stage, DevSecOps, GitHub Actions, Grafana | Entrega 3.1 a 3.5 |
| 135, 136 (Q3906571, Q3906572) | Java: nestmates e acesso a membros `private`; SonarQube Quality Gate em pipeline | Engenharia 2; Entrega 2.2 |
| 138 (Q3906574) | SAML 2.0 x OAuth2: quem emite as assertions | Arquitetura 2.3 |
| 139 (Q3906575) | Privacidade por padrão x segurança por padrão | Persistência 4.6 |
| 141 a 144 (Q3906577 a Q3906580) | Proxy + SIEM; validação só no cliente não impede injeção em REST; MFA; SIEM não substitui IPS | Desenv. seguro 1.1, 1.2 e 1.6; Arquitetura 2.2 |
| 148, 149, 153, 154 (Q3906584, Q3906585, Q3906589, Q3906590) | Menor privilégio em nuvem, TLS e criptografia em repouso, Zero Trust, RBAC | Arquitetura 2.5 e 2.8; Persistência 4.2 |
| 151, 152, 155, 156 (Q3906587, Q3906588, Q3906591, Q3906592) | Docker x Kubernetes, serverless, FinOps, CI/CD | Arquitetura 5.1; Entrega 3.1 |
| 157 a 162 (Q3906593 a Q3906598) | Alta disponibilidade, objetos, IAM, multicloud, lift and shift, LGPD na nuvem do governo | Arquitetura 5.1, 5.3, 5.5; Persistência 4 |
| 163 a 176 (Q3906599 a Q3906612) | IA: explicabilidade, discriminação algorítmica, PLN, multiagentes, MLOps, aprendizado por reforço (o item 165 foi anulado) | Arquitetura 4; também P2 (IA) |
| 177 a 180 (Q3906613 a Q3906616) | Contratação de TI: ETP x termo de referência, fábrica de software, direitos patrimoniais do código (IN SGD/ME 94/2022) | Entrega 5.1, 5.2 e 5.6 |

## Outras provas Cebraspe de TI úteis (só pela busca, pouco examinadas)
- TCE-RN 2026, Analista TI (Desenvolvimento de Sistemas e Inteligência da Informação): provas e gabaritos em https://www.cebraspe.org.br/concursos/tce_rn_25. Lido: Q4014187, transações e chave estrangeira. Não confirmei questão de Spring Boot nessa prova.
- IPAAM 2026 (Manaus), Análise de Sistemas: gabarito em https://arquivos.qconcursos.com/prova/arquivo_gabarito/148788/cespe-cebraspe-2026-ipaam-analista-ambiental-especialidade-analise-de-sistemas-gabarito.pdf (a prova em si não foi lida).
- TCE-AC 2024, prova específica de TI (PDF oficial): https://cdn.cebraspe.org.br/concursos/tce_ac_24/arquivos/993_TCE_AC_011_01.PDF. Vue.js (item 51), WCAG, REST, JWT/OpenID Connect, segurança web (XSS, CSRF, OWASP).
- BANRISUL 2025, Técnico TI II, Desenvolvimento de Software (PDF oficial): https://arquivos.qconcursos.com/prova/arquivo_prova/133106/cespe-cebraspe-2025-banrisul-tecnico-em-tecnologia-da-informacao-ii-desenvolvimento-de-software-prova.pdf
- DATAPREV 2023, Analista TI, Desenvolvimento de Software: https://www.pciconcursos.com.br/provas/download/analista-de-tecnologia-da-informacao-perfil-desenvolvimento-de-software-dataprev-cebraspe-2023
- BDMG 2025, Sistemas, Arquitetura e Solução de Dados: https://www.qconcursos.com/questoes-de-concursos/provas/cespe-cebraspe-2025-bdmg-analista-de-desenvolvimento-sistemas-arquitetura-e-solucao-de-dados
- Transações e ACID, concorrência e 2PL (lidas, Cebraspe): BANRISUL 2025 (Q3433427 a Q3433434 e Q3433446), TRF6 2025 (Q3167137, Q3170218), SEFAZ-SE 2025 (Q3641767), CAESB-DF 2025 (Q3445203), todas em https://www.qconcursos.com/questoes-de-concursos/questoes?discipline_ids%5B%5D=96&examining_board_ids%5B%5D=2&subject_ids%5B%5D=277

Concorrência e threads em Java (só pela busca): FUNPRESP-JUD 2026 (Q4599207, condição de corrida e `synchronized`), MEC 2015 (Q578225, thread safe; Q594996, condição de corrida).

## Outras bancas (só conteúdo)
- CGU 2022 (FGV), AFFC TI: https://www.pciconcursos.com/provas/cgu
- Spring e Hibernate em outras bancas: UERJ 2026 (devtools, Q4041497), MPE-ES 2026 FGV (`@RestController`, Q4216300), TJ-RJ 2026 FGV (Envers, Q3874365), CPRM 2025 FGV (Spring Boot e JWT com Spring Security, Q3757614), UFLA 2025 (escopo de beans, Q3753502). Não são Cebraspe, então não entram em caderno.

## P1 e P2: base Cebraspe
Não há prova Cebraspe com este programa. Base por tema vizinho:
- Conflito de interesses (Lei 12.813/2013): ANM 2025, MMA 2024 (Analista Ambiental), DPF 2025, MTE 2013. https://www.qconcursos.com/questoes-de-concursos/disciplinas/direito-legislacao-federal/lei-12-813-de-2013-conflito-de-interesses-no-exercicio-de-cargo-ou-emprego-do-poder-executivo-federal-e-impedimentos-posteriores-ao-exercicio-do-cargo-ou-emprego/questoes
- Controle interno, três linhas, programa de integridade (PDFs oficiais do Cebraspe): SEPLAD-DF 2022 https://cdn.cebraspe.org.br/concursos/seplad_df_22_auditor/arquivos/105_SEPLAD22CF2TURMA_001_01.pdf · SEBRAE 2025 https://cdn.cebraspe.org.br/concursos/sebrae_25_pse_1/arquivos/053_SEBRAE_PSE_001_02.pdf · FUNPRESP 2021 https://cdn.cebraspe.org.br/concursos/funpresp_21/arquivos/648_FUNPRESP_EXE_003_01.PDF · AL-CE 2020 https://cdn.cebraspe.org.br/concursos/al_ce_20/arquivos/539_ALCE_007_01.PDF
- Controle da administração, controle externo, auditoria governamental: TCU 2026 (básicos) e TCE-RN 2026 (Direito Administrativo).
- Sem questão Cebraspe encontrada ainda: subnotificação e indicadores de corrupção, falácia ecológica, IA responsável na administração, ouvidoria e proteção do denunciante, três formas de atuação da SFC.

## Fontes oficiais
- Edital CGU AFFC 2026: https://cdn.cebraspe.org.br/concursos/cgu_26_affc/arquivos/C7A60D15CB0DDDFA92233056D728C555505D6B935D7048646D49445EB346F825.pdf
- Manual de conflito de interesses da CGU (2022): https://repositorio.cgu.gov.br/bitstream/1/68381/3/manual_de_tratamento_de_conflito_de_interesse.pdf

## Correções em relação à versão 1
- A questão do `devtools` é da UERJ, não da UNEAL. Da UNEAL só vale a autoconfiguração (Q4234281).
- A questão de Spring Boot atribuída ao TCE-RN 2026 não foi confirmada e foi retirada.
- A questão SEPLAG-AL 2026 é sobre React, não Spring/Quarkus.
- A questão Spring Data JPA com `@Transactional` não é do Cebraspe (a etiqueta de Porto Velho 2026 era de outra questão, sobre ACID).
