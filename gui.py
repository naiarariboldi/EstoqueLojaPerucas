import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from logger import log_error

# Configurações de cores e estilos
COLORS = {
    'primary': '#8B4A9C',     
    'secondary': '#D8BFD8',
    'accent': '#FF69B4',
    'background': '#F8F4FF',
    'surface': '#FFFFFF',
    'text_primary': '#2D1B3D',
    'text_secondary': '#6B4C7A',
    'success': '#4CAF50',
    'error': '#F44336',
    'warning': '#FF9800'
}

# Configuração das fontes
FONTS = {
    'title': ('Segoe UI', 18, 'bold'),
    'subtitle': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 11),
    'button': ('Segoe UI', 10, 'bold'),
    'small': ('Segoe UI', 9)
}

# Classe para configurações de estilo 

#Botão personalizado 
class StyledButton(tk.Button):
    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        if style == 'primary':
            bg_color = COLORS['primary']
            fg_color = 'white'
            active_bg = COLORS['accent']
        elif style == 'secondary':
            bg_color = COLORS['secondary']
            fg_color = COLORS['text_primary']
            active_bg = COLORS['primary']
        elif style == 'success':
            bg_color = COLORS['success']
            fg_color = 'white'
            active_bg = '#45a049'
        elif style == 'danger':
            bg_color = COLORS['error']
            fg_color = 'white'
            active_bg = '#da190b'
        else:
            bg_color = COLORS['surface']
            fg_color = COLORS['text_primary']
            active_bg = COLORS['secondary']
        
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            activebackground=active_bg,
            activeforeground='white',
            font=FONTS['button'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            **kwargs
        )
        
        self.bind('<Leave>', self._on_leave)
        self.original_bg = bg_color
        self.hover_bg = active_bg
    
    def _on_enter(self, event):
        self.config(bg=self.hover_bg)
    
    def _on_leave(self, event):
        self.config(bg=self.original_bg)

#Campod de entrada
class StyledEntry(tk.Entry):
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            font=FONTS['body'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightcolor=COLORS['primary'],
            highlightbackground=COLORS['secondary'],
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_color = COLORS['text_secondary']
        self.normal_color = COLORS['text_primary']
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=self.placeholder_color)
            self.bind('<FocusIn>', self._on_focus_in)
            self.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.normal_color)
    
    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def get_value(self):
        value = self.get()
        return value if value != self.placeholder else ""

