import tkinter as tk
from tkinter import messagebox
from database import DatabaseManager
from gui import LoginWindow, MainWindow
from logger import setup_logger

#Aplicação principal (gerencia janelas e banco de dados)
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        setup_logger()

        try:
            # Configuração do banco
            self.db_manager = DatabaseManager(
                host="localhost",
                user="root",           
                password="",
                database="perucas_diferentonas"
            )

            # Mostra um erro se não for possível conectar ao banco  
            if not self.db_manager.connect():
                messagebox.showerror("Erro", "Não foi possível conectar ao MySQL.")
                self.destroy()
                return

            # Cria tabelas se não existirem
            if not self.db_manager.create_tables():
                messagebox.showerror("Erro", "Erro ao criar tabelas.")
                self.destroy()
                return

            self.show_login_window()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            self.destroy()

    # Abre janela de login
    def show_login_window(self):
        self.login_window = LoginWindow(self, self.db_manager, self.on_login_success)
        self.login_window.deiconify()

    def on_login_success(self):
        if hasattr(self, 'login_window'):
            self.login_window.destroy()
        self.show_main_window()

    # Abre janela principal do sistema
    def show_main_window(self):
        self.main_window = MainWindow(self, self.db_manager)
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_main_window_close)

    # Janela para sair
    def on_main_window_close(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.db_manager.disconnect()
            self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
