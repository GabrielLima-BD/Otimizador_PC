"""
🚀 Optimizer Package - Versão Avançada

Pacote completo de otimização para Windows com recursos avançados:

MÓDULOS BÁSICOS:
- SystemCleaner: Limpeza básica do sistema
- PerformanceOptimizer: Otimizações de performance
- NetworkOptimizer: Otimização de rede
- RegistryOptimizer: Limpeza do registro
- Utils: Utilitários gerais

MÓDULOS AVANÇADOS:
- HardwareDetector: Detecção automática de hardware
- AdvancedCleaner: Limpeza profunda e duplicatas
- AdvancedOptimizer: Otimizações avançadas do sistema
- SystemMonitor: Monitoramento em tempo real
- ScheduleManager: Agendamento inteligente de tarefas

Autor: Gabriel
Versão: 2.0.0 (Avançada)
"""

# Módulos básicos
from .cleaner import SystemCleaner
from .performance import PerformanceOptimizer
from .network import NetworkOptimizer
from .registry import RegistryOptimizer
from .utils import Utils

# Módulos avançados
try:
    from .hardware_detector import HardwareDetector
    HARDWARE_DETECTION_AVAILABLE = True
except ImportError:
    HARDWARE_DETECTION_AVAILABLE = False

try:
    from .advanced_cleaner import AdvancedCleaner
    ADVANCED_CLEANING_AVAILABLE = True
except ImportError:
    ADVANCED_CLEANING_AVAILABLE = False

try:
    from .advanced_optimizer import AdvancedOptimizer
    ADVANCED_OPTIMIZATION_AVAILABLE = True
except ImportError:
    ADVANCED_OPTIMIZATION_AVAILABLE = False

try:
    from .system_monitor import SystemMonitor
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False

try:
    from .schedule_manager import ScheduleManager, ScheduleType
    SCHEDULING_AVAILABLE = True
except ImportError:
    SCHEDULING_AVAILABLE = False

# Lista de todos os componentes disponíveis
__all__ = [
    # Básicos
    'SystemCleaner',
    'PerformanceOptimizer', 
    'NetworkOptimizer',
    'RegistryOptimizer',
    'Utils',
    
    # Avançados (condicionais)
]

# Adicionar módulos avançados se disponíveis
if HARDWARE_DETECTION_AVAILABLE:
    __all__.append('HardwareDetector')

if ADVANCED_CLEANING_AVAILABLE:
    __all__.append('AdvancedCleaner')

if ADVANCED_OPTIMIZATION_AVAILABLE:
    __all__.append('AdvancedOptimizer')

if MONITORING_AVAILABLE:
    __all__.append('SystemMonitor')

if SCHEDULING_AVAILABLE:
    __all__.extend(['ScheduleManager', 'ScheduleType'])

# Informações de versão e funcionalidades
__version__ = "2.0.0"
__author__ = "Gabriel"

FEATURES = {
    'basic_cleaning': True,
    'basic_optimization': True,
    'network_optimization': True,
    'registry_optimization': True,
    'hardware_detection': HARDWARE_DETECTION_AVAILABLE,
    'advanced_cleaning': ADVANCED_CLEANING_AVAILABLE,
    'advanced_optimization': ADVANCED_OPTIMIZATION_AVAILABLE,
    'system_monitoring': MONITORING_AVAILABLE,
    'task_scheduling': SCHEDULING_AVAILABLE
}

def get_available_features():
    """Retorna dicionário com funcionalidades disponíveis"""
    return FEATURES.copy()

def get_feature_status():
    """Retorna status textual das funcionalidades"""
    status = []
    
    # Básicas (sempre disponíveis)
    status.append("✅ Limpeza Básica")
    status.append("✅ Otimização de Performance")
    status.append("✅ Otimização de Rede")
    status.append("✅ Otimização do Registro")
    
    # Avançadas (condicionais)
    status.append("✅ Detecção de Hardware" if HARDWARE_DETECTION_AVAILABLE else "❌ Detecção de Hardware")
    status.append("✅ Limpeza Avançada" if ADVANCED_CLEANING_AVAILABLE else "❌ Limpeza Avançada")
    status.append("✅ Otimização Avançada" if ADVANCED_OPTIMIZATION_AVAILABLE else "❌ Otimização Avançada")
    status.append("✅ Monitoramento" if MONITORING_AVAILABLE else "❌ Monitoramento")
    status.append("✅ Agendamento" if SCHEDULING_AVAILABLE else "❌ Agendamento")
    
    return status