from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from domain.schemas.comentario_schemas import (
    ComentarioCreateRequest,
    ComentarioUpdateRequest,
    ComentarioResponse
)
from infrastructure.database import get_session
from infrastructure.comentario_repository import ComentarioRepository
from infrastructure.persona_repository import PersonaRepository
from application.comentario_service import ComentarioService
from api.dependencies import get_current_user

router = APIRouter(
    tags=["Gestión de Comentarios"],
    dependencies=[Depends(get_current_user)]
)

def get_comentario_service(session: Session = Depends(get_session)) -> ComentarioService:
    comentario_repo = ComentarioRepository(session)
    persona_repo = PersonaRepository(session)
    return ComentarioService(comentario_repo, persona_repo)

@router.post("/personas/{id_persona}/comentarios", response_model=ComentarioResponse, status_code=status.HTTP_201_CREATED)
def agregar_comentario(
    id_persona: int,
    request: ComentarioCreateRequest,
    service: ComentarioService = Depends(get_comentario_service)
):
    """Agrega un nuevo comentario a una persona"""
    return service.crear_comentario(id_persona, request)

@router.get("/personas/{id_persona}/comentarios", response_model=List[ComentarioResponse])
def obtener_comentarios_persona(
    id_persona: int,
    service: ComentarioService = Depends(get_comentario_service)
):
    """Obtiene el listado de comentarios de una persona en orden descendente"""
    return service.obtener_comentarios_persona(id_persona)

@router.patch("/comentarios/{id_comentario}", response_model=ComentarioResponse)
def actualizar_comentario(
    id_comentario: int,
    request: ComentarioUpdateRequest,
    service: ComentarioService = Depends(get_comentario_service)
):
    """Actualiza el texto y/o categoría de un comentario"""
    return service.actualizar_comentario(id_comentario, request)

@router.delete("/comentarios/{id_comentario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_comentario(
    id_comentario: int,
    service: ComentarioService = Depends(get_comentario_service)
):
    """Elimina un comentario por su id"""
    service.eliminar_comentario(id_comentario)
