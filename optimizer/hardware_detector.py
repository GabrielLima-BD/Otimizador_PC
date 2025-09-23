import psutil
import subprocess
import winreg
import logging
import wmi
from .utils import Utils

class HardwareDetector:
    """Detecta hardware e cria perfis otimizados"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hardware_info = {}
        self.optimization_profile = None
        
    def detect_hardware(self):
        """Detecta informações completas de hardware"""
        try:
            self.hardware_info = {
                'cpu': self._detect_cpu(),
                'memory': self._detect_memory(),
                'storage': self._detect_storage(),
                'gpu': self._detect_gpu(),
                'system_type': self._detect_system_type()
            }
            
            # Determina perfil baseado no hardware
            self.optimization_profile = self._determine_optimization_profile()
            
            return self.hardware_info
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de hardware: {e}")
            return None
    
    def detect_system_hardware(self):
        """Alias para detect_hardware() para compatibilidade"""
        return self.detect_hardware()
    
    def classify_system_profile(self, hardware_info=None):
        """Classifica o perfil do sistema baseado no hardware"""
        if not hardware_info:
            hardware_info = self.hardware_info or self.detect_hardware()
        
        if not hardware_info:
            return 'basic'
        
        try:
            cpu = hardware_info.get('cpu', {})
            memory = hardware_info.get('memory', {})
            gpu = hardware_info.get('gpu', {})
            storage = hardware_info.get('storage', {})
            
            # Critérios para classificação
            is_gaming_cpu = cpu.get('is_gaming_cpu', False)
            has_dedicated_gpu = gpu.get('type') == 'Dedicated'
            high_memory = memory.get('total_gb', 0) >= 16
            has_ssd = any(drive.get('is_ssd', False) for drive in storage.get('drives', []))
            
            # Classificação
            if is_gaming_cpu and has_dedicated_gpu and high_memory:
                return 'gaming_high_end'
            elif (is_gaming_cpu or has_dedicated_gpu) and memory.get('total_gb', 0) >= 8:
                return 'gaming_mid_range'
            elif memory.get('total_gb', 0) >= 8 and has_ssd:
                return 'productivity'
            elif memory.get('total_gb', 0) >= 4:
                return 'balanced'
            else:
                return 'basic'
                
        except Exception as e:
            self.logger.error(f"Erro na classificação do perfil: {e}")
            return 'basic'
    
    def _detect_cpu(self):
        """Detecta informações da CPU"""
        try:
            c = wmi.WMI()
            cpu_info = c.Win32_Processor()[0]
            
            cpu_data = {
                'name': cpu_info.Name.strip(),
                'cores': cpu_info.NumberOfCores,
                'threads': cpu_info.NumberOfLogicalProcessors,
                'max_clock': cpu_info.MaxClockSpeed,
                'architecture': cpu_info.Architecture,
                'manufacturer': cpu_info.Manufacturer,
                'is_gaming_cpu': self._is_gaming_cpu(cpu_info.Name),
                'performance_level': self._get_cpu_performance_level(cpu_info)
            }
            
            return cpu_data
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de CPU: {e}")
            return {'name': 'Unknown', 'cores': psutil.cpu_count(logical=False)}
    
    def _detect_memory(self):
        """Detecta informações de memória"""
        try:
            memory = psutil.virtual_memory()
            
            # Detecta tipo de RAM (DDR3, DDR4, DDR5)
            ram_type = self._detect_ram_type()
            
            memory_data = {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_percent': memory.percent,
                'type': ram_type,
                'performance_level': self._get_memory_performance_level(memory.total)
            }
            
            return memory_data
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de memória: {e}")
            return {}
    
    def _detect_storage(self):
        """Detecta tipos de armazenamento"""
        try:
            c = wmi.WMI()
            drives = []
            
            for disk in c.Win32_DiskDrive():
                drive_info = {
                    'model': disk.Model,
                    'size_gb': round(int(disk.Size) / (1024**3), 2) if disk.Size else 0,
                    'interface': disk.InterfaceType,
                    'is_ssd': self._is_ssd(disk.Model),
                    'is_nvme': self._is_nvme(disk.Model, disk.InterfaceType)
                }
                drives.append(drive_info)
            
            # Determina drive principal
            primary_drive = drives[0] if drives else {}
            
            storage_data = {
                'drives': drives,
                'primary_drive': primary_drive,
                'has_ssd': any(drive['is_ssd'] for drive in drives),
                'has_nvme': any(drive['is_nvme'] for drive in drives),
                'performance_level': self._get_storage_performance_level(drives)
            }
            
            return storage_data
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de armazenamento: {e}")
            return {}
    
    def _detect_gpu(self):
        """Detecta informações da GPU"""
        try:
            c = wmi.WMI()
            gpu_info = []
            
            for gpu in c.Win32_VideoController():
                if gpu.Name and 'Microsoft' not in gpu.Name:
                    gpu_data = {
                        'name': gpu.Name,
                        'driver_version': gpu.DriverVersion,
                        'memory_mb': gpu.AdapterRAM // (1024*1024) if gpu.AdapterRAM else 0,
                        'is_dedicated': self._is_dedicated_gpu(gpu.Name),
                        'is_gaming_gpu': self._is_gaming_gpu(gpu.Name),
                        'performance_level': self._get_gpu_performance_level(gpu.Name)
                    }
                    gpu_info.append(gpu_data)
            
            return {
                'gpus': gpu_info,
                'has_dedicated_gpu': any(gpu['is_dedicated'] for gpu in gpu_info),
                'is_gaming_system': any(gpu['is_gaming_gpu'] for gpu in gpu_info)
            }
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de GPU: {e}")
            return {}
    
    def _detect_system_type(self):
        """Detecta tipo de sistema (Desktop, Laptop, etc.)"""
        try:
            c = wmi.WMI()
            system = c.Win32_SystemEnclosure()[0]
            
            chassis_types = {
                3: 'Desktop', 4: 'Desktop', 5: 'Desktop', 6: 'Desktop', 7: 'Desktop',
                8: 'Laptop', 9: 'Laptop', 10: 'Laptop', 11: 'Laptop', 12: 'Laptop',
                13: 'All-in-One', 14: 'Laptop', 15: 'Desktop', 16: 'Desktop',
                17: 'Server', 18: 'Laptop', 19: 'Laptop', 20: 'Laptop', 21: 'Laptop'
            }
            
            chassis_type = int(system.ChassisTypes[0]) if system.ChassisTypes else 3
            system_type = chassis_types.get(chassis_type, 'Desktop')
            
            return {
                'type': system_type,
                'is_laptop': system_type in ['Laptop'],
                'is_desktop': system_type in ['Desktop'],
                'manufacturer': system.Manufacturer,
                'model': system.Model
            }
            
        except Exception as e:
            self.logger.error(f"Erro na detecção do tipo de sistema: {e}")
            return {'type': 'Desktop', 'is_laptop': False, 'is_desktop': True}
    
    def _determine_optimization_profile(self):
        """Determina perfil de otimização baseado no hardware"""
        profile = {
            'name': 'Balanced',
            'priority': 'balanced',
            'optimizations': []
        }
        
        try:
            # Análise baseada em GPU
            if self.hardware_info.get('gpu', {}).get('is_gaming_system'):
                profile['name'] = 'Gaming'
                profile['priority'] = 'performance'
                profile['optimizations'].extend([
                    'disable_game_dvr',
                    'optimize_gpu_scheduling',
                    'disable_fullscreen_optimizations',
                    'high_performance_power_plan'
                ])
            
            # Análise baseada em CPU
            cpu_info = self.hardware_info.get('cpu', {})
            if cpu_info.get('is_gaming_cpu') or cpu_info.get('performance_level') == 'high':
                profile['optimizations'].extend([
                    'disable_cpu_parking',
                    'optimize_processor_scheduling',
                    'disable_power_throttling'
                ])
            
            # Análise baseada em armazenamento
            storage_info = self.hardware_info.get('storage', {})
            if storage_info.get('has_ssd'):
                profile['optimizations'].extend([
                    'disable_defragmentation',
                    'enable_trim',
                    'disable_superfetch'
                ])
            else:
                profile['optimizations'].extend([
                    'enable_defragmentation',
                    'optimize_hdd_performance'
                ])
            
            # Análise baseada em memória
            memory_info = self.hardware_info.get('memory', {})
            if memory_info.get('total_gb', 0) >= 16:
                profile['optimizations'].extend([
                    'disable_paging_executive',
                    'increase_system_cache'
                ])
            elif memory_info.get('total_gb', 0) <= 8:
                profile['optimizations'].extend([
                    'optimize_virtual_memory',
                    'reduce_visual_effects'
                ])
            
            # Análise baseada no tipo de sistema
            system_info = self.hardware_info.get('system_type', {})
            if system_info.get('is_laptop'):
                profile['optimizations'].extend([
                    'optimize_battery_settings',
                    'disable_fast_startup'
                ])
            
            return profile
            
        except Exception as e:
            self.logger.error(f"Erro ao determinar perfil: {e}")
            return profile
    
    # Métodos auxiliares de detecção
    def _is_gaming_cpu(self, cpu_name):
        """Verifica se é CPU gamer"""
        gaming_keywords = ['ryzen 7', 'ryzen 9', 'i7', 'i9', 'fx-', 'threadripper']
        return any(keyword in cpu_name.lower() for keyword in gaming_keywords)
    
    def _get_cpu_performance_level(self, cpu_info):
        """Determina nível de performance da CPU"""
        if cpu_info.NumberOfCores >= 8 and cpu_info.MaxClockSpeed >= 3500:
            return 'high'
        elif cpu_info.NumberOfCores >= 4 and cpu_info.MaxClockSpeed >= 2500:
            return 'medium'
        else:
            return 'low'
    
    def _detect_ram_type(self):
        """Detecta tipo de RAM"""
        try:
            c = wmi.WMI()
            for memory in c.Win32_PhysicalMemory():
                if memory.SMBIOSMemoryType:
                    memory_types = {
                        20: 'DDR', 21: 'DDR2', 24: 'DDR3', 26: 'DDR4', 34: 'DDR5'
                    }
                    return memory_types.get(memory.SMBIOSMemoryType, 'Unknown')
            return 'Unknown'
        except:
            return 'Unknown'
    
    def _get_memory_performance_level(self, total_memory):
        """Determina nível de performance da memória"""
        total_gb = total_memory / (1024**3)
        if total_gb >= 32:
            return 'high'
        elif total_gb >= 16:
            return 'medium'
        else:
            return 'low'
    
    def _is_ssd(self, model):
        """Verifica se é SSD"""
        ssd_keywords = ['ssd', 'solid', 'nvme', 'pcie', 'samsung', 'crucial', 'kingston']
        return any(keyword in model.lower() for keyword in ssd_keywords)
    
    def _is_nvme(self, model, interface):
        """Verifica se é NVMe"""
        return 'nvme' in model.lower() or (interface and 'pcie' in interface.lower())
    
    def _get_storage_performance_level(self, drives):
        """Determina nível de performance do armazenamento"""
        if any(drive['is_nvme'] for drive in drives):
            return 'high'
        elif any(drive['is_ssd'] for drive in drives):
            return 'medium'
        else:
            return 'low'
    
    def _is_dedicated_gpu(self, gpu_name):
        """Verifica se é GPU dedicada"""
        integrated_keywords = ['intel', 'vega', 'radeon graphics']
        return not any(keyword in gpu_name.lower() for keyword in integrated_keywords)
    
    def _is_gaming_gpu(self, gpu_name):
        """Verifica se é GPU para jogos"""
        gaming_keywords = ['rtx', 'gtx', 'rx ', 'radeon rx', 'geforce']
        return any(keyword in gpu_name.lower() for keyword in gaming_keywords)
    
    def _get_gpu_performance_level(self, gpu_name):
        """Determina nível de performance da GPU"""
        high_end = ['rtx 40', 'rtx 30', 'rx 7', 'rx 6']
        medium_end = ['rtx 20', 'gtx 16', 'rx 5', 'rx 580']
        
        gpu_lower = gpu_name.lower()
        if any(keyword in gpu_lower for keyword in high_end):
            return 'high'
        elif any(keyword in gpu_lower for keyword in medium_end):
            return 'medium'
        else:
            return 'low'
    
    def get_recommended_optimizations(self):
        """Retorna otimizações recomendadas baseadas no hardware"""
        if not self.optimization_profile:
            return []
        
        return {
            'profile_name': self.optimization_profile['name'],
            'priority': self.optimization_profile['priority'],
            'optimizations': self.optimization_profile['optimizations'],
            'hardware_summary': {
                'cpu_level': self.hardware_info.get('cpu', {}).get('performance_level', 'unknown'),
                'memory_level': self.hardware_info.get('memory', {}).get('performance_level', 'unknown'),
                'storage_level': self.hardware_info.get('storage', {}).get('performance_level', 'unknown'),
                'gpu_level': self.hardware_info.get('gpu', {}).get('gpus', [{}])[0].get('performance_level', 'unknown') if self.hardware_info.get('gpu', {}).get('gpus') else 'unknown',
                'system_type': self.hardware_info.get('system_type', {}).get('type', 'unknown')
            }
        }