#!/usr/bin/env python3
"""Compatibilidade: gera amostras cegas v2 aleatorias e estratificadas.

Use --n e --seed para tornar o sorteio reproduzivel. Os arquivos da primeira
rodada sao preservados; os novos lotes recebem o sufixo `v2`.
"""
import argparse
from gerar_amostra_cega_v2 import generate


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=60)
    parser.add_argument('--seed', type=int, default=20261109)
    args = parser.parse_args()
    for block in ('P2', 'P3'):
        generate(block, args.n, args.seed)
