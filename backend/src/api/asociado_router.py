from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from domain.schemas.asociado_schemas import (
    AsociadoCreateRequest,
    AsociadoUpdateRequest,
    AsociadoResponse
)
from infrastructure.database import get_session
from infrastructure.asociado_repository import AsociadoRepository
from infrastructure.persona_repository import PersonaRepository
from application.asociado_service import AsociadoService
from api.dependencies import get_current_user

router = APIRouter(
    prefix="/asociados",
    tags=["Gestión de Asociados"],
    dependencies=[Depends(get_current_user)]
)

def get_asociado_service(session: Session = Depends(get_session)) -> AsociadoService:
    repo = AsociadoRepository(session)
    persona_repo = PersonaRepository(session)
    return AsociadoService(repo, persona_repo)

@router.get("/", response_model=List[AsociadoResponse])
def obtener_todos_asociados(
    limit: int = 50,
    offset: int = 0,
    service: AsociadoService = Depends(get_asociado_service)
):
    """Obtiene el listado de asociados activos"""
    return service.obtener_todos(limit=limit, offset=offset)

@router.get("/{id_asociado}", response_model=AsociadoResponse)
def obtener_asociado(
    id_asociado: int,
    service: AsociadoService = Depends(get_asociado_service)
):
    """Obtiene el detalle de un asociado por ID"""
    return service.obtener_por_id(id_asociado)

@router.post("/", response_model=AsociadoResponse, status_code=status.HTTP_201_CREATED)
def crear_asociado(
    request: AsociadoCreateRequest,
    service: AsociadoService = Depends(get_asociado_service)
):
    """Asigna el rol de asociado a una persona existente"""
    return service.crear_asociado(request)

@router.patch("/{id_asociado}", response_model=AsociadoResponse)
def actualizar_asociado(
    id_asociado: int,
    request: AsociadoUpdateRequest,
    service: AsociadoService = Depends(get_asociado_service)
):
    """Actualiza datos del perfil de asociado"""
    return service.actualizar_asociado(id_asociado, request)

@router.delete("/{id_asociado}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asociado(
    id_asociado: int,
    service: AsociadoService = Depends(get_asociado_service)
):
    """Elimina el registro de asociado"""
    service.eliminar_asociado(id_asociado)
