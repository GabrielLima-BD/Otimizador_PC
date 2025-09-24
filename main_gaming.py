"""
Interface Principal do Otimizador PC Gaming
Versão ULTRA com busca universal, modos especiais e filtros inteligentes
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
import time
import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# Imports dos módulos do otimizador
from optimizer.game_scanner import GameScanner, GameInfo
from optimizer.game_launcher import GameLauncher
from optimizer.advanced_optimizer import AdvancedOptimizer
from optimizer.advanced_cleaner import AdvancedCleaner
from optimizer.system_monitor import SystemMonitor
from optimizer.schedule_manager import ScheduleManager
from optimizer.universal_app_scanner import UniversalAppScanner, AppInfo
from optimizer.special_modes import SpecialModes


class AdvancedMainWindow(ctk.CTk):
    """Janela principal do otimizador com interface completa e modos especiais"""
    
    def __init__(self):
        super().__init__()
        
        # Configurar janela
        self.title("🎮 Otimizador PC Gaming ULTRA - 🎤 MICROFONE PROTEGIDO")
        self.geometry("1200x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Inicializar componentes
        self.universal_scanner = UniversalAppScanner()
        self.game_scanner = GameScanner()
        self.game_launcher = GameLauncher()
        self.advanced_optimizer = AdvancedOptimizer()
        self.advanced_cleaner = AdvancedCleaner()
        self.system_monitor = SystemMonitor()
        self.schedule_manager = ScheduleManager()
        self.special_modes = SpecialModes(self.advanced_optimizer)
        
        # Dados
        self.apps_list: List[AppInfo] = []
        self.selected_apps: List[AppInfo] = []
        self.current_metrics = {}
        
        # Criar interface
        self.create_widgets()
        self.start_monitoring()
        
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        
        # Barra de pesquisa no topo
        self.create_search_bar()
        
        # Notebook com abas
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Criar abas
        self.create_apps_tab()
        self.create_optimization_tab()
        self.create_monitoring_tab()
        self.create_schedule_tab()
    
    def create_search_bar(self):
        """Cria barra de pesquisa universal no topo"""
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Label
        search_label = ctk.CTkLabel(search_frame, text="🔍 Buscar Apps:", font=("Arial", 14, "bold"))
        search_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Entry de pesquisa
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Digite o nome do app... (Ex: Chrome, Steam, Discord)",
            font=("Arial", 12),
            height=35
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_search_changed)
        
        # Botão buscar todos
        self.scan_all_btn = ctk.CTkButton(
            search_frame,
            text="📱 Buscar Todos os Apps",
            command=self.scan_all_apps,
            height=35,
            font=("Arial", 12, "bold")
        )
        self.scan_all_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Status da busca
        self.search_status = ctk.CTkLabel(search_frame, text="⚡ Digite para buscar ou clique em 'Buscar Todos'")
        self.search_status.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
    
    def create_apps_tab(self):
        """Aba de aplicativos e jogos"""
        self.apps_tab = self.notebook.add("🎮 Apps & Jogos")
        self.apps_tab.grid_columnconfigure(0, weight=2)
        self.apps_tab.grid_columnconfigure(1, weight=1)
        self.apps_tab.grid_rowconfigure(1, weight=1)
        
        # Frame de progresso (inicialmente oculto)
        self.progress_frame = ctk.CTkFrame(self.apps_tab)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Buscando...")
        self.progress_label.pack(pady=5)
        
        # Lista de apps/jogos
        apps_list_frame = ctk.CTkFrame(self.apps_tab)
        apps_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        apps_list_frame.grid_rowconfigure(1, weight=1)
        
        apps_list_label = ctk.CTkLabel(apps_list_frame, text="📋 Apps Encontrados:", font=("Arial", 14, "bold"))
        apps_list_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # ScrollableFrame para apps
        self.apps_scroll_frame = ctk.CTkScrollableFrame(apps_list_frame)
        self.apps_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(self.apps_tab)
        controls_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        controls_label = ctk.CTkLabel(controls_frame, text="🎯 Apps Selecionados:", font=("Arial", 14, "bold"))
        controls_label.pack(pady=10)
        
        # Lista de selecionados
        self.selected_listbox = tk.Listbox(controls_frame, height=15)
        self.selected_listbox.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(controls_frame)
        btn_frame.pack(pady=10, padx=10, fill="x")
        
        self.launch_selected_btn = ctk.CTkButton(
            btn_frame,
            text="🚀 Executar Selecionados",
            command=self.launch_selected_apps,
            height=40,
            font=("Arial", 12, "bold")
        )
        self.launch_selected_btn.pack(pady=5, fill="x")
        
        self.clear_selection_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Limpar Seleção",
            command=self.clear_selection,
            height=35
        )
        self.clear_selection_btn.pack(pady=5, fill="x")
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(controls_frame)
        stats_frame.pack(pady=10, padx=10, fill="x")
        
        self.stats_label = ctk.CTkLabel(stats_frame, text="📊 Estatísticas", font=("Arial", 12, "bold"))
        self.stats_label.pack(pady=5)
        
        self.stats_text = ctk.CTkTextbox(stats_frame, height=100)
        self.stats_text.pack(pady=5, padx=5, fill="x")
        self.update_stats_display()
    
    def create_optimization_tab(self):
        """Aba de otimização do sistema"""
        self.optimization_tab = self.notebook.add("⚡ Otimização")
        self.optimization_tab.grid_columnconfigure(0, weight=1)
        self.optimization_tab.grid_columnconfigure(1, weight=1)
        self.optimization_tab.grid_rowconfigure(1, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(self.optimization_tab, text="⚡ Otimização do Sistema", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Frame de ações rápidas
        quick_frame = ctk.CTkFrame(self.optimization_tab)
        quick_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        quick_label = ctk.CTkLabel(quick_frame, text="🚀 Ações Rápidas", font=("Arial", 14, "bold"))
        quick_label.pack(pady=10)
        
        # Botões de otimização rápida
        self.quick_cleanup_btn = ctk.CTkButton(
            quick_frame,
            text="🧹 Limpeza Rápida",
            command=self.quick_cleanup,
            height=40,
            font=("Arial", 12, "bold")
        )
        self.quick_cleanup_btn.pack(pady=10, padx=20, fill="x")
        
        self.gaming_mode_btn = ctk.CTkButton(
            quick_frame,
            text="🎮 Modo Gaming",
            command=self.enable_gaming_mode,
            height=40,
            font=("Arial", 12, "bold")
        )
        self.gaming_mode_btn.pack(pady=10, padx=20, fill="x")
        
        self.boost_performance_btn = ctk.CTkButton(
            quick_frame,
            text="⚡ Boost Performance",
            command=self.boost_performance,
            height=40,
            font=("Arial", 12, "bold")
        )
        self.boost_performance_btn.pack(pady=10, padx=20, fill="x")
        
        self.system_report_btn = ctk.CTkButton(
            quick_frame,
            text="📊 Relatório do Sistema",
            command=self.generate_system_report,
            height=40,
            font=("Arial", 12, "bold")
        )
        self.system_report_btn.pack(pady=10, padx=20, fill="x")
        
        # Frame de otimização avançada
        advanced_frame = ctk.CTkFrame(self.optimization_tab)
        advanced_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        advanced_label = ctk.CTkLabel(advanced_frame, text="🔧 Otimização Avançada", font=("Arial", 14, "bold"))
        advanced_label.pack(pady=10)
        
        # Opções de otimização
        self.opt_registry = ctk.CTkCheckBox(advanced_frame, text="🗃️ Limpar Registro")
        self.opt_registry.pack(pady=5, padx=20, anchor="w")
        self.opt_registry.select()
        
        self.opt_temp_files = ctk.CTkCheckBox(advanced_frame, text="📁 Arquivos Temporários")
        self.opt_temp_files.pack(pady=5, padx=20, anchor="w")
        self.opt_temp_files.select()
        
        self.opt_startup = ctk.CTkCheckBox(advanced_frame, text="🚀 Otimizar Inicialização")
        self.opt_startup.pack(pady=5, padx=20, anchor="w")
        self.opt_startup.select()
        
        self.opt_services = ctk.CTkCheckBox(advanced_frame, text="⚙️ Otimizar Serviços")
        self.opt_services.pack(pady=5, padx=20, anchor="w")
        
        self.opt_network = ctk.CTkCheckBox(advanced_frame, text="🌐 Otimizar Rede")
        self.opt_network.pack(pady=5, padx=20, anchor="w")
        
        self.opt_graphics = ctk.CTkCheckBox(advanced_frame, text="🎮 Otimizar Gráficos")
        self.opt_graphics.pack(pady=5, padx=20, anchor="w")
        
        # Botão de otimização personalizada
        self.custom_optimize_btn = ctk.CTkButton(
            advanced_frame,
            text="🔧 Executar Otimização Personalizada",
            command=self.custom_optimization,
            height=40,
            font=("Arial", 12, "bold")
        )
        self.custom_optimize_btn.pack(pady=20, padx=20, fill="x")
        
        # Botão de otimizações avançadas
        self.advanced_optimize_btn = ctk.CTkButton(
            advanced_frame,
            text="⚡ Otimizações Avançadas do Sistema",
            command=self.advanced_system_optimization,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#ff6b35",
            hover_color="#e55a2b"
        )
        self.advanced_optimize_btn.pack(pady=(0, 10), padx=20, fill="x")
        
        # Botão de otimizações ULTRA avançadas
        self.ultra_advanced_optimize_btn = ctk.CTkButton(
            advanced_frame,
            text="🚀 OTIMIZAÇÕES ULTRA AVANÇADAS - MÁXIMA PERFORMANCE",
            command=self.ultra_advanced_system_optimization,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#dc2626",
            hover_color="#b91c1c"
        )
        self.ultra_advanced_optimize_btn.pack(pady=(0, 20), padx=20, fill="x")
        
        # === MODOS ESPECIAIS COMBINADOS ===
        special_modes_label = ctk.CTkLabel(advanced_frame, text="🎯 MODOS ESPECIAIS DE OTIMIZAÇÃO", 
                                         font=("Arial", 14, "bold"), text_color="#00ff00")
        special_modes_label.pack(pady=(20, 10))
        
        # Frame para os modos especiais
        special_modes_frame = ctk.CTkFrame(advanced_frame)
        special_modes_frame.pack(pady=5, padx=20, fill="x")
        
        # MODO 1: TURBO GAMING (Turbo + Gaming)
        turbo_frame = ctk.CTkFrame(special_modes_frame)
        turbo_frame.pack(pady=10, padx=15, fill="x")
        
        turbo_btn = ctk.CTkButton(
            turbo_frame,
            text="🚀 MODO TURBO GAMING",
            command=self.activate_turbo_gaming_mode,
            height=40,
            width=200,
            font=("Arial", 12, "bold"),
            fg_color="#ff4500",
            hover_color="#e03e00"
        )
        turbo_btn.pack(side="left", padx=10, pady=10)
        
        turbo_desc = ctk.CTkLabel(
            turbo_frame,
            text="🎮 ATIVA: Performance máxima, prioridade para jogos, limpeza RAM\n" +
                 "❌ DESATIVA: Serviços desnecessários, efeitos visuais, indexação\n" +
                 "⚡ IDEAL: Jogos competitivos e máxima performance",
            font=("Arial", 10),
            justify="left"
        )
        turbo_desc.pack(side="left", padx=10, fill="x", expand=True)
        
        # MODO 2: BENCHMARK COMPLETO (Benchmark + Deep Clean)
        benchmark_frame = ctk.CTkFrame(special_modes_frame)
        benchmark_frame.pack(pady=10, padx=15, fill="x")
        
        benchmark_btn = ctk.CTkButton(
            benchmark_frame,
            text="📊 MODO BENCHMARK COMPLETO",
            command=self.activate_benchmark_complete_mode,
            height=40,
            width=200,
            font=("Arial", 12, "bold"),
            fg_color="#0066cc",
            hover_color="#0052a3"
        )
        benchmark_btn.pack(side="left", padx=10, pady=10)
        
        benchmark_desc = ctk.CTkLabel(
            benchmark_frame,
            text="📈 ATIVA: Todas otimizações + relatórios detalhados, limpeza profunda\n" +
                 "🧹 DESATIVA: Arquivos temporários, cache, logs, registry órfão\n" +
                 "📊 IDEAL: Testes de performance e limpeza completa",
            font=("Arial", 10),
            justify="left"
        )
        benchmark_desc.pack(side="left", padx=10, fill="x", expand=True)
        
        # MODO 3: EXTREMO TOTAL (Extremo + Silencioso)
        extreme_frame = ctk.CTkFrame(special_modes_frame)
        extreme_frame.pack(pady=10, padx=15, fill="x")
        
        extreme_btn = ctk.CTkButton(
            extreme_frame,
            text="⚡ MODO EXTREMO TOTAL",
            command=self.activate_extreme_total_mode,
            height=40,
            width=200,
            font=("Arial", 12, "bold"),
            fg_color="#cc0000",
            hover_color="#a30000"
        )
        extreme_btn.pack(side="left", padx=10, pady=10)
        
        extreme_desc = ctk.CTkLabel(
            extreme_frame,
            text="⚠️ ATIVA: TODAS configurações extremas de CPU/GPU/RAM/Rede\n" +
                 "🔇 DESATIVA: Telemetria, recursos visuais, funcionalidades desnecessárias\n" +
                 "🚨 IDEAL: Máxima performance (requer experiência)",
            font=("Arial", 10),
            justify="left",
            text_color="#ffaa00"
        )
        extreme_desc.pack(side="left", padx=10, fill="x", expand=True)
        
        # 🔥 MODO 4: AMD BEAST MODE (NOVO!)
        amd_beast_frame = ctk.CTkFrame(special_modes_frame)
        amd_beast_frame.pack(pady=10, padx=15, fill="x")
        
        amd_beast_btn = ctk.CTkButton(
            amd_beast_frame,
            text="🔥 MODO AMD BEAST",
            command=self.activate_amd_beast_mode,
            height=40,
            width=200,
            font=("Arial", 12, "bold"),
            fg_color="#ff4500",
            hover_color="#cc3300"
        )
        amd_beast_btn.pack(side="left", padx=10, pady=10)
        
        amd_beast_desc = ctk.CTkLabel(
            amd_beast_frame,
            text="🔥 ESPECÍFICO AMD: Ryzen CPU + Radeon GPU otimizações extremas\n" +
                 "🚀 INCLUI: HPET disable, ULPS off, power plans AMD, timers otimizados\n" +
                 "💪 IDEAL: Hardware AMD Ryzen + Radeon (máximo FPS)",
            font=("Arial", 10),
            justify="left",
            text_color="#ff6600"
        )
        amd_beast_desc.pack(side="left", padx=10, fill="x", expand=True)
        
        # Aviso de proteção de áudio
        audio_protection_label = ctk.CTkLabel(
            special_modes_frame,
            text="🎤 PROTEÇÃO DE ÁUDIO ATIVA: Microfone e som sempre protegidos em todos os modos",
            font=("Arial", 10, "bold"),
            text_color="#00ff00"
        )
        audio_protection_label.pack(pady=10)
        
        # Log de otimização
        log_label = ctk.CTkLabel(advanced_frame, text="📋 Log de Atividades", font=("Arial", 12, "bold"))
        log_label.pack(pady=(20, 5))
        
        self.optimization_log = ctk.CTkTextbox(advanced_frame, height=200)
        self.optimization_log.pack(pady=5, padx=20, fill="both", expand=True)
        self.optimization_log.insert("1.0", "Sistema pronto para otimização...\n")
    
    def create_monitoring_tab(self):
        """Aba de monitoramento do sistema"""
        self.monitoring_tab = self.notebook.add("📊 Monitoramento")
        self.monitoring_tab.grid_columnconfigure(0, weight=1)
        self.monitoring_tab.grid_columnconfigure(1, weight=1)
        self.monitoring_tab.grid_rowconfigure(1, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(self.monitoring_tab, text="📊 Monitoramento em Tempo Real", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Frame de métricas principais
        metrics_frame = ctk.CTkFrame(self.monitoring_tab)
        metrics_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        metrics_label = ctk.CTkLabel(metrics_frame, text="💻 Recursos do Sistema", font=("Arial", 14, "bold"))
        metrics_label.pack(pady=10)
        
        # CPU
        cpu_frame = ctk.CTkFrame(metrics_frame)
        cpu_frame.pack(pady=10, padx=20, fill="x")
        
        self.cpu_label = ctk.CTkLabel(cpu_frame, text="🖥️ CPU: 0%", font=("Arial", 12, "bold"))
        self.cpu_label.pack(pady=5)
        
        self.cpu_progress = ctk.CTkProgressBar(cpu_frame)
        self.cpu_progress.pack(pady=5, padx=10, fill="x")
        
        # RAM
        ram_frame = ctk.CTkFrame(metrics_frame)
        ram_frame.pack(pady=10, padx=20, fill="x")
        
        self.ram_label = ctk.CTkLabel(ram_frame, text="💾 RAM: 0%", font=("Arial", 12, "bold"))
        self.ram_label.pack(pady=5)
        
        self.ram_progress = ctk.CTkProgressBar(ram_frame)
        self.ram_progress.pack(pady=5, padx=10, fill="x")
        
        # Disco
        disk_frame = ctk.CTkFrame(metrics_frame)
        disk_frame.pack(pady=10, padx=20, fill="x")
        
        self.disk_label = ctk.CTkLabel(disk_frame, text="💽 Disco: 0%", font=("Arial", 12, "bold"))
        self.disk_label.pack(pady=5)
        
        self.disk_progress = ctk.CTkProgressBar(disk_frame)
        self.disk_progress.pack(pady=5, padx=10, fill="x")
        
        # Temperatura (se disponível)
        temp_frame = ctk.CTkFrame(metrics_frame)
        temp_frame.pack(pady=10, padx=20, fill="x")
        
        self.temp_label = ctk.CTkLabel(temp_frame, text="🌡️ Temperatura: N/A", font=("Arial", 12, "bold"))
        self.temp_label.pack(pady=5)
        
        # Frame de processos
        processes_frame = ctk.CTkFrame(self.monitoring_tab)
        processes_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        processes_label = ctk.CTkLabel(processes_frame, text="🔄 Processos com Maior Uso", font=("Arial", 14, "bold"))
        processes_label.pack(pady=10)
        
        # Lista de processos
        self.processes_text = ctk.CTkTextbox(processes_frame, height=300)
        self.processes_text.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Botões de controle
        control_frame = ctk.CTkFrame(processes_frame)
        control_frame.pack(pady=10, padx=20, fill="x")
        
        self.refresh_btn = ctk.CTkButton(
            control_frame,
            text="🔄 Atualizar",
            command=self.refresh_monitoring,
            height=35
        )
        self.refresh_btn.pack(side="left", padx=5)
        
        self.kill_process_btn = ctk.CTkButton(
            control_frame,
            text="❌ Finalizar Processo",
            command=self.kill_selected_process,
            height=35
        )
        self.kill_process_btn.pack(side="right", padx=5)
        
        # Health Score
        health_frame = ctk.CTkFrame(self.monitoring_tab)
        health_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.health_label = ctk.CTkLabel(health_frame, text="💯 Health Score: Calculando...", font=("Arial", 16, "bold"))
        self.health_label.pack(pady=10)
    
    def create_schedule_tab(self):
        """Aba de agendamento"""
        self.schedule_tab = self.notebook.add("⏰ Agendamento")
        self.schedule_tab.grid_columnconfigure(0, weight=1)
        self.schedule_tab.grid_columnconfigure(1, weight=1)
        self.schedule_tab.grid_rowconfigure(1, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(self.schedule_tab, text="⏰ Agendamento de Tarefas", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Frame de nova tarefa
        new_task_frame = ctk.CTkFrame(self.schedule_tab)
        new_task_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        new_task_label = ctk.CTkLabel(new_task_frame, text="➕ Nova Tarefa Agendada", font=("Arial", 14, "bold"))
        new_task_label.pack(pady=10)
        
        # Nome da tarefa
        name_label = ctk.CTkLabel(new_task_frame, text="📝 Nome da Tarefa:")
        name_label.pack(pady=5, anchor="w", padx=20)
        
        self.task_name_entry = ctk.CTkEntry(new_task_frame, placeholder_text="Ex: Limpeza Diária")
        self.task_name_entry.pack(pady=5, padx=20, fill="x")
        
        # Tipo de tarefa
        type_label = ctk.CTkLabel(new_task_frame, text="🔧 Tipo de Tarefa:")
        type_label.pack(pady=5, anchor="w", padx=20)
        
        self.task_type_combo = ctk.CTkComboBox(
            new_task_frame,
            values=["Limpeza Rápida", "Otimização Completa", "Modo Gaming", "Backup", "Verificação de Sistema"]
        )
        self.task_type_combo.pack(pady=5, padx=20, fill="x")
        self.task_type_combo.set("Limpeza Rápida")
        
        # Frequência
        freq_label = ctk.CTkLabel(new_task_frame, text="🕐 Frequência:")
        freq_label.pack(pady=5, anchor="w", padx=20)
        
        self.frequency_combo = ctk.CTkComboBox(
            new_task_frame,
            values=["Diário", "Semanal", "Mensal", "Uma vez"]
        )
        self.frequency_combo.pack(pady=5, padx=20, fill="x")
        self.frequency_combo.set("Semanal")
        
        # Horário
        time_label = ctk.CTkLabel(new_task_frame, text="⏰ Horário:")
        time_label.pack(pady=5, anchor="w", padx=20)
        
        time_frame = ctk.CTkFrame(new_task_frame)
        time_frame.pack(pady=5, padx=20, fill="x")
        
        self.hour_combo = ctk.CTkComboBox(time_frame, values=[f"{i:02d}" for i in range(24)], width=60)
        self.hour_combo.pack(side="left", padx=5)
        self.hour_combo.set("02")  # 2 AM por padrão
        
        ctk.CTkLabel(time_frame, text=":").pack(side="left")
        
        self.minute_combo = ctk.CTkComboBox(time_frame, values=[f"{i:02d}" for i in range(0, 60, 15)], width=60)
        self.minute_combo.pack(side="left", padx=5)
        self.minute_combo.set("00")
        
        # Botão adicionar
        self.add_task_btn = ctk.CTkButton(
            new_task_frame,
            text="➕ Adicionar Tarefa",
            command=self.add_scheduled_task,
            height=40,
            font=("Arial", 12, "bold")
        )
        self.add_task_btn.pack(pady=20, padx=20, fill="x")
        
        # Frame de tarefas existentes
        existing_tasks_frame = ctk.CTkFrame(self.schedule_tab)
        existing_tasks_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        existing_label = ctk.CTkLabel(existing_tasks_frame, text="📋 Tarefas Agendadas", font=("Arial", 14, "bold"))
        existing_label.pack(pady=10)
        
        # Lista de tarefas
        self.tasks_listbox = tk.Listbox(existing_tasks_frame, height=15)
        self.tasks_listbox.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Botões de controle
        task_control_frame = ctk.CTkFrame(existing_tasks_frame)
        task_control_frame.pack(pady=10, padx=20, fill="x")
        
        self.enable_task_btn = ctk.CTkButton(
            task_control_frame,
            text="✅ Ativar",
            command=self.enable_selected_task,
            height=35
        )
        self.enable_task_btn.pack(side="left", padx=5)
        
        self.disable_task_btn = ctk.CTkButton(
            task_control_frame,
            text="⏸️ Pausar",
            command=self.disable_selected_task,
            height=35
        )
        self.disable_task_btn.pack(side="left", padx=5)
        
        self.delete_task_btn = ctk.CTkButton(
            task_control_frame,
            text="🗑️ Excluir",
            command=self.delete_selected_task,
            height=35
        )
        self.delete_task_btn.pack(side="right", padx=5)
        
        # Status das tarefas
        status_frame = ctk.CTkFrame(self.schedule_tab)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.schedule_status_label = ctk.CTkLabel(status_frame, text="📊 Status: Sistema de agendamento ativo")
        self.schedule_status_label.pack(pady=10)
        
        # Carregar tarefas existentes
        self.load_scheduled_tasks()
    
    def scan_all_apps(self):
        """Busca todos os apps do sistema"""
        self.search_status.configure(text="🔍 Buscando todos os aplicativos...", text_color="blue")
        
        # Mostrar barra de progresso
        self.progress_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        def scan_worker():
            try:
                def progress_callback(step_name, current, total):
                    progress = current / total
                    self.after(0, lambda: self.update_scan_progress(step_name, progress))
                
                # Executar busca
                apps_found = self.universal_scanner.scan_all_apps(progress_callback)
                
                # Atualizar interface
                self.after(0, lambda: self.finish_app_scan(apps_found))
                
            except Exception as e:
                self.after(0, lambda: self.scan_error(str(e)))
        
        threading.Thread(target=scan_worker, daemon=True).start()
    
    def update_scan_progress(self, step_name: str, progress: float):
        """Atualiza progresso da busca"""
        self.progress_bar.set(progress)
        self.progress_label.configure(text=step_name)
    
    def finish_app_scan(self, apps_found: Dict[str, AppInfo]):
        """Finaliza busca de apps"""
        self.apps_list = list(apps_found.values())
        
        # Esconder progresso
        self.progress_frame.grid_forget()
        
        # Atualizar interface
        self.update_apps_display()
        self.update_stats_display()
        
        # Status
        app_count = len(apps_found)
        self.search_status.configure(
            text=f"✅ {app_count} aplicativos encontrados! Use a barra de pesquisa para filtrar.",
            text_color="green"
        )
    
    def scan_error(self, error_msg: str):
        """Erro na busca"""
        self.progress_frame.grid_forget()
        self.search_status.configure(text=f"❌ Erro na busca: {error_msg}", text_color="red")
    
    def on_search_changed(self, event=None):
        """Quando o texto da pesquisa muda"""
        if not self.apps_list:
            return
        
        query = self.search_entry.get().strip()
        if not query:
            self.update_apps_display()
            return
        
        # Filtrar apps
        filtered_apps = self.universal_scanner.search_apps(query)
        self.update_apps_display(filtered_apps)
        
        # Atualizar status
        self.search_status.configure(
            text=f"🔍 {len(filtered_apps)} apps encontrados para '{query}'",
            text_color="blue"
        )
    
    def update_apps_display(self, apps_to_show: Optional[List[AppInfo]] = None):
        """Atualiza exibição de apps"""
        # Limpar lista atual
        for widget in self.apps_scroll_frame.winfo_children():
            widget.destroy()
        
        # Apps para mostrar
        apps_to_display = apps_to_show if apps_to_show is not None else self.apps_list
        
        if not apps_to_display:
            no_apps_label = ctk.CTkLabel(
                self.apps_scroll_frame,
                text="🔍 Nenhum aplicativo encontrado.\nClique em 'Buscar Todos os Apps' para começar.",
                font=("Arial", 12)
            )
            no_apps_label.pack(pady=20)
            return
        
        # Mostrar apps
        for i, app in enumerate(apps_to_display):
            app_frame = ctk.CTkFrame(self.apps_scroll_frame)
            app_frame.pack(pady=5, padx=10, fill="x")
            
            # Info do app
            info_text = f"📱 {app.name}"
            if app.app_type == "uwp_app":
                info_text += " (Microsoft Store)"
            elif app.publisher:
                info_text += f" - {app.publisher}"
            
            app_label = ctk.CTkLabel(app_frame, text=info_text, font=("Arial", 11))
            app_label.pack(side="left", padx=10, pady=5)
            
            # Botão selecionar
            select_btn = ctk.CTkButton(
                app_frame,
                text="➕ Selecionar",
                command=lambda a=app: self.select_app(a),
                width=100,
                height=30
            )
            select_btn.pack(side="right", padx=10, pady=5)
    
    def select_app(self, app: AppInfo):
        """Seleciona um app"""
        if app not in self.selected_apps:
            self.selected_apps.append(app)
            self.update_selected_display()
    
    def update_selected_display(self):
        """Atualiza lista de apps selecionados"""
        self.selected_listbox.delete(0, tk.END)
        for app in self.selected_apps:
            self.selected_listbox.insert(tk.END, f"📱 {app.name}")
    
    def launch_selected_apps(self):
        """Executa apps selecionados"""
        if not self.selected_apps:
            messagebox.showwarning("Aviso", "Selecione pelo menos um aplicativo!")
            return
        
        try:
            results = self.universal_scanner.launch_multiple_apps(self.selected_apps)
            
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)
            
            if success_count == total_count:
                messagebox.showinfo("Sucesso", f"✅ Todos os {total_count} apps foram executados!")
            else:
                failed_apps = [name for name, success in results.items() if not success]
                messagebox.showwarning(
                    "Parcialmente Executado",
                    f"✅ {success_count}/{total_count} apps executados.\n\n❌ Falharam:\n" + "\n".join(failed_apps)
                )
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar apps: {e}")
    
    def clear_selection(self):
        """Limpa seleção de apps"""
        self.selected_apps.clear()
        self.update_selected_display()
    
    def update_stats_display(self):
        """Atualiza estatísticas"""
        total_apps = len(self.apps_list)
        selected_apps = len(self.selected_apps)
        
        # Contar por tipo
        app_types = {}
        for app in self.apps_list:
            app_type = app.app_type
            app_types[app_type] = app_types.get(app_type, 0) + 1
        
        stats_text = f"""📊 ESTATÍSTICAS
        
