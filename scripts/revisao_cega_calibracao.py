#!/usr/bin/env python3
"""Prepara e valida pacotes de revisao cega para calibracao de P2/P3.

O pacote nunca expoe codigo_predito, estrato ou peso amostral. Os rotulos sao
gravados em arquivo separado e so sao incorporados depois que todos os IDs
forem preenchidos com um codigo de nivel 1 do bloco ou OUTRO.
"""
import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def ler_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def taxonomia(bloco):
    programa = ler_jsonl(BASE / "concursos" / "cgu-affc-ti-ds" / "programa.json")
    return [x for x in programa if x.get("prova") == bloco and x.get("nivel") == 1]


def preparar(args):
    itens = ler_jsonl(args.amostra)
    if not itens:
        raise SystemExit("amostra vazia")
    bloco = itens[0].get("bloco")
    if bloco not in ("P2", "P3") or any(x.get("bloco") != bloco for x in itens):
        raise SystemExit("a amostra deve conter um unico bloco P2 ou P3")
    ids = [x["id"] for x in itens]
    if len(ids) != len(set(ids)):
        raise SystemExit("IDs duplicados na amostra")

    outdir = Path(args.saida)
    outdir.mkdir(parents=True, exist_ok=True)
    rotulos = {iid: None for iid in ids}
    (outdir / "rotulos.json").write_text(json.dumps(rotulos, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "manifesto.json").write_text(
        json.dumps({"amostra": str(Path(args.amostra)), "bloco": bloco, "ids": ids}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    tamanho = max(1, args.tamanho)
    for inicio in range(0, len(itens), tamanho):
        lote = itens[inicio:inicio + tamanho]
        numero = inicio // tamanho + 1
        linhas = [
            f"# Revisao cega {bloco} — lote {numero}",
            "",
            "Classifique cada item sem consultar a previsao original. Use um codigo abaixo ou OUTRO.",
            "",
            "## Taxonomia",
            "",
        ]
        linhas += [f"- `{x['codigo']}` — {x['texto']}" for x in taxonomia(bloco)]
        linhas += ["", "## Itens", ""]
        for x in lote:
            texto = " ".join(str(x.get("enunciado") or "").split())
            linhas += [f"### {x['id']}", "", texto, "", "Rótulo: `PREENCHER`", ""]
        (outdir / f"lote-{numero:02d}.md").write_text("\n".join(linhas), encoding="utf-8")
    print(json.dumps({"bloco": bloco, "itens": len(itens), "lotes": (len(itens) + tamanho - 1) // tamanho,
                      "saida": str(outdir)}, ensure_ascii=False))


def aplicar(args):
    manifesto = json.loads((Path(args.pacote) / "manifesto.json").read_text(encoding="utf-8"))
    rotulos = json.loads((Path(args.pacote) / "rotulos.json").read_text(encoding="utf-8"))
    ids = manifesto["ids"]
    if set(rotulos) != set(ids):
        raise SystemExit("rotulos.json nao cobre exatamente os IDs do manifesto")
    validos = {x["codigo"] for x in taxonomia(manifesto["bloco"])} | {"OUTRO"}
    invalidos = {iid: rotulos[iid] for iid in ids if rotulos[iid] not in validos}
    if invalidos:
        raise SystemExit(f"rotulos ausentes ou invalidos: {len(invalidos)}")
    amostra = ler_jsonl(manifesto["amostra"])
    por_id = {x["id"]: x for x in amostra}
    for iid in ids:
        por_id[iid]["codigo_real"] = rotulos[iid]
    Path(args.saida).write_text(
        "".join(json.dumps(por_id[iid], ensure_ascii=False) + "\n" for iid in ids), encoding="utf-8"
    )
    print(json.dumps({"itens": len(ids), "saida": args.saida}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preparar")
    p.add_argument("amostra")
    p.add_argument("--saida", required=True)
    p.add_argument("--tamanho", type=int, default=20)
    p.set_defaults(func=preparar)
    p = sub.add_parser("aplicar")
    p.add_argument("pacote")
    p.add_argument("--saida", required=True)
    p.set_defaults(func=aplicar)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
