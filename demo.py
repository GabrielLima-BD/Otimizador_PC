#!/usr/bin/env python3
"""
Demonstração e Teste do Otimizador Windows 10 Pro
=================================================

Este arquivo demonstra como usar os módulos do otimizador individualmente
para testes e desenvolvimento.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório do projeto ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from optimizer import SystemCleaner, PerformanceOptimizer, NetworkOptimizer, RegistryOptimizer, Utils

def test_system_info():
    """Testa a obtenção de informações do sistema"""
    print("🔍 INFORMAÇÕES DO SISTEMA")
    print("=" * 50)
    
    info = Utils.get_system_info()
    for key, value in info.items():
        if key == 'disk_usage':
            print(f"{key}:")
            for disk, usage in value.items():
                print(f"  {disk} - {usage['percent']}% usado ({usage['used']}/{usage['total']})")
        else:
            print(f"{key}: {value}")
    print()

def test_admin_privileges():
    """Testa verificação de privilégios de administrador"""
    print("🔐 PRIVILÉGIOS DE ADMINISTRADOR")
    print("=" * 50)
    
    is_admin = Utils.is_admin()
    print(f"Executando como administrador: {'✅ Sim' if is_admin else '❌ Não'}")
    
    if not is_admin:
        print("⚠️  Para obter todos os recursos, execute como administrador")
    print()

def test_temp_directories():
    """Testa a detecção de diretórios temporários"""
    print("📁 DIRETÓRIOS TEMPORÁRIOS")
    print("=" * 50)
    
    temp_dirs = Utils.get_temp_dirs()
    for i, temp_dir in enumerate(temp_dirs, 1):
        exists = "✅" if os.path.exists(temp_dir) else "❌"
        print(f"{i}. {exists} {temp_dir}")
    print()

def test_cleaner_analysis():
    """Testa análise de limpeza sem executar"""
    print("🧹 ANÁLISE DE LIMPEZA (SEM EXECUTAR)")
    print("=" * 50)
    
    cleaner = SystemCleaner()
    temp_dirs = Utils.get_temp_dirs()
    
    total_files = 0
    total_size = 0
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(file_path)
                            total_files += 1
                            total_size += file_size
                        except (PermissionError, FileNotFoundError, OSError):
                            continue
            except (PermissionError, OSError):
                continue
    
    print(f"Arquivos temporários encontrados: {total_files:,}")
    print(f"Espaço que pode ser liberado: {Utils.format_size(total_size)}")
    print()

def test_network_speed():
    """Testa velocidade básica de rede"""
    print("🌐 TESTE DE REDE")
    print("=" * 50)
    
    network = NetworkOptimizer()
    
    print("Testando ping para servidores DNS...")
    dns_servers = {
        'Cloudflare': '1.1.1.1',
        'Google': '8.8.8.8',
        'Quad9': '9.9.9.9'
    }
    
    for name, server in dns_servers.items():
        ping_result = network._ping_test(server, 3)
        if ping_result:
            print(f"{name} ({server}): {ping_result:.2f}ms")
        else:
            print(f"{name} ({server}): Falha no teste")
    print()

def test_registry_backup():
    """Testa sistema de backup"""
    print("💾 SISTEMA DE BACKUP")
    print("=" * 50)
    
    # Dados de exemplo para backup
    test_data = {
        'test_timestamp': '2025-09-22T12:00:00',
        'test_operation': 'Demonstração de backup',
        'test_settings': {
            'option1': True,
            'option2': False,
            'value': 42
        }
    }
    
    backup_file = Utils.create_backup(test_data, 'test_demo')
    if backup_file:
        print(f"✅ Backup de teste criado: {backup_file}")
        
        # Testa carregamento do backup
        loaded_data = Utils.load_backup(backup_file)
        if loaded_data:
            print("✅ Backup carregado com sucesso")
            print(f"Dados carregados: {loaded_data}")
        else:
            print("❌ Falha ao carregar backup")
    else:
        print("❌ Falha ao criar backup")
    print()

def test_service_detection():
    """Testa detecção de serviços do Windows"""
    print("⚙️  SERVIÇOS DO WINDOWS")
    print("=" * 50)
    
    performance = PerformanceOptimizer()
    
    print("Serviços que podem ser otimizados:")
    for i, service in enumerate(performance.services_to_disable, 1):
        print(f"{i:2d}. {service}")
    
    print(f"\nTotal: {len(performance.services_to_disable)} serviços")
    print()

def run_all_tests():
    """Executa todos os testes"""
    print("🚀 OTIMIZADOR WINDOWS 10 PRO - DEMONSTRAÇÃO")
    print("=" * 60)
    print()
    
    try:
        test_system_info()
        test_admin_privileges()
        test_temp_directories()
        test_cleaner_analysis()
        test_network_speed()
        test_registry_backup()
        test_service_detection()
        
        print("✅ TODOS OS TESTES CONCLUÍDOS")
        print("=" * 60)
        print()
        print("💡 PRÓXIMOS PASSOS:")
        print("1. Execute 'python main.py' para abrir a interface gráfica")
        print("2. Execute como administrador para obter todos os recursos")
        print("3. Faça backup importante antes de grandes otimizações")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()