#Janela de Login
class LoginWindow(tk.Toplevel):
    def __init__(self, master, db_manager, on_login_success):
        super().__init__(master)
        self.db_manager = db_manager
        self.on_login_success = on_login_success
        self.title("Login - Perucas Diferentonas")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.configure(bg=COLORS['background'])
        self.center_window()
        self.create_widgets()

    #Configurações da janela
    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)
        
        title_label = tk.Label(
            main_frame,
            text="🎭 Perucas Diferentonas",
            font=FONTS['title'],
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Faça login para continuar",
            font=FONTS['body'],
            bg=COLORS['background'],
            fg=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(0, 30))
        
        login_card = tk.Frame(main_frame, bg=COLORS['surface'], relief='solid', bd=1)
        login_card.pack(fill='x', pady=10)
        
        card_inner = tk.Frame(login_card, bg=COLORS['surface'])
        card_inner.pack(padx=30, pady=30)
        
        #Campos de entrada
        tk.Label(
            card_inner,
            text="Usuário",
            font=FONTS['body'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        self.username_entry = StyledEntry(card_inner, placeholder="Digite seu usuário")
        self.username_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        tk.Label(
            card_inner,
            text="Senha",
            font=FONTS['body'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        self.password_entry = StyledEntry(card_inner, show="*")
        self.password_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Botões de login e para abrir a janela de criar conta
        button_frame = tk.Frame(card_inner, bg=COLORS['surface'])
        button_frame.pack(fill='x')
        
        login_btn = StyledButton(button_frame, "Entrar", self.attempt_login, style='primary')
        login_btn.pack(fill='x', pady=(0, 10))
        
        signup_btn = StyledButton(button_frame, "Criar Conta", self.open_signup, style='secondary')
        signup_btn.pack(fill='x')

    # Valida credenciais do usuário
    def attempt_login(self):
        username = self.username_entry.get_value().strip()
        password = self.password_entry.get_value().strip()

        if not username or not password:
            messagebox.showerror("Erro", "Preencha usuário e senha.")
            return

        try:
            if self.db_manager.check_user_credentials(username, password):
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.destroy()
                self.on_login_success()
            else:
                messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")
                log_error(f"Tentativa de login falhou: {username}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível verificar o login: {e}")
            log_error(f"Erro ao verificar login: {e}")

    # Abre janela de cadastro
    def open_signup(self):
        SignUpWindow(self.master, self.db_manager)

#Janela para cadastro
class SignUpWindow(tk.Toplevel):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.title("Criar Conta - Perucas Diferentonas")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.configure(bg=COLORS['background'])
        self.center_window()
        self.create_widgets()

    # Configurações da janela de cadastro
    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)
        
        title_label = tk.Label(
            main_frame,
            text="Criar Nova Conta",
            font=FONTS['title'],
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        title_label.pack(pady=(0, 30))
        
        signup_card = tk.Frame(main_frame, bg=COLORS['surface'], relief='solid', bd=1)
        signup_card.pack(fill='x', pady=10)
        
        card_inner = tk.Frame(signup_card, bg=COLORS['surface'])
        card_inner.pack(padx=30, pady=30)
        
        # Campos 
        tk.Label(
            card_inner,
            text="Email",
            font=FONTS['body'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        self.email_entry = StyledEntry(card_inner, placeholder="Digite seu email")
        self.email_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        tk.Label(
            card_inner,
            text="Usuário",
            font=FONTS['body'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        self.username_entry = StyledEntry(card_inner, placeholder="Escolha um usuário")
        self.username_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        tk.Label(
            card_inner,
            text="Senha",
            font=FONTS['body'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        self.password_entry = StyledEntry(card_inner, show="*", placeholder="Crie uma senha")
        self.password_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        create_btn = StyledButton(card_inner, "Criar Conta", self.attempt_create, style='success')
        create_btn.pack(fill='x')

    # Cria um novo usuário
    def attempt_create(self):
        email = self.email_entry.get_value()
        username = self.username_entry.get_value()
        password = self.password_entry.get_value()

        if not email or not username or not password:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        try:
            self.db_manager.add_user(email, username, password)
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar a conta: {e}")
            log_error(f"Erro ao criar conta: {e}")

#Janela principal
class MainWindow(tk.Toplevel):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.title("Perucas Diferentonas - Gerenciamento de Produtos")
        self.geometry("1400x900")
        self.configure(bg=COLORS['background'])
        self.center_window()
        self.create_widgets()
        self.load_products()

    # Configura janela principal
    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    # Cria e configura a janela
    def create_widgets(self):
        header_frame = tk.Frame(self, bg=COLORS['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=COLORS['primary'])
        header_content.pack(expand=True, fill='both', padx=30, pady=15)
        
        title_label = tk.Label(
            header_content,
            text="🎭 Perucas Diferentonas",
            font=FONTS['title'],
            bg=COLORS['primary'],
            fg='white'
        )
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(
            header_content,
            text="Sistema de Gerenciamento",
            font=FONTS['body'],
            bg=COLORS['primary'],
            fg=COLORS['secondary']
        )
        subtitle_label.pack(side='left', padx=(10, 0))
        
        main_container = tk.Frame(self, bg=COLORS['background'])
        main_container.pack(expand=True, fill='both', padx=30, pady=20)
        
        controls_frame = tk.Frame(main_container, bg=COLORS['surface'], relief='solid', bd=1)
        controls_frame.pack(fill='x', pady=(0, 20))
        
        controls_inner = tk.Frame(controls_frame, bg=COLORS['surface'])
        controls_inner.pack(padx=20, pady=15)
        
        controls_title = tk.Label(
            controls_inner,
            text="Controles de Produto",
            font=FONTS['subtitle'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        )
        controls_title.pack(anchor='w', pady=(0, 15))
        
        #Botões
        buttons_frame = tk.Frame(controls_inner, bg=COLORS['surface'])
        buttons_frame.pack(fill='x')
        
        StyledButton(buttons_frame, "➕ Adicionar", self.add_product, style='success').pack(side='left', padx=(0, 10))
        StyledButton(buttons_frame, "✏️ Atualizar", self.update_product, style='primary').pack(side='left', padx=(0, 10))
        StyledButton(buttons_frame, "🗑️ Deletar", self.delete_product, style='danger').pack(side='left', padx=(0, 10))
        StyledButton(buttons_frame, "🔄 Recarregar", self.load_products, style='secondary').pack(side='left')
        
        # Container de conteúdo lista e gráfico
        content_frame = tk.Frame(main_container, bg=COLORS['background'])
        content_frame.pack(expand=True, fill='both')
        
        # Lista de produtos
        list_frame = tk.Frame(content_frame, bg=COLORS['surface'], relief='solid', bd=1)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        list_header = tk.Frame(list_frame, bg=COLORS['surface'])
        list_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(
            list_header,
            text="📋 Lista de Produtos",
            font=FONTS['subtitle'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w')
        
        text_container = tk.Frame(list_frame, bg=COLORS['surface'])
        text_container.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        self.product_list_text = tk.Text(
            text_container,
            font=FONTS['small'],
            bg=COLORS['background'],
            fg=COLORS['text_primary'],
            relief='solid',
            bd=1,
            wrap='none',
            state=tk.DISABLED
        )
        
        scrollbar_y = tk.Scrollbar(text_container, orient='vertical', command=self.product_list_text.yview)
        scrollbar_x = tk.Scrollbar(text_container, orient='horizontal', command=self.product_list_text.xview)
        
        self.product_list_text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.product_list_text.pack(side='left', expand=True, fill='both')
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        
        # Gráfico
        chart_frame = tk.Frame(content_frame, bg=COLORS['surface'], relief='solid', bd=1, width=500)
        chart_frame.pack(side='right', fill='y')
        chart_frame.pack_propagate(False)
        
        chart_header = tk.Frame(chart_frame, bg=COLORS['surface'])
        chart_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(
            chart_header,
            text="📊 Análise de Estoque",
            font=FONTS['subtitle'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary']
        ).pack(anchor='w')
        
        self.chart_container = tk.Frame(chart_frame, bg=COLORS['surface'])
        self.chart_container.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        # Configura biblioteca com tema personalizado
        plt.style.use('default')
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.fig.patch.set_facecolor(COLORS['surface'])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.plot_sales_data()

    # Carrega produtos
    def load_products(self):
        self.product_list_text.config(state=tk.NORMAL)
        self.product_list_text.delete(1.0, tk.END)
        
        header = f"{'ID':<5} {'Nome':<25} {'Preço':<12} {'Estoque':<10}\n"
        separator = "─" * 60 + "\n"
        
        self.product_list_text.insert(tk.END, header)
        self.product_list_text.insert(tk.END, separator)
        
        #dados
        products = self.db_manager.get_products()
        if products:
            for p in products:
                name = p['nome'][:23] + "..." if len(p['nome']) > 23 else p['nome']
                
                line = f"{p['id']:<5} {name:<25} R$ {p['preco']:<8.2f} {p['estoque']:<10}\n"
                self.product_list_text.insert(tk.END, line)
        else:
            self.product_list_text.insert(tk.END, "\n" + " " * 20 + "Nenhum produto cadastrado.\n")
        
        self.product_list_text.config(state=tk.DISABLED)
        self.plot_sales_data()

    # Adiciona produto
    def add_product(self):
        dialog = ProductDialog(self, "Adicionar Produto")
        if dialog.result:
            try:
                self.db_manager.add_product(
                    dialog.result['name'],
                    dialog.result['description'],
                    dialog.result['price'],
                    dialog.result['stock']
                )
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                self.load_products()
            except Exception as e:
                log_error(f"Erro ao adicionar produto: {e}")
                messagebox.showerror("Erro", f"Não foi possível adicionar: {e}")

    # Atualiza produto
    def update_product(self):
        product_id = simpledialog.askinteger("Atualizar Produto", "ID do Produto:")
        if product_id is None:
            return
            
        dialog = ProductDialog(self, "Atualizar Produto")
        if dialog.result:
            try:
                self.db_manager.update_product(
                    product_id,
                    dialog.result['name'],
                    dialog.result['description'],
                    dialog.result['price'],
                    dialog.result['stock']
                )
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                self.load_products()
            except Exception as e:
                log_error(f"Erro ao atualizar produto {product_id}: {e}")
                messagebox.showerror("Erro", f"Não foi possível atualizar: {e}")

    # Remove produto
    def delete_product(self):
        product_id = simpledialog.askinteger("Deletar Produto", "ID do Produto:")
        if product_id is None:
            return
        if messagebox.askyesno("Confirmar Exclusão", f"Deletar produto ID {product_id}?"):
            try:
                self.db_manager.delete_product(product_id)
                messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
                self.load_products()
            except Exception as e:
                log_error(f"Erro ao deletar produto {product_id}: {e}")
                messagebox.showerror("Erro", f"Não foi possível deletar: {e}")

    # Gera gráfico e personaliza
    def plot_sales_data(self):
        self.ax.clear()
        data = self.db_manager.get_sales_data()
        
        if data:
            names = [d['nome'][:15] + "..." if len(d['nome']) > 15 else d['nome'] for d in data]
            stock = [d['estoque'] for d in data]  
            
            colors = [COLORS['primary'], COLORS['accent'], COLORS['secondary'], 
                    COLORS['success'], COLORS['warning']][:len(names)]
            
            bars = self.ax.barh(names, stock, color=colors, alpha=0.8)
            
            self.ax.set_xlabel('Quantidade em Estoque', fontsize=10, color=COLORS['text_primary'])
            self.ax.set_title('Top 5 Produtos por Estoque', fontsize=12, fontweight='bold', 
                            color=COLORS['text_primary'], pad=20)
            
            for i, (bar, value) in enumerate(zip(bars, stock)):
                self.ax.text(value + max(stock) * 0.01, bar.get_y() + bar.get_height()/2, 
                        str(value), va='center', fontsize=9, color=COLORS['text_primary'])
            
            self.ax.tick_params(colors=COLORS['text_secondary'], labelsize=9)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color(COLORS['text_secondary'])
            self.ax.spines['bottom'].set_color(COLORS['text_secondary'])
            
            self.ax.grid(True, axis='x', alpha=0.3, color=COLORS['text_secondary'])
            
        else:
            self.ax.text(0.5, 0.5, "📊\n\nSem dados para exibir", 
                        ha='center', va='center', transform=self.ax.transAxes,
                        fontsize=12, color=COLORS['text_secondary'])
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        
        self.ax.set_facecolor(COLORS['background'])
        self.fig.patch.set_facecolor(COLORS['surface'])
        self.canvas.draw_idle()

# Classe para janela adicionar produtos
class ProductDialog:
    def __init__(self, parent, title):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("1000x600")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLORS['background'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.center_window()
        self.create_widgets()
        
        self.dialog.wait_window()
    
    # Configura janela
    def center_window(self):
        self.dialog.update_idletasks()
        w, h = self.dialog.winfo_width(), self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (h // 2)
        self.dialog.geometry(f'{w}x{h}+{x}+{y}')
    
    # Cria interface
    def create_widgets(self):
        main_frame = tk.Frame(self.dialog, bg=COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        card = tk.Frame(main_frame, bg=COLORS['surface'], relief='solid', bd=1)
        card.pack(fill='both', expand=True)
        
        card_inner = tk.Frame(card, bg=COLORS['surface'])
        card_inner.pack(padx=25, pady=25, fill='both', expand=True)
        
        # Campos do produto
        fields = [
            ("Nome do Produto", "name"),
            ("Descrição", "description"),
            ("Preço (R$)", "price"),
            ("Estoque", "stock")
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            tk.Label(
                card_inner,
                text=label_text,
                font=FONTS['body'],
                bg=COLORS['surface'],
                fg=COLORS['text_primary']
            ).pack(anchor='w', pady=(0, 5))
            
            entry = StyledEntry(card_inner, placeholder=f"Digite {label_text.lower()}")
            entry.pack(fill='x', pady=(0, 15), ipady=8)
            self.entries[field_name] = entry
        
        button_frame = tk.Frame(card_inner, bg=COLORS['surface'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        StyledButton(button_frame, "Cancelar", self.cancel, style='secondary').pack(side='right', padx=(10, 0))
        StyledButton(button_frame, "Salvar", self.save, style='success').pack(side='right')
    
    # Salva dados do produto
    def save(self):
        try:
            name = self.entries['name'].get_value().strip()
            description = self.entries['description'].get_value().strip()
            price = float(self.entries['price'].get_value().strip())
            stock = int(self.entries['stock'].get_value().strip())
            
            if not name:
                messagebox.showerror("Erro", "Nome é obrigatório.")
                return
            
            if price <= 0 or stock < 0:
                messagebox.showerror("Erro", "Preço deve ser positivo e estoque não pode ser negativo.")
                return
            
            self.result = {
                'name': name,
                'description': description,
                'price': price,
                'stock': stock
            }
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos.")
    
    #Cancela operação
    def cancel(self):
        self.dialog.destroy()
