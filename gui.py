
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from database import DatabaseManager
from logger import log_error, setup_logger

class LoginWindow(tk.Toplevel):
    def __init__(self, master, db_manager, on_login_success):
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.on_login_success = on_login_success
        self.title("Login - Perucas Diferentonas")
        
        # ALTERE O TAMANHO AQUI ↓
        self.geometry("400x250")  # Largura x Altura
        
        self.resizable(False, False)
        self.center_window()
        self.create_widgets()


    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        tk.Label(self, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.attempt_login).pack(pady=10)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simples validação de login (para fins de demonstração)
        # Em um sistema real, isso envolveria consulta ao banco de dados
        if username == "admin" and password == "admin":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")
            log_error(f"Tentativa de login falhou para o usuário: {username}")

class MainWindow(tk.Toplevel):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.title("Perucas Diferentonas - Gerenciamento de Produtos")
        
        self.geometry("1200x800") 
        
        self.center_window()
        self.create_widgets()
        self.load_products()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Frame para botões de CRUD
        crud_frame = tk.Frame(self)
        crud_frame.pack(pady=10)

        tk.Button(crud_frame, text="Adicionar Produto", command=self.add_product).pack(side=tk.LEFT, padx=5)
        tk.Button(crud_frame, text="Atualizar Produto", command=self.update_product).pack(side=tk.LEFT, padx=5)
        tk.Button(crud_frame, text="Deletar Produto", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        tk.Button(crud_frame, text="Atualizar Lista", command=self.load_products).pack(side=tk.LEFT, padx=5)

        # Frame para a lista de produtos
        self.product_list_frame = tk.Frame(self)
        self.product_list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.product_list_label = tk.Label(self.product_list_frame, text="Lista de Produtos:", font=("Arial", 12, "bold"))
        self.product_list_label.pack(pady=5)

        self.product_list_text = tk.Text(self.product_list_frame, height=15, width=80, state=tk.DISABLED)
        self.product_list_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Frame para o gráfico de vendas
        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.chart_label = tk.Label(self.chart_frame, text="Gráfico de Vendas (Top 5 Produtos em Estoque):")
        self.chart_label.pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.plot_sales_data()

    def load_products(self):
        self.product_list_text.config(state=tk.NORMAL)
        self.product_list_text.delete(1.0, tk.END)
        products = self.db_manager.get_products()
        if products:
            self.product_list_text.insert(tk.END, "ID\tNome\t\tPreço\tEstoque\tDescrição\n")
            self.product_list_text.insert(tk.END, "---\t----\t\t-----\t-------\t-----------\n")
            for p in products:
                self.product_list_text.insert(tk.END, f"{p['id']}\t{p['name'][:15]}...\t{p['price']:.2f}\t{p['stock']}\t{p['description'][:30]}...\n")
        else:
            self.product_list_text.insert(tk.END, "Nenhum produto cadastrado.")
        self.product_list_text.config(state=tk.DISABLED)
        self.plot_sales_data() # Atualiza o gráfico também

    def add_product(self):
        name = simpledialog.askstring("Adicionar Produto", "Nome do Produto:")
        if not name: return
        description = simpledialog.askstring("Adicionar Produto", "Descrição:")
        if not description: return
        price = simpledialog.askfloat("Adicionar Produto", "Preço:")
        if price is None: return
        stock = simpledialog.askinteger("Adicionar Produto", "Estoque:")
        if stock is None: return

        try:
            self.db_manager.add_product(name, description, price, stock)
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            self.load_products()
        except Exception as e:
            log_error(f"Erro ao adicionar produto: {e}")
            messagebox.showerror("Erro", f"Não foi possível adicionar o produto: {e}")

    def update_product(self):
        product_id = simpledialog.askinteger("Atualizar Produto", "ID do Produto a ser atualizado:")
        if product_id is None: return

        # Poderíamos buscar o produto existente para preencher os campos
        name = simpledialog.askstring("Atualizar Produto", "Novo Nome do Produto:")
        if not name: return
        description = simpledialog.askstring("Atualizar Produto", "Nova Descrição:")
        if not description: return
        price = simpledialog.askfloat("Atualizar Produto", "Novo Preço:")
        if price is None: return
        stock = simpledialog.askinteger("Atualizar Produto", "Novo Estoque:")
        if stock is None: return

        try:
            self.db_manager.update_product(product_id, name, description, price, stock)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.load_products()
        except Exception as e:
            log_error(f"Erro ao atualizar produto {product_id}: {e}")
            messagebox.showerror("Erro", f"Não foi possível atualizar o produto: {e}")

    def delete_product(self):
        product_id = simpledialog.askinteger("Deletar Produto", "ID do Produto a ser deletado:")
        if product_id is None: return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o produto com ID {product_id}?"):
            try:
                self.db_manager.delete_product(product_id)
                messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
                self.load_products()
            except Exception as e:
                log_error(f"Erro ao deletar produto {product_id}: {e}")
                messagebox.showerror("Erro", f"Não foi possível deletar o produto: {e}")

    def plot_sales_data(self):
        self.ax.clear()
        sales_data = self.db_manager.get_sales_data()
        if sales_data:
            product_names = [d['name'] for d in sales_data]
            stock_levels = [d['stock'] for d in sales_data]

            y_pos = np.arange(len(product_names))
            self.ax.barh(y_pos, stock_levels, align='center', color='purple')
            self.ax.set_yticks(y_pos, labels=product_names)
            self.ax.invert_yaxis()  # Top to bottom
            self.ax.set_xlabel('Estoque')
            self.ax.set_title('Top 5 Produtos por Estoque')
        else:
            self.ax.text(0.5, 0.5, "Nenhum dado de vendas disponível", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)

        self.canvas.draw_idle()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw() # Esconde a janela principal até o login
        setup_logger()

        # Configuração do banco de dados (ajuste conforme seu ambiente MySQL)
        self.db_manager = DatabaseManager("perucas_diferentonas.db")
        if not self.db_manager.connect():
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados. Verifique as configurações.")
            log_error("Falha na conexão inicial com o banco de dados.")
            self.destroy()
            return
        self.db_manager.create_products_table()

        self.login_window = LoginWindow(self, self.db_manager, self.show_main_window)

    def show_main_window(self):
        self.main_window = MainWindow(self, self.db_manager)
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_main_window_close)

    def on_main_window_close(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair da aplicação?"):
            self.db_manager.disconnect()
            self.main_window.destroy()
            self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()

