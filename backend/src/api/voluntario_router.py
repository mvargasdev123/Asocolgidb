from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from domain.schemas.voluntario_schemas import (
    VoluntarioCreateRequest,
    VoluntarioUpdateRequest,
    VoluntarioResponse
)
from infrastructure.database import get_session
from infrastructure.voluntario_repository import VoluntarioRepository
from infrastructure.persona_repository import PersonaRepository
from application.voluntario_service import VoluntarioService
from api.dependencies import get_current_user

router = APIRouter(
    prefix="/voluntarios",
    tags=["Gestión de Voluntarios"],
    dependencies=[Depends(get_current_user)]
)

def get_voluntario_service(session: Session = Depends(get_session)) -> VoluntarioService:
    repo = VoluntarioRepository(session)
    persona_repo = PersonaRepository(session)
    return VoluntarioService(repo, persona_repo)

@router.get("/", response_model=List[VoluntarioResponse])
def obtener_todos_voluntarios(
    limit: int = 50,
    offset: int = 0,
    service: VoluntarioService = Depends(get_voluntario_service)
):
    """Obtiene el listado de voluntarios activos"""
    return service.obtener_todos(limit=limit, offset=offset)

@router.get("/{id_voluntario}", response_model=VoluntarioResponse)
def obtener_voluntario(
    id_voluntario: int,
    service: VoluntarioService = Depends(get_voluntario_service)
):
    """Obtiene el detalle de un voluntario por ID"""
    return service.obtener_por_id(id_voluntario)

@router.post("/", response_model=VoluntarioResponse, status_code=status.HTTP_201_CREATED)
def crear_voluntario(
    request: VoluntarioCreateRequest,
    service: VoluntarioService = Depends(get_voluntario_service)
):
    """Asigna el rol de voluntario a una persona existente"""
    return service.crear_voluntario(request)

@router.patch("/{id_voluntario}", response_model=VoluntarioResponse)
def actualizar_voluntario(
    id_voluntario: int,
    request: VoluntarioUpdateRequest,
    service: VoluntarioService = Depends(get_voluntario_service)
):
    """Actualiza datos del perfil de voluntario"""
    return service.actualizar_voluntario(id_voluntario, request)

@router.delete("/{id_voluntario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_voluntario(
    id_voluntario: int,
    service: VoluntarioService = Depends(get_voluntario_service)
):
    """Elimina el registro de voluntario"""
    service.eliminar_voluntario(id_voluntario)
