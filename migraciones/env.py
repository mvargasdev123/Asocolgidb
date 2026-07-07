import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# 1. IMPORTACIÓN DE MODELOS
from sqlmodel import SQLModel
from models.expediente import Expediente
from models.comentario import Comentario
from models.datos_asociado import DatosAsociado
from models.datos_voluntario import DatosVoluntario
from models.estado import Estado
from models.nacionalidad import Nacionalidad
from models.persona import Persona
from models.persona_estado import PersonaEstado
from models.tipo_documento import TipoDocumento
from models.usuario import Usuario
from models.telefono_persona import Telefono
from models.catalogos import NivelEducativo, MotivoConsulta, Derivacion, TecnicaAcogida

# 2. CARGAR EL .ENV
load_dotenv()

config = context.config

# 3. LEER LA URL DIRECTO DEL .ENV
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. APUNTAR A LOS METADATOS DE SQLMODEL (AQUÍ ES DONDE VA, NO AL FINAL)
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()