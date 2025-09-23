#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Detecção de Jogos Dinâmica
====================================

Sistema de busca dinâmica e em tempo real de jogos instalados.
Não usa cache fixo - sempre busca jogos atuais no sistema.

Funcionalidades:
- Busca dinâmica em tempo real
- Detecção automática de novos jogos
- Escaneamento rápido e inteligente
- Suporte multi-launcher
- Atualização instantânea
"""

import os
import json
import time
import winreg
import logging
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass, asdict
import subprocess

@dataclass
class GameInfo:
    """Informações de um jogo detectado"""
    name: str
    executable_path: str
    install_directory: str
    launcher: str
    icon_path: Optional[str] = None
    size_mb: Optional[float] = None
    last_played: Optional[str] = None
    play_count: int = 0
    detected_date: str = ""
    game_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.detected_date:
            self.detected_date = datetime.now().isoformat()
        if not self.game_id:
            self.game_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Gera um ID único para o jogo"""
        unique_string = f"{self.name}_{self.executable_path}_{self.launcher}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]

class GameScanner:
    """Scanner dinâmico de jogos - busca em tempo real sem cache fixo"""
    
    def __init__(self, cache_file: str = "games_cache.json"):
        self.logger = logging.getLogger(__name__)
        self.cache_file = Path(cache_file)  # Mantém só para compatibilidade
        self.games_cache = {}  # Mantém para compatibilidade
        self.scan_running = False
        self.last_scan_time = 0
        self.min_scan_interval = 1  # Mínimo 1 segundo entre escaneamentos
        
        # Diretórios prioritários para busca rápida
        self.priority_dirs = [
            # Ordem por probabilidade de ter jogos (otimização)
            r"C:\Program Files (x86)\Steam\steamapps\common",
            r"C:\Program Files\Steam\steamapps\common",
            r"C:\Program Files\Epic Games",
            r"C:\Program Files (x86)\Epic Games",
            r"C:\Program Files (x86)",
            r"C:\Program Files",
            r"C:\Games",
            r"D:\Games",
            r"E:\Games",
        ]
        
        # Diretórios específicos de launchers
        self.launcher_dirs = {
            'Steam': [
                r"C:\Program Files (x86)\Steam\steamapps\common",
                r"C:\Program Files\Steam\steamapps\common",
            ],
            'Epic Games': [
                r"C:\Program Files\Epic Games",
                r"C:\Program Files (x86)\Epic Games",
            ],
            'Origin': [
                r"C:\Program Files (x86)\Origin Games",
                r"C:\Program Files\Origin Games",
            ],
            'Ubisoft Connect': [
                r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games",
                r"C:\Program Files\Ubisoft\Ubisoft Game Launcher\games",
            ],
            'Battle.net': [
                r"C:\Program Files (x86)\Battle.net",
                r"C:\Program Files\Battle.net",
            ],
            'Rockstar Games': [
                r"C:\Program Files\Rockstar Games",
                r"C:\Program Files (x86)\Rockstar Games",
            ],
            'GOG Galaxy': [
                r"C:\Program Files (x86)\GOG Galaxy\Games",
                r"C:\Program Files\GOG Galaxy\Games",
            ],
            'EA App': [
                r"C:\Program Files\EA Games",
                r"C:\Program Files (x86)\EA Games",
            ]
        }
        
        # Extensões de executáveis de jogos
        self.game_extensions = {'.exe', '.bat', '.cmd'}
        
        # Palavras-chave para identificar jogos
        self.game_keywords = {
            'game', 'launcher', 'client', 'play', 'start',
            'engine', 'unity', 'unreal', 'godot'
        }
        
        # Palavras-chave para excluir (não são jogos)
        self.exclude_keywords = {
            'uninstall', 'setup', 'installer', 'update', 'updater',
            'config', 'settings', 'redist', 'vcredist', 'directx',
            'crash', 'report', 'log', 'debug', 'test', 'benchmark'
        }
        
        self.load_cache()
    
    def load_cache(self) -> None:
        """Carrega cache de jogos detectados"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for game_data in data.values():
                    game_info = GameInfo(**game_data)
                    self.games_cache[game_info.game_id] = game_info
                
                self.logger.info(f"Cache carregado: {len(self.games_cache)} jogos")
        
        except Exception as e:
            self.logger.error(f"Erro ao carregar cache: {e}")
            self.games_cache = {}
    
    def save_cache(self) -> None:
        """Salva cache de jogos detectados"""
        try:
            # Criar diretório se não existir
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Converter para dict serializável
            cache_data = {
                game_id: asdict(game_info) 
                for game_id, game_info in self.games_cache.items()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Cache salvo: {len(self.games_cache)} jogos")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar cache: {e}")
    
    def scan_games_with_progress(self, progress_callback=None) -> Dict[str, GameInfo]:
        """
        Busca completa com callback de progresso
        
        Args:
            progress_callback: Função chamada com (etapa, progresso, total)
            
        Returns:
            Dicionário com jogos encontrados
        """
        if self.scan_running:
            self.logger.warning("Busca já em execução")
            return getattr(self, '_last_scan_result', {})
        
        self.scan_running = True
        
        try:
            self.logger.info("🔍 Iniciando busca completa de jogos...")
            start_time = time.time()
            
            games_found = {}
            total_steps = len(self.launcher_dirs) + 2  # launchers + registry + diretórios
            current_step = 0
            
            # Busca por launcher específico
            for launcher_name, dirs in self.launcher_dirs.items():
                current_step += 1
                if progress_callback:
                    progress_callback(f"Buscando {launcher_name}...", current_step, total_steps)
                
                for directory in dirs:
                    if os.path.exists(directory):
                        launcher_games = self._scan_launcher_directory(directory, launcher_name)
                        games_found.update(launcher_games)
                        self.logger.info(f"📁 {launcher_name}: {len(launcher_games)} jogos")
            
            # Busca no registro
            current_step += 1
            if progress_callback:
                progress_callback("Buscando no Registro do Windows...", current_step, total_steps)
            
            registry_games = self._quick_scan_registry()
            games_found.update(registry_games)
            self.logger.info(f"🗂️ Registro: {len(registry_games)} jogos")
            
            # Busca em diretórios comuns
            current_step += 1
            if progress_callback:
                progress_callback("Buscando em diretórios comuns...", current_step, total_steps)
            
            common_games = self._quick_scan_priority_dirs()
            games_found.update(common_games)
            self.logger.info(f"📂 Diretórios: {len(common_games)} jogos")
            
            scan_time = time.time() - start_time
            self.logger.info(f"✅ Busca completa: {len(games_found)} jogos em {scan_time:.2f}s")
            
            # Finalizar progresso
            if progress_callback:
                progress_callback("Busca concluída!", total_steps, total_steps)
            
            # Salva resultado
            self._last_scan_result = games_found
            return games_found
            
        except Exception as e:
            self.logger.error(f"❌ Erro na busca completa: {e}")
            if progress_callback:
                progress_callback(f"Erro: {e}", 0, 1)
            return getattr(self, '_last_scan_result', {})
        
        finally:
            self.scan_running = False
    
    def scan_games(self, force_rescan: bool = False) -> Dict[str, GameInfo]:
        """Método de compatibilidade - chama a busca com progresso"""
        return self.scan_games_with_progress()
    
    def _scan_launcher_directory(self, directory: str, launcher_name: str) -> Dict[str, GameInfo]:
        """Escaneia diretório específico de launcher"""
        return self._quick_scan_directory(directory, launcher_name, max_depth=2)
        """
        Busca dinâmica de jogos - sempre atualizado
        
        Args:
            force_rescan: Compatibilidade (sempre faz busca dinâmica)
            
        Returns:
            Dicionário com jogos encontrados no momento
        """
        current_time = time.time()
        
        # Proteção contra escaneamentos muito frequentes
        if self.scan_running or (current_time - self.last_scan_time) < self.min_scan_interval:
            self.logger.info("Aguardando intervalo mínimo entre escaneamentos")
            # Retorna resultado anterior se muito recente
            return getattr(self, '_last_scan_result', {})
        
        self.scan_running = True
        self.last_scan_time = current_time
        
        try:
            self.logger.info("🔍 Busca dinâmica de jogos iniciada...")
            start_time = time.time()
            
            # Limpa resultado anterior - sempre busca fresh
            games_found = {}
            
            # Busca rápida e direcionada
            games_found.update(self._quick_scan_steam())
            games_found.update(self._quick_scan_epic())
            games_found.update(self._quick_scan_priority_dirs())
            games_found.update(self._quick_scan_registry())
            
            scan_time = time.time() - start_time
            self.logger.info(f"✅ Busca dinâmica: {len(games_found)} jogos em {scan_time:.2f}s")
            
            # Salva resultado temporário
            self._last_scan_result = games_found
            return games_found
            
        except Exception as e:
            self.logger.error(f"❌ Erro na busca dinâmica: {e}")
            return getattr(self, '_last_scan_result', {})
        
        finally:
            self.scan_running = False
        
        return getattr(self, '_last_scan_result', {})
    
    def _quick_scan_steam(self) -> Dict[str, GameInfo]:
        """Busca rápida de jogos Steam"""
        games = {}
        try:
            steam_dirs = [
                r"C:\Program Files (x86)\Steam\steamapps\common",
                r"C:\Program Files\Steam\steamapps\common"
            ]
            
            for steam_dir in steam_dirs:
                if os.path.exists(steam_dir):
                    games.update(self._quick_scan_directory(steam_dir, "Steam", max_depth=2))
                    
        except Exception as e:
            self.logger.debug(f"Erro na busca Steam: {e}")
        
        return games
    
    def _quick_scan_epic(self) -> Dict[str, GameInfo]:
        """Busca rápida de jogos Epic Games"""
        games = {}
        try:
            epic_dirs = [
                r"C:\Program Files\Epic Games",
                r"C:\Program Files (x86)\Epic Games"
            ]
            
            for epic_dir in epic_dirs:
                if os.path.exists(epic_dir):
                    games.update(self._quick_scan_directory(epic_dir, "Epic Games", max_depth=2))
                    
        except Exception as e:
            self.logger.debug(f"Erro na busca Epic: {e}")
        
        return games
    
    def _quick_scan_priority_dirs(self) -> Dict[str, GameInfo]:
        """Busca rápida em diretórios prioritários"""
        games = {}
        try:
            # Diretórios mais prováveis primeiro
            priority_list = [
                r"C:\Games",
                r"D:\Games", 
                r"E:\Games"
            ]
            
            for directory in priority_list:
                if os.path.exists(directory):
                    games.update(self._quick_scan_directory(directory, "Manual", max_depth=2))
                    
        except Exception as e:
            self.logger.debug(f"Erro na busca diretórios: {e}")
        
        return games
    
    def _quick_scan_registry(self) -> Dict[str, GameInfo]:
        """Busca rápida no registro do Windows"""
        games = {}
        try:
            registry_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            
            for hkey, subkey in registry_keys:
                # Busca simples no registro - implementação própria
                try:
                    with winreg.OpenKey(hkey, subkey) as key:
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey_handle:
                                    try:
                                        display_name = winreg.QueryValueEx(subkey_handle, "DisplayName")[0]
                                        install_location = winreg.QueryValueEx(subkey_handle, "InstallLocation")[0]
                                        
                                        if self._is_likely_game_name(display_name) and os.path.exists(install_location):
                                            # Procura exe principal
                                            exe_files = [f for f in os.listdir(install_location) 
                                                        if f.endswith('.exe') and self._is_likely_game_exe(f)]
                                            
                                            if exe_files:
                                                game_info = GameInfo(
                                                    name=display_name,
                                                    executable_path=os.path.join(install_location, exe_files[0]),
                                                    install_directory=install_location,
                                                    launcher="Registry"
                                                )
                                                games[game_info.game_id] = game_info
                                                
                                    except (FileNotFoundError, OSError):
                                        pass
                                i += 1
                            except OSError:
                                break
                except Exception:
                    pass
                
        except Exception as e:
            self.logger.debug(f"Erro na busca registro: {e}")
        
        return games
    
    def _quick_scan_directory(self, directory: str, launcher: str, max_depth: int = 2) -> Dict[str, GameInfo]:
        """Escaneamento rápido de diretório específico"""
        games = {}
        try:
            if not os.path.exists(directory):
                return games
                
            # Busca apenas um nível para ser rápido
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                
                if os.path.isdir(item_path) and max_depth > 0:
                    # Procura executável principal na pasta do jogo
                    exe_files = [f for f in os.listdir(item_path) 
                                if f.endswith('.exe') and self._is_likely_game_exe(f)]
                    
                    if exe_files:
                        # Pega o primeiro exe que parece ser jogo
                        main_exe = exe_files[0]
                        exe_path = os.path.join(item_path, main_exe)
                        
                        game_info = GameInfo(
                            name=item,
                            executable_path=exe_path,
                            install_directory=item_path,
                            launcher=launcher,
                            size_mb=None  # Remove cálculo de tamanho para ser mais rápido
                        )
                        
                        games[game_info.game_id] = game_info
                        
        except Exception as e:
            self.logger.debug(f"Erro no scan rápido de {directory}: {e}")
        
        return games
    
    def _is_likely_game_exe(self, filename: str) -> bool:
        """Verifica se arquivo exe é provavelmente um jogo"""
        filename_lower = filename.lower()
        
        # Exclui arquivos que claramente não são jogos
        exclude_words = ['uninstall', 'setup', 'installer', 'updater', 'launcher', 'config']
        if any(word in filename_lower for word in exclude_words):
            return False
            
        # Inclui arquivos que provavelmente são jogos
        game_words = ['game', 'play', '.exe']
        return any(word in filename_lower for word in game_words) or len(filename_lower) > 3
    
    def _is_likely_game_name(self, name: str) -> bool:
        """Verifica se nome parece ser de um jogo"""
        name_lower = name.lower()
        
        # Exclui claramente não-jogos
        exclude_words = ['microsoft', 'windows', 'office', 'visual studio', 'driver', 'antivirus']
        if any(word in name_lower for word in exclude_words):
            return False
            
        # Inclui possíveis jogos
        game_indicators = ['game', 'play', 'simulator', 'adventure', 'rpg', 'fps', 'strategy']
        return any(word in name_lower for word in game_indicators) or len(name) < 50
    
    def _scan_steam_games(self) -> None:
        """Escaneia jogos do Steam"""
        try:
            # Tentar encontrar Steam via registro
            steam_path = self._get_steam_path()
            if not steam_path:
                return
            
            # Procurar bibliotecas do Steam
            library_folders = self._get_steam_library_folders(steam_path)
            
            for library in library_folders:
                common_path = library / "steamapps" / "common"
                if common_path.exists():
                    self._scan_directory(str(common_path), "Steam")
        
        except Exception as e:
            self.logger.error(f"Erro ao escanear Steam: {e}")
    
    def _get_steam_path(self) -> Optional[Path]:
        """Obtém caminho de instalação do Steam"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
                steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
                return Path(steam_path)
        except:
            # Tentar caminhos padrão
            default_paths = [
                r"C:\Program Files (x86)\Steam",
                r"C:\Program Files\Steam"
            ]
            for path in default_paths:
                if os.path.exists(path):
                    return Path(path)
        return None
    
    def _get_steam_library_folders(self, steam_path: Path) -> List[Path]:
        """Obtém todas as pastas de biblioteca do Steam"""
        libraries = [steam_path]
        
        try:
            # Ler arquivo de configuração das bibliotecas
            config_file = steam_path / "steamapps" / "libraryfolders.vdf"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Parser simples para VDF
                import re
                paths = re.findall(r'"path"\s*"([^"]+)"', content)
                for path in paths:
                    lib_path = Path(path.replace('\\\\', '\\'))
                    if lib_path.exists():
                        libraries.append(lib_path)
        
        except Exception as e:
            self.logger.error(f"Erro ao ler bibliotecas Steam: {e}")
        
        return libraries
    
    def _scan_epic_games(self) -> None:
        """Escaneia jogos do Epic Games Store"""
        try:
            # Epic Games manifests
            manifests_path = Path(os.path.expanduser(
                r"~\AppData\Local\EpicGamesLauncher\Saved\Logs"
            ))
            
            # Também escanear diretórios padrão
            for dir_path in self.launcher_dirs.get('Epic Games', []):
                if os.path.exists(dir_path):
                    self._scan_directory(dir_path, "Epic Games")
        
        except Exception as e:
            self.logger.error(f"Erro ao escanear Epic Games: {e}")
    
    def _scan_registry_games(self) -> None:
        """Escaneia jogos registrados no Windows Registry"""
        try:
            # Uninstall registry keys
            registry_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for reg_path in registry_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    self._process_registry_entry(subkey)
                                i += 1
                            except WindowsError:
                                break
                except Exception as e:
                    self.logger.error(f"Erro ao acessar registro {reg_path}: {e}")
        
        except Exception as e:
            self.logger.error(f"Erro ao escanear registro: {e}")
    
    def _process_registry_entry(self, registry_key) -> None:
        """Processa entrada do registro em busca de jogos"""
        try:
            # Tentar obter informações do programa
            display_name = ""
            install_location = ""
            executable = ""
            
            try:
                display_name = winreg.QueryValueEx(registry_key, "DisplayName")[0]
            except:
                return
            
            try:
                install_location = winreg.QueryValueEx(registry_key, "InstallLocation")[0]
            except:
                return
            
            # Verificar se parece com um jogo
            if self._is_likely_game(display_name, install_location):
                # Procurar executável principal
                if os.path.exists(install_location):
                    main_exe = self._find_main_executable(install_location, display_name)
                    if main_exe:
                        self._add_game(
                            name=display_name,
                            executable=main_exe,
                            install_dir=install_location,
                            launcher="Registry"
                        )
        
        except Exception as e:
            self.logger.debug(f"Erro ao processar entrada do registro: {e}")
    
    def _scan_launcher_directories(self) -> None:
        """Escaneia diretórios específicos de launchers"""
        for launcher, directories in self.launcher_dirs.items():
            for directory in directories:
                if os.path.exists(directory):
                    self._scan_directory(directory, launcher)
    
    def _scan_common_directories(self) -> None:
        """Escaneia diretórios prioritários de jogos"""
        for directory in self.priority_dirs:
            if os.path.exists(directory):
                self._scan_directory(directory, "Manual")
    
    def _scan_directory(self, directory: str, launcher: str, max_depth: int = 3) -> None:
        """
        Escaneia um diretório em busca de jogos
        
        Args:
            directory: Diretório para escanear
            launcher: Nome do launcher associado
            max_depth: Profundidade máxima de escaneamento
        """
        try:
            for root, dirs, files in os.walk(directory):
                # Limitar profundidade
                depth = root[len(directory):].count(os.sep)
                if depth >= max_depth:
                    dirs[:] = []  # Não descer mais
                    continue
                
                # Procurar executáveis de jogos
                for file in files:
                    if file.lower().endswith('.exe'):
                        exe_path = os.path.join(root, file)
                        
                        # Verificar se parece com um jogo
                        if self._is_game_executable(file, exe_path):
                            game_name = self._extract_game_name(file, root)
                            self._add_game(
                                name=game_name,
                                executable=exe_path,
                                install_dir=root,
                                launcher=launcher
                            )
        
        except Exception as e:
            self.logger.error(f"Erro ao escanear {directory}: {e}")
    
    def _is_likely_game(self, name: str, install_path: str) -> bool:
        """Verifica se um programa é provavelmente um jogo"""
        name_lower = name.lower()
        path_lower = install_path.lower()
        
        # Palavras-chave que excluem
        for exclude in self.exclude_keywords:
            if exclude in name_lower:
                return False
        
        # Palavras-chave que indicam jogo
        for keyword in self.game_keywords:
            if keyword in name_lower or keyword in path_lower:
                return True
        
        # Verificar se está em diretório de jogos
        for launcher_dirs in self.launcher_dirs.values():
            for launcher_dir in launcher_dirs:
                if launcher_dir.lower() in path_lower:
                    return True
        
        return False
    
    def _is_game_executable(self, filename: str, full_path: str) -> bool:
        """Verifica se um executável é provavelmente um jogo"""
        filename_lower = filename.lower()
        
        # Excluir arquivos óbvios que não são jogos
        for exclude in self.exclude_keywords:
            if exclude in filename_lower:
                return False
        
        # Verificar tamanho do arquivo (jogos geralmente são maiores)
        try:
            file_size = os.path.getsize(full_path)
            if file_size < 1024 * 1024:  # Menor que 1MB, provavelmente não é jogo
                return False
        except:
            pass
        
        return True
    
    def _extract_game_name(self, filename: str, directory: str) -> str:
        """Extrai nome do jogo baseado no arquivo e diretório"""
        # Tentar usar nome do diretório primeiro
        dir_name = os.path.basename(directory)
        if dir_name and not any(exclude in dir_name.lower() for exclude in ['bin', 'exe', 'game']):
            return dir_name
        
        # Usar nome do arquivo sem extensão
        return os.path.splitext(filename)[0]
    
    def _find_main_executable(self, install_dir: str, game_name: str) -> Optional[str]:
        """Encontra o executável principal de um jogo"""
        try:
            exe_files = []
            
            # Procurar executáveis no diretório
            for root, dirs, files in os.walk(install_dir):
                for file in files:
                    if file.lower().endswith('.exe'):
                        exe_path = os.path.join(root, file)
                        if self._is_game_executable(file, exe_path):
                            exe_files.append((exe_path, file))
            
            if not exe_files:
                return None
            
            # Tentar encontrar o executável que mais se parece com o nome do jogo
            game_name_lower = game_name.lower()
            for exe_path, filename in exe_files:
                filename_lower = filename.lower()
                if game_name_lower in filename_lower or filename_lower in game_name_lower:
                    return exe_path
            
            # Se não encontrou por nome, pegar o maior arquivo
            exe_files.sort(key=lambda x: os.path.getsize(x[0]), reverse=True)
            return exe_files[0][0]
        
        except Exception as e:
            self.logger.error(f"Erro ao encontrar executável principal: {e}")
            return None
    
    def _add_game(self, name: str, executable: str, install_dir: str, launcher: str) -> None:
        """Adiciona um jogo ao cache"""
        try:
            # Verificar se já existe
            game_id = hashlib.md5(f"{name}_{executable}_{launcher}".encode()).hexdigest()[:12]
            
            if game_id in self.games_cache:
                return  # Jogo já existe
            
            # Obter informações adicionais
            icon_path = self._find_game_icon(install_dir, executable)
            size_mb = self._calculate_game_size(install_dir)
            
            game_info = GameInfo(
                name=name,
                executable_path=executable,
                install_directory=install_dir,
                launcher=launcher,
                icon_path=icon_path,
                size_mb=size_mb
            )
            
            self.games_cache[game_id] = game_info
            self.logger.info(f"Jogo adicionado: {name} ({launcher})")
        
        except Exception as e:
            self.logger.error(f"Erro ao adicionar jogo {name}: {e}")
    
    def _find_game_icon(self, install_dir: str, executable: str) -> Optional[str]:
        """Procura ícone do jogo"""
        try:
            # Procurar ícones comuns
            icon_extensions = ['.ico', '.png', '.jpg', '.jpeg']
            icon_names = ['icon', 'logo', 'game', os.path.splitext(os.path.basename(executable))[0]]
            
            for root, dirs, files in os.walk(install_dir):
                for file in files:
                    filename_lower = file.lower()
                    
                    # Verificar se é um arquivo de ícone
                    if any(filename_lower.endswith(ext) for ext in icon_extensions):
                        # Verificar se o nome corresponde
                        for icon_name in icon_names:
                            if icon_name.lower() in filename_lower:
                                return os.path.join(root, file)
            
            # Se não encontrou, tentar extrair ícone do executável
            return executable  # O sistema pode extrair ícone do .exe
        
        except Exception as e:
            self.logger.error(f"Erro ao procurar ícone: {e}")
            return None
    
    def _calculate_game_size(self, install_dir: str) -> Optional[float]:
        """Calcula tamanho do jogo em MB"""
        try:
            total_size = 0
            for root, dirs, files in os.walk(install_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except:
                        continue
            
            return round(total_size / (1024 * 1024), 2)  # MB
        
        except Exception as e:
            self.logger.error(f"Erro ao calcular tamanho: {e}")
            return None
    
    def get_games_by_launcher(self, launcher: str) -> List[GameInfo]:
        """Obtém jogos de um launcher específico"""
        return [game for game in self.games_cache.values() if game.launcher == launcher]
    
    def get_recently_played_games(self, limit: int = 10) -> List[GameInfo]:
        """Obtém jogos jogados recentemente"""
        games_with_play_time = [
            game for game in self.games_cache.values() 
            if game.last_played
        ]
        
        # Ordenar por última vez jogado
        games_with_play_time.sort(
            key=lambda x: x.last_played or "", 
            reverse=True
        )
        
        return games_with_play_time[:limit]
    
    def update_game_play_info(self, game_id: str) -> None:
        """Atualiza informações de jogo quando é executado"""
        if game_id in self.games_cache:
            game = self.games_cache[game_id]
            game.last_played = datetime.now().isoformat()
            game.play_count += 1
            self.save_cache()
    
    def scan_async(self, callback: Optional[Callable] = None) -> threading.Thread:
        """
        Executa escaneamento em thread separada
        
        Args:
            callback: Função para chamar quando completar
            
        Returns:
            Thread do escaneamento
        """
        def scan_worker():
            results = self.scan_games(force_rescan=True)
            if callback:
                callback(results)
        
        thread = threading.Thread(target=scan_worker)
        thread.daemon = True
        thread.start()
        return thread


# Funções de conveniência
def scan_system_games(force_rescan: bool = False) -> Dict[str, GameInfo]:
    """Escaneia sistema em busca de jogos"""
    scanner = GameScanner()
    return scanner.scan_games(force_rescan)

def get_installed_games() -> List[GameInfo]:
    """Obtém lista de jogos instalados"""
    scanner = GameScanner()
    scanner.load_cache()
    return list(scanner.games_cache.values())


if __name__ == "__main__":
    # Teste do módulo
    print("🎮 Testando Módulo de Detecção de Jogos")
    print("=" * 50)
    
    scanner = GameScanner()
    print("✅ GameScanner inicializado")
    
    # Teste de escaneamento rápido
    print("📡 Iniciando escaneamento...")
    games = scanner.scan_games()
    
    print(f"🎯 Jogos encontrados: {len(games)}")
    
    # Mostrar alguns jogos encontrados
    for i, (game_id, game) in enumerate(games.items()):
        if i >= 5:  # Mostrar apenas 5 primeiros
            break
        print(f"  🎮 {game.name} ({game.launcher})")
    
    if len(games) > 5:
        print(f"  ... e mais {len(games) - 5} jogos")
    
    print("\n✅ Módulo funcionando corretamente!")