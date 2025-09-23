import schedule
import time
import threading
import logging
import json
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

class ScheduleType(Enum):
    """Tipos de agendamento disponíveis"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    STARTUP = "startup"
    IDLE = "idle"
    CUSTOM = "custom"

class OptimizationTask:
    """Representa uma tarefa de otimização agendada"""
    
    def __init__(self, task_id, name, task_type, schedule_type, schedule_config, enabled=True):
        self.task_id = task_id
        self.name = name
        self.task_type = task_type  # 'cleanup', 'optimization', 'defrag', etc.
        self.schedule_type = schedule_type
        self.schedule_config = schedule_config
        self.enabled = enabled
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.run_count = 0
        self.success_count = 0
        self.error_count = 0
        self.average_duration = 0.0
        self.created_at = datetime.now()

class ScheduleManager:
    """Gerenciador de agendamento inteligente"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tasks = {}
        self.scheduler_thread = None
        self.running = False
        self.config_file = "schedule_config.json"
        self.task_callbacks = {}
        
        # Configurações padrão
        self.default_schedules = {
            'quick_cleanup': {
                'name': 'Limpeza Rápida Diária',
                'task_type': 'quick_cleanup',
                'schedule_type': ScheduleType.DAILY,
                'schedule_config': {'time': '08:00', 'enabled': True}
            },
            'deep_cleanup': {
                'name': 'Limpeza Profunda Semanal',
                'task_type': 'deep_cleanup',
                'schedule_type': ScheduleType.WEEKLY,
                'schedule_config': {'day': 'sunday', 'time': '02:00', 'enabled': True}
            },
            'system_optimization': {
                'name': 'Otimização do Sistema',
                'task_type': 'system_optimization',
                'schedule_type': ScheduleType.WEEKLY,
                'schedule_config': {'day': 'saturday', 'time': '03:00', 'enabled': True}
            },
            'registry_cleanup': {
                'name': 'Limpeza do Registro',
                'task_type': 'registry_cleanup',
                'schedule_type': ScheduleType.MONTHLY,
                'schedule_config': {'day': 1, 'time': '01:00', 'enabled': True}
            },
            'duplicate_cleanup': {
                'name': 'Remoção de Duplicatas',
                'task_type': 'duplicate_cleanup',
                'schedule_type': ScheduleType.WEEKLY,
                'schedule_config': {'day': 'friday', 'time': '20:00', 'enabled': False}
            }
        }
        
        self.load_configuration()
    
    def start_scheduler(self, progress_callback=None):
        """Inicia o agendador"""
        if self.running:
            return False
        
        if progress_callback:
            progress_callback("Iniciando agendador...", 0)
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        if progress_callback:
            progress_callback("Agendador iniciado", 100)
        
        self.logger.info("Agendador iniciado")
        return True
    
    def stop_scheduler(self):
        """Para o agendador"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)
        
        self.logger.info("Agendador parado")
    
    def _scheduler_loop(self):
        """Loop principal do agendador"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(30)  # Verificar a cada 30 segundos
            except Exception as e:
                self.logger.error(f"Erro no loop do agendador: {e}")
                time.sleep(60)
    
    def add_task(self, task_id, name, task_type, schedule_type, schedule_config, enabled=True):
        """Adiciona uma nova tarefa agendada"""
        try:
            task = OptimizationTask(task_id, name, task_type, schedule_type, schedule_config, enabled)
            self.tasks[task_id] = task
            
            if enabled:
                self._schedule_task(task)
            
            self.save_configuration()
            self.logger.info(f"Tarefa adicionada: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar tarefa {task_id}: {e}")
            return False
    
    def remove_task(self, task_id):
        """Remove uma tarefa agendada"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            
            # Cancelar agendamento
            self._unschedule_task(task)
            
            # Remover da lista
            del self.tasks[task_id]
            
            self.save_configuration()
            self.logger.info(f"Tarefa removida: {task.name}")
            return True
        
        return False
    
    def enable_task(self, task_id):
        """Habilita uma tarefa"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.enabled = True
            self._schedule_task(task)
            self.save_configuration()
            self.logger.info(f"Tarefa habilitada: {task.name}")
            return True
        return False
    
    def disable_task(self, task_id):
        """Desabilita uma tarefa"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.enabled = False
            self._unschedule_task(task)
            self.save_configuration()
            self.logger.info(f"Tarefa desabilitada: {task.name}")
            return True
        return False
    
    def _schedule_task(self, task):
        """Agenda uma tarefa específica"""
        try:
            config = task.schedule_config
            
            if task.schedule_type == ScheduleType.DAILY:
                schedule.every().day.at(config['time']).do(self._run_task, task.task_id).tag(task.task_id)
                
            elif task.schedule_type == ScheduleType.WEEKLY:
                day_method = getattr(schedule.every(), config['day'].lower())
                day_method.at(config['time']).do(self._run_task, task.task_id).tag(task.task_id)
                
            elif task.schedule_type == ScheduleType.MONTHLY:
                # Para mensal, usar uma abordagem diferente (verificar no loop)
                # Por enquanto, agenda para todo primeiro dia do mês
                schedule.every().day.at(config['time']).do(self._check_monthly_task, task.task_id).tag(task.task_id)
                
            elif task.schedule_type == ScheduleType.STARTUP:
                # Executar na próxima verificação do agendador
                schedule.every().minute.do(self._run_startup_task, task.task_id).tag(task.task_id)
            
            # Calcular próxima execução
            task.next_run = self._calculate_next_run(task)
            
            self.logger.info(f"Tarefa agendada: {task.name} - Próxima execução: {task.next_run}")
            
        except Exception as e:
            self.logger.error(f"Erro ao agendar tarefa {task.task_id}: {e}")
    
    def _unschedule_task(self, task):
        """Cancela agendamento de uma tarefa"""
        try:
            schedule.clear(task.task_id)
            task.next_run = None
            self.logger.info(f"Agendamento cancelado: {task.name}")
        except Exception as e:
            self.logger.error(f"Erro ao cancelar agendamento {task.task_id}: {e}")
    
    def _run_task(self, task_id):
        """Executa uma tarefa agendada"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Executando tarefa agendada: {task.name}")
            
            # Verificar se existe callback registrado
            if task.task_type in self.task_callbacks:
                callback = self.task_callbacks[task.task_type]
                success = callback(task_id, task.task_type)
            else:
                self.logger.warning(f"Nenhum callback registrado para tipo: {task.task_type}")
                success = False
            
            # Atualizar estatísticas
            duration = (datetime.now() - start_time).total_seconds()
            task.last_run = start_time
            task.run_count += 1
            
            if success:
                task.success_count += 1
            else:
                task.error_count += 1
            
            # Calcular duração média
            if task.run_count > 0:
                task.average_duration = ((task.average_duration * (task.run_count - 1)) + duration) / task.run_count
            
            # Calcular próxima execução
            task.next_run = self._calculate_next_run(task)
            
            self.save_configuration()
            
            result_msg = "com sucesso" if success else "com erro"
            self.logger.info(f"Tarefa '{task.name}' executada {result_msg} em {duration:.2f}s")
            
        except Exception as e:
            task.error_count += 1
            self.logger.error(f"Erro ao executar tarefa {task_id}: {e}")
    
    def _run_startup_task(self, task_id):
        """Executa tarefa de startup (apenas uma vez)"""
        self._run_task(task_id)
        # Cancelar para não executar novamente
        schedule.clear(task_id)
    
    def _check_monthly_task(self, task_id):
        """Verifica se é hora de executar tarefa mensal"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        if task.schedule_type != ScheduleType.MONTHLY:
            return
        
        now = datetime.now()
        target_day = task.schedule_config.get('day', 1)
        
        # Verificar se é o dia correto do mês
        if now.day == target_day:
            # Verificar se ainda não executou este mês
            if not task.last_run or task.last_run.month != now.month:
                self._run_task(task_id)
    
    def _calculate_next_run(self, task):
        """Calcula próxima execução de uma tarefa"""
        try:
            now = datetime.now()
            config = task.schedule_config
            
            if task.schedule_type == ScheduleType.DAILY:
                target_time = datetime.strptime(config['time'], '%H:%M').time()
                next_run = datetime.combine(now.date(), target_time)
                
                # Se já passou da hora hoje, agendar para amanhã
                if next_run <= now:
                    next_run += timedelta(days=1)
                
                return next_run
                
            elif task.schedule_type == ScheduleType.WEEKLY:
                days = {
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                    'friday': 4, 'saturday': 5, 'sunday': 6
                }
                
                target_day = days.get(config['day'].lower(), 0)
                target_time = datetime.strptime(config['time'], '%H:%M').time()
                
                days_ahead = target_day - now.weekday()
                if days_ahead <= 0:  # Já passou esta semana
                    days_ahead += 7
                
                next_run = datetime.combine(now.date() + timedelta(days=days_ahead), target_time)
                return next_run
                
            elif task.schedule_type == ScheduleType.MONTHLY:
                target_day = config.get('day', 1)
                target_time = datetime.strptime(config['time'], '%H:%M').time()
                
                # Próximo mês
                if now.day >= target_day:
                    if now.month == 12:
                        next_month = now.replace(year=now.year + 1, month=1, day=target_day)
                    else:
                        next_month = now.replace(month=now.month + 1, day=target_day)
                else:
                    next_month = now.replace(day=target_day)
                
                next_run = datetime.combine(next_month.date(), target_time)
                return next_run
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular próxima execução: {e}")
        
        return None
    
    def register_task_callback(self, task_type, callback):
        """Registra callback para um tipo de tarefa"""
        self.task_callbacks[task_type] = callback
        self.logger.info(f"Callback registrado para tipo: {task_type}")
    
    def get_scheduled_tasks(self):
        """Retorna lista de tarefas agendadas"""
        return {
            task_id: {
                'name': task.name,
                'task_type': task.task_type,
                'schedule_type': task.schedule_type.value,
                'enabled': task.enabled,
                'last_run': task.last_run.isoformat() if task.last_run else None,
                'next_run': task.next_run.isoformat() if task.next_run else None,
                'run_count': task.run_count,
                'success_count': task.success_count,
                'error_count': task.error_count,
                'success_rate': (task.success_count / task.run_count * 100) if task.run_count > 0 else 0,
                'average_duration': task.average_duration
            }
            for task_id, task in self.tasks.items()
        }
    
    def get_next_scheduled_tasks(self, limit=5):
        """Retorna próximas tarefas agendadas"""
        upcoming_tasks = []
        
        for task_id, task in self.tasks.items():
            if task.enabled and task.next_run:
                upcoming_tasks.append({
                    'task_id': task_id,
                    'name': task.name,
                    'next_run': task.next_run,
                    'time_until': task.next_run - datetime.now()
                })
        
        # Ordenar por próxima execução
        upcoming_tasks.sort(key=lambda x: x['next_run'])
        
        return upcoming_tasks[:limit]
    
    def create_default_schedules(self):
        """Cria agendamentos padrão"""
        for task_id, config in self.default_schedules.items():
            if task_id not in self.tasks:
                self.add_task(
                    task_id=task_id,
                    name=config['name'],
                    task_type=config['task_type'],
                    schedule_type=config['schedule_type'],
                    schedule_config=config['schedule_config'],
                    enabled=config['schedule_config'].get('enabled', True)
                )
        
        self.logger.info("Agendamentos padrão criados")
    
    def save_configuration(self):
        """Salva configuração das tarefas"""
        try:
            config = {}
            for task_id, task in self.tasks.items():
                config[task_id] = {
                    'name': task.name,
                    'task_type': task.task_type,
                    'schedule_type': task.schedule_type.value,
                    'schedule_config': task.schedule_config,
                    'enabled': task.enabled,
                    'last_run': task.last_run.isoformat() if task.last_run else None,
                    'run_count': task.run_count,
                    'success_count': task.success_count,
                    'error_count': task.error_count,
                    'average_duration': task.average_duration,
                    'created_at': task.created_at.isoformat()
                }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Erro ao salvar configuração: {e}")
    
    def load_configuration(self):
        """Carrega configuração das tarefas"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                for task_id, task_data in config.items():
                    task = OptimizationTask(
                        task_id=task_id,
                        name=task_data['name'],
                        task_type=task_data['task_type'],
                        schedule_type=ScheduleType(task_data['schedule_type']),
                        schedule_config=task_data['schedule_config'],
                        enabled=task_data['enabled']
                    )
                    
                    # Restaurar estatísticas
                    if task_data.get('last_run'):
                        task.last_run = datetime.fromisoformat(task_data['last_run'])
                    task.run_count = task_data.get('run_count', 0)
                    task.success_count = task_data.get('success_count', 0)
                    task.error_count = task_data.get('error_count', 0)
                    task.average_duration = task_data.get('average_duration', 0.0)
                    
                    if task_data.get('created_at'):
                        task.created_at = datetime.fromisoformat(task_data['created_at'])
                    
                    self.tasks[task_id] = task
                    
                    # Reagendar se habilitado
                    if task.enabled:
                        self._schedule_task(task)
                
                self.logger.info(f"Configuração carregada: {len(self.tasks)} tarefas")
            else:
                # Criar agendamentos padrão se não existe configuração
                self.create_default_schedules()
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração: {e}")
            # Criar agendamentos padrão em caso de erro
            self.create_default_schedules()
    
    def run_task_now(self, task_id):
        """Executa uma tarefa imediatamente"""
        if task_id in self.tasks:
            threading.Thread(target=self._run_task, args=(task_id,)).start()
            return True
        return False
    
    def is_running(self):
        """Verifica se o agendador está rodando"""
        return self.running
    
    def setup_default_tasks(self):
        """Configura tarefas padrão do sistema"""
        self.create_default_schedules()
        self.logger.info("Tarefas padrão configuradas")
    
    def get_scheduled_jobs(self):
        """Retorna lista de todas as tarefas agendadas"""
        jobs = []
        for task_id, task in self.tasks.items():
            jobs.append({
                'id': task_id,
                'name': task.name,
                'type': task.task_type,
                'schedule_type': task.schedule_type.value,
                'enabled': task.enabled,
                'last_run': task.last_run.isoformat() if task.last_run else None,
                'next_run': self._get_next_run_time(task),
                'run_count': task.run_count,
                'success_count': task.success_count,
                'error_count': task.error_count,
                'average_duration': task.average_duration
            })
        return jobs
    
    def _get_next_run_time(self, task):
        """Calcula próximo horário de execução de uma tarefa"""
        if not task.enabled:
            return None
        
        try:
            # Implementação simplificada - em produção seria mais complexa
            from datetime import datetime, timedelta
            
            now = datetime.now()
            config = task.schedule_config
            
            if task.schedule_type == ScheduleType.DAILY:
                time_str = config.get('time', '08:00')
                hour, minute = map(int, time_str.split(':'))
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if next_run <= now:
                    next_run += timedelta(days=1)
                return next_run.isoformat()
            
            elif task.schedule_type == ScheduleType.WEEKLY:
                # Implementação simplificada para semanal
                return (now + timedelta(days=7)).isoformat()
            
            elif task.schedule_type == ScheduleType.MONTHLY:
                # Implementação simplificada para mensal
                return (now + timedelta(days=30)).isoformat()
            
            return None
        except Exception:
            return None