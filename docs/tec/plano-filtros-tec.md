# Plano de filtros do TEC (planejado, nada criado ainda)

Regras (inspiradas na skill pública gerar-filtros-tec):
- Um filtro por tema do edital, nunca um caderno gigante; cada filtro com banca Cebraspe e status "não resolvidas".
- Antes de criar, consultar `docs/tec/tec-cadernos.json`; se já houver caderno do tema, reutilizar.
- Nome: `CGU-AAAA-MM-Bloco-Tema` (ex.: `CGU-2026-11-ARQ-OAuth-OIDC`).
- Temas com poucas questões (< 10) são agrupados com um tema vizinho.
- Ler só os itens que o Jonathas pedir, no ritmo das heurísticas; o banco local vem primeiro.

| Bloco do edital | Filtros sugeridos (nome) | Prioridade |
|---|---|---|
| Arquitetura e integração | CGU-ARQ-OAuth-OIDC-Tokens · CGU-ARQ-Spring-Security · CGU-ARQ-Microsservicos-Eventos · CGU-ARQ-Idempotencia-Mensageria | Alta |
| Persistência e dados | CGU-PERS-SQL-Indices · CGU-PERS-JPA-SpringData · CGU-PERS-ETL-Batch · CGU-PERS-LGPD-Cripto | Alta |
| Desenvolvimento seguro e entrega | CGU-SEG-DevSecOps-CICD · CGU-SEG-Testes-Qualidade · CGU-SEG-Scrum-Kanban · CGU-SEG-Contratacao-TI | Alta |
| Engenharia de software | CGU-ENG-Java-Colecoes-Excecoes · CGU-ENG-Concorrencia · CGU-ENG-Padroes-Projeto · CGU-ENG-Vue-UX | Média |
| P1/P2 | CGU-P1-PPA-LDO-LOA (reutilizar caderno 107753370) · demais temas sob demanda | Média |

Obs.: a existência e o tamanho de cada filtro no TEC não foram verificados.
