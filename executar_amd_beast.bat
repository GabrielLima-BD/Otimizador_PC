@echo off
title 🔥 OTIMIZADOR PC - TESTE AMD BEAST MODE
color 0C

echo.
echo ================================================================
echo 🔥 OTIMIZADOR PC - TESTE OTIMIZAÇÕES AMD EXTREMAS
echo ================================================================
echo.
echo 🚀 Este script aplicará otimizações EXTREMAS para hardware AMD:
echo.
echo ✅ INCLUÍDO:
echo   • AMD Ryzen Power Plans otimizados
echo   • AMD Radeon: ULPS OFF, sem throttling
echo   • HPET desabilitado (reduz latência)
echo   • Memory timings AMD otimizados
echo   • CPU: 100%% performance constante
echo   • Network: Latência extremamente reduzida
echo   • Gaming: Prioridades e configurações extremas
echo.
echo 🎤 ÁUDIO: Sempre protegido (microfone seguro)
echo.
echo ⚠️  ATENÇÃO: APENAS PARA HARDWARE AMD!
echo ⚠️  Recomendado reiniciar após execução
echo.
echo ================================================================

pause

echo.
echo 🚀 Executando otimizações AMD...
echo.

python test_amd_optimizations.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo ✅ OTIMIZAÇÕES AMD APLICADAS COM SUCESSO!
    echo ================================================================
    echo.
    echo 💪 Seu sistema AMD foi otimizado para máxima performance!
    echo.
    echo 🎮 RECOMENDAÇÕES:
    echo   • Reinicie o sistema agora
    echo   • Teste seus jogos favoritos
    echo   • Monitore temperaturas
    echo.
    echo 📊 RESULTADOS ESPERADOS:
    echo   • Maior FPS em jogos
    echo   • Menor latência de entrada
    echo   • Resposta mais rápida do sistema
    echo   • Melhor performance geral
    echo.
) else (
    echo.
    echo ================================================================
    echo ❌ ERRO NA EXECUÇÃO!
    echo ================================================================
    echo.
    echo Verifique os logs na pasta 'logs' para mais detalhes.
    echo.
)

echo.
echo Pressione qualquer tecla para continuar...
pause >nul