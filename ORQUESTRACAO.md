# ORQUESTRACAO — como o Claude conduz o workflow (ler antes de agir)

Regra de ouro: **o estado vive nos arquivos, não na memória do Claude.** O cargo-alvo e o edital estão em `concursos/<ativo>/concurso.json` e `programa.md` (fonte da verdade do que ensinar; códigos `PROVA·BLOCO n.m`). Antes de qualquer passo, rodar:

```
python3 banco.py concurso mostrar       # concurso e cargo ativos
python3 banco.py edital lacunas         # subitens do programa ainda sem questão (--listar --bloco P3·ENG)
python3 banco.py prova proxima          # o que fazer em cada prova pendente
python3 banco.py rank --edital "<tema>" # cobertura e plano do tema pedido
```

## 1. Pedido "aula/caderno do tema T"
1. `rank --edital T`. Leia a RECOMENDAÇÃO:
   - "classificar antes": há itens sem núcleo → classificar (passo 3) e repetir.
   - "MINERAR": cobertura < 70% → passo 2.
   - "PODE ENSINAR": ir ao passo 5.
2. **Minerar**: se não há prova pendente, escolher a próxima em `claude/ranking-compatibilidade-provas.md`, cadastrar (`prova add`) e seguir `prova proxima`. Uma prova por vez.
3. **Estados da prova e quem age** (cada mudança de estado passa por um portão no `banco.py`):

| Estado | Quem age | Comando que avança | Portão (recusa se falhar) |
|---|---|---|---|
| descoberta | **Script local** (`prova processar ID`); Chrome só se o download direto falhar | `prova processar ID` (baixa, grava hash, avança) | `provas/ID/prova.pdf` e `gabarito.pdf` válidos; hash gravado |
| baixada | **Script local** (mesmo comando extrai texto e itens) | `prova processar ID` avança sozinho se fechar | N itens = N gabaritos (anulados excluídos) = linhas de `extraidos/ID.jsonl` |
| extraida | **Agente `classificador-itens`** (skill `classificacao-itens-cebraspe`) | `prova estado ID classificada` | `classificacoes/ID.jsonl` cobre exatamente os itens; código do edital existente em `programa.json` (ou FORA) e etiquetas válidas |
| classificada | `prova amostra ID` + **agente `verificador-classificacao`** | `comparar ID` | concordância ≥ 90% edital, 80% núcleo, 80% pegadinha; senão volta a `extraida` |
| verificada | `banco.py` | `aplicar ID` | grava, ignora duplicatas, cadastra núcleos novos |
| persistida | — | — | — |
| bloqueada | decisão do Jonathas | `prova estado ID bloqueada --nota "motivo"` | (ex.: TEC 405/429) |

4. Depois de `aplicar`, voltar ao passo 1.
5. **Aula**: use o plano do `rank` (ENSINAR a1, a2…; máx. 10 núcleos por aula). Lacunas do edital sem questão são ensinadas pela base legal, marcadas "sem questão".
6. **Caderno**: escolher ≤10 ids do banco ligados aos núcleos da aula; salvar a lista em JSON; rodar `verificar-caderno lista.json`. Só entregar se der APROVADO.

## 1b. Economia de créditos (regra de trabalho)
Tudo que é mecânico roda **na máquina do Jonathas** e devolve ao Claude uma linha de resumo: download, hash, texto, itens, gabarito, portões, amostra, comparação, ranking, validação de caderno. O Claude só entra onde há julgamento: classificar (agente), verificar a amostra (agente), escrever aula e caderno.
- Nunca colar PDF, texto de prova ou JSONL inteiro na conversa. Passar ao agente **só o caminho** do arquivo.
- Não abrir `prova.txt` salvo para consertar item listado em "revisar à mão" ou "não localizados".
- Uma chamada de `prova processar ID` substitui o fluxo antigo (Chrome + extração manual).
- Classificação em lote: um agente por prova, lendo `extraidos/ID.jsonl` e escrevendo `classificacoes/ID.jsonl`; a conversa recebe só a contagem e os itens com dúvida.

## 1c. Arquivos de cada prova (`provas/ID/`)
`prova.pdf`, `gabarito.pdf` (use o definitivo), `fonte.txt` (origem e data), `prova.txt`, `gabarito.txt`. Prova com URL do gabarito indisponível: `prova processar ID --local PROVA.pdf GAB.pdf` copia de arquivos que você já baixou.

## 1e. Trocar de concurso ou cargo
`python3 banco.py concurso usar ID` (ou variável BANCO_CONCURSO). Novo edital: criar `concursos/<id>/`, colocar o PDF, rodar `python3 scripts/importar_edital.py edital.pdf --cargo N --saida concursos/<id>` e escrever `concurso.json`. Banco, núcleos, manifesto e classificações são separados por concurso; `provas/` e `extraidos/` são compartilhados.

