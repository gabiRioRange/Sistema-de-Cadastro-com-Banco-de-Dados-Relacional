from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do Banco de Dados (Descomente a linha abaixo para PostgreSQL)
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:senha@localhost/nome_do_banco"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sistema_cadastro.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para pegar a conexão com o banco (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()