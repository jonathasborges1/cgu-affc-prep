#!/usr/bin/env python3
"""Mede a calibração cega de P1/P2/P3 sem liberar bloco incompleto."""
import argparse
import glob
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
C = BASE / "concursos" / "cgu-affc-ti-ds"


def lerj(path):
    try:
        return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    except FileNotFoundError:
        return []


def assunto(codigo):
    if not codigo or codigo == "OUTRO":
        return "OUTRO"
    # O acervo legado contém o separador tanto correto (·) quanto com mojibake (Â·).
    codigo = codigo.replace("Â·", "·")
    m = re.match(r"(P[123]·[A-Z]+ \d+)", codigo)
    return m.group(1) if m else codigo


def ano(prova_id):
    m = re.search(r"(20\d{2})", prova_id or "")
    return int(m.group(1)) if m else None


def avaliar(bloco):
    prefixo = bloco.lower() + "-verif-1"
    mapa_lista = lerj(C / "amostras" / (prefixo + "-mapa.jsonl"))
    mapa = {x["id"]: x for x in mapa_lista}
    rotulos = {}
    duplicados = []
    for nome in sorted(glob.glob(str(C / "classificacoes" / (prefixo + "-*.jsonl")))):
        for item in lerj(nome):
            iid = item.get("id")
            if iid in rotulos:
                duplicados.append(iid)
            if iid in mapa:
                rotulos[iid] = item

    linhas = []
    por_triagem = Counter(x["triagem"] for x in mapa_lista)
    rotulados_por_triagem = Counter()
    acertos_por_triagem = Counter()
    for iid, rotulo in rotulos.items():
        m = mapa[iid]
        previsto = assunto(m.get("triagem"))
        real = assunto(rotulo.get("codigo"))
        rotulados_por_triagem[previsto] += 1
        if previsto == real:
            acertos_por_triagem[previsto] += 1
        linhas.append({"id": iid, "ano": ano(m.get("prova_id")), "previsto": previsto, "real": real})

    por_assunto = {}
    for cod, total in sorted(por_triagem.items()):
        n = rotulados_por_triagem[cod]
        por_assunto[cod] = {
            "amostra": total,
            "rotulados": n,
            "acertos": acertos_por_triagem[cod],
            "precisao": acertos_por_triagem[cod] / n if n else None,
            "completo": n == total,
        }

    n = len(linhas)
    acertos = sum(x["previsto"] == x["real"] for x in linhas)
    folds = []
    anos = sorted({x["ano"] for x in linhas if x["ano"]})
    for corte in anos:
        treino = [x for x in linhas if x["ano"] and x["ano"] < corte and x["real"] != "OUTRO"]
        teste = [x for x in linhas if x["ano"] == corte and x["real"] != "OUTRO"]
        if len(treino) < 80 or len(teste) < 15:
            continue
        top5 = {c for c, _ in Counter(x["real"] for x in treino).most_common(5)}
        recall = sum(x["real"] in top5 for x in teste) / len(teste)
        folds.append({"ano_teste": corte, "treino": len(treino), "teste": len(teste), "recall_top5": recall})

    itens_teste = sum(x["teste"] for x in folds)
    recall_top5 = (
        sum(x["recall_top5"] * x["teste"] for x in folds) / itens_teste if itens_teste else None
    )
    completo = len(rotulos) == len(mapa) and all(x["completo"] for x in por_assunto.values())
    precisao = acertos / n if n else None
    gates = {
        "amostra_completa": completo,
        "sem_duplicados": not duplicados,
        "precisao_minima_0_85": precisao is not None and precisao >= 0.85,
        "tres_folds_temporais": len(folds) >= 3,
        "recall_top5_minimo_0_75": recall_top5 is not None and recall_top5 >= 0.75,
    }
    return {
        "bloco": bloco,
        "amostra": len(mapa),
        "rotulados": len(rotulos),
        "progresso": len(rotulos) / len(mapa) if mapa else 0,
        "acertos_triagem": acertos,
        "precisao_triagem_parcial": precisao,
        "duplicados": sorted(set(duplicados)),
        "por_assunto": por_assunto,
        "backtest_temporal": {"folds": folds, "recall_top5": recall_top5, "itens_teste": itens_teste},
        "gates": gates,
        "confiavel": all(gates.values()),
        "aviso": "Métricas parciais não liberam prioridade." if not completo else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bloco", choices=("P1", "P2", "P3"))
    args = ap.parse_args()
    resultado = avaliar(args.bloco)
    destino = BASE / "docs" / ("calibracao-" + args.bloco.lower() + ".json")
    destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