## 1d. Manter o panorama atualizado
Sempre que mudar a estrutura (comando, estado, portão, pasta, agente, skill, regra de custo): editar os blocos DADOS e o CHANGELOG em `docs/gerar_panorama.py` e rodar `python3 docs/gerar_panorama.py` (local, sem créditos). Gera `docs/PANORAMA-CGU-BD.pdf`.

## 2. Falhas: o que fazer
- Portão recusou → corrigir a causa, nunca forçar o estado.
- Verificação reprovada → reclassificar a prova inteira passando os desacordos como exemplos; se reprovar de novo, parar e perguntar ao Jonathas.
- Site bloqueou (405/429/CAPTCHA) → `bloqueada`, parar de acessar, avisar. Não contornar.
- Item com `duvida` → mostrar ao Jonathas antes de usar em caderno (`verificar-caderno` já recusa).

## 3. Como disparar
- **Skill**: o usuário digita `/nome` ou descreve a tarefa; o Claude a carrega.
- **Agente**: o usuário pede em linguagem natural ("classifique a prova X"); o Claude lê `agentes/<nome>.md` e dispara com essas instruções + os caminhos dos arquivos. Provas independentes podem ir em paralelo.

## 4. Limites
Limiares (70% cobertura, 80% massa, 90/80/80 concordância, 10 núcleos/aula) são regras iniciais a calibrar. O extrator (`prova extrair`) foi testado só no padrão Cebraspe de duas colunas (TCE-AC 2024 cargo 11: 70/70 itens). Itens com código/figura saem marcados `revisar` e a figura fica no campo `figura`. Outras bancas ou layouts podem exigir ajuste.

## Etapa 1 — Descoberta otimizada (v4.3)
`python3 scripts/descobrir.py catalogo | ranquear | varrer | relatorio` (tudo local, zero créditos; log em `logs/execucao.log`).
- catalogo: cache da API pública do Cebraspe (eventos 2021+). ranquear: prior por metadados (cargo/órgão/recência) ordena as provas.
- varrer: baixa prova+gabarito, extrai itens (texto normal ou 2 colunas, escolhe o que fecha com o gabarito), pontua cada ITEM contra o programa (BM25 local) e grava `escopo/ID.jsonl` com TODO item compatível (mesmo 1). Prova com 0 compatíveis é descartada.
- Paradas: máx. de provas por rodada, ganho marginal baixo (4 provas) e alvo total de itens.
- Nomes: `<orgao>-<ano>-c<NN>-<area>` (ex.: tce-ac-2024-c06-gestao-dados); bloco comum = `-cg-bloco-comum`.

### Mineração recursiva e confiança (v4.5)
`python scripts/minerar.py` atualiza o catálogo e o ranking local antes de cada rodada, respeita a pausa mínima entre PDFs, reaproveita downloads válidos e não volta a baixar URL/hash já existente no acervo. HTTP 403/429 interrompe a rodada; falhas transitórias ficam retomáveis.

O laço repete descoberta e varredura enquanto a suficiência indicar lacunas. Ao final executa os classificadores locais de P1/P3 para atualizar filas auditáveis e grava `fila/automacao-local.json`; não aplica automaticamente nenhuma previsão ao banco. `scripts/validar_lotes.py` verifica estrutura e cobertura, mas a classificação semântica e a verificação independente ainda exigem o agente/usuário. Próximas ações ficam em `fila/automacao-pendencias.json`.

Confiança do P1 não é transferida para P2/P3. A amostra de descartados de P1 só mede o bloco P1; os outros blocos precisam de amostra própria. Para P2/P3, a existência de 30/15 rótulos cegos permite auditar a precisão da triagem, mas não aprova a ordem automaticamente.

## Teste de eficiência por etapa (04/11/2026) — resultados
| Etapa | Teste | Resultado | Ação |
|---|---|---|---|
| 1 Descoberta | recall: 30 itens descartados lidos à mão | 4–7 de 30 eram do edital (XSS, CSRF, JWT, TLS, Scrum) | `lexico.json` por tópico; recuperou 3 de 7; TLS/JWT ainda falham (exigem ≥2 termos) |
| 2/3 Baixada+extraída | contagem = gabarito, enunciados vazios | 12/12 contam certo, mas 7 itens vazios (BDMG, TC-DF) | `texto_melhor`: normal, colunas, colunas+layout; 0 vazios. Pendente: cabeçalho "Julgue os itens…" virando enunciado (c10 item 52) |
| 3 Duplicatas | mesma questão em vários cargos | 12% repetidas (63 removidas) | `descobrir.py dedupe` + `aplicar` descarta por texto |
| 4 Classificação | gates + custo | c11: ok; c10: 93k tokens, 40 itens, 13 FORA | pacote compacto ok; custo dominado pelo contexto do agente |
| 5 Verificação | canário adulterado | reprova 55% edital: detecta erro grosseiro | ok |
| 5 Verificação | c11 (11 itens) | aprovada 91/100/100 | ok |
| 5 Verificação | c10 (12 itens) | REPROVADA 67/50/83: 4 itens FORA para o classificador e do edital para o verificador (OAuth, TLS, cripto simétrica, assinatura digital) | fronteira FORA × edital é a falha; ver proposta |
| 6 Persistência | c11 | 19 inseridos, 0 duplicados | ok |
| 7 Rank | c11 | funciona; cobertura 0% com 3 itens | falta volume |

