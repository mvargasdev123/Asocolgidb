from fastapi import APIRouter, Depends, Path, HTTPException, Query
from sqlmodel import Session
from typing import Optional

# Importamos nuestras herramientas
from database import get_session
from schemas.persona_schema import PersonaCreate, PersonaRead, PersonaUpdate
from services.servicio_persona import ServicioPersona

# Importamos a nuestro guardia y el modelo del administrador
from api.dependencias import obtener_usuario_actual
from models.usuario import Usuario

# Creamos un "mini-FastAPI" solo para las rutas de las personas
router = APIRouter( 
    prefix="/personas", 
    tags=["Gestión de Personas"],
    dependencies=[Depends(obtener_usuario_actual)])

# Inyectamos la barrera de seguridad en la ruta
@router.post("/", response_model=PersonaRead)
def registrar_nueva_persona(
    datos_entrada: PersonaCreate,
    session: Session = Depends(get_session),
    # 🔥 LA BARRERA MÁGICA:
    usuario_actual: Usuario = Depends(obtener_usuario_actual) 
):
    # Si la ejecución llega a esta línea, es porque el token es legítimo, no ha expirado, 
    # y la variable 'usuario_actual' contiene los datos del admin que hizo la petición.
    servicio = ServicioPersona(session)
    return servicio.registrar_nueva_persona(datos_entrada)

@router.post("/", response_model=PersonaRead)
def crear_nueva_persona(
    datos_entrada: PersonaCreate, # 1. Recibimos y validamos datos con Pydantic
    session: Session = Depends(get_session) # 2. FastAPI nos inyecta la BD mágicamente
):
    # 3. Instanciamos el servicio (el cerebro) entregándole la sesión
    servicio = ServicioPersona(session)
    
    # 4. Le decimos al servicio que haga su magia con los datos validados
    persona_creada = servicio.registrar_nueva_persona(datos_entrada)
    
    # 5. Devolvemos el resultado. 
    # FastAPI lo pasará por PersonaRead automáticamente para filtrar datos sensibles.
    return persona_creada  

@router.get("/", response_model=list[PersonaRead])
def obtener_todas_las_personas(
    skip: int = Query(default=0, ge=0, description="Paginación: saltar N registros"),
    limit: int = Query(default=100, ge=1, le=1000, description="Paginación: límite máximo"),
    # LA NUEVA LÍNEA: El filtro de búsqueda opcional
    busqueda_nombre: Optional[str] = Query(default=None, description="Buscar por coincidencia parcial de nombre"),
    session: Session = Depends(get_session)
):
    servicio = ServicioPersona(session)
    return servicio.obtener_todas_las_personas(skip=skip, limit=limit, busqueda_nombre=busqueda_nombre)

# Los corchetes {id_persona} le dicen a FastAPI que ese pedazo de la URL es una variable
@router.get("/{id_persona}", response_model=PersonaRead)
def obtener_persona(id_persona: int, session: Session = Depends(get_session)):
    servicio = ServicioPersona(session)
    persona = servicio.obtener_persona_por_id(id_persona)
    
    # Si la persona es 'None' (no se encontró en la BD), lanzamos una granada 404
    if not persona:
        raise HTTPException(status_code=404, detail="Ese registro no existe en Asocolgi. Revisa el ID.")
    
    return persona

@router.patch("/{id_persona}", response_model=PersonaRead)
def actualizar_persona(
    datos_entrada: PersonaUpdate,
    id_persona: int = Path(..., description="ID del registro a modificar"),
    session: Session = Depends(get_session)
):
    servicio = ServicioPersona(session)
    return servicio.actualizar_datos_biograficos(id_persona, datos_entrada)

@router.delete("/{id_persona}")
def eliminar_persona(
    id_persona: int = Path(..., description="ID del registro a desactivar"),
    session: Session = Depends(get_session)
):
    servicio = ServicioPersona(session)
    return servicio.dar_de_baja_persona(id_persona)