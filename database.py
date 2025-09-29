import sqlite3
from sqlite3 import Error

class DatabaseManager:
    def __init__(self, db_path="perucas_diferentonas.db"):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Para retornar dicionários
            print("Conexão ao banco de dados SQLite bem-sucedida")
            return True
        except Error as e:
            print(f"Erro ao conectar ao SQLite: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexão SQLite fechada")

    def execute_query(self, query, params=None):
        cursor = None
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Erro ao executar query: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, params=None):
        cursor = None
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            # Converter para dicionário
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Error as e:
            print(f"Erro ao buscar dados: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def create_products_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
        """
        self.execute_query(query)
        print("Tabela 'products' verificada/criada.")

    def add_product(self, name, description, price, stock):
        query = "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)"
        params = (name, description, price, stock)
        return self.execute_query(query, params)

    def get_products(self):
        query = "SELECT * FROM products"
        return self.fetch_all(query)

    def update_product(self, product_id, name, description, price, stock):
        query = "UPDATE products SET name=?, description=?, price=?, stock=? WHERE id=?"
        params = (name, description, price, stock, product_id)
        return self.execute_query(query, params)

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id=?"
        params = (product_id,)
        return self.execute_query(query, params)

    def get_sales_data(self):
        # Simulação de dados de vendas para o gráfico
        query = "SELECT name, stock FROM products ORDER BY stock DESC LIMIT 5"
        return self.fetch_all(query)


# Exemplo de uso (para testes, pode ser removido ou comentado em produção)
if __name__ == "__main__":
    db = DatabaseManager("perucas_diferentonas.db")
    if db.connect():
        db.create_products_table()

        # Adicionar alguns produtos de exemplo se a tabela estiver vazia
        if not db.get_products():
            db.add_product("Peruca Arco-Íris Vibrante", "Peruca longa e colorida com todas as cores do arco-íris.", 89.99, 10)
            db.add_product("Peruca Galáxia Brilhante", "Peruca curta com tons de azul e roxo, e glitter estelar.", 120.50, 5)
            db.add_product("Peruca Sereia Encantada", "Peruca ondulada em tons de verde-água e rosa, com detalhes de conchas.", 95.00, 8)
            db.add_product("Peruca Fogo Ardente", "Peruca volumosa em tons de vermelho e laranja, simulando chamas.", 110.00, 7)
            db.add_product("Peruca Unicórnio Mágico", "Peruca pastel com mechas trançadas e um chifre de unicórnio removível.", 150.00, 3)
            print("Produtos de exemplo adicionados.")

        print("\nProdutos atuais:")
        for product in db.get_products():
            print(product)

        db.disconnect()