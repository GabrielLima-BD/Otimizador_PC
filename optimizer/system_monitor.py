import psutil
import time
import threading
import logging
from datetime import datetime, timedelta
from collections import deque
import json
import os

class SystemMonitor:
    """Monitor de sistema em tempo real com alertas e histórico"""
    
    def __init__(self, history_duration=3600):  # 1 hora de histórico
        self.logger = logging.getLogger(__name__)
        self.history_duration = history_duration
        self.monitoring = False
        self.monitor_thread = None
        
        # Histórico de dados (últimos X segundos)
        self.cpu_history = deque(maxlen=history_duration)
        self.memory_history = deque(maxlen=history_duration)
        self.disk_history = deque(maxlen=history_duration)
        self.network_history = deque(maxlen=history_duration)
        self.temperature_history = deque(maxlen=history_duration)
        
        # Callbacks para alertas
        self.alert_callbacks = []
        
        # Configurações de alerta
        self.alert_thresholds = {
            'cpu': 85.0,          # % CPU
            'memory': 90.0,       # % Memória
            'disk': 95.0,         # % Disco
            'temperature': 80.0,  # °C
            'network_errors': 10  # Erros por minuto
        }
        
        # Estatísticas da sessão atual
        self.session_stats = {
            'start_time': datetime.now(),
            'cpu_avg': 0.0,
            'memory_avg': 0.0,
            'disk_avg': 0.0,
            'alerts_triggered': 0,
            'peak_cpu': 0.0,
            'peak_memory': 0.0,
            'uptime': 0
        }
    
    def start_monitoring(self, interval=1.0, progress_callback=None):
        """Inicia o monitoramento em tempo real"""
        if self.monitoring:
            return False
        
        self.monitoring = True
        self.session_stats['start_time'] = datetime.now()
        
        if progress_callback:
            progress_callback("Iniciando monitoramento do sistema...", 0)
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        if progress_callback:
            progress_callback("Monitoramento iniciado", 100)
        
        self.logger.info("Monitoramento do sistema iniciado")
        return True
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        self.logger.info("Monitoramento do sistema parado")
    
    def _monitor_loop(self, interval):
        """Loop principal de monitoramento"""
        last_network = self._get_network_stats()
        
        while self.monitoring:
            try:
                timestamp = time.time()
                
                # Coletar dados do sistema
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                network = self._get_network_stats()
                temperatures = self._get_temperatures()
                
                # Calcular uso de rede (diferença desde última medição)
                network_usage = self._calculate_network_usage(network, last_network, interval)
                last_network = network
                
                # Armazenar no histórico
                self.cpu_history.append((timestamp, cpu_percent))
                self.memory_history.append((timestamp, memory.percent))
                self.disk_history.append((timestamp, disk.percent))
                self.network_history.append((timestamp, network_usage))
                self.temperature_history.append((timestamp, temperatures))
                
                # Atualizar estatísticas da sessão
                self._update_session_stats(cpu_percent, memory.percent, disk.percent)
                
                # Verificar alertas
                self._check_alerts(cpu_percent, memory.percent, disk.percent, temperatures, network_usage)
                
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Erro no loop de monitoramento: {e}")
                time.sleep(interval)
    
    def _get_network_stats(self):
        """Obtém estatísticas de rede"""
        try:
            network = psutil.net_io_counters()
            return {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv,
                'errin': network.errin,
                'errout': network.errout,
                'dropin': network.dropin,
                'dropout': network.dropout
            }
        except:
            return {
                'bytes_sent': 0, 'bytes_recv': 0,
                'packets_sent': 0, 'packets_recv': 0,
                'errin': 0, 'errout': 0,
                'dropin': 0, 'dropout': 0
            }
    
    def _calculate_network_usage(self, current, previous, interval):
        """Calcula uso de rede por segundo"""
        if not previous:
            return {'upload': 0, 'download': 0, 'errors': 0}
        
        upload = (current['bytes_sent'] - previous['bytes_sent']) / interval
        download = (current['bytes_recv'] - previous['bytes_recv']) / interval
        errors = ((current['errin'] + current['errout']) - 
                 (previous['errin'] + previous['errout'])) / interval
        
        return {
            'upload': max(0, upload),
            'download': max(0, download),
            'errors': max(0, errors)
        }
    
    def _get_temperatures(self):
        """Obtém temperaturas do sistema"""
        temperatures = {'cpu': None, 'gpu': None}
        
        try:
            # Verificar se sensors_temperatures está disponível (principalmente em Linux)
            sensors_temperatures = getattr(psutil, 'sensors_temperatures', None)
            if sensors_temperatures:
                temps = sensors_temperatures()
                if temps:
                    # Procurar temperatura da CPU
                    for name, entries in temps.items():
                        if 'cpu' in name.lower() or 'core' in name.lower():
                            if entries:
                                temperatures['cpu'] = entries[0].current
                                break
                    
                    # Procurar temperatura da GPU
                    for name, entries in temps.items():
                        if 'gpu' in name.lower() or 'nvidia' in name.lower() or 'amd' in name.lower():
                            if entries:
                                temperatures['gpu'] = entries[0].current
                                break
            else:
                # Em Windows, sensors_temperatures pode não estar disponível
                # Tentar métodos alternativos ou deixar como None
                temperatures = self._get_windows_temperatures()
        except Exception:
            pass
        
        return temperatures
    
    def _get_windows_temperatures(self):
        """Tenta obter temperaturas no Windows usando métodos alternativos"""
        temperatures = {'cpu': None, 'gpu': None}
        
        try:
            # Tentar usar WMI se disponível
            import wmi
            c = wmi.WMI(namespace="root\\wmi")
            
            # Tentar obter temperatura da CPU via WMI
            temperature_info = c.MSAcpi_ThermalZoneTemperature()
            if temperature_info:
                # Converter de décimos de Kelvin para Celsius
                temp_kelvin = temperature_info[0].CurrentTemperature / 10.0
                temp_celsius = temp_kelvin - 273.15
                if 0 < temp_celsius < 150:  # Sanity check
                    temperatures['cpu'] = temp_celsius
        except Exception:
            # Se WMI não estiver disponível ou falhar, deixar como None
            pass
        
        return temperatures
    
    def collect_metrics(self):
        """Coleta métricas atuais do sistema"""
        try:
            # Coletar dados básicos
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = self._get_network_stats()
            temperatures = self._get_temperatures()
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_total_gb': memory.total / (1024**3),
                'disk_percent': disk.percent,
                'disk_used_gb': disk.used / (1024**3),
                'disk_total_gb': disk.total / (1024**3),
                'network': network,
                'temperatures': temperatures,
                'timestamp': time.time()
            }
        except Exception as e:
            self.logger.error(f"Erro ao coletar métricas: {e}")
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'disk_percent': 0,
                'network': {},
                'temperatures': {'cpu': None, 'gpu': None},
                'timestamp': time.time()
            }
    
    def calculate_health_score(self, metrics=None):
        """Calcula pontuação de saúde do sistema (0-100)"""
        if not metrics:
            metrics = self.collect_metrics()
        
        # Componentes da pontuação
        cpu_score = max(0, 100 - metrics['cpu_percent'])
        memory_score = max(0, 100 - metrics['memory_percent'])
        disk_score = max(0, 100 - metrics['disk_percent'])
        
        # Pontuação de temperatura
        temp_score = 100
        if metrics['temperatures']['cpu']:
            if metrics['temperatures']['cpu'] > 80:
                temp_score = max(0, 100 - (metrics['temperatures']['cpu'] - 80) * 5)
            elif metrics['temperatures']['cpu'] > 70:
                temp_score = 90
        
        # Pesos para cada componente
        weights = {
            'cpu': 0.3,
            'memory': 0.3,
            'disk': 0.2,
            'temperature': 0.2
        }
        
        # Calcular pontuação final
        final_score = (
            cpu_score * weights['cpu'] +
            memory_score * weights['memory'] +
            disk_score * weights['disk'] +
            temp_score * weights['temperature']
        )
        
        return round(final_score, 1)
    
    def _update_session_stats(self, cpu, memory, disk):
        """Atualiza estatísticas da sessão"""
        # Calcular médias
        if self.cpu_history:
            self.session_stats['cpu_avg'] = sum(x[1] for x in self.cpu_history) / len(self.cpu_history)
        
        if self.memory_history:
            self.session_stats['memory_avg'] = sum(x[1] for x in self.memory_history) / len(self.memory_history)
        
        if self.disk_history:
            self.session_stats['disk_avg'] = sum(x[1] for x in self.disk_history) / len(self.disk_history)
        
        # Atualizar picos
        self.session_stats['peak_cpu'] = max(self.session_stats['peak_cpu'], cpu)
        self.session_stats['peak_memory'] = max(self.session_stats['peak_memory'], memory)
        
        # Calcular uptime
        uptime_delta = datetime.now() - self.session_stats['start_time']
        self.session_stats['uptime'] = int(uptime_delta.total_seconds())
    
    def _check_alerts(self, cpu, memory, disk, temperatures, network):
        """Verifica condições de alerta"""
        alerts = []
        
        # Alerta de CPU
        if cpu > self.alert_thresholds['cpu']:
            alerts.append({
                'type': 'cpu',
                'severity': 'high' if cpu > 95 else 'medium',
                'message': f'Alto uso de CPU: {cpu:.1f}%',
                'value': cpu,
                'threshold': self.alert_thresholds['cpu']
            })
        
        # Alerta de memória
        if memory > self.alert_thresholds['memory']:
            alerts.append({
                'type': 'memory',
                'severity': 'high' if memory > 95 else 'medium',
                'message': f'Alto uso de memória: {memory:.1f}%',
                'value': memory,
                'threshold': self.alert_thresholds['memory']
            })
        
        # Alerta de disco
        if disk > self.alert_thresholds['disk']:
            alerts.append({
                'type': 'disk',
                'severity': 'critical' if disk > 98 else 'high',
                'message': f'Espaço em disco baixo: {disk:.1f}%',
                'value': disk,
                'threshold': self.alert_thresholds['disk']
            })
        
        # Alerta de temperatura
        if temperatures['cpu'] and temperatures['cpu'] > self.alert_thresholds['temperature']:
            alerts.append({
                'type': 'temperature',
                'severity': 'critical' if temperatures['cpu'] > 90 else 'high',
                'message': f'Temperatura alta da CPU: {temperatures["cpu"]:.1f}°C',
                'value': temperatures['cpu'],
                'threshold': self.alert_thresholds['temperature']
            })
        
        # Alerta de erros de rede
        if network['errors'] > self.alert_thresholds['network_errors']:
            alerts.append({
                'type': 'network',
                'severity': 'medium',
                'message': f'Muitos erros de rede: {network["errors"]:.0f}/s',
                'value': network['errors'],
                'threshold': self.alert_thresholds['network_errors']
            })
        
        # Processar alertas
        for alert in alerts:
            self._trigger_alert(alert)
    
    def _trigger_alert(self, alert):
        """Dispara um alerta"""
        alert['timestamp'] = datetime.now()
        self.session_stats['alerts_triggered'] += 1
        
        # Chamar callbacks registrados
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Erro no callback de alerta: {e}")
        
        # Log do alerta
        self.logger.warning(f"ALERTA: {alert['message']}")
    
    def add_alert_callback(self, callback):
        """Adiciona callback para alertas"""
        self.alert_callbacks.append(callback)
    
    def get_current_stats(self):
        """Obtém estatísticas atuais do sistema"""
        try:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Obter processos que mais consomem recursos
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 0 or proc_info['memory_percent'] > 0:
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Ordenar por uso de CPU
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            top_processes = processes[:10]
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu,
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                },
                'memory': {
                    'percent': memory.percent,
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used
                },
                'disk': {
                    'percent': disk.percent,
                    'total': disk.total,
                    'free': disk.free,
                    'used': disk.used
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'top_processes': top_processes,
                'uptime': time.time() - psutil.boot_time()
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def get_historical_data(self, data_type='all', duration=3600):
        """Obtém dados históricos"""
        current_time = time.time()
        start_time = current_time - duration
        
        def filter_data(data_deque):
            return [(t, v) for t, v in data_deque if t >= start_time]
        
        if data_type == 'cpu':
            return filter_data(self.cpu_history)
        elif data_type == 'memory':
            return filter_data(self.memory_history)
        elif data_type == 'disk':
            return filter_data(self.disk_history)
        elif data_type == 'network':
            return filter_data(self.network_history)
        elif data_type == 'temperature':
            return filter_data(self.temperature_history)
        else:
            return {
                'cpu': filter_data(self.cpu_history),
                'memory': filter_data(self.memory_history),
                'disk': filter_data(self.disk_history),
                'network': filter_data(self.network_history),
                'temperature': filter_data(self.temperature_history)
            }
    
    def export_session_report(self, filepath):
        """Exporta relatório da sessão de monitoramento"""
        try:
            report = {
                'session_info': {
                    'start_time': self.session_stats['start_time'].isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration_seconds': self.session_stats['uptime']
                },
                'statistics': self.session_stats,
                'thresholds': self.alert_thresholds,
                'historical_data': {
                    'cpu': list(self.cpu_history),
                    'memory': list(self.memory_history),
                    'disk': list(self.disk_history),
                    'network': list(self.network_history),
                    'temperature': list(self.temperature_history)
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Relatório exportado para: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar relatório: {e}")
            return False
    
    def set_alert_threshold(self, metric, value):
        """Define limiar de alerta para uma métrica"""
        if metric in self.alert_thresholds:
            self.alert_thresholds[metric] = value
            self.logger.info(f"Limiar de alerta para {metric} definido como {value}")
            return True
        return False
    
    def get_system_health_score(self):
        """Calcula pontuação de saúde do sistema (0-100)"""
        if not self.cpu_history or not self.memory_history:
            return None
        
        # Obter médias dos últimos 5 minutos
        current_time = time.time()
        recent_time = current_time - 300  # 5 minutos
        
        recent_cpu = [v for t, v in self.cpu_history if t >= recent_time]
        recent_memory = [v for t, v in self.memory_history if t >= recent_time]
        recent_disk = [v for t, v in self.disk_history if t >= recent_time]
        
        if not recent_cpu:
            return None
        
        # Calcular pontuações (0-100, onde 100 é melhor)
        cpu_score = max(0, 100 - (sum(recent_cpu) / len(recent_cpu)))
        memory_score = max(0, 100 - (sum(recent_memory) / len(recent_memory)))
        disk_score = max(0, 100 - (sum(recent_disk) / len(recent_disk))) if recent_disk else 100
        
        # Penalizar por alertas recentes
        alert_penalty = min(50, self.session_stats['alerts_triggered'] * 5)
        
        # Pontuação final (média ponderada)
        health_score = (cpu_score * 0.4 + memory_score * 0.4 + disk_score * 0.2) - alert_penalty
        
        return max(0, min(100, health_score))
    
    def is_monitoring(self):
        """Verifica se está monitorando"""
        return self.monitoring