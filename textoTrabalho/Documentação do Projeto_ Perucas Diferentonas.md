# Documentação do Projeto: Perucas Diferentonas

## 1. Introdução

Este documento detalha o desenvolvimento de uma aplicação desktop para gerenciamento de uma loja virtual de perucas "diferentonas". O objetivo principal é demonstrar a criação de uma aplicação Python utilizando a biblioteca Tkinter para a interface gráfica, MySQL para o gerenciamento de dados e Matplotlib para visualização de informações. A aplicação permite o cadastro, consulta, atualização e exclusão (CRUD) de produtos, além de apresentar um sistema de login e registro de erros.

## 2. Diagrama de Classes (UML Simplificado)

```mermaid
classDiagram
    class DatabaseManager {
        +__init__(host, database, user, password)
        +connect()
        +disconnect()
        +execute_query(query, params)
        +fetch_all(query, params)
        +create_products_table()
        +add_product(name, description, price, stock)
        +get_products()
        +update_product(id, name, description, price, stock)
        +delete_product(id)
        +get_sales_data()
    }

    class LoginWindow {
        +__init__(master, db_manager, on_login_success)
        +attempt_login()
    }

    class MainWindow {
        +__init__(master, db_manager)
        +load_products()
        +add_product()
        +update_product()
        +delete_product()
        +plot_sales_data()
    }

    class Application {
        +__init__()
        +show_main_window()
        +on_main_window_close()
    }

    class Logger {
        +setup_logger()
        +log_error(message)
    }

    Application --|> Tk
    Application --> LoginWindow
    Application --> MainWindow
    LoginWindow --> DatabaseManager
    MainWindow --> DatabaseManager
    MainWindow --> Logger
    LoginWindow --> Logger
```

## 3. Explicação do Código (Principais Funções e Métodos)

O projeto é modularizado em quatro arquivos Python principais (`database.py`, `logger.py`, `gui.py`, `main.py`), cada um com responsabilidades bem definidas.

### `database.py`

Este módulo contém a classe `DatabaseManager`, responsável por toda a interação com o banco de dados MySQL.

*   `__init__(self, host, database, user, password)`: Construtor que inicializa as credenciais de conexão.
*   `connect()`: Estabelece a conexão com o banco de dados MySQL.
*   `disconnect()`: Fecha a conexão com o banco de dados.
*   `execute_query(query, params)`: Executa comandos SQL que modificam o banco de dados (INSERT, UPDATE, DELETE).
*   `fetch_all(query, params)`: Executa comandos SQL que retornam dados (SELECT).
*   `create_products_table()`: Cria a tabela `products` se ela não existir, com campos para `id`, `name`, `description`, `price` e `stock`.
*   `add_product(name, description, price, stock)`: Adiciona um novo produto à tabela.
*   `get_products()`: Retorna todos os produtos cadastrados.
*   `update_product(id, name, description, price, stock)`: Atualiza os dados de um produto existente.
*   `delete_product(id)`: Remove um produto da tabela.
*   `get_sales_data()`: Simula a obtenção de dados de vendas (neste caso, top 5 produtos por estoque) para o gráfico.

### `logger.py`

Este módulo implementa um sistema de log simples para registrar erros em um arquivo `error.log`.

*   `setup_logger()`: Configura o logger para escrever mensagens de erro no arquivo `error.log`.
*   `log_error(message)`: Registra uma mensagem de erro no log.

### `gui.py`

Este módulo define as classes para as janelas da interface gráfica do usuário (GUI) usando Tkinter.

*   **`LoginWindow(tk.Toplevel)`**:
    *   `__init__(self, master, db_manager, on_login_success)`: Inicializa a janela de login, recebendo o gerenciador de banco de dados e uma função de callback para sucesso no login.
    *   `attempt_login()`: Verifica as credenciais de login (atualmente "admin" / "admin") e, em caso de sucesso, chama `on_login_success`.

