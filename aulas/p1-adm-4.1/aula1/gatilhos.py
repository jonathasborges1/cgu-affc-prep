"""Wrapper da aula: usa aulas/_template/gatilhos_lib.py com as regras de gatilhos.json desta pasta."""
import sys
from pathlib import Path
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D.parent.parent/'_template'))
import gatilhos_lib as _g
def aplicar(s): return _g.aplicar(s,D)
