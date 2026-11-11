#!/usr/bin/env python3
"""Registra um evento no fluxo do app (aba Workflow). Uso pelo Claude e pelos scripts.
Exemplos:
  python scripts/evento.py --etapa 4 --lote tema-p1-adm-4-1-a --feito 12 --total 40 "classificando itens"
  python scripts/evento.py --etapa 5 --nivel ok --fonte claude "verificação concluída"
Também como biblioteca: from evento import evento; evento('mensagem', etapa=3)"""
import json, sys, time, datetime, argparse
from pathlib import Path
EVT = Path(__file__).resolve().parent.parent / 'logs' / 'eventos.jsonl'

def evento(msg, etapa=None, nivel='info', fonte='script', lote=None, feito=None, total=None):
    t = time.time()
    ev = {'t': round(t, 2), 'h': datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S'), 'etapa': etapa,
          'nivel': nivel, 'fonte': fonte, 'msg': str(msg).replace('\n', ' ')[:300]}
    if lote: ev['lote'] = lote
    if feito is not None: ev['feito'] = feito
    if total is not None: ev['total'] = total
    EVT.parent.mkdir(exist_ok=True)
    with open(EVT, 'a', encoding='utf-8') as f: f.write(json.dumps(ev, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('msg')
    ap.add_argument('--etapa', type=int); ap.add_argument('--nivel', default='info', choices=['info', 'ok', 'aviso', 'erro'])
    ap.add_argument('--fonte', default='claude'); ap.add_argument('--lote'); ap.add_argument('--feito', type=int); ap.add_argument('--total', type=int)
    a = ap.parse_args(); evento(a.msg, a.etapa, a.nivel, a.fonte, a.lote, a.feito, a.total)