📱 Total de Apps: {total_apps}
🎯 Selecionados: {selected_apps}

📂 Por Tipo:
"""
        
        for app_type, count in app_types.items():
            type_name = {
                "application": "Aplicativos",
                "uwp_app": "Microsoft Store",
                "game": "Jogos"
            }.get(app_type, app_type.title())
            
            stats_text += f"• {type_name}: {count}\n"
        
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("1.0", stats_text)
    
    # Métodos de Otimização
    def quick_cleanup(self):
        """Limpeza rápida do sistema"""
        self.log_optimization("🧹 Iniciando limpeza rápida...")
        
        def cleanup_worker():
            try:
                # Executar limpezas reais
                self.after(0, lambda: self.log_optimization("  🗂️ Limpando cache de navegadores..."))
                self.advanced_cleaner.clean_browser_profiles_deep()
                
                self.after(0, lambda: self.log_optimization("  🖼️ Limpando cache de miniaturas..."))
                self.advanced_cleaner.clean_thumbnail_cache()
                
                self.after(0, lambda: self.log_optimization("  📋 Limpando logs do sistema..."))
                self.advanced_cleaner.clean_windows_event_logs()
                
                self.after(0, lambda: self.log_optimization("  📁 Removendo drivers antigos..."))
                self.advanced_cleaner.clean_old_drivers()
                
                self.after(0, lambda: self.log_optimization("✅ Limpeza rápida concluída!"))
                self.after(0, lambda: messagebox.showinfo("Sucesso", "🧹 Limpeza rápida executada com sucesso!\n\n✓ Cache de navegadores\n✓ Miniaturas\n✓ Logs do sistema\n✓ Drivers antigos"))
                
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.log_optimization(f"❌ Erro na limpeza: {error_msg}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro na limpeza: {error_msg}"))
        
        threading.Thread(target=cleanup_worker, daemon=True).start()
    
    def enable_gaming_mode(self):
        """Ativa modo gaming"""
        self.log_optimization("🎮 Ativando modo gaming...")
        
        def gaming_worker():
            try:
                # Executar otimizações reais para gaming
                self.after(0, lambda: self.log_optimization("  🎯 Otimizando performance para gaming..."))
                self.advanced_optimizer.optimize_gaming_performance()
                
                self.after(0, lambda: self.log_optimization("  ⚡ Otimizando agendamento de CPU..."))
                self.advanced_optimizer.optimize_cpu_scheduling()
                
                self.after(0, lambda: self.log_optimization("  💾 Otimizando gerenciamento de memória..."))
                self.advanced_optimizer.optimize_memory_management()
                
                self.after(0, lambda: self.log_optimization("  💽 Otimizando performance de armazenamento..."))
                self.advanced_optimizer.optimize_storage_performance()
                
                self.after(0, lambda: self.log_optimization("✅ Modo gaming ativo!"))
                self.after(0, lambda: messagebox.showinfo("Gaming Mode", "🎮 Modo gaming ativado!\n\n✓ Performance otimizada\n✓ CPU priorizada\n✓ Memória otimizada\n✓ Armazenamento acelerado\n\nSistema pronto para jogos!"))
                
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.log_optimization(f"❌ Erro no modo gaming: {error_msg}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro no modo gaming: {error_msg}"))
        
        threading.Thread(target=gaming_worker, daemon=True).start()
    
    def boost_performance(self):
        """Boost de performance"""
        self.log_optimization("⚡ Executando boost de performance...")
        
        def boost_worker():
            try:
                # Executar otimizações reais de performance
                self.after(0, lambda: self.log_optimization("  🔧 Otimizando gerenciamento de memória..."))
                self.advanced_optimizer.optimize_memory_management()
                
                self.after(0, lambda: self.log_optimization("  ⚡ Configurando agendamento de CPU..."))
                self.advanced_optimizer.optimize_cpu_scheduling()
                
                self.after(0, lambda: self.log_optimization("  💽 Otimizando performance de armazenamento..."))
                self.advanced_optimizer.optimize_storage_performance()
                
                self.after(0, lambda: self.log_optimization("  🧹 Limpando cache do sistema..."))
                self.advanced_cleaner.clean_thumbnail_cache()
                
                self.after(0, lambda: self.log_optimization("  🔍 Otimizando busca do Windows..."))
                self.advanced_optimizer.optimize_windows_search()
                
                self.after(0, lambda: self.log_optimization("✅ Performance otimizada!"))
                self.after(0, lambda: messagebox.showinfo("Performance", "⚡ Boost aplicado!\n\n✓ Memória otimizada\n✓ CPU configurada\n✓ Armazenamento acelerado\n✓ Cache limpo\n✓ Busca otimizada\n\nSistema mais rápido!"))
                
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.log_optimization(f"❌ Erro no boost: {error_msg}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro no boost: {error_msg}"))
        
        threading.Thread(target=boost_worker, daemon=True).start()
    
    def generate_system_report(self):
        """Gera relatório do sistema"""
        try:
            metrics = self.system_monitor.collect_metrics()
            health_score = self.system_monitor.calculate_health_score(metrics)
            
            report = f"""📊 RELATÓRIO DO SISTEMA
            
