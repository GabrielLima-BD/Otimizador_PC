"""
Sistema Universal de Busca de Aplicativos
Encontra TODOS os apps instalados no PC (como menu iniciar)
VERSÃO ULTRA: Filtros inteligentes, sem duplicatas, seleção melhorada
"""

import os
import winreg
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Callable, Set
from dataclasses import dataclass
import threading
import time
import re

@dataclass
class AppInfo:
    """Informações de um aplicativo"""
    name: str
    executable_path: str
    icon_path: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    publisher: Optional[str] = None
    install_directory: Optional[str] = None
    app_type: str = "application"  # application, game, system, etc
    is_uwp: bool = False  # Universal Windows Platform app
    priority: int = 0  # Para ordenação (apps mais importantes primeiro)
    is_selectable: bool = True  # Se o app pode ser selecionado
    
    @property
    def app_id(self) -> str:
        """ID único do app baseado no executável normalizado"""
        normalized_path = os.path.normpath(self.executable_path.lower())
        return f"{self.name.lower().strip()}_{hash(normalized_path)}"
    
    @property 
    def display_name(self) -> str:
        """Nome limpo para exibição"""
        # Remove versões, parênteses e caracteres especiais
        clean_name = re.sub(r'\s*\([^)]*\)', '', self.name)
        clean_name = re.sub(r'\s*v?\d+\.\d+.*', '', clean_name)
        return clean_name.strip()

