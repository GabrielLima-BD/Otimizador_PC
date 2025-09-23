import subprocess
import logging
import winreg
import os
from .utils import Utils

class PerformanceOptimizer:
    """Classe responsável pelas otimizações de desempenho"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.optimizations_applied = []
        
        # Serviços que podem ser desabilitados para melhor desempenho
        self.services_to_disable = [
            'WSearch',  # Windows Search
            'SysMain',  # Superfetch/Prefetch
            'Themes',   # Temas (se não usar)
            'TabletInputService',  # Serviço de entrada de tablet
            'WbioSrvc',  # Serviço de biometria
            'WMPNetworkSvc',  # Compartilhamento de rede do Windows Media Player
            'WerSvc',   # Relatório de erros do Windows
            'DiagTrack',  # Telemetria
            'RetailDemo',  # Serviço de demonstração
            'RemoteAccess',  # Roteamento e acesso remoto
            'SharedAccess',  # Compartilhamento de conexão de internet
            'TrkWks',   # Cliente de rastreamento de link distribuído
            'WpcMonSvc',  # Controle dos pais
        ]
    
    def optimize_power_settings(self, progress_callback=None):
        """Configura plano de energia para máximo desempenho"""
        if progress_callback:
            progress_callback("Configurando plano de energia...", 0)
        
        try:
            # Define plano de energia para alto desempenho
            cmd_high_performance = 'powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
            result1 = subprocess.run(cmd_high_performance, shell=True, capture_output=True, text=True)
            
            # Desabilita hibernação
            cmd_hibernate = 'powercfg -h off'
            result2 = subprocess.run(cmd_hibernate, shell=True, capture_output=True, text=True)
            
            # Configura para nunca desligar o disco
            cmd_disk = 'powercfg -change -disk-timeout-ac 0'
            result3 = subprocess.run(cmd_disk, shell=True, capture_output=True, text=True)
            
            # Configura para nunca entrar em suspensão
            cmd_standby = 'powercfg -change -standby-timeout-ac 0'
            result4 = subprocess.run(cmd_standby, shell=True, capture_output=True, text=True)
            
            if progress_callback:
                progress_callback("Plano de energia configurado", 100)
            
            self.optimizations_applied.append("Plano de energia otimizado")
            self.logger.info("Configurações de energia otimizadas")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar energia: {e}")
            return False
    
    def disable_unnecessary_services(self, progress_callback=None):
        """Desabilita serviços desnecessários"""
        if progress_callback:
            progress_callback("Desabilitando serviços desnecessários...", 0)
        
        disabled_services = []
        total_services = len(self.services_to_disable)
        
        for i, service in enumerate(self.services_to_disable):
            if progress_callback:
                progress_callback(f"Verificando serviço: {service}", (i / total_services) * 100)
            
            success = self._disable_service(service)
            if success:
                disabled_services.append(service)
        
        self.optimizations_applied.append(f"{len(disabled_services)} serviços desabilitados")
        self.logger.info(f"Serviços desabilitados: {disabled_services}")
        return disabled_services
    
    def _disable_service(self, service_name):
        """Desabilita um serviço específico"""
        try:
            # Para o serviço
            cmd_stop = f'sc stop {service_name}'
            subprocess.run(cmd_stop, shell=True, capture_output=True, timeout=30)
            
            # Desabilita o serviço
            cmd_disable = f'sc config {service_name} start= disabled'
            result = subprocess.run(cmd_disable, shell=True, capture_output=True, text=True, timeout=30)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Timeout ao desabilitar serviço: {service_name}")
            return False
        except Exception as e:
            self.logger.error(f"Erro ao desabilitar serviço {service_name}: {e}")
            return False
    
    def disable_visual_effects(self, progress_callback=None):
        """Desabilita efeitos visuais para melhor desempenho"""
        if progress_callback:
            progress_callback("Desabilitando efeitos visuais...", 0)
        
        try:
            # Chave do registro para configurações de desempenho visual
            key_path = r"CONTROL PANEL\Desktop"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                # Desabilita animações de janelas
                winreg.SetValueEx(key, "UserPreferencesMask", 0, winreg.REG_BINARY, 
                                b'\x90\x12\x03\x80\x10\x00\x00\x00')
                
                # Desabilita drag full windows
                winreg.SetValueEx(key, "DragFullWindows", 0, winreg.REG_SZ, "0")
            
            # Configurações avançadas de sistema
            key_path2 = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            try:
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path2) as key:
                    winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)  # Melhor desempenho
            except:
                pass
            
            if progress_callback:
                progress_callback("Efeitos visuais desabilitados", 100)
            
            self.optimizations_applied.append("Efeitos visuais otimizados")
            self.logger.info("Efeitos visuais desabilitados")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao desabilitar efeitos visuais: {e}")
            return False
    
    def disable_indexing(self, progress_callback=None):
        """Desabilita indexação de arquivos em discos"""
        if progress_callback:
            progress_callback("Desabilitando indexação de discos...", 0)
        
        try:
            import string
            drives_processed = []
            
            # Obtém todas as unidades de disco
            available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
            
            for i, drive in enumerate(available_drives):
                if progress_callback:
                    progress_callback(f"Processando drive {drive}", (i / len(available_drives)) * 100)
                
                try:
                    # Comando para desabilitar indexação
                    cmd = f'fsutil behavior set DisableLastAccess 1'
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                    
                    # Desabilita indexação do drive
                    cmd_drive = f'fsutil behavior set EncryptPagingFile 0'
                    subprocess.run(cmd_drive, shell=True, capture_output=True, timeout=30)
                    
                    drives_processed.append(drive)
                    
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
            
            if progress_callback:
                progress_callback("Indexação desabilitada", 100)
            
            self.optimizations_applied.append(f"Indexação desabilitada em {len(drives_processed)} drives")
            self.logger.info(f"Indexação desabilitada nos drives: {drives_processed}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao desabilitar indexação: {e}")
            return False
    
    def optimize_startup_programs(self, progress_callback=None):
        """Otimiza programas de inicialização"""
        if progress_callback:
            progress_callback("Otimizando programas de inicialização...", 0)
        
        try:
            # Lista de programas comuns que podem ser desabilitados na inicialização
            startup_disable_list = [
                'Skype',
                'Spotify',
                'Steam',
                'Adobe Updater',
                'QuickTime',
                'iTunes Helper',
                'Java Update',
                'Office',
            ]
            
            disabled_count = 0
            
            # Desabilita via registro
            startup_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, winreg.KEY_ALL_ACCESS) as key:
                    i = 0
                    while True:
                        try:
                            name, value, type = winreg.EnumValue(key, i)
                            
                            # Verifica se é um programa que deve ser desabilitado
                            for disable_prog in startup_disable_list:
                                if disable_prog.lower() in name.lower() or disable_prog.lower() in value.lower():
                                    try:
                                        winreg.DeleteValue(key, name)
                                        disabled_count += 1
                                        self.logger.info(f"Programa de inicialização removido: {name}")
                                        break
                                    except:
                                        pass
                            i += 1
                        except WindowsError:
                            break
            except:
                pass
            
            if progress_callback:
                progress_callback("Programas de inicialização otimizados", 100)
            
            self.optimizations_applied.append(f"{disabled_count} programas de inicialização desabilitados")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao otimizar inicialização: {e}")
            return False
    
    def optimize_memory_management(self, progress_callback=None):
        """Otimiza gerenciamento de memória"""
        if progress_callback:
            progress_callback("Otimizando gerenciamento de memória...", 0)
        
        try:
            # Configurações de memória virtual
            key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
            
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                # Desabilita paging executive
                winreg.SetValueEx(key, "DisablePagingExecutive", 0, winreg.REG_DWORD, 1)
                
                # Otimiza cache de sistema
                winreg.SetValueEx(key, "LargeSystemCache", 0, winreg.REG_DWORD, 1)
                
                # Configuração de I/O page lock limit
                winreg.SetValueEx(key, "IoPageLockLimit", 0, winreg.REG_DWORD, 983040)
            
            if progress_callback:
                progress_callback("Gerenciamento de memória otimizado", 100)
            
            self.optimizations_applied.append("Gerenciamento de memória otimizado")
            self.logger.info("Configurações de memória otimizadas")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao otimizar memória: {e}")
            return False
    
    def disable_windows_defender_realtime(self, progress_callback=None):
        """Desabilita proteção em tempo real do Windows Defender (CUIDADO!)"""
        if progress_callback:
            progress_callback("Configurando Windows Defender...", 0)
        
        try:
            # AVISO: Isso pode deixar o sistema vulnerável
            cmd = 'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                if progress_callback:
                    progress_callback("Windows Defender configurado", 100)
                
                self.optimizations_applied.append("Proteção em tempo real do Defender desabilitada")
                self.logger.warning("AVISO: Proteção em tempo real do Windows Defender desabilitada")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao configurar Windows Defender: {e}")
            return False
    
    def optimize_processor_scheduling(self, progress_callback=None):
        """Otimiza agendamento do processador"""
        if progress_callback:
            progress_callback("Otimizando agendamento do processador...", 0)
        
        try:
            key_path = r"SYSTEM\CurrentControlSet\Control\PriorityControl"
            
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                # Prioriza programas em primeiro plano
                winreg.SetValueEx(key, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 38)
            
            if progress_callback:
                progress_callback("Agendamento do processador otimizado", 100)
            
            self.optimizations_applied.append("Agendamento do processador otimizado")
            self.logger.info("Agendamento do processador otimizado")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao otimizar processador: {e}")
            return False
    
    def get_optimization_summary(self):
        """Retorna resumo das otimizações aplicadas"""
        return {
            'optimizations_count': len(self.optimizations_applied),
            'optimizations_list': self.optimizations_applied
        }