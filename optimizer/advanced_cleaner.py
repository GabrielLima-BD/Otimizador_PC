import os
import shutil
import subprocess
import hashlib
import logging
import winreg
from collections import defaultdict
from pathlib import Path
from .utils import Utils

class AdvancedCleaner:
    """Limpeza profunda e avançada do sistema"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.duplicate_files = []
        self.cleaned_size = 0
        self.cleaned_files = 0
        
    def find_duplicate_files(self, directories=None, progress_callback=None):
        """Encontra arquivos duplicados baseado em hash MD5"""
        if directories is None:
            directories = [
                os.path.expanduser("~/Downloads"),
                os.path.expanduser("~/Documents"),
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/Pictures"),
                os.path.expanduser("~/Videos"),
                os.path.expanduser("~/Music")
            ]
        
        if progress_callback:
            progress_callback("Analisando arquivos para duplicatas...", 0)
        
        file_hashes = defaultdict(list)
        total_files = 0
        processed_files = 0
        
        # Primeira passagem: contar arquivos
        for directory in directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    total_files += len(files)
        
        # Segunda passagem: calcular hashes
        for directory in directories:
            if not os.path.exists(directory):
                continue
                
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    processed_files += 1
                    
                    if progress_callback:
                        progress = (processed_files / total_files) * 100 if total_files > 0 else 0
                        progress_callback(f"Analisando: {file}", progress)
                    
                    try:
                        # Ignora arquivos muito pequenos ou muito grandes
                        file_size = os.path.getsize(file_path)
                        if file_size < 1024 or file_size > 500 * 1024 * 1024:  # < 1KB ou > 500MB
                            continue
                        
                        file_hash = self._calculate_file_hash(file_path)
                        if file_hash:
                            file_hashes[file_hash].append({
                                'path': file_path,
                                'size': file_size,
                                'modified': os.path.getmtime(file_path)
                            })
                    except (PermissionError, FileNotFoundError, OSError):
                        continue
        
        # Encontra duplicatas
        duplicates = []
        for file_hash, file_list in file_hashes.items():
            if len(file_list) > 1:
                # Ordena por data de modificação (mantém o mais antigo)
                file_list.sort(key=lambda x: x['modified'])
                duplicates.append({
                    'hash': file_hash,
                    'files': file_list,
                    'original': file_list[0],
                    'duplicates': file_list[1:],
                    'total_size': sum(f['size'] for f in file_list[1:])
                })
        
        self.duplicate_files = duplicates
        
        if progress_callback:
            progress_callback("Análise de duplicatas concluída", 100)
        
        return duplicates
    
    def remove_duplicate_files(self, duplicates_to_remove=None, progress_callback=None):
        """Remove arquivos duplicados selecionados"""
        if duplicates_to_remove is None:
            duplicates_to_remove = self.duplicate_files
        
        removed_count = 0
        removed_size = 0
        
        total_duplicates = sum(len(dup['duplicates']) for dup in duplicates_to_remove)
        processed_duplicates = 0
        
        for duplicate_group in duplicates_to_remove:
            for duplicate_file in duplicate_group['duplicates']:
                processed_duplicates += 1
                
                if progress_callback:
                    progress = (processed_duplicates / total_duplicates) * 100 if total_duplicates > 0 else 0
                    progress_callback(f"Removendo: {os.path.basename(duplicate_file['path'])}", progress)
                
                try:
                    os.remove(duplicate_file['path'])
                    removed_count += 1
                    removed_size += duplicate_file['size']
                    self.logger.info(f"Arquivo duplicado removido: {duplicate_file['path']}")
                except (PermissionError, FileNotFoundError, OSError) as e:
                    self.logger.warning(f"Não foi possível remover {duplicate_file['path']}: {e}")
        
        if progress_callback:
            progress_callback("Remoção de duplicatas concluída", 100)
        
        return {
            'removed_count': removed_count,
            'removed_size': removed_size,
            'removed_size_formatted': Utils.format_size(removed_size)
        }
    
    def clean_old_drivers(self, progress_callback=None):
        """Remove drivers antigos e não utilizados"""
        if progress_callback:
            progress_callback("Limpando drivers antigos...", 0)
        
        try:
            # Limpa cache de drivers
            driver_store = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'DriverStore', 'FileRepository')
            
            if os.path.exists(driver_store):
                # Usa DISM para limpeza de drivers
                cmd = 'dism /online /cleanup-image /analyzecomponentstore'
                subprocess.run(cmd, shell=True, capture_output=True, timeout=300)
                
                if progress_callback:
                    progress_callback("Analisando drivers...", 50)
                
                # Limpa drivers antigos
                cmd = 'dism /online /cleanup-image /startcomponentcleanup /resetbase'
                result = subprocess.run(cmd, shell=True, capture_output=True, timeout=600)
                
                if progress_callback:
                    progress_callback("Limpeza de drivers concluída", 100)
                
                return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Limpeza de drivers excedeu tempo limite")
        except Exception as e:
            self.logger.error(f"Erro na limpeza de drivers: {e}")
        
        return False
    
    def clean_windows_event_logs(self, progress_callback=None):
        """Limpa logs de eventos do Windows"""
        if progress_callback:
            progress_callback("Limpando logs de eventos...", 0)
        
        # Lista de logs de eventos comuns
        event_logs = [
            'Application', 'System', 'Security', 'Setup', 'ForwardedEvents',
            'Microsoft-Windows-TaskScheduler/Operational',
            'Microsoft-Windows-PowerShell/Operational',
            'Microsoft-Windows-Windows Defender/Operational',
            'Microsoft-Windows-WindowsUpdateClient/Operational'
        ]
        
        cleared_logs = 0
        
        for i, log_name in enumerate(event_logs):
            if progress_callback:
                progress = (i / len(event_logs)) * 100
                progress_callback(f"Limpando log: {log_name}", progress)
            
            try:
                cmd = f'wevtutil cl "{log_name}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                
                if result.returncode == 0:
                    cleared_logs += 1
                    self.logger.info(f"Log limpo: {log_name}")
                else:
                    self.logger.warning(f"Não foi possível limpar log: {log_name}")
                    
            except subprocess.TimeoutExpired:
                self.logger.warning(f"Timeout ao limpar log: {log_name}")
            except Exception as e:
                self.logger.error(f"Erro ao limpar log {log_name}: {e}")
        
        if progress_callback:
            progress_callback("Limpeza de logs concluída", 100)
        
        return cleared_logs
    
    def clean_old_restore_points(self, keep_newest=2, progress_callback=None):
        """Remove pontos de restauração antigos, mantendo os mais recentes"""
        if progress_callback:
            progress_callback("Limpando pontos de restauração antigos...", 0)
        
        try:
            # Lista pontos de restauração
            cmd = 'powershell -Command "Get-ComputerRestorePoint | Sort-Object CreationTime"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split('\n')
                
                # Filtra linhas válidas (ignora cabeçalhos)
                restore_points = []
                for line in lines:
                    if line and not line.startswith('SequenceNumber') and not line.startswith('---'):
                        parts = line.split()
                        if parts and parts[0].isdigit():
                            restore_points.append(int(parts[0]))
                
                # Remove pontos antigos (mantém os mais recentes)
                points_to_remove = []
                if len(restore_points) > keep_newest:
                    points_to_remove = restore_points[:-keep_newest]
                    
                    for i, sequence_number in enumerate(points_to_remove):
                        if progress_callback:
                            progress = (i / len(points_to_remove)) * 100
                            progress_callback(f"Removendo ponto de restauração {sequence_number}", progress)
                        
                        try:
                            cmd = f'powershell -Command "Remove-ComputerRestorePoint -RestorePoint {sequence_number}"'
                            subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
                            self.logger.info(f"Ponto de restauração removido: {sequence_number}")
                        except:
                            continue
                
                if progress_callback:
                    progress_callback("Limpeza de pontos de restauração concluída", 100)
                
                return len(points_to_remove)
            
        except Exception as e:
            self.logger.error(f"Erro na limpeza de pontos de restauração: {e}")
        
        return 0
    
    def clean_browser_profiles_deep(self, progress_callback=None):
        """Limpeza profunda de perfis de navegadores"""
        if progress_callback:
            progress_callback("Limpeza profunda de navegadores...", 0)
        
        browsers = {
            'Chrome': {
                'profile_path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
                'cache_folders': ['Default/Cache', 'Default/Code Cache', 'Default/GPUCache', 'ShaderCache'],
                'data_folders': ['Default/Local Storage', 'Default/Session Storage', 'Default/IndexedDB']
            },
            'Edge': {
                'profile_path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data'),
                'cache_folders': ['Default/Cache', 'Default/Code Cache', 'Default/GPUCache', 'ShaderCache'],
                'data_folders': ['Default/Local Storage', 'Default/Session Storage', 'Default/IndexedDB']
            },
            'Firefox': {
                'profile_path': os.path.join(os.environ.get('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles'),
                'cache_folders': ['cache2', 'startupCache', 'OfflineCache'],
                'data_folders': ['storage', 'webappsstore.sqlite']
            }
        }
        
        cleaned_browsers = 0
        
        for i, (browser_name, browser_info) in enumerate(browsers.items()):
            if progress_callback:
                progress = (i / len(browsers)) * 100
                progress_callback(f"Limpando {browser_name}...", progress)
            
            if os.path.exists(browser_info['profile_path']):
                try:
                    # Limpa cache folders
                    for cache_folder in browser_info['cache_folders']:
                        cache_path = os.path.join(browser_info['profile_path'], cache_folder)
                        if os.path.exists(cache_path):
                            shutil.rmtree(cache_path, ignore_errors=True)
                    
                    # Limpa dados opcionais (mais cuidadoso)
                    for data_folder in browser_info['data_folders']:
                        data_path = os.path.join(browser_info['profile_path'], data_folder)
                        if os.path.exists(data_path):
                            if os.path.isdir(data_path):
                                shutil.rmtree(data_path, ignore_errors=True)
                            else:
                                try:
                                    os.remove(data_path)
                                except:
                                    pass
                    
                    cleaned_browsers += 1
                    self.logger.info(f"Limpeza profunda do {browser_name} concluída")
                    
                except Exception as e:
                    self.logger.error(f"Erro na limpeza profunda do {browser_name}: {e}")
        
        if progress_callback:
            progress_callback("Limpeza profunda de navegadores concluída", 100)
        
        return cleaned_browsers
    
    def clean_thumbnail_cache(self, progress_callback=None):
        """Remove cache de thumbnails do Windows"""
        if progress_callback:
            progress_callback("Limpando cache de thumbnails...", 0)
        
        thumbnail_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Explorer'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'IconCache.db'),
        ]
        
        cleaned_files = 0
        
        for i, thumbnail_path in enumerate(thumbnail_paths):
            if progress_callback:
                progress = (i / len(thumbnail_paths)) * 100
                progress_callback(f"Limpando thumbnails...", progress)
            
            if os.path.exists(thumbnail_path):
                try:
                    if os.path.isfile(thumbnail_path):
                        os.remove(thumbnail_path)
                        cleaned_files += 1
                    elif os.path.isdir(thumbnail_path):
                        for file in os.listdir(thumbnail_path):
                            if file.endswith('.db'):
                                file_path = os.path.join(thumbnail_path, file)
                                try:
                                    os.remove(file_path)
                                    cleaned_files += 1
                                except:
                                    continue
                except Exception as e:
                    self.logger.error(f"Erro ao limpar thumbnails em {thumbnail_path}: {e}")
        
        if progress_callback:
            progress_callback("Cache de thumbnails limpo", 100)
        
        return cleaned_files
    
    def _calculate_file_hash(self, file_path):
        """Calcula hash MD5 de um arquivo"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def get_advanced_cleanup_summary(self):
        """Retorna resumo da limpeza avançada"""
        return {
            'duplicate_files_found': len(self.duplicate_files),
            'duplicate_space_savings': sum(dup['total_size'] for dup in self.duplicate_files),
            'duplicate_space_formatted': Utils.format_size(sum(dup['total_size'] for dup in self.duplicate_files)),
            'total_cleaned_files': self.cleaned_files,
            'total_cleaned_size': self.cleaned_size,
            'total_cleaned_formatted': Utils.format_size(self.cleaned_size)
        }