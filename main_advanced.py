#!/usr/bin/env python3
"""
🚀 Otimizador Windows 10 Pro - Versão Avançada
================================================

Um otimizador completo e avançado para Windows 10/11 que inclui:

🧹 LIMPEZA AVANÇADA:
- Limpeza básica e profunda do sistema
- Detecção e remoção de arquivos duplicados
- Limpeza de drivers antigos e logs de eventos
- Limpeza profunda de navegadores e caches

⚡ OTIMIZAÇÃO INTELIGENTE:
- Detecção automática de hardware
- Perfis de otimização baseados no hardware detectado
- Otimizações de memória, CPU e armazenamento
- Configurações específicas para gaming

📊 MONITORAMENTO EM TEMPO REAL:
- Monitoramento contínuo do sistema
- Alertas automáticos para problemas
- Histórico de performance
- Relatórios detalhados

⏰ AGENDAMENTO INTELIGENTE:
- Tarefas automáticas de manutenção
- Agendamentos personalizáveis
- Execução em background

🖥️ INTERFACE AVANÇADA:
- Design moderno com tema escuro
- Gráficos em tempo real
- Múltiplas abas organizadas
- Sistema de backup integrado

Autor: Gabriel - Sistema de Otimização Avançada
Versão: 2.0.0 (Avançada)
Data: Dezembro 2024

IMPORTANTE: Execute como administrador para obter todos os recursos!
"""

import sys
import os
import logging
import traceback
import ctypes
from pathlib import Path

# Adiciona o diretório atual ao path para importações
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def is_admin():
    """Verifica se está executando como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_logging():
    """Configura sistema de logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"optimizer_advanced_{os.getpid()}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Sistema de logging avançado inicializado")
    return logger

def install_dependencies():
    """Instala todas as dependências necessárias"""
    import subprocess
    
    print("📦 Verificando e instalando dependências avançadas...")
    
    # Dependências obrigatórias
    required_packages = [
        'customtkinter>=5.2.0',
        'psutil>=5.9.0',
        'pywin32>=307',
        'requests>=2.31.0',
        'Pillow>=10.0.0',
        'matplotlib>=3.8.0',
        'schedule>=1.2.0'
    ]
    
    # Dependências opcionais (podem falhar em alguns sistemas)
    optional_packages = [
        'WMI>=1.5.0'
    ]
    
    all_success = True
    
    # Instalar dependências obrigatórias
    for package in required_packages:
        try:
            print(f"  📦 Instalando {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, 
                "--quiet", "--no-warn-script-location"
            ])
            print(f"  ✅ {package} instalado")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Erro ao instalar {package}: {e}")
            all_success = False
    
    # Tentar instalar dependências opcionais
    for package in optional_packages:
        try:
            print(f"  📦 Tentando instalar {package} (opcional)...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, 
                "--quiet", "--no-warn-script-location"
            ])
            print(f"  ✅ {package} instalado")
        except subprocess.CalledProcessError:
            print(f"  ⚠️ {package} não instalado (funcionalidade limitada)")
    
    return all_success

def check_system_requirements():
    """Verifica requisitos do sistema"""
    print("🔍 Verificando requisitos do sistema...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ é necessário. Versão atual: {sys.version_info[0]}.{sys.version_info[1]}")
        return False
    
    print(f"✅ Python {sys.version_info[0]}.{sys.version_info[1]} - OK")
    
    # Verificar Windows
    if sys.platform != "win32":
        print("❌ Este otimizador foi projetado para Windows 10/11")
        return False
    
    print("✅ Sistema Windows detectado")
    
    # Verificar privilégios
    if is_admin():
        print("✅ Privilégios de administrador - OK")
    else:
        print("⚠️ Executando sem privilégios de administrador")
        print("   Algumas funcionalidades podem estar limitadas")
    
    return True

def try_import_advanced_ui():
    """Tenta importar interface avançada"""
    try:
        from advanced_ui import AdvancedOptimizerUI
        return AdvancedOptimizerUI
    except ImportError as e:
        print(f"⚠️ Interface avançada não disponível: {e}")
        return None

