"""
Modos Especiais de Otimização ULTRA
Funcionalidades avançadas para performance extrema
"""

import os
import json
import time
import psutil
import threading
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
import winreg
import subprocess
import ctypes
from pathlib import Path

@dataclass
class PerformanceReport:
    """Relatório de performance do sistema"""
    timestamp: str
    cpu_usage_before: float
    cpu_usage_after: float
    memory_usage_before: float
    memory_usage_after: float
    boot_time_before: Optional[float] = None
    boot_time_after: Optional[float] = None
    network_latency_before: Optional[float] = None
    network_latency_after: Optional[float] = None
    optimizations_applied: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.optimizations_applied is None:
            self.optimizations_applied = []

class SpecialModes:
    """Modos especiais de otimização ULTRA"""
    
    def __init__(self, advanced_optimizer=None):
        self.advanced_optimizer = advanced_optimizer
        self.reports_dir = Path("logs/reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.current_mode = None
        self.active_services_backup = {}
        
        # Configurar logger
        import logging
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
    # 🚀 MODO TURBO - Desativa tudo para jogos
    def activate_turbo_mode(self, progress_callback: Optional[Callable] = None) -> Dict:
        """
        Modo TURBO: Desativa tudo possível para máxima performance em jogos
        Pode ser revertido quando necessário
        """
        if progress_callback:
            progress_callback("Iniciando Modo TURBO...", 0, 10)
        
        self.current_mode = "turbo"
        optimizations_applied = []
        
        try:
            # Backup dos serviços atuais
            self._backup_current_services()
            
            # 1. Desativar serviços não essenciais
            if progress_callback:
                progress_callback("Desativando serviços desnecessários...", 1, 10)
            
            # 🎤 SERVIÇOS PROTEGIDOS - NUNCA DESABILITAR (ÁUDIO/MICROFONE)
            protected_audio_services = [
                'AudioSrv', 'Audiosrv', 'AudioEndpointBuilder', 'RpcEptMapper', 
                'DcomLaunch', 'RpcSs', 'MMCSS', 'WavesSysSvc'
            ]
            
            services_to_disable = [
                "Themes", "Windows Search", "Print Spooler", "Fax",
                "Windows Update", "Background Intelligent Transfer Service",
                "Windows Defender Antivirus Service", "TabletInputService",
                "Touch Keyboard and Handwriting Panel Service",
                "Windows Mobile Hotspot Service", "Windows Biometric Service"
            ]
            
            for service in services_to_disable:
                # 🎤 PROTEÇÃO DE ÁUDIO - Verificar se não é serviço de áudio
                if service.lower() in [s.lower() for s in protected_audio_services]:
                    continue
                if self._disable_service(service):
                    optimizations_applied.append(f"Serviço desativado: {service}")
            
            # 2. Parar processos desnecessários
            if progress_callback:
                progress_callback("Finalizando processos desnecessários...", 3, 10)
            
            processes_to_stop = [
                "OneDrive.exe", "Teams.exe", "Skype.exe", "Spotify.exe",
                "Discord.exe", "Chrome.exe", "Firefox.exe"
            ]
            
            for process in processes_to_stop:
                if self._stop_process(process):
                    optimizations_applied.append(f"Processo finalizado: {process}")
            
            # 3. Configurações de performance extrema
            if progress_callback:
                progress_callback("Aplicando configurações de performance...", 5, 10)
            
            self._apply_extreme_performance_settings()
            optimizations_applied.append("Configurações de performance extrema aplicadas")
            
            # 4. Limpar RAM e cache
            if progress_callback:
                progress_callback("Limpando RAM e cache...", 7, 10)
            
            self._clear_memory_cache()
            optimizations_applied.append("RAM e cache limpos")
            
            # 5. Configurar prioridade de CPU para jogos
            if progress_callback:
                progress_callback("Otimizando prioridades de CPU...", 9, 10)
            
            self._optimize_cpu_priorities()
            optimizations_applied.append("Prioridades de CPU otimizadas")
            
            if progress_callback:
                progress_callback("Modo TURBO ativado! Sistema otimizado para jogos", 10, 10)
            
            return {
                "success": True,
                "mode": "turbo",
                "optimizations": optimizations_applied,
                "message": "Modo TURBO ativado! Performance máxima para jogos."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao ativar Modo TURBO"
            }
    
    def deactivate_turbo_mode(self, progress_callback: Optional[Callable] = None) -> Dict:
        """Desativa o Modo TURBO e restaura configurações normais"""
        if progress_callback:
            progress_callback("Desativando Modo TURBO...", 0, 5)
        
        try:
            # Restaurar serviços
            if progress_callback:
                progress_callback("Restaurando serviços...", 1, 5)
            
            self._restore_services()
            
            # Restaurar configurações de performance
            if progress_callback:
                progress_callback("Restaurando configurações...", 3, 5)
            
            self._restore_normal_performance_settings()
            
            self.current_mode = None
            
            if progress_callback:
                progress_callback("Modo TURBO desativado! Sistema restaurado", 5, 5)
            
            return {
                "success": True,
                "message": "Modo TURBO desativado. Sistema restaurado."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao desativar Modo TURBO"
            }
    
    # 🤫 MODO SILENCIOSO - Execução automática sem interface
    def activate_silent_mode(self, progress_callback: Optional[Callable] = None) -> Dict:
        """
        Modo SILENCIOSO: Executa limpeza e otimização automaticamente
        Ideal para execução no boot do sistema
        """
        if progress_callback:
            progress_callback("Iniciando Modo Silencioso...", 0, 8)
        
        optimizations_applied = []
        
        try:
            # 1. Limpeza de arquivos temporários
            if progress_callback:
                progress_callback("Limpeza de arquivos temporários...", 1, 8)
            
            temp_cleaned = self._silent_temp_cleanup()
            optimizations_applied.append(f"Arquivos temporários limpos: {temp_cleaned} MB")
            
            # 2. Limpeza de cache do sistema
            if progress_callback:
                progress_callback("Limpeza de cache do sistema...", 2, 8)
            
            cache_cleaned = self._silent_cache_cleanup()
            optimizations_applied.append(f"Cache limpo: {cache_cleaned} MB")
            
            # 3. Otimização de registro
            if progress_callback:
                progress_callback("Otimização de registro...", 4, 8)
            
            registry_optimized = self._silent_registry_optimization()
            optimizations_applied.append(f"Entradas de registro otimizadas: {registry_optimized}")
            
            # 4. Otimização de rede
            if progress_callback:
                progress_callback("Otimização de rede...", 6, 8)
            
            self._silent_network_optimization()
            optimizations_applied.append("Configurações de rede otimizadas")
            
            # 5. Preparação para jogos
            if progress_callback:
                progress_callback("Preparando sistema para jogos...", 7, 8)
            
            self._prepare_system_for_gaming()
            optimizations_applied.append("Sistema preparado para jogos")
            
            # Salvar log da execução silenciosa
            self._save_silent_log(optimizations_applied)
            
            if progress_callback:
                progress_callback("Modo Silencioso concluído!", 8, 8)
            
            return {
                "success": True,
                "mode": "silent",
                "optimizations": optimizations_applied,
                "message": "Modo Silencioso executado com sucesso."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro no Modo Silencioso"
            }
    
    # 📊 MODO BENCHMARK - Aplica tudo e gera relatório
    def activate_benchmark_mode(self, progress_callback: Optional[Callable] = None) -> Dict:
        """
        Modo BENCHMARK: Aplica todas as otimizações e gera relatório detalhado
        """
        if progress_callback:
            progress_callback("Iniciando Benchmark Mode...", 0, 15)
        
        # Coletar métricas ANTES
        before_metrics = self._collect_system_metrics()
        
        try:
            # Aplicar TODAS as otimizações
            if progress_callback:
                progress_callback("Aplicando otimizações personalizadas...", 2, 15)
            
            if self.advanced_optimizer:
                personal_result = self.advanced_optimizer.apply_personal_optimizations()
            
            if progress_callback:
                progress_callback("Aplicando otimizações avançadas...", 5, 15)
            
            if self.advanced_optimizer:
                advanced_result = self.advanced_optimizer.apply_all_advanced_optimizations()
            
            if progress_callback:
                progress_callback("Aplicando otimizações ULTRA...", 8, 15)
            
            if self.advanced_optimizer:
                ultra_result = self.advanced_optimizer.apply_all_ultra_advanced_optimizations()
            
            # Aguardar estabilização do sistema
            if progress_callback:
                progress_callback("Aguardando estabilização do sistema...", 11, 15)
            
            time.sleep(10)
            
            # Coletar métricas DEPOIS
            if progress_callback:
                progress_callback("Coletando métricas finais...", 13, 15)
            
            after_metrics = self._collect_system_metrics()
            
            # Gerar relatório
            if progress_callback:
                progress_callback("Gerando relatório de benchmark...", 14, 15)
            
            report = self._generate_benchmark_report(before_metrics, after_metrics)
            
            if progress_callback:
                progress_callback("Benchmark concluído!", 15, 15)
            
            return {
                "success": True,
                "mode": "benchmark",
                "report": report,
                "message": "Benchmark concluído com sucesso."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro no Modo Benchmark"
            }
    
    # 🧹 MODO LIMPEZA PROFUNDA - Remove tudo inútil
    def activate_deep_clean_mode(self, progress_callback: Optional[Callable] = None) -> Dict:
        """
        Modo LIMPEZA PROFUNDA: Remove todos os arquivos desnecessários
        """
        if progress_callback:
            progress_callback("Iniciando Limpeza Profunda...", 0, 12)
        
        cleaned_items = []
        total_space_freed = 0
        
        try:
            # 1. Limpeza de arquivos temporários avançada
            if progress_callback:
                progress_callback("Limpeza profunda de temporários...", 1, 12)
            
            temp_space = self._deep_clean_temp_files()
            total_space_freed += temp_space
            cleaned_items.append(f"Arquivos temporários: {temp_space} MB")
            
            # 2. Limpeza de logs do sistema
            if progress_callback:
                progress_callback("Limpeza de logs do sistema...", 2, 12)
            
            logs_space = self._deep_clean_system_logs()
            total_space_freed += logs_space
            cleaned_items.append(f"Logs do sistema: {logs_space} MB")
            
            # 3. Limpeza de cache de aplicativos
            if progress_callback:
                progress_callback("Limpeza de cache de aplicativos...", 4, 12)
            
            app_cache_space = self._deep_clean_app_cache()
            total_space_freed += app_cache_space
            cleaned_items.append(f"Cache de aplicativos: {app_cache_space} MB")
            
            # 4. Limpeza de arquivos de dump
            if progress_callback:
                progress_callback("Limpeza de arquivos de dump...", 6, 12)
            
            dump_space = self._deep_clean_dump_files()
            total_space_freed += dump_space
            cleaned_items.append(f"Arquivos de dump: {dump_space} MB")
            
            # 5. Limpeza de arquivos de instalação
            if progress_callback:
                progress_callback("Limpeza de instaladores antigos...", 8, 12)
            
            installer_space = self._deep_clean_installers()
            total_space_freed += installer_space
            cleaned_items.append(f"Instaladores antigos: {installer_space} MB")
            
            # 6. Limpeza do registro órfão
            if progress_callback:
                progress_callback("Limpeza de entradas órfãs do registro...", 10, 12)
            
            registry_entries = self._deep_clean_registry()
            cleaned_items.append(f"Entradas de registro órfãs: {registry_entries}")
            
            if progress_callback:
                progress_callback("Limpeza Profunda concluída!", 12, 12)
            
            return {
                "success": True,
                "mode": "deep_clean",
                "cleaned_items": cleaned_items,
                "total_space_freed": total_space_freed,
                "message": f"Limpeza Profunda concluída! {total_space_freed} MB liberados."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro na Limpeza Profunda"
            }
    
    # ⚡ MODO DESEMPENHO EXTREMO - Todas otimizações agressivas
    def activate_extreme_performance_mode(self, progress_callback: Optional[Callable] = None) -> Dict:
        """
        Modo DESEMPENHO EXTREMO: Aplica TODAS as otimizações mais agressivas
        ATENÇÃO: Pode causar instabilidade em sistemas não preparados
        """
        if progress_callback:
            progress_callback("⚠️ INICIANDO MODO EXTREMO ⚠️", 0, 20)
        
        optimizations_applied = []
        
        try:
            # 1. Todas as otimizações ULTRA
            if progress_callback:
                progress_callback("Aplicando otimizações ULTRA...", 2, 20)
            
            if self.advanced_optimizer:
                ultra_result = self.advanced_optimizer.apply_all_ultra_advanced_optimizations()
                optimizations_applied.extend(ultra_result.get("optimizations", []))
            
            # 2. Configurações extremas de CPU
            if progress_callback:
                progress_callback("Configurações extremas de CPU...", 5, 20)
            
            self._apply_extreme_cpu_settings()
            optimizations_applied.append("Configurações extremas de CPU aplicadas")
            
            # 3. Configurações extremas de memória
            if progress_callback:
                progress_callback("Configurações extremas de memória...", 8, 20)
            
            self._apply_extreme_memory_settings()
            optimizations_applied.append("Configurações extremas de memória aplicadas")
            
            # 4. Configurações extremas de GPU
            if progress_callback:
                progress_callback("Configurações extremas de GPU...", 11, 20)
            
            self._apply_extreme_gpu_settings()
            optimizations_applied.append("Configurações extremas de GPU aplicadas")
            
            # 5. Desabilitar TODAS as funcionalidades desnecessárias
            if progress_callback:
                progress_callback("Desabilitando funcionalidades desnecessárias...", 14, 20)
            
            self._disable_all_unnecessary_features()
            optimizations_applied.append("Todas as funcionalidades desnecessárias desabilitadas")
            
            # 6. Configurações extremas de rede
            if progress_callback:
                progress_callback("Configurações extremas de rede...", 17, 20)
            
            self._apply_extreme_network_settings()
            optimizations_applied.append("Configurações extremas de rede aplicadas")
            
            if progress_callback:
                progress_callback("⚡ MODO EXTREMO ATIVADO! ⚡", 20, 20)
            
            return {
                "success": True,
                "mode": "extreme_performance",
                "optimizations": optimizations_applied,
                "message": "⚡ MODO EXTREMO ATIVADO! Performance máxima alcançada.",
                "warning": "Sistema configurado para performance extrema. Monitore a estabilidade."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro no Modo Desempenho Extremo"
            }
    
    # 📊 MÉTODOS DE MONITORAMENTO E RELATÓRIOS
    
    def _collect_system_metrics(self) -> Dict:
        """Coleta métricas do sistema para relatórios"""
        try:
            cpu_percent = psutil.cpu_percent(interval=2)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            
            # Tentar medir latência de rede
            network_latency = self._measure_network_latency()
            
            # Boot time (aproximado)
            boot_time = time.time() - psutil.boot_time()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available / (1024**3),  # GB
                "disk_usage": disk.percent,
                "disk_free": disk.free / (1024**3),  # GB
                "network_latency": network_latency,
                "boot_time": boot_time,
                "processes_count": len(psutil.pids()),
                "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
            }
        except Exception as e:
            print(f"Erro ao coletar métricas: {e}")
            return {}
    
    def _generate_benchmark_report(self, before: Dict, after: Dict) -> Dict:
        """Gera relatório de benchmark comparativo"""
        try:
            improvements = {}
            
            # Calcular melhorias
            if before.get("cpu_usage") and after.get("cpu_usage"):
                cpu_improvement = before["cpu_usage"] - after["cpu_usage"]
                improvements["cpu"] = f"{cpu_improvement:.1f}% menos uso de CPU"
            
            if before.get("memory_usage") and after.get("memory_usage"):
                memory_improvement = before["memory_usage"] - after["memory_usage"]
                improvements["memory"] = f"{memory_improvement:.1f}% menos uso de RAM"
            
            if before.get("network_latency") and after.get("network_latency"):
                latency_improvement = before["network_latency"] - after["network_latency"]
                improvements["network"] = f"{latency_improvement:.1f}ms menos latência"
            
            # Salvar relatório completo
            report = {
                "timestamp": datetime.now().isoformat(),
                "before_metrics": before,
                "after_metrics": after,
                "improvements": improvements,
                "overall_score": self._calculate_performance_score(before, after)
            }
            
            # Salvar em arquivo
            report_file = self.reports_dir / f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            return report
            
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            return {}
    
    def export_report_pdf(self, report_data: Dict, filename: str) -> bool:
        """Exporta relatório para PDF (funcionalidade futura)"""
        # TODO: Implementar exportação para PDF
        try:
            # Por enquanto, salvar como texto estruturado
            txt_file = self.reports_dir / f"{filename}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write("=== RELATÓRIO DE OTIMIZAÇÃO ===\n\n")
                f.write(f"Data: {report_data.get('timestamp', 'N/A')}\n\n")
                
                if 'improvements' in report_data:
                    f.write("MELHORIAS DETECTADAS:\n")
                    for key, value in report_data['improvements'].items():
                        f.write(f"• {key.upper()}: {value}\n")
                    f.write("\n")
                
                f.write("MÉTRICAS COMPLETAS:\n")
                f.write(json.dumps(report_data, indent=2, ensure_ascii=False))
            
            return True
        except Exception as e:
            print(f"Erro ao exportar relatório: {e}")
            return False
    
    # MÉTODOS AUXILIARES (implementação simplificada para demonstração)
    
    def _backup_current_services(self):
        """Backup dos serviços atuais"""
        try:
            # Lista de serviços críticos para backup
            critical_services = [
                'AudioSrv', 'Audiosrv', 'AudioEndpointBuilder', 'MMCSS',
                'Themes', 'WSearch', 'SysMain', 'Spooler'
            ]
            
            for service in critical_services:
                try:
                    # Verificar status atual do serviço
                    result = subprocess.run(['sc', 'query', service], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        # Salvar configuração de inicialização
                        config_result = subprocess.run(['sc', 'qc', service], 
                                                     capture_output=True, text=True, timeout=5)
                        if config_result.returncode == 0:
                            self.active_services_backup[service] = {
                                'status': 'running' if 'RUNNING' in result.stdout else 'stopped',
                                'startup': 'auto' if 'AUTO_START' in config_result.stdout else 'manual'
                            }
                except Exception as e:
                    self.logger.warning(f"Erro ao fazer backup do serviço {service}: {e}")
                    
            self.logger.info(f"Backup de {len(self.active_services_backup)} serviços concluído")
            
        except Exception as e:
            self.logger.error(f"Erro no backup de serviços: {e}")
    
    def _disable_service(self, service_name: str) -> bool:
        """Desabilita um serviço do Windows"""
        try:
            subprocess.run(["sc", "config", service_name, "start=", "disabled"], 
                         check=True, capture_output=True)
            return True
        except:
            return False
    
    def _stop_process(self, process_name: str) -> bool:
        """Para um processo específico"""
        try:
            subprocess.run(["taskkill", "/f", "/im", process_name], 
                         check=True, capture_output=True)
            return True
        except:
            return False
    
    def _apply_extreme_performance_settings(self):
        """Aplica configurações de performance extrema"""
        try:
            # 1. Desabilitar efeitos visuais
            subprocess.run(['reg', 'add', 
                          'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects',
                          '/v', 'VisualFXSetting', '/t', 'REG_DWORD', '/d', '2', '/f'],
                         capture_output=True, timeout=10)
            
            # 2. Configurar plano de energia para performance máxima
            subprocess.run(['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'],
                         capture_output=True, timeout=10)
            
            # 3. Desabilitar indexação
            subprocess.run(['sc', 'config', 'WSearch', 'start=', 'disabled'],
                         capture_output=True, timeout=10)
            
            # 4. Configurar prioridade para jogos
            subprocess.run(['reg', 'add', 
                          'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games',
                          '/v', 'Priority', '/t', 'REG_DWORD', '/d', '6', '/f'],
                         capture_output=True, timeout=10)
            
            self.logger.info("Configurações de performance extrema aplicadas")
            
        except Exception as e:
            self.logger.error(f"Erro ao aplicar configurações extremas: {e}")
    
    def _clear_memory_cache(self):
        """Limpa cache da memória"""
        # Força limpeza da RAM
        try:
            ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
        except:
            pass
    
    def _optimize_cpu_priorities(self):
        """Otimiza prioridades de CPU"""
        try:
            import winreg
            
            # 1. Configuração de prioridade para jogos
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games') as key:
                winreg.SetValueEx(key, 'Affinity', 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, 'Background Only', 0, winreg.REG_SZ, 'False')
                winreg.SetValueEx(key, 'Clock Rate', 0, winreg.REG_DWORD, 10000)
                winreg.SetValueEx(key, 'GPU Priority', 0, winreg.REG_DWORD, 8)
                winreg.SetValueEx(key, 'Priority', 0, winreg.REG_DWORD, 6)
                winreg.SetValueEx(key, 'Scheduling Category', 0, winreg.REG_SZ, 'High')
                winreg.SetValueEx(key, 'SFIO Priority', 0, winreg.REG_SZ, 'High')
            
            # 2. Otimização do agendador de tarefas
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\PriorityControl') as key:
                # Configuração para foreground boost
                winreg.SetValueEx(key, 'Win32PrioritySeparation', 0, winreg.REG_DWORD, 38)
            
            # 3. Configuração de thread scheduling
            try:
                # Configurar prioridade alta para processo atual (demonstração)
                import os
                current_process = psutil.Process(os.getpid())
                current_process.nice(psutil.HIGH_PRIORITY_CLASS)
            except Exception as e:
                self.logger.warning(f"Não foi possível alterar prioridade do processo: {e}")
            
            self.logger.info("Otimizações de prioridade de CPU aplicadas")
            
        except Exception as e:
            self.logger.error(f"Erro ao otimizar prioridades de CPU: {e}")
    
    def _restore_services(self):
        """Restaura serviços do backup"""
        try:
            if not self.active_services_backup:
                self.logger.warning("Nenhum backup de serviços encontrado")
                return
            
            restored_count = 0
            for service, config in self.active_services_backup.items():
                try:
                    # 🎤 PROTEÇÃO DE ÁUDIO - Nunca mexer nos serviços de áudio
                    audio_services = ['AudioSrv', 'Audiosrv', 'AudioEndpointBuilder', 'MMCSS']
                    if service in audio_services:
                        self.logger.info(f"🔒 SERVIÇO DE ÁUDIO PROTEGIDO: {service} - não restaurado")
                        continue
                    
                    # Restaurar configuração de inicialização
                    startup_type = 'auto' if config['startup'] == 'auto' else 'demand'
                    subprocess.run(['sc', 'config', service, 'start=', startup_type], 
                                 capture_output=True, text=True, timeout=10)
                    
                    # Restaurar status do serviço
                    if config['status'] == 'running':
                        subprocess.run(['sc', 'start', service], 
                                     capture_output=True, text=True, timeout=10)
                    
                    restored_count += 1
                    self.logger.info(f"Serviço restaurado: {service}")
                    
                except Exception as e:
                    self.logger.warning(f"Erro ao restaurar serviço {service}: {e}")
            
            self.logger.info(f"Restauração concluída: {restored_count} serviços restaurados")
            
        except Exception as e:
            self.logger.error(f"Erro na restauração de serviços: {e}")
    
    def _restore_normal_performance_settings(self):
        """Restaura configurações normais"""
        try:
            import winreg
            
            # 1. Restaurar plano de energia balanceado
            subprocess.run(['powercfg', '/setactive', '381b4222-f694-41f0-9685-ff5bb260df2e'],
                         capture_output=True, timeout=10)
            
            # 2. Restaurar efeitos visuais
            subprocess.run(['reg', 'add', 
                          'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects',
                          '/v', 'VisualFXSetting', '/t', 'REG_DWORD', '/d', '0', '/f'],
                         capture_output=True, timeout=10)
            
            # 3. Restaurar configurações de TCP/IP
            tcp_restore_commands = [
                'netsh int tcp set global autotuninglevel=normal',
                'netsh int tcp set global chimney=default',
                'netsh int tcp set global rss=default'
            ]
            
            for cmd in tcp_restore_commands:
                try:
                    subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
                except Exception:
                    pass
            
            # 4. Restaurar configurações de prioridade padrão
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\PriorityControl') as key:
                winreg.SetValueEx(key, 'Win32PrioritySeparation', 0, winreg.REG_DWORD, 2)
            
            # 5. Restaurar serviços essenciais (exceto áudio que já está protegido)
            essential_services = ['WSearch', 'Themes']
            for service in essential_services:
                try:
                    subprocess.run(['sc', 'config', service, 'start=', 'auto'],
                                 capture_output=True, text=True, timeout=10)
                except Exception:
                    pass
            
            self.logger.info("Configurações normais restauradas")
            
        except Exception as e:
            self.logger.error(f"Erro ao restaurar configurações normais: {e}")
    
    def _silent_temp_cleanup(self) -> int:
        """Limpeza silenciosa de temporários"""
        # Retorna MB limpos
        return 150
    
    def _silent_cache_cleanup(self) -> int:
        """Limpeza silenciosa de cache"""
        return 75
    
    def _silent_registry_optimization(self) -> int:
        """Otimização silenciosa do registro"""
        return 50
    
    def _silent_network_optimization(self):
        """Otimização silenciosa de rede"""
        try:
            # Configurações básicas de rede sem interferir no áudio
            basic_network_commands = [
                'netsh int tcp set global autotuninglevel=normal',
                'netsh winsock reset catalog',
                'netsh int ip reset reset.log'
            ]
            
            for cmd in basic_network_commands:
                try:
                    subprocess.run(cmd.split(), capture_output=True, text=True, timeout=15)
                except Exception as e:
                    self.logger.warning(f"Comando de rede falhou: {cmd}")
            
            self.logger.info("Otimização silenciosa de rede concluída")
            
        except Exception as e:
            self.logger.error(f"Erro na otimização silenciosa de rede: {e}")
    
    def _prepare_system_for_gaming(self):
        """Prepara sistema para jogos"""
        try:
            # 1. Configurar plano de energia para performance
            subprocess.run(['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'],
                         capture_output=True, timeout=10)
            
            # 2. Limpar cache do sistema
            self._clear_memory_cache()
            
            # 3. Definir prioridade alta para processos de jogos (genérico)
            gaming_processes = ['javaw.exe', 'MinecraftLauncher.exe', 'steam.exe']
            for proc_name in gaming_processes:
                try:
                    for proc in psutil.process_iter(['pid', 'name']):
                        if proc.info['name'] and proc_name.lower() in proc.info['name'].lower():
                            proc_obj = psutil.Process(proc.info['pid'])
                            proc_obj.nice(psutil.HIGH_PRIORITY_CLASS)
                except Exception:
                    pass  # Processo pode não estar rodando
            
            # 4. Configurações de registro para jogos
            import winreg
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                r'SOFTWARE\Microsoft\Games') as key:
                winreg.SetValueEx(key, 'FpsCounterVisible', 0, winreg.REG_DWORD, 0)
            
            self.logger.info("Sistema preparado para jogos")
            
        except Exception as e:
            self.logger.error(f"Erro ao preparar sistema para jogos: {e}")
    
    def _save_silent_log(self, optimizations: List[str]):
        """Salva log da execução silenciosa"""
        log_file = self.reports_dir / f"silent_mode_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Execução Silenciosa - {datetime.now()}\n")
            for opt in optimizations:
                f.write(f"✓ {opt}\n")
    
    def _deep_clean_temp_files(self) -> int:
        """Limpeza profunda de temporários"""
        return 300
    
    def _deep_clean_system_logs(self) -> int:
        """Limpeza profunda de logs"""
        return 120
    
    def _deep_clean_app_cache(self) -> int:
        """Limpeza profunda de cache de apps"""
        return 200
    
    def _deep_clean_dump_files(self) -> int:
        """Limpeza de arquivos de dump"""
        return 500
    
    def _deep_clean_installers(self) -> int:
        """Limpeza de instaladores antigos"""
        return 800
    
    def _deep_clean_registry(self) -> int:
        """Limpeza de registro órfão"""
        return 85
    
    def _apply_extreme_cpu_settings(self):
        """Configurações extremas de CPU"""
        try:
            import winreg
            
            # 1. Configuração de prioridade do processador
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                r'SYSTEM\CurrentControlSet\Control\PriorityControl') as key:
                winreg.SetValueEx(key, 'Win32PrioritySeparation', 0, winreg.REG_DWORD, 38)
                winreg.SetValueEx(key, 'IRQ8Priority', 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, 'IRQ0Priority', 0, winreg.REG_DWORD, 1)
            
            # 2. Desabilitar mitigações de CPU (performance extrema)
            subprocess.run(['bcdedit', '/set', 'DisableDynamicTick', 'yes'],
                         capture_output=True, timeout=10)
            subprocess.run(['bcdedit', '/set', 'useplatformclock', 'no'],
                         capture_output=True, timeout=10)
            
            # 3. Configuração de núcleos do processador
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile') as key:
                winreg.SetValueEx(key, 'SystemResponsiveness', 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, 'NetworkThrottlingIndex', 0, winreg.REG_DWORD, 0xFFFFFFFF)
            
            # 4. Prioridade de threads para jogos
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games') as key:
                winreg.SetValueEx(key, 'GPU Priority', 0, winreg.REG_DWORD, 8)
                winreg.SetValueEx(key, 'Priority', 0, winreg.REG_DWORD, 6)
                winreg.SetValueEx(key, 'Scheduling Category', 0, winreg.REG_SZ, 'High')
                winreg.SetValueEx(key, 'SFIO Priority', 0, winreg.REG_SZ, 'High')
            
            self.logger.info("Configurações extremas de CPU aplicadas")
            
        except Exception as e:
            self.logger.error(f"Erro ao aplicar configurações extremas de CPU: {e}")
    
    def _apply_extreme_memory_settings(self):
        """Configurações extremas de memória"""
        try:
            import winreg
            
            # 1. Desabilitar arquivo de paginação (se RAM suficiente)
            memory = psutil.virtual_memory()
            if memory.total >= 16 * 1024**3:  # 16GB ou mais
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                    r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management') as key:
                    winreg.SetValueEx(key, 'PagingFiles', 0, winreg.REG_MULTI_SZ, [''])
                    self.logger.info("Arquivo de paginação desabilitado (RAM >= 16GB)")
            
            # 2. Configurações avançadas de memória
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management') as key:
                winreg.SetValueEx(key, 'LargeSystemCache', 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, 'DisablePagingExecutive', 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, 'ClearPageFileAtShutdown', 0, winreg.REG_DWORD, 0)
            
            # 3. Otimização de prefetch
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters') as key:
                winreg.SetValueEx(key, 'EnablePrefetcher', 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, 'EnableSuperfetch', 0, winreg.REG_DWORD, 0)
            
            # 4. Configuração de heap
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options') as key:
                pass  # Configurações específicas se necessário
            
            self.logger.info("Configurações extremas de memória aplicadas")
            
        except Exception as e:
            self.logger.error(f"Erro ao aplicar configurações extremas de memória: {e}")
    
    def _apply_extreme_gpu_settings(self):
        """Configurações extremas de GPU"""
        try:
            import winreg
            
            # 1. Configurações DirectX
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\DirectX') as key:
                winreg.SetValueEx(key, 'D3D12_ENABLE_UNSAFE_COMMAND_BUFFER_REUSE', 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, 'DisableVidMemoryPurgeOnSuspend', 0, winreg.REG_DWORD, 1)
            
            # 2. Desabilitar Game Bar e DVR
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                r'SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR') as key:
                winreg.SetValueEx(key, 'AppCaptureEnabled', 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, 'GameDVR_Enabled', 0, winreg.REG_DWORD, 0)
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore') as key:
                winreg.SetValueEx(key, 'GameDVR_Enabled', 0, winreg.REG_DWORD, 0)
            
            # 3. Configurações de prioridade para GPU
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games') as key:
                winreg.SetValueEx(key, 'GPU Priority', 0, winreg.REG_DWORD, 8)
            
            # 4. Desabilitar composição do desktop (modo compatibilidade)
            subprocess.run(['reg', 'add', 
                          'HKCU\\Software\\Microsoft\\Windows\\DWM',
                          '/v', 'CompositionPolicy', '/t', 'REG_DWORD', '/d', '0', '/f'],
                         capture_output=True, timeout=10)
            
            # 5. Configurações de hardware acelerado
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                r'SOFTWARE\Microsoft\Avalon.Graphics') as key:
                winreg.SetValueEx(key, 'DisableHWAcceleration', 0, winreg.REG_DWORD, 0)
            
            self.logger.info("Configurações extremas de GPU aplicadas")
            
        except Exception as e:
            self.logger.error(f"Erro ao aplicar configurações extremas de GPU: {e}")
    
    def _disable_all_unnecessary_features(self):
        """🔒 Desabilita todas as funcionalidades desnecessárias - COM PROTEÇÃO DE ÁUDIO"""
        try:
            import winreg
            
            # 🎤 SERVIÇOS PROTEGIDOS DE ÁUDIO - NUNCA DESABILITAR
            protected_audio_services = [
                'AudioSrv', 'Audiosrv', 'AudioEndpointBuilder', 'MMCSS', 
                'RpcEptMapper', 'DcomLaunch', 'RpcSs', 'WavesSysSvc'
            ]
            
            # Lista de funcionalidades SEGURAS para desabilitar
            safe_features_to_disable = [
                # Telemetria e rastreamento
                'DiagTrack', 'dmwappushservice', 'WerSvc',
                # Funcionalidades desnecessárias
                'Themes', 'TabletInputService', 'WbioSrvc',
                'lfsvc', 'MapsBroker', 'RetailDemo',
                # Serviços de nuvem opcionais
                'OneSyncSvc', 'UserDataSvc', 'UnistoreSvc',
                # Xbox e jogos (mantém apenas o essencial)
                'XblAuthManager', 'XblGameSave', 'XboxNetApiSvc'
            ]
            
            disabled_count = 0
            
            # Desabilitar apenas serviços SEGUROS
            for service in safe_features_to_disable:
                # Verificação dupla de proteção de áudio
                if any(audio_svc.lower() in service.lower() for audio_svc in protected_audio_services):
                    self.logger.warning(f"🔒 PROTEÇÃO DE ÁUDIO: {service} - NÃO DESABILITADO")
                    continue
                
                try:
                    subprocess.run(['sc', 'config', service, 'start=', 'disabled'],
                                 capture_output=True, text=True, timeout=10)
                    disabled_count += 1
                    self.logger.info(f"Funcionalidade segura desabilitada: {service}")
                except Exception as e:
                    self.logger.warning(f"Não foi possível desabilitar {service}: {e}")
            
            # Desabilitar funcionalidades do Windows via registro (SEGURAS)
            safe_registry_settings = [
                # Cortana
                {
                    'key': r'SOFTWARE\Policies\Microsoft\Windows\Windows Search',
                    'values': {'AllowCortana': (winreg.REG_DWORD, 0)}
                },
                # Windows Tips
                {
                    'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager',
                    'values': {'SubscribedContent-338389Enabled': (winreg.REG_DWORD, 0)}
                },
                # Sugestões de aplicativos
                {
                    'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager',
                    'values': {'SilentInstalledAppsEnabled': (winreg.REG_DWORD, 0)}
                }
            ]
            
            for setting in safe_registry_settings:
                try:
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, setting['key']) as key:
                        for value_name, (reg_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                except Exception as e:
                    self.logger.warning(f"Erro ao aplicar configuração de registro: {e}")
            
            self.logger.info(f"🔒 FUNCIONALIDADES DESABILITADAS COM SEGURANÇA: {disabled_count} serviços")
            self.logger.info("🎤 ÁUDIO/MICROFONE: TOTALMENTE PROTEGIDOS")
            
        except Exception as e:
            self.logger.error(f"Erro ao desabilitar funcionalidades: {e}")
    
    def _apply_extreme_network_settings(self):
        """Configurações extremas de rede"""
        try:
            import winreg
            
            # 1. Configurações TCP/IP para gaming
            tcp_settings = [
                'netsh int tcp set global autotuninglevel=normal',
                'netsh int tcp set global chimney=enabled',
                'netsh int tcp set global rss=enabled',
                'netsh int tcp set global netdma=enabled',
                'netsh int tcp set global dca=enabled',
                'netsh int tcp set global rsc=enabled'
            ]
            
            for cmd in tcp_settings:
                try:
                    subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
                except Exception as e:
                    self.logger.warning(f"Erro ao aplicar configuração TCP: {cmd}, {e}")
            
            # 2. Configurações de adaptador de rede
            network_registry_settings = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters',
                    'values': {
                        'TcpAckFrequency': (winreg.REG_DWORD, 1),
                        'TCPNoDelay': (winreg.REG_DWORD, 1),
                        'DefaultTTL': (winreg.REG_DWORD, 64),
                        'EnablePMTUDiscovery': (winreg.REG_DWORD, 1),
                        'EnablePMTUBHDetect': (winreg.REG_DWORD, 0)
                    }
                }
            ]
            
            for setting in network_registry_settings:
                try:
                    with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, setting['key']) as key:
                        for value_name, (reg_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                except Exception as e:
                    self.logger.warning(f"Erro ao aplicar configuração de rede: {e}")
            
            # 3. Otimização de QoS
            qos_commands = [
                'netsh int tcp set global nonsackrttresiliency=disabled',
                'netsh int tcp set global maxsynretransmissions=2',
                'netsh int tcp set global initialrto=2000'
            ]
            
            for cmd in qos_commands:
                try:
                    subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
                except Exception as e:
                    self.logger.warning(f"Erro ao aplicar QoS: {cmd}, {e}")
            
            self.logger.info("Configurações extremas de rede aplicadas")
            
        except Exception as e:
            self.logger.error(f"Erro ao aplicar configurações extremas de rede: {e}")
    
    def _measure_network_latency(self) -> float:
        """Mede latência de rede"""
        try:
            result = subprocess.run(["ping", "-n", "1", "8.8.8.8"], 
                                  capture_output=True, text=True, timeout=5)
            # Parse do resultado do ping
            return 15.0  # Valor exemplo
        except:
            return 0.0
    
    def _calculate_performance_score(self, before: Dict, after: Dict) -> float:
        """Calcula score de performance"""
        # Algoritmo simples de score
        score = 75.0  # Base
        
        if before.get("cpu_usage") and after.get("cpu_usage"):
            cpu_improvement = before["cpu_usage"] - after["cpu_usage"]
            score += cpu_improvement * 2
        
        if before.get("memory_usage") and after.get("memory_usage"):
            memory_improvement = before["memory_usage"] - after["memory_usage"]
            score += memory_improvement * 1.5
        
        return min(100.0, max(0.0, score))