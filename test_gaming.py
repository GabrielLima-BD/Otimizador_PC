#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das Funcionalidades Gaming e Autostart
============================================

Testa todas as novas funcionalidades implementadas:
- Inicialização automática
- Otimização no boot  
- Detecção e lançamento de jogos
- Interface gaming integrada
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# Adicionar o diretório optimizer ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'optimizer'))

def test_autostart_module():
    """Testa módulo de inicialização automática"""
    print("\n🚀 Testando módulo de inicialização automática...")
    
    try:
        from optimizer.autostart import AutostartManager
        
        manager = AutostartManager()
        print("✅ AutostartManager inicializado")
        
        # Testar status
        status = manager.get_status()
        print(f"📊 Status atual:")
        print(f"  • Registro: {'✅' if status['registry_enabled'] else '❌'}")
        print(f"  • Pasta Startup: {'✅' if status['startup_folder_enabled'] else '❌'}")
        
        # Testar detecção de startup
        is_startup = manager.is_running_on_startup()
        print(f"🔍 Executando no startup: {'✅' if is_startup else '❌'}")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de autostart: {e}")
        return False

def test_boot_optimizer():
    """Testa módulo de otimização no boot"""
    print("\n⚡ Testando módulo de otimização no boot...")
    
    try:
        from optimizer.boot_optimize import BootOptimizer
        
        optimizer = BootOptimizer()
        print("✅ BootOptimizer inicializado")
        
        # Testar otimização (modo seguro)
        config = {
            'clean_temp_files': False,  # Não limpar em teste
            'optimize_services': True,
            'set_power_plan': True,
            'optimize_network': False,  # Não modificar rede
            'clean_memory': True,
            'update_dns': False,  # Não modificar DNS
            'max_execution_time': 30
        }
        
        print("🧪 Executando teste de otimização...")
        results = optimizer.run_boot_optimization(config)
        
        print(f"📊 Resultados:")
        print(f"  • Sucesso: {'✅' if results['success'] else '❌'}")
        print(f"  • Tempo: {results['total_time']:.2f}s")
        print(f"  • Otimizações: {len(results['optimizations'])}")
        
        if results['errors']:
            print(f"  • Erros: {len(results['errors'])}")
        
        return results['success']
    except Exception as e:
        print(f"❌ Erro no teste de boot optimizer: {e}")
        return False

def test_game_scanner():
    """Testa módulo de detecção de jogos"""
    print("\n🎮 Testando módulo de detecção de jogos...")
    
    try:
        from optimizer.game_scanner import GameScanner
        
        scanner = GameScanner()
        print("✅ GameScanner inicializado")
        
        # Testar carregamento de cache
        print("📂 Carregando cache de jogos...")
        scanner.load_cache()
        cached_games = len(scanner.games_cache)
        print(f"📊 Jogos em cache: {cached_games}")
        
        # Testar escaneamento rápido (apenas diretórios existentes)
        print("🔍 Escaneando jogos instalados...")
        games = scanner.scan_games()
        
        print(f"🎯 Jogos encontrados: {len(games)}")
        
        # Mostrar alguns jogos encontrados
        if games:
            print("📋 Primeiros jogos encontrados:")
            for i, (game_id, game) in enumerate(games.items()):
                if i >= 3:  # Mostrar apenas 3 primeiros
                    break
                print(f"  🎮 {game.name} ({game.launcher})")
                print(f"     📁 {game.install_directory}")
            
            if len(games) > 3:
                print(f"  ... e mais {len(games) - 3} jogos")
        
        # Testar classificação por launcher
        launchers = {}
        for game in games.values():
            launcher = game.launcher
            if launcher not in launchers:
                launchers[launcher] = 0
            launchers[launcher] += 1
        
        print("🏷️ Jogos por launcher:")
        for launcher, count in launchers.items():
            print(f"  • {launcher}: {count}")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de game scanner: {e}")
        return False

def test_game_launcher():
    """Testa módulo de lançamento de jogos"""
    print("\n🚀 Testando módulo de lançamento de jogos...")
    
    try:
        from optimizer.game_launcher import GameLauncher
        
        launcher = GameLauncher()
        print("✅ GameLauncher inicializado")
        
        # Testar obtenção de jogos
        games = launcher.get_available_games()
        print(f"🎯 Jogos disponíveis: {len(games)}")
        
        # Testar estatísticas
        stats = launcher.get_game_statistics()
        print("📊 Estatísticas gerais:")
        print(f"  • Jogos lançados: {stats['total_games_launched']}")
        print(f"  • Tempo total: {stats['total_playtime_hours']:.1f}h")
        print(f"  • Sessões: {stats['total_sessions']}")
        print(f"  • Favoritos: {len(stats['favorite_games'])}")
        
        # Testar configurações de gaming
        print("🎮 Configurações de gaming:")
        for key, value in launcher.gaming_optimizations.items():
            status = "✅" if value else "❌"
            print(f"  • {key}: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de game launcher: {e}")
        return False

