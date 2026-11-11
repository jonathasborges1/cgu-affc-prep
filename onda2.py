#!/usr/bin/env python3 -I
"""
onda2.py — Onda 2 do plano de ataque CGU/AFFC 2026
====================================================
Objetivo: classificar as top-N provas TI mais compatíveis com o P3 do edital,
gerar escopo filtrado por termos do edital e preparar lotes para o agente
classificador Claude.

Pipeline por prova:
  1. Verifica se a prova está em estado 'extraida' e tem extraidos/ID.jsonl
  2. Roda `prova filtrar ID --termos TERMOS` → gera escopo/ID.jsonl
  3. Chama o agente classificador (via instrução impressa, ainda manual)
  4. Após classificação: merge escopo + classificacoes → add-json (via merge_persiste)

Uso:
  python3 onda2.py              # mostra o plano (sem executar)
  python3 onda2.py --filtrar    # executa etapa de filtro em todas as provas do plano
  python3 onda2.py --persistir  # merge + add-json das já classificadas
  python3 onda2.py --status     # resumo atual (escopo, classificacao, banco)
  python3 onda2.py --id ID      # opera só nessa prova (combinar com --filtrar ou --persistir)
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BANCO_DIR = Path(__file__).parent
BANCO_PY  = BANCO_DIR / "banco.py"
CONC_FILE = BANCO_DIR / "concursos" / "ativo.txt"
ATIVO     = CONC_FILE.read_text().strip()
CONC_DIR  = BANCO_DIR / "concursos" / ATIVO

EXTRAIDOS_DIR    = BANCO_DIR / "extraidos"
ESCOPO_DIR       = CONC_DIR / "escopo"
CLASSIF_DIR      = CONC_DIR / "classificacoes"
BANCO_JSONL      = CONC_DIR / "banco.jsonl"

# ---------------------------------------------------------------------------
# Termos do edital P3 — usados no prova filtrar
# Organizados por subbloco para facilitar ajuste
# ---------------------------------------------------------------------------
TERMOS_P3_ENG = [
    # Java e OO
    "java", "classe", "objeto", "heranca", "polimorfismo", "encapsulamento",
    "interface", "colecao", "generics", "excecao", "exception",
    # Algoritmos e estruturas
    "algoritmo", "complexidade", "big-o", "lista", "fila", "pilha", "arvore",
    "grafo", "hash", "ordenacao", "busca", "recursao",
    # Concorrência
    "concorrencia", "paralelismo", "thread", "sincronia", "deadlock",
    "race condition", "mutex", "semaforo",
    # UI/UX
    "usabilidade", "acessibilidade", "interface", "prototipo", "responsivo",
    "vue", "javascript", "componente",
    # Manutenção
    "debito tecnico", "acoplamento", "modularidade", "legado", "refatoracao",
    "interoperabilidade",
]

TERMOS_P3_ARQ = [
    # Arquiteturas
    "microsservico", "monolito", "evento", "event-driven", "soa",
    "serverless", "cloud", "nuvem",
    # Spring
    "spring", "spring boot", "spring framework", "injecao de dependencia",
    "inversao de controle", "ioc", "bean", "autowired",
    # APIs e segurança
    "rest", "api", "oauth", "openid", "jwt", "token", "autenticacao",
    "autorizacao", "spring security", "rbac", "scope",
    # Mensageria
    "mensageria", "kafka", "rabbitmq", "fila", "topico", "idempotencia",
    "consistencia eventual",
    # IA / LLM integração
    "llm", "rag", "embedding", "vetor", "agente", "tool calling",
    "prompt injection",
    # Confiabilidade
    "log", "metrica", "rastreamento", "observabilidade", "latencia",
    "disponibilidade", "circuit breaker", "kubernetes", "docker", "conteine",
]

TERMOS_P3_DADOS = [
    # Modelagem
    "normalizacao", "entidade", "relacionamento", "chave primaria",
    "chave estrangeira", "integridade referencial",
    # NoSQL
    "nosql", "documento", "chave-valor", "mongodb", "redis",
    # JPA / Spring Data
    "jpa", "hibernate", "entidade", "mapeamento", "lazy", "eager",
    "spring data", "repositorio", "pagina", "paginacao",
    # SQL
    "sql", "select", "join", "group by", "subquery", "index", "indice",
    "plano de execucao", "transacao", "commit", "rollback",
    # ETL / Batch
    "etl", "elt", "spring batch", "job", "step", "chunk",
    "reprocessamento", "idempotencia", "parquet", "csv",
    # Privacidade
    "lgpd", "dado pessoal", "dado sensivel", "minimizacao", "anonimizacao",
    "pseudonimizacao", "criptografia", "privacidade",
]

TERMOS_P3_SEG = [
    # Vulnerabilidades
    "sqli", "xss", "csrf", "injecao", "owasp", "vulnerabilidade",
    "validacao de entrada", "sanitizacao",
    # Segredos / dependências
    "segredo", "secret", "dependencia", "supply chain", "sbom",
    "token", "credencial", "vazamento",
    # Testes
    "teste unitario", "teste integracao", "teste contrato", "tdd",
    "cobertura", "analise estatica", "sonar", "lint",
    # CI/CD / DevSecOps
    "ci/cd", "pipeline", "devsecops", "deploy", "rollback",
    "ambiente", "versionamento", "git",
    # Produto / Gestão
    "scrum", "kanban", "sprint", "backlog", "produto digital",
    "pdtic", "transformacao digital",
    # Contratação TI
    "contratacao", "termo de referencia", "etp", "estudo tecnico",
    "nivel de servico", "sla", "fiscalizacao", "propriedade intelectual",
]

TODOS_TERMOS = list(dict.fromkeys(
    TERMOS_P3_ENG + TERMOS_P3_ARQ + TERMOS_P3_DADOS + TERMOS_P3_SEG
))

# ---------------------------------------------------------------------------
# Plano da Onda 2: provas priorizadas (do ranking de compatibilidade)
# Formato: (prova_id, nota_compatibilidade, descricao)
# ---------------------------------------------------------------------------
PLANO = [
    # Tier 1 — altíssima compatibilidade, Cebraspe C/E, foco em Desenv. Sistemas
    ("tce-ac-2024-c11-desenvolvimento-sistemas",   10, "TCE-AC 2024 · cargo 11 · Desenvolvimento de Sistemas (97% compat)"),
    ("dataprev-2023-c07-desenvolvimento-software", 10, "DATAPREV 2023 · cargo 7 · Desenvolvimento de Software (80% compat)"),
    ("tce-rn-2026-c04-ti-desenvolvimento",          9, "TCE-RN 2026 · cargo 4 · Desenvolvimento de Sistemas (80% compat)"),
    ("stj-2024-c03-apoio-especializado-especialidade-an", 9, "STJ 2024 · cargo 3 · Análise de Sistemas (71% compat)"),
    ("tbg-2023-c04-desenvolvimento-software",       9, "TBG 2023 · cargo 4 · Desenvolvimento de Software (77% compat)"),

    # Tier 2 — boa compatibilidade Cebraspe C/E
    ("trf6-2024-c03-apoio-especializado-especialidade-an",  8, "TRF6 2024 · cargo 3 · Análise de Sistemas (84% compat)"),
    ("dataprev-2023-c04-arquitetura-engenharia-tecnologica", 8, "DATAPREV 2023 · cargo 4 · Arquitetura (71% compat)"),
    ("dataprev-2023-c19-seguranca-cibernetica",     8, "DATAPREV 2023 · cargo 19 · Segurança Cibernética"),
    ("dataprev-2023-c11-engenheiro-dados",          8, "DATAPREV 2023 · cargo 11 · Engenheiro de Dados"),
    ("bdmg-2024-c04-sistemas-arquitetura-solucoes-dados", 8, "BDMG 2024 · cargo 4 · Sistemas, Arquitetura e Dados (77% compat)"),

    # Tier 3 — compatível, C/E, foco parcial em P3
    ("seplag-ce-2024-c03-ciencia-computacao-ou-afins", 7, "SEPLAG-CE 2024 · cargo 3 · Ciência da Computação"),
    ("cnpq-2023-c02-desenvolvimento",               7, "CNPq 2023 · cargo 2 · Desenvolvimento"),
    ("banco-do-nordeste-2022-c01-desenvolvimento-sistemas", 7, "Banco do Nordeste 2022 · Desenvolvimento de Sistemas"),
    ("tce-rj-analista-2021-c01-especialidade-tecnologia-informacao", 6, "TCE-RJ 2021 · Analista TI"),
    ("secont-es-2022-c06-tecnologia-informacao",    6, "SECONT-ES 2022 · cargo 6 · TI"),

    # Tier 4 — suplementares (específicos para lacunas)
    ("tce-ac-2024-c06-gestao-dados",               5, "TCE-AC 2024 · cargo 6 · Gestão de Dados (lacuna DADOS)"),
    ("tce-ac-2024-c07-infraestrutura-ti",           5, "TCE-AC 2024 · cargo 7 · Infraestrutura TI"),
    ("tce-ac-2024-c08-planejamento-ti",             5, "TCE-AC 2024 · cargo 8 · Planejamento TI"),
    ("tce-ac-2024-c09-projetos-ti",                 5, "TCE-AC 2024 · cargo 9 · Projetos TI"),
    ("tce-ac-2024-c10-seguranca-informacao",        5, "TCE-AC 2024 · cargo 10 · Segurança da Informação"),
    ("anm-2024-c24-tecnologia-informacao-ciencia-dados", 5, "ANM 2024 · cargo 24 · TI e Ciência de Dados"),
    ("cnmp-2023-c08-tecnologia-informacao-comunicacao-es", 4, "CNMP 2023 · cargo 8 · TI"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def banco(*args, capture=True):
    """Chama banco.py com os argumentos dados."""
    cmd = [sys.executable, "-I", str(BANCO_PY)] + list(args)
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if capture:
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    return None, None, result.returncode


def carregar_provas():
    """Retorna dict prova_id → estado."""
    out, _, _ = banco("prova", "listar")
    estados = {}
    for linha in out.splitlines():
        partes = linha.split()
        if len(partes) >= 2:
            estados[partes[0]] = partes[1]
    return estados


def tem_escopo(prova_id):
    return (ESCOPO_DIR / f"{prova_id}.jsonl").exists()


def tem_classificacao(prova_id):
    return (CLASSIF_DIR / f"{prova_id}.jsonl").exists()


def tem_extraido(prova_id):
    return (EXTRAIDOS_DIR / f"{prova_id}.jsonl").exists()


def contar_itens(path):
    if not path.exists():
        return 0
    with open(path) as f:
        return sum(1 for line in f if line.strip())


def termos_str():
    return ",".join(TODOS_TERMOS)


def merge_e_persiste(prova_id):
    """Merge escopo + classificacoes e chama add-json."""
    escopo_path  = ESCOPO_DIR  / f"{prova_id}.jsonl"
    classif_path = CLASSIF_DIR / f"{prova_id}.jsonl"

    if not escopo_path.exists():
        return False, "sem escopo"
    if not classif_path.exists():
        return False, "sem classificacao"

    # Carrega escopo indexado por item
    escopo = {}
    with open(escopo_path) as f:
        for line in f:
            e = json.loads(line)
            escopo[str(e["item"])] = e

    # Carrega classificações indexadas por item
    classif = {}
    with open(classif_path) as f:
        for line in f:
            c = json.loads(line)
            classif[str(c["item"])] = c

    # Merge
    merged = []
    pulados = 0
    for item_key, e in escopo.items():
        c = classif.get(item_key)
        if not c:
            pulados += 1
            continue
        edital = c.get("edital", "")
        if str(edital).upper() == "FORA":
            pulados += 1
            continue

        m = {
            "prova_id":   prova_id,
            "banca":      e.get("banca", ""),
            "orgao":      e.get("orgao", ""),
            "cargo":      e.get("cargo", ""),
            "ano":        e.get("ano", 0),
            "ref":        e.get("ref", ""),
            "url":        e.get("url", ""),
            "url_gab":    e.get("url_gab", ""),
            "item":       str(item_key),
            "enunciado":  e.get("enunciado", ""),
            "gabarito":   e.get("gabarito", ""),
            "tema":       edital,
            "edital":     edital,  # garante campo edital populado
            "subtema":    c.get("nucleo_texto", ""),
            "nivel":      c.get("nivel", ""),
            "padrao":     c.get("padrao", ""),
            "tags":       c.get("tags", []),
            "nucleos":    [c["nucleo_id"]] if c.get("nucleo_id") else [],
            "fonte":      f"oficial-{prova_id}",
            "peso_prova": 1.0,
            "base_legal": c.get("base_legal", ""),
        }
        merged.append(m)

    if not merged:
        return False, f"nenhum item aproveitável (pulados={pulados})"

    # Salva temporário e chama add-json
    tmp = Path("/tmp") / f"onda2_merge_{prova_id}.jsonl"
    with open(tmp, "w") as f:
        for m in merged:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    out, err, rc = banco("add-json", str(tmp))
    tmp.unlink(missing_ok=True)

    if rc != 0:
        return False, f"add-json falhou (rc={rc}): {err[:200]}"

    # Extrai contagem da saída
    inseridas = 0
    for token in out.split():
        if token.isdigit():
            inseridas = int(token)
            break

    return True, f"inseridas≈{inseridas} (pulados={pulados}) | {out[:120]}"


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

def cmd_status(args):
    """Mostra situação atual de cada prova do plano."""
    estados = carregar_provas()

    print(f"\n{'ID':<52} {'estado':12} {'extrai':7} {'escopo':7} {'classif':7}")
    print("-" * 92)

    para_filtrar   = []
    para_classify  = []
    para_persistir = []
    fora_manifesto = []

    for prova_id, nota, desc in PLANO:
        estado    = estados.get(prova_id, "—")
        extrai    = "✓" if tem_extraido(prova_id) else "✗"
        escopo    = "✓" if tem_escopo(prova_id)   else "✗"
        classif   = "✓" if tem_classificacao(prova_id) else "✗"

        print(f"{prova_id:<52} {estado:<12} {extrai:<7} {escopo:<7} {classif:<7}")

        if estado == "—":
            fora_manifesto.append(prova_id)
        elif estado == "extraida" and extrai == "✓" and escopo == "✗":
            para_filtrar.append(prova_id)
        elif escopo == "✓" and classif == "✗":
            para_classify.append(prova_id)
        elif escopo == "✓" and classif == "✓":
            para_persistir.append(prova_id)

    print()
    print(f"Para filtrar    ({len(para_filtrar)}): {', '.join(para_filtrar[:5])}{'...' if len(para_filtrar)>5 else ''}")
    print(f"Para classificar({len(para_classify)}): {', '.join(para_classify[:5])}{'...' if len(para_classify)>5 else ''}")
    print(f"Para persistir  ({len(para_persistir)}): {', '.join(para_persistir[:5])}{'...' if len(para_persistir)>5 else ''}")
    print(f"Fora do manifesto ({len(fora_manifesto)}): {', '.join(fora_manifesto[:5])}{'...' if len(fora_manifesto)>5 else ''}")


def cmd_filtrar(args):
    """Roda prova filtrar em todas as provas do plano que ainda não têm escopo."""
    estados = carregar_provas()
    termos  = termos_str()

    ids = [p[0] for p in PLANO] if not args.id else [args.id]

    ok = falhou = pulado = 0
    for prova_id in ids:
        estado = estados.get(prova_id, "—")

        # Precisa estar extraida e ter o arquivo de extraidos
        if estado not in ("extraida", "classificada"):
            print(f"[SKIP]   {prova_id} (estado={estado})")
            pulado += 1
            continue

        if not tem_extraido(prova_id):
            print(f"[SKIP]   {prova_id} (sem extraidos/{prova_id}.jsonl)")
            pulado += 1
            continue

        if tem_escopo(prova_id) and not args.force:
            n = contar_itens(ESCOPO_DIR / f"{prova_id}.jsonl")
            print(f"[JÁ OK]  {prova_id} (escopo já existe: {n} itens)")
            pulado += 1
            continue

        print(f"[FILTR]  {prova_id} ...", end=" ", flush=True)
        out, err, rc = banco("prova", "filtrar", prova_id, "--termos", termos)
        if rc == 0:
            n = contar_itens(ESCOPO_DIR / f"{prova_id}.jsonl")
            print(f"OK — {n} itens → escopo/{prova_id}.jsonl")
            ok += 1
        else:
            print(f"ERRO rc={rc}")
            if err:
                print(f"         {err[:200]}")
            falhou += 1

    print(f"\nFiltro: ok={ok}, falhou={falhou}, pulado={pulado}")
    if ok:
        print("\nPróximo passo: classificar os escopos gerados com o agente Claude.")
        print("  → python3 onda2.py --status   para ver quais precisam de classificação")


def cmd_persistir(args):
    """Faz merge escopo+classificacao e persiste no banco para provas já classificadas."""
    ids = [p[0] for p in PLANO] if not args.id else [args.id]

    ok = falhou = pulado = 0
    total_inseridas = 0

    for prova_id in ids:
        if not tem_escopo(prova_id):
            pulado += 1
            continue
        if not tem_classificacao(prova_id):
            pulado += 1
            continue

        print(f"[MERGE]  {prova_id} ...", end=" ", flush=True)
        sucesso, msg = merge_e_persiste(prova_id)
        if sucesso:
            print(f"OK — {msg}")
            # Extrai número de inseridas
            for tok in msg.split():
                tok = tok.replace("inseridas≈", "").replace(",", "")
                if tok.isdigit():
                    total_inseridas += int(tok)
                    break
            ok += 1
        else:
            print(f"FALHOU — {msg}")
            falhou += 1

    print(f"\nPersistência: ok={ok}, falhou={falhou}, pulado={pulado}")
    if total_inseridas:
        print(f"Questões inseridas (estimativa): ~{total_inseridas}")
        print("\nVerificando cobertura atualizada...")
        banco("edital", "lacunas", capture=False)


def cmd_plano(args):
    """Mostra o plano sem executar nada."""
    print("\n=== PLANO ONDA 2 ===")
    print(f"{'#':>3}  {'nota':>5}  {'prova_id':<52}  descrição")
    print("-" * 100)
    for i, (pid, nota, desc) in enumerate(PLANO, 1):
        print(f"{i:>3}  {nota:>5}  {pid:<52}  {desc}")

    print(f"\nTotal: {len(PLANO)} provas no plano")
    print(f"Termos de filtro: {len(TODOS_TERMOS)} termos")
    print("\nUso:")
    print("  python3 onda2.py --status      # situação atual")
    print("  python3 onda2.py --filtrar     # gera escopo com prova filtrar")
    print("  python3 onda2.py --persistir   # persiste provas já classificadas")
    print("  python3 onda2.py --id ID --filtrar    # opera só nessa prova")


def cmd_instrucao_classificador(args):
    """Imprime a instrução completa para o agente classificador."""
    estados = carregar_provas()
    ids = [p[0] for p in PLANO] if not args.id else [args.id]

    para_classify = [
        pid for pid in ids
        if tem_escopo(pid) and not tem_classificacao(pid)
    ]

    if not para_classify:
        print("Nenhuma prova precisa de classificação agora.")
        print("Rode --filtrar primeiro ou --status para verificar.")
        return

    for prova_id in para_classify[:3]:  # máximo 3 por vez para não sobrecarregar
        n = contar_itens(ESCOPO_DIR / f"{prova_id}.jsonl")
        print(f"\n{'='*70}")
        print(f"CLASSIFICAR: {prova_id}  ({n} itens)")
        print(f"{'='*70}")
        print(f"""
