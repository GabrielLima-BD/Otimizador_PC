#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Build para Executável Único
=====================================

Cria um executável .exe único contendo todo o sistema:
- Interface Gaming completa
- Busca de jogos
- Otimizações
- Autostart
- Dashboard

Uso: python build_exe.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Instala PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller já instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller instalado com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar PyInstaller: {e}")
            return False

def create_spec_file():
    """Cria arquivo .spec personalizado para o build"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Todos os arquivos Python do projeto
a = Analysis(
    ['main_gaming.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('optimizer/*.py', 'optimizer'),
        ('assets', 'assets'),
        ('*.json', '.'),
        ('*.md', '.'),
        ('*.txt', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'psutil',
        'comtypes',
        'winreg',
        'threading',
        'subprocess',
        'json',
        'pathlib',
        'datetime',
        'time',
        'logging',
        'hashlib',
        'dataclasses',
        'typing',
        'tkinter',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.ttk'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OtimizadorPC_Gaming',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Interface gráfica
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    with open('OtimizadorPC.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Arquivo .spec criado")

def build_executable():
    """Constrói o executável"""
    print("🔨 Iniciando build do executável...")
    
    try:
        # Comando PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",  # Arquivo único
            "--windowed",  # Interface gráfica (sem console)
            "--name=OtimizadorPC_Gaming",
            "--distpath=dist",
            "--workpath=build",
            "--clean",
            "OtimizadorPC.spec"
        ]
        
        subprocess.check_call(cmd)
        print("✅ Build concluído com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        return False

def create_installer_info():
    """Cria arquivo de informações do instalador"""
    info_content = """
🎮 OTIMIZADOR PC GAMING v2.0
============================

📁 ARQUIVO ÚNICO PORTÁVEL
- Não precisa instalação
- Funciona em qualquer PC Windows 10/11
- Contém todas as funcionalidades

🚀 FUNCIONALIDADES INCLUÍDAS:
✅ Busca automática de jogos (Steam, Epic, Ubisoft, Rockstar, etc.)
✅ Lançamento otimizado de jogos
✅ Otimizações avançadas do sistema
✅ Configuração de autostart
✅ Dashboard de monitoramento
✅ Limpeza e performance

📱 COMO USAR:
1. Baixe o arquivo OtimizadorPC_Gaming.exe
2. Execute como administrador (recomendado)
3. Use a interface completa!

💾 TAMANHO: ~50-100MB (tudo incluído)
🔒 PORTÁVEL: Não modifica registro/sistema
⚡ RÁPIDO: Executável nativo Windows

Desenvolvido em Python + CustomTkinter
"""
    
    with open('dist/LEIA-ME.txt', 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print("✅ Arquivo de informações criado")

def main():
    """Função principal do build"""
    print("🎮 CONSTRUINDO OTIMIZADOR PC GAMING")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('main_gaming.py'):
        print("❌ Arquivo main_gaming.py não encontrado!")
        print("   Execute este script no diretório do projeto")
        return False
    
    # Instalar PyInstaller
    if not install_pyinstaller():
        return False
    
    # Criar diretório de assets se não existir
    os.makedirs('assets', exist_ok=True)
    
    # Criar arquivo .spec
    create_spec_file()
    
    # Fazer o build
    if not build_executable():
        return False
    
    # Verificar se o executável foi criado
    exe_path = Path('dist/OtimizadorPC_Gaming.exe')
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"🎯 EXECUTÁVEL CRIADO COM SUCESSO!")
        print(f"📁 Local: {exe_path.absolute()}")
        print(f"💾 Tamanho: {size_mb:.1f} MB")
        
        # Criar arquivo de informações
        create_installer_info()
        
        print("✨ BUILD COMPLETO!")
        print("🚀 Agora você pode distribuir o arquivo .exe!")
        return True
    else:
        print("❌ Executável não foi criado")
        return False

if __name__ == "__main__":
    success = main()
    input("\\nPressione Enter para sair...")
    sys.exit(0 if success else 1)