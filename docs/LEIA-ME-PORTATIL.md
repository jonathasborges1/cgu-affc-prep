# Kit portátil CGU/AFFC (cópia de 04/11/2026)

Tudo o que o workflow precisa para rodar em outra conta Claude está nesta pasta (`cgu-bd`).

## O que há aqui
| Peça | Onde | O que é |
|---|---|---|
| Dados | `banco.jsonl`, `nucleos.jsonl`, `provas.jsonl` (quando existir) e pastas `extraidos/`, `classificacoes/`, `amostras/`, `verificacoes/` | Estado do trabalho |
| Código | `banco.py` (Python 3, sem instalar nada) | Fiscal e calculadora |
| Roteiro | `ORQUESTRACAO.md`, `docs/workflow-v2.md`, `docs/ARQUIVOS.md` | Como conduzir |
| Agentes | `agentes/*.md` | Instruções do classificador e do verificador |
| Skills | `skills/<nome>/SKILL.md` (3 skills) | Cópias exatas das skills da conta (sincronizadas em 04/11/2026) |
| Apoio | `taxonomia-pegadinhas.md`, `edital-topicos.md` | Etiquetas e códigos do edital |
| Referência | `referencia/*.md` | Docs que estavam só no Projeto (provas, ranking, métodos, bancos) |
| Regras do professor | `docs/INSTRUCOES-DO-PROJETO.md` | Descrição do Projeto, sem o programa do edital |

## Recriar em outra conta (ordem sugerida)
1. **Projeto novo:** crie um Projeto, cole `docs/INSTRUCOES-DO-PROJETO.md` na descrição e acrescente o programa do edital (do Projeto antigo ou do PDF oficial).
2. **Skills:** cadastre as 3 pastas de `skills/` como skills da nova conta. Cada uma é uma pasta com `SKILL.md`; em geral o envio é por um arquivo ZIP da pasta, na área de Skills das configurações (o nome exato do menu pode variar). Alternativa sem instalar: peça ao Claude para ler o `SKILL.md` do `cgu-bd` e segui-lo.
3. **Pasta:** conecte `cgu-bd` à conversa (app desktop) para o Claude ler e gravar os dados.
4. **Docs do Projeto (opcional):** envie os arquivos de `referencia/` e `ORQUESTRACAO.md` ao conhecimento do Projeto, para o Claude consultá-los sem abrir a pasta.
5. **Primeira frase na conversa nova:** "Leia `ORQUESTRACAO.md` em `cgu-bd` e rode `python3 banco.py prova proxima`".

## O que NÃO é portátil
- **Memória do Claude** (preferências e fatos sobre você): fica na conta. As preferências que importam já estão em `docs/INSTRUCOES-DO-PROJETO.md` (aulas em PDF dark mode, fórmulas deduzidas, caderno com no máximo 10 questões, referência e URL por questão, Chrome quando outro acesso falhar).
- **Agentes como "subagentes registrados":** nunca estiveram registrados; o Claude os dispara lendo `agentes/*.md`.
- **Sessões de Chrome, logins e permissões** (TEC, Cebraspe, pasta, apagar arquivos): precisam ser refeitos em cada conta/sessão.
- **Bloqueio do TEC:** é da sua conta no TEC, não do Claude; vale em qualquer conta.

## Observação sobre as cópias
As skills são cópias byte a byte das da conta. Os arquivos de `referencia/` foram regravados a partir do Projeto; mantive o texto, com poucos ajustes de atualização (marcados nos próprios arquivos, ex.: `fluxo-aula-por-engenharia-reversa.md` e `plano-cadernos.md`). Os bancos antigos em partes `.jsonl` do Projeto não foram copiados porque o `banco.jsonl` do PC já os contém.
