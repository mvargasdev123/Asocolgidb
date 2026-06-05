from fastapi import APIRouter, Depends
from sqlmodel import Session

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