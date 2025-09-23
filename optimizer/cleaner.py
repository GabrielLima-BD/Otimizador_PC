import os
import shutil
import subprocess
import logging
import tempfile
from .utils import Utils

class SystemCleaner:
    """Classe responsável pela limpeza do sistema"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cleaned_size = 0
        self.cleaned_files = 0
        
        # Apps bloatware comuns do Windows 10
        self.bloatware_apps = [
            "Microsoft.3DBuilder",
            "Microsoft.AppConnector",
            "Microsoft.BingFinance",
            "Microsoft.BingNews",
            "Microsoft.BingSports",
            "Microsoft.BingWeather",
            "Microsoft.Getstarted",
            "Microsoft.MicrosoftOfficeHub",
            "Microsoft.MicrosoftSolitaireCollection",
            "Microsoft.People",
            "Microsoft.SkypeApp",
            "Microsoft.WindowsAlarms",
            "Microsoft.WindowsCamera",
            "Microsoft.WindowsMaps",
            "Microsoft.WindowsPhone",
            "Microsoft.WindowsSoundRecorder",
            "Microsoft.XboxApp",
            "Microsoft.ZuneMusic",
            "Microsoft.ZuneVideo",
            "Microsoft.OneConnect",
            "Microsoft.ConnectivityStore",
            "Microsoft.Microsoft3DViewer",
            "Microsoft.Print3D",
            "Microsoft.MixedReality.Portal"
        ]
    
    def clean_temp_files(self, progress_callback=None):
        """Limpa arquivos temporários do sistema"""
        self.logger.info("Iniciando limpeza de arquivos temporários...")
        
        temp_dirs = Utils.get_temp_dirs()
        total_dirs = len(temp_dirs)
        
        for i, temp_dir in enumerate(temp_dirs):
            if progress_callback:
                progress_callback(f"Limpando: {temp_dir}", (i / total_dirs) * 100)
            
            try:
                self._clean_directory(temp_dir)
            except Exception as e:
                self.logger.error(f"Erro ao limpar {temp_dir}: {e}")
        
        self.logger.info(f"Limpeza concluída. {self.cleaned_files} arquivos removidos, {Utils.format_size(self.cleaned_size)} liberados")
        return self.cleaned_files, self.cleaned_size
    
    def _clean_directory(self, directory):
        """Limpa um diretório específico"""
        if not os.path.exists(directory):
            return
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    self.cleaned_size += file_size
                    self.cleaned_files += 1
                except (PermissionError, FileNotFoundError, OSError):
                    continue
            
            # Remove diretórios vazios
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                except (PermissionError, OSError):
                    continue
    
    def clean_recycle_bin(self, progress_callback=None):
        """Esvazia a lixeira"""
        if progress_callback:
            progress_callback("Esvaziando lixeira...", 0)
        
        try:
            import ctypes
            from ctypes import wintypes
            
            # Função da API do Windows para esvaziar lixeira
            SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
            SHEmptyRecycleBin.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.DWORD]
            SHEmptyRecycleBin.restype = wintypes.LONG
            
            # Flags: SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
            result = SHEmptyRecycleBin(None, None, 0x00000001 | 0x00000002 | 0x00000004)
            
            if result == 0:
                self.logger.info("Lixeira esvaziada com sucesso")
                if progress_callback:
                    progress_callback("Lixeira esvaziada", 100)
                return True
            else:
                self.logger.warning("Falha ao esvaziar lixeira")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao esvaziar lixeira: {e}")
            return False
    
    def clean_browser_data(self, progress_callback=None):
        """Limpa dados dos navegadores"""
        if progress_callback:
            progress_callback("Limpando dados dos navegadores...", 0)
        
        browser_paths = {
            'Chrome': [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
            ],
            'Edge': [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
            ],
            'Firefox': [
                os.path.join(os.environ.get('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles'),
            ]
        }
        
        total_browsers = len(browser_paths)
        for i, (browser, paths) in enumerate(browser_paths.items()):
            if progress_callback:
                progress_callback(f"Limpando {browser}...", (i / total_browsers) * 100)
            
            for path in paths:
                if os.path.exists(path):
                    try:
                        if 'Profiles' in path:  # Firefox
                            self._clean_firefox_profiles(path)
                        else:
                            self._clean_directory(path)
                        self.logger.info(f"Cache do {browser} limpo")
                    except Exception as e:
                        self.logger.error(f"Erro ao limpar {browser}: {e}")
    
    def _clean_firefox_profiles(self, profiles_path):
        """Limpa profiles do Firefox"""
        if not os.path.exists(profiles_path):
            return
        
        for profile_dir in os.listdir(profiles_path):
            profile_path = os.path.join(profiles_path, profile_dir)
            if os.path.isdir(profile_path):
                cache_path = os.path.join(profile_path, 'cache2')
                if os.path.exists(cache_path):
                    self._clean_directory(cache_path)
    
    def remove_bloatware(self, progress_callback=None):
        """Remove aplicativos bloatware do Windows"""
        if progress_callback:
            progress_callback("Removendo aplicativos desnecessários...", 0)
        
        removed_apps = []
        total_apps = len(self.bloatware_apps)
        
        for i, app in enumerate(self.bloatware_apps):
            if progress_callback:
                progress_callback(f"Verificando {app}...", (i / total_apps) * 100)
            
            success, result = self._remove_app_package(app)
            if success:
                removed_apps.append(app)
                self.logger.info(f"App removido: {app}")
        
        self.logger.info(f"Remoção de bloatware concluída. {len(removed_apps)} apps removidos")
        return removed_apps
    
    def _remove_app_package(self, package_name):
        """Remove um pacote de aplicativo específico"""
        try:
            # Comando PowerShell para remover app
            cmd = f'Get-AppxPackage "{package_name}" | Remove-AppxPackage'
            
            result = subprocess.run(
                ['powershell', '-Command', cmd],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0, result.stdout
            
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)
    
    def clean_windows_logs(self, progress_callback=None):
        """Limpa logs do Windows"""
        if progress_callback:
            progress_callback("Limpando logs do Windows...", 0)
        
        log_paths = [
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Logs'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'LogFiles'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp'),
        ]
        
        total_paths = len(log_paths)
        for i, log_path in enumerate(log_paths):
            if progress_callback:
                progress_callback(f"Limpando {log_path}...", (i / total_paths) * 100)
            
            if os.path.exists(log_path):
                try:
                    self._clean_directory(log_path)
                except Exception as e:
                    self.logger.error(f"Erro ao limpar logs em {log_path}: {e}")
    
    def run_disk_cleanup(self, progress_callback=None):
        """Executa limpeza de disco do Windows"""
        if progress_callback:
            progress_callback("Executando limpeza de disco...", 0)
        
        try:
            # Executa cleanmgr com configurações automáticas
            subprocess.run([
                'cleanmgr', '/sagerun:1'
            ], timeout=300)
            
            if progress_callback:
                progress_callback("Limpeza de disco concluída", 100)
            
            self.logger.info("Limpeza de disco executada com sucesso")
            return True
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Limpeza de disco excedeu tempo limite")
            return False
        except Exception as e:
            self.logger.error(f"Erro na limpeza de disco: {e}")
            return False
    
    def get_cleanup_summary(self):
        """Retorna resumo da limpeza realizada"""
        return {
            'files_cleaned': self.cleaned_files,
            'space_freed': self.cleaned_size,
            'space_freed_formatted': Utils.format_size(self.cleaned_size)
        }