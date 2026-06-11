from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

# Importamos nuestras herramientas habituales
from database import get_session
from schemas.roles_schema import VoluntarioCreate
from services.servicio_roles import ServicioRoles

# Creamos el enrutador específico para las operaciones de roles
router = APIRouter(prefix="/roles", tags=["Gestión de Roles"])

@router.post("/ascender/voluntario/{id_persona}")
def ascender_persona_a_voluntario(
    datos_entrada: VoluntarioCreate, # El cuerpo de la petición (JSON)
    # Validamos que el ID de la URL sea un número entero
    id_persona: int = Path(..., description="ID del registro en Asocolgi"), 
    session: Session = Depends(get_session) # Inyectamos la conexión a SQLite
):
    # Instanciamos nuestro flamante servicio de roles
    servicio = ServicioRoles(session)
    
    # Ejecutamos la mutación. Si algo falla (ej. si la persona no existe), 
    # el servicio lanzará un HTTPException automáticamente.
    resultado = servicio.ascender_a_voluntario(id_persona, datos_entrada)
    
    return resultado