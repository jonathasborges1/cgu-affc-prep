# Workflow v2: tema do edital → aulas e caderno por probabilidade (04/11/2026)

Pergunta que responde: "o que eu preciso saber para ir bem na prova neste tema?". Unidade de estudo = **núcleo** (a ideia que um item testa). Massa, cobertura e regra de profundidade: ver `workflow-engenharia-reversa-probabilistica.md` (continua valendo).

## Quem faz o quê (recursos do Claude usados)

| # | Etapa | Executor | Recurso |
|---|---|---|---|
| ① | Consulta ao banco: núcleos, massa, cobertura | `banco.py rank` (script) | skill `priorizacao-temas-banca` |
| ② | Busca de provas novas (1 PDF por vez, pausa) | Eu, no Chrome | skills `coleta-questoes-concurso` + `chrome-browser`; permissão explícita para baixar |
| ③ | Extração de itens + gabarito | Script (Python) | skill `pdf-reading` (apoio); manifesto `provas.jsonl` |
| ④ | Classificação | **Agente `classificador-itens`**, um por prova, em paralelo | skill `classificacao-itens-cebraspe`, `edital-topicos.md`, `taxonomia-pegadinhas.md`, `nucleos.jsonl` |
| ④b | Verificação independente | **Agente `verificador-classificacao`** (amostra de ~20%, sem ver o original) | mesma skill; script compara e mede concordância |
| ⑤ | Gravação | `banco.py add-json` (valida, ignora duplicatas, atualiza manifesto) | só grava se a verificação passou |
| ⑥ | Plano de aula | `banco.py rank` + eu | skill `priorizacao-temas-banca` |
| ⑦ | Aula (PDF dark) + caderno (≤10 itens com referência real) | Eu | skill `pdf`; regras do Projeto |

## Fluxo

```
tema do edital
   │
① rank ── cobertura ≥ ~70%? ── sim ─────────────────────────────┐
   │ não                                                         │
② buscar (Chrome, serial) → ③ extrair (script)                   │
   │                                                             │
④ classificadores em paralelo (1 por prova) ── JSONL             │
   │                                                             │
④b verificador (amostra 20%) → concordância ok? ── não → reclassifica a prova
   │ sim                                                         │
⑤ banco.py grava + manifesto → volta a ① ───────────────────────┤
                                                                 ▼
                                ⑥ plano (massa + vizinhos + lacunas) → ⑦ aula + caderno
```

## Critérios de qualidade (portões)
- **Cobertura ≥ ~70%** para parar de minerar (ou acabaram as provas-espelho).
- **Verificação:** concordância mínima edital ≥ 90%, núcleo ≥ 80%, pegadinha (≥1 em comum) ≥ 80%. Abaixo disso, a prova volta ao classificador com os desacordos como exemplos. Itens em desacordo vão para revisão sua.
- **Extração:** nº de itens extraídos = nº de gabaritos; senão a prova não avança.
- **Caderno:** cada questão com banca, órgão, cargo, ano, URL; máx. 10; gabarito conferido no GAB definitivo.

## Onde cada coisa fica
- PC (`cgu-bd`): `banco.py`, `concursos/<ativo>/` (banco.jsonl, nucleos.jsonl, provas.jsonl, programa.json, concurso.json), `ORQUESTRACAO.md`, `docs/ARQUIVOS.md`, `edital-topicos.md`, `taxonomia-pegadinhas.md`, `skills/classificacao-itens-cebraspe/SKILL.md`, `agentes/classificador-itens.md`, `agentes/verificador-classificacao.md`.
- Skills da conta (aparecem para o Claude): `priorizacao-temas-banca`, `coleta-questoes-concurso` e, após você salvar o cartão, `classificacao-itens-cebraspe`.
- Agentes: as definições ficam no PC e no Projeto; para rodar, eu as disparo com a ferramenta de agentes passando o texto da definição como instrução (não ficam registrados na sua conta como subagentes permanentes).

## Outros recursos considerados
- **Lista de tarefas** (já uso): mostra o andamento por etapa e prova.
- **Perguntas de múltipla escolha**: para decisões suas (baixar PDF? aceitar núcleo duvidoso?).
- **Memória do Projeto**: guarda regras de coleta e preferências entre sessões.
- **Tarefa agendada**: possível para minerar devagar (ex.: 1 prova por dia), mas o Chrome precisa estar aberto no seu PC; não ativei. Decida depois do teste.
- **Hooks / automações locais**: não necessários agora.
- **Validação de caderno** (`banco.py verificar-caderno`): pronta; checa referência, URL, ≤10 itens, gabarito e itens com dúvida antes de eu entregar.

## Status das peças (atualizado em 04/11/2026)
Prontas no `banco.py` v4, testadas com prova sintética montada com itens reais do banco:
`nucleo add`, `set-nucleos`, `prova add/estado/listar/proxima/amostra` (manifesto `provas.jsonl` com portões), `comparar`, `aplicar`, `rank`, `verificar-caderno`.
Roteiro de condução: `orquestracao.md`. Formatos e locais: `arquivos-formato-e-local.md`.
Falta: o **extrator de PDF** (será feito no primeiro uso real e registrado em `orquestracao.md`).
Piloto PPA/LDO/LOA: os 10 itens já têm núcleos; `rank` reproduz 8 núcleos e cobertura de 40%.

## Limites honestos
- Limiares (80%, 70%, 90/80/80, distância 2) são regras iniciais minhas, a calibrar.
- O classificador usa julgamento de IA; por isso existe o verificador e a revisão humana dos duvidosos.
- Nível de dificuldade é estimativa, não dado oficial da banca.
- Ritmo de coleta e Termos de Uso do TEC/Cebraspe: não confirmados.
