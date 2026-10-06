import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Localiza a raiz do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Carrega as variáveis do arquivo .env
load_dotenv(PASTA_PROJETO / ".env")

# Monta a URL de conexão
url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
    query={"sslmode": "require"}
)

engine = create_engine(url)

# Testa a conexão
try:
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("SELECT version();")
        )

        print("Conexão realizada com sucesso!")
        print(resultado.fetchone()[0])

except Exception as erro:
    print("Erro ao conectar ao banco:")
    print(erro)