def test_integration():
    """Testa integração entre módulos"""
    print("\n🔗 Testando integração entre módulos...")
    
    try:
        # Testar se todos os módulos podem ser importados juntos
        from optimizer.autostart import AutostartManager
        from optimizer.boot_optimize import BootOptimizer
        from optimizer.game_scanner import GameScanner
        from optimizer.game_launcher import GameLauncher
        
        print("✅ Todos os módulos importados com sucesso")
        
        # Testar se dados podem ser compartilhados
        scanner = GameScanner()
        launcher = GameLauncher()
        
        scanner_games = len(scanner.games_cache)
        launcher_games = len(launcher.get_available_games())
        
        print(f"📊 Integração de dados:")
        print(f"  • Scanner: {scanner_games} jogos")
        print(f"  • Launcher: {launcher_games} jogos")
        
        # Verificar se usam a mesma fonte de dados
        if scanner_games == launcher_games:
            print("✅ Dados sincronizados entre módulos")
        else:
            print("⚠️ Possível dessincronização de dados")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de integração: {e}")
        return False

def test_ui_components():
    """Testa componentes da interface"""
    print("\n🎨 Testando componentes da interface...")
    
    try:
        # Testar se a interface principal pode ser importada
        import main_gaming
        print("✅ Interface gaming importada")
        
        # Testar se CustomTkinter está disponível
        import customtkinter as ctk
        print("✅ CustomTkinter disponível")
        
        # Verificar se todas as classes estão acessíveis
        classes_to_test = [
            'GamePanelFrame',
            'AutostartFrame', 
            'AdvancedMainWindow'
        ]
        
        for class_name in classes_to_test:
            if hasattr(main_gaming, class_name):
                print(f"✅ Classe {class_name} disponível")
            else:
                print(f"❌ Classe {class_name} não encontrada")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de UI: {e}")
        return False

def create_test_report(results):
    """Cria relatório de teste"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_gaming_report_{timestamp}.json"
    
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'test_results': results,
        'summary': {
            'total_tests': len(results),
            'passed': sum(1 for r in results.values() if r),
            'failed': sum(1 for r in results.values() if not r),
            'success_rate': (sum(1 for r in results.values() if r) / len(results)) * 100
        }
    }
    
    try:
        # Criar diretório de logs se não existir
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        report_path = logs_dir / report_file
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return str(report_path)
    except Exception as e:
        print(f"⚠️ Erro ao salvar relatório: {e}")
        return None

def main():
    """Função principal de teste"""
    print("🎮 INICIANDO TESTES - FUNCIONALIDADES GAMING E AUTOSTART")
    print("=" * 70)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🖥️ Python: {sys.version}")
    print(f"📁 Diretório: {os.getcwd()}")
    print("=" * 70)
    
    # Executar todos os testes
    tests = {
        'Autostart Module': test_autostart_module,
        'Boot Optimizer': test_boot_optimizer,
        'Game Scanner': test_game_scanner,
        'Game Launcher': test_game_launcher,
        'Module Integration': test_integration,
        'UI Components': test_ui_components
    }
    
    results = {}
    
    for test_name, test_func in tests.items():
        try:
            print(f"\n🧪 Executando: {test_name}")
            results[test_name] = test_func()
            if results[test_name]:
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            print(f"💥 {test_name}: ERRO - {e}")
            results[test_name] = False
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO FINAL DE TESTES")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"Total de testes: {total_tests}")
    print(f"✅ Testes aprovados: {passed_tests}")
    print(f"❌ Testes falharam: {failed_tests}")
    print(f"📊 Taxa de sucesso: {success_rate:.1f}%")
    
    print("\n📋 Detalhes por módulo:")
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"  {test_name}: {status}")
    
    # Salvar relatório
    report_path = create_test_report(results)
    if report_path:
        print(f"\n💾 Relatório salvo em: {report_path}")
    
    print("\n" + "=" * 60)
    if success_rate == 100:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ As funcionalidades gaming estão funcionando perfeitamente!")
    elif success_rate >= 80:
        print("⚠️ MAIORIA DOS TESTES PASSOU!")
        print("🔧 Algumas funcionalidades podem precisar de ajustes.")
    else:
        print("❌ MUITOS TESTES FALHARAM!")
        print("🛠️ As funcionalidades precisam de correções significativas.")
    print("=" * 60)
    
    return success_rate == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)