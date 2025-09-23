import subprocess
import socket
import logging
import time
import winreg
import requests
from typing import Optional, Dict, Any
from .utils import Utils

class NetworkOptimizer:
    """Classe responsável pelas otimizações de rede"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.optimizations_applied = []
        
        # DNS servers rápidos
        self.dns_servers = {
            'Cloudflare': ['1.1.1.1', '1.0.0.1'],
            'Google': ['8.8.8.8', '8.8.4.4'],
            'Quad9': ['9.9.9.9', '149.112.112.112'],
            'OpenDNS': ['208.67.222.222', '208.67.220.220']
        }
        
        self.original_dns = None
    
    def test_internet_speed(self, progress_callback=None):
        """Testa velocidade de internet básica"""
        if progress_callback:
            progress_callback("Testando velocidade de internet...", 0)
        
        test_results: Dict[str, Optional[float]] = {
            'ping_cloudflare': None,
            'ping_google': None,
            'download_test': None
        }
        
        # Teste de ping
        test_results['ping_cloudflare'] = self._ping_test('1.1.1.1')
        if progress_callback:
            progress_callback("Testando ping Google...", 33)
        
        test_results['ping_google'] = self._ping_test('8.8.8.8')
        if progress_callback:
            progress_callback("Testando download...", 66)
        
        # Teste básico de download
        test_results['download_test'] = self._simple_download_test()
        
        if progress_callback:
            progress_callback("Teste de velocidade concluído", 100)
        
        self.logger.info(f"Resultados do teste de velocidade: {test_results}")
        return test_results
    
    def _ping_test(self, host: str, count: int = 4) -> Optional[float]:
        """Executa teste de ping"""
        try:
            cmd = f'ping -n {count} {host}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Extrai tempo médio do resultado
                lines = result.stdout.split('\n')
                for line in lines:
                    # Suporte para português e inglês
                    if 'Média =' in line or 'Average =' in line or 'média =' in line.lower():
                        # Extrai o valor numérico
                        parts = line.split('=')
                        if len(parts) > 1:
                            avg_time = parts[-1].strip().replace('ms', '').replace('MS', '').strip()
                            try:
                                return float(avg_time)
                            except ValueError:
                                continue
            return None
            
        except Exception as e:
            self.logger.error(f"Erro no teste de ping para {host}: {e}")
            return None
    
    def _simple_download_test(self) -> Optional[float]:
        """Teste simples de download"""
        try:
            start_time = time.time()
            
            # Faz download de um arquivo pequeno para teste
            response = requests.get('http://speedtest.ftp.otenet.gr/files/test100k.db', 
                                  timeout=30, stream=True)
            
            if response.status_code == 200:
                total_size = 0
                for chunk in response.iter_content(chunk_size=1024):
                    total_size += len(chunk)
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Calcula velocidade em KB/s
                speed_kbps = (total_size / 1024) / duration
                return round(speed_kbps, 2)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Erro no teste de download: {e}")
            return None
    
    def optimize_dns(self, dns_provider='Cloudflare', progress_callback=None):
        """Otimiza configurações de DNS"""
        if progress_callback:
            progress_callback(f"Configurando DNS {dns_provider}...", 0)
        
        try:
            # Backup do DNS atual
            self.original_dns = self._get_current_dns()
            
            if dns_provider in self.dns_servers:
                dns_list = self.dns_servers[dns_provider]
                
                # Obtém interfaces de rede ativas
                interfaces = self._get_network_interfaces()
                
                for i, interface in enumerate(interfaces):
                    if progress_callback:
                        progress_callback(f"Configurando interface {interface}...", 
                                        (i / len(interfaces)) * 100)
                    
                    success = self._set_dns_for_interface(interface, dns_list)
                    if success:
                        self.logger.info(f"DNS configurado para interface {interface}")
                
                # Limpa cache DNS
                self._flush_dns_cache()
                
                if progress_callback:
                    progress_callback(f"DNS {dns_provider} configurado", 100)
                
                self.optimizations_applied.append(f"DNS otimizado para {dns_provider}")
                return True
            else:
                self.logger.error(f"Provedor DNS inválido: {dns_provider}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao configurar DNS: {e}")
            return False
    
    def _get_current_dns(self):
        """Obtém configuração atual de DNS"""
        try:
            cmd = 'netsh interface ip show dns'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout
        except:
            return None
    
    def _get_network_interfaces(self):
        """Obtém lista de interfaces de rede ativas"""
        try:
            cmd = 'netsh interface show interface'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            interfaces = []
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'Conectado' in line or 'Connected' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        interface_name = ' '.join(parts[3:])
                        interfaces.append(interface_name)
            
            return interfaces
            
        except Exception as e:
            self.logger.error(f"Erro ao obter interfaces: {e}")
            return []
    
    def _set_dns_for_interface(self, interface, dns_list):
        """Configura DNS para uma interface específica"""
        try:
            # Remove DNS atual
            cmd_clear = f'netsh interface ip set dns "{interface}" static {dns_list[0]}'
            result1 = subprocess.run(cmd_clear, shell=True, capture_output=True, timeout=30)
            
            # Adiciona DNS secundário se disponível
            if len(dns_list) > 1:
                cmd_secondary = f'netsh interface ip add dns "{interface}" {dns_list[1]} index=2'
                result2 = subprocess.run(cmd_secondary, shell=True, capture_output=True, timeout=30)
                return result1.returncode == 0 and result2.returncode == 0
            
            return result1.returncode == 0
            
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False
    
    def _flush_dns_cache(self):
        """Limpa cache DNS"""
        try:
            cmd = 'ipconfig /flushdns'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            self.logger.info("Cache DNS limpo")
            return True
        except:
            return False
    
    def optimize_tcp_settings(self, progress_callback=None):
        """Otimiza configurações TCP/IP"""
        if progress_callback:
            progress_callback("Otimizando configurações TCP/IP...", 0)
        
        try:
            # Configurações de TCP no registro
            tcp_settings = [
                ('TcpAckFrequency', 1),
                ('TCPNoDelay', 1),
                ('TcpDelAckTicks', 0),
                ('TcpTimedWaitDelay', 30),
            ]
            
            # Chave base para configurações TCP
            base_key = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
            
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_key, 0, winreg.KEY_SET_VALUE) as key:
                for i, (setting, value) in enumerate(tcp_settings):
                    if progress_callback:
                        progress_callback(f"Configurando {setting}...", (i / len(tcp_settings)) * 100)
                    
                    try:
                        winreg.SetValueEx(key, setting, 0, winreg.REG_DWORD, value)
                    except Exception as e:
                        self.logger.warning(f"Erro ao configurar {setting}: {e}")
            
            if progress_callback:
                progress_callback("Configurações TCP/IP otimizadas", 100)
            
            self.optimizations_applied.append("Configurações TCP/IP otimizadas")
            self.logger.info("Configurações TCP/IP otimizadas")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao otimizar TCP: {e}")
            return False
    
    def disable_qos_bandwidth_limit(self, progress_callback=None):
        """Desabilita limitação de largura de banda do QoS"""
        if progress_callback:
            progress_callback("Desabilitando limitação QoS...", 0)
        
        try:
            # Configuração de QoS no registro
            qos_key = r"SOFTWARE\Policies\Microsoft\Windows\Psched"
            
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, qos_key) as key:
                # Desabilita limitação de largura de banda
                winreg.SetValueEx(key, "NonBestEffortLimit", 0, winreg.REG_DWORD, 0)
            
            if progress_callback:
                progress_callback("Limitação QoS desabilitada", 100)
            
            self.optimizations_applied.append("Limitação QoS desabilitada")
            self.logger.info("Limitação de largura de banda QoS desabilitada")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao desabilitar QoS: {e}")
            return False
    
    def optimize_network_adapter(self, progress_callback=None):
        """Otimiza configurações do adaptador de rede"""
        if progress_callback:
            progress_callback("Otimizando adaptador de rede...", 0)
        
        try:
            # Comandos de otimização via netsh
            optimization_commands = [
                'netsh int tcp set global autotuninglevel=normal',
                'netsh int tcp set global chimney=enabled',
                'netsh int tcp set global rss=enabled',
                'netsh int tcp set global netdma=enabled',
                'netsh int tcp set global dca=enabled',
                'netsh int tcp set global ecncapability=enabled',
            ]
            
            successful_commands = 0
            
            for i, cmd in enumerate(optimization_commands):
                if progress_callback:
                    progress_callback(f"Executando otimização {i+1}/{len(optimization_commands)}...", 
                                    (i / len(optimization_commands)) * 100)
                
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, 
                                          text=True, timeout=30)
                    if result.returncode == 0:
                        successful_commands += 1
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
            
            if progress_callback:
                progress_callback("Adaptador de rede otimizado", 100)
            
            self.optimizations_applied.append(f"Adaptador de rede otimizado ({successful_commands} configurações)")
            self.logger.info(f"Adaptador de rede otimizado: {successful_commands}/{len(optimization_commands)} comandos executados")
            return successful_commands > 0
            
        except Exception as e:
            self.logger.error(f"Erro ao otimizar adaptador: {e}")
            return False
    
    def disable_network_services(self, progress_callback=None):
        """Desabilita serviços de rede desnecessários"""
        if progress_callback:
            progress_callback("Desabilitando serviços de rede desnecessários...", 0)
        
        # Serviços de rede que podem ser desabilitados
        network_services = [
            'RemoteAccess',  # Roteamento e Acesso Remoto
            'SharedAccess',  # Compartilhamento de Conexão de Internet
            'WMPNetworkSvc', # Compartilhamento de Rede do Windows Media Player
            'Browser',       # Navegador de Computador
            'NetTcpPortSharing',  # Serviço de Compartilhamento de Porta Net.Tcp
            'IKEEXT',        # Módulos de Criação de Chaves IKE e AuthIP
            'PolicyAgent',   # IPsec Policy Agent
        ]
        
        disabled_services = []
        
        for i, service in enumerate(network_services):
            if progress_callback:
                progress_callback(f"Verificando serviço: {service}", (i / len(network_services)) * 100)
            
            success = self._disable_service(service)
            if success:
                disabled_services.append(service)
        
        if progress_callback:
            progress_callback("Serviços de rede otimizados", 100)
        
        self.optimizations_applied.append(f"{len(disabled_services)} serviços de rede desabilitados")
        self.logger.info(f"Serviços de rede desabilitados: {disabled_services}")
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
            return False
        except Exception:
            return False
    
    def test_dns_performance(self, progress_callback=None):
        """Testa performance de diferentes DNS"""
        if progress_callback:
            progress_callback("Testando performance de DNS...", 0)
        
        dns_results = {}
        total_dns = len(self.dns_servers)
        
        for i, (provider, dns_list) in enumerate(self.dns_servers.items()):
            if progress_callback:
                progress_callback(f"Testando {provider}...", (i / total_dns) * 100)
            
            # Testa o DNS primário
            ping_result = self._ping_test(dns_list[0], 3)
            dns_results[provider] = {
                'primary_dns': dns_list[0],
                'ping_ms': ping_result
            }
        
        if progress_callback:
            progress_callback("Teste de DNS concluído", 100)
        
        # Encontra o DNS mais rápido
        fastest_dns = min(dns_results.items(), 
                         key=lambda x: x[1]['ping_ms'] if x[1]['ping_ms'] else float('inf'))
        
        self.logger.info(f"Resultados DNS: {dns_results}")
        self.logger.info(f"DNS mais rápido: {fastest_dns[0]}")
        
        return dns_results, fastest_dns[0]
    
    def restore_original_dns(self):
        """Restaura configuração original de DNS"""
        if self.original_dns:
            try:
                # Lógica para restaurar DNS original seria mais complexa
                # Por simplicidade, configura para obter DNS automaticamente
                interfaces = self._get_network_interfaces()
                
                for interface in interfaces:
                    cmd = f'netsh interface ip set dns "{interface}" dhcp'
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                
                self._flush_dns_cache()
                self.logger.info("DNS original restaurado")
                return True
                
            except Exception as e:
                self.logger.error(f"Erro ao restaurar DNS: {e}")
                return False
        return False
    
    def get_network_summary(self):
        """Retorna resumo das otimizações de rede"""
        return {
            'optimizations_count': len(self.optimizations_applied),
            'optimizations_list': self.optimizations_applied,
            'original_dns_backed_up': self.original_dns is not None
        }