class UniversalAppScanner:
    """Scanner universal de aplicativos do sistema com filtros inteligentes"""
    
    def __init__(self):
        self.apps_cache: Dict[str, AppInfo] = {}
        self.search_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            r"C:\Users\{}\AppData\Local\Programs".format(os.getenv('USERNAME')),
            r"C:\Users\{}\AppData\Roaming".format(os.getenv('USERNAME')),
        ]
        
        # Filtros para evitar duplicatas e apps não selecionáveis
        self.excluded_names = {
            'uninstall', 'setup', 'installer', 'updater', 'launcher',
            'microsoft visual c++', 'microsoft .net', 'redistributable',
            'runtime', 'framework', 'update for', 'security update',
            'hotfix', 'kb', 'service pack', 'driver', 'directx'
        }
        
        self.system_publishers = {
            'microsoft corporation', 'intel corporation', 'nvidia corporation',
            'amd', 'realtek', 'adobe systems incorporated'
        }
        
        self.gaming_keywords = {
            'game', 'gaming', 'steam', 'epic', 'ubisoft', 'origin', 'gog',
            'blizzard', 'riot', 'valve', 'electronic arts', 'activision'
        }
    
    def _is_duplicate(self, new_app: AppInfo, existing_apps: Dict[str, AppInfo]) -> bool:
        """Verifica se o app é duplicata de um já existente"""
        new_name_clean = new_app.display_name.lower().strip()
        new_path_clean = os.path.normpath(new_app.executable_path.lower())
        
        for existing_app in existing_apps.values():
            existing_name_clean = existing_app.display_name.lower().strip()
            existing_path_clean = os.path.normpath(existing_app.executable_path.lower())
            
            # Mesmo nome e caminho similar
            if new_name_clean == existing_name_clean:
                if os.path.dirname(new_path_clean) == os.path.dirname(existing_path_clean):
                    return True
            
            # Mesmo executável
            if new_path_clean == existing_path_clean:
                return True
        
        return False
    
    def _calculate_priority(self, app: AppInfo) -> int:
        """Calcula prioridade do app (maior = mais importante)"""
        priority = 50  # Base
        
        # Gaming apps têm prioridade alta
        name_lower = app.name.lower()
        if any(keyword in name_lower for keyword in self.gaming_keywords):
            priority += 30
        
        # Apps populares
        popular_apps = ['chrome', 'firefox', 'discord', 'spotify', 'vlc', 'obs', 'photoshop']
        if any(popular in name_lower for popular in popular_apps):
            priority += 20
        
        # Apps do sistema têm prioridade baixa
        if app.publisher and app.publisher.lower() in self.system_publishers:
            priority -= 20
        
        # UWP apps têm prioridade média
        if app.is_uwp:
            priority += 10
        
        return priority
    
    def _is_selectable(self, app: AppInfo) -> bool:
        """Verifica se o app pode ser selecionado pelo usuário"""
        name_lower = app.name.lower()
        
        # Não selecionáveis: instaladores, atualizadores, etc
        if any(excluded in name_lower for excluded in self.excluded_names):
            return False
        
        # Verificar se o executável existe e é acessível
        if not os.path.exists(app.executable_path):
            return False
        
        # Verificar se não é um arquivo do sistema crítico
        system_paths = [r'c:\windows', r'c:\program files\windows']
        for sys_path in system_paths:
            if app.executable_path.lower().startswith(sys_path.lower()):
                return False
        
        return True
    
    def scan_all_apps(self, progress_callback: Optional[Callable] = None) -> Dict[str, AppInfo]:
        """
        Busca TODOS os aplicativos instalados no sistema
        Similar ao menu iniciar do Windows - COM FILTROS INTELIGENTES
        """
        apps_found = {}
        total_steps = 5
        current_step = 0
        
        try:
            # 1. Apps do Registry (Programas instalados)
            if progress_callback:
                progress_callback("Buscando programas instalados...", current_step, total_steps)
            
            registry_apps = self._scan_registry_apps()
            self._merge_apps_with_filters(apps_found, registry_apps)
            current_step += 1
            
            # 2. Apps UWP (Microsoft Store)
            if progress_callback:
                progress_callback("Buscando apps da Microsoft Store...", current_step, total_steps)
            
            uwp_apps = self._scan_uwp_apps()
            self._merge_apps_with_filters(apps_found, uwp_apps)
            current_step += 1
            
            # 3. Menu Iniciar
            if progress_callback:
                progress_callback("Buscando atalhos do menu iniciar...", current_step, total_steps)
            
            start_menu_apps = self._scan_start_menu()
            self._merge_apps_with_filters(apps_found, start_menu_apps)
            current_step += 1
            
            # 4. Área de Trabalho
            if progress_callback:
                progress_callback("Buscando atalhos da área de trabalho...", current_step, total_steps)
            
            desktop_apps = self._scan_desktop()
            self._merge_apps_with_filters(apps_found, desktop_apps)
            current_step += 1
            
            # 5. Diretórios comuns de programas
            if progress_callback:
                progress_callback("Finalizando busca em diretórios...", current_step, total_steps)
            
            directory_apps = self._scan_common_directories()
            self._merge_apps_with_filters(apps_found, directory_apps)
            current_step += 1
            
            if progress_callback:
                progress_callback(f"Busca concluída! {len(apps_found)} apps encontrados", current_step, total_steps)
            
            # Aplicar filtros finais e ordenação
            filtered_apps = self._apply_final_filters(apps_found)
            self.apps_cache = filtered_apps
            return filtered_apps
            
        except Exception as e:
            print(f"Erro na busca de apps: {e}")
            return apps_found
    
    def _merge_apps_with_filters(self, target_dict: Dict[str, AppInfo], source_dict: Dict[str, AppInfo]):
        """Mescla apps evitando duplicatas"""
        for app_id, app in source_dict.items():
            if not self._is_duplicate(app, target_dict):
                app.priority = self._calculate_priority(app)
                app.is_selectable = self._is_selectable(app)
                target_dict[app_id] = app
    
    def _apply_final_filters(self, apps: Dict[str, AppInfo]) -> Dict[str, AppInfo]:
        """Aplica filtros finais e ordena por prioridade"""
        # Filtrar apenas apps selecionáveis
        selectable_apps = {k: v for k, v in apps.items() if v.is_selectable}
        
        # Ordenar por prioridade (maior primeiro)
        sorted_items = sorted(selectable_apps.items(), key=lambda x: x[1].priority, reverse=True)
        
        return dict(sorted_items)
    
    def _scan_registry_apps(self) -> Dict[str, AppInfo]:
        """Busca apps no registro do Windows"""
        apps = {}
        
        # Locais do registro onde ficam os programas instalados
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        
        for hkey, subkey_path in registry_paths:
            try:
                with winreg.OpenKey(hkey, subkey_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                app_info = self._extract_app_from_registry(subkey)
                                if app_info:
                                    apps[app_info.app_id] = app_info
                        except Exception:
                            continue
            except Exception:
                continue
        
        return apps
    
    def _extract_app_from_registry(self, registry_key) -> Optional[AppInfo]:
        """Extrai informações do app do registro"""
        try:
            # Nome do app
            try:
                display_name = winreg.QueryValueEx(registry_key, "DisplayName")[0]
            except:
                return None
            
            # Pular apps do sistema e atualizações
            if any(skip in display_name.lower() for skip in [
                "microsoft visual c++", "microsoft .net", "update for",
                "security update", "hotfix", "kb", "microsoft office"
            ]):
                return None
            
            # Executável
            executable = None
            try:
                executable = winreg.QueryValueEx(registry_key, "DisplayIcon")[0]
                if not executable.endswith('.exe'):
                    executable = None
            except:
                pass
            
            if not executable:
                try:
                    uninstall_string = winreg.QueryValueEx(registry_key, "UninstallString")[0]
                    if uninstall_string and '.exe' in uninstall_string:
                        # Extrair executável da string de desinstalação
                        parts = uninstall_string.split('.exe')
                        if parts:
                            executable = parts[0] + '.exe'
                            executable = executable.strip('"').strip()
                except:
                    pass
            
            if not executable or not os.path.exists(executable):
                return None
            
            # Outras informações
            try:
                version = winreg.QueryValueEx(registry_key, "DisplayVersion")[0]
            except:
                version = None
            
            try:
                publisher = winreg.QueryValueEx(registry_key, "Publisher")[0]
            except:
                publisher = None
            
            try:
                install_location = winreg.QueryValueEx(registry_key, "InstallLocation")[0]
            except:
                install_location = os.path.dirname(executable)
            
            return AppInfo(
                name=display_name,
                executable_path=executable,
                version=version,
                publisher=publisher,
                install_directory=install_location,
                app_type="application"
            )
            
        except Exception:
            return None
    
    def _scan_uwp_apps(self) -> Dict[str, AppInfo]:
        """Busca apps UWP (Microsoft Store)"""
        apps = {}
        
        try:
            # Usar PowerShell para listar apps UWP
            ps_command = "Get-AppxPackage | Where-Object {$_.Name -notlike '*Microsoft*' -and $_.Name -notlike '*Windows*'} | Select-Object Name, InstallLocation"
            
            result = subprocess.run([
                "powershell", "-Command", ps_command
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                current_app = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('Name'):
                        if 'name' in current_app and current_app.get('name'):
                            # Processar app anterior
                            app_info = self._create_uwp_app_info(current_app)
                            if app_info:
                                apps[app_info.app_id] = app_info
                        current_app = {'name': line.split(':', 1)[1].strip()}
                    elif line.startswith('InstallLocation'):
                        current_app['location'] = line.split(':', 1)[1].strip()
                
                # Processar último app
                if 'name' in current_app and current_app.get('name'):
                    app_info = self._create_uwp_app_info(current_app)
                    if app_info:
                        apps[app_info.app_id] = app_info
                        
        except Exception:
            pass
        
        return apps
    
    def _create_uwp_app_info(self, app_data: dict) -> Optional[AppInfo]:
        """Cria AppInfo para app UWP"""
        try:
            name = app_data.get('name', '').strip()
            location = app_data.get('location', '').strip()
            
            if not name or not location or not os.path.exists(location):
                return None
            
            return AppInfo(
                name=name,
                executable_path=location,  # Para UWP, usamos o diretório
                install_directory=location,
                app_type="uwp_app",
                is_uwp=True
            )
        except:
            return None
    
    def _scan_start_menu(self) -> Dict[str, AppInfo]:
        """Busca atalhos no menu iniciar"""
        apps = {}
        
        start_menu_paths = [
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs"),
        ]
        
        for start_path in start_menu_paths:
            if os.path.exists(start_path):
                for root, dirs, files in os.walk(start_path):
                    for file in files:
                        if file.endswith('.lnk'):
                            shortcut_path = os.path.join(root, file)
                            app_info = self._extract_from_shortcut(shortcut_path)
                            if app_info:
                                apps[app_info.app_id] = app_info
        
        return apps
    
    def _scan_desktop(self) -> Dict[str, AppInfo]:
        """Busca atalhos na área de trabalho"""
        apps = {}
        
        desktop_paths = [
            os.path.expandvars(r"%USERPROFILE%\Desktop"),
            os.path.expandvars(r"%PUBLIC%\Desktop"),
        ]
        
        for desktop_path in desktop_paths:
            if os.path.exists(desktop_path):
                for file in os.listdir(desktop_path):
                    if file.endswith('.lnk'):
                        shortcut_path = os.path.join(desktop_path, file)
                        app_info = self._extract_from_shortcut(shortcut_path)
                        if app_info:
                            apps[app_info.app_id] = app_info
        
        return apps
    
    def _extract_from_shortcut(self, shortcut_path: str) -> Optional[AppInfo]:
        """Extrai informações de um atalho .lnk"""
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            
            target_path = shortcut.Targetpath
            if not target_path or not target_path.endswith('.exe') or not os.path.exists(target_path):
                return None
            
            name = os.path.splitext(os.path.basename(shortcut_path))[0]
            
            return AppInfo(
                name=name,
                executable_path=target_path,
                install_directory=os.path.dirname(target_path),
                app_type="application"
            )
            
        except Exception:
            return None
    
    def _scan_common_directories(self) -> Dict[str, AppInfo]:
        """Busca executáveis em diretórios comuns"""
        apps = {}
        
        for search_path in self.search_paths:
            try:
                if not os.path.exists(search_path):
                    continue
                
                # Buscar apenas no primeiro nível para não demorar muito
                for item in os.listdir(search_path):
                    item_path = os.path.join(search_path, item)
                    if os.path.isdir(item_path):
                        # Procurar por executável principal na pasta
                        for file in os.listdir(item_path):
                            if file.endswith('.exe') and not file.lower().startswith('unins'):
                                exe_path = os.path.join(item_path, file)
                                if os.path.exists(exe_path):
                                    app_info = AppInfo(
                                        name=os.path.splitext(file)[0],
                                        executable_path=exe_path,
                                        install_directory=item_path,
                                        app_type="application"
                                    )
                                    apps[app_info.app_id] = app_info
                                    break  # Apenas um exe por pasta
                                    
            except Exception:
                continue
        
        return apps
    
    def search_apps(self, query: str) -> List[AppInfo]:
        """Busca apps por nome (filtro de pesquisa)"""
        if not self.apps_cache:
            return []
        
        query = query.lower().strip()
        if not query:
            return list(self.apps_cache.values())
        
        results = []
        for app in self.apps_cache.values():
            if query in app.name.lower():
                results.append(app)
        
        # Ordenar por relevância (nome que começa com a busca primeiro)
        results.sort(key=lambda app: (
            not app.name.lower().startswith(query),
            app.name.lower()
        ))
        
        return results
    
    def launch_app(self, app: AppInfo) -> bool:
        """Executa um aplicativo"""
        try:
            if app.is_uwp:
                # Para apps UWP, tentar usar explorer
                subprocess.Popen([
                    "explorer.exe", f"shell:appsFolder\\{app.name}"
                ], shell=True)
            else:
                # Para apps normais
                subprocess.Popen([app.executable_path], shell=True)
            return True
        except Exception as e:
            print(f"Erro ao executar {app.name}: {e}")
            return False
    
    def launch_multiple_apps(self, apps: List[AppInfo]) -> Dict[str, bool]:
        """Executa múltiplos apps de uma vez"""
        results = {}
        
        for app in apps:
            success = self.launch_app(app)
            results[app.name] = success
            
            # Pequeno delay entre execuções
            time.sleep(0.5)
        
        return results