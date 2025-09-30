
import logging

def setup_logger():
    logging.basicConfig(
        filename='error.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_error(message):
    logging.error(message)

# Exemplo de uso
if __name__ == "__main__":
    setup_logger()
    try:
        1 / 0
    except ZeroDivisionError as e:
        log_error(f"Erro de divisão por zero: {e}")
    print("Verifique o arquivo error.log para o registro do erro.")