def try_import_basic_ui():
    """Tenta importar interface básica"""
    try:
        from ui import OptimizerUI
        return OptimizerUI
    except ImportError as e:
        print(f"❌ Interface básica não disponível: {e}")
        return None

def main():
    """Função principal do otimizador avançado"""
    
    print("=" * 70)
    print("🚀 OTIMIZADOR WINDOWS 10 PRO - VERSÃO AVANÇADA")
    print("=" * 70)
    print("🧹 Limpeza Avançada | ⚡ Otimização Inteligente | 📊 Monitoramento")
    print("⏰ Agendamento Automático | 🔧 Detecção de Hardware")
    print("=" * 70)
    print("")
    
    logger = None
    
    try:
        # Configurar logging
        logger = setup_logging()
        logger.info("🎯 Iniciando Otimizador Windows 10 Pro - Versão Avançada")
        
        # Verificar requisitos
        if not check_system_requirements():
            print("\n❌ Requisitos do sistema não atendidos")
            logger.error("❌ Requisitos do sistema não atendidos")
            sys.exit(1)
        
        # Instalar dependências
        print("\n📦 Verificando dependências...")
        if not install_dependencies():
            print("⚠️ Algumas dependências falharam, mas continuando...")
            logger.warning("⚠️ Nem todas as dependências foram instaladas")
        else:
            print("✅ Todas as dependências instaladas")
            logger.info("✅ Dependências instaladas com sucesso")
        
        # Carregar interface
        print("\n🎨 Carregando interface...")
        
        # Tentar interface avançada primeiro
        UIClass = try_import_advanced_ui()
        
        if UIClass:
            print("✅ Interface avançada carregada")
            logger.info("✅ Interface avançada inicializada")
            interface_type = "avançada"
        else:
            # Fallback para interface básica
            print("🔄 Carregando interface básica...")
            UIClass = try_import_basic_ui()
            
            if UIClass:
                print("✅ Interface básica carregada")
                logger.info("✅ Interface básica como fallback")
                interface_type = "básica"
            else:
                print("❌ Não foi possível carregar nenhuma interface")
                logger.error("❌ Falha ao carregar qualquer interface")
                sys.exit(1)
        
        # Criar e executar aplicação
        print(f"\n🚀 Iniciando otimizador com interface {interface_type}...")
        logger.info(f"🚀 Aplicação iniciada com interface {interface_type}")
        
        app = UIClass()
        
        # Executar aplicação
        app.run()
        
        print("\n✅ Otimizador encerrado com sucesso")
        logger.info("✅ Aplicação encerrada normalmente")
        
    except KeyboardInterrupt:
        print("\n⏹️ Otimizador interrompido pelo usuário")
        if logger:
            logger.info("⏹️ Aplicação interrompida pelo usuário")
    
    except Exception as e:
        error_msg = f"💥 Erro crítico no otimizador: {str(e)}"
        print(f"\n{error_msg}")
        
        if logger:
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
        else:
            print(f"Detalhes do erro:\n{traceback.format_exc()}")
        
        # Salvar relatório de erro
        try:
            error_file = Path("logs") / f"crash_report_{os.getpid()}.txt"
            error_file.parent.mkdir(exist_ok=True)
            
            with open(error_file, "w", encoding="utf-8") as f:
                f.write("RELATÓRIO DE ERRO - OTIMIZADOR AVANÇADO\n")
                f.write("=" * 50 + "\n")
                f.write(f"Data: {__import__('datetime').datetime.now()}\n")
                f.write(f"PID: {os.getpid()}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Plataforma: {sys.platform}\n")
                f.write(f"Admin: {is_admin()}\n")
                f.write("\nERRO:\n")
                f.write(f"{str(e)}\n\n")
                f.write("TRACEBACK COMPLETO:\n")
                f.write(traceback.format_exc())
            
            print(f"\n📄 Relatório de erro salvo em: {error_file}")
            
        except Exception as save_error:
            print(f"❌ Não foi possível salvar relatório: {save_error}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()