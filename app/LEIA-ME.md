# CGU Treino (MVP)

## Como abrir
1. Duplo clique em `iniciar.bat` (nesta pasta, dentro de `cgu-bd\app`).
2. O navegador abre em http://127.0.0.1:8787. Se não abrir, digite esse endereço.
3. Para encerrar, feche a janela preta.

Precisa de Python 3.10+ (`python --version`). Sem Python: `winget install Python.Python.3.12`.
Não instala nenhum pacote. O servidor só responde neste computador.

## Telas
- **Painel**: itens e núcleos do banco, provas por etapa do workflow, itens por seção do edital, log.
- **Treino**: micro-aulas e cadernos (A definições, B pegadinhas, C mistura). Um item por vez: Certo, Errado ou Em branco.
  Acerto +1, erro −1, branco 0. Cada resposta é gravada na hora. "Refazer meus erros" reabre os itens errados.
  "Atualizar plano" regenera os cadernos a partir do banco.
- **Progresso**: erros por núcleo e por tipo de pegadinha, fila de revisão, últimos dias.
- **Aulas**: abre a aula em HTML (botão "Marcar aula como lida") e o PDF.
- **Banco**: busca por texto, seção do edital, nível e etiqueta.

## Onde ficam os dados
- Progresso: `%LOCALAPPDATA%\cgu-treino\treino.db` (SQLite, fora do OneDrive).
- Espelho legível: `cgu-bd\progresso\respostas.jsonl` (uma linha por resposta) — é o arquivo que o Claude lê para analisar seus erros.
- Banco de questões: lido ao vivo de `cgu-bd\concursos\...` (sem cópia).

## Levar para outro computador
Copie a pasta `cgu-bd` e, se quiser o histórico, `treino.db` para a mesma pasta de dados no outro PC.
