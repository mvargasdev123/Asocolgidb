from fastapi import APIRouter, Depends
from sqlmodel import Session
from domain.schemas.metrics_schemas import (
    MetricsSummaryResponse,
    AsociadosMorososPendientesResponse
)
from infrastructure.database import get_session
from infrastructure.metrics_repository import MetricsRepository
from application.metrics_service import MetricsService
from api.dependencies import get_current_user

router = APIRouter(
    prefix="/metrics",
    tags=["Dashboard de Métricas"],
    dependencies=[Depends(get_current_user)]
)

def get_metrics_service(session: Session = Depends(get_session)) -> MetricsService:
    repository = MetricsRepository(session)
    return MetricsService(repository)

@router.get("", response_model=MetricsSummaryResponse)
def obtener_metricas(service: MetricsService = Depends(get_metrics_service)):
    """Obtiene el resumen consolidado para el Dashboard de Métricas"""
    return service.obtener_metricas_dashboard()

@router.get("/asociados-morosos-pendientes", response_model=AsociadosMorososPendientesResponse)
def obtener_asociados_morosos_y_pendientes(service: MetricsService = Depends(get_metrics_service)):
    """Obtiene la lista clasificada de asociados morosos y asociados pendientes por cuota"""
    return service.obtener_asociados_morosos_y_pendientes()
