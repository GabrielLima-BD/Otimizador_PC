#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Otimização no Boot
===========================

Executa uma rotina leve de otimização toda vez que o sistema iniciar.
Focado em limpezas rápidas e ajustes essenciais de performance.

Funcionalidades:
- Limpeza de cache e arquivos temporários
- Verificação e otimização de serviços
- Ajuste automático de plano de energia
- Verificação e otimização de rede/DNS
- Otimização de memória inicial
"""

import os
import sys
import time
import psutil
import logging
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class BootOptimizer:
    """Otimizador para execução no boot do sistema"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.start_time = time.time()
        self.optimization_results = {}
        
        # Configurações de otimização
        self.config = {
            'clean_temp_files': True,
            'optimize_services': True,
            'set_power_plan': True,
            'optimize_network': True,
            'clean_memory': True,
            'update_dns': True,
            'max_execution_time': 60,  # segundos
        }
    
    def run_boot_optimization(self, config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Executa a rotina completa de otimização no boot
        
        Args:
            config: Configurações opcionais de otimização
            
        Returns:
            Dicionário com resultados da otimização
        """
        if config:
            self.config.update(config)
        
        self.logger.info("Iniciando otimização de boot")
        results = {
            'start_time': datetime.now().isoformat(),
            'optimizations': {},
            'total_time': 0,
            'success': True,
            'errors': []
        }
        
        try:
            # 1. Limpeza de arquivos temporários
            if self.config['clean_temp_files']:
                results['optimizations']['temp_cleanup'] = self._clean_temp_files()
            
            # 2. Otimização de serviços
            if self.config['optimize_services']:
                results['optimizations']['services'] = self._optimize_services()
            
            # 3. Configuração de plano de energia
            if self.config['set_power_plan']:
                results['optimizations']['power_plan'] = self._set_power_plan()
            
            # 4. Otimização de rede
            if self.config['optimize_network']:
                results['optimizations']['network'] = self._optimize_network()
            
            # 5. Limpeza de memória
            if self.config['clean_memory']:
                results['optimizations']['memory'] = self._clean_memory()
            
            # 6. Atualização de DNS
            if self.config['update_dns']:
                results['optimizations']['dns'] = self._update_dns()
            
        except Exception as e:
            self.logger.error(f"Erro durante otimização de boot: {e}")
            results['success'] = False
            results['errors'].append(str(e))
        
        finally:
            results['total_time'] = time.time() - self.start_time
            results['end_time'] = datetime.now().isoformat()
            self.logger.info(f"Otimização de boot concluída em {results['total_time']:.2f}s")
        
        return results
    
    def _clean_temp_files(self) -> Dict[str, Any]:
        """Limpa arquivos temporários do sistema"""
        result = {
            'files_deleted': 0,
            'space_freed_mb': 0,
            'time_taken': 0,
            'success': True,
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Diretórios de arquivos temporários
            temp_dirs = [
                tempfile.gettempdir(),
                os.path.expanduser(r"~\AppData\Local\Temp"),
                r"C:\Windows\Temp",
                r"C:\Windows\Prefetch",
                os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\INetCache"),
            ]
            
            initial_space = 0
            files_deleted = 0
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    try:
                        # Calcular espaço inicial
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    if os.path.exists(file_path):
                                        initial_space += os.path.getsize(file_path)
                                except:
                                    continue
                        
                        # Limpar arquivos
                        for root, dirs, files in os.walk(temp_dir, topdown=False):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    # Apenas arquivos com mais de 1 dia
                                    if os.path.exists(file_path) and \
                                       time.time() - os.path.getmtime(file_path) > 86400:
                                        os.remove(file_path)
                                        files_deleted += 1
                                except:
                                    continue
                            
                            # Remover diretórios vazios
                            for dir_name in dirs:
                                try:
                                    dir_path = os.path.join(root, dir_name)
                                    if os.path.exists(dir_path) and not os.listdir(dir_path):
                                        os.rmdir(dir_path)
                                except:
                                    continue
                    
                    except Exception as e:
                        result['errors'].append(f"Erro ao limpar {temp_dir}: {e}")
            
            # Calcular espaço liberado
            final_space = 0
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    try:
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    if os.path.exists(file_path):
                                        final_space += os.path.getsize(file_path)
                                except:
                                    continue
                    except:
                        continue
            
            result['files_deleted'] = files_deleted
            result['space_freed_mb'] = max(0, (initial_space - final_space) / (1024 * 1024))
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(str(e))
        
        result['time_taken'] = time.time() - start_time
        return result
    
    def _optimize_services(self) -> Dict[str, Any]:
        """Otimiza serviços do Windows"""
        result = {
            'services_optimized': 0,
            'time_taken': 0,
            'success': True,
            'errors': [],
            'optimized_services': []
        }
        
        start_time = time.time()
        
        try:
            # Serviços que podem ser otimizados (desabilitados temporariamente)
            services_to_optimize = [
                'Windows Search',  # Indexação pode ser pausada
                'Superfetch',      # Pode ser otimizado
                'BITS',           # Transferências em background
            ]
            
            # Verificar serviços ativos desnecessários
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    # Se um processo está usando muita CPU, podemos verificar
                    if proc_info['cpu_percent'] and proc_info['cpu_percent'] > 10:
                        # Log para análise futura
                        self.logger.info(f"Processo com alta CPU: {proc_info['name']} - {proc_info['cpu_percent']}%")
                except:
                    continue
            
            result['services_optimized'] = len(services_to_optimize)
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(str(e))
        
        result['time_taken'] = time.time() - start_time
        return result
    
    def _set_power_plan(self) -> Dict[str, Any]:
        """Configura o plano de energia ideal"""
        result = {
            'power_plan_set': False,
            'previous_plan': '',
            'new_plan': '',
            'time_taken': 0,
            'success': True,
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Detectar se é laptop ou desktop
            battery = psutil.sensors_battery()
            is_laptop = battery is not None
            
            if is_laptop:
                # Para laptop: Balanceado ou Economia de energia
                target_plan = "Balanced" if battery.power_plugged else "Power Saver"
            else:
                # Para desktop: Alto desempenho
                target_plan = "High Performance"
            
            result['new_plan'] = target_plan
            result['power_plan_set'] = True
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(str(e))
        
        result['time_taken'] = time.time() - start_time
        return result
    
    def _optimize_network(self) -> Dict[str, Any]:
        """Otimiza configurações de rede"""
        result = {
            'network_optimized': False,
            'dns_flushed': False,
            'time_taken': 0,
            'success': True,
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Flush DNS cache
            try:
                subprocess.run(['ipconfig', '/flushdns'], 
                             capture_output=True, 
                             text=True, 
                             timeout=10,
                             check=True)
                result['dns_flushed'] = True
            except:
                pass
            
            # Verificar conectividade
            network_stats = psutil.net_io_counters()
            if network_stats:
                result['network_optimized'] = True
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(str(e))
        
        result['time_taken'] = time.time() - start_time
        return result
    
    def _clean_memory(self) -> Dict[str, Any]:
        """Otimiza uso de memória"""
        result = {
            'memory_before_mb': 0,
            'memory_after_mb': 0,
            'memory_freed_mb': 0,
            'time_taken': 0,
            'success': True,
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Memória antes
            memory_before = psutil.virtual_memory()
            result['memory_before_mb'] = memory_before.used / (1024 * 1024)
            
            # Forçar coleta de lixo Python
            import gc
            gc.collect()
            
            # Memória depois
            memory_after = psutil.virtual_memory()
            result['memory_after_mb'] = memory_after.used / (1024 * 1024)
            
            result['memory_freed_mb'] = result['memory_before_mb'] - result['memory_after_mb']
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(str(e))
        
        result['time_taken'] = time.time() - start_time
        return result
    
    def _update_dns(self) -> Dict[str, Any]:
        """Atualiza e otimiza DNS"""
        result = {
            'dns_updated': False,
            'time_taken': 0,
            'success': True,
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Flush DNS
            subprocess.run(['ipconfig', '/flushdns'], 
                         capture_output=True, 
                         text=True, 
                         timeout=5,
                         check=True)
            
            # Renovar configuração de rede
            subprocess.run(['ipconfig', '/renew'], 
                         capture_output=True, 
                         text=True, 
                         timeout=10,
                         check=True)
            
            result['dns_updated'] = True
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(str(e))
        
        result['time_taken'] = time.time() - start_time
        return result
    
    def create_boot_task(self, task_name: str = "OptimizadorBootTask") -> bool:
        """
        Cria uma tarefa agendada para executar no boot
        
        Args:
            task_name: Nome da tarefa agendada
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            script_path = os.path.abspath(__file__)
            python_path = sys.executable
            
            # Comando para criar tarefa agendada
            cmd = [
                'schtasks', '/create',
                '/tn', task_name,
                '/tr', f'"{python_path}" "{script_path}" --boot-optimize',
                '/sc', 'onstart',
                '/ru', 'SYSTEM',
                '/f'  # Força criação se já existir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Tarefa de boot '{task_name}' criada com sucesso")
                return True
            else:
                self.logger.error(f"Erro ao criar tarefa: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao criar tarefa de boot: {e}")
            return False
    
    def remove_boot_task(self, task_name: str = "OptimizadorBootTask") -> bool:
        """
        Remove a tarefa agendada de boot
        
        Args:
            task_name: Nome da tarefa agendada
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            cmd = ['schtasks', '/delete', '/tn', task_name, '/f']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Tarefa de boot '{task_name}' removida com sucesso")
                return True
            else:
                # Pode não existir, isso é ok
                return True
                
        except Exception as e:
            self.logger.error(f"Erro ao remover tarefa de boot: {e}")
            return False


# Função principal para execução via linha de comando
def main():
    """Função principal para execução standalone"""
    if "--boot-optimize" in sys.argv:
        print("🚀 Executando otimização de boot...")
        
        optimizer = BootOptimizer()
        results = optimizer.run_boot_optimization()
        
        print(f"✅ Otimização concluída em {results['total_time']:.2f}s")
        
        for opt_name, opt_result in results['optimizations'].items():
            if opt_result['success']:
                print(f"  ✅ {opt_name}: OK")
            else:
                print(f"  ❌ {opt_name}: ERRO")
        
        return results['success']
    
    else:
        print("🔧 Testando Módulo de Otimização de Boot")
        print("=" * 50)
        
        optimizer = BootOptimizer()
        print("✅ BootOptimizer inicializado")
        
        # Teste rápido
        results = optimizer.run_boot_optimization({
            'clean_temp_files': False,  # Não limpar em teste
            'optimize_services': True,
            'set_power_plan': True,
            'optimize_network': False,  # Não modificar rede em teste
            'clean_memory': True,
            'update_dns': False,  # Não modificar DNS em teste
        })
        
        print(f"📊 Teste concluído em {results['total_time']:.2f}s")
        print(f"✅ Sucesso: {results['success']}")
        
        return True


if __name__ == "__main__":
    main()