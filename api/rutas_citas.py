from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

# Importaciones de nuestras herramientas
from database import get_session
from schemas.cita_schema import CitaCreate, CitaRead
from services.servicio_citas import ServicioCitas

# Creamos el enrutador
router = APIRouter(prefix="/citas", tags=["Gestión de Citas"])

@router.post("/{id_persona}", response_model=CitaRead)
def registrar_nueva_cita(
    datos_entrada: CitaCreate,
    id_persona: int = Path(..., description="ID de la persona que recibe la atención"),
    session: Session = Depends(get_session)
):
    # Instanciamos el cerebro de las citas
    servicio = ServicioCitas(session)
    
    # Ejecutamos la lógica y devolvemos el resultado
    return servicio.agendar_cita(id_persona, datos_entrada)