from sqlmodel import SQLModel, create_engine, Session

# El nombre de tu archivo de fideos instantáneos
sqlite_file_name = "Asocolgi.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# El parámetro connect_args es un truco vital de SQLite con FastAPI.
# Evita que SQLite llore cuando múltiples peticiones web intentan hablarle al mismo tiempo.
engine = create_engine(
    sqlite_url, 
    echo=True, # echo=True escupe en la consola el SQL crudo. Útil para debugear, apágalo en producción.
    connect_args={"check_same_thread": False} 
)

def create_db_and_tables():
    # Esto lee todas las clases que hereden de SQLModel y crea las tablas mágicamente
    SQLModel.metadata.create_all(engine)

def get_session():
    # Nuestro inyector de dependencias. Abre y cierra la conexión limpiamente.
    with Session(engine) as session:
        yield session
