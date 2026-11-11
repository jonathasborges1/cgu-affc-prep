@echo off
chcp 65001 >nul
set PORTA=8787
set ACHOU=0
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /R /C:":%PORTA% .*LISTENING"') do (
  taskkill /F /T /PID %%p >nul 2>nul
  set ACHOU=1
)
if "%ACHOU%"=="1" (echo CGU Treino encerrado.) else (echo Nenhum app rodando na porta %PORTA%.)
timeout /t 2 >nul
