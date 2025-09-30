import tkinter as tk
from tkinter import messagebox
from database import DatabaseManager
from gui import LoginWindow, MainWindow
from logger import setup_logger, log_error

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        setup_logger()

        self.db_manager = DatabaseManager("perucas_diferentonas.db")
        if not self.db_manager.connect():
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco.")
            log_error("Falha ao conectar ao banco.")
            self.destroy()
            return

        self.db_manager.create_products_table()
        self.db_manager.create_users_table()

        self.login_window = LoginWindow(self, self.db_manager, self.show_main_window)

    def show_main_window(self):
        self.main_window = MainWindow(self, self.db_manager)
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_main_window_close)

    def on_main_window_close(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.db_manager.disconnect()
            self.main_window.destroy()
            self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
