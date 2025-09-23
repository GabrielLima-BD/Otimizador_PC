@echo off
title Criando Executavel Unico - Otimizador PC Gaming
cls

echo.
echo =====================================
echo   CRIANDO EXECUTAVEL UNICO
echo   OTIMIZADOR PC GAMING v2.0
echo =====================================
echo.

echo [1/4] Instalando PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Criando executavel unico...
pyinstaller --onefile --windowed --name="OtimizadorPC_Gaming" --distpath=dist --workpath=build --clean main_gaming.py

echo.
echo [3/4] Verificando resultado...
if exist "dist\OtimizadorPC_Gaming.exe" (
    echo ✅ EXECUTAVEL CRIADO COM SUCESSO!
    echo.
    echo 📁 Local: dist\OtimizadorPC_Gaming.exe
    dir "dist\OtimizadorPC_Gaming.exe"
    echo.
    echo [4/4] Criando arquivo de informacoes...
    
    echo 🎮 OTIMIZADOR PC GAMING v2.0 > dist\LEIA-ME.txt
    echo ============================ >> dist\LEIA-ME.txt
    echo. >> dist\LEIA-ME.txt
    echo 📁 ARQUIVO UNICO PORTAVEL >> dist\LEIA-ME.txt
    echo - Nao precisa instalacao >> dist\LEIA-ME.txt
    echo - Funciona em qualquer PC Windows 10/11 >> dist\LEIA-ME.txt
    echo - Contem todas as funcionalidades >> dist\LEIA-ME.txt
    echo. >> dist\LEIA-ME.txt
    echo 🚀 FUNCIONALIDADES: >> dist\LEIA-ME.txt
    echo ✅ Busca de jogos Steam, Epic, Ubisoft, Rockstar >> dist\LEIA-ME.txt
    echo ✅ Lancamento otimizado de jogos >> dist\LEIA-ME.txt
    echo ✅ Otimizacoes avancadas do sistema >> dist\LEIA-ME.txt
    echo ✅ Configuracao de autostart >> dist\LEIA-ME.txt
    echo ✅ Dashboard de monitoramento >> dist\LEIA-ME.txt
    echo. >> dist\LEIA-ME.txt
    echo 📱 COMO USAR: >> dist\LEIA-ME.txt
    echo 1. Execute OtimizadorPC_Gaming.exe como administrador >> dist\LEIA-ME.txt
    echo 2. Use a interface completa! >> dist\LEIA-ME.txt
    
    echo.
    echo ✨ BUILD COMPLETO!
    echo 🚀 Arquivo pronto para distribuicao em: dist\
    echo.
    echo Abrindo pasta...
    explorer dist
) else (
    echo ❌ ERRO: Executavel nao foi criado
    echo Verifique se todos os arquivos estao presentes
)

echo.
pause