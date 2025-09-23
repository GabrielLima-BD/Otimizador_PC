import winreg
import logging
import os
from .utils import Utils

class RegistryOptimizer:
    """Classe responsável pelas otimizações do registro do Windows"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.registry_changes = []
        self.backup_data = {}
    
    def disable_telemetry(self, progress_callback=None):
        """Desabilita telemetria e coleta de dados do Windows"""
        if progress_callback:
            progress_callback("Desabilitando telemetria...", 0)
        
        telemetry_settings = [
            # Telemetria principal
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", 
             "AllowTelemetry", winreg.REG_DWORD, 0),
            
            # Experiências do cliente
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", 
             "AllowTelemetry", winreg.REG_DWORD, 0),
            
            # Programa de aperfeiçoamento
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Siuf\Rules", 
             "NumberOfSIUFInPeriod", winreg.REG_DWORD, 0),
             
            # Feedback e diagnósticos
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Siuf\Rules", 
             "PeriodInNanoSeconds", winreg.REG_DWORD, 0),
        ]
        
        success_count = 0
        total_settings = len(telemetry_settings)
        
        for i, (hive, key_path, value_name, value_type, value_data) in enumerate(telemetry_settings):
            if progress_callback:
                progress_callback(f"Configurando telemetria {i+1}/{total_settings}...", 
                                (i / total_settings) * 100)
            
            success = self._set_registry_value(hive, key_path, value_name, value_type, value_data)
            if success:
                success_count += 1
        
        if progress_callback:
            progress_callback("Telemetria desabilitada", 100)
        
        self.registry_changes.append(f"Telemetria desabilitada ({success_count} configurações)")
        self.logger.info(f"Telemetria desabilitada: {success_count}/{total_settings} configurações aplicadas")
        return success_count > 0
    
    def disable_cortana(self, progress_callback=None):
        """Desabilita Cortana"""
        if progress_callback:
            progress_callback("Desabilitando Cortana...", 0)
        
        cortana_settings = [
            # Desabilita Cortana globalmente
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", 
             "AllowCortana", winreg.REG_DWORD, 0),
            
            # Desabilita pesquisa na web
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search", 
             "BingSearchEnabled", winreg.REG_DWORD, 0),
             
            # Desabilita busca de dispositivos
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search", 
             "AllowSearchToUseLocation", winreg.REG_DWORD, 0),
             
            # Desabilita histórico de pesquisa
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search", 
             "CortanaConsent", winreg.REG_DWORD, 0),
        ]
        
        success_count = 0
        
        for i, (hive, key_path, value_name, value_type, value_data) in enumerate(cortana_settings):
            if progress_callback:
                progress_callback(f"Configurando Cortana {i+1}/{len(cortana_settings)}...", 
                                (i / len(cortana_settings)) * 100)
            
            success = self._set_registry_value(hive, key_path, value_name, value_type, value_data)
            if success:
                success_count += 1
        
        if progress_callback:
            progress_callback("Cortana desabilitada", 100)
        
        self.registry_changes.append(f"Cortana desabilitada ({success_count} configurações)")
        self.logger.info(f"Cortana desabilitada: {success_count} configurações aplicadas")
        return success_count > 0
    
    def disable_windows_tips(self, progress_callback=None):
        """Desabilita dicas e sugestões do Windows"""
        if progress_callback:
            progress_callback("Desabilitando dicas do Windows...", 0)
        
        tips_settings = [
            # Dicas do Windows
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", 
             "SoftLandingEnabled", winreg.REG_DWORD, 0),
             
            # Sugestões da tela de bloqueio
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", 
             "RotatingLockScreenEnabled", winreg.REG_DWORD, 0),
             
            # Apps sugeridos
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", 
             "SystemPaneSuggestionsEnabled", winreg.REG_DWORD, 0),
             
            # Notificações de dicas
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Notifications\Settings\Windows.SystemToast.StartupApp", 
             "Enabled", winreg.REG_DWORD, 0),
        ]
        
        success_count = 0
        
        for i, (hive, key_path, value_name, value_type, value_data) in enumerate(tips_settings):
            if progress_callback:
                progress_callback(f"Configurando dicas {i+1}/{len(tips_settings)}...", 
                                (i / len(tips_settings)) * 100)
            
            success = self._set_registry_value(hive, key_path, value_name, value_type, value_data)
            if success:
                success_count += 1
        
        if progress_callback:
            progress_callback("Dicas do Windows desabilitadas", 100)
        
        self.registry_changes.append(f"Dicas do Windows desabilitadas ({success_count} configurações)")
        return success_count > 0
    
    def optimize_explorer_performance(self, progress_callback=None):
        """Otimiza performance do Windows Explorer"""
        if progress_callback:
            progress_callback("Otimizando Windows Explorer...", 0)
        
        explorer_settings = [
            # Desabilita thumbnail cache
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", 
             "DisableThumbnailCache", winreg.REG_DWORD, 1),
             
            # Mostra extensões de arquivos
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 
             "HideFileExt", winreg.REG_DWORD, 0),
             
            # Desabilita visualização de arquivos na barra de tarefas
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 
             "ExtendedUIHoverTime", winreg.REG_DWORD, 10000),
             
            # Otimiza para melhor performance
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 
             "VisualFXSetting", winreg.REG_DWORD, 2),
        ]
        
        success_count = 0
        
        for i, (hive, key_path, value_name, value_type, value_data) in enumerate(explorer_settings):
            if progress_callback:
                progress_callback(f"Configurando Explorer {i+1}/{len(explorer_settings)}...", 
                                (i / len(explorer_settings)) * 100)
            
            success = self._set_registry_value(hive, key_path, value_name, value_type, value_data)
            if success:
                success_count += 1
        
        if progress_callback:
            progress_callback("Windows Explorer otimizado", 100)
        
        self.registry_changes.append(f"Windows Explorer otimizado ({success_count} configurações)")
        return success_count > 0
    
    def disable_windows_updates_restart(self, progress_callback=None):
        """Desabilita reinicializações automáticas do Windows Update"""
        if progress_callback:
            progress_callback("Configurando Windows Update...", 0)
        
        update_settings = [
            # Desabilita reinicialização automática
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU", 
             "NoAutoRebootWithLoggedOnUsers", winreg.REG_DWORD, 1),
             
            # Configura horário de reinicialização
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU", 
             "AUPowerManagement", winreg.REG_DWORD, 0),
        ]
        
        success_count = 0
        
        for i, (hive, key_path, value_name, value_type, value_data) in enumerate(update_settings):
            if progress_callback:
                progress_callback(f"Configurando Update {i+1}/{len(update_settings)}...", 
                                (i / len(update_settings)) * 100)
            
            success = self._set_registry_value(hive, key_path, value_name, value_type, value_data)
            if success:
                success_count += 1
        
        if progress_callback:
            progress_callback("Windows Update configurado", 100)
        
        self.registry_changes.append(f"Windows Update configurado ({success_count} configurações)")
        return success_count > 0
    
    def disable_background_apps(self, progress_callback=None):
        """Desabilita apps em segundo plano"""
        if progress_callback:
            progress_callback("Desabilitando apps em segundo plano...", 0)
        
        try:
            # Chave principal para apps em segundo plano
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                # Desabilita globalmente
                winreg.SetValueEx(key, "GlobalUserDisabled", 0, winreg.REG_DWORD, 1)
            
            if progress_callback:
                progress_callback("Apps em segundo plano desabilitados", 100)
            
            self.registry_changes.append("Apps em segundo plano desabilitados")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao desabilitar apps em segundo plano: {e}")
            return False
    
    def optimize_startup_delay(self, progress_callback=None):
        """Otimiza delay de inicialização de aplicações"""
        if progress_callback:
            progress_callback("Otimizando delay de inicialização...", 0)
        
        startup_settings = [
            # Reduz delay de aplicações de desktop
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize", 
             "StartupDelayInMSec", winreg.REG_DWORD, 0),
        ]
        
        success_count = 0
        
        for i, (hive, key_path, value_name, value_type, value_data) in enumerate(startup_settings):
            if progress_callback:
                progress_callback(f"Configurando startup {i+1}/{len(startup_settings)}...", 
                                (i / len(startup_settings)) * 100)
            
            success = self._set_registry_value(hive, key_path, value_name, value_type, value_data)
            if success:
                success_count += 1
        
        if progress_callback:
            progress_callback("Delay de inicialização otimizado", 100)
        
        self.registry_changes.append("Delay de inicialização otimizado")
        return success_count > 0
    
    def disable_location_tracking(self, progress_callback=None):
        """Desabilita rastreamento de localização"""
        if progress_callback:
            progress_callback("Desabilitando rastreamento de localização...", 0)
        
        location_settings = [
            # Desabilita serviço de localização
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location", 
             "Value", winreg.REG_SZ, "Deny"),
             
            # Desabilita para todos os usuários
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\lfsvc\Service\Configuration", 
             "Status", winreg.REG_DWORD, 0),
        ]
        
        success_count = 0
        
        for i, (hive, key_path, value_name, value_type, value_data) in enumerate(location_settings):
            if progress_callback:
                progress_callback(f"Configurando localização {i+1}/{len(location_settings)}...", 
                                (i / len(location_settings)) * 100)
            
            success = self._set_registry_value(hive, key_path, value_name, value_type, value_data)
            if success:
                success_count += 1
        
        if progress_callback:
            progress_callback("Rastreamento de localização desabilitado", 100)
        
        self.registry_changes.append(f"Rastreamento de localização desabilitado ({success_count} configurações)")
        return success_count > 0
    
    def _set_registry_value(self, hive, key_path, value_name, value_type, value_data):
        """Define um valor no registro de forma segura"""
        try:
            # Backup do valor atual
            current_value = self._get_registry_value(hive, key_path, value_name)
            backup_key = f"{hive}\\{key_path}\\{value_name}"
            self.backup_data[backup_key] = current_value
            
            # Cria a chave se não existir e define o valor
            with winreg.CreateKey(hive, key_path) as key:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
            
            self.logger.info(f"Registro alterado: {key_path}\\{value_name} = {value_data}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao alterar registro {key_path}\\{value_name}: {e}")
            return False
    
    def _get_registry_value(self, hive, key_path, value_name):
        """Obtém valor atual do registro"""
        try:
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ) as key:
                value, reg_type = winreg.QueryValueEx(key, value_name)
                return {'value': value, 'type': reg_type}
        except:
            return None
    
    def create_registry_backup(self):
        """Cria backup das alterações de registro"""
        backup_file = Utils.create_backup(self.backup_data, 'registry')
        if backup_file:
            self.logger.info(f"Backup do registro criado: {backup_file}")
            return backup_file
        return None
    
    def restore_registry_from_backup(self, backup_data):
        """Restaura registro a partir do backup"""
        restored_count = 0
        
        for backup_key, backup_value in backup_data.items():
            if backup_value is None:
                continue
                
            try:
                # Parse da chave de backup
                parts = backup_key.split('\\')
                hive_name = parts[0]
                key_path = '\\'.join(parts[1:-1])
                value_name = parts[-1]
                
                # Converte nome da hive para constante
                hive_map = {
                    'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
                    'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
                    'HKEY_USERS': winreg.HKEY_USERS,
                    'HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
                }
                
                hive = hive_map.get(hive_name)
                if hive is None:
                    continue
                
                # Restaura o valor
                with winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, value_name, 0, 
                                    backup_value['type'], backup_value['value'])
                
                restored_count += 1
                self.logger.info(f"Valor restaurado: {backup_key}")
                
            except Exception as e:
                self.logger.error(f"Erro ao restaurar {backup_key}: {e}")
        
        return restored_count
    
    def get_registry_summary(self):
        """Retorna resumo das alterações de registro"""
        return {
            'changes_count': len(self.registry_changes),
            'changes_list': self.registry_changes,
            'backup_entries': len(self.backup_data)
        }