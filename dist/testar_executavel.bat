@echo off
echo ================================
echo   TESTE DO EXECUTAVEL CRIADO
echo ================================
echo.

cd /d "%~dp0"

echo Verificando se o arquivo existe...
if exist "OtimizadorPC_Gaming.exe" (
    echo ✅ OtimizadorPC_Gaming.exe encontrado!
    echo.
    
    echo Tamanho do arquivo:
    dir OtimizadorPC_Gaming.exe | find ".exe"
    echo.
    
    echo ⚠️  Para testar o executável:
    echo 1. Execute como Administrador
    echo 2. Clique duas vezes em OtimizadorPC_Gaming.exe
    echo 3. A interface deve abrir com as abas Gaming e Otimização
    echo.
    
    echo 🎯 Funcionalidades para testar:
    echo - Aba Gaming: Buscar Jogos Instalados
    echo - Aba Otimização: Verificar Sistema
    echo - Aba Monitoramento: Ver uso de recursos
    echo - Aba Agendamento: Configurar tarefas
    echo.
    
    pause
    
) else (
    echo ❌ Arquivo OtimizadorPC_Gaming.exe não encontrado!
    echo Algo deu errado na criação do executável.
    pause
)