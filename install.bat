@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║               🚀 OTIMIZADOR WINDOWS 10 PRO 🚀                ║
echo ║                    INSTALADOR AUTOMÁTICO                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 Baixe e instale Python 3.7+ em: https://python.org
    echo ✅ Marque a opção "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

:: Atualiza pip
echo 📦 Atualizando pip...
python -m pip install --upgrade pip

:: Instala dependências
echo 📦 Instalando dependências...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Erro ao instalar dependências
    echo 🔄 Tentando instalação individual...
    
    python -m pip install customtkinter==5.2.2
    python -m pip install psutil==5.9.8
    python -m pip install pywin32==306
    python -m pip install requests==2.31.0
    python -m pip install Pillow==10.3.0
)

:: Cria diretórios necessários
echo 📁 Criando diretórios...
if not exist "logs" mkdir logs
if not exist "logs\backups" mkdir logs\backups
if not exist "assets" mkdir assets

echo.
echo ✅ Instalação concluída com sucesso!
echo.
echo 🚀 Para executar o otimizador:
echo    1. Clique com botão direito no Prompt de Comando
echo    2. Selecione "Executar como administrador"
echo    3. Digite: python main.py
echo.
echo ⚠️  IMPORTANTE: Execute sempre como administrador!
echo.
pause