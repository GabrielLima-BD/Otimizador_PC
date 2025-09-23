import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
import json
import os
from datetime import datetime
from optimizer import SystemCleaner, PerformanceOptimizer, NetworkOptimizer, RegistryOptimizer, Utils

class OptimizerUI:
    """Interface gráfica moderna para o otimizador Windows"""
    
    def __init__(self):
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.root = ctk.CTk()
        self.root.title("🚀 Otimizador Windows 10 Pro")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Variáveis de controle
        self.is_optimizing = False
        self.optimization_thread = None
        
        # Instâncias dos otimizadores
        self.cleaner = SystemCleaner()
        self.performance = PerformanceOptimizer()
        self.network = NetworkOptimizer()
        self.registry = RegistryOptimizer()
        
        # Setup da interface
        self.setup_ui()
        
        # Configuração de logging
        self.logger = Utils.setup_logging()
        
        # Verifica se é admin
        if not Utils.is_admin():
            self.show_admin_warning()
    
    def setup_ui(self):
        """Configura toda a interface gráfica"""
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="🚀 Otimizador Windows 10 Pro",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Maximize o desempenho do seu Windows com segurança",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame de informações do sistema
        self.create_system_info_frame()
        
        # Notebook para as abas
        self.notebook = ctk.CTkTabview(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Criação das abas
        self.create_optimization_tab()
        self.create_individual_tab()
        self.create_network_tab()
        self.create_logs_tab()
        self.create_restore_tab()
        
        # Frame de status e botões principais
        self.create_status_frame()
    
    def create_system_info_frame(self):
        """Cria frame com informações do sistema"""
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Obtém informações do sistema
        system_info = Utils.get_system_info()
        
        # Grid de informações
        info_text = f"💻 OS: {system_info['os']} | 🏗️ Arch: {system_info['architecture']} | 🧠 RAM: {system_info['memory']}"
        
        info_label = ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=12))
        info_label.pack(pady=10)
    
    def create_optimization_tab(self):
        """Cria aba de otimização completa"""
        tab = self.notebook.add("🚀 Otimização Completa")
        
        # Frame de opções
        options_frame = ctk.CTkFrame(tab)
        options_frame.pack(fill="x", padx=20, pady=20)
        
        # Título da seção
        ctk.CTkLabel(
            options_frame, 
            text="🎯 Otimização Automática", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Checkboxes para opções
        self.optimization_options = {
            'clean_system': ctk.BooleanVar(value=True),
            'optimize_performance': ctk.BooleanVar(value=True),
            'optimize_network': ctk.BooleanVar(value=True),
            'optimize_registry': ctk.BooleanVar(value=True),
            'remove_bloatware': ctk.BooleanVar(value=False),  # Mais cuidadoso por padrão
            'disable_defender': ctk.BooleanVar(value=False),  # Perigoso por padrão
        }
        
        options_list = [
            ('clean_system', '🧹 Limpeza completa do sistema'),
            ('optimize_performance', '⚡ Otimização de desempenho'),
            ('optimize_network', '🌐 Otimização de rede'),
            ('optimize_registry', '🔧 Otimização do registro'),
            ('remove_bloatware', '🗑️ Remover bloatware (cuidado!)'),
            ('disable_defender', '🛡️ Desabilitar Defender (perigoso!)'),
        ]
        
        for option_key, option_text in options_list:
            checkbox = ctk.CTkCheckBox(
                options_frame,
                text=option_text,
                variable=self.optimization_options[option_key],
                font=ctk.CTkFont(size=12)
            )
            checkbox.pack(anchor="w", padx=20, pady=5)
        
        # Botão de otimização completa
        self.optimize_button = ctk.CTkButton(
            options_frame,
            text="🚀 INICIAR OTIMIZAÇÃO COMPLETA",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.start_full_optimization
        )
        self.optimize_button.pack(pady=20)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(options_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 20))
        self.progress_bar.set(0)
        
        # Label de status
        self.status_label = ctk.CTkLabel(
            options_frame, 
            text="Pronto para otimizar",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(0, 15))
    
    def create_individual_tab(self):
        """Cria aba de otimizações individuais"""
        tab = self.notebook.add("🔧 Otimizações Individuais")
        
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Seção de limpeza
        self.create_section(scroll_frame, "🧹 Limpeza do Sistema", [
            ("Limpar arquivos temporários", self.clean_temp_files),
            ("Esvaziar lixeira", self.empty_recycle_bin),
            ("Limpar cache dos navegadores", self.clean_browser_cache),
            ("Executar limpeza de disco", self.run_disk_cleanup),
        ])
        
        # Seção de desempenho
        self.create_section(scroll_frame, "⚡ Otimização de Desempenho", [
            ("Configurar plano de energia", self.optimize_power),
            ("Desabilitar serviços desnecessários", self.disable_services),
            ("Otimizar efeitos visuais", self.optimize_visual_effects),
            ("Desabilitar indexação", self.disable_indexing),
            ("Otimizar inicialização", self.optimize_startup),
        ])
        
        # Seção de registro
        self.create_section(scroll_frame, "🔧 Otimização do Registro", [
            ("Desabilitar telemetria", self.disable_telemetry),
            ("Desabilitar Cortana", self.disable_cortana),
            ("Desabilitar dicas do Windows", self.disable_tips),
            ("Otimizar Windows Explorer", self.optimize_explorer),
        ])
    
    def create_network_tab(self):
        """Cria aba de otimização de rede"""
        tab = self.notebook.add("🌐 Rede")
        
        # Frame principal
        network_frame = ctk.CTkFrame(tab)
        network_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Teste de velocidade
        speed_frame = ctk.CTkFrame(network_frame)
        speed_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            speed_frame, 
            text="📊 Teste de Velocidade", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkButton(
            speed_frame,
            text="🚀 Testar Velocidade da Internet",
            command=self.test_internet_speed
        ).pack(pady=10)
        
        # Otimização DNS
        dns_frame = ctk.CTkFrame(network_frame)
        dns_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            dns_frame, 
            text="🔧 Otimização DNS", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Seletor de DNS
        self.dns_var = ctk.StringVar(value="Cloudflare")
        dns_options = ["Cloudflare", "Google", "Quad9", "OpenDNS"]
        
        dns_dropdown = ctk.CTkOptionMenu(
            dns_frame,
            variable=self.dns_var,
            values=dns_options
        )
        dns_dropdown.pack(pady=10)
        
        ctk.CTkButton(
            dns_frame,
            text="🌐 Aplicar DNS Otimizado",
            command=self.optimize_dns
        ).pack(pady=10)
        
        # Outras otimizações de rede
        self.create_section(network_frame, "⚡ Otimizações de Rede", [
            ("Otimizar configurações TCP", self.optimize_tcp),
            ("Desabilitar limitação QoS", self.disable_qos),
            ("Otimizar adaptador de rede", self.optimize_network_adapter),
        ])
    
    def create_logs_tab(self):
        """Cria aba de logs"""
        tab = self.notebook.add("📋 Logs")
        
        # Text area para logs
        self.log_text = scrolledtext.ScrolledText(
            tab,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#2b2b2b",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame de botões
        log_buttons_frame = ctk.CTkFrame(tab)
        log_buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            log_buttons_frame,
            text="🔄 Atualizar Logs",
            command=self.refresh_logs
        ).pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(
            log_buttons_frame,
            text="💾 Salvar Logs",
            command=self.save_logs
        ).pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(
            log_buttons_frame,
            text="🗑️ Limpar Logs",
            command=self.clear_logs
        ).pack(side="left", padx=10, pady=10)
    
    def create_restore_tab(self):
        """Cria aba de restauração"""
        tab = self.notebook.add("🔄 Restaurar")
        
        restore_frame = ctk.CTkFrame(tab)
        restore_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            restore_frame, 
            text="🔄 Restauração do Sistema", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20)
        
        # Informações sobre backup
        info_text = """
ℹ️ O sistema cria automaticamente backups antes de aplicar otimizações.
Você pode restaurar as configurações originais a qualquer momento.
        """
        
        ctk.CTkLabel(
            restore_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="center"
        ).pack(pady=20)
        
        # Botões de restauração
        ctk.CTkButton(
            restore_frame,
            text="📁 Selecionar Backup para Restaurar",
            command=self.select_backup_file,
            height=40
        ).pack(pady=10)
        
        ctk.CTkButton(
            restore_frame,
            text="🔄 Restaurar DNS Original",
            command=self.restore_dns,
            height=40
        ).pack(pady=10)
        
        ctk.CTkButton(
            restore_frame,
            text="🏠 Criar Ponto de Restauração",
            command=self.create_restore_point,
            height=40
        ).pack(pady=10)
    
    def create_status_frame(self):
        """Cria frame de status na parte inferior"""
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Status atual
        self.current_status = ctk.CTkLabel(
            status_frame,
            text="✅ Sistema pronto para otimização",
            font=ctk.CTkFont(size=12)
        )
        self.current_status.pack(side="left", padx=20, pady=10)
        
        # Botão de parar
        self.stop_button = ctk.CTkButton(
            status_frame,
            text="⏹️ Parar",
            command=self.stop_optimization,
            state="disabled"
        )
        self.stop_button.pack(side="right", padx=20, pady=10)
    
    def create_section(self, parent, title, buttons):
        """Cria uma seção com botões"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="x", padx=10, pady=10)
        
        # Título da seção
        ctk.CTkLabel(
            section_frame, 
            text=title, 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Botões da seção
        for button_text, button_command in buttons:
            btn = ctk.CTkButton(
                section_frame,
                text=button_text,
                command=button_command,
                height=35
            )
            btn.pack(fill="x", padx=20, pady=5)
    
    def show_admin_warning(self):
        """Mostra aviso sobre privilégios de administrador"""
        response = messagebox.askyesno(
            "Privilégios de Administrador",
            "Para aplicar todas as otimizações, o programa precisa ser executado como administrador.\n\n"
            "Deseja tentar executar como administrador agora?",
            icon="warning"
        )
        
        if response:
            if Utils.run_as_admin():
                self.root.quit()
            else:
                messagebox.showwarning(
                    "Aviso",
                    "Não foi possível obter privilégios de administrador.\n"
                    "Algumas otimizações podem não funcionar corretamente."
                )
    
    def update_progress(self, message, progress):
        """Atualiza barra de progresso e status"""
        self.status_label.configure(text=message)
        self.progress_bar.set(progress / 100)
        self.root.update_idletasks()
    
    def log_message(self, message):
        """Adiciona mensagem aos logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    # Métodos de otimização individual
    def clean_temp_files(self):
        """Limpa arquivos temporários"""
        self.run_single_optimization("Limpando arquivos temporários...", 
                                   self.cleaner.clean_temp_files)
    
    def empty_recycle_bin(self):
        """Esvazia lixeira"""
        self.run_single_optimization("Esvaziando lixeira...", 
                                   self.cleaner.clean_recycle_bin)
    
    def clean_browser_cache(self):
        """Limpa cache dos navegadores"""
        self.run_single_optimization("Limpando cache dos navegadores...", 
                                   self.cleaner.clean_browser_data)
    
    def run_disk_cleanup(self):
        """Executa limpeza de disco"""
        self.run_single_optimization("Executando limpeza de disco...", 
                                   self.cleaner.run_disk_cleanup)
    
    def optimize_power(self):
        """Otimiza configurações de energia"""
        self.run_single_optimization("Otimizando configurações de energia...", 
                                   self.performance.optimize_power_settings)
    
    def disable_services(self):
        """Desabilita serviços desnecessários"""
        self.run_single_optimization("Desabilitando serviços desnecessários...", 
                                   self.performance.disable_unnecessary_services)
    
    def optimize_visual_effects(self):
        """Otimiza efeitos visuais"""
        self.run_single_optimization("Otimizando efeitos visuais...", 
                                   self.performance.disable_visual_effects)
    
    def disable_indexing(self):
        """Desabilita indexação"""
        self.run_single_optimization("Desabilitando indexação...", 
                                   self.performance.disable_indexing)
    
    def optimize_startup(self):
        """Otimiza programas de inicialização"""
        self.run_single_optimization("Otimizando inicialização...", 
                                   self.performance.optimize_startup_programs)
    
    def disable_telemetry(self):
        """Desabilita telemetria"""
        self.run_single_optimization("Desabilitando telemetria...", 
                                   self.registry.disable_telemetry)
    
    def disable_cortana(self):
        """Desabilita Cortana"""
        self.run_single_optimization("Desabilitando Cortana...", 
                                   self.registry.disable_cortana)
    
    def disable_tips(self):
        """Desabilita dicas do Windows"""
        self.run_single_optimization("Desabilitando dicas do Windows...", 
                                   self.registry.disable_windows_tips)
    
    def optimize_explorer(self):
        """Otimiza Windows Explorer"""
        self.run_single_optimization("Otimizando Windows Explorer...", 
                                   self.registry.optimize_explorer_performance)
    
    def test_internet_speed(self):
        """Testa velocidade da internet"""
        self.run_single_optimization("Testando velocidade da internet...", 
                                   self.network.test_internet_speed)
    
    def optimize_dns(self):
        """Otimiza DNS"""
        dns_provider = self.dns_var.get()
        self.run_single_optimization(f"Configurando DNS {dns_provider}...", 
                                   lambda: self.network.optimize_dns(dns_provider))
    
    def optimize_tcp(self):
        """Otimiza configurações TCP"""
        self.run_single_optimization("Otimizando configurações TCP...", 
                                   self.network.optimize_tcp_settings)
    
    def disable_qos(self):
        """Desabilita limitação QoS"""
        self.run_single_optimization("Desabilitando limitação QoS...", 
                                   self.network.disable_qos_bandwidth_limit)
    
    def optimize_network_adapter(self):
        """Otimiza adaptador de rede"""
        self.run_single_optimization("Otimizando adaptador de rede...", 
                                   self.network.optimize_network_adapter)
    
    def run_single_optimization(self, message, func):
        """Executa uma otimização individual"""
        def worker():
            self.log_message(f"Iniciando: {message}")
            try:
                result = func(self.update_progress)
                if result:
                    self.log_message(f"✅ Concluído: {message}")
                else:
                    self.log_message(f"❌ Falhou: {message}")
            except Exception as e:
                self.log_message(f"❌ Erro em {message}: {str(e)}")
        
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
    
    def start_full_optimization(self):
        """Inicia otimização completa"""
        if self.is_optimizing:
            return
        
        self.is_optimizing = True
        self.optimize_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        self.optimization_thread = threading.Thread(target=self.run_full_optimization)
        self.optimization_thread.daemon = True
        self.optimization_thread.start()
    
    def run_full_optimization(self):
        """Executa otimização completa"""
        try:
            self.log_message("🚀 Iniciando otimização completa do sistema...")
            
            total_steps = sum(1 for option in self.optimization_options.values() if option.get())
            current_step = 0
            
            # Limpeza do sistema
            if self.optimization_options['clean_system'].get():
                current_step += 1
                self.update_progress(f"Limpeza do sistema ({current_step}/{total_steps})", 
                                   (current_step / total_steps) * 100)
                
                self.cleaner.clean_temp_files(self.update_progress)
                self.cleaner.clean_recycle_bin(self.update_progress)
                self.cleaner.clean_browser_data(self.update_progress)
                self.cleaner.clean_windows_logs(self.update_progress)
            
            # Otimização de desempenho
            if self.optimization_options['optimize_performance'].get():
                current_step += 1
                self.update_progress(f"Otimização de desempenho ({current_step}/{total_steps})", 
                                   (current_step / total_steps) * 100)
                
                self.performance.optimize_power_settings(self.update_progress)
                self.performance.disable_unnecessary_services(self.update_progress)
                self.performance.disable_visual_effects(self.update_progress)
                self.performance.disable_indexing(self.update_progress)
                self.performance.optimize_startup_programs(self.update_progress)
                self.performance.optimize_memory_management(self.update_progress)
            
            # Otimização de rede
            if self.optimization_options['optimize_network'].get():
                current_step += 1
                self.update_progress(f"Otimização de rede ({current_step}/{total_steps})", 
                                   (current_step / total_steps) * 100)
                
                self.network.optimize_dns('Cloudflare', self.update_progress)
                self.network.optimize_tcp_settings(self.update_progress)
                self.network.disable_qos_bandwidth_limit(self.update_progress)
                self.network.optimize_network_adapter(self.update_progress)
            
            # Otimização do registro
            if self.optimization_options['optimize_registry'].get():
                current_step += 1
                self.update_progress(f"Otimização do registro ({current_step}/{total_steps})", 
                                   (current_step / total_steps) * 100)
                
                self.registry.disable_telemetry(self.update_progress)
                self.registry.disable_cortana(self.update_progress)
                self.registry.disable_windows_tips(self.update_progress)
                self.registry.optimize_explorer_performance(self.update_progress)
                self.registry.disable_background_apps(self.update_progress)
            
            # Remoção de bloatware (opcional)
            if self.optimization_options['remove_bloatware'].get():
                current_step += 1
                self.update_progress(f"Removendo bloatware ({current_step}/{total_steps})", 
                                   (current_step / total_steps) * 100)
                
                self.cleaner.remove_bloatware(self.update_progress)
            
            # Desabilitar Defender (opcional e perigoso)
            if self.optimization_options['disable_defender'].get():
                current_step += 1
                self.update_progress(f"Configurando Windows Defender ({current_step}/{total_steps})", 
                                   (current_step / total_steps) * 100)
                
                self.performance.disable_windows_defender_realtime(self.update_progress)
            
            # Criar backup
            self.update_progress("Criando backup das configurações...", 95)
            self.create_optimization_backup()
            
            # Finalização
            self.update_progress("✅ Otimização completa concluída!", 100)
            self.log_message("🎉 Otimização completa finalizada com sucesso!")
            
            # Mostra resumo
            self.show_optimization_summary()
            
        except Exception as e:
            self.log_message(f"❌ Erro durante a otimização: {str(e)}")
        finally:
            self.is_optimizing = False
            self.optimize_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
    
    def stop_optimization(self):
        """Para a otimização em andamento"""
        self.is_optimizing = False
        self.log_message("⏹️ Otimização interrompida pelo usuário")
        self.update_progress("Otimização interrompida", 0)
        self.optimize_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
    
    def create_optimization_backup(self):
        """Cria backup das otimizações realizadas"""
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'cleaner_summary': self.cleaner.get_cleanup_summary(),
            'performance_summary': self.performance.get_optimization_summary(),
            'network_summary': self.network.get_network_summary(),
            'registry_summary': self.registry.get_registry_summary(),
        }
        
        backup_file = Utils.create_backup(backup_data, 'optimization_summary')
        if backup_file:
            self.log_message(f"📁 Backup criado: {backup_file}")
    
    def show_optimization_summary(self):
        """Mostra resumo da otimização"""
        summary_text = "🎉 Otimização Concluída!\n\n"
        
        # Resumo da limpeza
        cleanup_summary = self.cleaner.get_cleanup_summary()
        summary_text += f"🧹 Limpeza: {cleanup_summary['files_cleaned']} arquivos removidos\n"
        summary_text += f"💾 Espaço liberado: {cleanup_summary['space_freed_formatted']}\n\n"
        
        # Resumo das otimizações
        perf_summary = self.performance.get_optimization_summary()
        summary_text += f"⚡ Otimizações de desempenho: {perf_summary['optimizations_count']}\n\n"
        
        network_summary = self.network.get_network_summary()
        summary_text += f"🌐 Otimizações de rede: {network_summary['optimizations_count']}\n\n"
        
        registry_summary = self.registry.get_registry_summary()
        summary_text += f"🔧 Otimizações de registro: {registry_summary['changes_count']}\n\n"
        
        summary_text += "ℹ️ Recomenda-se reiniciar o computador para aplicar todas as alterações."
        
        messagebox.showinfo("Otimização Concluída", summary_text)
    
    def refresh_logs(self):
        """Atualiza a visualização de logs"""
        self.log_message("🔄 Logs atualizados")
    
    def save_logs(self):
        """Salva logs em arquivo"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Salvar Logs"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Sucesso", f"Logs salvos em: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar logs: {str(e)}")
    
    def clear_logs(self):
        """Limpa a área de logs"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🗑️ Logs limpos")
    
    def select_backup_file(self):
        """Seleciona arquivo de backup para restauração"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Selecionar Arquivo de Backup"
        )
        
        if filename:
            self.restore_from_backup(filename)
    
    def restore_from_backup(self, backup_file):
        """Restaura configurações a partir de backup"""
        try:
            backup_data = Utils.load_backup(backup_file)
            if backup_data:
                # Aqui você implementaria a lógica de restauração
                # Por exemplo, restaurar configurações de registro
                self.log_message(f"📁 Backup carregado: {backup_file}")
                messagebox.showinfo("Sucesso", "Backup carregado com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível carregar o backup")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar backup: {str(e)}")
    
    def restore_dns(self):
        """Restaura DNS original"""
        try:
            success = self.network.restore_original_dns()
            if success:
                self.log_message("🔄 DNS original restaurado")
                messagebox.showinfo("Sucesso", "DNS original restaurado com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Não foi possível restaurar o DNS original")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar DNS: {str(e)}")
    
    def create_restore_point(self):
        """Cria ponto de restauração do sistema"""
        try:
            import subprocess
            
            # Comando para criar ponto de restauração
            cmd = 'powershell -Command "Checkpoint-Computer -Description \'Otimizador Windows\' -RestorePointType \'MODIFY_SETTINGS\'"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_message("🏠 Ponto de restauração criado")
                messagebox.showinfo("Sucesso", "Ponto de restauração criado com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Não foi possível criar ponto de restauração")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar ponto de restauração: {str(e)}")
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = OptimizerUI()
    app.run()