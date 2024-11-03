from dotenv import load_dotenv
from time import sleep
import oracledb
import os

# Carrega as variaveis de ambiente do arquivo .env
load_dotenv()


def connect():
    try:
        # Dados para conexão
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        service_name = os.getenv("DB_SERVICE_NAME")

        # Criando conexão
        dsn = f"{username}/{password}@{host}:{port}/{service_name}"
        print(f"Conectando ao banco de dados em {host}:{port} como {username}...")
        sleep(1)
        connection = oracledb.connect(dsn)
        if connection:
            print("Conexão feita com sucesso!")
            return connection
    except Exception as e:
        print(f"Falha na conexão: {e}.")
    return None

