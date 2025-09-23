#!/usr/bin/env python3
"""
🚀 Otimizador Windows 10 Pro
============================

Um otimizador completo para Windows 10 que:
- Remove arquivos desnecessários e bloatware
- Otimiza configurações de sistema e rede
- Maximiza o desempenho do PC
- Permite restaurar configurações com segurança

Autor: Sistema de Otimização Inteligente
Versão: 1.0.0
Data: Setembro 2025

IMPORTANTE: Execute como administrador para obter todos os recursos!
"""

import sys
import os
import logging
import traceback
from pathlib import Path

# Adiciona o diretório atual ao path para importações
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from ui import OptimizerUI
    from optimizer.utils import Utils
    import customtkinter as ctk
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")
    print("\n📦 Instalando dependências necessárias...")
    
    import subprocess
    
    # Lista de dependências necessárias
    required_packages = [
        'customtkinter==5.2.2',
        'psutil==5.9.8',
        'pywin32==306', 
        'requests==2.31.0',
        'Pillow==10.3.0'
    ]
    
    for package in required_packages:
        try:
            print(f"Instalando {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar {package}: {e}")
    
    print("✅ Dependências instaladas. Reinicie o programa.")
    input("Pressione Enter para sair...")
    sys.exit(1)

def check_system_requirements():
    """Verifica requisitos do sistema"""
    import platform
    
    # Verifica se é Windows
    if platform.system() != 'Windows':
        print("❌ Este otimizador foi projetado especificamente para Windows 10/11")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Verifica versão do Python
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    print("✅ Requisitos do sistema verificados")

def setup_application():
    """Configura a aplicação"""
    try:
        # Cria diretórios necessários
        directories = ['logs', 'logs/backups', 'assets']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Configura logging
        logger = Utils.setup_logging()
        logger.info("Otimizador Windows 10 Pro iniciado")
        logger.info(f"Sistema: {Utils.get_system_info()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def show_welcome_message():
    """Mostra mensagem de boas-vindas"""
    welcome_text = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                🚀 OTIMIZADOR WINDOWS 10 PRO 🚀                ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  ✨ Maximize o desempenho do seu Windows com segurança       ║
    ║  🧹 Limpeza completa de arquivos desnecessários             ║
    ║  ⚡ Otimização de sistema e rede                             ║
    ║  🔧 Configurações avançadas de registro                     ║
    ║  🔄 Backup e restauração de configurações                   ║
    ║                                                              ║
    ║  ⚠️  IMPORTANTE: Execute como Administrador                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(welcome_text)

def check_admin_privileges():
    """Verifica e solicita privilégios de administrador"""
    if not Utils.is_admin():
        print("\n⚠️  AVISO: Privilégios de administrador necessários!")
        print("Algumas otimizações requerem execução como administrador.")
        
        response = input("\nDeseja tentar executar como administrador? (s/n): ").lower()
        
        if response in ['s', 'sim', 'y', 'yes']:
            print("🔄 Tentando executar como administrador...")
            if Utils.run_as_admin():
                print("✅ Programa será reiniciado como administrador")
                sys.exit(0)
            else:
                print("❌ Não foi possível obter privilégios de administrador")
                print("⚠️  Continuando com privilégios limitados...")
        else:
            print("⚠️  Continuando com privilégios limitados...")
    else:
        print("✅ Executando com privilégios de administrador")

def handle_exception(exc_type, exc_value, exc_traceback):
    """Manipulador global de exceções"""
    if issubclass(exc_type, KeyboardInterrupt):
        print("\n\n⏹️  Programa interrompido pelo usuário")
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Log do erro
    logger = logging.getLogger(__name__)
    logger.error("Exceção não capturada", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Mostra erro para o usuário
    error_msg = f"""
    ❌ ERRO CRÍTICO:
    {exc_type.__name__}: {exc_value}
    
    Verifique o arquivo de log para mais detalhes.
    """
    print(error_msg)
    
    # Salva traceback em arquivo
    with open('logs/crash_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"Crash Report - {Utils.get_system_info()}\n")
        f.write("=" * 50 + "\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
    
    input("\nPressione Enter para sair...")

def main():
    """Função principal"""
    try:
        # Configura manipulador de exceções
        sys.excepthook = handle_exception
        
        # Mostra mensagem de boas-vindas
        show_welcome_message()
        
        # Verifica requisitos
        print("🔍 Verificando requisitos do sistema...")
        check_system_requirements()
        
        # Verifica privilégios de administrador
        print("🔐 Verificando privilégios de administrador...")
        check_admin_privileges()
        
        # Configura aplicação
        print("⚙️  Configurando aplicação...")
        if not setup_application():
            print("❌ Falha na configuração da aplicação")
            input("Pressione Enter para sair...")
            return
        
        # Inicia interface gráfica
        print("🎨 Iniciando interface gráfica...")
        print("✅ Aplicação carregada com sucesso!\n")
        
        # Cria e executa a aplicação
        app = OptimizerUI()
        app.run()
        
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        print("Verifique o arquivo de log para mais detalhes.")
        traceback.print_exc()
        input("\nPressione Enter para sair...")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Programa interrompido pelo usuário")
    
    finally:
        print("\n👋 Obrigado por usar o Otimizador Windows 10 Pro!")

if __name__ == "__main__":
    main()