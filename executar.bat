@echo off
title Otimizador Windows 10 Pro

:: Verifica se está executando como administrador
net session >nul 2>&1
if not %errorLevel% == 0 (
    echo.
    echo ⚠️  AVISO: Execute como Administrador para obter todos os recursos!
    echo.
    echo 🔄 Clique com botão direito neste arquivo e selecione:
    echo    "Executar como administrador"
    echo.
    pause
    exit /b 1
)

:: Muda para o diretório do script
cd /d "%~dp0"

:: Executa o otimizador
echo.
echo 🚀 Iniciando Otimizador Windows 10 Pro...
echo.
python main.py

:: Pausa se houve erro
if errorlevel 1 (
    echo.
    echo ❌ Houve um erro na execução
    pause
)