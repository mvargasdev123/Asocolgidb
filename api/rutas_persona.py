from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi import HTTPException

# Importamos nuestras herramientas
from database import get_session
from schemas.persona_schema import PersonaCreate, PersonaRead
from services.servicio_persona import ServicioPersona

# Creamos un "mini-FastAPI" solo para las rutas de las personas
router = APIRouter(prefix="/personas", tags=["Personas"])

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
def listar_personas(session: Session = Depends(get_session)):
    servicio = ServicioPersona(session)
    return servicio.obtener_todas_las_personas()

# Los corchetes {id_persona} le dicen a FastAPI que ese pedazo de la URL es una variable
@router.get("/{id_persona}", response_model=PersonaRead)
def obtener_persona(id_persona: int, session: Session = Depends(get_session)):
    servicio = ServicioPersona(session)
    persona = servicio.obtener_persona_por_id(id_persona)
    
    # Si la persona es 'None' (no se encontró en la BD), lanzamos una granada 404
    if not persona:
        raise HTTPException(status_code=404, detail="Ese registro no existe en Asocolgi. Revisa el ID.")
    
    return persona