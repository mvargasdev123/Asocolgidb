import os
import re
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, select
from models.estado import Estado
from models.usuario import Usuario 
from utils.seguridad import obtener_hash_password 

# 1. Cargamos la bóveda secreta
load_dotenv(override=True)

# 2. Leemos la URL segura de Supabase. Cero fallbacks inseguros.
# Si alguien olvida poner el .env, el programa explota elegantemente aquí mismo.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("¡ALERTA ROJA! No se encontró DATABASE_URL en el entorno.")

# 3. Pequeño truco de compatibilidad: SQLAlchemy prefiere "postgresql://" en vez de "postgres://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Si la URL arrastra parámetros de SQLite por error, los podamos aquí mismo
if "check_same_thread" in DATABASE_URL:
    DATABASE_URL = re.sub(r'[&?]check_same_thread=[^&]+', '', DATABASE_URL)

# 5. Creamos el motor asegurando que NO pasamos argumentos fantasmas
# Forzamos connect_args vacío por si acaso tu framework intenta heredar algo de la config vieja
engine = create_engine(DATABASE_URL, echo=True, connect_args={})

# =======================================================
# DE AQUÍ PARA ABAJO, TODO QUEDA EXACTAMENTE IGUAL
# =======================================================

def create_db_and_tables():
    # Esto lee todas las clases que hereden de SQLModel y crea las tablas mágicamente
    SQLModel.metadata.create_all(engine)

def inicializar_estados_base():
    with Session(engine) as session:
        estados_permitidos = ["Externo", "Voluntario", "Asociado"]
        
        for nombre in estados_permitidos:
            estado_existente = session.exec(select(Estado).where(Estado.nombre_estado == nombre)).first()
            if not estado_existente:
                nuevo_estado = Estado(nombre_estado=nombre)
                session.add(nuevo_estado)
                print(f"Sembrando estado: {nombre} 🌱")
        session.commit()

def get_session():
    with Session(engine) as session:
        yield session

def inicializar_super_usuario():
    with Session(engine) as session:
        correo_admin = "admin@asocolgi.org"
        admin_existente = session.exec(select(Usuario).where(Usuario.email == correo_admin)).first()
        
        if not admin_existente:
            hash_fuerte = obtener_hash_password("admin123")
            nuevo_admin = Usuario(
                email=correo_admin,
                hashed_password=hash_fuerte,
                es_admin=True 
            )
            session.add(nuevo_admin)
            session.commit()
            print("Superusuario sembrado con éxito 👑")