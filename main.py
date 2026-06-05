from fastapi import FastAPI
from database import create_db_and_tables, engine, inicializar_estados_base

# ¡IMPORTANTE! Tienes que importar TODOS los modelos aquí antes de llamar a create_db_and_tables()
# Si no lo haces, SQLModel no sabrá que existen y no creará las tablas.
from models.tipo_documento import TipoDocumento
from models.nacionalidad import Nacionalidad
from models.persona import Persona
from models.estado import Estado
from models.persona_estado import PersonaEstado
from models.datos_contratado import DatosContratado
from models.datos_voluntario import DatosVoluntario
from models.datos_asociado import DatosAsociado
from models.cita_atencion import CitaAtencion
# Importa también los de telefono y comentarios...

# IMPORTAMOS NUESTRO ENRUTADOR
from api import rutas_persona

app = FastAPI(title="API Asociación ASOCOLGI")

# Este evento se dispara justo cuando arranca el servidor
@app.on_event("startup")
def on_startup():
    print("Iniciando la creación de la base de datos...")
    create_db_and_tables()

    print("Sembrando datos maestros...")
    inicializar_estados_base() # Llamamos al sembrador mágico

# ENCHUFAMOS LAS RUTAS A LA APLICACIÓN PRINCIPAL
app.include_router(rutas_persona.router)

@app.get("/")
def read_root():
    return {"mensaje": "El backend respira."}