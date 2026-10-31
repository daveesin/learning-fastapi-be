from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os


# Importa o link do banco de dados
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a conexão do seu banco
db = create_engine(DATABASE_URL)

# Cria a base do banco de dados
Base = declarative_base()