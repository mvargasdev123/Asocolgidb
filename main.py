from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, engine, inicializar_estados_base, inicializar_super_usuario

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
from models.usuario import Usuario

# Importa también los de telefono y comentarios...

# IMPORTAMOS NUESTRO ENRUTADOR
from api import rutas_persona, rutas_roles, rutas_citas, rutas_auth, rutas_estadisticas, rutas_comentarios # Añadimos rutas_roles

app = FastAPI(title="API Asociación ASOCOLGI")

# Debe ir justo debajo de la creación de 'app' y antes de las rutas
app.add_middleware(
    CORSMiddleware,
    # El asterisco "*" significa "deja entrar a todo el mundo". 
    # Para desarrollo está perfecto. Cuando subas esto a un servidor real, 
    # aquí pondrás la URL exacta de tu frontend (ej. ["https://app.asocolgi.org"])
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los verbos (GET, POST, PATCH, DELETE)
    allow_headers=["*"], # Permite todos los encabezados
)

# Este evento se dispara justo cuando arranca el servidor
@app.on_event("startup")
def on_startup():
    print("Iniciando la creación de la base de datos...")
    create_db_and_tables()

    print("Sembrando datos maestros...")
    inicializar_estados_base() # Llamamos al sembrador mágico
    inicializar_super_usuario() # Llamamos al super usuario

# ENCHUFAMOS LAS RUTAS A LA APLICACIÓN PRINCIPAL
app.include_router(rutas_persona.router)
app.include_router(rutas_roles.router) # Conectamos los roles
app.include_router(rutas_citas.router)
app.include_router(rutas_auth.router)
app.include_router(rutas_estadisticas.router)
app.include_router(rutas_comentarios.router)

@app.get("/")
def read_root():
    return {"mensaje": "El backend respira."}