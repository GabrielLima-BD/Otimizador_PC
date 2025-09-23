import os
import json
import logging
import time
from datetime import datetime
import ctypes
import sys

class Utils:
    """Classe com funções auxiliares para o otimizador"""
    
    @staticmethod
    def setup_logging():
        """Configura o sistema de logs"""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'optimizer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    @staticmethod
    def is_admin():
        """Verifica se o programa está sendo executado como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def run_as_admin():
        """Executa o programa como administrador"""
        if Utils.is_admin():
            return True
        else:
            try:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                return True
            except:
                return False
    
    @staticmethod
    def create_backup(data, backup_type):
        """Cria backup das configurações"""
        backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f'{backup_type}_backup_{timestamp}.json')
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return backup_file
        except Exception as e:
            logging.error(f"Erro ao criar backup: {e}")
            return None
    
    @staticmethod
    def load_backup(backup_file):
        """Carrega backup das configurações"""
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar backup: {e}")
            return None
    
    @staticmethod
    def format_size(bytes_size):
        """Formata tamanho em bytes para formato legível"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    @staticmethod
    def get_system_info():
        """Obtém informações básicas do sistema"""
        import platform
        import psutil
        
        info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'memory': Utils.format_size(psutil.virtual_memory().total),
            'disk_usage': {}
        }
        
        # Informações de disco
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info['disk_usage'][partition.device] = {
                    'total': Utils.format_size(usage.total),
                    'used': Utils.format_size(usage.used),
                    'free': Utils.format_size(usage.free),
                    'percent': round(usage.used / usage.total * 100, 2)
                }
            except:
                continue
        
        return info
    
    @staticmethod
    def safe_execute(func, *args, **kwargs):
        """Executa função de forma segura com tratamento de erro"""
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            logging.error(f"Erro ao executar {func.__name__}: {e}")
            return False, str(e)
    
    @staticmethod
    def get_temp_dirs():
        """Retorna lista de diretórios temporários do Windows"""
        temp_dirs = []
        
        # Diretórios temporários comuns
        possible_temps = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
            os.path.join(os.environ.get('APPDATA', ''), 'Local', 'Temp'),
        ]
        
        for temp_dir in possible_temps:
            if temp_dir and os.path.exists(temp_dir):
                temp_dirs.append(temp_dir)
        
        return list(set(temp_dirs))  # Remove duplicatas