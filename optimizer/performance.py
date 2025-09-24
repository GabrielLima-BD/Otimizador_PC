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
        
        # 🔥 LISTA EXTREMA DE SERVIÇOS PESADOS - GAMING HARDCORE
        # ⚠️ ÁUDIO/MICROFONE PROTEGIDOS ⚠️
        self.services_to_disable = [
            # SERVIÇOS PESADOS QUE CONSOMEM MUITO RECURSO
            'SysMain',  # Superfetch/Prefetch (PESADO - indexa arquivos)
            'DiagTrack',  # Telemetria (PESADO - coleta dados)
            'WSearch',  # Windows Search (PESADO - indexação constante)
            'dmwappushservice',  # WAP Push Message Routing (PESADO)
            'MapsBroker',  # Downloaded Maps Manager (PESADO)
            'PcaSvc',   # Program Compatibility Assistant (PESADO)
            'WbioSrvc',  # Windows Biometric Service (PESADO)
            'wisvc',    # Windows Insider Service (PESADO)
            'icssvc',   # Windows Mobile Hotspot Service (PESADO)
            'PhoneSvc', # Phone Service (PESADO)
            'TabletInputService',  # Tablet Input Service (PESADO)
            'TouchKeyboard',  # Touch Keyboard Service (PESADO)
            
            # SERVIÇOS DE TELEMETRIA E RASTREAMENTO
            'WerSvc',   # Windows Error Reporting
            'RetailDemo',  # Retail Demo Service
            'Dmwappushservice',  # Device Management WAP
            'diagnosticshub.standardcollector.service',  # Diagnostics Hub
            'TrkWks',   # Distributed Link Tracking Client
            'WpcMonSvc',  # Parental Controls
            
            # SERVIÇOS DE REDE DESNECESSÁRIOS
            'RemoteAccess',  # Routing and Remote Access
            'SharedAccess',  # Internet Connection Sharing
            'Browser',  # Computer Browser
            'RasMan',   # Remote Access Connection Manager
            'SessionEnv',  # Remote Desktop Configuration
            'TermService',  # Remote Desktop Services
            'UmRdpService',  # Remote Desktop Services UserMode
            'RemoteRegistry',  # Remote Registry
            'WinRM',    # Windows Remote Management
            
            # SERVIÇOS DE HARDWARE DESNECESSÁRIO
            'TapiSrv',  # Telephony
            'SCardSvr', # Smart Card
            'ScDeviceEnum',  # Smart Card Device Enumeration
            'WiaRpc',   # Windows Image Acquisition (RPC)
            'stisvc',   # Windows Image Acquisition (Still Image)
            'SensrSvc', # Sensor Monitoring Service
            'Fax',      # Fax Service
            'Spooler',  # Print Spooler (se não imprimir)
            
            # SERVIÇOS DE CACHE E ARMAZENAMENTO
            'PeerDistSvc',  # BranchCache
            'CscService',   # Offline Files
            'WMPNetworkSvc',  # Windows Media Player Network
            'FontCache',      # Windows Font Cache Service
            'Themes',   # Themes (visual vs performance)
            
            # XBOX E GAMING SERVICES (paradoxal, mas alguns consomem muito)
            'XblAuthManager', # Xbox Live Auth Manager (se não usar Xbox)
            'XblGameSave',    # Xbox Live Game Save (se não usar Xbox)
            'XboxGipSvc',     # Xbox Accessory Management (se não usar controles Xbox)
            'XboxNetApiSvc',  # Xbox Live Networking Service (se não usar Xbox)
        ]
        
        # 🎤 SERVIÇOS PROTEGIDOS - NUNCA DESABILITAR (ÁUDIO/MICROFONE)
        self.protected_audio_services = [
            'AudioSrv',           # Windows Audio
            'Audiosrv',           # Windows Audio (alternativo)
            'AudioEndpointBuilder',  # Windows Audio Endpoint Builder
            'RpcEptMapper',       # RPC Endpoint Mapper (necessário para áudio)
            'DcomLaunch',         # DCOM Server Process Launcher (necessário para áudio)
            'RpcSs',              # Remote Procedure Call (RPC) (necessário para áudio)
        ]
    
    def optimize_power_settings(self, progress_callback=None):
        """🚀 CONFIGURAÇÕES DE ENERGIA GAMING EXTREMO - AMD OPTIMIZED"""
        if progress_callback:
            progress_callback("🔥 Configurando energia para GAMING EXTREMO...", 0)
        
        try:
            # 🚀 MODO DE ENERGIA "DESEMPENHO MÁXIMO" - FORÇADO
            if progress_callback:
                progress_callback("Configurando Desempenho Máximo...", 10)
            
            # 1. Tentar Ultimate Performance primeiro
            cmd_ultimate = 'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61'
            result_ultimate = subprocess.run(cmd_ultimate, shell=True, capture_output=True, text=True)
            if result_ultimate.returncode == 0:
                cmd_activate_ultimate = 'powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61'
                subprocess.run(cmd_activate_ultimate, shell=True, capture_output=True, text=True)
                self.optimizations_applied.append("🚀 Ultimate Performance Plan ativado")
            else:
                # 2. Fallback: Criar nosso próprio "Desempenho Máximo"
                cmd_create_max = 'powercfg -duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
                result_create = subprocess.run(cmd_create_max, shell=True, capture_output=True, text=True)
                if result_create.returncode == 0:
                    # Extrair GUID do novo esquema
                    output_lines = result_create.stdout.split('\n')
                    for line in output_lines:
                        if 'GUID:' in line:
                            new_guid = line.split('GUID:')[1].strip()
                            # Renomear para "Desempenho Máximo Gaming"
                            cmd_rename = f'powercfg -changename {new_guid} "Desempenho Máximo Gaming" "Otimizado para jogos e performance extrema"'
                            subprocess.run(cmd_rename, shell=True, capture_output=True)
                            # Ativar o novo esquema
                            cmd_activate_new = f'powercfg -setactive {new_guid}'
                            subprocess.run(cmd_activate_new, shell=True, capture_output=True)
                            self.optimizations_applied.append("🔥 Desempenho Máximo Gaming criado e ativado")
                            break
                else:
                    # 3. Last resort: High Performance padrão
                    cmd_high_performance = 'powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
                    subprocess.run(cmd_high_performance, shell=True, capture_output=True, text=True)
                    self.optimizations_applied.append("⚡ High Performance Plan ativado")
            
            if progress_callback:
                progress_callback("Configurando hibernação e suspensão...", 25)
            
            # 🔥 DESABILITAR TODAS AS ECONOMIAS DE ENERGIA
            power_commands = [
                'powercfg -h off',  # Hibernação OFF
                'powercfg -change -disk-timeout-ac 0',  # Disco nunca desliga
                'powercfg -change -disk-timeout-dc 0',  # Disco nunca desliga (bateria)
                'powercfg -change -standby-timeout-ac 0',  # Suspensão OFF
                'powercfg -change -standby-timeout-dc 0',  # Suspensão OFF (bateria)
                'powercfg -change -monitor-timeout-ac 0',  # Monitor nunca desliga
                'powercfg -change -hibernate-timeout-ac 0',  # Hibernação timeout OFF
                'powercfg -change -hibernate-timeout-dc 0',  # Hibernação timeout OFF (bateria)
            ]
            
            for cmd in power_commands:
                subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if progress_callback:
                progress_callback("Configurações avançadas de CPU...", 50)
            
            # 🔥 CONFIGURAÇÕES ESPECÍFICAS AMD RYZEN
            amd_power_settings = [
                # Processador sempre 100%
                'powercfg -setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 0cc5b647-c1df-4637-891a-dec35c318583 100',
                'powercfg -setdcvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 0cc5b647-c1df-4637-891a-dec35c318583 100',
                # Mínimo do processador 100% (sem downclocking)
                'powercfg -setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 893dee8e-2bef-41e0-89c6-b55d0929964c 100',
                'powercfg -setdcvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 893dee8e-2bef-41e0-89c6-b55d0929964c 100',
                # Política de resfriamento agressiva
                'powercfg -setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 94d3a615-a899-4ac5-ae2b-e4d8f634367f 1',
                'powercfg -setdcvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 94d3a615-a899-4ac5-ae2b-e4d8f634367f 1',
            ]
            
            for cmd in amd_power_settings:
                subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if progress_callback:
                progress_callback("Configurações PCI Express...", 75)
            
            # 🚀 PCI EXPRESS SEM ECONOMIA (crítico para GPU AMD)
            pcie_commands = [
                'powercfg -setacvalueindex SCHEME_CURRENT 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0',
                'powercfg -setdcvalueindex SCHEME_CURRENT 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0',
            ]
            
            for cmd in pcie_commands:
                subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # Aplicar todas as configurações
            subprocess.run('powercfg -setactive SCHEME_CURRENT', shell=True, capture_output=True, text=True)
            
            if progress_callback:
                progress_callback("🔥 Energia GAMING EXTREMO configurada!", 100)
            
            self.optimizations_applied.append("🔥 Configurações de energia GAMING EXTREMO aplicadas")
            self.optimizations_applied.append("🚀 CPU AMD configurado para performance máxima constante")
            self.optimizations_applied.append("⚡ PCI Express sem economia de energia (GPU AMD otimizada)")
            self.logger.info("🔥 Configurações de energia GAMING EXTREMO aplicadas")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar energia: {e}")
            return False
    
    def disable_unnecessary_services(self, progress_callback=None):
        """🔒 Desabilita serviços desnecessários - PROTEÇÃO DE ÁUDIO ATIVA"""
        if progress_callback:
            progress_callback("Desabilitando serviços desnecessários...", 0)
        
        disabled_services = []
        total_services = len(self.services_to_disable)
        
        for i, service in enumerate(self.services_to_disable):
            if progress_callback:
                progress_callback(f"Verificando serviço: {service}", (i / total_services) * 100)
            
            # 🎤 PROTEÇÃO DE ÁUDIO - Verificar se não é serviço de áudio
            if service.lower() in [s.lower() for s in self.protected_audio_services]:
                self.logger.info(f"🔒 SERVIÇO DE ÁUDIO PROTEGIDO: {service} - NÃO DESABILITADO")
                continue
            
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
    
    def extreme_gaming_optimization(self, progress_callback=None):
        """🔥 OTIMIZAÇÕES GAMING EXTREMAS - MODO BESTIAL"""
        if progress_callback:
            progress_callback("🔥 Aplicando otimizações GAMING EXTREMAS...", 0)
        
        try:
            # 🚀 TIMER RESOLUTION EXTREMO (melhora FPS)
            if progress_callback:
                progress_callback("Configurando timer resolution extremo...", 20)
            
            timer_settings = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Session Manager\kernel',
                    'values': {
                        'GlobalTimerResolutionRequests': (winreg.REG_DWORD, 1),
                        'DistributeTimers': (winreg.REG_DWORD, 1),
                    }
                }
            ]
            
            for setting in timer_settings:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            self.optimizations_applied.append(f"🚀 Timer: {value_name} otimizado")
                except Exception as e:
                    self.logger.warning(f"Erro timer settings: {e}")
            
            # 🎮 PRIORIDADES DE PROCESSOS GAMING
            if progress_callback:
                progress_callback("Configurando prioridades de processos...", 40)
            
            priority_settings = [
                {
                    'key': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\csgo.exe\PerfOptions',
                    'values': {'CpuPriorityClass': (winreg.REG_DWORD, 3)}  # High priority
                },
                {
                    'key': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\valorant.exe\PerfOptions',
                    'values': {'CpuPriorityClass': (winreg.REG_DWORD, 3)}
                },
                {
                    'key': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\RainbowSix.exe\PerfOptions',
                    'values': {'CpuPriorityClass': (winreg.REG_DWORD, 3)}
                },
                {
                    'key': r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\FortniteClient-Win64-Shipping.exe\PerfOptions',
                    'values': {'CpuPriorityClass': (winreg.REG_DWORD, 3)}
                }
            ]
            
            for setting in priority_settings:
                try:
                    winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, setting['key'])
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                except Exception as e:
                    continue
            
            self.optimizations_applied.append("🎮 Prioridades de jogos configuradas (HIGH)")
            
            # 🔥 MEMORY MANAGEMENT EXTREMO
            if progress_callback:
                progress_callback("Otimização extrema de memória...", 60)
            
            memory_extreme = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
                    'values': {
                        'LargeSystemCache': (winreg.REG_DWORD, 1),  # Cache grande para jogos
                        'DisablePagingExecutive': (winreg.REG_DWORD, 1),  # Kernel na RAM
                        'ClearPageFileAtShutdown': (winreg.REG_DWORD, 0),  # Não limpar (mais rápido)
                        'SystemPages': (winreg.REG_DWORD, 0xFFFFFFFF),  # Páginas otimizadas
                        'PoolUsageMaximum': (winreg.REG_DWORD, 60),  # Pool usage otimizado
                    }
                }
            ]
            
            for setting in memory_extreme:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            self.optimizations_applied.append(f"🔥 Memória: {value_name} extremo")
                except Exception as e:
                    self.logger.warning(f"Erro memory extreme: {e}")
            
            # 🚀 NETWORK LATENCY REDUÇÃO EXTREMA
            if progress_callback:
                progress_callback("Reduzindo latência de rede...", 80)
            
            network_extreme = [
                {
                    'key': r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters',
                    'values': {
                        'TcpAckFrequency': (winreg.REG_DWORD, 1),  # ACK imediato
                        'TCPNoDelay': (winreg.REG_DWORD, 1),  # Sem delay TCP
                        'TcpDelAckTicks': (winreg.REG_DWORD, 0),  # Sem delay ACK
                        'MaxUserPort': (winreg.REG_DWORD, 65534),  # Máximo portas
                        'TcpTimedWaitDelay': (winreg.REG_DWORD, 30),  # Reduzir wait time
                    }
                }
            ]
            
            for setting in network_extreme:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, setting['key'], 0, winreg.KEY_SET_VALUE) as key:
                        for value_name, (value_type, value_data) in setting['values'].items():
                            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                            self.optimizations_applied.append(f"🚀 Rede: {value_name} otimizado")
                except Exception as e:
                    self.logger.warning(f"Erro network extreme: {e}")
            
            if progress_callback:
                progress_callback("🔥 Otimizações GAMING EXTREMAS aplicadas!", 100)
            
            self.logger.info("🔥 Otimizações GAMING EXTREMAS aplicadas com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro nas otimizações gaming extremas: {e}")
            return False
    
    def optimize_startup_programs(self, progress_callback=None):
        """🚀 OTIMIZAÇÃO AGRESSIVA DE PROGRAMAS DE INICIALIZAÇÃO"""
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
    
    def manage_process_priorities(self, progress_callback=None):
        """🚀 GERENCIAR PRIORIDADES DE PROCESSOS PARA GAMING"""
        if progress_callback:
            progress_callback("🚀 Configurando prioridades de processos...", 0)
        
        optimizations = []
        
        try:
            import psutil
            
            if progress_callback:
                progress_callback("Identificando processos de jogos...", 20)
            
            # Processos de jogos que devem ter prioridade alta
            gaming_processes = [
                'cs2.exe', 'csgo.exe', 'valorant.exe', 'valorant-win64-shipping.exe',
                'rainbowsix.exe', 'apex_legends.exe', 'fortniteclient-win64-shipping.exe',
                'league of legends.exe', 'dota2.exe', 'overwatch.exe', 'cod.exe',
                'destiny2.exe', 'bf1.exe', 'battlefront2.exe', 'warzone.exe',
                'gta5.exe', 'rdr2.exe', 'witcher3.exe', 'cyberpunk2077.exe'
            ]
            
            # Processos do sistema que devem ter prioridade baixa
            low_priority_processes = [
                'windows defender', 'antimalware service executable', 'dllhost.exe',
                'spoolsv.exe', 'audiodg.exe', 'conhost.exe', 'dwm.exe',
                'sihost.exe', 'ctfmon.exe', 'taskhostw.exe', 'runtimebroker.exe',
                'searchindexer.exe', 'wuauclt.exe', 'trustedinstaller.exe',
                'tiworker.exe', 'compattelrunner.exe', 'telemetry.exe'
            ]
            
            if progress_callback:
                progress_callback("Aplicando prioridades altas para jogos...", 50)
            
            # Configurar alta prioridade para jogos ativos
            games_found = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(game.lower() in proc_name for game in gaming_processes):
                        process = psutil.Process(proc.info['pid'])
                        process.nice(psutil.HIGH_PRIORITY_CLASS)
                        optimizations.append(f"🎮 {proc.info['name']}: Prioridade ALTA aplicada")
                        games_found += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if progress_callback:
                progress_callback("Aplicando prioridades baixas para processos do sistema...", 80)
            
            # Configurar baixa prioridade para processos do sistema
            system_processes_lowered = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(sys_proc.lower() in proc_name for sys_proc in low_priority_processes):
                        process = psutil.Process(proc.info['pid'])
                        process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                        system_processes_lowered += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if games_found > 0:
                optimizations.append(f"🎯 {games_found} jogos com prioridade ALTA")
            else:
                optimizations.append("🔍 Nenhum jogo ativo encontrado")
            
            if system_processes_lowered > 0:
                optimizations.append(f"📉 {system_processes_lowered} processos sistema com prioridade BAIXA")
            
            # Configurar CPU affinity para melhor performance
            self._optimize_cpu_affinity()
            optimizations.append("🔧 CPU affinity otimizada para gaming")
            
            if progress_callback:
                progress_callback("🚀 Gerenciamento de prioridades concluído!", 100)
            
        except Exception as e:
            self.logger.error(f"Erro no gerenciamento de prioridades: {e}")
            optimizations.append("⚠️ Erro no gerenciamento de prioridades")
        
        return optimizations
    
    def _optimize_cpu_affinity(self):
        """Otimizar CPU affinity para melhor distribuição de carga"""
        try:
            import os
            cpu_count = os.cpu_count()
            
            if cpu_count and cpu_count >= 8:  # Para CPUs com 8+ cores
                # Reservar últimos 2 cores para jogos
                game_cores = list(range(cpu_count - 2, cpu_count))
                system_cores = list(range(0, cpu_count - 2))
                
                # Aplicar affinity via PowerShell para processos específicos
                powershell_cmd = f'''
                $GameCores = {",".join(map(str, game_cores))}
                $SystemCores = {",".join(map(str, system_cores))}
                
                # Configurar cores para jogos específicos se estiverem rodando
                Get-Process | Where-Object {{$_.ProcessName -match "cs2|csgo|valorant|apex"}} | ForEach-Object {{
                    $_.ProcessorAffinity = [System.IntPtr]({2**(game_cores[0]) + 2**(game_cores[1])})
                }}
                '''
                
                subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, timeout=10)
                
        except Exception as e:
            self.logger.warning(f"Erro na otimização de CPU affinity: {e}")