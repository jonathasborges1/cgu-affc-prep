#!/usr/bin/env python3
"""
Persiste lotes temáticos P1/P2 (e opcionalmente P3) que têm
escopo (ou extraidos/) + classificações prontas.
"""
import os, sys, json, subprocess, argparse
from pathlib import Path

CONC_DIR = Path("concursos/cgu-affc-ti-ds")
CLASDIR  = CONC_DIR / "classificacoes"
ESCDIR   = CONC_DIR / "escopo"
EXTDIR   = Path("extraidos")

OBRIG = ['banca','ano','ref','url','url_gab','item','enunciado','gabarito','tema']


def lerj(path):
    items = []
    if not Path(path).exists():
        return items
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except Exception:
                    pass
    return items


def banco_add_json(tmp_path, dry_run=False):
    if dry_run:
        items = lerj(tmp_path)
        return True, f"[DRY-RUN] {len(items)} itens prontos para inserir"
    result = subprocess.run(
        ["python3", "-I", "banco.py", "add-json", str(tmp_path)],
        capture_output=True, text=True,
        env={**os.environ, "BANCO_DIR": "concursos/cgu-affc-ti-ds"}
    )
    out = result.stdout.strip()
    err = result.stderr.strip()
    if result.returncode != 0:
        return False, f"add-json falhou (rc={result.returncode}): {err[:200]}"
    return True, out


def merge_e_persiste(lote_id, dry_run=False):
    escopo_path  = ESCDIR  / f"{lote_id}.jsonl"
    extrai_path  = EXTDIR  / f"{lote_id}.jsonl"
    classif_path = CLASDIR / f"{lote_id}.jsonl"

    src_path = escopo_path if escopo_path.exists() else extrai_path
    src_name = "escopo" if escopo_path.exists() else "extraido"

    if not src_path.exists():
        return False, "sem escopo nem extraido"
    if not classif_path.exists():
        return False, "sem classificacao"

    escopo = {}
    for e in lerj(src_path):
        escopo[str(e["item"])] = e

    classif = {}
    for c in lerj(classif_path):
        classif[str(c["item"])] = c

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
            "prova_id":   lote_id,
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
            "edital":     edital,
            "subtema":    c.get("nucleo_texto", ""),
            "nivel":      c.get("nivel", ""),
            "padrao":     c.get("padrao", ""),
            "tags":       c.get("tags", []),
            "nucleos":    [c["nucleo_id"]] if c.get("nucleo_id") else [],
            "fonte":      f"oficial-{lote_id}",
            "peso_prova": 1.0,
            "base_legal": c.get("base_legal", ""),
        }
        merged.append(m)

    if not merged:
        return False, f"nenhum item aproveitável (pulados={pulados}, src={src_name})"

    tmp = Path("/tmp") / f"lote_merge_{lote_id}.jsonl"
    with open(tmp, "w") as f:
        for m in merged:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    ok, msg = banco_add_json(tmp, dry_run=dry_run)
    if not dry_run:
        tmp.unlink(missing_ok=True)

    return ok, f"src={src_name} merged={len(merged)} pulados={pulados} | {msg}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--prefixo", default="")
    p.add_argument("--tudo", action="store_true")
    p.add_argument("--id", default="")
    args = p.parse_args()

    if args.id:
        lotes = [args.id]
    else:
        lotes = []
        for fname in sorted(os.listdir(str(CLASDIR))):
            if not (fname.startswith("tema-p") and fname.endswith(".jsonl")):
                continue
            base = fname[:-6]
            if args.prefixo and not base.startswith(args.prefixo):
                continue
            if not args.tudo and base.startswith("tema-p3"):
                continue
            has_src = (ESCDIR / fname).exists() or (EXTDIR / fname).exists()
            has_cls = (CLASDIR / fname).exists()
            if has_src and has_cls:
                lotes.append(base)

    if not lotes:
        print("Nenhum lote encontrado.")
        return

    print(f"{'ID':<45} {'resultado'}")
    print("-" * 90)

    total_ok = total_err = 0
    for lote_id in lotes:
        ok, msg = merge_e_persiste(lote_id, dry_run=args.dry_run)
        status = "OK " if ok else "ERR"
        print(f"[{status}] {lote_id:<43} {msg}")
        if ok:
            total_ok += 1
        else:
            total_err += 1

    print("-" * 90)
    print(f"Total: {total_ok} OK, {total_err} erros")


if __name__ == "__main__":
    main()
