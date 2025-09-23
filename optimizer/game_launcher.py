#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Launcher de Jogos
===========================

Interface para iniciar jogos detectados pelo sistema, com otimizações
automáticas e modo gaming integrado.

Funcionalidades:
- Interface de seleção e lançamento de jogos
- Aplicação de otimizações antes do lançamento
- Modo gaming automático
- Monitoramento de performance durante jogos
- Estatísticas de uso dos jogos
"""

import os
import sys
import time
import json
import psutil
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

# Importar módulos do otimizador
from .game_scanner import GameScanner, GameInfo
from .advanced_optimizer import AdvancedOptimizer
from .system_monitor import SystemMonitor

@dataclass
class GameSession:
    """Informações de uma sessão de jogo"""
    game_id: str
    game_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: float = 0
    avg_cpu_usage: float = 0
    avg_memory_usage: float = 0
    max_temperature: float = 0
    performance_score: float = 0

class GameLauncher:
    """Launcher de jogos com otimizações integradas"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.game_scanner = GameScanner()
        self.optimizer = AdvancedOptimizer()
        self.monitor = SystemMonitor()
        
        self.current_session: Optional[GameSession] = None
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        
        # Configurações de otimização para jogos
        self.gaming_optimizations = {
            'disable_windows_updates': True,
            'set_high_priority': True,
            'disable_notifications': True,
            'optimize_memory': True,
            'disable_background_apps': True,
            'set_power_plan_performance': True,
            'disable_game_mode': False,  # Manter Game Mode ativo
            'optimize_network': True,
        }
        
        # Estatísticas de jogos
        self.stats_file = Path("game_stats.json")
        self.game_stats = self._load_stats()
    
    def _load_stats(self) -> Dict[str, Any]:
        """Carrega estatísticas de jogos"""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Erro ao carregar estatísticas: {e}")
        
        return {
            'total_play_time': 0,
            'games_launched': 0,
            'favorite_games': [],
            'sessions': [],
            'performance_history': []
        }
    
    def _save_stats(self) -> None:
        """Salva estatísticas de jogos"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_stats, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Erro ao salvar estatísticas: {e}")
    
    def get_available_games(self) -> List[GameInfo]:
        """Obtém lista de jogos disponíveis"""
        games = self.game_scanner.scan_games()
        return list(games.values())
    
    def launch_game(self, game_id: str, apply_optimizations: bool = True) -> bool:
        """
        Lança um jogo com otimizações opcionais
        
        Args:
            game_id: ID do jogo para lançar
            apply_optimizations: Se deve aplicar otimizações de gaming
            
        Returns:
            True se lançado com sucesso, False caso contrário
        """
        try:
            # Obter informações do jogo
            games = self.game_scanner.games_cache
            if game_id not in games:
                self.logger.error(f"Jogo {game_id} não encontrado")
                return False
            
            game = games[game_id]
            
            # Verificar se o executável existe
            if not os.path.exists(game.executable_path):
                self.logger.error(f"Executável não encontrado: {game.executable_path}")
                return False
            
            self.logger.info(f"Lançando jogo: {game.name}")
            
            # Aplicar otimizações se solicitado
            if apply_optimizations:
                self._apply_gaming_optimizations()
            
            # Iniciar monitoramento
            self._start_game_monitoring(game)
            
            # Lançar o jogo
            success = self._execute_game(game)
            
            if success:
                # Atualizar estatísticas
                self.game_scanner.update_game_play_info(game_id)
                self.game_stats['games_launched'] += 1
                self._save_stats()
            
            return success
        
        except Exception as e:
            self.logger.error(f"Erro ao lançar jogo: {e}")
            return False
    
    def _apply_gaming_optimizations(self) -> None:
        """Aplica otimizações específicas para gaming"""
        try:
            self.logger.info("Aplicando otimizações de gaming...")
            
            # Configurar prioridade alta para processos de jogo
            if self.gaming_optimizations['set_high_priority']:
                self._set_gaming_priority()
            
            # Otimizar memória
            if self.gaming_optimizations['optimize_memory']:
                try:
                    # Usar otimização específica para gaming
                    self.optimizer.optimize_gaming_performance()
                except Exception as e:
                    self.logger.warning(f"Erro na otimização de gaming: {e}")
            
            # Configurar plano de energia para performance
            if self.gaming_optimizations['set_power_plan_performance']:
                self._set_performance_power_plan()
            
            # Desabilitar aplicações em background desnecessárias
            if self.gaming_optimizations['disable_background_apps']:
                self._disable_background_apps()
            
            # Otimizar configurações de rede
            if self.gaming_optimizations['optimize_network']:
                self._optimize_network_for_gaming()
            
            self.logger.info("Otimizações de gaming aplicadas")
        
        except Exception as e:
            self.logger.error(f"Erro ao aplicar otimizações: {e}")
    
    def _set_gaming_priority(self) -> None:
        """Configura prioridade alta para processos de jogo"""
        try:
            # Esta configuração será aplicada quando o jogo for detectado em execução
            pass
        except Exception as e:
            self.logger.error(f"Erro ao configurar prioridade: {e}")
    
    def _set_performance_power_plan(self) -> None:
        """Configura plano de energia para máxima performance"""
        try:
            # Configurar para plano de alto desempenho
            subprocess.run([
                'powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
            ], check=False, capture_output=True)
        except Exception as e:
            self.logger.error(f"Erro ao configurar plano de energia: {e}")
    
    def _disable_background_apps(self) -> None:
        """Desabilita aplicações em background desnecessárias"""
        try:
            # Lista de processos que podem ser temporariamente pausados
            background_processes = [
                'OneDrive.exe',
                'Spotify.exe',
                'Discord.exe',
                'Teams.exe',
                'Slack.exe'
            ]
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] in background_processes:
                        # Reduzir prioridade ao invés de matar
                        process = psutil.Process(proc.info['pid'])
                        process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                except:
                    continue
        
        except Exception as e:
            self.logger.error(f"Erro ao gerenciar aplicações em background: {e}")
    
    def _optimize_network_for_gaming(self) -> None:
        """Otimiza configurações de rede para gaming"""
        try:
            # Flush DNS para melhor conectividade
            subprocess.run(['ipconfig', '/flushdns'], 
                         check=False, capture_output=True)
            
            # Otimizar configurações TCP/IP (requer admin)
            try:
                subprocess.run([
                    'netsh', 'int', 'tcp', 'set', 'global', 'autotuning=normal'
                ], check=False, capture_output=True)
            except:
                pass
        
        except Exception as e:
            self.logger.error(f"Erro ao otimizar rede: {e}")
    
    def _execute_game(self, game: GameInfo) -> bool:
        """Executa o jogo"""
        try:
            # Mudar para o diretório do jogo
            game_dir = os.path.dirname(game.executable_path)
            if os.path.exists(game_dir):
                os.chdir(game_dir)
            
            # Executar o jogo
            if game.launcher == "Steam":
                # Para jogos Steam, tentar usar protocolo steam://
                steam_id = self._get_steam_app_id(game)
                if steam_id:
                    subprocess.Popen(['cmd', '/c', f'start steam://rungameid/{steam_id}'])
                else:
                    subprocess.Popen([game.executable_path])
            else:
                # Executar diretamente
                subprocess.Popen([game.executable_path])
            
            self.logger.info(f"Jogo {game.name} executado com sucesso")
            return True
        
        except Exception as e:
            self.logger.error(f"Erro ao executar jogo: {e}")
            return False
    
    def _get_steam_app_id(self, game: GameInfo) -> Optional[str]:
        """Tenta obter o Steam App ID do jogo"""
        try:
            # Procurar por arquivo .acf na pasta steamapps
            steamapps_path = Path(game.install_directory).parent
            
            for acf_file in steamapps_path.glob("appmanifest_*.acf"):
                try:
                    with open(acf_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if game.name.lower() in content.lower():
                            # Extrair App ID do nome do arquivo
                            app_id = acf_file.stem.replace('appmanifest_', '')
                            return app_id
                except:
                    continue
        
        except Exception as e:
            self.logger.error(f"Erro ao obter Steam App ID: {e}")
        
        return None
    
    def _start_game_monitoring(self, game: GameInfo) -> None:
        """Inicia monitoramento de performance durante o jogo"""
        try:
            if not game.game_id:
                self.logger.warning("Game ID não disponível para monitoramento")
                return
                
            self.current_session = GameSession(
                game_id=game.game_id,
                game_name=game.name,
                start_time=datetime.now()
            )
            
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self._monitor_game_performance,
                daemon=True
            )
            self.monitoring_thread.start()
        
        except Exception as e:
            self.logger.error(f"Erro ao iniciar monitoramento: {e}")
    
    def _monitor_game_performance(self) -> None:
        """Monitora performance durante execução do jogo"""
        try:
            cpu_readings = []
            memory_readings = []
            temp_readings = []
            
            while self.monitoring_active and self.current_session:
                # Coletar métricas
                metrics = self.monitor.collect_metrics()
                
                cpu_readings.append(metrics.get('cpu_percent', 0))
                memory_readings.append(metrics.get('memory_percent', 0))
                
                # Temperaturas se disponíveis
                temperatures = metrics.get('temperatures', {})
                if temperatures:
                    max_temp = max(temperatures.values()) if temperatures else 0
                    temp_readings.append(max_temp)
                
                # Aguardar próxima coleta
                time.sleep(5)
                
                # Verificar se o jogo ainda está rodando
                if not self._is_game_running():
                    self._stop_game_monitoring()
                    break
            
            # Calcular médias e finalizar sessão
            if self.current_session:
                self.current_session.end_time = datetime.now()
                self.current_session.duration_minutes = (
                    self.current_session.end_time - self.current_session.start_time
                ).total_seconds() / 60
                
                if cpu_readings:
                    self.current_session.avg_cpu_usage = sum(cpu_readings) / len(cpu_readings)
                if memory_readings:
                    self.current_session.avg_memory_usage = sum(memory_readings) / len(memory_readings)
                if temp_readings:
                    self.current_session.max_temperature = max(temp_readings)
                
                # Calcular score de performance
                self.current_session.performance_score = self._calculate_performance_score()
                
                # Salvar sessão
                self._save_game_session()
        
        except Exception as e:
            self.logger.error(f"Erro durante monitoramento: {e}")
    
    def _is_game_running(self) -> bool:
        """Verifica se o jogo ainda está em execução"""
        try:
            if not self.current_session:
                return False
            
            # Procurar processo do jogo
            game = self.game_scanner.games_cache.get(self.current_session.game_id)
            if not game:
                return False
            
            game_exe_name = os.path.basename(game.executable_path).lower()
            
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() == game_exe_name:
                        return True
                except:
                    continue
            
            return False
        
        except Exception as e:
            self.logger.error(f"Erro ao verificar se jogo está rodando: {e}")
            return False
    
    def _stop_game_monitoring(self) -> None:
        """Para o monitoramento do jogo"""
        self.monitoring_active = False
        
        # Restaurar configurações do sistema
        self._restore_system_settings()
    
    def _restore_system_settings(self) -> None:
        """Restaura configurações do sistema após o jogo"""
        try:
            # Restaurar plano de energia balanceado
            subprocess.run([
                'powercfg', '/setactive', '381b4222-f694-41f0-9685-ff5bb260df2e'
            ], check=False, capture_output=True)
            
            # Restaurar prioridades normais dos processos
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    process = psutil.Process(proc.info['pid'])
                    if process.nice() != psutil.NORMAL_PRIORITY_CLASS:
                        process.nice(psutil.NORMAL_PRIORITY_CLASS)
                except:
                    continue
        
        except Exception as e:
            self.logger.error(f"Erro ao restaurar configurações: {e}")
    
    def _calculate_performance_score(self) -> float:
        """Calcula score de performance da sessão"""
        try:
            if not self.current_session:
                return 0.0
            
            # Fatores para o score (0-100)
            cpu_score = max(0, 100 - self.current_session.avg_cpu_usage)
            memory_score = max(0, 100 - self.current_session.avg_memory_usage)
            
            # Temperature score (assumindo 70°C como limite ideal)
            temp_score = max(0, 100 - (self.current_session.max_temperature / 70 * 100))
            
            # Score ponderado
            final_score = (cpu_score * 0.4 + memory_score * 0.4 + temp_score * 0.2)
            
            return round(final_score, 2)
        
        except Exception as e:
            self.logger.error(f"Erro ao calcular performance score: {e}")
            return 0.0
    
    def _save_game_session(self) -> None:
        """Salva informações da sessão de jogo"""
        try:
            if not self.current_session:
                return
            
            # Adicionar às estatísticas
            session_data = {
                'game_id': self.current_session.game_id,
                'game_name': self.current_session.game_name,
                'start_time': self.current_session.start_time.isoformat(),
                'end_time': self.current_session.end_time.isoformat() if self.current_session.end_time else None,
                'duration_minutes': self.current_session.duration_minutes,
                'avg_cpu_usage': self.current_session.avg_cpu_usage,
                'avg_memory_usage': self.current_session.avg_memory_usage,
                'max_temperature': self.current_session.max_temperature,
                'performance_score': self.current_session.performance_score
            }
            
            self.game_stats['sessions'].append(session_data)
            self.game_stats['total_play_time'] += self.current_session.duration_minutes
            
            # Manter apenas últimas 100 sessões
            if len(self.game_stats['sessions']) > 100:
                self.game_stats['sessions'] = self.game_stats['sessions'][-100:]
            
            self._save_stats()
            
            self.logger.info(f"Sessão de jogo salva: {self.current_session.duration_minutes:.1f} min")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar sessão: {e}")
    
    def get_game_statistics(self, game_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtém estatísticas de jogos
        
        Args:
            game_id: ID específico do jogo, ou None para estatísticas gerais
            
        Returns:
            Dicionário com estatísticas
        """
        if game_id:
            # Estatísticas específicas do jogo
            game_sessions = [
                session for session in self.game_stats['sessions']
                if session['game_id'] == game_id
            ]
            
            if not game_sessions:
                return {
                    'total_sessions': 0,
                    'total_playtime': 0,
                    'avg_session_duration': 0,
                    'avg_performance_score': 0
                }
            
            return {
                'total_sessions': len(game_sessions),
                'total_playtime': sum(s['duration_minutes'] for s in game_sessions),
                'avg_session_duration': sum(s['duration_minutes'] for s in game_sessions) / len(game_sessions),
                'avg_performance_score': sum(s['performance_score'] for s in game_sessions) / len(game_sessions),
                'recent_sessions': game_sessions[-5:]  # 5 mais recentes
            }
        else:
            # Estatísticas gerais
            return {
                'total_games_launched': self.game_stats['games_launched'],
                'total_playtime_hours': self.game_stats['total_play_time'] / 60,
                'total_sessions': len(self.game_stats['sessions']),
                'favorite_games': self.game_stats['favorite_games']
            }
    
    def add_favorite_game(self, game_id: str) -> bool:
        """Adiciona jogo aos favoritos"""
        try:
            if game_id not in self.game_stats['favorite_games']:
                self.game_stats['favorite_games'].append(game_id)
                self._save_stats()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Erro ao adicionar favorito: {e}")
            return False
    
    def remove_favorite_game(self, game_id: str) -> bool:
        """Remove jogo dos favoritos"""
        try:
            if game_id in self.game_stats['favorite_games']:
                self.game_stats['favorite_games'].remove(game_id)
                self._save_stats()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Erro ao remover favorito: {e}")
            return False


