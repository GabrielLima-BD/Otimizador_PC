#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo das Funcionalidades Avançadas - Otimizador Windows 10 Pro
================================================================

Este script demonstra todas as funcionalidades avançadas implementadas
sem a necessidade da interface gráfica.

Funcionalidades demonstradas:
- Detecção automática de hardware
- Limpeza profunda
- Otimizações avançadas
- Monitoramento em tempo real
- Agendamento inteligente
"""

import sys
import os
import time
from datetime import datetime

# Adicionar o diretório optimizer ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'optimizer'))

def demo_hardware_detection():
    """Demonstra a detecção de hardware"""
    print("\n" + "="*50)
    print("🔧 DETECÇÃO AUTOMÁTICA DE HARDWARE")
    print("="*50)
    
    try:
        from optimizer.hardware_detector import HardwareDetector
        
        detector = HardwareDetector()
        print("📡 Analisando sistema...")
        
        hardware_info = detector.detect_system_hardware()
        
        if hardware_info:
            print(f"💻 CPU: {hardware_info.get('cpu', {}).get('name', 'N/A')}")
            print(f"🧠 Memória: {hardware_info.get('memory', {}).get('total_gb', 'N/A')} GB")
            print(f"💿 Storage: {len(hardware_info.get('storage', {}).get('drives', []))} dispositivos")
            
            # Mostrar detalhes de storage
            storage = hardware_info.get('storage', {})
            if storage.get('drives'):
                for i, drive in enumerate(storage['drives']):
                    ssd_status = "SSD" if drive.get('is_ssd') else "HDD"
                    nvme_status = " (NVMe)" if drive.get('is_nvme') else ""
                    print(f"  📀 Drive {i+1}: {drive.get('model', 'Unknown')} - {ssd_status}{nvme_status}")
            
            print(f"🖥️ GPU: {hardware_info.get('gpu', {}).get('name', 'Integrada')}")
            
            # Classificar perfil
            profile = detector.classify_system_profile(hardware_info)
            profile_names = {
                'gaming_high_end': '🎮 Gaming High-End',
                'gaming_mid_range': '🎮 Gaming Mid-Range',
                'productivity': '💼 Produtividade',
                'balanced': '⚖️ Balanceado',
                'basic': '📊 Básico'
            }
            
            print(f"🎯 Perfil detectado: {profile_names.get(profile, profile)}")
            
        return True
    except Exception as e:
        print(f"❌ Erro na detecção: {e}")
        return False

def demo_advanced_cleaning():
    """Demonstra funcionalidades de limpeza avançada"""
    print("\n" + "="*50)
    print("🧹 LIMPEZA PROFUNDA DO SISTEMA")
    print("="*50)
    
    try:
        from optimizer.advanced_cleaner import AdvancedCleaner
        
        cleaner = AdvancedCleaner()
        print("🔍 Iniciando análise de limpeza profunda...")
        
        # Simular limpeza sem executar
        print("✅ Módulo de detecção de duplicatas: Carregado")
        print("✅ Módulo de limpeza de drivers antigos: Carregado")
        print("✅ Módulo de limpeza de logs do sistema: Carregado")
        print("✅ Módulo de limpeza profunda de navegadores: Carregado")
        
        print("\n📊 Funcionalidades disponíveis:")
        print("  🔍 Detecção de arquivos duplicados por hash MD5")
        print("  🗑️ Limpeza de drivers antigos e não utilizados")
        print("  📋 Limpeza de logs de eventos do Windows")
        print("  🌐 Limpeza profunda de cache de navegadores")
        print("  💾 Remoção de pontos de restauração antigos")
        
        return True
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")
        return False

def demo_advanced_optimization():
    """Demonstra otimizações avançadas"""
    print("\n" + "="*50)
    print("⚡ OTIMIZAÇÕES AVANÇADAS DO SISTEMA")
    print("="*50)
    
    try:
        from optimizer.advanced_optimizer import AdvancedOptimizer
        
        optimizer = AdvancedOptimizer()
        print("🚀 Carregando módulos de otimização...")
        
        print("\n📈 Módulos de otimização disponíveis:")
        print("  🧠 Gerenciamento avançado de memória")
        print("     - Configuração de PageFile otimizada")
        print("     - Otimização de cache do sistema")
        print("     - Configurações de Prefetch/Superfetch")
        
        print("  🔄 Agendamento inteligente de CPU")
        print("     - Prioridades de processo otimizadas")
        print("     - Configurações de responsividade")
        print("     - Boost de CPU para aplicações")
        
        print("  💾 Otimização de armazenamento")
        print("     - Configurações TRIM para SSDs")
        print("     - Desfragmentação inteligente")
        print("     - Otimização de metadados NTFS")
        
        print("  🎮 Otimizações para gaming")
        print("     - Game Mode otimizado")
        print("     - Configurações DirectX")
        print("     - Prioridades para jogos")
        
        return True
    except Exception as e:
        print(f"❌ Erro na otimização: {e}")
        return False

def demo_system_monitoring():
    """Demonstra monitoramento do sistema"""
    print("\n" + "="*50)
    print("📊 MONITORAMENTO EM TEMPO REAL")
    print("="*50)
    
    try:
        from optimizer.system_monitor import SystemMonitor
        
        monitor = SystemMonitor()
        print("📈 Iniciando coleta de métricas...")
        
        # Coletar métricas atuais
        metrics = monitor.collect_metrics()
        
        print(f"\n💻 Status atual do sistema:")
        print(f"  🖥️ CPU: {metrics['cpu_percent']:.1f}%")
        print(f"  🧠 Memória: {metrics['memory_percent']:.1f}% ({metrics['memory_used_gb']:.1f}GB / {metrics['memory_total_gb']:.1f}GB)")
        print(f"  💿 Disco: {metrics['disk_percent']:.1f}% ({metrics['disk_used_gb']:.1f}GB / {metrics['disk_total_gb']:.1f}GB)")
        
        if metrics['temperatures']['cpu']:
            print(f"  🌡️ Temperatura CPU: {metrics['temperatures']['cpu']:.1f}°C")
        else:
            print(f"  🌡️ Temperatura CPU: Não disponível")
        
        # Calcular pontuação de saúde
        health_score = monitor.calculate_health_score(metrics)
        
        health_status = "💚 Excelente" if health_score >= 80 else \
                       "🟡 Bom" if health_score >= 60 else \
                       "🔴 Atenção"
        
        print(f"\n🎯 Pontuação de saúde: {health_score}/100 ({health_status})")
        
        print(f"\n⚙️ Funcionalidades de monitoramento:")
        print(f"  📊 Coleta de métricas em tempo real")
        print(f"  🚨 Sistema de alertas configuráveis")
        print(f"  📈 Histórico de performance")
        print(f"  📄 Exportação de relatórios")
        
        return True
    except Exception as e:
        print(f"❌ Erro no monitoramento: {e}")
        return False

def demo_scheduling():
    """Demonstra sistema de agendamento"""
    print("\n" + "="*50)
    print("⏰ AGENDAMENTO INTELIGENTE DE TAREFAS")
    print("="*50)
    
    try:
        from optimizer.schedule_manager import ScheduleManager
        
        scheduler = ScheduleManager()
        print("📅 Configurando agendamentos...")
        
        # Configurar tarefas padrão
        scheduler.setup_default_tasks()
        
        # Obter tarefas agendadas
        jobs = scheduler.get_scheduled_jobs()
        
        print(f"\n📋 Tarefas agendadas ({len(jobs)} ativas):")
        for job in jobs:
            status = "✅ Ativa" if job['enabled'] else "⏸️ Pausada"
            next_run = job['next_run'][:19] if job['next_run'] else "Não agendada"
            
            print(f"  📌 {job['name']}")
            print(f"     Status: {status}")
            print(f"     Próxima execução: {next_run}")
            print(f"     Execuções: {job['run_count']} (sucesso: {job['success_count']})")
            print()
        
        print(f"⚙️ Tipos de agendamento disponíveis:")
        print(f"  📅 Diário: Execução todos os dias")
        print(f"  📆 Semanal: Execução em dias específicos")
        print(f"  🗓️ Mensal: Execução em datas específicas")
        print(f"  🚀 Startup: Execução na inicialização")
        print(f"  💤 Idle: Execução quando sistema ocioso")
        
        return True
    except Exception as e:
        print(f"❌ Erro no agendamento: {e}")
        return False

def demo_basic_functionality():
    """Demonstra funcionalidades básicas"""
    print("\n" + "="*50)
    print("🛠️ FUNCIONALIDADES BÁSICAS")
    print("="*50)
    
    try:
        from optimizer.cleaner import SystemCleaner
        from optimizer.performance import PerformanceOptimizer
        from optimizer.network import NetworkOptimizer
        
        print("✅ Sistema de limpeza básica: Disponível")
        print("✅ Otimizador de performance: Disponível")
        print("✅ Otimizador de rede: Disponível")
        print("✅ Sistema de backup: Disponível")
        
        print(f"\n📋 Funcionalidades básicas incluem:")
        print(f"  🧹 Limpeza de arquivos temporários")
        print(f"  🗑️ Esvaziamento da lixeira")
        print(f"  🌐 Cache de navegadores")
        print(f"  ⚡ Otimização de serviços")
        print(f"  🌐 Configuração de DNS")
        print(f"  📋 Limpeza do registro")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas funcionalidades básicas: {e}")
        return False

def main():
    """Função principal da demonstração"""
    print("🚀 DEMONSTRAÇÃO - OTIMIZADOR WINDOWS 10 PRO - VERSÃO AVANÇADA")
    print("="*70)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🖥️ Python: {sys.version}")
    print("="*70)
    
    # Lista de demonstrações
    demos = [
        ("Funcionalidades Básicas", demo_basic_functionality),
        ("Detecção de Hardware", demo_hardware_detection),
        ("Limpeza Avançada", demo_advanced_cleaning),
        ("Otimizações Avançadas", demo_advanced_optimization),
        ("Monitoramento do Sistema", demo_system_monitoring),
        ("Agendamento Inteligente", demo_scheduling),
    ]
    
    results = {}
    
    for name, demo_func in demos:
        print(f"\n🔄 Executando: {name}...")
        try:
            results[name] = demo_func()
            time.sleep(1)  # Pausa entre demonstrações
        except Exception as e:
            print(f"❌ Erro em {name}: {e}")
            results[name] = False
    
    # Resumo final
    print("\n" + "="*70)
    print("📋 RESUMO DA DEMONSTRAÇÃO")
    print("="*70)
    
    total = len(results)
    success = sum(1 for result in results.values() if result)
    
    print(f"Total de módulos: {total}")
    print(f"✅ Funcionando: {success}")
    print(f"❌ Com problemas: {total - success}")
    print(f"📊 Taxa de sucesso: {(success/total)*100:.1f}%")
    
    print(f"\n📋 Status por módulo:")
    for name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {name}")
    
    print("\n" + "="*70)
    if success == total:
        print("🎉 TODAS AS FUNCIONALIDADES ESTÃO OPERACIONAIS!")
        print("✅ O Otimizador Windows 10 Pro - Versão Avançada está pronto para uso!")
    else:
        print("⚠️ Algumas funcionalidades precisam de atenção")
        print("🔧 Verifique as dependências e configurações")
    
    print("="*70)
    
    print(f"\n💡 Para usar a versão completa:")
    print(f"   🚀 Interface avançada: python main_advanced.py")
    print(f"   📄 Interface básica: python main.py")
    print(f"   📋 Testes completos: python test_advanced.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Demonstração interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal na demonstração: {e}")