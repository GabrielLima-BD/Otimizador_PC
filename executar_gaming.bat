@echo off
title Otimizador Windows 10 Pro - Gaming Edition
echo.
echo ======================================
echo   OTIMIZADOR WINDOWS 10 PRO
echo      GAMING EDITION v2.0
echo ======================================
echo.
echo Escolha uma opcao:
echo.
echo [1] Executar Interface Gaming (Recomendado)
echo [2] Executar Interface Avancada Original  
echo [3] Executar Interface Basica
echo [4] Executar Testes Gaming
echo [5] Executar Testes Completos
echo [6] Escanear Jogos (Console)
echo [7] Configurar Autostart
echo [0] Sair
echo.
set /p choice="Digite sua opcao (0-7): "

if "%choice%"=="1" goto gaming
if "%choice%"=="2" goto advanced
if "%choice%"=="3" goto basic
if "%choice%"=="4" goto test_gaming
if "%choice%"=="5" goto test_complete
if "%choice%"=="6" goto scan_games
if "%choice%"=="7" goto autostart
if "%choice%"=="0" goto exit
goto invalid

:gaming
echo.
echo Iniciando Interface Gaming...
python main_gaming.py
goto end

:advanced
echo.
echo Iniciando Interface Avancada...
python main_advanced.py
goto end

:basic
echo.
echo Iniciando Interface Basica...
python main.py
goto end

:test_gaming
echo.
echo Executando Testes Gaming...
python test_gaming.py
pause
goto menu

:test_complete
echo.
echo Executando Testes Completos...
python test_advanced.py
pause
goto menu

:scan_games
echo.
echo Escaneando Jogos...
python -c "from optimizer.game_scanner import GameScanner; scanner = GameScanner(); games = scanner.scan_games(force_rescan=True); print(f'Jogos encontrados: {len(games)}'); [print(f'  {game.name} ({game.launcher})') for game in list(games.values())[:10]]"
pause
goto menu

:autostart
echo.
echo Configurando Autostart...
python -c "from optimizer.autostart import AutostartManager; manager = AutostartManager(); status = manager.get_status(); print(f'Status atual: Registro={status[\"registry_enabled\"]}, Pasta={status[\"startup_folder_enabled\"]}'); choice = input('Habilitar autostart? (s/n): '); manager.enable_autostart('registry', True) if choice.lower() == 's' else manager.disable_autostart('all'); print('Configuracao atualizada!')"
pause
goto menu

:invalid
echo.
echo Opcao invalida! Tente novamente.
pause
goto menu

:exit
echo.
echo Saindo...
exit

:end
echo.
echo Programa finalizado.
pause

:menu
cls
goto start