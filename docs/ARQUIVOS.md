# ARQUIVOS — formato e local de cada peça

## Mapa de pastas
```
cgu-bd/
  README.md  ORQUESTRACAO.md      ← entrada e roteiro (ler primeiro)
  banco.py  scripts/                  ← código
  concursos/ativo.txt  concursos/<id>/  ← concurso.json (cargo-alvo), edital-oficial.pdf, programa.json/.md,
                                         regras-da-prova.md, banco.jsonl, nucleos.jsonl, provas.jsonl, classificacoes/ ...
  edital-topicos.md  taxonomia-pegadinhas.md   ← tabelas lidas por skills/agentes
  docs/tec/ (plano-filtros-tec.md, tec-cadernos.json, openapi)  ← coleta no TEC
  skills/  agentes/               ← instruções (.md)
  docs/                           ← manuais (este arquivo, workflow, portabilidade, regras do Projeto)
  referencia/                     ← documentos históricos transcritos do Projeto
  extraidos/ classificacoes/ amostras/ verificacoes/ cadernos/ provas/*   ← criados no primeiro uso
```
(* criado sob demanda)

Pasta no PC: `C:\Users\jonathas.000\Documents\provas\CGU-AFFC-Auditor-Fiscal-Financas-Controle\cgu-bd\`
Espelho (cópia de segurança e leitura pelo Claude): Projeto "CGU AFFC", pasta `claude/`.

## A. Instruções (texto, .md) — dizem COMO fazer
| Peça | Formato | Onde fica | Quem usa |
|---|---|---|---|
| Skill `classificacao-itens-cebraspe` | `SKILL.md` (cabeçalho `name` + `description`, depois instruções) | **conta Claude** + cópia em `cgu-bd\skills\classificacao-itens-cebraspe\SKILL.md` | Claude e agentes |
| Skills `priorizacao-temas-banca`, `coleta-questoes-concurso` | idem | **conta Claude** + cópia em `cgu-bd\skills\<nome>\SKILL.md` | Claude |
| Agente `classificador-itens`, `verificador-classificacao` | `.md` com cabeçalho (`name`, `description`, `tools`, `model`) + instruções | `cgu-bd\agentes\*.md` e Projeto `claude/agente-*.md`. **Não registrados na conta**: o Claude os lê e dispara | Claude |
| `ORQUESTRACAO.md` | texto | `cgu-bd\` e Projeto | Claude (roteiro) |
| `taxonomia-pegadinhas.md`, `edital-topicos.md` | tabelas em texto | `cgu-bd\` e Projeto | Claude, agentes |

## B. Dados (JSONL = uma linha de JSON por registro) — o ESTADO
| Arquivo | Conteúdo | Quem escreve |
|---|---|---|
| `concursos/<id>/banco.jsonl` | itens classificados (enunciado, gabarito C/E, ref, url, edital, núcleos, tags, nível) | `banco.py` |
| `concursos/<id>/nucleos.jsonl` | ideias testadas: id, texto, edital, base legal | `banco.py` |
| `concursos/<id>/provas.jsonl` | **manifesto**: estado de cada prova + histórico + hash + resultado da verificação | `banco.py` |
| `extraidos/ID.jsonl` | itens extraídos do PDF, sem classificação | extrator |
| `concursos/<id>/classificacoes/ID.jsonl` | saída do classificador (uma linha por item) | agente classificador |
| `concursos/<id>/amostras|verificacoes/ID.jsonl` | amostra (20%) e reclassificação independente | `banco.py` / agente verificador |
| `provas/ID/` | `prova.pdf`, `gabarito.pdf`, `fonte.txt`, `prova.txt`, `gabarito.txt` (originais e texto) | `banco.py prova processar` (local) |
| `cadernos/*.json` | lista de ids de cada caderno, validada pelo `verificar-caderno` | Claude |

## C. Código
`banco.py` (v4, só biblioteca padrão do Python). Dados são texto puro: abrem em qualquer editor, versionam em git e sobrevivem à pasta sincronizada.

## Resumo em uma frase
Skills e agentes = **instruções em .md** (o "como"); o **estado** do processo = **arquivos .jsonl** (o "onde estamos"); o `banco.py` = **fiscal** que só deixa o processo avançar se o portão passar.
