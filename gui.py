import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from logger import log_error

class LoginWindow(tk.Toplevel):
    def __init__(self, master, db_manager, on_login_success):
        super().__init__(master)
        self.db_manager = db_manager
        self.on_login_success = on_login_success
        self.title("Login - Perucas Diferentonas")
        self.geometry("400x250")
        self.resizable(False, False)
        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def create_widgets(self):
        tk.Label(self, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.attempt_login).pack(pady=10)
        tk.Button(self, text="Sign Up", command=self.open_signup).pack(pady=5)

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

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


    def open_signup(self):
        SignUpWindow(self.master, self.db_manager)


class SignUpWindow(tk.Toplevel):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.title("Criar Conta")
        self.geometry("400x250")
        self.resizable(False, False)
        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def create_widgets(self):
        tk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Criar conta", command=self.attempt_create).pack(pady=10)

    def attempt_create(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

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


class MainWindow(tk.Toplevel):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.title("Perucas Diferentonas - Gerenciamento de Produtos")
        self.geometry("1200x800")
        self.center_window()
        self.create_widgets()
        self.load_products()

    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def create_widgets(self):
        crud_frame = tk.Frame(self)
        crud_frame.pack(pady=10)

        tk.Button(crud_frame, text="Adicionar Produto", command=self.add_product).pack(side=tk.LEFT, padx=5)
        tk.Button(crud_frame, text="Atualizar Produto", command=self.update_product).pack(side=tk.LEFT, padx=5)
        tk.Button(crud_frame, text="Deletar Produto", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        tk.Button(crud_frame, text="Atualizar Lista", command=self.load_products).pack(side=tk.LEFT, padx=5)

        self.product_list_text = tk.Text(self, height=15, width=80, state=tk.DISABLED)
        self.product_list_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.plot_sales_data()

    def load_products(self):
        self.product_list_text.config(state=tk.NORMAL)
        self.product_list_text.delete(1.0, tk.END)
        products = self.db_manager.get_products()
        if products:
            self.product_list_text.insert(tk.END, "ID\tNome\t\tPreço\tEstoque\tDescrição\n")
            self.product_list_text.insert(tk.END, "---\t----\t\t-----\t-------\t-----------\n")
            for p in products:
                self.product_list_text.insert(
                    tk.END,
                    f"{p['id']}\t{p['name'][:15]}...\t{p['price']:.2f}\t{p['stock']}\t{p['description'][:30]}...\n"
                )
        else:
            self.product_list_text.insert(tk.END, "Nenhum produto cadastrado.")
        self.product_list_text.config(state=tk.DISABLED)
        self.plot_sales_data()

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
            messagebox.showinfo("Sucesso", "Produto adicionado!")
            self.load_products()
        except Exception as e:
            log_error(f"Erro ao adicionar produto: {e}")
            messagebox.showerror("Erro", f"Não foi possível adicionar: {e}")

    def update_product(self):
        product_id = simpledialog.askinteger("Atualizar Produto", "ID do Produto:")
        if product_id is None: return
        name = simpledialog.askstring("Atualizar Produto", "Novo Nome:")
        if not name: return
        description = simpledialog.askstring("Atualizar Produto", "Nova Descrição:")
        if not description: return
        price = simpledialog.askfloat("Atualizar Produto", "Novo Preço:")
        if price is None: return
        stock = simpledialog.askinteger("Atualizar Produto", "Novo Estoque:")
        if stock is None: return
        try:
            self.db_manager.update_product(product_id, name, description, price, stock)
            messagebox.showinfo("Sucesso", "Produto atualizado!")
            self.load_products()
        except Exception as e:
            log_error(f"Erro ao atualizar produto {product_id}: {e}")
            messagebox.showerror("Erro", f"Não foi possível atualizar: {e}")

    def delete_product(self):
        product_id = simpledialog.askinteger("Deletar Produto", "ID do Produto:")
        if product_id is None: return
        if messagebox.askyesno("Confirmar Exclusão", f"Deletar produto ID {product_id}?"):
            try:
                self.db_manager.delete_product(product_id)
                messagebox.showinfo("Sucesso", "Produto deletado!")
                self.load_products()
            except Exception as e:
                log_error(f"Erro ao deletar produto {product_id}: {e}")
                messagebox.showerror("Erro", f"Não foi possível deletar: {e}")

    def plot_sales_data(self):
        self.ax.clear()
        data = self.db_manager.get_sales_data()
        if data:
            names = [d['name'] for d in data]
            stock = [d['stock'] for d in data]
            y = np.arange(len(names))
            self.ax.barh(y, stock, color='purple')
            self.ax.set_yticks(y, labels=names)
            self.ax.invert_yaxis()
            self.ax.set_xlabel('Estoque')
            self.ax.set_title('Top 5 Produtos por Estoque')
        else:
            self.ax.text(0.5, 0.5, "Sem dados", ha='center', va='center', transform=self.ax.transAxes)
        self.canvas.draw_idle()
