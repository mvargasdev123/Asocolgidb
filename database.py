from sqlmodel import SQLModel, create_engine, Session, select
from models.estado import Estado

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

def inicializar_estados_base():
    # Abrimos una sesión manual porque esto corre antes de que haya peticiones web
    with Session(engine) as session:
        estados_permitidos = ["Externo", "Voluntario", "Asociado", "Contratado"]
        
        for nombre in estados_permitidos:
            # Buscamos si el estado ya existe en la base de datos
            estado_existente = session.exec(select(Estado).where(Estado.nombre_estado == nombre)).first()
            
            # Si no existe (es decir, nos devuelve None), lo creamos
            if not estado_existente:
                nuevo_estado = Estado(nombre_estado=nombre)
                session.add(nuevo_estado)
                print(f"Sembrando estado: {nombre} 🌱")
        
        # Guardamos todos los cambios de golpe
        session.commit()

def get_session():
    # Nuestro inyector de dependencias. Abre y cierra la conexión limpiamente.
    with Session(engine) as session:
        yield session
