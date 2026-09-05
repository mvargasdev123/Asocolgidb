from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from domain.schemas.persona_schemas import PersonaCreateRequest, PersonaUpdateRequest
from domain.models.usuario import Usuario
from infrastructure.database import get_session
from infrastructure.persona_repository import PersonaRepository
from application.persona_service import PersonaService
from api.dependencies import get_current_user

# Protegemos TODAS las rutas de este router exigiendo el token JWT
router = APIRouter(
    prefix="/personas",
    tags=["Gestión de Personas"],
    dependencies=[Depends(get_current_user)]
)

def get_persona_service(session: Session = Depends(get_session)) -> PersonaService:
    repository = PersonaRepository(session)
    return PersonaService(repository)

@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_nueva_persona(
    request: PersonaCreateRequest,
    service: PersonaService = Depends(get_persona_service)
):
    """Crea una nueva persona con sus roles y catálogos dinámicos (Spec 02)"""
    return service.registrar_persona(request)

@router.get("/")
def obtener_todas_las_personas(
    last_id: int | None = None,
    limit: int = 10,
    service: PersonaService = Depends(get_persona_service)
):
    """Obtiene el listado de personas activas (Spec 03)"""
    return service.obtener_todas(last_id=last_id, limit=limit)

@router.get("/{id_persona}")
def obtener_persona(
    id_persona: int,
    service: PersonaService = Depends(get_persona_service)
):
    """Obtiene el detalle completo de una persona (Spec 03)"""
    return service.obtener_por_id_dict(id_persona)

@router.patch("/{id_persona}")
def actualizar_persona(
    id_persona: int,
    request: PersonaUpdateRequest,
    service: PersonaService = Depends(get_persona_service)
):
    """Actualiza datos específicos de una persona (Spec 03)"""
    return service.actualizar_persona(id_persona, request)

@router.delete("/{id_persona}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_persona(
    id_persona: int,
    service: PersonaService = Depends(get_persona_service)
):
    """Realiza un Soft Delete (oculta) a la persona sin borrar sus datos (Spec 03)"""
    service.eliminar_persona(id_persona)
