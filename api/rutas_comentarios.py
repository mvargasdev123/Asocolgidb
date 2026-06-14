from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

from database import get_session
from schemas.comentario_schema import ComentarioCreate, ComentarioRead
from services.servicio_comentario import ServicioComentario
from api.dependencias import obtener_usuario_actual

router = APIRouter(
    prefix="/comentarios", 
    tags=["Gestión de Comentarios"],
    dependencies=[Depends(obtener_usuario_actual)] 
)

@router.post("/{id_persona}", response_model=ComentarioRead)
def agregar_comentario(
    datos_entrada: ComentarioCreate,
    id_persona: int = Path(..., description="ID de la persona comentada"),
    session: Session = Depends(get_session)
):
    servicio = ServicioComentario(session)
    return servicio.agregar_comentario(id_persona, datos_entrada)

@router.delete("/{id_comentario}")
def eliminar_comentario(
    id_comentario: int = Path(..., description="ID del comentario a borrar"),
    session: Session = Depends(get_session)
):
    servicio = ServicioComentario(session)
    return servicio.borrar_comentario(id_comentario)