## Lote por tema (validação ponta a ponta, tema P3·SEG 1)
`descobrir.py tema "P3·SEG 1"` junta os itens de todas as provas pendentes que caem na seção do edital numa prova-lote (`tema-...`), que passa por classificar → verificar → comparar → aplicar. Regra no pacote: usar primeiro os códigos do tema alvo; FORA só se nenhum código tratar do assunto.
Resultado: 41 itens (5 provas) → 38 aplicados (3 excluídos: enunciado truncado/gabarito não verificável) → rank: 28 itens, 20 núcleos, cobertura 54%.
`python3 scripts/painel.py` gera `painel.html` (funil, ENTRA/SAI/GATE por etapa, estado das provas, cobertura por seção).

## Cache de aulas (heurística, 04/11/2026)
Antes de gerar qualquer aula (com ou sem workflow): `python3 scripts/aula.py status "<tema>"`.
- EM DIA -> entregar `aulas/<tema>/aulaN/aula.pdf` (zero tokens).
- DESATUALIZADA (itens novos nos mesmos núcleos) -> atualizar só o caderno e as pegadinhas; teoria fica.
- Núcleo novo -> escrever só o bloco novo; reaproveitar o resto.
- "refazer" -> versão nova (v2), manter a v1.
- Sem workflow: consultar o cache primeiro; aula livre sem banco fica com origem diferente e não entra no cache do workflow.
- Caderno repetido: `aula.py proximos "<tema>"` traz só itens ainda não usados (ledger `aulas/cadernos_usados.jsonl`).
- Visual: `aulas/_template/dark.css` + `corpo.html` por aula; `scripts/render_aula.py aulas/<tema>/aulaN` gera o PDF sem gastar tokens (precisa playwright; rodar no container se a VM não tiver).
- Fonte de cada aula: `corpo.html` + `manifest.json` (núcleos, estado e hash do banco, itens do caderno).

## Micro-aulas e trilha de treino (04/11/2026)
`aula.py plano "<tema>" [--max-nucleos 5 --fracao 0.28 --teto 6]` divide o tema em micro-aulas (~30 min), amostra os itens por núcleo (cota proporcional, piso 1, teto 6, para ao saturar) e monta cadernos A (definições), B (pegadinhas), C (mistura), todos <=10 itens e sem repetir itens já usados (ledger). `aula.py relatorio DIR` gera `relatorio.html` com gabarito comentado automático (sem tokens). Exemplo com banco simulado: `demo-simulacao/exemplo-plano-simulado.html` (`scripts/demo_sintetico.py`).

## App local CGU Treino (M1, 04/11/2026)
`app/iniciar.bat` (duplo clique) abre http://127.0.0.1:8787: Painel, Treino (cadernos com progresso), Progresso, Aulas (HTML), Banco. Progresso em `%LOCALAPPDATA%\cgu-treino\treino.db` + espelho `progresso/respostas.jsonl` (lido pelo Claude para analisar erros). O app só chama/lê os arquivos do workflow; não reimplementa nada. Próximas fatias: M2 execução das etapas mecânicas com log ao vivo; M3 aulas e fila de pedidos ao Claude; M4 API key.

## Progresso ao vivo (app v0.0.17, 04/11/2026)
A aba Workflow é dinâmica: atualiza a cada 2 s e junta (a) eventos derivados de alterações em arquivos e do `execucao.log` (automático) e (b) eventos que o Claude e os scripts registram.
Registrar (b) em toda etapa: `python scripts/evento.py --etapa N --lote <lote> --feito X --total Y [--nivel info|ok|aviso|erro] [--fonte claude|script] "mensagem"`.
Etapas: 1 Descoberta · 2 Download e extração · 3 Escopo e duplicatas · 4 Classificação · 5 Verificação · 6 Persistência · 7 Priorização · 8 Aula.
Momentos: início da etapa ("iniciando"), a cada bloco (feito/total em itens), fim (`--nivel ok`) e qualquer falha (`--nivel erro` com a causa). Não escrever segredos nem texto de questão no evento (máx. 300 caracteres).
Progresso automático por lote: classificação = itens em `classificacoes/<lote>.jsonl` + `-pendentes-revisao.jsonl` contra o total em `escopo/<lote>.jsonl`; verificação = itens em `verificacoes/<lote>.jsonl`.
