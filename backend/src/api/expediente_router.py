from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session
from domain.schemas.expediente_schemas import (
    ExpedienteCreateRequest,
    ExpedienteUpdateRequest,
    ExpedienteResponse
)
from infrastructure.database import get_session
from infrastructure.expediente_repository import ExpedienteRepository
from infrastructure.persona_repository import PersonaRepository
from application.expediente_service import ExpedienteService
from api.dependencies import get_current_user

router = APIRouter(
    tags=["Expedientes Legales"],
    dependencies=[Depends(get_current_user)]
)

def get_expediente_service(session: Session = Depends(get_session)) -> ExpedienteService:
    expediente_repo = ExpedienteRepository(session)
    persona_repo = PersonaRepository(session)
    return ExpedienteService(expediente_repo, persona_repo)

@router.get("/expedientes", response_model=List[ExpedienteResponse])
@router.get("/expedientes/", response_model=List[ExpedienteResponse])
def obtener_todos_expedientes(
    estado: Optional[str] = Query(default=None),
    service: ExpedienteService = Depends(get_expediente_service)
):
    """Obtiene todos los expedientes legales, opcionalmente filtrados por estado"""
    return service.obtener_todos_expedientes(estado=estado)

@router.post("/personas/{id_persona}/expedientes", response_model=ExpedienteResponse, status_code=status.HTTP_201_CREATED)
def crear_expediente(
    id_persona: int,
    request: ExpedienteCreateRequest,
    service: ExpedienteService = Depends(get_expediente_service)
):
    """Crea un nuevo expediente legal para un voluntario"""
    return service.crear_expediente(id_persona, request)

@router.get("/personas/{id_persona}/expedientes", response_model=List[ExpedienteResponse])
def obtener_expedientes_persona(
    id_persona: int,
    service: ExpedienteService = Depends(get_expediente_service)
):
    """Obtiene los expedientes de una persona específica"""
    return service.obtener_expedientes_persona(id_persona)

@router.get("/expedientes/{id_expediente}", response_model=ExpedienteResponse)
def obtener_expediente(
    id_expediente: int,
    service: ExpedienteService = Depends(get_expediente_service)
):
    """Obtiene un expediente legal por su id"""
    return service.obtener_expediente_por_id(id_expediente)

@router.patch("/expedientes/{id_expediente}", response_model=ExpedienteResponse)
def actualizar_expediente(
    id_expediente: int,
    request: ExpedienteUpdateRequest,
    service: ExpedienteService = Depends(get_expediente_service)
):
    """Actualiza el estado o tipo de trámite de un expediente"""
    return service.actualizar_expediente(id_expediente, request)

@router.delete("/expedientes/{id_expediente}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_expediente(
    id_expediente: int,
    service: ExpedienteService = Depends(get_expediente_service)
):
    """Elimina un expediente legal"""
    service.eliminar_expediente(id_expediente)