*   **`MainWindow(tk.Toplevel)`**:
    *   `__init__(self, master, db_manager)`: Inicializa a janela principal, que contém as funcionalidades de CRUD de produtos e o gráfico de vendas.
    *   `load_products()`: Carrega os produtos do banco de dados e os exibe em um widget de texto.
    *   `add_product()`, `update_product()`, `delete_product()`: Métodos que interagem com o `DatabaseManager` para realizar as operações CRUD, utilizando `simpledialog` para entrada de dados.
    *   `plot_sales_data()`: Gera e exibe um gráfico de barras com os top 5 produtos em estoque usando Matplotlib.

*   **`Application(tk.Tk)`**:
    *   `__init__(self)`: Classe principal da aplicação. Inicializa o logger, o `DatabaseManager`, tenta conectar ao banco de dados e exibe a `LoginWindow`.
    *   `show_main_window()`: Chamada após o login bem-sucedido para exibir a `MainWindow`.
    *   `on_main_window_close()`: Lida com o fechamento da janela principal, desconectando do banco de dados.

### `main.py`

Este é o ponto de entrada da aplicação. Ele simplesmente cria uma instância da classe `Application` e inicia o loop principal do Tkinter.

## 4. Instruções para Execução

Para configurar e executar a aplicação, siga os passos abaixo:

### 4.1. Pré-requisitos

*   **Python 3.x** instalado.
*   **Servidor MySQL** em execução. Você pode usar XAMPP, WAMP, MAMP ou instalar o MySQL Server diretamente.

### 4.2. Configuração do Banco de Dados MySQL

1.  **Crie um banco de dados:** No seu servidor MySQL, crie um novo banco de dados. Por exemplo, `perucas_diferentonas_db`.
    ```sql
    CREATE DATABASE perucas_diferentonas_db;
    ```
2.  **Crie um usuário (opcional, mas recomendado):** Crie um usuário com permissões para acessar este banco de dados. Por exemplo, `root` com senha `password` (para ambiente de desenvolvimento).
    ```sql
    CREATE USER 'root'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON perucas_diferentonas_db.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
    ```
3.  **Atualize as credenciais:** No arquivo `gui.py`, na classe `Application`, ajuste as credenciais do `DatabaseManager` se necessário:
    ```python
    self.db_manager = DatabaseManager("localhost", "perucas_diferentonas_db", "root", "password")
    ```

### 4.3. Instalação das Dependências Python

1.  Navegue até o diretório raiz do projeto no terminal.
2.  Instale as bibliotecas necessárias usando `pip` e o arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    As dependências incluem `mysql-connector-python`, `matplotlib` e `numpy`.

### 4.4. Execução da Aplicação

1.  Após instalar as dependências e configurar o banco de dados, execute o arquivo `main.py`:
    ```bash
    python main.py
    ```
2.  A janela de login será exibida. Use `admin` como usuário e `admin` como senha para acessar a aplicação.
3.  A aplicação criará automaticamente a tabela `products` no banco de dados e adicionará alguns produtos de exemplo se a tabela estiver vazia.

## 5. Exemplos de Uso (Prints das Telas e Operações)

### 5.1. Janela de Login

