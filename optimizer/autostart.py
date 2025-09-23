#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Inicialização Automática
=================================

Gerencia a configuração do programa para iniciar automaticamente com o Windows.
Suporta tanto registro do Windows quanto pasta de inicialização.

Funcionalidades:
- Adicionar/remover do registro do Windows
- Adicionar/remover da pasta de inicialização
- Verificar status atual de inicialização
- Configuração de argumentos de linha de comando
"""

import os
import sys
import winreg
import shutil
import logging
from pathlib import Path
from typing import Optional, Dict, Any

class AutostartManager:
    """Gerenciador de inicialização automática do Windows"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.app_name = "OptimizadorWindows10Pro"
        self.executable_path = self._get_executable_path()
        self.startup_folder = self._get_startup_folder()
        
    def _get_executable_path(self) -> str:
        """Obtém o caminho completo do executável atual"""
        if getattr(sys, 'frozen', False):
            # Se executando como executável compilado
            return sys.executable
        else:
            # Se executando como script Python
            script_path = os.path.abspath(sys.argv[0])
            python_path = sys.executable
            return f'"{python_path}" "{script_path}"'
    
    def _get_startup_folder(self) -> Path:
        """Obtém o caminho da pasta de inicialização do usuário"""
        startup_path = os.path.expanduser(
            r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        )
        return Path(startup_path)
    
    def is_enabled_registry(self) -> bool:
        """Verifica se a inicialização automática está habilitada no registro"""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run"
            ) as key:
                winreg.QueryValueEx(key, self.app_name)
                return True
        except FileNotFoundError:
            return False
        except Exception as e:
            self.logger.error(f"Erro ao verificar registro: {e}")
            return False
    
    def is_enabled_startup_folder(self) -> bool:
        """Verifica se existe um atalho na pasta de inicialização"""
        shortcut_path = self.startup_folder / f"{self.app_name}.lnk"
        return shortcut_path.exists()
    
    def enable_registry(self, minimized: bool = True) -> bool:
        """
        Habilita inicialização automática via registro do Windows
        
        Args:
            minimized: Se deve iniciar minimizado
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            # Comando para executar
            command = self.executable_path
            if minimized:
                command += " --minimized"
            
            # Adicionar ao registro
            with winreg.CreateKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run"
            ) as key:
                winreg.SetValueEx(
                    key, 
                    self.app_name, 
                    0, 
                    winreg.REG_SZ, 
                    command
                )
            
            self.logger.info("Inicialização automática habilitada no registro")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao habilitar no registro: {e}")
            return False
    
    def disable_registry(self) -> bool:
        """
        Desabilita inicialização automática do registro
        
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.DeleteValue(key, self.app_name)
            
            self.logger.info("Inicialização automática removida do registro")
            return True
            
        except FileNotFoundError:
            # Já não existe no registro
            return True
        except Exception as e:
            self.logger.error(f"Erro ao remover do registro: {e}")
            return False
    
    def enable_startup_folder(self, minimized: bool = True) -> bool:
        """
        Cria atalho na pasta de inicialização
        
        Args:
            minimized: Se deve iniciar minimizado
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            import comtypes.client
            
            # Criar diretório se não existir
            self.startup_folder.mkdir(parents=True, exist_ok=True)
            
            # Caminho do atalho
            shortcut_path = self.startup_folder / f"{self.app_name}.lnk"
            
            # Criar atalho usando COM
            shell = comtypes.client.CreateObject("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            
            if getattr(sys, 'frozen', False):
                shortcut.Targetpath = sys.executable
                if minimized:
                    shortcut.Arguments = "--minimized"
            else:
                shortcut.Targetpath = sys.executable
                script_path = os.path.abspath(sys.argv[0])
                args = f'"{script_path}"'
                if minimized:
                    args += " --minimized"
                shortcut.Arguments = args
            
            shortcut.WorkingDirectory = os.path.dirname(self.executable_path.strip('"'))
            shortcut.IconLocation = shortcut.Targetpath
            shortcut.WindowStyle = 7 if minimized else 1  # 7 = Minimized, 1 = Normal
            shortcut.Save()
            
            self.logger.info("Atalho criado na pasta de inicialização")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar atalho: {e}")
            return False
    
    def disable_startup_folder(self) -> bool:
        """
        Remove atalho da pasta de inicialização
        
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            shortcut_path = self.startup_folder / f"{self.app_name}.lnk"
            if shortcut_path.exists():
                shortcut_path.unlink()
                self.logger.info("Atalho removido da pasta de inicialização")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao remover atalho: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtém status atual da inicialização automática
        
        Returns:
            Dicionário com informações de status
        """
        return {
            'registry_enabled': self.is_enabled_registry(),
            'startup_folder_enabled': self.is_enabled_startup_folder(),
            'executable_path': self.executable_path,
            'startup_folder_path': str(self.startup_folder)
        }
    
    def enable_autostart(self, method: str = "registry", minimized: bool = True) -> bool:
        """
        Habilita inicialização automática usando o método especificado
        
        Args:
            method: "registry" ou "startup_folder"
            minimized: Se deve iniciar minimizado
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        if method == "registry":
            return self.enable_registry(minimized)
        elif method == "startup_folder":
            return self.enable_startup_folder(minimized)
        else:
            raise ValueError("Método deve ser 'registry' ou 'startup_folder'")
    
    def disable_autostart(self, method: str = "all") -> bool:
        """
        Desabilita inicialização automática
        
        Args:
            method: "registry", "startup_folder" ou "all"
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        success = True
        
        if method in ["registry", "all"]:
            success &= self.disable_registry()
        
        if method in ["startup_folder", "all"]:
            success &= self.disable_startup_folder()
        
        return success
    
    def is_running_on_startup(self) -> bool:
        """Verifica se o programa foi iniciado automaticamente"""
        return "--minimized" in sys.argv or "--autostart" in sys.argv


# Funções de conveniência
def enable_autostart(method: str = "registry", minimized: bool = True) -> bool:
    """Habilita inicialização automática"""
    manager = AutostartManager()
    return manager.enable_autostart(method, minimized)

def disable_autostart(method: str = "all") -> bool:
    """Desabilita inicialização automática"""
    manager = AutostartManager()
    return manager.disable_autostart(method)

def get_autostart_status() -> Dict[str, Any]:
    """Obtém status da inicialização automática"""
    manager = AutostartManager()
    return manager.get_status()

def is_autostart_enabled() -> bool:
    """Verifica se a inicialização automática está habilitada"""
    manager = AutostartManager()
    status = manager.get_status()
    return status['registry_enabled'] or status['startup_folder_enabled']


if __name__ == "__main__":
    # Teste do módulo
    print("🔧 Testando Módulo de Inicialização Automática")
    print("=" * 50)
    
    manager = AutostartManager()
    status = manager.get_status()
    
    print(f"📍 Caminho do executável: {status['executable_path']}")
    print(f"📁 Pasta de inicialização: {status['startup_folder_path']}")
    print(f"📋 Registro habilitado: {status['registry_enabled']}")
    print(f"🔗 Atalho habilitado: {status['startup_folder_enabled']}")
    
    print("\n✅ Módulo funcionando corretamente!")