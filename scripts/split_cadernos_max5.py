"""Divide cadernos existentes em grupos de no máximo 5 questões.

Preserva a ordem já definida pelo plano/aula; assim, questões próximas no
mesmo núcleo continuam juntas e não misturamos temas artificialmente.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = 5

def split_manifest(path: Path) -> tuple[bool, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    old = data.get("cadernos")
    if not isinstance(old, dict):
        return False, 0
    novo: dict[str, list[str]] = {}
    n = 0
    for _, itens in old.items():
        if not isinstance(itens, list):
            continue
        for i in range(0, len(itens), MAX):
            n += 1
            novo[str(n)] = itens[i:i + MAX]
    if novo == old:
        return False, len(novo)
    data["cadernos"] = novo
    data["caderno"] = [item for grupo in novo.values() for item in grupo]
    data["caderno_limite"] = MAX
    data["cadernos_split"] = True
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return True, len(novo)

def main() -> None:
    alterados = []
    for path in sorted((ROOT / "aulas").glob("**/manifest.json")):
        changed, count = split_manifest(path)
        if changed:
            alterados.append((str(path.relative_to(ROOT)), count))
    print(json.dumps({"limite": MAX, "manifestos_alterados": alterados}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
