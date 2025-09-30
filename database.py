import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco: {e}")
            return False

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            return False

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or [])
        return [dict(row) for row in self.cursor.fetchall()]

    # ---------- Tabelas ----------
    def create_products_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """
        self.execute_query(query)

    def create_users_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
        self.execute_query(query)

    # ---------- Produtos ----------
    def get_products(self):
        return self.fetch_all("SELECT * FROM products")

    def add_product(self, name, description, price, stock):
        query = "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)"
        self.execute_query(query, (name, description, price, stock))

    def update_product(self, product_id, name, description, price, stock):
        query = """UPDATE products
                   SET name=?, description=?, price=?, stock=?
                   WHERE id=?"""
        self.execute_query(query, (name, description, price, stock, product_id))

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id=?"
        self.execute_query(query, (product_id,))

    def get_sales_data(self):
        # Top 5 produtos por estoque
        query = "SELECT name, stock FROM products ORDER BY stock DESC LIMIT 5"
        return self.fetch_all(query)

    # ---------- Usuários ----------
    def add_user(self, email, username, password):
        query = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)"
        self.execute_query(query, (email, username, password))

    def check_user_credentials(self, username, password):
        """
        Retorna True se existir um usuário com este username e password.
        """
        query = "SELECT * FROM users WHERE username=? AND password=?"
        result = self.fetch_all(query, (username, password))
        return len(result) > 0
