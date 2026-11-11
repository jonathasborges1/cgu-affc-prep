# Como o filtro do TEC Concursos funciona (e a rota do nosso tema)

Observado em 04/11/2026 na tela https://www.tecconcursos.com.br/questoes/filtrar, no navegador embutido, com o usuário logado.
Contrato técnico: `docs/tec/tec-filtros.openapi.yaml` (estilo Swagger). Este arquivo explica em português.

## 1. Resposta curta: a rota devolve "todas as questões de prova"?

**Não.** Ela faz três coisas separadas:

| Etapa | Chamada | O que devolve |
|---|---|---|
| Contar | `POST /api/questoes/contagem/filtros` | só o total (`{"int": 1674}`) |
| Listar | `POST /api/questoes/filtros` | só **ids** das questões, uma página de cerca de 100 por chamada |
| Detalhar | por id (a tela busca o texto de cada questão à parte) | enunciado, alternativas, gabarito (exige login/plano) |

E "todas" vale só para o **catálogo do TEC e para a classificação do TEC**: uma questão que o TEC classificou em outro assunto não entra na rota, mesmo que fale do tema.

## 2. Modelo mental

```
Nome digitado --GET /api/assuntos?nome=...-->  matéria + assunto (id, hierarquia, descendentes)
      |
      v
Filtros ativos = lista de pares (tipo, id)   ex.: ASSUNTO=1463, BANCA=4, FILTRO_QUESTAO=REMOVER_ANULADAS
      |
      +--POST /contagem/filtros--> total
      +--POST /questoes/filtros--> ids (~100 por pagina)
      +--POST /materias/... e /assuntos/...--> tabelas de distribuição
```

Pontos que importam:
- **Os filtros se combinam com E** (cada filtro novo reduz o total). Contagens observadas: sem filtro 4.244.858; assunto 1463 = 8.082; + Remover anuladas = 7.933; + Banca CEBRASPE = **1.674**.
- **Assunto pai inclui os filhos.** O campo `descendentes` do assunto 1463 é `1463;1464;1465;1468;1469;1741`.
- **A busca por nome é global**, não restrita à matéria marcada. Mesmo nome pode existir em várias matérias.
- **O nome do filtro "Remover anuladas" é um filtro como os outros**: `tipo=FILTRO_QUESTAO`, `id=REMOVER_ANULADAS`.

## 3. Formato da requisição (observado)

Corpo form-urlencoded, um bloco `filtros[i].tipo` + `filtros[i].id` por filtro:

```
POST /api/questoes/contagem/filtros
universo=&formato=OBJETIVA&gerarEmSerie=false&caderno=
&filtros[0].tipo=ASSUNTO&filtros[0].id=1463
&filtros[1].tipo=FILTRO_QUESTAO&filtros[1].id=REMOVER_ANULADAS
&filtros[2].tipo=BANCA&filtros[2].id=4
-> {"int": 1674}
```

```
POST /api/questoes/filtros
formato=OBJETIVA&universo=&pagina=
&filtros[0].id=1463&filtros[0].tipo=ASSUNTO
&filtros[1].id=REMOVER_ANULADAS&filtros[1].tipo=FILTRO_QUESTAO
&filtros[2].id=4&filtros[2].tipo=BANCA
-> {"questoes": [3828763, 3830511, 3830513, ...]}   (~100 ids)
```

## 4. A rota do tema P1 · Administração pública 4.1 (PPA, LDO e LOA), Cebraspe

Onde o TEC classifica o tema (não é em "Administração pública"):

- Matéria: **AFO, Direito Financeiro e Contabilidade Pública** (id 69)
- Assunto pai: **Instrumentos Orçamentários na CF 88 (PPA, LDO e LOA)** (id **1463**, hierarquia 02.05)
- Filhos conhecidos: 1464 PPA – Plano Plurianual (CF/1988 e Lei 4.320/1964); 1469 Tópicos Mesclados de PPA, LDO e LOA. Os ids 1465, 1468 e 1741 não tiveram o nome conferido.

Filtros: `ASSUNTO=1463` + `BANCA=4` (CEBRASPE/CESPE) + `FILTRO_QUESTAO=REMOVER_ANULADAS`.
**Resultado: 1.674 questões** (confirmado na tela em 04/11/2026). Com o filtro de ano 2022–2026 o total cai (não medido).

Ruído a evitar na busca por "PPA": Decreto 2.829/1998 (norma antiga, conferir vigência), Decreto Estadual 22.770/2024 (BA), Lei Estadual 20.755/2020 (GO), Lei Estadual 11.626/2020 (PB). O edital pede o tema em nível conceitual.

## 5. Limites desta documentação

- Observação, não contrato. O TEC pode mudar os endpoints.
- Não verificados: tipos de filtro de matéria, ano e órgão; `REMOVER_DESATUALIZADAS`; formato das páginas seguintes (`pagina`); corpo de `/materias/buscar-questoes-por-materia` e de `/assuntos/buscar-questoes-por-asssunto-mais-materia`; resposta de sucesso do detalhe da questão.
- O detalhe por id respondeu HTTP 402 em sessão anterior (sem plano/limite do gratuito).

## 6. Uso responsável

Chamadas diretas em rajada geraram bloqueio (405/429 e "Human Verification") em 04/11/2026, e os termos de uso do TEC ainda não foram lidos. Para estudar, monte o filtro pela interface (guia `Guia_Filtros_TEC_Concursos.pdf`) e salve o caderno. Estes endpoints estão documentados para entender o funcionamento, não para varredura automática.
