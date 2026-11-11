#!/usr/bin/env python3
"""Experimento 10/11/2026: classificador P2 treinado nos 679 rotulos cegos (p2-verif-1).
Resultado (CV 5-fold, TF-IDF + Naive Bayes puro-Python, detector binario + assunto):
  binario P2xOUTRO: precisao 0.69, recall 0.56
  assunto nos 210 positivos: top1 0.50, top3 0.73
  triagem combinada: precisao de assunto 0.41 (tudo) a 0.64 (margem alta, cobertura 8%)
Conclusao: muito melhor que a triagem lexica (13%), mas longe do gate de 85%.
Com ~10 positivos por assunto nao ha sinal para 85%; o gate de P2 so passa com
centenas de rotulos positivos novos ou decisao de relaxar a regra (como P1).
Reproducao: montar /tmp/ds-p2.json a partir de amostras/p2-verif-1-mapa.jsonl +
classificacoes/p2-verif-1-*.jsonl + enunciados dos escopos, e rodar a CV deste arquivo.
"""