![Janela de Login](https://private-us-east-1.manuscdn.com/sessionFile/nYD4TNaBUcI5r7MacIg1lq/sandbox/0z6W62tmw1ELXxTv0BXXeS-images_1759145399313_na1fn_L2hvbWUvdWJ1bnR1L3BlcnVjYXNfZGlmZXJlbnRvbmFzL2xvZ2luX3NjcmVlbnNob3Q.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbllENFROYUJVY0k1cjdNYWNJZzFscS9zYW5kYm94LzB6Nlc2MnRtdzFFTFh4VHYwQlhYZVMtaW1hZ2VzXzE3NTkxNDUzOTkzMTNfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmxjblZqWVhOZlpHbG1aWEpsYm5SdmJtRnpMMnh2WjJsdVgzTmpjbVZsYm5Ob2IzUS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=iCXh4w88EDcgdE60vInQVVK9asftoPYkNhaJym9oyI2ZgqMFc7dFKow4z0hESFk4KVraK2EwLSthIaHf7MO9qcBxa1QovblE6hqF70WLngST1f451dIG62-ZKV7tSuGciOVWb-jTtvLEnFEXHsjyB8tGut51KctJ27leOy4eS84KL~rGEYEu4jbotX5QNcJNiBbAo6vjIUrn3ZnHSv75wM5ziazbERzGX9ngOvf~~edLJIqPE2zvG9U9oGb~FlHlgizg9r69C5b9L9CDt2ZLPsXrSbEaqWtcbE5oT2zNlaiXUc-ZQpI2bfrydGf5E2DZpPpQyMt-XRdSVkOEb5ip9w__)

### 5.2. Janela Principal (CRUD de Produtos e Gráfico)

![Janela Principal](https://private-us-east-1.manuscdn.com/sessionFile/nYD4TNaBUcI5r7MacIg1lq/sandbox/0z6W62tmw1ELXxTv0BXXeS-images_1759145399323_na1fn_L2hvbWUvdWJ1bnR1L3BlcnVjYXNfZGlmZXJlbnRvbmFzL21haW5fd2luZG93X3NjcmVlbnNob3Q.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbllENFROYUJVY0k1cjdNYWNJZzFscS9zYW5kYm94LzB6Nlc2MnRtdzFFTFh4VHYwQlhYZVMtaW1hZ2VzXzE3NTkxNDUzOTkzMjNfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmxjblZqWVhOZlpHbG1aWEpsYm5SdmJtRnpMMjFoYVc1ZmQybHVaRzkzWDNOamNtVmxibk5vYjNRLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=E418O6bAI-s6orR~rQ5J-sgbRHUkKhTpUouWH1qIMFxU4ofrd0VDdRwXevmk5PkEM73fl3hJEbXiexl0SRwCzO80oh7CopKgS3A0S0jxUsovLTUJZyTtYMr2xvIFYN7GS82fybaSj9Coj59swuF81oE6inuLSZD6J3TjaDaGcevM7sS88tJH5YncXl3eBKV8dsNt6qXqK6k63T0n33h9dh76oA3n1Zd28NjVOzDMlPdYUFYRgzdnO72xxaaNwv4k8hyihYRQw4YlaFH~BZd4cp6Hf5h-lxiExV1sWtDrhsVyn9KJfPF-eh88IUwyXeCU3m2wdfScxFg504rF3lG4ow__)

### 5.3. Adicionar Produto

![Adicionar Produto](https://private-us-east-1.manuscdn.com/sessionFile/nYD4TNaBUcI5r7MacIg1lq/sandbox/0z6W62tmw1ELXxTv0BXXeS-images_1759145399325_na1fn_L2hvbWUvdWJ1bnR1L3BlcnVjYXNfZGlmZXJlbnRvbmFzL2FkZF9wcm9kdWN0X3NjcmVlbnNob3Q.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbllENFROYUJVY0k1cjdNYWNJZzFscS9zYW5kYm94LzB6Nlc2MnRtdzFFTFh4VHYwQlhYZVMtaW1hZ2VzXzE3NTkxNDUzOTkzMjVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmxjblZqWVhOZlpHbG1aWEpsYm5SdmJtRnpMMkZrWkY5d2NtOWtkV04wWDNOamNtVmxibk5vYjNRLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=tej4IfYy71jwn2U2SuGO1o9IoCJxwgh5uWtCI24OCOihuIXR5lWVw2-C4YJWnv2-8FjTk24IfHwlSevpZzYSWXJsEKClxF8~bTW0M~RQ7T9phg4s2I6-M-sl-fK2vMmAttfYtolf85MfPPmFp2nbKoJlVAwA9bV8x4Jkeb~dobRm3EWRgYwSjHHqWMpI8YK1gR2Q3Fr5yeK3qzUSGebstW5DYCVQYZsn~bCgWEv~ewwX7capHz05zHToYxAqXOgVFeuMuXFrJOR1vEpgMbQsnDFfh~hzCFx2CzC7-RShQT9M~nqrlxFuoDuX58gQgHNzbhPM-qEZhOOY5WM5zRWvog__)

### 5.4. Atualizar Produto

![Atualizar Produto](https://private-us-east-1.manuscdn.com/sessionFile/nYD4TNaBUcI5r7MacIg1lq/sandbox/0z6W62tmw1ELXxTv0BXXeS-images_1759145399327_na1fn_L2hvbWUvdWJ1bnR1L3BlcnVjYXNfZGlmZXJlbnRvbmFzL3VwZGF0ZV9wcm9kdWN0X3NjcmVlbnNob3Q.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbllENFROYUJVY0k1cjdNYWNJZzFscS9zYW5kYm94LzB6Nlc2MnRtdzFFTFh4VHYwQlhYZVMtaW1hZ2VzXzE3NTkxNDUzOTkzMjdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmxjblZqWVhOZlpHbG1aWEpsYm5SdmJtRnpMM1Z3WkdGMFpWOXdjbTlrZFdOMFgzTmpjbVZsYm5Ob2IzUS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=KnmjKr6ff3U-Hdm8vuNB7cHcD3LOFEpGLo8PXlZ5lVOOLId1riaifAxtTV9CZ~peXorcDgu894c731h4modg8fVp4OdpdkOQXXXWVmhrJEuTaA7aita359y2SvUKG4uYtr2DuLOr8ttCl7FSPFECG3okx3niRL5apJVV4zDHNKIb0cAvXScr5Bm7Jh5XpdujHD9tMkyvNCdwJIcaFvjoBlbICEPvdhQPSRcCVAYAwdhRebK7vCu0addBrat9Kx9hHh2fTv~hz25UytdcxIBOyUDOyZAWYdb2~ul~F6eBwRP26kITgMQ2kjtq-SxAMIb5GeqcEDD064uXH5bkuuS6oQ__)

### 5.5. Deletar Produto

![Deletar Produto](https://private-us-east-1.manuscdn.com/sessionFile/nYD4TNaBUcI5r7MacIg1lq/sandbox/0z6W62tmw1ELXxTv0BXXeS-images_1759145399328_na1fn_L2hvbWUvdWJ1bnR1L3BlcnVjYXNfZGlmZXJlbnRvbmFzL2RlbGV0ZV9wcm9kdWN0X3NjcmVlbnNob3Q.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbllENFROYUJVY0k1cjdNYWNJZzFscS9zYW5kYm94LzB6Nlc2MnRtdzFFTFh4VHYwQlhYZVMtaW1hZ2VzXzE3NTkxNDUzOTkzMjhfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzQmxjblZqWVhOZlpHbG1aWEpsYm5SdmJtRnpMMlJsYkdWMFpWOXdjbTlrZFdOMFgzTmpjbVZsYm5Ob2IzUS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=LO2yABYfnM2sOtxBclkKRZj45eulvoee-3OM5eDaZaH3aJDPajw3G12AboiGz9xEXoTA9iOGFy4Orehgt75f8mPpPA~GqITHG~BjXT3oXxflgbLPJWhE54QWC8OaoCfG97u-W9iCpqCcFyzcQzMSxm7gom5K6y0wV6PKU1uA5GuepFLDhMlelx~o9obcNDKHC6w2IMluLUfSdC-wgnSxJZKMs3uEQGS816-i0ugccfdd7JhTE7jb80IIpfLPr03YwSwW2RdulUzebyCe1icj5ANTtG8uox3p2MG8j7pCLVHwejiRbfhROHnDMmC6xv-DBP~H8HrliNGYQ8JWnHTNyg__)

### 5.6. Registro de Erros (`error.log`)

```
2025-09-29 10:30:05 - ERROR - Tentativa de login falhou para o usuário: usuario_errado
2025-09-29 10:35:10 - ERROR - Erro ao adicionar produto: 1048 (23000): Column 'name' cannot be null
```

---

**Autor:** Manus AI
**Data:** 29 de Setembro de 2025

