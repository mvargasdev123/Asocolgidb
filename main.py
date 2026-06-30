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
from models.datos_voluntario import DatosVoluntario
from models.datos_asociado import DatosAsociado
from models.cita_atencion import CitaAtencion
from models.usuario import Usuario
from models.telefono_persona import Telefono
from models.catalogos import NivelEducativo, MotivoConsulta, Derivacion, TecnicaAcogida
from models.expediente import Expediente
from models.comentario import Comentario


# Importa también los de telefono y comentarios...

# IMPORTAMOS NUESTRO ENRUTADOR
from api import rutas_persona, rutas_roles, rutas_citas, rutas_auth, rutas_estadisticas, rutas_comentarios, rutas_expedientes# Añadimos rutas_roles

app = FastAPI(title="API Asociación ASOCOLGI", 
            description="Backend de grado empresarial para la gestión de la asociación",
            version="1.0.0"
            )

# --- LA BARRERA DE PROTECCIÓN CORS ---
# Por ahora, en desarrollo/staging, le permitiremos el acceso a TODO EL MUNDO ("*").
# Cuando el frontend tenga una URL fija (ej: app.asocolgi.org), reemplazarás el "*" por esa URL.
origins = [
    "*",
]

# Debe ir justo debajo de la creación de 'app' y antes de las rutas
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Quién puede hablar con la API
    allow_credentials=True,
    allow_methods=["*"],         # Qué métodos se permiten (GET, POST, DELETE, etc.)
    allow_headers=["*"],         # Qué cabeceras se permiten (como la de Authorization con el JWT)
)

# Este evento se dispara justo cuando arranca el servidor
@app.on_event("startup")
def on_startup():

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
app.include_router(rutas_expedientes.router)

@app.get("/")
def read_root():
    return {"mensaje": "El backend respira."}