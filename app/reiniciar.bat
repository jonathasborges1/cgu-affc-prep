@echo off
chcp 65001 >nul
rem Pede ao app para reiniciar (ele reabre na mesma janela). Se nao estiver rodando, abre o iniciar.bat.
powershell -NoProfile -Command "try { Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8787/api/reiniciar -Body {} | Out-Null; exit 0 } catch { exit 1 }"
if errorlevel 1 start "CGU Treino" "%~dp0iniciar.bat"