Skill: classificacao-itens-cebraspe
Prova: {prova_id}
Itens: escopo/{prova_id}.jsonl
Saída: classificacoes/{prova_id}.jsonl

Instrução ao agente:
  Leia cada item de escopo/{prova_id}.jsonl.
  Para cada item, classifique conforme o programa.json do concurso ativo.
  Campos obrigatórios na saída:
    item, edital (código P3·XXX N.N ou FORA), nucleo_id, nucleo_texto,
    nivel (fácil/médio/difícil), confianca (0-1), padrao (descrição curta da pegadinha)

  Após salvar classificacoes/{prova_id}.jsonl, rode:
    python3 banco.py prova estado {prova_id} classificada
    python3 onda2.py --id {prova_id} --persistir
""")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(
        description="Onda 2 — classificação das top provas TI para CGU/AFFC 2026"
    )
    p.add_argument("--status",    action="store_true", help="Mostra situação atual")
    p.add_argument("--filtrar",   action="store_true", help="Roda prova filtrar")
    p.add_argument("--persistir", action="store_true", help="Merge + add-json das classificadas")
    p.add_argument("--instrucao", action="store_true", help="Imprime instrução para o classificador")
    p.add_argument("--id",        default=None,        help="Operar só nessa prova")
    p.add_argument("--force",     action="store_true", help="Refaz mesmo se já existe")
    args = p.parse_args()

    # Default: mostra o plano
    if not any([args.status, args.filtrar, args.persistir, args.instrucao]):
        cmd_plano(args)
        return

    if args.status:
        cmd_status(args)
    if args.filtrar:
        cmd_filtrar(args)
    if args.persistir:
        cmd_persistir(args)
    if args.instrucao:
        cmd_instrucao_classificador(args)


if __name__ == "__main__":
    main()
