import os
from sqlmodel import SQLModel, create_engine, Session
import domain.models  # Importante para que SQLModel registre todas las tablas y relaciones

# Se lee la URL de la base de datos de las variables de entorno. 
# Para QA (testing) usaremos sqlite:///:memory: por defecto si no está definida
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")

# Para SQLite necesitamos connect_args. Para PostgreSQL no hace falta, 
# pero la dejaremos vacía en caso de postgres.
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
