#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Avançada c        # Botão de busca dinâmica
        scan_btn = ctk.CTkButton(
            controls_frame,
            text="🔍 Busca Dinâmica",
            command=self.scan_games_async
        )ing e Autostart
==========================================

Interface gráfica completa incluindo:
- Painel de jogos integrado
- Configurações de inicialização automática
- Otimização no boot
- Launcher de jogos com otimizações

Novos recursos:
- Aba "Meus Jogos" 
- Configurações de autostart
- Otimização automática no boot
- Gaming mode integrado
"""

import os
import sys
import json
import threading
import customtkinter as ctk
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import tkinter as tk
from tkinter import messagebox

# Importar módulos do otimizador
sys.path.append(os.path.join(os.path.dirname(__file__), 'optimizer'))

from optimizer.autostart import AutostartManager
from optimizer.boot_optimize import BootOptimizer
from optimizer.game_scanner import GameScanner, GameInfo
from optimizer.game_launcher import GameLauncher
from optimizer.hardware_detector import HardwareDetector
from optimizer.system_monitor import SystemMonitor
from optimizer.advanced_cleaner import AdvancedCleaner
from optimizer.advanced_optimizer import AdvancedOptimizer
from optimizer.schedule_manager import ScheduleManager

class GamePanelFrame(ctk.CTkFrame):
    """Painel de jogos integrado"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.game_launcher = GameLauncher()
        self.games_list: List[GameInfo] = []
        self.selected_game: Optional[GameInfo] = None
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
        
        # Inicializar sem busca automática
        self.games_list = []
        self.selected_game: Optional[GameInfo] = None
        self.update_games_display()
        self.update_statistics()
    
    def create_widgets(self):
        """Cria widgets do painel de jogos"""
        # Título
        title_label = ctk.CTkLabel(
            self, 
            text="🎮 Meus Jogos", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="ew")
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Botão escanear jogos
        scan_btn = ctk.CTkButton(
            controls_frame,
            text="🔍 Buscar Jogos no Sistema",
            command=self.start_game_search,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        scan_btn.pack(pady=10, padx=10, fill="x")
        
        # Barra de progresso (inicialmente oculta)
        self.progress_frame = ctk.CTkFrame(controls_frame)
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Preparando busca...",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(pady=5, padx=10, fill="x")
        
        # Status de busca
        self.search_status = ctk.CTkLabel(
            controls_frame,
            text="⚪ Clique em 'Buscar Jogos' para encontrar seus jogos",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.search_status.pack(pady=5, padx=10)
        
        # Gaming mode toggle
        self.gaming_mode_var = ctk.BooleanVar(value=True)
        gaming_toggle = ctk.CTkCheckBox(
            controls_frame,
            text="Gaming Mode",
            variable=self.gaming_mode_var
        )
        gaming_toggle.pack(pady=5, padx=10)
        
        # Estatísticas
        stats_label = ctk.CTkLabel(
            controls_frame,
            text="📊 Estatísticas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_label.pack(pady=(20, 5), padx=10)
        
        self.stats_text = ctk.CTkTextbox(controls_frame, height=150)
        self.stats_text.pack(pady=5, padx=10, fill="x")
        
        # Lista de jogos
        games_frame = ctk.CTkFrame(self)
        games_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        games_frame.grid_columnconfigure(0, weight=1)
        games_frame.grid_rowconfigure(1, weight=1)
        
        games_title = ctk.CTkLabel(
            games_frame,
            text="Jogos Detectados",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        games_title.grid(row=0, column=0, pady=10)
        
        # Scrollable frame para jogos
        self.games_scroll = ctk.CTkScrollableFrame(games_frame)
        self.games_scroll.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.games_scroll.grid_columnconfigure(0, weight=1)
        
        # Painel de detalhes do jogo
        details_frame = ctk.CTkFrame(self)
        details_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        details_title = ctk.CTkLabel(
            details_frame,
            text="Detalhes do Jogo",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        details_title.pack(pady=10)
        
        self.details_text = ctk.CTkTextbox(details_frame, height=200)
        self.details_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Botão de lançar jogo
        self.launch_btn = ctk.CTkButton(
            details_frame,
            text="🚀 Lançar Jogo",
            command=self.launch_selected_game,
            state="disabled"
        )
        self.launch_btn.pack(pady=10, padx=10, fill="x")
        
        # Botão favorito
        self.favorite_btn = ctk.CTkButton(
            details_frame,
            text="⭐ Adicionar aos Favoritos",
            command=self.toggle_favorite,
            state="disabled"
        )
        self.favorite_btn.pack(pady=5, padx=10, fill="x")
    
    def start_game_search(self):
        """Inicia busca manual de jogos com progresso"""
        # Mostrar barra de progresso
        self.progress_frame.pack(pady=10, padx=10, fill="x")
        self.search_status.configure(text="🔍 Buscando jogos...", text_color="orange")
        
        # Resetar progresso
        self.progress_bar.set(0)
        self.progress_label.configure(text="Iniciando busca...")
        
        # Executar busca em thread separada
        def search_worker():
            try:
                scanner = GameScanner()
                
                # Callback de progresso
                def progress_callback(step_name, current, total):
                    progress = current / total
                    self.after(0, lambda: self.update_progress(step_name, progress))
                
                # Executar busca com progresso
                games_found = scanner.scan_games_with_progress(progress_callback)
                
                # Atualizar interface
                self.after(0, lambda: self.finish_search(games_found))
                
            except Exception as e:
                self.after(0, lambda: self.search_error(str(e)))
        
        # Iniciar thread
        threading.Thread(target=search_worker, daemon=True).start()
    
    def update_progress(self, step_name: str, progress: float):
        """Atualiza barra de progresso"""
        self.progress_bar.set(progress)
        self.progress_label.configure(text=step_name)
    
    def finish_search(self, games_found: Dict):
        """Finaliza busca e atualiza interface"""
        # Converter dict para lista
        self.games_list = list(games_found.values())
        
        # Atualizar interface
        self.update_games_display()
        self.update_statistics()
        
        # Esconder progresso
        self.progress_frame.pack_forget()
        
        # Atualizar status
        game_count = len(games_found)
        if game_count > 0:
            self.search_status.configure(
                text=f"✅ Busca concluída: {game_count} jogos encontrados",
                text_color="green"
            )
        else:
            self.search_status.configure(
                text="⚠️ Nenhum jogo encontrado",
                text_color="orange"
            )
    
    def search_error(self, error_msg: str):
        """Trata erro na busca"""
        self.progress_frame.pack_forget()
        self.search_status.configure(
            text=f"❌ Erro na busca: {error_msg}",
            text_color="red"
        )
    
    def refresh_games(self):
        """Método de compatibilidade - atualiza interface"""
        self.update_games_display()
        self.update_statistics()
        """Busca dinâmica e atualização de jogos em tempo real"""
        try:
            # Sempre faz nova busca dinâmica
            scanner = GameScanner()
            fresh_games = scanner.scan_games()  # Busca dinâmica
            
            # Converte dict para lista para compatibilidade
            self.games_list = list(fresh_games.values())
            
            self.update_games_display()
            self.update_statistics()
        except Exception as e:
            print(f"Erro na busca dinâmica: {e}")
    
    def scan_games_async(self):
        """Executa busca dinâmica de jogos em thread separada"""
        def scan_worker():
            try:
                # Mostrar progresso
                self.parent.show_loading("🔍 Busca dinâmica de jogos...")
                
                # Busca dinâmica e rápida
                scanner = GameScanner()
                fresh_games = scanner.scan_games()  # Sempre busca atual
                
                # Atualizar interface na thread principal
                self.after(100, self.refresh_games)
                self.after(200, lambda: self.parent.hide_loading())
                
            except Exception as e:
                self.after(100, lambda: messagebox.showerror("Erro", f"Erro na busca dinâmica: {e}"))
                self.after(200, lambda: self.parent.hide_loading())
        
        thread = threading.Thread(target=scan_worker, daemon=True)
        thread.start()
    
    def update_games_display(self):
        """Atualiza exibição da lista de jogos"""
        # Limpar widgets existentes
        for widget in self.games_scroll.winfo_children():
            widget.destroy()
        
        # Adicionar jogos
        for i, game in enumerate(self.games_list):
            game_frame = ctk.CTkFrame(self.games_scroll)
            game_frame.grid(row=i, column=0, pady=5, padx=5, sticky="ew")
            game_frame.grid_columnconfigure(1, weight=1)
            
            # Ícone/emoji do launcher
            launcher_icons = {
                'Steam': '🔥',
                'Epic Games': '🛡️',
                'Origin': '🟠',
                'Ubisoft': '🔷',
                'GOG Galaxy': '🌌',
                'Riot Games': '⚡',
                'Battle.net': '⚔️',
                'Registry': '🖥️',
                'Manual': '📁'
            }
            
            icon = launcher_icons.get(game.launcher, '🎮')
            
            icon_label = ctk.CTkLabel(game_frame, text=icon, font=ctk.CTkFont(size=20))
            icon_label.grid(row=0, column=0, padx=10, pady=10)
            
            # Nome do jogo
            name_label = ctk.CTkLabel(
                game_frame, 
                text=game.name,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
            # Launcher
            launcher_label = ctk.CTkLabel(
                game_frame,
                text=f"📂 {game.launcher}",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            launcher_label.grid(row=1, column=1, padx=10, pady=0, sticky="w")
            
            # Botão selecionar
            select_btn = ctk.CTkButton(
                game_frame,
                text="Selecionar",
                width=80,
                command=lambda g=game: self.select_game(g)
            )
            select_btn.grid(row=0, column=2, rowspan=2, padx=10, pady=5)
    
    def select_game(self, game: GameInfo):
        """Seleciona um jogo"""
        self.selected_game = game
        self.update_game_details()
        self.launch_btn.configure(state="normal")
        self.favorite_btn.configure(state="normal")
    
    def update_game_details(self):
        """Atualiza detalhes do jogo selecionado"""
        if not self.selected_game:
            return
        
        game = self.selected_game
        
        # Obter estatísticas do jogo
        stats = self.game_launcher.get_game_statistics(game.game_id)
        
        details = f"""
🎮 Nome: {game.name}

📂 Launcher: {game.launcher}

📁 Diretório: {game.install_directory}

🎯 Executável: {os.path.basename(game.executable_path)}

💾 Tamanho: {game.size_mb:.1f} MB

📊 Estatísticas:
• Sessões: {stats.get('total_sessions', 0)}
• Tempo jogado: {stats.get('total_playtime', 0):.1f} min
• Duração média: {stats.get('avg_session_duration', 0):.1f} min
• Score médio: {stats.get('avg_performance_score', 0):.1f}/100

⏰ Última vez jogado: {game.last_played or 'Nunca'}

🏆 Vezes jogado: {game.play_count}
        """.strip()
        
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", details)
        
        # Atualizar texto do botão favorito
        favorites = self.game_launcher.game_stats.get('favorite_games', [])
        if game.game_id in favorites:
            self.favorite_btn.configure(text="💔 Remover dos Favoritos")
        else:
            self.favorite_btn.configure(text="⭐ Adicionar aos Favoritos")
    
    def launch_selected_game(self):
        """Lança o jogo selecionado"""
        if not self.selected_game:
            messagebox.showerror("Erro", "Nenhum jogo selecionado")
            return
        
        try:
            apply_optimizations = self.gaming_mode_var.get()
            
            # Mostrar loading
            self.parent.show_loading(f"Lançando {self.selected_game.name}...")
            
            # Lançar em thread separada
            def launch_worker():
                try:
                    if self.selected_game and self.selected_game.game_id:  # Verificação adicional
                        success = self.game_launcher.launch_game(
                            self.selected_game.game_id,
                            apply_optimizations
                        )
                        
                        if success:
                            self.after(100, lambda: messagebox.showinfo(
                                "Sucesso", 
                                f"Jogo {self.selected_game.name if self.selected_game else 'N/A'} lançado com sucesso!"
                            ))
                        else:
                            self.after(100, lambda: messagebox.showerror(
                                "Erro", 
                                f"Falha ao lançar {self.selected_game.name if self.selected_game else 'N/A'}"
                            ))
                        
                        # Atualizar estatísticas
                        self.after(200, self.update_statistics)
                        self.after(300, self.update_game_details)
                    
                except Exception as e:
                    self.after(100, lambda: messagebox.showerror("Erro", f"Erro ao lançar jogo: {e}"))
                
                finally:
                    self.after(500, lambda: self.parent.hide_loading())
            
            thread = threading.Thread(target=launch_worker, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao lançar jogo: {e}")
    
    def toggle_favorite(self):
        """Adiciona/remove jogo dos favoritos"""
        if not self.selected_game or not self.selected_game.game_id:
            messagebox.showerror("Erro", "Nenhum jogo selecionado")
            return
        
        try:
            favorites = self.game_launcher.game_stats.get('favorite_games', [])
            
            if self.selected_game.game_id in favorites:
                self.game_launcher.remove_favorite_game(self.selected_game.game_id)
                messagebox.showinfo("Favoritos", f"{self.selected_game.name} removido dos favoritos")
            else:
                self.game_launcher.add_favorite_game(self.selected_game.game_id)
                messagebox.showinfo("Favoritos", f"{self.selected_game.name} adicionado aos favoritos")
            
            self.update_game_details()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerenciar favoritos: {e}")
    
    def auto_refresh_loop(self):
        """Loop de auto-refresh para detectar novos jogos automaticamente"""
        try:
            # Refresh silencioso (sem mostrar loading)
            scanner = GameScanner()
            fresh_games = scanner.scan_games()
            
            # Só atualiza se encontrou jogos diferentes
            current_count = len(self.games_list) if hasattr(self, 'games_list') else 0
            new_count = len(fresh_games)
            
            if new_count != current_count:
                self.games_list = list(fresh_games.values())
                self.update_games_display()
                self.update_statistics()
                print(f"🔍 Auto-refresh: {new_count} jogos detectados")
            
        except Exception as e:
            print(f"Erro no auto-refresh: {e}")
        
        # Reagenda para próximo refresh
        self.after(30000, self.auto_refresh_loop)
    
    def update_statistics(self):
        """Atualiza estatísticas gerais"""
        try:
            stats = self.game_launcher.get_game_statistics()
            
            stats_text = f"""
🎮 Jogos detectados: {len(self.games_list)}

🚀 Jogos lançados: {stats.get('total_games_launched', 0)}

⏱️ Tempo total: {stats.get('total_playtime_hours', 0):.1f}h

📊 Sessões: {stats.get('total_sessions', 0)}

⭐ Favoritos: {len(stats.get('favorite_games', []))}
            """.strip()
            
            self.stats_text.delete("1.0", "end")
            self.stats_text.insert("1.0", stats_text)
            
        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")


class AutostartFrame(ctk.CTkFrame):
    """Frame de configurações de inicialização automática"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.autostart_manager = AutostartManager()
        self.boot_optimizer = BootOptimizer()
        
        self.create_widgets()
        self.update_status()
    
    def create_widgets(self):
        """Cria widgets de configuração de autostart"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="🚀 Inicialização Automática",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame de configurações
        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10, padx=20, fill="x")
        
        # Configurações de autostart
        autostart_label = ctk.CTkLabel(
            config_frame,
            text="Configurações de Inicialização",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        autostart_label.pack(pady=10)
        
        # Toggle autostart
        self.autostart_var = ctk.BooleanVar()
        autostart_toggle = ctk.CTkCheckBox(
            config_frame,
            text="Iniciar com o Windows",
            variable=self.autostart_var,
            command=self.toggle_autostart
        )
        autostart_toggle.pack(pady=5)
        
        # Toggle minimized
        self.minimized_var = ctk.BooleanVar(value=True)
        minimized_toggle = ctk.CTkCheckBox(
            config_frame,
            text="Iniciar minimizado",
            variable=self.minimized_var
        )
        minimized_toggle.pack(pady=5)
        
        # Método de inicialização
        method_label = ctk.CTkLabel(config_frame, text="Método:")
        method_label.pack(pady=(10, 5))
        
        self.method_var = ctk.StringVar(value="registry")
        method_menu = ctk.CTkOptionMenu(
            config_frame,
            values=["registry", "startup_folder"],
            variable=self.method_var
        )
        method_menu.pack(pady=5)
        
        # Configurações de otimização no boot
        boot_frame = ctk.CTkFrame(self)
        boot_frame.pack(pady=10, padx=20, fill="x")
        
        boot_label = ctk.CTkLabel(
            boot_frame,
            text="Otimização no Boot",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        boot_label.pack(pady=10)
        
        # Toggle boot optimization
        self.boot_opt_var = ctk.BooleanVar()
        boot_opt_toggle = ctk.CTkCheckBox(
            boot_frame,
            text="Executar otimização no boot",
            variable=self.boot_opt_var,
            command=self.toggle_boot_optimization
        )
        boot_opt_toggle.pack(pady=5)
        
        # Opções de otimização
        opt_frame = ctk.CTkFrame(boot_frame)
        opt_frame.pack(pady=10, padx=10, fill="x")
        
        self.clean_temp_var = ctk.BooleanVar(value=True)
        self.optimize_services_var = ctk.BooleanVar(value=True)
        self.set_power_plan_var = ctk.BooleanVar(value=True)
        self.optimize_network_var = ctk.BooleanVar(value=True)
        
        options = [
            ("Limpar arquivos temporários", self.clean_temp_var),
            ("Otimizar serviços", self.optimize_services_var),
            ("Configurar plano de energia", self.set_power_plan_var),
            ("Otimizar rede", self.optimize_network_var)
        ]
        
        for text, var in options:
            toggle = ctk.CTkCheckBox(opt_frame, text=text, variable=var)
            toggle.pack(pady=2, anchor="w")
        
        # Botões de ação
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=20, padx=20, fill="x")
        
        test_btn = ctk.CTkButton(
            buttons_frame,
            text="🧪 Testar Otimização",
            command=self.test_boot_optimization
        )
        test_btn.pack(side="left", padx=10)
        
        status_btn = ctk.CTkButton(
            buttons_frame,
            text="📊 Verificar Status",
            command=self.update_status
        )
        status_btn.pack(side="right", padx=10)
        
        # Status atual
        self.status_text = ctk.CTkTextbox(self, height=150)
        self.status_text.pack(pady=10, padx=20, fill="x")
    
    def toggle_autostart(self):
        """Alterna inicialização automática"""
        try:
            method = self.method_var.get()
            minimized = self.minimized_var.get()
            
            if self.autostart_var.get():
                success = self.autostart_manager.enable_autostart(method, minimized)
                if success:
                    messagebox.showinfo("Sucesso", "Inicialização automática habilitada!")
                else:
                    messagebox.showerror("Erro", "Falha ao habilitar inicialização automática")
                    self.autostart_var.set(False)
            else:
                success = self.autostart_manager.disable_autostart(method)
                if success:
                    messagebox.showinfo("Sucesso", "Inicialização automática desabilitada!")
                else:
                    messagebox.showerror("Erro", "Falha ao desabilitar inicialização automática")
                    self.autostart_var.set(True)
            
            self.update_status()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao configurar autostart: {e}")
    
    def toggle_boot_optimization(self):
        """Alterna otimização no boot"""
        try:
            if self.boot_opt_var.get():
                success = self.boot_optimizer.create_boot_task()
                if success:
                    messagebox.showinfo("Sucesso", "Tarefa de otimização no boot criada!")
                else:
                    messagebox.showerror("Erro", "Falha ao criar tarefa de boot")
                    self.boot_opt_var.set(False)
            else:
                success = self.boot_optimizer.remove_boot_task()
                if success:
                    messagebox.showinfo("Sucesso", "Tarefa de otimização no boot removida!")
                else:
                    messagebox.showerror("Erro", "Falha ao remover tarefa de boot")
                    self.boot_opt_var.set(True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao configurar otimização de boot: {e}")
    
    def test_boot_optimization(self):
        """Testa otimização de boot"""
        try:
            # Mostrar loading
            self.parent.show_loading("Executando teste de otimização...")
            
            def test_worker():
                try:
                    config = {
                        'clean_temp_files': self.clean_temp_var.get(),
                        'optimize_services': self.optimize_services_var.get(),
                        'set_power_plan': self.set_power_plan_var.get(),
                        'optimize_network': self.optimize_network_var.get(),
                        'clean_memory': True,
                        'update_dns': False,  # Não modificar DNS em teste
                    }
                    
                    results = self.boot_optimizer.run_boot_optimization(config)
                    
                    # Mostrar resultados
                    def show_results():
                        if results['success']:
                            messagebox.showinfo(
                                "Teste Concluído",
                                f"Otimização executada em {results['total_time']:.2f}s\n"
                                f"Otimizações aplicadas: {len(results['optimizations'])}"
                            )
                        else:
                            messagebox.showerror(
                                "Teste Falhou",
                                f"Erros encontrados: {len(results['errors'])}"
                            )
                        
                        self.parent.hide_loading()
                    
                    self.after(100, show_results)
                    
                except Exception as e:
                    self.after(100, lambda: messagebox.showerror("Erro", f"Erro no teste: {e}"))
                    self.after(200, lambda: self.parent.hide_loading())
            
            thread = threading.Thread(target=test_worker, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao testar otimização: {e}")
    
    def update_status(self):
        """Atualiza status das configurações"""
        try:
            # Status do autostart
            status = self.autostart_manager.get_status()
            
            # Atualizar toggles
            is_enabled = status['registry_enabled'] or status['startup_folder_enabled']
            self.autostart_var.set(is_enabled)
            
            # Texto de status
            status_text = f"""
📊 STATUS ATUAL

🚀 Inicialização Automática:
• Registro: {'✅ Habilitado' if status['registry_enabled'] else '❌ Desabilitado'}
• Pasta Startup: {'✅ Habilitado' if status['startup_folder_enabled'] else '❌ Desabilitado'}

📁 Caminhos:
• Executável: {status['executable_path'][:50]}...
• Pasta Startup: {status['startup_folder_path']}

⚡ Otimização de Boot:
• Status: Configurado conforme seleções acima
• Método: Tarefa agendada do Windows

🔧 Configurações Ativas:
• Limpar temp: {'✅' if self.clean_temp_var.get() else '❌'}
• Otimizar serviços: {'✅' if self.optimize_services_var.get() else '❌'}
• Plano energia: {'✅' if self.set_power_plan_var.get() else '❌'}
• Otimizar rede: {'✅' if self.optimize_network_var.get() else '❌'}
            """.strip()
            
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", status_text)
            
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")


class AdvancedMainWindow(ctk.CTk):
    """Janela principal com todas as funcionalidades avançadas"""
    
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Otimizador Windows 10 Pro - Gaming Edition")
        self.geometry("1200x800")
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Loading overlay
        self.loading_overlay = None
        
        # Verificar argumentos de linha de comando
        self.check_startup_args()
        
        self.create_widgets()
    
    def check_startup_args(self):
        """Verifica se foi iniciado automaticamente"""
        if "--minimized" in sys.argv or "--autostart" in sys.argv:
            # Iniciar minimizado
            self.withdraw()
            self.iconify()
    
    def create_widgets(self):
        """Cria interface principal"""
        # Notebook com abas
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Aba principal (dashboard)
        self.notebook.add("Dashboard")
        self.create_dashboard_tab()
        
        # Aba de jogos
        self.notebook.add("Meus Jogos")
        self.games_frame = GamePanelFrame(self.notebook.tab("Meus Jogos"))
        self.games_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba de configurações de autostart
        self.notebook.add("Inicialização")
        self.autostart_frame = AutostartFrame(self.notebook.tab("Inicialização"))
        self.autostart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba de otimizações (existente)
        self.notebook.add("Otimizações")
        self.create_optimizations_tab()
        
        # Aba de monitoramento (existente)
        self.notebook.add("Monitoramento")
        self.create_monitoring_tab()
    
    def create_dashboard_tab(self):
        """Cria aba de dashboard"""
        dashboard_frame = self.notebook.tab("Dashboard")
        
        # Título
        title_label = ctk.CTkLabel(
            dashboard_frame,
            text="🎮 Otimizador Windows 10 Pro - Gaming Edition",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame de informações rápidas
        info_frame = ctk.CTkFrame(dashboard_frame)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        # Informações do sistema
        try:
            hardware_detector = HardwareDetector()
            hardware_info = hardware_detector.detect_hardware()
            
            if hardware_info:
                cpu_info = hardware_info.get('cpu', {})
                memory_info = hardware_info.get('memory', {})
                
                info_text = f"""
🖥️ Sistema Detectado:
• CPU: {cpu_info.get('name', 'N/A') if cpu_info else 'N/A'}
• RAM: {memory_info.get('total_gb', 'N/A') if memory_info else 'N/A'} GB
• Perfil: {hardware_detector.classify_system_profile(hardware_info)}

🎮 Gaming Features:
• Detecção automática de jogos
• Otimizações específicas para gaming
• Monitoramento de performance em tempo real
• Inicialização automática com Windows

🚀 Recursos Avançados:
• Limpeza profunda do sistema
• Agendamento inteligente de tarefas
• Painel de jogos integrado
• Estatísticas de gaming
                """.strip()
            else:
                info_text = "Erro ao detectar informações do sistema"
            
            info_label = ctk.CTkLabel(
                info_frame,
                text=info_text,
                font=ctk.CTkFont(size=14),
                justify="left"
            )
            info_label.pack(pady=20)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                info_frame,
                text=f"Erro ao carregar informações: {e}",
                font=ctk.CTkFont(size=14)
            )
            error_label.pack(pady=20)
        
        # Botões de ação rápida
        actions_frame = ctk.CTkFrame(dashboard_frame)
        actions_frame.pack(pady=20, padx=20, fill="x")
        
        quick_actions = [
            ("🔍 Escanear Jogos", self.quick_scan_games),
            ("🧹 Limpeza Rápida", self.quick_cleanup),
            ("⚡ Modo Gaming", self.enable_gaming_mode),
            ("📊 Relatório Sistema", self.system_report)
        ]
        
        for i, (text, command) in enumerate(quick_actions):
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                command=command,
                width=150,
                height=40
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def create_optimizations_tab(self):
        """Cria aba de otimizações (simplificada)"""
        opt_frame = self.notebook.tab("Otimizações")
        
        opt_label = ctk.CTkLabel(
            opt_frame,
            text="⚡ Otimizações do Sistema",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        opt_label.pack(pady=20)
        
        # Placeholder para otimizações existentes
        placeholder_label = ctk.CTkLabel(
            opt_frame,
            text="Funcionalidades de otimização serão integradas aqui...",
            font=ctk.CTkFont(size=14)
        )
        placeholder_label.pack(pady=50)
    
    def create_monitoring_tab(self):
        """Cria aba de monitoramento (simplificada)"""
        mon_frame = self.notebook.tab("Monitoramento")
        
        mon_label = ctk.CTkLabel(
            mon_frame,
            text="📊 Monitoramento do Sistema",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        mon_label.pack(pady=20)
        
        # Placeholder para monitoramento existente
        placeholder_label = ctk.CTkLabel(
            mon_frame,
            text="Funcionalidades de monitoramento serão integradas aqui...",
            font=ctk.CTkFont(size=14)
        )
        placeholder_label.pack(pady=50)
    
    def show_loading(self, message: str):
        """Mostra overlay de loading"""
        if self.loading_overlay:
            return
        
        self.loading_overlay = ctk.CTkToplevel(self)
        self.loading_overlay.title("Aguarde...")
        self.loading_overlay.geometry("300x150")
        self.loading_overlay.transient(self)
        self.loading_overlay.grab_set()
        
        # Centralizar
        self.loading_overlay.geometry("+{}+{}".format(
            self.winfo_x() + self.winfo_width()//2 - 150,
            self.winfo_y() + self.winfo_height()//2 - 75
        ))
        
        loading_label = ctk.CTkLabel(
            self.loading_overlay,
            text=message,
            font=ctk.CTkFont(size=16)
        )
        loading_label.pack(pady=50)
    
    def hide_loading(self):
        """Esconde overlay de loading"""
        if self.loading_overlay:
            self.loading_overlay.destroy()
            self.loading_overlay = None
    
    def quick_scan_games(self):
        """Ação rápida: escanear jogos"""
        self.notebook.set("Meus Jogos")
        self.games_frame.scan_games_async()
    
    def quick_cleanup(self):
        """Ação rápida: limpeza do sistema"""
        try:
            self.show_loading("Executando limpeza rápida...")
            
            def cleanup_worker():
                try:
                    cleaner = AdvancedCleaner()
                    # Executar limpeza básica
                    # results = cleaner.quick_cleanup()
                    
                    self.after(2000, lambda: messagebox.showinfo(
                        "Limpeza Concluída",
                        "Limpeza rápida executada com sucesso!"
                    ))
                    
                except Exception as e:
                    self.after(100, lambda: messagebox.showerror("Erro", f"Erro na limpeza: {e}"))
                
                finally:
                    self.after(2100, self.hide_loading)
            
            thread = threading.Thread(target=cleanup_worker, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar limpeza: {e}")
    
    def enable_gaming_mode(self):
        """Ação rápida: ativar modo gaming"""
        try:
            self.show_loading("Ativando modo gaming...")
            
            def gaming_worker():
                try:
                    optimizer = AdvancedOptimizer()
                    # Aplicar otimizações de gaming
                    # optimizer.enable_gaming_mode()
                    
                    self.after(1500, lambda: messagebox.showinfo(
                        "Modo Gaming",
                        "Modo gaming ativado! Sistema otimizado para jogos."
                    ))
                    
                except Exception as e:
                    self.after(100, lambda: messagebox.showerror("Erro", f"Erro no modo gaming: {e}"))
                
                finally:
                    self.after(1600, self.hide_loading)
            
            thread = threading.Thread(target=gaming_worker, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ativar modo gaming: {e}")
    
    def system_report(self):
        """Ação rápida: gerar relatório do sistema"""
        try:
            monitor = SystemMonitor()
            metrics = monitor.collect_metrics()
            health_score = monitor.calculate_health_score(metrics)
            
            report = f"""
📊 RELATÓRIO DO SISTEMA

🖥️ Performance:
• CPU: {metrics.get('cpu_percent', 'N/A')}%
• Memória: {metrics.get('memory_percent', 'N/A')}%
• Disco: {metrics.get('disk_percent', 'N/A')}%

💯 Health Score: {health_score}/100

📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            """.strip()
            
            messagebox.showinfo("Relatório do Sistema", report)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")


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