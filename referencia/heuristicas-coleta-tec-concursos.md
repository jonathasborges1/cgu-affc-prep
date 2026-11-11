# Heurísticas de coleta no TEC Concursos (ler ANTES de qualquer consulta ao TEC)

Criado em 04/11/2026 depois do bloqueio da sessão de 02–04/11. Complementa `fluxo-aula-por-engenharia-reversa.md` e `metodo-coleta-cebraspe-chrome.md`.

> **Aviso de honestidade:** os números abaixo (8 s entre requisições, 30 itens por sessão, espera de 2 h) são hipóteses prudentes minhas, derivadas do bloqueio e do script de terceiros. NÃO são limites publicados ou confirmados pelo TEC. Os termos de uso do TEC ainda não foram lidos (a página devolveu 429 e o WebFetch não alcança o domínio).

## O que aconteceu
- Li 620 questões do caderno 107753370 pela API `/api/cadernos/ID/questoes/N` em ~30 s, uma atrás da outra, sem pausa, dentro do navegador logado do Jonathas.
- Resultado: página "Human Verification" (HTTP 405), depois HTTP 429 "Too Many Requests". Mais de 40 min depois, até uma única requisição à página de termos ainda voltava 429. A penalidade dura e vale para a sessão/conta, não só para a rajada.
- Causa provável: volume (620 chamadas), cadência perfeita (nenhuma pausa), sequência 1..N sem relação com navegação humana e chamadas de API sem os parâmetros que a própria tela usa.

## O que aprendi com o script de terceiros (Coletor de Questões, greasyfork 588048, v2.7.6)
Só leitura do código; não foi instalado nem usado.
- Usa a mesma rota de API por questão, mas com o parâmetro `atualizarCronometro=true`, que a própria tela envia, e cabeçalho de requisição XHR.
- Lê o gabarito no próprio JSON da questão (campos como `numeroAlternativaCorreta` / `gabarito`). A confirmar com UMA chamada quando o bloqueio passar.
- Plano B mais barato: a página `/questoes/cadernos/ID/imprimir` (impressão do caderno, recurso do próprio site), com muitas questões e o gabarito numa só requisição, por faixa.
- Versões antigas esperavam 4–8 s entre ações e clicavam na interface em vez de varrer a API.
- Persiste o progresso por caderno, deduplica por id, usa trava para só uma aba coletar e pausa quando a aba fica oculta.
- Fraqueza: a versão atual NÃO trata 429, captcha nem "Human Verification" (só repete 3 vezes com espera curta). Repetir depois de um sinal de bloqueio é o que não devemos fazer.

## Regras (heurísticas) que devo seguir
1. **Termos primeiro.** Antes de qualquer coleta além de ler a tela que o Jonathas está vendo, confirmar o que os termos do TEC permitem (https://www.tecconcursos.com.br/termos-de-uso). Estado em 04/11/2026: não lidos; pendente. Se eu não conseguir abrir, pedir ao Jonathas que abra e cole o trecho sobre coleta automatizada/robôs.
2. **Menos requisições, não só mais devagar.** Preferir o recurso do próprio site (impressão do caderno por faixa) a uma requisição por questão. Nunca varrer um caderno inteiro.
3. **Filtrar antes de ler.** Escolher candidatas por título, ano, órgão e enunciado já exibidos na listagem; ler só as ~15 melhores por tema. Um filtro por tema, nome `CGU-AAAA-MM-Bloco-Tema`, conferindo `docs/tec/tec-cadernos.json` antes de criar outro.
4. **Teto por sessão (hipótese prudente):** no máximo ~30 itens lidos por sessão e 1 sessão por dia.
5. **Cadência (hipótese prudente):** uma requisição por vez (sem paralelismo), mínimo de ~8 s entre requisições, com pequena variação. Nada de lote em loop.
6. **Parar no primeiro sinal.** Ao ver 429, 405, 403, "Human Verification", reCAPTCHA ou título de página estranho: parar tudo, não repetir, não tentar outra rota, avisar o Jonathas e esperar pelo menos ~2 h antes de testar com UMA única requisição.
7. **Sem contornar proteção.** Não resolver captcha ou verificação, não trocar IP, não alterar a identificação do navegador, não usar o cookie de sessão fora do navegador dele.
8. **Dentro do navegador do Jonathas e com os parâmetros da tela.** O estado em JS se perde ao navegar: gravar no banco logo após cada lote pequeno.
9. **Gravar e nunca reler.** Cada item entra no `banco.jsonl` com id da questão do TEC, para deduplicar. Antes de ir ao TEC, buscar no banco.
10. **Cebraspe primeiro.** Texto de item e gabarito definitivo vêm das provas oficiais; o TEC serve para achar temas e ler comentários de professores.
11. **Consentimento por sessão.** Avisar o Jonathas antes de começar uma coleta no TEC e quanto será lido.

## Teste de retomada (quando o bloqueio passar)
1. Esperar ≥ ~2 h, com o Jonathas abrindo o TEC normalmente.
2. UMA requisição `/api/cadernos/107753370/questoes/525?atualizarCronometro=true` e inspecionar os nomes dos campos do JSON (gabarito?). Sem requisição extra.
3. Se o gabarito vier no JSON: coletar as ~15 candidatas, uma a cada ≥ ~8 s, gravando cada uma.
4. Se vier 429/405: parar e avisar.
