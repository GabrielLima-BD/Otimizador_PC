@echo off
title 🔥 CONSTRUINDO OTIMIZADOR PC AMD BEAST v2.0
color 0A

echo.
echo ================================================================
echo 🔥 CONSTRUINDO OTIMIZADOR PC AMD BEAST v2.0
echo ================================================================
echo.
echo 🚀 Gerando executável com todas as otimizações AMD...
echo.

REM Verificar se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  PyInstaller não encontrado. Instalando...
    pip install pyinstaller
)

echo 🔧 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist\OtimizadorPC_AMD_Beast_v2.0.exe" del "dist\OtimizadorPC_AMD_Beast_v2.0.exe"

echo 🚀 Construindo executável...
pyinstaller --clean OtimizadorPC_AMD_Beast_v2.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo ✅ EXECUTÁVEL CRIADO COM SUCESSO!
    echo ================================================================
    echo.
    echo 📁 Localização: dist\OtimizadorPC_AMD_Beast_v2.0.exe
    echo 📏 Tamanho: 
    dir "dist\OtimizadorPC_AMD_Beast_v2.0.exe" | findstr "OtimizadorPC_AMD_Beast_v2.0.exe"
    echo.
    echo 🔥 NOVIDADES DA v2.0:
    echo   • MODO AMD BEAST específico para Ryzen + Radeon
    echo   • Otimizações gaming extremas
    echo   • HPET disabled para AMD
    echo   • ULPS off para Radeon
    echo   • Power plans AMD otimizados
    echo   • Network latency redução extrema
    echo   • Timer resolution otimizado
    echo.
    echo 🎮 PRONTO PARA USO!
    echo.
) else (
    echo.
    echo ================================================================
    echo ❌ ERRO NA CONSTRUÇÃO!
    echo ================================================================
    echo.
    echo Verifique os erros acima e tente novamente.
    echo.
)

pause