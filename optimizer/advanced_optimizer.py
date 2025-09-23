import os
import subprocess
import logging
import psutil
import winreg
from .utils import Utils

class AdvancedOptimizer:
    """Sistema de otimizações avançadas do Windows"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.optimizations_applied = []
    
    def optimize_memory_management(self, progress_callback=None):
        """Otimiza gerenciamento de memória do sistema"""
        if progress_callback:
            progress_callback("Otimizando gerenciamento de memória...", 0)
        
        optimizations = []
        
        try:
            # Configurações de memória virtual
            memory_settings = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
                    'values': {
                        'ClearPageFileAtShutdown': (winreg.REG_DWORD, 0),  # Não limpar pagefile ao desligar
                        'DisablePagingExecutive': (winreg.REG_DWORD, 1),  # Manter kernel na RAM
                        'LargeSystemCache': (winreg.REG_DWORD, 1),  # Cache maior para sistema
                        'SystemPages': (winreg.REG_DWORD, 0xFFFFFFFF),  # Otimizar páginas do sistema
                    }
                },
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters',
                    'values': {
                        'EnablePrefetcher': (winreg.REG_DWORD, 3),  # Prefetch otimizado
                        'EnableSuperfetch': (winreg.REG_DWORD, 3),  # Superfetch ativo
                        'EnableBootTrace': (winreg.REG_DWORD, 0),  # Desabilitar trace de boot
                    }
                }
            ]
            
            for i, setting in enumerate(memory_settings):
                if progress_callback:
                    progress = (i / len(memory_settings)) * 50
                    progress_callback(f"Aplicando configuração de memória {i+1}/{len(memory_settings)}", progress)
                
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            optimizations.append(f"Memória: {value_name} configurado")
                except Exception as e:
                    self.logger.warning(f"Erro ao configurar {setting['key']}: {e}")
            
            if progress_callback:
                progress_callback("Configurações de memória aplicadas", 50)
            
        except Exception as e:
            self.logger.error(f"Erro na otimização de memória: {e}")
        
        return optimizations
    
    def optimize_cpu_scheduling(self, progress_callback=None):
        """Otimiza agendamento de CPU e prioridades"""
        if progress_callback:
            progress_callback("Otimizando agendamento de CPU...", 0)
        
        optimizations = []
        
        try:
            # Configurações de CPU e agendamento
            cpu_settings = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\PriorityControl',
                    'values': {
                        'Win32PrioritySeparation': (winreg.REG_DWORD, 38),  # Prioridade para foreground
                        'IRQ8Priority': (winreg.REG_DWORD, 1),  # Prioridade alta para timer
                        'IRQ0Priority': (winreg.REG_DWORD, 1),  # Prioridade alta para sistema
                    }
                },
                {
                    'key': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile',
                    'values': {
                        'SystemResponsiveness': (winreg.REG_DWORD, 10),  # Responsividade do sistema
                        'NetworkThrottlingIndex': (winreg.REG_DWORD, 0xFFFFFFFF),  # Sem throttling de rede
                    }
                }
            ]
            
            for i, setting in enumerate(cpu_settings):
                if progress_callback:
                    progress = (i / len(cpu_settings)) * 100
                    progress_callback(f"Aplicando configuração de CPU {i+1}/{len(cpu_settings)}", progress)
                
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            optimizations.append(f"CPU: {value_name} configurado")
                except Exception as e:
                    self.logger.warning(f"Erro ao configurar {setting['key']}: {e}")
            
            if progress_callback:
                progress_callback("Otimização de CPU concluída", 100)
            
        except Exception as e:
            self.logger.error(f"Erro na otimização de CPU: {e}")
        
        return optimizations
    
    def optimize_storage_performance(self, progress_callback=None):
        """Otimiza performance de armazenamento"""
        if progress_callback:
            progress_callback("Otimizando armazenamento...", 0)
        
        optimizations = []
        
        try:
            # Detectar drives SSD
            ssd_drives = self._detect_ssd_drives()
            
            if progress_callback:
                progress_callback("Detectando drives SSD...", 25)
            
            # Configurações para SSDs
            if ssd_drives:
                for drive in ssd_drives:
                    try:
                        # Desabilitar desfragmentação automática em SSDs
                        cmd = f'schtasks /change /tn "Microsoft\\Windows\\Defrag\\ScheduledDefrag" /disable'
                        subprocess.run(cmd, shell=True, capture_output=True)
                        optimizations.append("Desfragmentação automática desabilitada para SSDs")
                        
                        # Configurar TRIM
                        cmd = f'fsutil behavior set DisableDeleteNotify 0'
                        result = subprocess.run(cmd, shell=True, capture_output=True)
                        if result.returncode == 0:
                            optimizations.append("TRIM habilitado para SSDs")
                        
                    except Exception as e:
                        self.logger.warning(f"Erro ao otimizar SSD {drive}: {e}")
            
            if progress_callback:
                progress_callback("Configurando sistema de arquivos...", 50)
            
            # Configurações gerais de armazenamento
            storage_settings = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\FileSystem',
                    'values': {
                        'NtfsDisableLastAccessUpdate': (winreg.REG_DWORD, 1),  # Desabilitar LastAccess
                        'NtfsDisable8dot3NameCreation': (winreg.REG_DWORD, 1),  # Desabilitar nomes 8.3
                        'NtfsEncryptionService': (winreg.REG_DWORD, 1),  # Otimizar criptografia
                    }
                }
            ]
            
            for setting in storage_settings:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            optimizations.append(f"Armazenamento: {value_name} configurado")
                except Exception as e:
                    self.logger.warning(f"Erro ao configurar sistema de arquivos: {e}")
            
            if progress_callback:
                progress_callback("Otimização de armazenamento concluída", 100)
            
        except Exception as e:
            self.logger.error(f"Erro na otimização de armazenamento: {e}")
        
        return optimizations
    
    def optimize_gaming_performance(self, progress_callback=None):
        """Otimizações específicas para jogos"""
        if progress_callback:
            progress_callback("Aplicando otimizações para jogos...", 0)
        
        optimizations = []
        
        try:
            # Configurações para jogos
            gaming_settings = [
                {
                    'key': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games',
                    'values': {
                        'GPU Priority': (winreg.REG_DWORD, 8),  # Prioridade alta para GPU
                        'Priority': (winreg.REG_DWORD, 6),  # Prioridade alta para jogos
                        'Scheduling Category': (winreg.REG_SZ, 'High'),  # Categoria alta
                        'SFIO Priority': (winreg.REG_SZ, 'High'),  # I/O prioritário
                    }
                },
                {
                    'key': r'SOFTWARE\Microsoft\DirectX',
                    'values': {
                        'D3D12_ENABLE_UNSAFE_COMMAND_BUFFER_REUSE': (winreg.REG_DWORD, 1),  # Otimizar DirectX12
                        'DisableVidMemoryPurgeOnSuspend': (winreg.REG_DWORD, 1),  # Manter VRAM
                    }
                }
            ]
            
            for i, setting in enumerate(gaming_settings):
                if progress_callback:
                    progress = (i / len(gaming_settings)) * 70
                    progress_callback(f"Aplicando configuração de jogos {i+1}/{len(gaming_settings)}", progress)
                
                try:
                    # Criar chave se não existir
                    winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, setting['key'])
                    
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            optimizations.append(f"Gaming: {value_name} configurado")
                except Exception as e:
                    self.logger.warning(f"Erro ao configurar jogos {setting['key']}: {e}")
            
            if progress_callback:
                progress_callback("Configurando Game Mode...", 80)
            
            # Habilitar Game Mode
            try:
                game_mode_key = r'SOFTWARE\Microsoft\GameBar'
                winreg.CreateKey(winreg.HKEY_CURRENT_USER, game_mode_key)
                
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, game_mode_key, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, 'AllowAutoGameMode', 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, 'AutoGameModeEnabled', 0, winreg.REG_DWORD, 1)
                    optimizations.append("Game Mode habilitado")
            except Exception as e:
                self.logger.warning(f"Erro ao configurar Game Mode: {e}")
            
            if progress_callback:
                progress_callback("Otimizações para jogos concluídas", 100)
            
        except Exception as e:
            self.logger.error(f"Erro nas otimizações para jogos: {e}")
        
        return optimizations
    
    def optimize_startup_programs(self, progress_callback=None):
        """Otimiza programas de inicialização"""
        if progress_callback:
            progress_callback("Otimizando programas de inicialização...", 0)
        
        optimizations = []
        
        # Programas comuns que podem ser desabilitados na inicialização
        startup_blacklist = [
            'Adobe Updater',
            'iTunes Helper',
            'QuickTime Task',
            'Java Update Scheduler',
            'Spotify',
            'Skype',
            'Teams',
            'Office Click-to-Run',
            'OneDrive',
            'Steam',
            'Epic Games Launcher',
            'CCleaner',
            'Acrobat Assistant'
        ]
        
        try:
            # Verificar programas de inicialização do usuário
            startup_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
            
            if progress_callback:
                progress_callback("Analisando programas de inicialização...", 25)
            
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            
                            # Verificar se o programa está na blacklist
                            for blacklisted in startup_blacklist:
                                if blacklisted.lower() in name.lower() or blacklisted.lower() in value.lower():
                                    try:
                                        winreg.DeleteValue(key, name)
                                        optimizations.append(f"Removido da inicialização: {name}")
                                        self.logger.info(f"Programa removido da inicialização: {name}")
                                        break
                                    except:
                                        continue
                            else:
                                i += 1
                                
                        except OSError:
                            break
                            
            except Exception as e:
                self.logger.warning(f"Erro ao verificar startup do usuário: {e}")
            
            if progress_callback:
                progress_callback("Verificando startup do sistema...", 75)
            
            # Verificar programas de inicialização do sistema
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, startup_key, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            
                            # Verificar se o programa está na blacklist
                            for blacklisted in startup_blacklist:
                                if blacklisted.lower() in name.lower() or blacklisted.lower() in value.lower():
                                    try:
                                        winreg.DeleteValue(key, name)
                                        optimizations.append(f"Removido da inicialização do sistema: {name}")
                                        self.logger.info(f"Programa removido da inicialização do sistema: {name}")
                                        break
                                    except:
                                        continue
                            else:
                                i += 1
                                
                        except OSError:
                            break
                            
            except Exception as e:
                self.logger.warning(f"Erro ao verificar startup do sistema: {e}")
            
            if progress_callback:
                progress_callback("Otimização de inicialização concluída", 100)
            
        except Exception as e:
            self.logger.error(f"Erro na otimização de startup: {e}")
        
        return optimizations
    
    def optimize_windows_search(self, progress_callback=None):
        """Otimiza o Windows Search"""
        if progress_callback:
            progress_callback("Otimizando Windows Search...", 0)
        
        optimizations = []
        
        try:
            search_settings = [
                {
                    'key': r'SOFTWARE\Microsoft\Windows Search',
                    'values': {
                        'SetupCompletedSuccessfully': (winreg.REG_DWORD, 0),  # Reconfigurar search
                        'PortNumber': (winreg.REG_DWORD, 0),  # Desabilitar porta
                    }
                },
                {
                    'key': r'SOFTWARE\Policies\Microsoft\Windows\Windows Search',
                    'values': {
                        'AllowCortana': (winreg.REG_DWORD, 0),  # Desabilitar Cortana
                        'AllowSearchToUseLocation': (winreg.REG_DWORD, 0),  # Sem localização
                        'ConnectedSearchUseWeb': (winreg.REG_DWORD, 0),  # Sem busca web
                        'DisableWebSearch': (winreg.REG_DWORD, 1),  # Desabilitar busca web
                    }
                }
            ]
            
            for i, setting in enumerate(search_settings):
                if progress_callback:
                    progress = (i / len(search_settings)) * 100
                    progress_callback(f"Configurando search {i+1}/{len(search_settings)}", progress)
                
                try:
                    # Criar chave se não existir
                    winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, setting['key'])
                    
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            optimizations.append(f"Search: {value_name} configurado")
                except Exception as e:
                    self.logger.warning(f"Erro ao configurar search {setting['key']}: {e}")
            
            if progress_callback:
                progress_callback("Windows Search otimizado", 100)
            
        except Exception as e:
            self.logger.error(f"Erro na otimização do Windows Search: {e}")
        
        return optimizations
    
    def _detect_ssd_drives(self):
        """Detecta drives SSD no sistema"""
        ssd_drives = []
        
        try:
            # Usar WMI para detectar drives SSD
            cmd = 'powershell -Command "Get-PhysicalDisk | Where-Object {$_.MediaType -eq \'SSD\'} | Select-Object DeviceID"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line and 'DeviceID' not in line and '---' not in line:
                        ssd_drives.append(line.strip())
            
        except Exception as e:
            self.logger.warning(f"Erro ao detectar SSDs: {e}")
        
        return ssd_drives
    
    def get_optimization_summary(self):
        """Retorna resumo das otimizações aplicadas"""
        return {
            'total_optimizations': len(self.optimizations_applied),
            'optimizations': self.optimizations_applied
        }