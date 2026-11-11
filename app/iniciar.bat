@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python nao encontrado. Instale com:  winget install Python.Python.3.12
  pause
  exit /b 1
)
set CGU_LOOP=1
set ARGS=
title CGU Treino
:run
echo Iniciando CGU Treino... (feche esta janela para encerrar)
python servidor.py %ARGS%
rem codigo 3 = reinicio pedido pelo app: reabre na mesma janela, sem abrir outra aba do navegador
if %errorlevel%==3 (
  set ARGS=--sem-navegador
  goto run
)
if %errorlevel% neq 0 pause
