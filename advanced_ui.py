import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import logging
import os
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as mplstyle
from collections import deque
import time

from optimizer.cleaner import SystemCleaner
from optimizer.performance import PerformanceOptimizer
from optimizer.network import NetworkOptimizer
from optimizer.registry import RegistryOptimizer
from optimizer.utils import Utils
from optimizer.hardware_detector import HardwareDetector
from optimizer.advanced_cleaner import AdvancedCleaner
from optimizer.advanced_optimizer import AdvancedOptimizer
from optimizer.system_monitor import SystemMonitor
from optimizer.schedule_manager import ScheduleManager, ScheduleType

# Configurar matplotlib para tema escuro
mplstyle.use('dark_background')
plt.style.use('dark_background')

class AdvancedOptimizerUI:
    """Interface gráfica avançada para o otimizador Windows"""
    
    def __init__(self):
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.root = ctk.CTk()
        self.root.title("🚀 Otimizador Windows 10 Pro - Versão Avançada")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Variáveis de controle
        self.is_optimizing = False
        self.optimization_thread = None
        self.current_tab = "home"
        
        # Instâncias dos otimizadores
        self.cleaner = SystemCleaner()
        self.performance = PerformanceOptimizer()
        self.network = NetworkOptimizer()
        self.registry = RegistryOptimizer()
        self.hardware_detector = HardwareDetector()
        self.advanced_cleaner = AdvancedCleaner()
        self.advanced_optimizer = AdvancedOptimizer()
        self.system_monitor = SystemMonitor()
        self.schedule_manager = ScheduleManager()
        
        # Dados do sistema
        self.hardware_info = None
        self.optimization_profile = None
        
        # Setup da interface
        self.setup_ui()
        
        # Configuração de logging
        self.logger = Utils.setup_logging()
        
        # Detectar hardware na inicialização
        self.detect_hardware()
        
        # Configurar callbacks do agendador
        self.setup_scheduler_callbacks()
        
        # Verifica se é admin
        if not Utils.is_admin():
            self.show_admin_warning()
    
    def setup_ui(self):
        """Configura toda a interface gráfica avançada"""
        
        # Frame principal com sidebar
        self.setup_sidebar()
        self.setup_main_content()
        
        # Inicializar com a aba Home
        self.show_home_tab()
    
    def setup_sidebar(self):
        """Configura sidebar com navegação"""
        
        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        
        # Logo e título
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🚀 Otimizador Pro", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(pady=(20, 10))
        
        # Status do sistema
        self.system_status_frame = ctk.CTkFrame(self.sidebar_frame)
        self.system_status_frame.pack(fill="x", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.system_status_frame,
            text="Status do Sistema",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(pady=5)
        
        self.health_score_label = ctk.CTkLabel(
            self.system_status_frame,
            text="Carregando...",
            font=ctk.CTkFont(size=12)
        )
        self.health_score_label.pack(pady=2)
        
        # Botões de navegação
        nav_buttons = [
            ("🏠 Início", "home"),
            ("🧹 Limpeza", "cleanup"),
            ("⚡ Performance", "performance"),
            ("🌐 Rede", "network"),
            ("📊 Monitoramento", "monitoring"),
            ("⏰ Agendamento", "scheduling"),
            ("🔧 Configurações", "settings")
        ]
        
        self.nav_buttons = {}
        for text, tab_id in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                width=180,
                height=40,
                command=lambda t=tab_id: self.switch_tab(t)
            )
            btn.pack(pady=5, padx=10)
            self.nav_buttons[tab_id] = btn
        
        # Informações do hardware
        self.hardware_frame = ctk.CTkFrame(self.sidebar_frame)
        self.hardware_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        self.hardware_label = ctk.CTkLabel(
            self.hardware_frame,
            text="Hardware",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.hardware_label.pack(pady=5)
        
        self.hardware_info_label = ctk.CTkLabel(
            self.hardware_frame,
            text="Detectando...",
            font=ctk.CTkFont(size=10),
            wraplength=180
        )
        self.hardware_info_label.pack(pady=2)
    
    def setup_main_content(self):
        """Configura área principal de conteúdo"""
        
        self.main_content = ctk.CTkFrame(self.root)
        self.main_content.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
        
        # Container para as diferentes abas
        self.tab_container = ctk.CTkFrame(self.main_content)
        self.tab_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    def switch_tab(self, tab_id):
        """Muda para uma aba específica"""
        
        # Limpar conteúdo atual
        for widget in self.tab_container.winfo_children():
            widget.destroy()
        
        # Atualizar botão ativo
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == tab_id:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        self.current_tab = tab_id
        
        # Mostrar aba correspondente
        if tab_id == "home":
            self.show_home_tab()
        elif tab_id == "cleanup":
            self.show_cleanup_tab()
        elif tab_id == "performance":
            self.show_performance_tab()
        elif tab_id == "network":
            self.show_network_tab()
        elif tab_id == "monitoring":
            self.show_monitoring_tab()
        elif tab_id == "scheduling":
            self.show_scheduling_tab()
        elif tab_id == "settings":
            self.show_settings_tab()
    
    def show_home_tab(self):
        """Mostra aba inicial com resumo do sistema"""
        
        # Título
        title = ctk.CTkLabel(
            self.tab_container,
            text="🏠 Painel Principal",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Frame principal dividido em colunas
        content_frame = ctk.CTkFrame(self.tab_container)
        content_frame.pack(fill="both", expand=True)
        
        # Coluna esquerda - Resumo do sistema
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Informações do sistema
        system_info_frame = ctk.CTkFrame(left_frame)
        system_info_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            system_info_frame,
            text="📊 Informações do Sistema",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.system_info_text = ctk.CTkTextbox(system_info_frame, height=200)
        self.system_info_text.pack(fill="x", padx=10, pady=(0, 10))
        
        # Otimização rápida
        quick_opt_frame = ctk.CTkFrame(left_frame)
        quick_opt_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            quick_opt_frame,
            text="⚡ Otimização Rápida",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        quick_buttons_frame = ctk.CTkFrame(quick_opt_frame)
        quick_buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            quick_buttons_frame,
            text="🧹 Limpeza Rápida",
            height=40,
            command=self.quick_cleanup
        ).pack(side="left", padx=(0, 5), fill="x", expand=True)
        
        ctk.CTkButton(
            quick_buttons_frame,
            text="⚡ Otimização Básica",
            height=40,
            command=self.quick_optimization
        ).pack(side="right", padx=(5, 0), fill="x", expand=True)
        
        # Coluna direita - Gráficos e monitoramento
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Gráfico de uso do sistema
        chart_frame = ctk.CTkFrame(right_frame)
        chart_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        ctk.CTkLabel(
            chart_frame,
            text="📈 Uso do Sistema",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Container para o gráfico
        self.chart_container = ctk.CTkFrame(chart_frame)
        self.chart_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Próximas tarefas agendadas
        schedule_frame = ctk.CTkFrame(right_frame)
        schedule_frame.pack(fill="x")
        
        ctk.CTkLabel(
            schedule_frame,
            text="⏰ Próximas Tarefas",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.next_tasks_text = ctk.CTkTextbox(schedule_frame, height=100)
        self.next_tasks_text.pack(fill="x", padx=10, pady=(0, 10))
        
        # Inicializar dados
        self.update_home_data()
        self.create_system_chart()
    
    def show_cleanup_tab(self):
        """Mostra aba de limpeza avançada"""
        
        # Título
        title = ctk.CTkLabel(
            self.tab_container,
            text="🧹 Limpeza Avançada",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Notebook para diferentes tipos de limpeza
        notebook = ttk.Notebook(self.tab_container)
        notebook.pack(fill="both", expand=True)
        
        # Aba de limpeza básica
        basic_frame = ctk.CTkFrame(notebook)
        notebook.add(basic_frame, text="Limpeza Básica")
        
        self.setup_basic_cleanup(basic_frame)
        
        # Aba de limpeza avançada
        advanced_frame = ctk.CTkFrame(notebook)
        notebook.add(advanced_frame, text="Limpeza Profunda")
        
        self.setup_advanced_cleanup(advanced_frame)
        
        # Aba de duplicatas
        duplicate_frame = ctk.CTkFrame(notebook)
        notebook.add(duplicate_frame, text="Arquivos Duplicados")
        
        self.setup_duplicate_cleanup(duplicate_frame)
    
    def setup_basic_cleanup(self, parent):
        """Configura limpeza básica"""
        
        # Opções de limpeza
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        self.cleanup_vars = {}
        cleanup_options = [
            ("temp_files", "🗂️ Arquivos temporários"),
            ("recycle_bin", "🗑️ Lixeira"),
            ("browser_cache", "🌐 Cache dos navegadores"),
            ("system_cache", "💾 Cache do sistema"),
            ("log_files", "📄 Arquivos de log"),
            ("thumbnails", "🖼️ Cache de miniaturas")
        ]
        
        for var_name, text in cleanup_options:
            var = ctk.BooleanVar(value=True)
            self.cleanup_vars[var_name] = var
            
            checkbox = ctk.CTkCheckBox(options_frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=5)
        
        # Botões de ação
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Analisar",
            command=self.analyze_cleanup,
            height=40
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            button_frame,
            text="🧹 Limpar",
            command=self.perform_cleanup,
            height=40
        ).pack(side="left", padx=5)
        
        # Resultado
        self.cleanup_result = ctk.CTkTextbox(parent, height=200)
        self.cleanup_result.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_advanced_cleanup(self, parent):
        """Configura limpeza avançada"""
        
        # Opções avançadas
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        self.advanced_cleanup_vars = {}
        advanced_options = [
            ("old_drivers", "🔧 Drivers antigos"),
            ("event_logs", "📋 Logs de eventos do Windows"),
            ("restore_points", "💾 Pontos de restauração antigos"),
            ("browser_profiles", "🌐 Limpeza profunda de navegadores"),
            ("thumbnail_cache", "🖼️ Cache de thumbnails do sistema")
        ]
        
        for var_name, text in advanced_options:
            var = ctk.BooleanVar(value=False)
            self.advanced_cleanup_vars[var_name] = var
            
            checkbox = ctk.CTkCheckBox(options_frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=5)
        
        # Aviso
        warning_label = ctk.CTkLabel(
            options_frame,
            text="⚠️ Atenção: Estas operações são mais agressivas e podem levar mais tempo",
            font=ctk.CTkFont(size=12),
            text_color="orange"
        )
        warning_label.pack(pady=10)
        
        # Botões
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Analisar Limpeza Avançada",
            command=self.analyze_advanced_cleanup,
            height=40
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            button_frame,
            text="🧹 Executar Limpeza Avançada",
            command=self.perform_advanced_cleanup,
            height=40
        ).pack(side="left", padx=5)
        
        # Resultado
        self.advanced_cleanup_result = ctk.CTkTextbox(parent, height=200)
        self.advanced_cleanup_result.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_duplicate_cleanup(self, parent):
        """Configura limpeza de duplicatas"""
        
        # Seleção de diretórios
        dir_frame = ctk.CTkFrame(parent)
        dir_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            dir_frame,
            text="📁 Diretórios para busca:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.search_dirs = ctk.CTkTextbox(dir_frame, height=80)
        self.search_dirs.pack(fill="x", padx=10, pady=5)
        
        # Diretórios padrão
        default_dirs = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Videos")
        ]
        self.search_dirs.insert("0.0", "\n".join(default_dirs))
        
        # Botões
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Buscar Duplicatas",
            command=self.find_duplicates,
            height=40
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            button_frame,
            text="🗑️ Remover Duplicatas",
            command=self.remove_duplicates,
            height=40
        ).pack(side="left", padx=5)
        
        # Lista de duplicatas
        self.duplicate_tree = ttk.Treeview(
            parent,
            columns=("Original", "Duplicata", "Tamanho"),
            show="headings"
        )
        self.duplicate_tree.heading("Original", text="Arquivo Original")
        self.duplicate_tree.heading("Duplicata", text="Arquivo Duplicado")
        self.duplicate_tree.heading("Tamanho", text="Tamanho")
        self.duplicate_tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_performance_tab(self):
        """Mostra aba de otimização de performance"""
        
        title = ctk.CTkLabel(
            self.tab_container,
            text="⚡ Otimização de Performance",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Notebook para diferentes otimizações
        notebook = ttk.Notebook(self.tab_container)
        notebook.pack(fill="both", expand=True)
        
        # Aba de otimização básica
        basic_perf_frame = ctk.CTkFrame(notebook)
        notebook.add(basic_perf_frame, text="Otimização Básica")
        self.setup_basic_performance(basic_perf_frame)
        
        # Aba de otimização avançada
        advanced_perf_frame = ctk.CTkFrame(notebook)
        notebook.add(advanced_perf_frame, text="Otimização Avançada")
        self.setup_advanced_performance(advanced_perf_frame)
        
        # Aba de perfil de hardware
        hardware_frame = ctk.CTkFrame(notebook)
        notebook.add(hardware_frame, text="Perfil de Hardware")
        self.setup_hardware_profile(hardware_frame)
    
    def setup_basic_performance(self, parent):
        """Configura otimização básica de performance"""
        
        # Opções de otimização
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        self.perf_vars = {}
        perf_options = [
            ("disable_services", "🛑 Desabilitar serviços desnecessários"),
            ("visual_effects", "🎨 Otimizar efeitos visuais"),
            ("power_plan", "⚡ Configurar plano de energia"),
            ("startup_programs", "🚀 Otimizar programas de inicialização"),
            ("system_responsiveness", "⚡ Melhorar responsividade do sistema")
        ]
        
        for var_name, text in perf_options:
            var = ctk.BooleanVar(value=True)
            self.perf_vars[var_name] = var
            
            checkbox = ctk.CTkCheckBox(options_frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=5)
        
        # Botões
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Analisar Sistema",
            command=self.analyze_performance,
            height=40
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            button_frame,
            text="⚡ Otimizar",
            command=self.optimize_performance,
            height=40
        ).pack(side="left", padx=5)
        
        # Resultado
        self.perf_result = ctk.CTkTextbox(parent, height=200)
        self.perf_result.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_advanced_performance(self, parent):
        """Configura otimização avançada de performance"""
        
        # Opções avançadas
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        self.advanced_perf_vars = {}
        advanced_perf_options = [
            ("memory_management", "🧠 Otimização de memória"),
            ("cpu_scheduling", "🔄 Agendamento de CPU"),
            ("storage_performance", "💾 Performance de armazenamento"),
            ("gaming_optimization", "🎮 Otimizações para jogos"),
            ("windows_search", "🔍 Otimização do Windows Search")
        ]
        
        for var_name, text in advanced_perf_options:
            var = ctk.BooleanVar(value=False)
            self.advanced_perf_vars[var_name] = var
            
            checkbox = ctk.CTkCheckBox(options_frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=5)
        
        # Botões
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="⚡ Aplicar Otimizações Avançadas",
            command=self.apply_advanced_optimizations,
            height=40
        ).pack()
        
        # Resultado
        self.advanced_perf_result = ctk.CTkTextbox(parent, height=200)
        self.advanced_perf_result.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_hardware_profile(self, parent):
        """Configura perfil baseado no hardware"""
        
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="🔧 Informações do Hardware",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.hardware_profile_text = ctk.CTkTextbox(info_frame, height=300)
        self.hardware_profile_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão para detectar hardware
        ctk.CTkButton(
            info_frame,
            text="🔍 Detectar Hardware",
            command=self.detect_hardware,
            height=40
        ).pack(pady=10)
        
        # Botão para aplicar perfil recomendado
        ctk.CTkButton(
            info_frame,
            text="⚡ Aplicar Perfil Recomendado",
            command=self.apply_hardware_profile,
            height=40
        ).pack(pady=5)
    
    def show_network_tab(self):
        """Mostra aba de otimização de rede"""
        
        title = ctk.CTkLabel(
            self.tab_container,
            text="🌐 Otimização de Rede",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Opções de rede
        options_frame = ctk.CTkFrame(self.tab_container)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        self.network_vars = {}
        network_options = [
            ("dns_optimization", "🌐 Otimizar servidores DNS"),
            ("tcp_optimization", "🔧 Otimizar configurações TCP"),
            ("qos_removal", "📊 Remover limitações QoS"),
            ("network_adapter", "📡 Otimizar adaptador de rede")
        ]
        
        for var_name, text in network_options:
            var = ctk.BooleanVar(value=True)
            self.network_vars[var_name] = var
            
            checkbox = ctk.CTkCheckBox(options_frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=5)
        
        # Teste de velocidade
        speed_frame = ctk.CTkFrame(self.tab_container)
        speed_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            speed_frame,
            text="📊 Teste de Velocidade",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.speed_test_result = ctk.CTkLabel(speed_frame, text="Clique em 'Testar Velocidade' para começar")
        self.speed_test_result.pack(pady=5)
        
        # Botões
        button_frame = ctk.CTkFrame(self.tab_container)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Testar Velocidade",
            command=self.test_network_speed,
            height=40
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            button_frame,
            text="🌐 Otimizar Rede",
            command=self.optimize_network,
            height=40
        ).pack(side="left", padx=5)
        
        # Resultado
        self.network_result = ctk.CTkTextbox(self.tab_container, height=200)
        self.network_result.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_monitoring_tab(self):
        """Mostra aba de monitoramento do sistema"""
        
        title = ctk.CTkLabel(
            self.tab_container,
            text="📊 Monitoramento do Sistema",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Controles do monitoramento
        control_frame = ctk.CTkFrame(self.tab_container)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            control_frame,
            text="▶️ Iniciar Monitoramento",
            command=self.start_monitoring,
            height=40
        ).pack(side="left", padx=(10, 5))
        
        ctk.CTkButton(
            control_frame,
            text="⏹️ Parar Monitoramento",
            command=self.stop_monitoring,
            height=40
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            control_frame,
            text="📄 Exportar Relatório",
            command=self.export_monitoring_report,
            height=40
        ).pack(side="right", padx=(5, 10))
        
        # Status do monitoramento
        self.monitoring_status = ctk.CTkLabel(
            control_frame,
            text="Monitoramento parado",
            font=ctk.CTkFont(size=12)
        )
        self.monitoring_status.pack(pady=10)
        
        # Gráficos em tempo real
        charts_frame = ctk.CTkFrame(self.tab_container)
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Container para gráficos
        self.monitoring_charts = ctk.CTkFrame(charts_frame)
        self.monitoring_charts.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Alertas
        alerts_frame = ctk.CTkFrame(self.tab_container)
        alerts_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            alerts_frame,
            text="🚨 Alertas do Sistema",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        
        self.alerts_text = ctk.CTkTextbox(alerts_frame, height=100)
        self.alerts_text.pack(fill="x", padx=10, pady=(0, 10))
    
    def show_scheduling_tab(self):
        """Mostra aba de agendamento de tarefas"""
        
        title = ctk.CTkLabel(
            self.tab_container,
            text="⏰ Agendamento de Tarefas",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Controles do agendador
        control_frame = ctk.CTkFrame(self.tab_container)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            control_frame,
            text="▶️ Iniciar Agendador",
            command=self.start_scheduler,
            height=40
        ).pack(side="left", padx=(10, 5))
        
        ctk.CTkButton(
            control_frame,
            text="⏹️ Parar Agendador",
            command=self.stop_scheduler,
            height=40
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            control_frame,
            text="➕ Nova Tarefa",
            command=self.create_new_task,
            height=40
        ).pack(side="right", padx=(5, 10))
        
        # Lista de tarefas agendadas
        tasks_frame = ctk.CTkFrame(self.tab_container)
        tasks_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            tasks_frame,
            text="📅 Tarefas Agendadas",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Tabela de tarefas
        self.tasks_tree = ttk.Treeview(
            tasks_frame,
            columns=("Nome", "Tipo", "Próxima Execução", "Status", "Última Execução"),
            show="headings"
        )
        self.tasks_tree.heading("Nome", text="Nome da Tarefa")
        self.tasks_tree.heading("Tipo", text="Tipo")
        self.tasks_tree.heading("Próxima Execução", text="Próxima Execução")
        self.tasks_tree.heading("Status", text="Status")
        self.tasks_tree.heading("Última Execução", text="Última Execução")
        self.tasks_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Atualizar lista de tarefas
        self.update_tasks_list()
    
    def show_settings_tab(self):
        """Mostra aba de configurações"""
        
        title = ctk.CTkLabel(
            self.tab_container,
            text="🔧 Configurações",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Notebook para diferentes configurações
        notebook = ttk.Notebook(self.tab_container)
        notebook.pack(fill="both", expand=True)
        
        # Aba de configurações gerais
        general_frame = ctk.CTkFrame(notebook)
        notebook.add(general_frame, text="Geral")
        self.setup_general_settings(general_frame)
        
        # Aba de configurações de monitoramento
        monitoring_settings_frame = ctk.CTkFrame(notebook)
        notebook.add(monitoring_settings_frame, text="Monitoramento")
        self.setup_monitoring_settings(monitoring_settings_frame)
        
        # Aba de backup e restauração
        backup_frame = ctk.CTkFrame(notebook)
        notebook.add(backup_frame, text="Backup e Restauração")
        self.setup_backup_settings(backup_frame)
    
    def setup_general_settings(self, parent):
        """Configura configurações gerais"""
        
        # Auto-start
        autostart_frame = ctk.CTkFrame(parent)
        autostart_frame.pack(fill="x", padx=10, pady=10)
        
        self.autostart_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            autostart_frame,
            text="🚀 Iniciar com o Windows",
            variable=self.autostart_var
        ).pack(anchor="w", padx=10, pady=10)
        
        # Tema
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            theme_frame,
            text="🎨 Tema da Interface:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.theme_var = ctk.StringVar(value="dark")
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            command=self.change_theme
        )
        theme_menu.pack(anchor="w", padx=10, pady=5)
        
        # Nível de log
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            log_frame,
            text="📄 Nível de Log:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.log_level_var = ctk.StringVar(value="INFO")
        log_menu = ctk.CTkOptionMenu(
            log_frame,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            variable=self.log_level_var
        )
        log_menu.pack(anchor="w", padx=10, pady=5)
        
        # Botão salvar
        ctk.CTkButton(
            parent,
            text="💾 Salvar Configurações",
            command=self.save_settings,
            height=40
        ).pack(pady=20)
    
    def setup_monitoring_settings(self, parent):
        """Configura configurações de monitoramento"""
        
        # Limiares de alerta
        thresholds_frame = ctk.CTkFrame(parent)
        thresholds_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            thresholds_frame,
            text="🚨 Limiares de Alerta",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # CPU
        cpu_frame = ctk.CTkFrame(thresholds_frame)
        cpu_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(cpu_frame, text="CPU (%):", width=100).pack(side="left", padx=5)
        self.cpu_threshold = ctk.CTkSlider(cpu_frame, from_=50, to=100, number_of_steps=50)
        self.cpu_threshold.set(85)
        self.cpu_threshold.pack(side="left", fill="x", expand=True, padx=5)
        
        self.cpu_threshold_label = ctk.CTkLabel(cpu_frame, text="85%", width=50)
        self.cpu_threshold_label.pack(side="right", padx=5)
        
        # Memória
        memory_frame = ctk.CTkFrame(thresholds_frame)
        memory_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(memory_frame, text="Memória (%):", width=100).pack(side="left", padx=5)
        self.memory_threshold = ctk.CTkSlider(memory_frame, from_=50, to=100, number_of_steps=50)
        self.memory_threshold.set(90)
        self.memory_threshold.pack(side="left", fill="x", expand=True, padx=5)
        
        self.memory_threshold_label = ctk.CTkLabel(memory_frame, text="90%", width=50)
        self.memory_threshold_label.pack(side="right", padx=5)
        
        # Disco
        disk_frame = ctk.CTkFrame(thresholds_frame)
        disk_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(disk_frame, text="Disco (%):", width=100).pack(side="left", padx=5)
        self.disk_threshold = ctk.CTkSlider(disk_frame, from_=70, to=100, number_of_steps=30)
        self.disk_threshold.set(95)
        self.disk_threshold.pack(side="left", fill="x", expand=True, padx=5)
        
        self.disk_threshold_label = ctk.CTkLabel(disk_frame, text="95%", width=50)
        self.disk_threshold_label.pack(side="right", padx=5)
        
        # Configurar callbacks
        self.cpu_threshold.configure(command=lambda v: self.cpu_threshold_label.configure(text=f"{int(v)}%"))
        self.memory_threshold.configure(command=lambda v: self.memory_threshold_label.configure(text=f"{int(v)}%"))
        self.disk_threshold.configure(command=lambda v: self.disk_threshold_label.configure(text=f"{int(v)}%"))
    
    def setup_backup_settings(self, parent):
        """Configura configurações de backup"""
        
        backup_frame = ctk.CTkFrame(parent)
        backup_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            backup_frame,
            text="💾 Backup e Restauração",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Backup automático
        self.auto_backup_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            backup_frame,
            text="🔄 Backup automático antes das otimizações",
            variable=self.auto_backup_var
        ).pack(anchor="w", padx=10, pady=5)
        
        # Localização do backup
        location_frame = ctk.CTkFrame(backup_frame)
        location_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(location_frame, text="📁 Localização dos backups:").pack(anchor="w", padx=5, pady=5)
        
        self.backup_location = ctk.CTkEntry(location_frame, placeholder_text="Selecione a pasta...")
        self.backup_location.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(
            location_frame,
            text="📂 Selecionar",
            command=self.select_backup_location,
            width=100
        ).pack(side="right", padx=5)
        
        # Botões de ação
        action_frame = ctk.CTkFrame(backup_frame)
        action_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkButton(
            action_frame,
            text="💾 Criar Backup Manual",
            command=self.create_manual_backup,
            height=40
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            action_frame,
            text="🔄 Restaurar Backup",
            command=self.restore_backup,
            height=40
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            action_frame,
            text="🗑️ Limpar Backups Antigos",
            command=self.clean_old_backups,
            height=40
        ).pack(side="right", padx=(5, 0))
        
        # Lista de backups
        ctk.CTkLabel(
            backup_frame,
            text="📋 Backups Disponíveis",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(20, 5))
        
        self.backup_list = tk.Listbox(backup_frame, height=8)
        self.backup_list.pack(fill="x", padx=10, pady=5)
        
        # Atualizar lista de backups
        self.update_backup_list()
    
    # Métodos de funcionalidade
    
    def detect_hardware(self):
        """Detecta hardware do sistema"""
        def detect_thread():
            try:
                self.hardware_info_label.configure(text="Detectando...")
                
                # Detectar hardware
                self.hardware_info = self.hardware_detector.detect_system_hardware()
                self.optimization_profile = self.hardware_detector.classify_system_profile(self.hardware_info)
                
                # Atualizar interface
                self.root.after(0, self.update_hardware_display)
                
            except Exception as e:
                self.logger.error(f"Erro ao detectar hardware: {e}")
                self.root.after(0, lambda: self.hardware_info_label.configure(text="Erro na detecção"))
        
        threading.Thread(target=detect_thread, daemon=True).start()
    
    def update_hardware_display(self):
        """Atualiza exibição das informações de hardware"""
        if self.hardware_info:
            # Sidebar
            hw_text = f"CPU: {self.hardware_info['cpu']['brand'][:20]}...\n"
            hw_text += f"RAM: {self.hardware_info['memory']['total_gb']:.1f}GB\n"
            hw_text += f"GPU: {self.hardware_info['gpu']['type']}\n"
            hw_text += f"Perfil: {self.optimization_profile}"
            
            self.hardware_info_label.configure(text=hw_text)
            
            # Aba de hardware (se existir)
            if hasattr(self, 'hardware_profile_text'):
                detailed_text = "🔧 INFORMAÇÕES DO HARDWARE DETECTADO\n\n"
                
                # CPU
                cpu_info = self.hardware_info['cpu']
                detailed_text += f"🖥️ PROCESSADOR:\n"
                detailed_text += f"   Marca: {cpu_info['brand']}\n"
                detailed_text += f"   Arquitetura: {cpu_info['architecture']}\n"
                detailed_text += f"   Cores: {cpu_info['cores']}\n"
                detailed_text += f"   Threads: {cpu_info['threads']}\n"
                detailed_text += f"   Frequência: {cpu_info['frequency']:.2f} GHz\n"
                detailed_text += f"   Classificação: {cpu_info['gaming_classification']}\n\n"
                
                # Memória
                mem_info = self.hardware_info['memory']
                detailed_text += f"💾 MEMÓRIA:\n"
                detailed_text += f"   Total: {mem_info['total_gb']:.1f} GB\n"
                detailed_text += f"   Tipo: {mem_info['ddr_type']}\n"
                detailed_text += f"   Nível de Performance: {mem_info['performance_level']}\n\n"
                
                # Armazenamento
                storage_info = self.hardware_info['storage']
                detailed_text += f"💿 ARMAZENAMENTO:\n"
                detailed_text += f"   Tipo Principal: {storage_info['primary_type']}\n"
                detailed_text += f"   Drives SSD: {storage_info['ssd_count']}\n"
                detailed_text += f"   Drives HDD: {storage_info['hdd_count']}\n"
                detailed_text += f"   NVMe Detectado: {storage_info['has_nvme']}\n\n"
                
                # GPU
                gpu_info = self.hardware_info['gpu']
                detailed_text += f"🎮 GPU:\n"
                detailed_text += f"   Tipo: {gpu_info['type']}\n"
                detailed_text += f"   Gaming Capable: {gpu_info['gaming_capable']}\n\n"
                
                # Sistema
                system_info = self.hardware_info['system']
                detailed_text += f"🖱️ SISTEMA:\n"
                detailed_text += f"   Tipo: {system_info['type']}\n"
                detailed_text += f"   Portátil: {system_info['is_laptop']}\n\n"
                
                # Perfil de otimização
                detailed_text += f"⚡ PERFIL DE OTIMIZAÇÃO RECOMENDADO:\n"
                detailed_text += f"   {self.optimization_profile}\n\n"
                
                if self.optimization_profile == "Gaming High-End":
                    detailed_text += "🎮 Configurações recomendadas para jogos de alta performance\n"
                elif self.optimization_profile == "Gaming Mid-Range":
                    detailed_text += "🎮 Configurações balanceadas para jogos\n"
                elif self.optimization_profile == "Productivity":
                    detailed_text += "💼 Configurações otimizadas para produtividade\n"
                elif self.optimization_profile == "Balanced":
                    detailed_text += "⚖️ Configurações equilibradas para uso geral\n"
                else:
                    detailed_text += "📊 Configurações básicas de otimização\n"
                
                self.hardware_profile_text.delete("0.0", "end")
                self.hardware_profile_text.insert("0.0", detailed_text)
    
    def update_home_data(self):
        """Atualiza dados da aba inicial"""
        def update_thread():
            try:
                # Obter informações do sistema
                import psutil
                
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                system_text = f"💻 INFORMAÇÕES DO SISTEMA\n\n"
                system_text += f"🖥️ CPU: {cpu_percent:.1f}% de uso\n"
                system_text += f"🧠 Memória: {memory.percent:.1f}% de uso ({Utils.format_size(memory.used)} / {Utils.format_size(memory.total)})\n"
                system_text += f"💿 Disco: {disk.percent:.1f}% de uso ({Utils.format_size(disk.used)} / {Utils.format_size(disk.total)})\n\n"
                
                # Obter próximas tarefas
                next_tasks = self.schedule_manager.get_next_scheduled_tasks(3)
                tasks_text = "⏰ PRÓXIMAS TAREFAS:\n\n"
                
                if next_tasks:
                    for task in next_tasks:
                        time_until = task['time_until']
                        if time_until.total_seconds() > 0:
                            if time_until.days > 0:
                                time_str = f"{time_until.days}d {time_until.seconds//3600}h"
                            elif time_until.seconds > 3600:
                                time_str = f"{time_until.seconds//3600}h {(time_until.seconds%3600)//60}m"
                            else:
                                time_str = f"{time_until.seconds//60}m"
                            
                            tasks_text += f"• {task['name']}\n  Em: {time_str}\n\n"
                        else:
                            tasks_text += f"• {task['name']}\n  Atrasada\n\n"
                else:
                    tasks_text += "Nenhuma tarefa agendada\n"
                
                # Atualizar interface na thread principal
                self.root.after(0, lambda: self.update_home_ui(system_text, tasks_text))
                
            except Exception as e:
                self.logger.error(f"Erro ao atualizar dados da home: {e}")
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def update_home_ui(self, system_text, tasks_text):
        """Atualiza interface da home na thread principal"""
        if hasattr(self, 'system_info_text'):
            self.system_info_text.delete("0.0", "end")
            self.system_info_text.insert("0.0", system_text)
        
        if hasattr(self, 'next_tasks_text'):
            self.next_tasks_text.delete("0.0", "end")
            self.next_tasks_text.insert("0.0", tasks_text)
        
        # Atualizar status de saúde
        if self.system_monitor.is_monitoring():
            health_score = self.system_monitor.get_system_health_score()
            if health_score is not None:
                if health_score >= 80:
                    status_text = f"🟢 Excelente ({health_score:.0f}%)"
                    status_color = "green"
                elif health_score >= 60:
                    status_text = f"🟡 Bom ({health_score:.0f}%)"
                    status_color = "orange"
                else:
                    status_text = f"🔴 Precisa Atenção ({health_score:.0f}%)"
                    status_color = "red"
                
                self.health_score_label.configure(text=status_text, text_color=status_color)
            else:
                self.health_score_label.configure(text="📊 Coletando dados...", text_color="white")
        else:
            self.health_score_label.configure(text="⏸️ Monitoramento parado", text_color="gray")
    
    def create_system_chart(self):
        """Cria gráfico de uso do sistema"""
        try:
            # Limpar container existente
            for widget in self.chart_container.winfo_children():
                widget.destroy()
            
            # Criar figura matplotlib
            fig, ax = plt.subplots(figsize=(6, 4), facecolor='#212121')
            ax.set_facecolor('#212121')
            
            # Dados de exemplo (será atualizado pelo monitoramento)
            import psutil
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            categories = ['CPU', 'Memória', 'Disco']
            values = [cpu, memory, disk]
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
            
            bars = ax.bar(categories, values, color=colors, alpha=0.8)
            
            # Configurar gráfico
            ax.set_ylabel('Uso (%)', color='white')
            ax.set_title('Uso Atual do Sistema', color='white', fontsize=12, weight='bold')
            ax.set_ylim(0, 100)
            ax.tick_params(colors='white')
            
            # Adicionar valores nas barras
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{value:.1f}%', ha='center', va='bottom', color='white')
            
            # Ajustar layout
            plt.tight_layout()
            
            # Adicionar ao container
            canvas = FigureCanvasTkAgg(fig, self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            self.logger.error(f"Erro ao criar gráfico: {e}")
    
    def setup_scheduler_callbacks(self):
        """Configura callbacks do agendador"""
        
        def cleanup_callback(task_id, task_type):
            """Callback para tarefas de limpeza"""
            try:
                if task_type == "quick_cleanup":
                    return self.perform_scheduled_cleanup(quick=True)
                elif task_type == "deep_cleanup":
                    return self.perform_scheduled_cleanup(quick=False)
                elif task_type == "duplicate_cleanup":
                    return self.perform_scheduled_duplicate_cleanup()
                elif task_type == "registry_cleanup":
                    return self.perform_scheduled_registry_cleanup()
            except Exception as e:
                self.logger.error(f"Erro no callback de limpeza {task_type}: {e}")
                return False
            
            return False
        
        def optimization_callback(task_id, task_type):
            """Callback para tarefas de otimização"""
            try:
                if task_type == "system_optimization":
                    return self.perform_scheduled_optimization()
            except Exception as e:
                self.logger.error(f"Erro no callback de otimização {task_type}: {e}")
                return False
            
            return False
        
        # Registrar callbacks
        self.schedule_manager.register_task_callback("quick_cleanup", cleanup_callback)
        self.schedule_manager.register_task_callback("deep_cleanup", cleanup_callback)
        self.schedule_manager.register_task_callback("duplicate_cleanup", cleanup_callback)
        self.schedule_manager.register_task_callback("registry_cleanup", cleanup_callback)
        self.schedule_manager.register_task_callback("system_optimization", optimization_callback)
    
    def show_admin_warning(self):
        """Mostra aviso sobre privilégios de administrador"""
        messagebox.showwarning(
            "Privilégios de Administrador",
            "⚠️ Para o funcionamento completo do otimizador, "
            "é recomendado executar como administrador.\n\n"
            "Algumas funcionalidades podem estar limitadas."
        )
    
    # Métodos de ação - implementar conforme necessário
    def quick_cleanup(self): pass
    def quick_optimization(self): pass
    def analyze_cleanup(self): pass
    def perform_cleanup(self): pass
    def analyze_advanced_cleanup(self): pass
    def perform_advanced_cleanup(self): pass
    def find_duplicates(self): pass
    def remove_duplicates(self): pass
    def analyze_performance(self): pass
    def optimize_performance(self): pass
    def apply_advanced_optimizations(self): pass
    def apply_hardware_profile(self): pass
    def test_network_speed(self): pass
    def optimize_network(self): pass
    def start_monitoring(self): pass
    def stop_monitoring(self): pass
    def export_monitoring_report(self): pass
    def start_scheduler(self): pass
    def stop_scheduler(self): pass
    def create_new_task(self): pass
    def update_tasks_list(self): pass
    def change_theme(self, theme): pass
    def save_settings(self): pass
    def select_backup_location(self): pass
    def create_manual_backup(self): pass
    def restore_backup(self): pass
    def clean_old_backups(self): pass
    def update_backup_list(self): pass
    def perform_scheduled_cleanup(self, quick=True): return True
    def perform_scheduled_duplicate_cleanup(self): return True
    def perform_scheduled_registry_cleanup(self): return True
    def perform_scheduled_optimization(self): return True
    
    def run(self):
        """Executa a interface"""
        self.root.mainloop()

# Usar a nova interface
OptimizerUI = AdvancedOptimizerUI