# Base para Slides de Apresentação: Perucas Diferentonas

## Slide 1: Título

**Título:** Perucas Diferentonas: Uma Aplicação Desktop para Gerenciamento de Loja Virtual

**Subtítulo:** Desenvolvido com Python, Tkinter e MySQL

**Apresentador:** [Seu Nome/Nome da Equipe]

**Data:** 29 de Setembro de 2025

---

## Slide 2: Introdução e Contexto

*   **O que é o projeto?** Uma aplicação desktop para gerenciar uma loja virtual de perucas com um toque único.
*   **Objetivo:** Demonstrar o desenvolvimento de uma aplicação completa utilizando Python, Tkinter para GUI, MySQL para persistência de dados e Matplotlib para visualização.
*   **Funcionalidades Principais:** Login de usuário, CRUD de produtos, visualização de dados de vendas.

---

## Slide 3: Tecnologias Utilizadas

*   **Python:** Linguagem de programação principal.
*   **Tkinter:** Biblioteca padrão do Python para criação de interfaces gráficas de usuário (GUI).
*   **MySQL:** Sistema de gerenciamento de banco de dados relacional para armazenamento de informações de produtos.
*   **Matplotlib:** Biblioteca para criação de gráficos e visualizações de dados (ex: gráfico de vendas).
*   **mysql-connector-python:** Driver Python para MySQL.
*   **logging:** Módulo padrão do Python para registro de eventos e erros.

---

## Slide 4: Estrutura do Projeto

*   **`main.py`:** Ponto de entrada da aplicação, inicializa a interface.
*   **`database.py`:** Gerencia a conexão e as operações CRUD com o banco de dados MySQL.
*   **`gui.py`:** Contém as classes para as janelas de login e principal (CRUD de produtos, gráfico).
*   **`logger.py`:** Configura e gerencia o registro de erros em `error.log`.
*   **`requirements.txt`:** Lista as dependências do projeto.
*   **`error.log`:** Arquivo de log para erros.

---

## Slide 5: Diagrama de Classes (UML Simplificado)

(Inserir imagem do diagrama de classes gerado na documentação)

*   **`Application`:** Orquestra as janelas de login e principal.
*   **`LoginWindow`:** Gerencia a autenticação do usuário.
*   **`MainWindow`:** Interface principal para interação com produtos e visualização de vendas.
*   **`DatabaseManager`:** Abstrai as operações de banco de dados.
*   **`Logger`:** Centraliza o registro de erros.

---

## Slide 6: Demonstração: Janela de Login

(Inserir screenshot da janela de login)

*   Interface simples para autenticação.
*   Credenciais de demonstração: `usuário: admin`, `senha: admin`.
*   Registro de tentativas de login falhas em `error.log`.

---

## Slide 7: Demonstração: Janela Principal e CRUD de Produtos

(Inserir screenshot da janela principal com a lista de produtos)

*   **Listagem de Produtos:** Exibe produtos com ID, Nome, Preço, Estoque e Descrição.
*   **Adicionar Produto:** Formulário para incluir novos itens.
*   **Atualizar Produto:** Edita informações de produtos existentes.
*   **Deletar Produto:** Remove produtos do catálogo.
*   **Atualizar Lista:** Recarrega os dados do banco.

---

## Slide 8: Demonstração: Gráfico de Vendas

(Inserir screenshot do gráfico de vendas)

*   Visualização dos Top 5 produtos com maior estoque (simulando vendas).
*   Utiliza Matplotlib para gerar gráficos de barras.
*   Atualizado dinamicamente com as operações de CRUD.

---

## Slide 9: Como Instalar e Executar

1.  **Pré-requisitos:** Python 3.x, Servidor MySQL em execução.
2.  **Configuração do MySQL:** Criar banco de dados `perucas_diferentonas_db` e usuário (se necessário).
3.  **Instalar Dependências:** `pip install -r requirements.txt`
4.  **Executar:** `python main.py`

(Detalhes completos no `relatorio.pdf`)

---

## Slide 10: Conclusão

*   Projeto demonstra a integração de Tkinter, MySQL e Matplotlib em uma aplicação desktop.
*   Estrutura modular e orientada a objetos.
*   Funcionalidades essenciais para gerenciamento de estoque de uma loja virtual.
*   Base para futuras expansões (ex: gerenciamento de usuários, histórico de vendas).

---

## Slide 11: Perguntas

Obrigado!

[Seu Email/Contato]