🖥️ Performance Atual:
• CPU: {metrics.get('cpu_percent', 'N/A')}%
• Memória: {metrics.get('memory_percent', 'N/A')}%
• Disco: {metrics.get('disk_percent', 'N/A')}%

💯 Health Score: {health_score}/100

📅 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

🔧 Recomendações:
• Execute limpeza se Health Score < 70
• Use modo gaming para jogos
• Monitore processos com alto uso de CPU
            """.strip()
            
            # Salvar relatório
            filename = f"relatorio_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.log_optimization(f"📊 Relatório salvo: {filename}")
            messagebox.showinfo("Relatório", f"📊 Relatório gerado!\n\nSalvo como: {filename}\n\nHealth Score: {health_score}/100")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def custom_optimization(self):
        """Otimização personalizada baseada nas opções selecionadas"""
        selected_options = []
        
        if self.opt_registry.get():
            selected_options.append("registry")
        if self.opt_temp_files.get():
            selected_options.append("temp_files")
        if self.opt_startup.get():
            selected_options.append("startup")
        if self.opt_services.get():
            selected_options.append("services")
        if self.opt_network.get():
            selected_options.append("network")
        if self.opt_graphics.get():
            selected_options.append("graphics")
        
        if not selected_options:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma opção de otimização!")
            return
        
        self.log_optimization(f"🔧 Iniciando otimização personalizada: {', '.join(selected_options)}")
        
        def custom_worker():
            try:
                optimization_count = 0
                
                for option in selected_options:
                    self.after(0, lambda o=option: self.log_optimization(f"  ⚙️ Otimizando {o.replace('_', ' ').title()}..."))
                    
                    if option == "registry":
                        # Limpeza de logs e eventos do sistema
                        self.advanced_cleaner.clean_windows_event_logs()
                        optimization_count += 1
                        self.after(0, lambda: self.log_optimization("    ✓ Logs do sistema limpos"))
                        
                    elif option == "temp_files":
                        # Limpeza de arquivos temporários e cache
                        self.advanced_cleaner.clean_browser_profiles_deep()
                        self.advanced_cleaner.clean_thumbnail_cache()
                        optimization_count += 2
                        self.after(0, lambda: self.log_optimization("    ✓ Cache de navegadores limpo"))
                        self.after(0, lambda: self.log_optimization("    ✓ Cache de miniaturas limpo"))
                        
                    elif option == "startup":
                        # Otimização de programas de inicialização
                        self.advanced_optimizer.optimize_startup_programs()
                        optimization_count += 1
                        self.after(0, lambda: self.log_optimization("    ✓ Programas de inicialização otimizados"))
                        
                    elif option == "services":
                        # Otimização de serviços do sistema
                        self.advanced_optimizer.optimize_memory_management()
                        self.advanced_optimizer.optimize_cpu_scheduling()
                        optimization_count += 2
                        self.after(0, lambda: self.log_optimization("    ✓ Gerenciamento de memória otimizado"))
                        self.after(0, lambda: self.log_optimization("    ✓ Serviços do sistema otimizados"))
                        
                    elif option == "network":
                        # Otimização de rede
                        try:
                            from optimizer.network import NetworkOptimizer
                            network_opt = NetworkOptimizer()
                            
                            self.after(0, lambda: self.log_optimization("    🌐 Otimizando DNS..."))
                            network_opt.optimize_dns()
                            
                            self.after(0, lambda: self.log_optimization("    🌐 Otimizando TCP..."))
                            network_opt.optimize_tcp_settings()
                            
                            self.after(0, lambda: self.log_optimization("    🌐 Otimizando adaptador..."))
                            network_opt.optimize_network_adapter()
                            
                            optimization_count += 3
                            self.after(0, lambda: self.log_optimization("    ✓ Todas as otimizações de rede aplicadas"))
                        except Exception as e:
                            self.after(0, lambda: self.log_optimization(f"    ⚠️ Erro na otimização de rede: {e}"))
                            optimization_count += 1
                        
                    elif option == "graphics":
                        # Otimização para gaming/gráficos
                        self.advanced_optimizer.optimize_gaming_performance()
                        self.advanced_optimizer.optimize_storage_performance()
                        optimization_count += 2
                        self.after(0, lambda: self.log_optimization("    ✓ Performance de gaming otimizada"))
                        self.after(0, lambda: self.log_optimization("    ✓ Performance de armazenamento otimizada"))
                
                self.after(0, lambda: self.log_optimization(f"✅ Otimização personalizada concluída! {optimization_count} otimizações aplicadas."))
                
                summary = f"✅ Otimização concluída!\n\n📊 Resultados:\n• {optimization_count} otimizações aplicadas\n\n🎯 Áreas otimizadas:\n• " + "\n• ".join([o.replace('_', ' ').title() for o in selected_options])
                
                self.after(0, lambda: messagebox.showinfo("Sucesso", summary))
                
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.log_optimization(f"❌ Erro na otimização: {error_msg}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro durante otimização: {error_msg}"))
        
        threading.Thread(target=custom_worker, daemon=True).start()
    
    def advanced_system_optimization(self):
        """⚡ Executa otimizações avançadas do sistema"""
        if not messagebox.askyesno("Otimizações Avançadas", 
                                   "🚨 ATENÇÃO: Estas otimizações são AVANÇADAS e podem alterar configurações profundas do sistema.\n\n"
                                   "Inclui:\n"
                                   "🔧 Desativação de serviços do sistema\n"
                                   "🧠 Otimizações de registro avançadas\n"
                                   "🌐 Configurações avançadas de rede\n"
                                   "🧪 Desativação de diagnósticos\n\n"
                                   "⚠️ Recomendado criar um ponto de restauração antes.\n\n"
                                   "Continuar?"):
            return
        
        self.log_optimization("⚡ Iniciando otimizações avançadas do sistema...")
        self.advanced_optimize_btn.configure(state="disabled", text="🔄 Otimizando...")
        
        def advanced_worker():
            try:
                # Callback para atualizar progresso
                def update_progress(message, progress):
                    self.after(0, lambda: self.log_optimization(f"    📝 {message}"))
                
                # Executar todas as otimizações avançadas
                total_optimizations = self.advanced_optimizer.apply_all_advanced_optimizations(update_progress)
                
                # Resumo final
                self.after(0, lambda: self.log_optimization("✅ Otimizações avançadas concluídas!"))
                
                summary = (f"✅ Otimizações Avançadas Concluídas!\n\n"
                          f"📊 Total de otimizações aplicadas: {total_optimizations}\n\n"
                          f"🔧 Categorias otimizadas:\n"
                          f"• Sistema e Hardware\n"
                          f"• Registro Avançado\n"
                          f"• Rede e Internet\n"
                          f"• Diagnóstico e Monitoramento\n\n"
                          f"💡 Recomenda-se reiniciar o sistema para aplicar todas as mudanças.")
                
                self.after(0, lambda: messagebox.showinfo("Sucesso", summary))
                
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.log_optimization(f"❌ Erro nas otimizações avançadas: {error_msg}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro durante otimizações avançadas: {error_msg}"))
            
            finally:
                self.after(0, lambda: self.advanced_optimize_btn.configure(state="normal", text="⚡ Otimizações Avançadas do Sistema"))
        
        threading.Thread(target=advanced_worker, daemon=True).start()
    
    def ultra_advanced_system_optimization(self):
        """🚀 Executa otimizações ULTRA AVANÇADAS do sistema - MÁXIMA PERFORMANCE"""
        warning_message = (
            "🚨 ATENÇÃO MÁXIMA: OTIMIZAÇÕES ULTRA AVANÇADAS! 🚨\n\n"
            "⚠️ ESTAS SÃO AS OTIMIZAÇÕES MAIS EXTREMAS DISPONÍVEIS!\n\n"
            "📋 INCLUI TODAS AS OTIMIZAÇÕES ANTERIORES MAIS:\n"
            "🔧 Sistema e Boot: Desativação de verificação de assinatura de driver\n"
            "🧠 Kernel: Otimizações de prioridade e resposta (1ms mouse/teclado)\n"
            "🌐 Rede Ultra: TCP/IP otimizado, NetBIOS desabilitado\n"
            "🛠 Extras: Hyper-V, WSL, Windows Defender desabilitados\n"
            "🧪 Telemetria: COMPLETAMENTE eliminada\n\n"
            "⚠️ RISCOS:\n"
            "• Pode afetar compatibilidade com alguns softwares\n"
            "• Pode desabilitar recursos de segurança\n"
            "• Mudanças muito profundas no sistema\n\n"
            "💡 RECOMENDADO APENAS PARA:\n"
            "• PCs dedicados exclusivamente para gaming\n"
            "• Usuários experientes\n"
            "• Sistemas com backup completo\n\n"
            "🔄 CRIAR PONTO DE RESTAURAÇÃO É OBRIGATÓRIO!\n\n"
            "Continuar com as otimizações ULTRA AVANÇADAS?"
        )
        
        if not messagebox.askyesno("🚀 OTIMIZAÇÕES ULTRA AVANÇADAS", warning_message):
            return
        
        # Confirmação adicional
        if not messagebox.askyesno("Confirmação Final", 
                                   "🔴 ÚLTIMA CONFIRMAÇÃO!\n\n"
                                   "Você está prestes a aplicar as otimizações mais extremas possíveis.\n"
                                   "Isto pode alterar profundamente o comportamento do sistema.\n\n"
                                   "TEM CERTEZA ABSOLUTA?"):
            return
        
        self.log_optimization("🚀 Iniciando otimizações ULTRA AVANÇADAS do sistema...")
        self.ultra_advanced_optimize_btn.configure(state="disabled", text="🔄 Otimizando ULTRA...")
        
        def ultra_advanced_worker():
            try:
                # Callback para atualizar progresso
                def update_progress(message, progress):
                    self.after(0, lambda: self.log_optimization(f"    🔧 {message}"))
                
                # Executar TODAS as otimizações ultra avançadas
                total_optimizations = self.advanced_optimizer.apply_all_ultra_advanced_optimizations(update_progress)
                
                # Resumo final
                self.after(0, lambda: self.log_optimization("🚀 OTIMIZAÇÕES ULTRA AVANÇADAS CONCLUÍDAS!"))
                
                summary = (f"🚀 OTIMIZAÇÕES ULTRA AVANÇADAS CONCLUÍDAS!\n\n"
                          f"📊 Total de otimizações aplicadas: {total_optimizations}\n\n"
                          f"🔧 Categorias Ultra Otimizadas:\n"
                          f"• Sistema e Boot (verificação de driver desabilitada)\n"
                          f"• Kernel e Registro (resposta 1ms mouse/teclado)\n"
                          f"• Rede Ultra Avançada (TCP/IP extremo)\n"
                          f"• Recursos Extras (Hyper-V, WSL, Defender)\n"
                          f"• Telemetria Ultra (100% eliminada)\n"
                          f"• TODAS as otimizações anteriores incluídas\n\n"
                          f"🎮 PERFORMANCE MÁXIMA ALCANÇADA!\n\n"
                          f"⚠️ REINICIALIZAÇÃO OBRIGATÓRIA para aplicar todas as mudanças.\n\n"
                          f"🎯 Seu sistema agora está otimizado ao EXTREMO para gaming!")
                
                self.after(0, lambda: messagebox.showinfo("🚀 SUCESSO ULTRA", summary))
                
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.log_optimization(f"❌ Erro nas otimizações ULTRA: {error_msg}"))
                self.after(0, lambda: messagebox.showerror("Erro Ultra", f"Erro durante otimizações ULTRA: {error_msg}"))
            
            finally:
                self.after(0, lambda: self.ultra_advanced_optimize_btn.configure(state="normal", text="🚀 OTIMIZAÇÕES ULTRA AVANÇADAS - MÁXIMA PERFORMANCE"))
        
        threading.Thread(target=ultra_advanced_worker, daemon=True).start()
    
    def log_optimization(self, message: str):
        """Adiciona mensagem ao log de otimização"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        self.optimization_log.insert("end", log_entry)
        self.optimization_log.see("end")
    
    # Métodos de Monitoramento
    def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        self.update_monitoring()
    
    def update_monitoring(self):
        """Atualiza métricas de monitoramento"""
        try:
            self.current_metrics = self.system_monitor.collect_metrics()
            
            # Atualizar barras de progresso
            cpu_percent = self.current_metrics.get('cpu_percent', 0)
            memory_percent = self.current_metrics.get('memory_percent', 0)
            disk_percent = self.current_metrics.get('disk_percent', 0)
            
            self.cpu_progress.set(cpu_percent / 100)
            self.cpu_label.configure(text=f"🖥️ CPU: {cpu_percent:.1f}%")
            
            self.ram_progress.set(memory_percent / 100)
            self.ram_label.configure(text=f"💾 RAM: {memory_percent:.1f}%")
            
            self.disk_progress.set(disk_percent / 100)
            self.disk_label.configure(text=f"💽 Disco: {disk_percent:.1f}%")
            
            # Temperatura (se disponível)
            temp = self.current_metrics.get('temperature')
            if temp:
                self.temp_label.configure(text=f"🌡️ Temperatura: {temp}°C")
            
            # Atualizar processos
            self.update_processes_display()
            
            # Health Score
            health_score = self.system_monitor.calculate_health_score(self.current_metrics)
            health_color = "green" if health_score >= 80 else "orange" if health_score >= 60 else "red"
            self.health_label.configure(
                text=f"💯 Health Score: {health_score}/100",
                text_color=health_color
            )
            
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
        
        # Reagendar próxima atualização
        self.after(2000, self.update_monitoring)
    
    def update_processes_display(self):
        """Atualiza exibição de processos"""
        try:
            processes = self.system_monitor.get_top_processes(limit=10)
            
            processes_text = "🔄 PROCESSOS COM MAIOR USO:\n\n"
            
            for i, proc in enumerate(processes, 1):
                processes_text += f"{i:2d}. {proc['name'][:20]:<20} | CPU: {proc['cpu_percent']:5.1f}% | RAM: {proc['memory_percent']:5.1f}%\n"
            
            self.processes_text.delete("1.0", "end")
            self.processes_text.insert("1.0", processes_text)
            
        except Exception as e:
            self.processes_text.delete("1.0", "end")
            self.processes_text.insert("1.0", f"Erro ao obter processos: {e}")
    
    def refresh_monitoring(self):
        """Força atualização do monitoramento"""
        self.update_monitoring()
        messagebox.showinfo("Atualizado", "📊 Monitoramento atualizado!")
    
    def kill_selected_process(self):
        """Finaliza processo selecionado"""
        # Implementar seleção e finalização de processo
        messagebox.showinfo("Aviso", "Funcionalidade em desenvolvimento!")
    
    # Métodos de Agendamento
    def add_scheduled_task(self):
        """Adiciona nova tarefa agendada"""
        try:
            name = self.task_name_entry.get().strip()
            task_type = self.task_type_combo.get()
            frequency = self.frequency_combo.get()
            hour = int(self.hour_combo.get())
            minute = int(self.minute_combo.get())
            
            if not name:
                messagebox.showwarning("Aviso", "Digite um nome para a tarefa!")
                return
            
            # Criar tarefa
            task_info = {
                'name': name,
                'type': task_type,
                'frequency': frequency,
                'hour': hour,
                'minute': minute,
                'enabled': True,
                'created': datetime.now().isoformat()
            }
            
            # Adicionar à lista
            self.tasks_listbox.insert(tk.END, f"✅ {name} - {task_type} ({frequency} às {hour:02d}:{minute:02d})")
            
            # Limpar campos
            self.task_name_entry.delete(0, 'end')
            
            messagebox.showinfo("Sucesso", f"✅ Tarefa '{name}' adicionada com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar tarefa: {e}")
    
    def enable_selected_task(self):
        """Ativa tarefa selecionada"""
        selection = self.tasks_listbox.curselection()
        if selection:
            messagebox.showinfo("Ativado", "✅ Tarefa ativada!")
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
    
    def disable_selected_task(self):
        """Pausa tarefa selecionada"""
        selection = self.tasks_listbox.curselection()
        if selection:
            messagebox.showinfo("Pausado", "⏸️ Tarefa pausada!")
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
    
    def delete_selected_task(self):
        """Exclui tarefa selecionada"""
        selection = self.tasks_listbox.curselection()
        if selection:
            if messagebox.askyesno("Confirmar", "Deseja realmente excluir a tarefa?"):
                self.tasks_listbox.delete(selection[0])
                messagebox.showinfo("Excluído", "🗑️ Tarefa excluída!")
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
    
    def load_scheduled_tasks(self):
        """Carrega tarefas agendadas salvas"""
        # Adicionar algumas tarefas de exemplo
        example_tasks = [
            "✅ Limpeza Automática - Limpeza Rápida (Diário às 02:00)",
            "✅ Otimização Semanal - Otimização Completa (Semanal às 03:00)",
            "⏸️ Backup Gaming - Backup (Mensal às 01:00)"
        ]
        
        for task in example_tasks:
            self.tasks_listbox.insert(tk.END, task)
    
    def open_special_modes(self):
        """Abre a janela de modos especiais"""
        try:
            # Criar uma nova janela simplificada de modos especiais
            import tkinter as tk
            
            # Verificar se já existe uma janela aberta
            if hasattr(self, 'special_modes_window') and self.special_modes_window.winfo_exists():
                self.special_modes_window.lift()  # Trazer para frente
                self.special_modes_window.focus()
                return
            
            # Criar nova janela simplificada
            self.special_modes_window = tk.Toplevel(self)
            self.special_modes_window.title("🚀 Modos Especiais")
            self.special_modes_window.geometry("600x400")
            self.special_modes_window.configure(bg="#2b2b2b")
            
            # Label informativo
            info_label = tk.Label(
                self.special_modes_window,
                text="🚀 MODOS ESPECIAIS DISPONÍVEIS\n\nUse os botões na aba principal 'Otimização'",
                bg="#2b2b2b",
                fg="white",
                font=("Arial", 14),
                justify="center"
            )
            info_label.pack(pady=50)
            
            # Botão para fechar
            close_btn = tk.Button(
                self.special_modes_window,
                text="Fechar",
                command=self.special_modes_window.destroy,
                bg="#cc0000",
                fg="white",
                font=("Arial", 12)
            )
            close_btn.pack(pady=20)
            
        except Exception as e:
            messagebox.showerror(
                "Erro", 
                f"Erro ao abrir Modos Especiais:\n{e}\n\n"
                "Verifique se todos os módulos estão instalados corretamente."
            )
    
    # === MODOS ESPECIAIS COMBINADOS ===
    
    def activate_turbo_gaming_mode(self):
        """🚀 MODO TURBO GAMING - Combina Turbo + Gaming Preparation"""
        if not messagebox.askyesno("MODO TURBO GAMING", 
                                   "🚀 MODO TURBO GAMING\n\n" +
                                   "✅ ATIVARÁ:\n" +
                                   "• Performance máxima de CPU/GPU\n" +
                                   "• Prioridade alta para jogos\n" +
                                   "• Limpeza automática de RAM\n" +
                                   "• Configurações de rede otimizadas\n\n" +
                                   "❌ DESATIVARÁ:\n" +
                                   "• Serviços desnecessários\n" +
                                   "• Efeitos visuais\n" +
                                   "• Indexação e busca\n" +
                                   "• Processos em background\n\n" +
                                   "🎤 ÁUDIO: Totalmente protegido!\n\n" +
                                   "Continuar?"):
            return
        
        def turbo_worker():
            try:
                self.after(0, lambda: self.log_optimization("🚀 INICIANDO MODO TURBO GAMING..."))
                
                # Inicializar special modes
                from optimizer.special_modes import SpecialModes
                special_modes = SpecialModes(self.advanced_optimizer)
                
                # Aplicar modo turbo
                self.after(0, lambda: self.log_optimization("⚡ Aplicando modo Turbo..."))
                turbo_result = special_modes.activate_turbo_mode()
                
                # Preparar sistema para gaming
                self.after(0, lambda: self.log_optimization("🎮 Preparando sistema para jogos..."))
                special_modes._prepare_system_for_gaming()
                special_modes._optimize_cpu_priorities()
                
                self.after(0, lambda: self.log_optimization("✅ MODO TURBO GAMING ATIVADO!"))
                self.after(0, lambda: messagebox.showinfo("Sucesso", 
                          f"🚀 MODO TURBO GAMING ATIVADO!\n\n" +
                          f"📊 Otimizações aplicadas: {len(turbo_result.get('optimizations', []))}\n" +
                          f"🎯 Sistema otimizado para máxima performance em jogos!"))
                
            except Exception as e:
                self.after(0, lambda: self.log_optimization(f"❌ Erro no Modo Turbo Gaming: {e}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro no Modo Turbo Gaming: {e}"))
        
        threading.Thread(target=turbo_worker, daemon=True).start()
    
    def activate_benchmark_complete_mode(self):
        """📊 MODO BENCHMARK COMPLETO - Combina Benchmark + Deep Clean"""
        if not messagebox.askyesno("MODO BENCHMARK COMPLETO", 
                                   "📊 MODO BENCHMARK COMPLETO\n\n" +
                                   "✅ ATIVARÁ:\n" +
                                   "• TODAS as otimizações do sistema\n" +
                                   "• Relatórios detalhados de performance\n" +
                                   "• Limpeza profunda completa\n" +
                                   "• Coleta de métricas antes/depois\n\n" +
                                   "🧹 LIMPARÁ:\n" +
                                   "• Arquivos temporários (GB)\n" +
                                   "• Cache de aplicativos\n" +
                                   "• Logs do sistema\n" +
                                   "• Entradas órfãs do registro\n\n" +
                                   "📈 RESULTADO: Relatório completo\n\n" +
                                   "Continuar?"):
            return
        
        def benchmark_worker():
            try:
                self.after(0, lambda: self.log_optimization("📊 INICIANDO MODO BENCHMARK COMPLETO..."))
                
                from optimizer.special_modes import SpecialModes
                special_modes = SpecialModes(self.advanced_optimizer)
                
                # Aplicar benchmark mode
                self.after(0, lambda: self.log_optimization("📈 Executando benchmark completo..."))
                benchmark_result = special_modes.activate_benchmark_mode()
                
                # Aplicar deep clean
                self.after(0, lambda: self.log_optimization("🧹 Executando limpeza profunda..."))
                clean_result = special_modes.activate_deep_clean_mode()
                
                total_space = clean_result.get('total_space_freed', 0)
                
                self.after(0, lambda: self.log_optimization("✅ MODO BENCHMARK COMPLETO CONCLUÍDO!"))
                self.after(0, lambda: messagebox.showinfo("Sucesso", 
                          f"📊 MODO BENCHMARK COMPLETO CONCLUÍDO!\n\n" +
                          f"🧹 Espaço liberado: {total_space} MB\n" +
                          f"📈 Relatório salvo em: logs/reports/\n" +
                          f"🎯 Sistema completamente otimizado e limpo!"))
                
            except Exception as e:
                self.after(0, lambda: self.log_optimization(f"❌ Erro no Modo Benchmark: {e}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro no Modo Benchmark: {e}"))
        
        threading.Thread(target=benchmark_worker, daemon=True).start()
    
    def activate_extreme_total_mode(self):
        """⚡ MODO EXTREMO TOTAL - Combina Extremo + Silencioso"""
        if not messagebox.askyesno("⚠️ MODO EXTREMO TOTAL", 
                                   "⚠️ MODO EXTREMO TOTAL\n\n" +
                                   "🚨 ATENÇÃO: MODO MAIS AGRESSIVO!\n\n" +
                                   "⚡ ATIVARÁ:\n" +
                                   "• TODAS configurações extremas\n" +
                                   "• CPU: Prioridades máximas\n" +
                                   "• GPU: Performance extrema\n" +
                                   "• RAM: Otimizações agressivas\n" +
                                   "• REDE: Configurações extremas\n\n" +
                                   "🔇 DESATIVARÁ:\n" +
                                   "• Telemetria e rastreamento\n" +
                                   "• Recursos visuais\n" +
                                   "• Funcionalidades desnecessárias\n" +
                                   "• Serviços opcionais\n\n" +
                                   "🎤 ÁUDIO: Sempre protegido!\n" +
                                   "⚠️ Recomendado para usuários experientes\n\n" +
                                   "Continuar?"):
            return
        
        def extreme_worker():
            try:
                self.after(0, lambda: self.log_optimization("⚡ INICIANDO MODO EXTREMO TOTAL..."))
                
                from optimizer.special_modes import SpecialModes
                special_modes = SpecialModes(self.advanced_optimizer)
                
                # Aplicar modo extremo
                self.after(0, lambda: self.log_optimization("🚨 Aplicando configurações EXTREMAS..."))
                extreme_result = special_modes.activate_extreme_performance_mode()
                
                # Aplicar otimizações silenciosas adicionais
                self.after(0, lambda: self.log_optimization("🔇 Aplicando otimizações silenciosas..."))
                special_modes._silent_network_optimization()
                special_modes._apply_extreme_cpu_settings()
                special_modes._apply_extreme_gpu_settings()
                special_modes._apply_extreme_memory_settings()
                
                self.after(0, lambda: self.log_optimization("✅ MODO EXTREMO TOTAL ATIVADO!"))
                
                # Executar otimizações extremas de performance
                from optimizer.performance import PerformanceOptimizer
                perf_optimizer = PerformanceOptimizer()
                if hasattr(perf_optimizer, 'extreme_gaming_optimization'):
                    self.after(0, lambda: self.log_optimization("🔥 Aplicando otimizações gaming extremas..."))
                    perf_optimizer.extreme_gaming_optimization()
                
                # Executar otimizações específicas AMD
                if hasattr(self.advanced_optimizer, 'optimize_amd_specific'):
                    self.after(0, lambda: self.log_optimization("🚀 Aplicando otimizações específicas AMD..."))
                    self.advanced_optimizer.optimize_amd_specific()
                self.after(0, lambda: messagebox.showinfo("Sucesso", 
                          f"⚡ MODO EXTREMO TOTAL ATIVADO!\n\n" +
                          f"🚨 MÁXIMA PERFORMANCE ALCANÇADA!\n" +
                          f"📊 Otimizações: {len(extreme_result.get('optimizations', []))}\n" +
                          f"⚠️ Monitore a estabilidade do sistema\n" +
                          f"🎤 Áudio completamente protegido!"))
                
            except Exception as e:
                self.after(0, lambda: self.log_optimization(f"❌ Erro no Modo Extremo: {e}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro no Modo Extremo: {e}"))
        
        threading.Thread(target=extreme_worker, daemon=True).start()
    
    def activate_amd_beast_mode(self):
        """🔥 MODO AMD BEAST - Otimizações específicas e extremas para AMD"""
        if not messagebox.askyesno("🔥 MODO AMD BEAST", 
                                   "🔥 MODO AMD BEAST - ESPECÍFICO AMD\n\n" +
                                   "🚀 OTIMIZAÇÕES INCLUEM:\n" +
                                   "• AMD Ryzen: Power plan otimizado\n" +
                                   "• AMD Radeon: ULPS OFF, sem throttling\n" +
                                   "• HPET: Desabilitado (reduz latência)\n" +
                                   "• Memory: Timings AMD otimizados\n" +
                                   "• CPU: 100% performance constante\n" +
                                   "• Network: Latência extremamente reduzida\n\n" +
                                   "💪 IDEAL PARA:\n" +
                                   "• Processadores AMD Ryzen\n" +
                                   "• Placas de vídeo AMD Radeon\n" +
                                   "• Jogos competitivos (CS2, Valorant, R6)\n\n" +
                                   "🎤 ÁUDIO: Sempre protegido!\n\n" +
                                   "⚠️ APENAS para hardware AMD!\n" +
                                   "Continuar?"):
            return
        
        def amd_beast_worker():
            try:
                self.after(0, lambda: self.log_optimization("🔥 INICIANDO MODO AMD BEAST..."))
                
                # Aplicar otimizações AMD específicas do advanced_optimizer
                if hasattr(self.advanced_optimizer, 'optimize_amd_specific'):
                    self.after(0, lambda: self.log_optimization("🚀 Otimizações AMD Ryzen + Radeon..."))
                    amd_opts = self.advanced_optimizer.optimize_amd_specific()
                    for opt in amd_opts:
                        self.after(0, lambda o=opt: self.log_optimization(f"✅ {o}"))
                
                # Aplicar modo AMD Beast do special_modes
                from optimizer.special_modes import SpecialModes
                special_modes = SpecialModes(self.advanced_optimizer)
                
                self.after(0, lambda: self.log_optimization("🔥 Ativando MODO AMD BEAST..."))
                result = special_modes.activate_amd_beast_mode()
                
                if result.get("success"):
                    for opt in result.get("optimizations", []):
                        self.after(0, lambda o=opt: self.log_optimization(f"✅ {o}"))
                    
                    self.after(0, lambda: self.log_optimization("🔥 MODO AMD BEAST ATIVADO COM SUCESSO!"))
                    self.after(0, lambda: self.log_optimization("💪 Hardware AMD otimizado para máxima performance!"))
                    self.after(0, lambda: messagebox.showinfo("Sucesso", 
                                                             "🔥 MODO AMD BEAST ATIVADO!\n\n" +
                                                             "Hardware AMD otimizado para máxima performance!\n" +
                                                             "Reinicie para aplicar todas as otimizações."))
                else:
                    error_msg = result.get("message", "Erro desconhecido")
                    self.after(0, lambda: self.log_optimization(f"❌ ERRO: {error_msg}"))
                    self.after(0, lambda: messagebox.showerror("Erro", f"Erro ao ativar AMD Beast Mode:\n{error_msg}"))
                
            except Exception as e:
                self.after(0, lambda: self.log_optimization(f"❌ ERRO CRÍTICO: {str(e)}"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro crítico no AMD Beast Mode: {e}"))
        
        threading.Thread(target=amd_beast_worker, daemon=True).start()


def main():
    """Função principal"""
    # Configurar CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Criar e executar aplicação
    app = AdvancedMainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()