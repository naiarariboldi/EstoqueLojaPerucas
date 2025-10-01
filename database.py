import pymysql
from pymysql import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            # Configurações para conexão com banco de dados
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            self.cursor = self.conn.cursor()
            
            # Criar banco se não existir
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.cursor.execute(f"USE {self.database}")
            
            print("✅ Conectado ao MySQL e banco verificado!")
            return True
            
        except Error as e:
            print(f"❌ Erro na conexão: {e}")
            return False

    # Disconecta do Banco de Dados
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    # Executa INSERT, UPDATE e DELETE
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except Error as e:
            print(f"❌ Erro ao executar query: {e}")
            return False

    # Busca dados
    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"❌ Erro ao buscar dados: {e}")
            return []

    # Busca um dado único
    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"❌ Erro ao buscar dado único: {e}")
            return None
        
    # Cria as tabelas necessárias se não existirem
    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100),
                    email VARCHAR(100),
                    senha VARCHAR(255)
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100),
                    preco DECIMAL(10,2),
                    estoque INT
                )
            """)
            
            self.conn.commit()
            print("✅ Tabelas criadas/verificadas com sucesso!")
            return True
            
        except Error as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return False
    
    # Verifica se o usuário e senha são válidos"
    def check_user_credentials(self, username, password):
        try:
            query = "SELECT * FROM usuarios WHERE nome = %s AND senha = %s"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            return user is not None
        except Error as e:
            print(f"❌ Erro ao verificar credenciais: {e}")
            return False

    # Cadastra um novo usuário
    def add_user(self, email, username, password):
        try:
            query = "INSERT INTO usuarios (email, nome, senha) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (email, username, password))
            self.conn.commit()
            print(f"✅ Usuário {username} criado com sucesso!")
            return True
        except Error as e:
            print(f"❌ Erro ao adicionar usuário: {e}")
            return False

    # Busca produtos
    def get_products(self):
        try:
            query = "SELECT * FROM produtos ORDER BY id"
            return self.fetch_all(query)
        except Error as e:
            print(f"❌ Erro ao buscar produtos: {e}")
            return []

    # Adiciona produtos
    def add_product(self, name, description, price, stock):
        try:
            query = "INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)"
            result = self.execute_query(query, (name, price, stock))
            if result:
                print(f"✅ Produto {name} adicionado com sucesso!")
            return result
        except Error as e:
            print(f"❌ Erro ao adicionar produto: {e}")
            return False

    # Atualiza produtos
    def update_product(self, product_id, name, description, price, stock):
        try:
            query = """
                UPDATE produtos 
                SET nome = %s, preco = %s, estoque = %s 
                WHERE id = %s
            """
            result = self.execute_query(query, (name, price, stock, product_id))
            if result:
                print(f"✅ Produto ID {product_id} atualizado com sucesso!")
            return result
        except Error as e:
            print(f"❌ Erro ao atualizar produto: {e}")
            return False

    # Deleta produtos
    def delete_product(self, product_id):
        try:
            query = "DELETE FROM produtos WHERE id = %s"
            result = self.execute_query(query, (product_id,))
            if result:
                print(f"✅ Produto ID {product_id} deletado com sucesso!")
            return result
        except Error as e:
            print(f"❌ Erro ao deletar produto: {e}")
            return False

    # Busca dados para o grafico
    def get_sales_data(self):
        try:
            query = "SELECT nome, estoque FROM produtos ORDER BY estoque DESC LIMIT 5"
            return self.fetch_all(query)
        except Error as e:
            print(f"❌ Erro ao buscar dados de vendas: {e}")
            return []