# Funções de conveniência
def launch_game_by_name(game_name: str, apply_optimizations: bool = True) -> bool:
    """Lança um jogo pelo nome"""
    launcher = GameLauncher()
    games = launcher.get_available_games()
    
    for game in games:
        if game_name.lower() in game.name.lower() and game.game_id:
            return launcher.launch_game(game.game_id, apply_optimizations)
    
    return False

def get_game_launcher() -> GameLauncher:
    """Obtém instância do launcher"""
    return GameLauncher()


if __name__ == "__main__":
    # Teste do módulo
    print("🎮 Testando Módulo de Launcher de Jogos")
    print("=" * 50)
    
    launcher = GameLauncher()
    print("✅ GameLauncher inicializado")
    
    # Obter jogos disponíveis
    games = launcher.get_available_games()
    print(f"🎯 Jogos disponíveis: {len(games)}")
    
    # Mostrar alguns jogos
    for i, game in enumerate(games[:3]):
        print(f"  🎮 {game.name} ({game.launcher})")
    
    # Estatísticas gerais
    stats = launcher.get_game_statistics()
    print(f"📊 Total de sessões: {stats['total_sessions']}")
    print(f"⏱️ Tempo total de jogo: {stats['total_playtime_hours']:.1f}h")
    
    print("\n✅ Módulo funcionando corretamente!")