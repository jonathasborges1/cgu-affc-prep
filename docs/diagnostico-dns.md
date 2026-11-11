# Diagnóstico de DNS da descoberta

## Resultado

Em 10/11/2026, o processo restrito não conseguiu resolver `apis.cebraspe.org.br`:

- Python/urllib: `getaddrinfo failed`.
- `curl.exe`: `Could not resolve host`.
- `urllib.request.getproxies()`: nenhum proxy configurado.
- A mesma API respondeu HTTP 200 quando a chamada foi executada com acesso de rede autorizado fora do isolamento.

Conclusão: o domínio e a resolução DNS externa estão operacionais. A falha é a ausência de DNS/saída de rede no ambiente restrito de execução. Alterar o DNS global do Windows não corrige a política de rede do processo e pode afetar outras conexões.

## Solução aplicada nesta execução

A coleta foi executada com acesso de rede autorizado: `python scripts/descobrir.py catalogo --tempo 90 --ano-min 2021` terminou com sucesso e confirmou 458 eventos em cache (0 novos; 319 dentro do filtro do concurso/ano). Isso comprova que o endpoint está acessível quando o processo recebe a rota de rede apropriada.

O orquestrador agora identifica erros comuns de resolução e informa a causa e a ação correta, sem recomendar trocar DNS do Windows.

## Correção persistente do ambiente

Permitir DNS e HTTPS de saída para o processo que executa o app, ou configurar um proxy HTTPS aprovado e disponibilizá-lo nas variáveis `HTTPS_PROXY`/`HTTP_PROXY`. Destinos necessários à descoberta:

- `apis.cebraspe.org.br:443` (catálogo de eventos)
- `cdn.cebraspe.org.br:443` (PDFs públicos de prova e gabarito)

Depois de liberar a rota, validar com `python scripts/descobrir.py catalogo --tempo 90 --ano-min 2021`. Não é necessário trocar os servidores DNS do adaptador do Windows.

## Comportamento atual

O cache local de catálogo e ranking continua utilizável sem rede. Downloads novos ficam indisponíveis no modo restrito. Não usar IP fixo como contorno: os endereços podem mudar e isso quebra TLS/roteamento.
