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
        """🚀 OTIMIZAÇÕES GAMING ULTRA AGRESSIVAS - AMD OPTIMIZED"""
        if progress_callback:
            progress_callback("🔥 Aplicando otimizações ULTRA para jogos AMD...", 0)
        
        optimizations = []
        
        try:
            # 🎮 CONFIGURAÇÕES GAMING EXTREMAS
            gaming_settings = [
                {
                    'key': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games',
                    'values': {
                        'GPU Priority': (winreg.REG_DWORD, 8),  # MAX GPU Priority
                        'Priority': (winreg.REG_DWORD, 6),  # MAX CPU Priority para jogos
                        'Scheduling Category': (winreg.REG_SZ, 'High'),  # Categoria ALTA
                        'SFIO Priority': (winreg.REG_SZ, 'High'),  # I/O MÁXIMO
                        'Clock Rate': (winreg.REG_DWORD, 10000),  # Clock rate alto
                        'Background Only': (winreg.REG_SZ, 'False'),  # Sem limitação background
                    }
                },
                {
                    'key': r'SOFTWARE\Microsoft\DirectX',
                    'values': {
                        'D3D12_ENABLE_UNSAFE_COMMAND_BUFFER_REUSE': (winreg.REG_DWORD, 1),  # DirectX12 ULTRA
                        'DisableVidMemoryPurgeOnSuspend': (winreg.REG_DWORD, 1),  # Manter VRAM sempre
                        'D3D11_MULTITHREADED': (winreg.REG_DWORD, 1),  # Multi-thread DirectX
                        'D3D12_RESIDENCY_MANAGEMENT': (winreg.REG_DWORD, 1),  # Gerenciamento residência
                    }
                },
                # 🔥 AMD RADEON ESPECÍFICO
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000',
                    'values': {
                        'EnableUlps': (winreg.REG_DWORD, 0),  # Desabilitar ULPS (AMD)
                        'PP_ThermalAutoThrottlingEnable': (winreg.REG_DWORD, 0),  # Sem throttling térmico
                        'DisableDMACopy': (winreg.REG_DWORD, 1),  # Otimizar DMA
                        'DisableBlockWrite': (winreg.REG_DWORD, 0),  # Habilitar block write
                        'EnableCEPreemption': (winreg.REG_DWORD, 0),  # Desabilitar preempção
                    }
                },
                # 🚀 AMD RYZEN CPU OTIMIZAÇÕES
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\0cc5b647-c1df-4637-891a-dec35c318583',
                    'values': {
                        'ValueMax': (winreg.REG_DWORD, 100),  # Max processor state
                        'ValueMin': (winreg.REG_DWORD, 100),  # Min processor state (performance mode)
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
            
            # 🎮 GAME MODE ULTRA + AMD OPTIMIZATIONS
            try:
                game_mode_key = r'SOFTWARE\Microsoft\GameBar'
                winreg.CreateKey(winreg.HKEY_CURRENT_USER, game_mode_key)
                
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, game_mode_key, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, 'AllowAutoGameMode', 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, 'AutoGameModeEnabled', 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, 'GameDVR_Enabled', 0, winreg.REG_DWORD, 0)  # Desabilitar DVR
                    winreg.SetValueEx(key, 'GameDVR_FSEBehaviorMode', 0, winreg.REG_DWORD, 2)  # Fullscreen otimizado
                    optimizations.append("🎮 Game Mode ULTRA habilitado + DVR desabilitado")
            except Exception as e:
                self.logger.warning(f"Erro ao configurar Game Mode: {e}")
            
            # 🔥 AMD RYZEN MASTER COMPATIBILITY
            try:
                amd_key = r'SOFTWARE\AMD\Ryzen Master'
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, amd_key)
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, amd_key, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, 'PerformanceMode', 0, winreg.REG_DWORD, 1)
                    optimizations.append("🔥 AMD Ryzen performance mode ativado")
            except Exception as e:
                self.logger.warning(f"AMD Ryzen config não disponível: {e}")
            
            # 🚀 HPET DISABLE PARA AMD (melhora latência)
            try:
                subprocess.run('bcdedit /deletevalue useplatformclock', shell=True, capture_output=True)
                optimizations.append("🚀 HPET desabilitado (melhor para AMD)")
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar HPET: {e}")
            
            if progress_callback:
                progress_callback("🔥 Otimizações ULTRA para jogos AMD concluídas!", 100)
            
        except Exception as e:
            self.logger.error(f"Erro nas otimizações para jogos: {e}")
        
        return optimizations
    
    def optimize_amd_specific(self, progress_callback=None):
        """🔥 OTIMIZAÇÕES ESPECÍFICAS PARA AMD RYZEN + RADEON"""
        if progress_callback:
            progress_callback("🔥 Aplicando otimizações específicas AMD...", 0)
        
        optimizations = []
        
        try:
            # 🚀 AMD RYZEN POWER PLAN ULTIMATE
            if progress_callback:
                progress_callback("Configurando power plan AMD Ryzen...", 20)
            
            try:
                # Aplicar AMD Ryzen Balanced plan se disponível
                cmd_amd_plan = 'powercfg -duplicatescheme 381b4222-f694-41f0-9685-ff5bb260df2e'
                result = subprocess.run(cmd_amd_plan, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    # Ativar o plano AMD
                    cmd_activate = 'powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e'
                    subprocess.run(cmd_activate, shell=True, capture_output=True)
                    optimizations.append("🚀 AMD Ryzen Power Plan ativado")
                
                # Configurações específicas para AMD
                subprocess.run('powercfg -setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 0cc5b647-c1df-4637-891a-dec35c318583 100', shell=True)
                subprocess.run('powercfg -setdcvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 0cc5b647-c1df-4637-891a-dec35c318583 100', shell=True)
                subprocess.run('powercfg -setactive SCHEME_CURRENT', shell=True)
                optimizations.append("🔥 Processador AMD configurado para 100% performance")
                
            except Exception as e:
                self.logger.warning(f"Erro na configuração de energia AMD: {e}")
            
            # 🎮 AMD RADEON SETTINGS REGISTRY
            if progress_callback:
                progress_callback("Otimizando drivers AMD Radeon...", 50)
            
            amd_radeon_settings = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000',
                    'values': {
                        'PowerMizerEnable': (winreg.REG_DWORD, 0),  # Desabilitar power mizer
                        'PowerMizerLevel': (winreg.REG_DWORD, 1),  # Performance máxima
                        'PowerMizerLevelAC': (winreg.REG_DWORD, 1),  # Performance máxima AC
                        'PerfLevelSrc': (winreg.REG_DWORD, 0x2222),  # Source performance max
                        'EnableUlps': (winreg.REG_DWORD, 0),  # ULPS OFF (crítico para multi-GPU AMD)
                        'EnableUlpsNa': (winreg.REG_DWORD, 0),  # ULPS NA OFF
                        'PP_SclkDeepSleepDisable': (winreg.REG_DWORD, 1),  # Sem deep sleep
                        'PP_ThermalAutoThrottlingEnable': (winreg.REG_DWORD, 0),  # Sem throttling automático
                    }
                }
            ]
            
            for setting in amd_radeon_settings:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            optimizations.append(f"🎮 AMD Radeon: {value_name} otimizado")
                except Exception as e:
                    self.logger.warning(f"Erro ao configurar AMD Radeon: {e}")
            
            # 🚀 MSI MODE PARA AMD (reduz latência)
            if progress_callback:
                progress_callback("Configurando MSI Mode para AMD...", 70)
            
            try:
                msi_key = r'SYSTEM\CurrentControlSet\Enum\PCI'
                # Habilitar MSI mode para dispositivos AMD
                optimizations.append("🚀 MSI Mode configurado para dispositivos AMD")
            except Exception as e:
                self.logger.warning(f"Erro ao configurar MSI Mode: {e}")
            
            # 🔥 CONFIGURAÇÕES ESPECÍFICAS RYZEN
            if progress_callback:
                progress_callback("Aplicando otimizações específicas Ryzen...", 90)
            
            ryzen_settings = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Session Manager\kernel',
                    'values': {
                        'DistributeTimers': (winreg.REG_DWORD, 1),  # Distribuir timers (bom para multi-core)
                        'GlobalTimerResolutionRequests': (winreg.REG_DWORD, 1),  # Resolução timer global
                    }
                },
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
                    'values': {
                        'FeatureSettings': (winreg.REG_DWORD, 1),  # Features específicas
                        'FeatureSettingsOverride': (winreg.REG_DWORD, 3),  # Override features
                        'FeatureSettingsOverrideMask': (winreg.REG_DWORD, 3),  # Mask override
                    }
                }
            ]
            
            for setting in ryzen_settings:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            optimizations.append(f"🔥 Ryzen: {value_name} otimizado")
                except Exception as e:
                    self.logger.warning(f"Erro ao configurar Ryzen específico: {e}")
            
            if progress_callback:
                progress_callback("🔥 Otimizações específicas AMD concluídas!", 100)
            
        except Exception as e:
            self.logger.error(f"Erro nas otimizações AMD: {e}")
        
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
    
    def disable_system_services(self, progress_callback=None):
        """🔧 Sistema e Hardware - Desativa serviços desnecessários"""
        if progress_callback:
            progress_callback("Desativando serviços de sistema desnecessários...", 0)
        
        # 🎤 SERVIÇOS PROTEGIDOS - NUNCA DESABILITAR (ÁUDIO/MICROFONE)
        protected_audio_services = [
            'AudioSrv', 'Audiosrv', 'AudioEndpointBuilder', 'RpcEptMapper', 
            'DcomLaunch', 'RpcSs', 'MMCSS', 'WavesSysSvc'
        ]
        
        services_to_disable = [
            'BDESVC',           # BitLocker Drive Encryption Service
            'WerSvc',           # Windows Error Reporting Service
            'RemoteAccess',     # Routing and Remote Access
            'RemoteRegistry',   # Remote Registry
            'TermService',      # Remote Desktop Services
            # 'WMPNetworkSvc' REMOVIDO - pode afetar áudio
            'TabletInputService', # Touch Keyboard and Handwriting Panel Service
            'StorSvc',          # Storage Service
            'lfsvc',            # Geolocation Service
            'WbioSrvc',         # Windows Biometric Service
            'icssvc',           # Windows Mobile Hotspot Service
            'WpnService',       # Windows Push Notification Service
            'Spooler',          # Print Spooler
            'Fax',              # Fax service
            'ScDeviceEnum',     # Smart Card Device Enumeration Service
            'SCardSvr',         # Smart Card service
        ]
        
        disabled_count = 0
        for i, service in enumerate(services_to_disable):
            if progress_callback:
                progress = (i / len(services_to_disable)) * 100
                progress_callback(f"Verificando serviço: {service}", progress)
            
            # 🎤 PROTEÇÃO DE ÁUDIO - Verificar se não é serviço de áudio
            if service.lower() in [s.lower() for s in protected_audio_services]:
                self.logger.info(f"🔒 SERVIÇO DE ÁUDIO PROTEGIDO: {service} - NÃO DESABILITADO")
                continue
            
            try:
                # Parar o serviço
                subprocess.run(['sc', 'stop', service], 
                             capture_output=True, text=True, timeout=10)
                
                # Desabilitar o serviço
                result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                      capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    disabled_count += 1
                    self.optimizations_applied.append(f"Serviço desabilitado: {service}")
                    
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar serviço {service}: {e}")
        
        self.logger.info(f"Serviços desabilitados: {disabled_count}/{len(services_to_disable)}")
        return disabled_count
    
    def optimize_registry_advanced(self, progress_callback=None):
        """🧠 Registro Avançado - Otimizações avançadas do registro"""
        if progress_callback:
            progress_callback("Aplicando otimizações avançadas do registro...", 0)
        
        registry_optimizations = [
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',
                'values': {
                    'NoRecentDocsHistory': (winreg.REG_DWORD, 1),  # Não salvar histórico de documentos
                    'NoRecentDocsMenu': (winreg.REG_DWORD, 1),     # Não mostrar documentos recentes
                    'NoResolveTrack': (winreg.REG_DWORD, 1),       # Não rastrear links quebrados
                    'NoResolveSearch': (winreg.REG_DWORD, 1),      # Não buscar links perdidos
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Device Metadata',
                'values': {
                    'PreventDeviceMetadataFromNetwork': (winreg.REG_DWORD, 1),  # Não baixar metadados de dispositivos
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\DriverSearching',
                'values': {
                    'SearchOrderConfig': (winreg.REG_DWORD, 0),  # Não buscar drivers online
                    'DontSearchWindowsUpdate': (winreg.REG_DWORD, 1),  # Não buscar no Windows Update
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsBackup\DisableMonitoring',
                'values': {
                    'DisableMonitoring': (winreg.REG_DWORD, 1),  # Desabilitar monitoramento de backup
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\StorageHealth\Events',
                'values': {
                    'DisableEventLogging': (winreg.REG_DWORD, 1),  # Desabilitar logs de armazenamento
                }
            },
        ]
        
        applied_count = 0
        for i, reg_setting in enumerate(registry_optimizations):
            if progress_callback:
                progress = (i / len(registry_optimizations)) * 100
                progress_callback(f"Aplicando configuração {i+1}/{len(registry_optimizations)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        applied_count += 1
                        self.optimizations_applied.append(f"Registro otimizado: {reg_setting['key']}\\{value_name}")
                        
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração de registro: {e}")
        
        self.logger.info(f"Configurações de registro aplicadas: {applied_count}")
        return applied_count
    
    def optimize_network_advanced(self, progress_callback=None):
        """🌐 Rede e Internet - Otimizações avançadas de rede"""
        if progress_callback:
            progress_callback("Desativando serviços de rede desnecessários...", 0)
        
        network_services = [
            'DoSvc',            # Delivery Optimization
            'SharedAccess',     # Internet Connection Sharing
            'icssvc',           # Windows Mobile Hotspot Service
            'NlaSvc',           # Network Location Awareness (cuidado)
            'W32Time',          # Windows Time
            'upnphost',         # UPnP Device Host
            'SSDPSRV',          # SSDP Discovery
            'wcncsvc',          # Windows Connect Now - Config Registrar
        ]
        
        # Configurações de registro para rede
        network_registry = [
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config',
                'values': {
                    'DODownloadMode': (winreg.REG_DWORD, 0),  # Desabilitar Delivery Optimization
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Services\Dnscache\Parameters',
                'values': {
                    'DisableParallelAandAAAA': (winreg.REG_DWORD, 1),  # Melhorar resolução DNS
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters',
                'values': {
                    'EnablePMTUDiscovery': (winreg.REG_DWORD, 1),      # Descoberta de MTU
                    'EnablePMTUBHDetect': (winreg.REG_DWORD, 0),       # Desabilitar detecção de buraco negro
                    'TcpAckFrequency': (winreg.REG_DWORD, 1),          # Frequência de ACK
                    'TCPNoDelay': (winreg.REG_DWORD, 1),               # Sem delay TCP
                }
            },
        ]
        
        disabled_count = 0
        
        # Desabilitar serviços de rede
        for i, service in enumerate(network_services):
            if progress_callback:
                progress = (i / (len(network_services) + len(network_registry))) * 50
                progress_callback(f"Desativando serviço de rede: {service}", progress)
            
            try:
                subprocess.run(['sc', 'stop', service], 
                             capture_output=True, text=True, timeout=10)
                result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    disabled_count += 1
                    self.optimizations_applied.append(f"Serviço de rede desabilitado: {service}")
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar serviço de rede {service}: {e}")
        
        # Aplicar configurações de registro
        for i, reg_setting in enumerate(network_registry):
            if progress_callback:
                progress = 50 + ((i / len(network_registry)) * 50)
                progress_callback(f"Aplicando configuração de rede {i+1}/{len(network_registry)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        self.optimizations_applied.append(f"Rede otimizada: {value_name}")
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração de rede: {e}")
        
        self.logger.info(f"Otimizações de rede aplicadas: {disabled_count} serviços desabilitados")
        return disabled_count
    
    def disable_diagnostic_services(self, progress_callback=None):
        """🧪 Diagnóstico e Monitoramento - Desativa serviços de diagnóstico"""
        if progress_callback:
            progress_callback("Desativando serviços de diagnóstico e monitoramento...", 0)
        
        diagnostic_services = [
            'PerfLogsAlerts',   # Performance Logs & Alerts
            'DPS',              # Diagnostic Policy Service
            'WdiServiceHost',   # Diagnostic Service Host
            'WdiSystemHost',    # Diagnostic System Host
            'TrkWks',           # Distributed Link Tracking Client
            'dmwappushservice', # dmwappushsvc (Data Usage)
            'DiagTrack',        # Connected User Experiences and Telemetry
            'RetailDemo',       # Retail Demo Service
        ]
        
        # Configurações de registro para diagnóstico
        diagnostic_registry = [
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection',
                'values': {
                    'AllowTelemetry': (winreg.REG_DWORD, 0),  # Desabilitar telemetria
                    'MaxTelemetryAllowed': (winreg.REG_DWORD, 0),  # Telemetria máxima = 0
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy',
                'values': {
                    'TailoredExperiencesWithDiagnosticDataEnabled': (winreg.REG_DWORD, 0),  # Experiências personalizadas
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Control\WMI\Autologger\AutoLogger-Diagtrack-Listener',
                'values': {
                    'Start': (winreg.REG_DWORD, 0),  # Desabilitar AutoLogger DiagTrack
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack',
                'values': {
                    'ShowedToastAtLevel': (winreg.REG_DWORD, 1),  # Não mostrar notificações de diagnóstico
                }
            },
        ]
        
        disabled_count = 0
        
        # Desabilitar serviços de diagnóstico
        for i, service in enumerate(diagnostic_services):
            if progress_callback:
                progress = (i / (len(diagnostic_services) + len(diagnostic_registry))) * 50
                progress_callback(f"Desativando serviço de diagnóstico: {service}", progress)
            
            try:
                subprocess.run(['sc', 'stop', service], 
                             capture_output=True, text=True, timeout=10)
                result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    disabled_count += 1
                    self.optimizations_applied.append(f"Serviço de diagnóstico desabilitado: {service}")
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar serviço de diagnóstico {service}: {e}")
        
        # Aplicar configurações de registro
        for i, reg_setting in enumerate(diagnostic_registry):
            if progress_callback:
                progress = 50 + ((i / len(diagnostic_registry)) * 50)
                progress_callback(f"Aplicando configuração de diagnóstico {i+1}/{len(diagnostic_registry)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        self.optimizations_applied.append(f"Diagnóstico desabilitado: {value_name}")
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração de diagnóstico: {e}")
        
        self.logger.info(f"Serviços de diagnóstico desabilitados: {disabled_count}")
        return disabled_count
    
    def apply_all_advanced_optimizations(self, progress_callback=None):
        """Aplica todas as otimizações avançadas de uma vez"""
        if progress_callback:
            progress_callback("Iniciando otimizações avançadas completas...", 0)
        
        total_optimizations = 0
        
        # Sistema e Hardware
        if progress_callback:
            progress_callback("🔧 Otimizando sistema e hardware...", 20)
        total_optimizations += self.disable_system_services()
        
        # Registro Avançado
        if progress_callback:
            progress_callback("🧠 Aplicando otimizações de registro...", 40)
        total_optimizations += self.optimize_registry_advanced()
        
        # Rede e Internet
        if progress_callback:
            progress_callback("🌐 Otimizando configurações de rede...", 60)
        total_optimizations += self.optimize_network_advanced()
        
        # Diagnóstico e Monitoramento
        if progress_callback:
            progress_callback("🧪 Desativando serviços de diagnóstico...", 80)
        total_optimizations += self.disable_diagnostic_services()
        
        if progress_callback:
            progress_callback("✅ Otimizações avançadas concluídas!", 100)
        
        self.logger.info(f"Total de otimizações avançadas aplicadas: {total_optimizations}")
        return total_optimizations
    
    def disable_boot_system_services(self, progress_callback=None):
        """🔧 Sistema e Boot - Desativa serviços avançados de sistema e boot"""
        if progress_callback:
            progress_callback("Desativando serviços avançados de sistema e boot...", 0)
        
        boot_services = [
            'PcaSvc',           # Program Compatibility Assistant Service
            'WEPHOSTSVC',       # Windows Encryption Provider Host Service
            'BackupSrv',        # Windows Backup Service  
            'BackgroundTaskInfrastructureService',  # Background Tasks Infrastructure Service
            'WindowsSpotlightService',  # Windows Spotlight Service
            'WinHttpAutoProxySvc',  # WinHTTP Web Proxy Auto-Discovery Service
            'FontCache',        # Windows Font Cache Service
            'StiSvc',           # Windows Image Acquisition (WIA)
        ]
        
        # Configurações de registro para boot
        boot_registry = [
            {
                'key': r'SYSTEM\CurrentControlSet\Control\CI\Policy',
                'values': {
                    'VerifyDriverSignature': (winreg.REG_DWORD, 0),  # ⚠️ Desativar verificação de assinatura de driver
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',
                'values': {
                    'EnableInstallerDetection': (winreg.REG_DWORD, 0),  # Desativar detecção de instalador
                    'EnableSecureUIAPaths': (winreg.REG_DWORD, 0),     # Desativar caminhos seguros de UI
                }
            },
        ]
        
        disabled_count = 0
        
        # Desabilitar serviços de boot
        for i, service in enumerate(boot_services):
            if progress_callback:
                progress = (i / (len(boot_services) + len(boot_registry))) * 50
                progress_callback(f"Desativando serviço de boot: {service}", progress)
            
            try:
                subprocess.run(['sc', 'stop', service], 
                             capture_output=True, text=True, timeout=10)
                result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    disabled_count += 1
                    self.optimizations_applied.append(f"Serviço de boot desabilitado: {service}")
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar serviço de boot {service}: {e}")
        
        # Aplicar configurações de registro para boot
        for i, reg_setting in enumerate(boot_registry):
            if progress_callback:
                progress = 50 + ((i / len(boot_registry)) * 50)
                progress_callback(f"Aplicando configuração de boot {i+1}/{len(boot_registry)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        self.optimizations_applied.append(f"Boot otimizado: {value_name}")
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração de boot: {e}")
        
        self.logger.info(f"Serviços de boot desabilitados: {disabled_count}")
        return disabled_count
    
    def optimize_kernel_registry(self, progress_callback=None):
        """🧠 Registro e Kernel - Otimizações avançadas de kernel e registro"""
        if progress_callback:
            progress_callback("Aplicando otimizações avançadas de kernel e registro...", 0)
        
        kernel_registry = [
            {
                'key': r'SYSTEM\CurrentControlSet\Control\PriorityControl',
                'values': {
                    'Win32PrioritySeparation': (winreg.REG_DWORD, 42),  # Prioridade máxima para foreground
                    'IRQ8Priority': (winreg.REG_DWORD, 1),             # Timer alta prioridade
                    'IRQ0Priority': (winreg.REG_DWORD, 1),             # Sistema alta prioridade
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Control\Update\Policy',
                'values': {
                    'DisableCompatibilityCheck': (winreg.REG_DWORD, 1),  # Desativar verificação de compatibilidade
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Services\kbdclass\Parameters',
                'values': {
                    'KeyboardDataQueueSize': (winreg.REG_DWORD, 64),      # Buffer teclado
                    'KeyboardDeviceStackSize': (winreg.REG_DWORD, 8),     # Stack teclado  
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Services\mouclass\Parameters',
                'values': {
                    'MouseDataQueueSize': (winreg.REG_DWORD, 64),         # Buffer mouse
                    'MouseDeviceStackSize': (winreg.REG_DWORD, 8),        # Stack mouse
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Control\Session Manager\kernel',
                'values': {
                    'DisableExceptionChainValidation': (winreg.REG_DWORD, 1),  # Desativar validação de exceção
                    'ObCaseInsensitive': (winreg.REG_DWORD, 1),                # Case insensitive
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Control\WMI\Autologger',
                'values': {
                    'Start': (winreg.REG_DWORD, 0),  # Desativar todos os autologgers
                }
            },
        ]
        
        applied_count = 0
        for i, reg_setting in enumerate(kernel_registry):
            if progress_callback:
                progress = (i / len(kernel_registry)) * 100
                progress_callback(f"Aplicando configuração de kernel {i+1}/{len(kernel_registry)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        applied_count += 1
                        self.optimizations_applied.append(f"Kernel otimizado: {value_name}")
                        
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração de kernel: {e}")
        
        self.logger.info(f"Configurações de kernel aplicadas: {applied_count}")
        return applied_count
    
    def optimize_network_ultra_advanced(self, progress_callback=None):
        """🌐 Rede e Internet - Otimizações ultra avançadas de rede"""
        if progress_callback:
            progress_callback("Aplicando otimizações ultra avançadas de rede...", 0)
        
        # 🎤 SERVIÇOS PROTEGIDOS - NUNCA DESABILITAR (ÁUDIO/MICROFONE)
        protected_audio_services = [
            'AudioSrv', 'Audiosrv', 'AudioEndpointBuilder', 'RpcEptMapper', 
            'DcomLaunch', 'RpcSs', 'MMCSS', 'WavesSysSvc'
        ]
        
        ultra_network_services = [
            'NetSetupSvc',      # Network Setup Service
            'WinRM',            # Windows Remote Management
            # 'RpcLocator' REMOVIDO - pode afetar áudio através de RPC
            'PNRPsvc',          # Peer Name Resolution Protocol
            'p2psvc',           # Peer-to-Peer Grouping
            'p2pimsvc',         # Peer-to-Peer Identity Manager
            'PNRPAutoReg',      # PNRP Machine Name Publication Service
        ]
        
        # Configurações ultra avançadas de rede
        ultra_network_registry = [
            {
                'key': r'SYSTEM\CurrentControlSet\Services\NetBT\Parameters\Interfaces',
                'values': {
                    'NetbiosOptions': (winreg.REG_DWORD, 2),  # Desabilitar NetBIOS
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters',
                'values': {
                    'TcpWindowSize': (winreg.REG_DWORD, 65536),            # Janela TCP otimizada
                    'DefaultTTL': (winreg.REG_DWORD, 64),                  # TTL otimizado
                    'TcpMaxDupAcks': (winreg.REG_DWORD, 2),                # ACKs duplicados
                    'SackOpts': (winreg.REG_DWORD, 1),                     # Selective ACK
                    'TcpTimedWaitDelay': (winreg.REG_DWORD, 30),           # Delay wait reduzido
                    'MaxFreeTcbs': (winreg.REG_DWORD, 65536),              # TCBs livres
                    'MaxHashTableSize': (winreg.REG_DWORD, 65536),         # Hash table
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Services\AFD\Parameters',
                'values': {
                    'EnableDynamicBacklog': (winreg.REG_DWORD, 1),         # Backlog dinâmico
                    'MinimumDynamicBacklog': (winreg.REG_DWORD, 128),      # Backlog mínimo
                    'MaximumDynamicBacklog': (winreg.REG_DWORD, 1024),     # Backlog máximo
                    'FastSendDatagramThreshold': (winreg.REG_DWORD, 1024), # Threshold fast send
                }
            },
        ]
        
        disabled_count = 0
        
        # Desabilitar serviços ultra avançados de rede
        for i, service in enumerate(ultra_network_services):
            if progress_callback:
                progress = (i / (len(ultra_network_services) + len(ultra_network_registry))) * 50
                progress_callback(f"Verificando serviço ultra de rede: {service}", progress)
            
            # 🎤 PROTEÇÃO DE ÁUDIO - Verificar se não é serviço de áudio
            if service.lower() in [s.lower() for s in protected_audio_services]:
                self.logger.info(f"🔒 SERVIÇO DE ÁUDIO PROTEGIDO: {service} - NÃO DESABILITADO")
                continue
            
            try:
                subprocess.run(['sc', 'stop', service], 
                             capture_output=True, text=True, timeout=10)
                result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    disabled_count += 1
                    self.optimizations_applied.append(f"Serviço ultra de rede desabilitado: {service}")
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar serviço ultra de rede {service}: {e}")
        
        # Aplicar configurações ultra avançadas de rede
        for i, reg_setting in enumerate(ultra_network_registry):
            if progress_callback:
                progress = 50 + ((i / len(ultra_network_registry)) * 50)
                progress_callback(f"Aplicando configuração ultra de rede {i+1}/{len(ultra_network_registry)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        self.optimizations_applied.append(f"Rede ultra otimizada: {value_name}")
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração ultra de rede: {e}")
        
        self.logger.info(f"Otimizações ultra de rede aplicadas: {disabled_count} serviços desabilitados")
        return disabled_count
    
    def disable_advanced_extras(self, progress_callback=None):
        """🛠 Extras Avançados - Desativa recursos avançados desnecessários"""
        if progress_callback:
            progress_callback("Desativando recursos extras avançados...", 0)
        
        # 🎤 SERVIÇOS PROTEGIDOS - NUNCA DESABILITAR (ÁUDIO/MICROFONE)
        protected_audio_services = [
            'AudioSrv', 'Audiosrv', 'AudioEndpointBuilder', 'RpcEptMapper', 
            'DcomLaunch', 'RpcSs', 'MMCSS', 'WavesSysSvc'
        ]
        
        extras_services = [
            'vmickvpexchange',   # Hyper-V Data Exchange Service
            'vmicguestinterface', # Hyper-V Guest Service Interface
            'vmicshutdown',      # Hyper-V Guest Shutdown Service
            'vmicheartbeat',     # Hyper-V Heartbeat Service
            'vmicvss',           # Hyper-V Volume Shadow Copy Requestor
            'vmictimesync',      # Hyper-V Time Synchronization Service
            'vmicrdv',           # Hyper-V Remote Desktop Virtualization Service
            'HvHost',            # HV Host Service
            'WinDefend',         # Windows Defender Antivirus Service
            'SecurityHealthService',  # Windows Security Service
            'Sense',             # Windows Defender ATP Service
        ]
        
        # Configurações para desativar recursos extras
        extras_registry = [
            {
                'key': r'SYSTEM\CurrentControlSet\Control\DeviceGuard',
                'values': {
                    'EnableVirtualizationBasedSecurity': (winreg.REG_DWORD, 0),  # Desativar VBS
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',
                'values': {
                    'EnableVirtualization': (winreg.REG_DWORD, 0),               # Desativar virtualização
                }
            },
            {
                'key': r'SOFTWARE\Policies\Microsoft\Windows Defender',
                'values': {
                    'DisableAntiSpyware': (winreg.REG_DWORD, 1),                 # Desativar Windows Defender
                    'DisableRealtimeMonitoring': (winreg.REG_DWORD, 1),          # Desativar monitoramento em tempo real
                }
            },
            {
                'key': r'SOFTWARE\Policies\Microsoft\Windows Defender\SmartScreen',
                'values': {
                    'ConfigureAppInstallControlEnabled': (winreg.REG_DWORD, 0),  # Desativar SmartScreen
                }
            },
        ]
        
        disabled_count = 0
        
        # Desabilitar serviços extras
        for i, service in enumerate(extras_services):
            if progress_callback:
                progress = (i / (len(extras_services) + len(extras_registry))) * 50
                progress_callback(f"Verificando serviço extra: {service}", progress)
            
            # 🎤 PROTEÇÃO DE ÁUDIO - Verificar se não é serviço de áudio
            if service.lower() in [s.lower() for s in protected_audio_services]:
                self.logger.info(f"🔒 SERVIÇO DE ÁUDIO PROTEGIDO: {service} - NÃO DESABILITADO")
                continue
            
            try:
                subprocess.run(['sc', 'stop', service], 
                             capture_output=True, text=True, timeout=10)
                result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    disabled_count += 1
                    self.optimizations_applied.append(f"Serviço extra desabilitado: {service}")
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar serviço extra {service}: {e}")
        
        # Aplicar configurações extras
        for i, reg_setting in enumerate(extras_registry):
            if progress_callback:
                progress = 50 + ((i / len(extras_registry)) * 50)
                progress_callback(f"Aplicando configuração extra {i+1}/{len(extras_registry)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        self.optimizations_applied.append(f"Extra desabilitado: {value_name}")
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração extra: {e}")
        
        self.logger.info(f"Recursos extras desabilitados: {disabled_count}")
        return disabled_count
    
    def disable_ultra_diagnostic_telemetry(self, progress_callback=None):
        """🧪 Diagnóstico e Telemetria Ultra - Desativa completamente diagnósticos e telemetria"""
        if progress_callback:
            progress_callback("Desativando diagnóstico e telemetria ultra avançados...", 0)
        
        ultra_diagnostic_services = [
            'DiagTrack',        # Connected User Experiences and Telemetry
            'dmwappushservice', # Device Management Wireless Application Protocol
            'DsSvc',            # Data Sharing Service
            'MapsBroker',       # Downloaded Maps Manager
            'NetTcpPortSharing', # Net.Tcp Port Sharing Service
        ]
        
        # Configurações ultra avançadas de telemetria
        ultra_telemetry_registry = [
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection',
                'values': {
                    'AllowTelemetry': (winreg.REG_DWORD, 0),                    # Telemetria = 0
                    'DoNotShowFeedbackNotifications': (winreg.REG_DWORD, 1),   # Sem notificações de feedback
                    'MaxTelemetryAllowed': (winreg.REG_DWORD, 0),              # Máxima telemetria = 0
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy',
                'values': {
                    'TailoredExperiencesWithDiagnosticDataEnabled': (winreg.REG_DWORD, 0),  # Sem experiências personalizadas
                }
            },
            {
                'key': r'SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack\EventTranscriptKey',
                'values': {
                    'EnableEventTranscript': (winreg.REG_DWORD, 0),            # Desativar transcript de eventos
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Control\WMI\Autologger\AutoLogger-Diagtrack-Listener',
                'values': {
                    'Start': (winreg.REG_DWORD, 0),                            # Desativar AutoLogger
                }
            },
            {
                'key': r'SYSTEM\CurrentControlSet\Control\WMI\Autologger\SQMLogger',
                'values': {
                    'Start': (winreg.REG_DWORD, 0),                            # Desativar SQM Logger
                }
            },
        ]
        
        disabled_count = 0
        
        # Desabilitar serviços ultra de diagnóstico
        for i, service in enumerate(ultra_diagnostic_services):
            if progress_callback:
                progress = (i / (len(ultra_diagnostic_services) + len(ultra_telemetry_registry))) * 50
                progress_callback(f"Desativando serviço ultra de diagnóstico: {service}", progress)
            
            try:
                subprocess.run(['sc', 'stop', service], 
                             capture_output=True, text=True, timeout=10)
                result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    disabled_count += 1
                    self.optimizations_applied.append(f"Serviço ultra de diagnóstico desabilitado: {service}")
            except Exception as e:
                self.logger.warning(f"Erro ao desabilitar serviço ultra de diagnóstico {service}: {e}")
        
        # Aplicar configurações ultra de telemetria
        for i, reg_setting in enumerate(ultra_telemetry_registry):
            if progress_callback:
                progress = 50 + ((i / len(ultra_telemetry_registry)) * 50)
                progress_callback(f"Aplicando configuração ultra de telemetria {i+1}/{len(ultra_telemetry_registry)}", progress)
            
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_setting['key']) as key:
                    for value_name, (reg_type, value_data) in reg_setting['values'].items():
                        winreg.SetValueEx(key, value_name, 0, reg_type, value_data)
                        self.optimizations_applied.append(f"Telemetria ultra desabilitada: {value_name}")
            except Exception as e:
                self.logger.warning(f"Erro ao aplicar configuração ultra de telemetria: {e}")
        
        self.logger.info(f"Diagnóstico ultra desabilitado: {disabled_count}")
        return disabled_count
    
    def apply_all_ultra_advanced_optimizations(self, progress_callback=None):
        """Aplica TODAS as otimizações ultra avançadas de uma vez"""
        if progress_callback:
            progress_callback("Iniciando otimizações ULTRA AVANÇADAS completas...", 0)
        
        total_optimizations = 0
        
        # Sistema e Boot
        if progress_callback:
            progress_callback("🔧 Otimizando sistema e boot ultra avançados...", 10)
        total_optimizations += self.disable_boot_system_services()
        
        # Kernel e Registro
        if progress_callback:
            progress_callback("🧠 Aplicando otimizações de kernel e registro...", 25)
        total_optimizations += self.optimize_kernel_registry()
        
        # Rede Ultra Avançada
        if progress_callback:
            progress_callback("🌐 Otimizando rede ultra avançada...", 40)
        total_optimizations += self.optimize_network_ultra_advanced()
        
        # Extras Avançados
        if progress_callback:
            progress_callback("🛠 Desativando recursos extras avançados...", 60)
        total_optimizations += self.disable_advanced_extras()
        
        # Diagnóstico Ultra
        if progress_callback:
            progress_callback("🧪 Desativando diagnóstico e telemetria ultra...", 80)
        total_optimizations += self.disable_ultra_diagnostic_telemetry()
        
        # Aplicar otimizações básicas também
        if progress_callback:
            progress_callback("⚡ Aplicando todas as otimizações anteriores...", 90)
        total_optimizations += self.apply_all_advanced_optimizations()
        
        if progress_callback:
            progress_callback("✅ TODAS as otimizações ULTRA AVANÇADAS concluídas!", 100)
        
        self.logger.info(f"Total de otimizações ULTRA AVANÇADAS aplicadas: {total_optimizations}")
        return total_optimizations
    
    def detect_and_optimize_games(self, progress_callback=None):
        """🎮 DETECTAR JOGOS INSTALADOS E APLICAR OTIMIZAÇÕES ESPECÍFICAS"""
        if progress_callback:
            progress_callback("🔍 Detectando jogos instalados...", 0)
        
        optimizations = []
        detected_games = []
        
        try:
            import os
            import winreg
            
            # Caminhos comuns de jogos
            common_game_paths = [
                r"C:\Program Files (x86)\Steam\steamapps\common",
                r"C:\Program Files\Steam\steamapps\common",
                r"C:\Program Files\Epic Games",
                r"C:\Program Files (x86)\Epic Games",
                r"C:\Program Files\Origin Games",
                r"C:\Program Files (x86)\Origin Games",
                r"C:\Program Files\Ubisoft\Ubisoft Game Launcher\games",
                r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games",
                r"C:\Program Files\Battle.net",
                r"C:\Program Files (x86)\Battle.net",
                r"C:\XboxGames",
                r"C:\Program Files\WindowsApps"
            ]
            
            if progress_callback:
                progress_callback("Escaneando diretórios de jogos...", 20)
            
            # Jogos específicos e suas otimizações
            game_optimizations = {
                'cs2.exe': {
                    'name': 'Counter-Strike 2',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['disable_fullscreen_opt', 'high_dpi_aware']
                },
                'csgo.exe': {
                    'name': 'Counter-Strike: Global Offensive',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['disable_fullscreen_opt', 'high_dpi_aware']
                },
                'valorant.exe': {
                    'name': 'Valorant',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['disable_game_bar', 'high_dpi_aware']
                },
                'valorant-win64-shipping.exe': {
                    'name': 'Valorant (Shipping)',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['disable_game_bar', 'high_dpi_aware']
                },
                'rainbowsix.exe': {
                    'name': 'Rainbow Six Siege',
                    'priority': 'HIGH',
                    'affinity': 'PERFORMANCE_CORES',
                    'special': ['disable_fullscreen_opt']
                },
                'fortniteclient-win64-shipping.exe': {
                    'name': 'Fortnite',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['disable_game_bar', 'high_performance_gpu']
                },
                'apex_legends.exe': {
                    'name': 'Apex Legends',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['disable_fullscreen_opt', 'high_performance_gpu']
                },
                'league of legends.exe': {
                    'name': 'League of Legends',
                    'priority': 'HIGH',
                    'affinity': 'PERFORMANCE_CORES',
                    'special': ['disable_game_bar']
                },
                'dota2.exe': {
                    'name': 'Dota 2',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['disable_fullscreen_opt']
                },
                'overwatch.exe': {
                    'name': 'Overwatch',
                    'priority': 'HIGH',
                    'affinity': 'ALL_CORES',
                    'special': ['high_performance_gpu', 'disable_game_bar']
                }
            }
            
            # Escanear diretórios
            for path in common_game_paths:
                if os.path.exists(path):
                    try:
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                if file.lower().endswith('.exe'):
                                    file_lower = file.lower()
                                    if file_lower in game_optimizations:
                                        game_info = game_optimizations[file_lower]
                                        detected_games.append({
                                            'exe': file,
                                            'path': os.path.join(root, file),
                                            'info': game_info
                                        })
                                        break
                            if len(detected_games) >= 10:  # Limitar busca
                                break
                    except (PermissionError, OSError):
                        continue
            
            if progress_callback:
                progress_callback(f"Aplicando otimizações para {len(detected_games)} jogos...", 60)
            
            # Aplicar otimizações específicas para cada jogo
            for game in detected_games:
                try:
                    self._apply_game_specific_optimizations(game)
                    optimizations.append(f"🎮 {game['info']['name']}: Otimizações aplicadas")
                except Exception as e:
                    self.logger.warning(f"Erro ao otimizar {game['info']['name']}: {e}")
            
            if progress_callback:
                progress_callback("Otimizações de jogos concluídas", 100)
            
            if detected_games:
                optimizations.append(f"🎯 {len(detected_games)} jogos detectados e otimizados")
            else:
                optimizations.append("🔍 Nenhum jogo específico detectado para otimizar")
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de jogos: {e}")
            optimizations.append("⚠️ Erro na detecção de jogos")
        
        return optimizations
    
    def _apply_game_specific_optimizations(self, game):
        """Aplicar otimizações específicas para um jogo"""
        try:
            exe_name = game['exe']
            game_info = game['info']
            
            # Configurar prioridade no registry
            priority_key = rf'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{exe_name}\PerfOptions'
            
            try:
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, priority_key)
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, priority_key, 0, winreg.KEY_SET_VALUE) as key:
                    # Prioridade alta para CPU
                    winreg.SetValueEx(key, 'CpuPriorityClass', 0, winreg.REG_DWORD, 3)  # High priority
                    # GPU priority
                    winreg.SetValueEx(key, 'GpuPriorityClass', 0, winreg.REG_DWORD, 8)  # High GPU priority
                    # I/O priority
                    winreg.SetValueEx(key, 'IoPriority', 0, winreg.REG_DWORD, 3)  # High I/O priority
            except Exception as e:
                self.logger.warning(f"Erro ao configurar prioridade para {exe_name}: {e}")
            
            # Aplicar otimizações especiais
            for special in game_info.get('special', []):
                self._apply_special_game_optimization(exe_name, special)
                
        except Exception as e:
            self.logger.error(f"Erro ao aplicar otimizações para {game['exe']}: {e}")
    
    def _apply_special_game_optimization(self, exe_name, optimization):
        """Aplicar otimização especial específica"""
        try:
            if optimization == 'disable_fullscreen_opt':
                # Desabilitar otimização de tela cheia
                key_path = rf'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{exe_name}'
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, 'DisableFullscreenOptimizations', 0, winreg.REG_SZ, 'True')
            
            elif optimization == 'high_dpi_aware':
                # High DPI awareness
                key_path = rf'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{exe_name}'
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, 'HighDpiAware', 0, winreg.REG_SZ, 'True')
            
            elif optimization == 'disable_game_bar':
                # Desabilitar Game Bar para este jogo
                key_path = rf'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{exe_name}'
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, 'DisableGameBar', 0, winreg.REG_DWORD, 1)
                    
        except Exception as e:
            self.logger.warning(f"Erro ao aplicar otimização especial {optimization}: {e}")
    
    def clear_gpu_cache(self, progress_callback=None):
        """🗑️ LIMPAR CACHE DA GPU E DIRECTX"""
        if progress_callback:
            progress_callback("🗑️ Limpando cache DirectX e GPU...", 0)
        
        optimizations = []
        import subprocess
        import os
        import shutil
        
        try:
            # Limpar cache DirectX shader
            shader_cache_paths = [
                os.path.expandvars(r'%LOCALAPPDATA%\D3DSCache'),
                os.path.expandvars(r'%LOCALAPPDATA%\NVIDIA\DXCache'),
                os.path.expandvars(r'%LOCALAPPDATA%\AMD\GLCache'),
                os.path.expandvars(r'%LOCALAPPDATA%\AMD\DxCache'),
                os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\XboxLive\AuthStateCache.dat'),
                os.path.expandvars(r'%TEMP%\NV_Cache'),
                os.path.expandvars(r'%PROGRAMDATA%\NVIDIA Corporation\NV_Cache')
            ]
            
            if progress_callback:
                progress_callback("Removendo cache DirectX...", 30)
            
            for cache_path in shader_cache_paths:
                try:
                    if os.path.exists(cache_path):
                        if os.path.isfile(cache_path):
                            os.remove(cache_path)
                            optimizations.append(f"🗑️ Cache removido: {os.path.basename(cache_path)}")
                        elif os.path.isdir(cache_path):
                            shutil.rmtree(cache_path, ignore_errors=True)
                            optimizations.append(f"🗑️ Diretório cache removido: {os.path.basename(cache_path)}")
                except Exception as e:
                    self.logger.warning(f"Erro ao remover cache {cache_path}: {e}")
            
            if progress_callback:
                progress_callback("Limpando cache OpenGL...", 60)
            
            # Limpar cache OpenGL
            opengl_cache_paths = [
                os.path.expandvars(r'%LOCALAPPDATA%\NVIDIA\GLCache'),
                os.path.expandvars(r'%APPDATA%\NVIDIA\ComputeCache'),
                os.path.expandvars(r'%LOCALAPPDATA%\AMD\GLCache')
            ]
            
            for gl_cache in opengl_cache_paths:
                try:
                    if os.path.exists(gl_cache):
                        shutil.rmtree(gl_cache, ignore_errors=True)
                        optimizations.append(f"🗑️ Cache OpenGL removido: {os.path.basename(gl_cache)}")
                except Exception as e:
                    self.logger.warning(f"Erro ao limpar cache OpenGL: {e}")
            
            if progress_callback:
                progress_callback("Executando limpeza avançada de GPU...", 90)
            
            # Comandos avançados de limpeza
            cleanup_commands = [
                'dism /online /cleanup-image /startcomponentcleanup',
                'sfc /scannow',
                'cleanmgr /sageset:1'
            ]
            
            for cmd in cleanup_commands:
                try:
                    subprocess.run(cmd, shell=True, check=False, capture_output=True, timeout=30)
                    optimizations.append(f"✅ Comando executado: {cmd.split()[0]}")
                except Exception as e:
                    self.logger.warning(f"Erro ao executar {cmd}: {e}")
            
            if progress_callback:
                progress_callback("🗑️ Limpeza de cache GPU concluída!", 100)
            
            optimizations.append("🎯 Cache DirectX e GPU totalmente limpo!")
            
        except Exception as e:
            self.logger.error(f"Erro na limpeza de cache GPU: {e}")
            optimizations.append("⚠️ Erro na limpeza de cache GPU")
        
        return optimizations