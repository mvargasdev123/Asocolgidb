from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from services.servicio_estadisticas import ServicioEstadisticas
from api.dependencias import obtener_usuario_actual # El pase VIP

router = APIRouter(
    prefix="/estadisticas", 
    tags=["Dashboard y Métricas"],
    dependencies=[Depends(obtener_usuario_actual)] # Guardia activado
)

@router.get("/")
def obtener_resumen_dashboard(session: Session = Depends(get_session)):
    servicio = ServicioEstadisticas(session)
    return servicio.obtener_panel_principal()