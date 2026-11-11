# CGU/AFFC – projeto de estudo (cgu-bd)
Objetivo: banco de questões reais do Cebraspe (CGU/AFFC 2026, TI – Desenvolvimento de Sistemas) e aulas em HTML/PDF dark.

Regras fixas:
- Fonte de questões: (1) o CDN oficial do Cebraspe (provas PDF públicas); (2) TEC Concursos, SOMENTE como fonte assistida: o usuário é assinante e baixa/imprime o caderno por conta própria; o Claude lê apenas o PDF entregue, sem automação, robô, scraping nem uso de cookies/sessão, e `ref`/`url` de cada item apontam ao TEC. Mesmo assim, lote TEC só entra no banco depois de `verificada` e sem `duvida` na classificação. Nunca automatizar sites que proíbem robôs.
- Nunca inventar questão. Toda questão exige prova de origem + item; sem referência real, remover.
- Classificação usa o edital (`concursos/<ativo>/edital`), taxonomia fechada de pegadinhas. Classificador e verificador trabalham em contextos separados.
- Só rodar scripts do projeto: `python scripts/descobrir.py`, `python scripts/aula.py`, `python banco.py`. Gravar apenas em `aulas/`, `concursos/`, `progresso/chat/`, `fila/`.
- Aula: ≤5 núcleos por micro-aula, cadernos ≤10 itens, sem repetir itens do ledger (`aulas/cadernos_usados.jsonl`). Verifique o cache com `python scripts/aula.py status "<tema>"` antes de gerar.
- Conteúdo fora da área de TI: ensinar do zero, com analogias, tabelas e esquemas; dedução passo a passo de qualquer fórmula.
- Progresso ao vivo (aba Workflow do app): em TODA etapa, registrar eventos com `python scripts/evento.py --etapa N --lote <lote> --feito X --total Y "mensagem"` — ao iniciar, a cada bloco de itens e ao terminar (`--nivel ok`) ou falhar (`--nivel erro`). Grava só em `logs/eventos.jsonl`. O app também deriva progresso sozinho dos arquivos, mas só o Claude sabe o que está fazendo agora.

- REGRA DE PARADA: aulas e cadernos sao criados so sob pedido do aluno, um por vez. O app garante apenas a estrutura-base (`aula.py preparar "<tema>"`, somente leitura). Caderno e a ultima etapa e exige pedido proprio; `aula.py plano|registrar` e `associar.py --gravar` exigem `--confirmar-caderno`.

- MODELO VISUAL: toda aula tem >=1 figura original (SVG, sem imagens da web) por bloco, gerada por `figuras.py` com `aulas/_template/visuais.py`; seguir `aulas/_template/MODELO-AULA-VISUAL.md` e conferir as figuras em PNG antes de entregar.

- PROTOCOLO PEDAGOGICO: cada bloco conceitual segue `aulas/_template/MODELO-AULA-PEDAGOGICO.md` (aposta, analogia, cenário no setor público com decisão e consequência, exemplo x contraexemplo, pegadinha, recuperação com autoexplicação; ajuda decrescente).

- GLOSSARIO: toda sigla nova de aula entra em `aulas/_template/glossario.json` (ou `aulas/<aula>/glossario.json`); o app mostra tooltip com o nome completo (ver MODELO-AULA-PEDAGOGICO.md).

- GATILHOS: palavras-gatilho (pode, deve, apenas, só, exclusivamente...) coloridas verde/vermelho/amarelo conforme a afirmação esteja certa/errada/cuidado; nunca no caderno (ver MODELO-AULA-PEDAGOGICO.md).
- ORDEM DOS TERMOS: nenhum termo técnico antes do bloco que o define; use termo-ponte (span.ponte) e caixa 🔁 Retomada no bloco do segundo conceito; cada aula tem termos.json e blocos.py roda ordem_termos (deve dar 0).
