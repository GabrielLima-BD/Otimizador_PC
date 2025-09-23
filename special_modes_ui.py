"""
Interface dos Modos Especiais ULTRA
Sistema completo de modos de performance avançados
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
import psutil
from datetime import datetime
import json
from typing import Dict, List, Optional, Callable
import queue

class SpecialModesWindow(ctk.CTkToplevel):
    """Janela dos modos especiais de otimização"""
    
    def __init__(self, parent, special_modes=None):
        super().__init__(parent)
        
        self.title("🚀 Modos Especiais ULTRA - Performance Extrema")
        self.geometry("1000x800")
        
        # Configurar janela
        self.transient(parent)
        self.grab_set()
        
        self.special_modes = special_modes
        self.monitoring_active = False
        self.performance_data = {"cpu": [], "memory": [], "timestamps": []}
        self.progress_queue = queue.Queue()
        
        self.setup_ui()
        self.center_window()
        
        # Iniciar processamento da queue
        self.after(100, self._process_progress_queue)
        
    def setup_ui(self):
        """Configura a interface"""
        
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🚀 MODOS ESPECIAIS ULTRA",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Performance Extrema | Limpeza Profunda | Monitoramento Avançado",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 5))
        
        # 🎤 AVISO DE PROTEÇÃO DE ÁUDIO
        audio_protection_label = ctk.CTkLabel(
            header_frame,
            text="🎤 PROTEÇÃO ATIVA: Serviços de áudio/microfone estão protegidos e nunca serão desabilitados",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00ff00"
        )
        audio_protection_label.pack(pady=(0, 10))
        
        # Container principal com abas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Abas principais
        self.setup_modes_tab()
        self.setup_monitoring_tab()
        self.setup_reports_tab()
        self.setup_settings_tab()
    
    def setup_modes_tab(self):
        """Aba dos modos especiais"""
        modes_tab = self.tabview.add("🎮 Modos Especiais")
        
        # Frame dos modos principais
        main_frame = ctk.CTkScrollableFrame(modes_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 🚀 MODO TURBO
        turbo_frame = ctk.CTkFrame(main_frame)
        turbo_frame.pack(fill="x", pady=5)
        
        turbo_header = ctk.CTkLabel(
            turbo_frame,
            text="🚀 MODO TURBO - Gaming Extremo",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ff6b35"
        )
        turbo_header.pack(pady=10)
        
        turbo_desc = ctk.CTkLabel(
            turbo_frame,
            text="• Desativa serviços desnecessários\\n• Finaliza processos que consomem recursos\\n• Otimiza prioridades de CPU para jogos\\n• Limpa RAM e cache do sistema",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        turbo_desc.pack(pady=5)
        
        turbo_buttons = ctk.CTkFrame(turbo_frame)
        turbo_buttons.pack(fill="x", padx=10, pady=10)
        
        self.turbo_button = ctk.CTkButton(
            turbo_buttons,
            text="🚀 ATIVAR MODO TURBO",
            command=self.activate_turbo_mode,
            height=50,
            width=200,
            fg_color="#ff6b35",
            hover_color="#e55a2b"
        )
        self.turbo_button.pack(side="left", padx=5)
        
        self.deactivate_turbo_button = ctk.CTkButton(
            turbo_buttons,
            text="🔄 DESATIVAR TURBO",
            command=self.deactivate_turbo_mode,
            height=50,
            width=200,
            fg_color="#636e72",
            hover_color="#575d61"
        )
        self.deactivate_turbo_button.pack(side="right", padx=5)
        
        # 🤫 MODO SILENCIOSO
        silent_frame = ctk.CTkFrame(main_frame)
        silent_frame.pack(fill="x", pady=5)
        
        silent_header = ctk.CTkLabel(
            silent_frame,
            text="🤫 MODO SILENCIOSO - Automação Completa",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#6c5ce7"
        )
        silent_header.pack(pady=10)
        
        silent_desc = ctk.CTkLabel(
            silent_frame,
            text="• Execução automática no boot do sistema\\n• Limpeza silenciosa de arquivos temporários\\n• Otimização de registro sem interrupções\\n• Preparação automática para jogos",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        silent_desc.pack(pady=5)
        
        self.silent_button = ctk.CTkButton(
            silent_frame,
            text="🤫 EXECUTAR MODO SILENCIOSO",
            command=self.activate_silent_mode,
            height=50,
            fg_color="#6c5ce7",
            hover_color="#5a4fcf"
        )
        self.silent_button.pack(pady=10)
        
        # 📊 MODO BENCHMARK
        benchmark_frame = ctk.CTkFrame(main_frame)
        benchmark_frame.pack(fill="x", pady=5)
        
        benchmark_header = ctk.CTkLabel(
            benchmark_frame,
            text="📊 MODO BENCHMARK - Teste Completo",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00b894"
        )
        benchmark_header.pack(pady=10)
        
        benchmark_desc = ctk.CTkLabel(
            benchmark_frame,
            text="• Aplica TODAS as otimizações disponíveis\\n• Coleta métricas antes e depois\\n• Gera relatório detalhado de performance\\n• Calcula score de melhoria do sistema",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        benchmark_desc.pack(pady=5)
        
        self.benchmark_button = ctk.CTkButton(
            benchmark_frame,
            text="📊 INICIAR BENCHMARK COMPLETO",
            command=self.activate_benchmark_mode,
            height=50,
            fg_color="#00b894",
            hover_color="#00a085"
        )
        self.benchmark_button.pack(pady=10)
        
        # 🧹 MODO LIMPEZA PROFUNDA
        clean_frame = ctk.CTkFrame(main_frame)
        clean_frame.pack(fill="x", pady=5)
        
        clean_header = ctk.CTkLabel(
            clean_frame,
            text="🧹 MODO LIMPEZA PROFUNDA - Remove Tudo Inútil",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#fd79a8"
        )
        clean_header.pack(pady=10)
        
        clean_desc = ctk.CTkLabel(
            clean_frame,
            text="• Remove arquivos temporários avançados\\n• Limpa logs e dumps do sistema\\n• Remove cache de todos os aplicativos\\n• Limpa entradas órfãs do registro",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        clean_desc.pack(pady=5)
        
        self.clean_button = ctk.CTkButton(
            clean_frame,
            text="🧹 INICIAR LIMPEZA PROFUNDA",
            command=self.activate_deep_clean_mode,
            height=50,
            fg_color="#fd79a8",
            hover_color="#e66992"
        )
        self.clean_button.pack(pady=10)
        
        # ⚡ MODO EXTREMO
        extreme_frame = ctk.CTkFrame(main_frame)
        extreme_frame.pack(fill="x", pady=5)
        
        extreme_header = ctk.CTkLabel(
            extreme_frame,
            text="⚡ MODO EXTREMO - MÁXIMA PERFORMANCE",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#d63031"
        )
        extreme_header.pack(pady=10)
        
        extreme_warning = ctk.CTkLabel(
            extreme_frame,
            text="⚠️ ATENÇÃO: Este modo aplica as otimizações mais agressivas!\\nPode causar instabilidade em sistemas não preparados.\\nRecomendado apenas para PCs dedicados ao gaming.",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#d63031",
            justify="center"
        )
        extreme_warning.pack(pady=5)
        
        extreme_desc = ctk.CTkLabel(
            extreme_frame,
            text="• TODAS as otimizações ULTRA aplicadas\\n• Configurações extremas de CPU/GPU/RAM\\n• Desabilitação de funcionalidades do Windows\\n• Performance absoluta sacrificando compatibilidade",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        extreme_desc.pack(pady=5)
        
        self.extreme_button = ctk.CTkButton(
            extreme_frame,
            text="⚡ ATIVAR MODO EXTREMO ⚡",
            command=self.activate_extreme_mode,
            height=60,
            fg_color="#d63031",
            hover_color="#b71c1c",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.extreme_button.pack(pady=15)
        
        # Status e progresso
        status_frame = ctk.CTkFrame(modes_tab)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.current_mode_label = ctk.CTkLabel(
            status_frame,
            text="Status: Modo Normal Ativo",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.current_mode_label.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(status_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=5)
    
    def setup_monitoring_tab(self):
        """Aba de monitoramento"""
        monitoring_tab = self.tabview.add("📊 Monitoramento")
        
        # Controles
        controls_frame = ctk.CTkFrame(monitoring_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        control_header = ctk.CTkLabel(
            controls_frame,
            text="📈 MONITORAMENTO EM TEMPO REAL",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        control_header.pack(pady=10)
        
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_monitor_button = ctk.CTkButton(
            buttons_frame,
            text="▶️ INICIAR",
            command=self.start_monitoring,
            fg_color="#00b894",
            width=120
        )
        self.start_monitor_button.pack(side="left", padx=5)
        
        self.stop_monitor_button = ctk.CTkButton(
            buttons_frame,
            text="⏹️ PARAR",
            command=self.stop_monitoring,
            fg_color="#d63031",
            width=120
        )
        self.stop_monitor_button.pack(side="left", padx=5)
        
        self.save_data_button = ctk.CTkButton(
            buttons_frame,
            text="💾 SALVAR",
            command=self.save_monitoring_data,
            fg_color="#6c5ce7",
            width=120
        )
        self.save_data_button.pack(side="left", padx=5)
        
        # Métricas em tempo real
        metrics_frame = ctk.CTkFrame(monitoring_tab)
        metrics_frame.pack(fill="x", padx=10, pady=5)
        
        metrics_header = ctk.CTkLabel(
            metrics_frame,
            text="📋 MÉTRICAS ATUAIS DO SISTEMA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        metrics_header.pack(pady=10)
        
        # Grid de métricas 3x2
        metrics_grid = ctk.CTkFrame(metrics_frame)
        metrics_grid.pack(fill="x", padx=20, pady=10)
        
        self.cpu_label = ctk.CTkLabel(
            metrics_grid, 
            text="🖥️ CPU: ---%",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.cpu_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.memory_label = ctk.CTkLabel(
            metrics_grid, 
            text="🧠 RAM: ---%",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.memory_label.grid(row=0, column=1, padx=20, pady=10)
        
        self.disk_label = ctk.CTkLabel(
            metrics_grid, 
            text="💾 Disco: ---%",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.disk_label.grid(row=0, column=2, padx=20, pady=10)
        
        self.network_label = ctk.CTkLabel(
            metrics_grid, 
            text="🌐 Rede: --- ms",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.network_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.processes_label = ctk.CTkLabel(
            metrics_grid, 
            text="⚙️ Processos: ---",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.processes_label.grid(row=1, column=1, padx=20, pady=10)
        
        self.temp_label = ctk.CTkLabel(
            metrics_grid, 
            text="🌡️ Temp: ---°C",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.temp_label.grid(row=1, column=2, padx=20, pady=10)
        
        # Gráfico placeholder
        graph_frame = ctk.CTkFrame(monitoring_tab)
        graph_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        graph_label = ctk.CTkLabel(
            graph_frame,
            text="📈 GRÁFICO DE PERFORMANCE EM TEMPO REAL\\n\\n(Os dados são atualizados quando o monitoramento está ativo)\\n\\nCPU, RAM, Disco, Rede - Histórico dos últimos 60 segundos",
            font=ctk.CTkFont(size=14),
            height=200,
            justify="center"
        )
        graph_label.pack(fill="both", expand=True, pady=30)
    
    def setup_reports_tab(self):
        """Aba de relatórios"""
        reports_tab = self.tabview.add("📋 Relatórios")
        
        header = ctk.CTkLabel(
            reports_tab,
            text="📊 RELATÓRIOS E HISTÓRICO DE OTIMIZAÇÕES",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.pack(pady=15)
        
        # Botões de relatório
        buttons_frame = ctk.CTkFrame(reports_tab)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        self.generate_report_button = ctk.CTkButton(
            buttons_frame,
            text="📄 GERAR RELATÓRIO COMPLETO",
            command=self.generate_performance_report,
            height=50,
            fg_color="#00b894"
        )
        self.generate_report_button.pack(pady=5)
        
        self.export_pdf_button = ctk.CTkButton(
            buttons_frame,
            text="📑 EXPORTAR PARA PDF",
            command=self.export_report_pdf,
            height=50,
            fg_color="#6c5ce7"
        )
        self.export_pdf_button.pack(pady=5)
        
        self.view_history_button = ctk.CTkButton(
            buttons_frame,
            text="🕒 ATUALIZAR HISTÓRICO",
            command=self.load_optimization_history,
            height=50,
            fg_color="#fd79a8"
        )
        self.view_history_button.pack(pady=5)
        
        # Área do histórico
        history_frame = ctk.CTkFrame(reports_tab)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        history_header = ctk.CTkLabel(
            history_frame,
            text="📚 HISTÓRICO DE EXECUÇÕES",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        history_header.pack(pady=10)
        
        self.history_text = ctk.CTkTextbox(
            history_frame,
            height=400,
            font=ctk.CTkFont(size=12)
        )
        self.history_text.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Carregar histórico inicial
        self.load_optimization_history()
    
    def setup_settings_tab(self):
        """Aba de configurações"""
        settings_tab = self.tabview.add("⚙️ Configurações")
        
        header = ctk.CTkLabel(
            settings_tab,
            text="🔧 CONFIGURAÇÕES AVANÇADAS DOS MODOS",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.pack(pady=15)
        
        # Configurações de monitoramento
        monitor_frame = ctk.CTkFrame(settings_tab)
        monitor_frame.pack(fill="x", padx=10, pady=10)
        
        monitor_header = ctk.CTkLabel(
            monitor_frame,
            text="📊 Configurações de Monitoramento",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        monitor_header.pack(pady=10)
        
        interval_frame = ctk.CTkFrame(monitor_frame)
        interval_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(interval_frame, text="Intervalo de Atualização (segundos):", font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        
        self.update_interval_var = tk.StringVar(value="2")
        interval_entry = ctk.CTkEntry(
            interval_frame,
            textvariable=self.update_interval_var,
            width=80,
            font=ctk.CTkFont(size=12)
        )
        interval_entry.pack(side="right", padx=10)
        
        self.auto_start_var = tk.BooleanVar(value=False)
        auto_start_check = ctk.CTkCheckBox(
            monitor_frame,
            text="Iniciar monitoramento automaticamente com a janela",
            variable=self.auto_start_var,
            font=ctk.CTkFont(size=12)
        )
        auto_start_check.pack(pady=10)
        
        # Configurações de segurança
        security_frame = ctk.CTkFrame(settings_tab)
        security_frame.pack(fill="x", padx=10, pady=10)
        
        security_header = ctk.CTkLabel(
            security_frame,
            text="🛡️ Configurações de Segurança",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        security_header.pack(pady=10)
        
        self.auto_backup_var = tk.BooleanVar(value=True)
        backup_check = ctk.CTkCheckBox(
            security_frame,
            text="Fazer backup automático antes do Modo Turbo",
            variable=self.auto_backup_var,
            font=ctk.CTkFont(size=12)
        )
        backup_check.pack(pady=5)
        
        self.double_confirm_var = tk.BooleanVar(value=True)
        confirm_check = ctk.CTkCheckBox(
            security_frame,
            text="Exigir confirmação dupla para Modo Extremo",
            variable=self.double_confirm_var,
            font=ctk.CTkFont(size=12)
        )
        confirm_check.pack(pady=5)
        
        self.create_restore_var = tk.BooleanVar(value=True)
        restore_check = ctk.CTkCheckBox(
            security_frame,
            text="Criar ponto de restauração antes de alterações críticas",
            variable=self.create_restore_var,
            font=ctk.CTkFont(size=12)
        )
        restore_check.pack(pady=5)
        
        # Botão salvar
        save_button = ctk.CTkButton(
            settings_tab,
            text="💾 SALVAR TODAS AS CONFIGURAÇÕES",
            command=self.save_settings,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00b894"
        )
        save_button.pack(pady=30)
    
    # MÉTODOS DOS MODOS ESPECIAIS
    
    def activate_turbo_mode(self):
        """Ativa o modo turbo"""
        if not self.special_modes:
            messagebox.showerror("Erro", "Sistema de modos especiais não disponível")
            return
        
        result = messagebox.askyesno(
            "🚀 Confirmar Modo Turbo",
            "O MODO TURBO irá otimizar seu sistema para gaming:\\n\\n"
            "✅ Desativar serviços desnecessários\\n"
            "✅ Finalizar processos que consomem recursos\\n"
            "✅ Otimizar prioridades de CPU\\n"
            "✅ Limpar RAM e cache\\n\\n"
            "Seu sistema ficará otimizado para jogos.\\n\\n"
            "Deseja continuar?",
            icon="question"
        )
        
        if result:
            thread = threading.Thread(target=self._run_turbo_mode)
            thread.daemon = True
            thread.start()
    
    def _run_turbo_mode(self):
        """Executa o modo turbo em thread separada"""
        def progress_callback(message, current, total):
            progress = current / total if total > 0 else 0
            self.progress_queue.put(("progress", progress, message))
        
        try:
            if self.special_modes:
                result = self.special_modes.activate_turbo_mode(progress_callback)
                self.progress_queue.put(("complete", result))
            else:
                self.progress_queue.put(("error", "Sistema de modos especiais não disponível"))
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
    
    def deactivate_turbo_mode(self):
        """Desativa o modo turbo"""
        if not self.special_modes:
            return
        
        result = messagebox.askyesno(
            "🔄 Desativar Modo Turbo",
            "Deseja restaurar as configurações normais do sistema?\\n\\n"
            "Isso irá reverter as otimizações do Modo Turbo.",
            icon="question"
        )
        
        if result:
            thread = threading.Thread(target=self._run_deactivate_turbo)
            thread.daemon = True
            thread.start()
    
    def _run_deactivate_turbo(self):
        """Desativa o modo turbo"""
        def progress_callback(message, current, total):
            progress = current / total if total > 0 else 0
            self.progress_queue.put(("progress", progress, message))
        
        try:
            if self.special_modes:
                result = self.special_modes.deactivate_turbo_mode(progress_callback)
                self.progress_queue.put(("complete", result))
            else:
                self.progress_queue.put(("error", "Sistema de modos especiais não disponível"))
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
    
    def activate_silent_mode(self):
        """Ativa o modo silencioso"""
        if not self.special_modes:
            messagebox.showerror("Erro", "Sistema de modos especiais não disponível")
            return
        
        thread = threading.Thread(target=self._run_silent_mode)
        thread.daemon = True
        thread.start()
    
    def _run_silent_mode(self):
        """Executa o modo silencioso"""
        def progress_callback(message, current, total):
            progress = current / total if total > 0 else 0
            self.progress_queue.put(("progress", progress, message))
        
        try:
            if self.special_modes:
                result = self.special_modes.activate_silent_mode(progress_callback)
                self.progress_queue.put(("complete", result))
            else:
                self.progress_queue.put(("error", "Sistema de modos especiais não disponível"))
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
    
    def activate_benchmark_mode(self):
        """Ativa o modo benchmark"""
        if not self.special_modes:
            messagebox.showerror("Erro", "Sistema de modos especiais não disponível")
            return
        
        result = messagebox.askyesno(
            "📊 Confirmar Benchmark",
            "O MODO BENCHMARK irá:\\n\\n"
            "🔄 Aplicar TODAS as otimizações disponíveis\\n"
            "📊 Coletar métricas antes e depois\\n"
            "📈 Gerar relatório detalhado de performance\\n"
            "⏱️ O processo pode demorar vários minutos\\n\\n"
            "Continuar com o benchmark completo?",
            icon="question"
        )
        
        if result:
            thread = threading.Thread(target=self._run_benchmark_mode)
            thread.daemon = True
            thread.start()
    
    def _run_benchmark_mode(self):
        """Executa o modo benchmark"""
        def progress_callback(message, current, total):
            progress = current / total if total > 0 else 0
            self.progress_queue.put(("progress", progress, message))
        
        try:
            if self.special_modes:
                result = self.special_modes.activate_benchmark_mode(progress_callback)
                self.progress_queue.put(("complete", result))
            else:
                self.progress_queue.put(("error", "Sistema de modos especiais não disponível"))
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
    
    def activate_deep_clean_mode(self):
        """Ativa o modo limpeza profunda"""
        if not self.special_modes:
            messagebox.showerror("Erro", "Sistema de modos especiais não disponível")
            return
        
        thread = threading.Thread(target=self._run_deep_clean_mode)
        thread.daemon = True
        thread.start()
    
    def _run_deep_clean_mode(self):
        """Executa a limpeza profunda"""
        def progress_callback(message, current, total):
            progress = current / total if total > 0 else 0
            self.progress_queue.put(("progress", progress, message))
        
        try:
            if self.special_modes:
                result = self.special_modes.activate_deep_clean_mode(progress_callback)
                self.progress_queue.put(("complete", result))
            else:
                self.progress_queue.put(("error", "Sistema de modos especiais não disponível"))
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
    
    def activate_extreme_mode(self):
        """Ativa o modo extremo"""
        if not self.special_modes:
            messagebox.showerror("Erro", "Sistema de modos especiais não disponível")
            return
        
        # Confirmação dupla se habilitada
        if self.double_confirm_var.get():
            result1 = messagebox.askyesno(
                "⚠️ ATENÇÃO - MODO EXTREMO ⚠️",
                "VOCÊ ESTÁ PRESTES A ATIVAR O MODO MAIS AGRESSIVO!\\n\\n"
                "❌ RISCOS:\\n"
                "• Pode causar instabilidade do sistema\\n"
                "• Algumas funcionalidades podem parar de funcionar\\n"
                "• Modificações profundas no Windows\\n"
                "• Recomendado APENAS para PCs dedicados ao gaming\\n\\n"
                "🎯 BENEFÍCIOS:\\n"
                "• Máxima performance possível\\n"
                "• Latência mínima\\n"
                "• FPS maximizado\\n\\n"
                "Você tem CERTEZA absoluta que deseja continuar?",
                icon="warning"
            )
            
            if not result1:
                return
            
            result2 = messagebox.askyesno(
                "⚠️ CONFIRMAÇÃO FINAL ⚠️",
                "ÚLTIMA CHANCE DE CANCELAR!\\n\\n"
                "Ao clicar SIM, o MODO EXTREMO será ativado e fará\\n"
                "modificações irreversíveis em seu sistema.\\n\\n"
                "CONFIRMA A ATIVAÇÃO DO MODO EXTREMO?",
                icon="error"
            )
            
            if not result2:
                return
        
        thread = threading.Thread(target=self._run_extreme_mode)
        thread.daemon = True
        thread.start()
    
    def _run_extreme_mode(self):
        """Executa o modo extremo"""
        def progress_callback(message, current, total):
            progress = current / total if total > 0 else 0
            self.progress_queue.put(("progress", progress, message))
        
        try:
            if self.special_modes:
                result = self.special_modes.activate_extreme_performance_mode(progress_callback)
                self.progress_queue.put(("complete", result))
            else:
                self.progress_queue.put(("error", "Sistema de modos especiais não disponível"))
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
    
    def _process_progress_queue(self):
        """Processa a queue de progresso"""
        try:
            while True:
                event_type, data, *args = self.progress_queue.get_nowait()
                
                if event_type == "progress":
                    progress_value, message = data, args[0] if args else ""
                    self.progress_bar.set(progress_value)
                    self.progress_label.configure(text=message)
                
                elif event_type == "complete":
                    result = data
                    self.progress_bar.set(1.0)
                    
                    if result.get("success", False):
                        success_msg = "✅ " + result.get("message", "Operação concluída!")
                        self.progress_label.configure(text=success_msg)
                        
                        if "mode" in result:
                            mode_name = result["mode"].replace("_", " ").title()
                            self.current_mode_label.configure(text=f"Status: {mode_name} Ativo 🚀")
                        
                        # Mostrar detalhes em popup
                        if "optimizations" in result:
                            opts = result["optimizations"]
                            details = f"✅ Operação concluída com sucesso!\\n\\n"
                            details += f"📊 {len(opts)} otimizações aplicadas:\\n\\n"
                            
                            for i, opt in enumerate(opts[:8]):  # Mostrar até 8 itens
                                details += f"• {opt}\\n"
                            
                            if len(opts) > 8:
                                details += f"\\n... e mais {len(opts)-8} otimizações"
                            
                            if "total_space_freed" in result:
                                details += f"\\n\\n💾 Espaço liberado: {result['total_space_freed']} MB"
                            
                            messagebox.showinfo("🎉 Sucesso!", details)
                    
                    else:
                        error_msg = "❌ " + result.get("error", "Erro desconhecido")
                        self.progress_label.configure(text=error_msg)
                        messagebox.showerror("❌ Erro", result.get("error", "Erro desconhecido"))
                    
                    # Reset progress após 5 segundos
                    self.after(5000, lambda: self.progress_bar.set(0))
                    self.after(5000, lambda: self.progress_label.configure(text=""))
                
                elif event_type == "error":
                    error_msg = data
                    self.progress_bar.set(0)
                    self.progress_label.configure(text="❌ " + error_msg)
                    messagebox.showerror("❌ Erro", error_msg)
        
        except queue.Empty:
            pass
        
        # Continuar processando
        self.after(100, self._process_progress_queue)
    
    # MÉTODOS DE MONITORAMENTO
    
    def start_monitoring(self):
        """Inicia o monitoramento"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.start_monitor_button.configure(state="disabled", text="🟢 ATIVO")
        self.stop_monitor_button.configure(state="normal")
        
        monitor_thread = threading.Thread(target=self._monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.monitoring_active = False
        self.start_monitor_button.configure(state="normal", text="▶️ INICIAR")
        self.stop_monitor_button.configure(state="disabled", text="⏹️ PARADO")
    
    def _monitoring_loop(self):
        """Loop de monitoramento"""
        while self.monitoring_active:
            try:
                # Coletar métricas
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('C:')
                processes_count = len(psutil.pids())
                
                # Atualizar interface
                self.after(0, lambda: self._update_metrics_display(
                    cpu_percent, memory.percent, disk.percent, 
                    processes_count, 15.0, 45.0  # network, temp placeholder
                ))
                
                # Armazenar dados
                self.performance_data["cpu"].append(cpu_percent)
                self.performance_data["memory"].append(memory.percent)
                self.performance_data["timestamps"].append(datetime.now())
                
                # Manter apenas 60 pontos
                if len(self.performance_data["cpu"]) > 60:
                    for key in self.performance_data:
                        self.performance_data[key] = self.performance_data[key][-60:]
                
                # Intervalo
                interval = float(self.update_interval_var.get() or 2)
                time.sleep(interval)
                
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                time.sleep(2)
    
    def _update_metrics_display(self, cpu, memory, disk, processes, network, temp):
        """Atualiza métricas na interface"""
        self.cpu_label.configure(text=f"🖥️ CPU: {cpu:.1f}%")
        self.memory_label.configure(text=f"🧠 RAM: {memory:.1f}%")
        self.disk_label.configure(text=f"💾 Disco: {disk:.1f}%")
        self.processes_label.configure(text=f"⚙️ Processos: {processes}")
        self.network_label.configure(text=f"🌐 Rede: {network:.1f} ms")
        self.temp_label.configure(text=f"🌡️ Temp: {temp:.1f}°C")
    
    def save_monitoring_data(self):
        """Salva dados de monitoramento"""
        if not self.performance_data["cpu"]:
            messagebox.showwarning("⚠️ Aviso", "Nenhum dado de monitoramento disponível.\\nInicie o monitoramento primeiro.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Salvar Dados de Monitoramento",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Todos os arquivos", "*.*")],
            initialfile=f"monitoring_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if filename:
            try:
                data_to_save = {
                    "cpu": self.performance_data["cpu"],
                    "memory": self.performance_data["memory"],
                    "timestamps": [ts.isoformat() for ts in self.performance_data["timestamps"]],
                    "exported_at": datetime.now().isoformat(),
                    "total_samples": len(self.performance_data["cpu"])
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("💾 Sucesso", f"Dados salvos com sucesso!\\n\\nArquivo: {filename}\\nAmostras: {len(self.performance_data['cpu'])}")
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao salvar dados:\\n{e}")
    
    # MÉTODOS DE RELATÓRIOS
    
    def generate_performance_report(self):
        """Gera relatório de performance"""
        try:
            # Coletar métricas atuais
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            
            report = f"""
📊 RELATÓRIO DE PERFORMANCE DO SISTEMA
======================================

🕒 Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

📈 MÉTRICAS ATUAIS:
• CPU: {cpu_percent:.1f}%
• RAM: {memory.percent:.1f}% ({memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB)
• Disco C: {disk.percent:.1f}% ({disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB)
• Processos ativos: {len(psutil.pids())}

🔧 MODOS ESPECIAIS DISPONÍVEIS:
• 🚀 Modo Turbo: Otimização para gaming
• 🤫 Modo Silencioso: Automação completa
• 📊 Modo Benchmark: Teste e relatório
• 🧹 Limpeza Profunda: Remove arquivos inúteis
• ⚡ Modo Extremo: Performance máxima

📊 DADOS DE MONITORAMENTO:
• Amostras coletadas: {len(self.performance_data.get('cpu', []))}
• Monitoramento ativo: {'Sim' if self.monitoring_active else 'Não'}

💡 RECOMENDAÇÕES:
• Execute o Modo Turbo para otimizar jogos
• Use a Limpeza Profunda para liberar espaço
• Monitore o sistema em tempo real
• Faça backup antes do Modo Extremo
"""
            
            # Salvar relatório
            filename = filedialog.asksaveasfilename(
                title="Salvar Relatório de Performance",
                defaultextension=".txt",
                filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
                initialfile=f"relatorio_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                messagebox.showinfo("📄 Relatório Gerado", f"Relatório salvo com sucesso!\\n\\nArquivo: {filename}")
        
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao gerar relatório:\\n{e}")
    
    def export_report_pdf(self):
        """Exporta relatório para PDF"""
        messagebox.showinfo(
            "📑 Exportar PDF", 
            "Funcionalidade de exportação PDF será implementada em versão futura.\\n\\n"
            "Por enquanto, use 'Gerar Relatório Completo' para salvar em TXT."
        )
    
    def load_optimization_history(self):
        """Carrega histórico de otimizações"""
        try:
            history = f"""
📚 HISTÓRICO DE OTIMIZAÇÕES E EXECUÇÕES
=====================================

🕒 Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

📊 ESTATÍSTICAS GERAIS:
• Sistema: Windows 10/11
• Otimizador: Versão ULTRA
• Modos disponíveis: 5 modos especiais
• Status atual: {self.current_mode_label.cget('text')}

🚀 MODOS EXECUTADOS RECENTEMENTE:
• Nenhum modo especial executado ainda
• Execute algum modo para ver o histórico aqui

📈 ÚLTIMAS MÉTRICAS:
• Monitoramento ativo: {'Sim' if self.monitoring_active else 'Não'}
• Dados coletados: {len(self.performance_data.get('cpu', []))} amostras
• Intervalo de coleta: {self.update_interval_var.get()}s

🔧 CONFIGURAÇÕES ATUAIS:
• Auto-start monitoramento: {'Sim' if self.auto_start_var.get() else 'Não'}
• Backup automático: {'Sim' if self.auto_backup_var.get() else 'Não'}
• Confirmação dupla extremo: {'Sim' if self.double_confirm_var.get() else 'Não'}

💡 PRÓXIMOS PASSOS:
1. Execute o Modo Turbo para otimizar o sistema
2. Ative o monitoramento em tempo real
3. Use a Limpeza Profunda para liberar espaço
4. Teste o Modo Benchmark para relatório completo

⚠️ IMPORTANTE:
• Faça backup antes de usar o Modo Extremo
• O Modo Silencioso é ideal para automação
• Monitore o sistema após otimizações
"""
            
            self.history_text.delete("0.0", "end")
            self.history_text.insert("0.0", history)
            
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            self.history_text.delete("0.0", "end")
            self.history_text.insert("0.0", f"Erro ao carregar histórico: {e}")
    
    def save_settings(self):
        """Salva configurações"""
        try:
            settings = {
                "update_interval": self.update_interval_var.get(),
                "auto_start_monitoring": self.auto_start_var.get(),
                "auto_backup": self.auto_backup_var.get(),
                "double_confirm_extreme": self.double_confirm_var.get(),
                "create_restore_point": self.create_restore_var.get(),
                "saved_at": datetime.now().isoformat()
            }
            
            with open("special_modes_settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("💾 Configurações Salvas", "Todas as configurações foram salvas com sucesso!")
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao salvar configurações:\\n{e}")
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"1000x800+{x}+{y}")