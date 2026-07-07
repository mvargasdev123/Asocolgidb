from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

from database import get_session
from schemas.comentario_schema import ComentarioCreate, ComentarioRead, ComentarioUpdate
from services.servicio_comentario import ServicioComentario
from api.dependencias import obtener_usuario_actual

router = APIRouter(
    tags=["Gestión de Comentarios"],
    dependencies=[Depends(obtener_usuario_actual)] 
)

@router.post("/personas/{id_persona}/comentarios", response_model=ComentarioRead)
def agregar_comentario(
    datos_entrada: ComentarioCreate,
    id_persona: int = Path(..., description="ID de la persona comentada"),
    session: Session = Depends(get_session)
):
    servicio = ServicioComentario(session)
    return servicio.agregar_comentario(id_persona, datos_entrada)

@router.get("/personas/{id_persona}/comentarios", response_model=list[ComentarioRead])
def obtener_comentarios_persona(
    id_persona: int = Path(..., description="ID de la persona"),
    session: Session = Depends(get_session)
):
    servicio = ServicioComentario(session)
    return servicio.obtener_comentarios_de_persona(id_persona)

@router.patch("/comentarios/{id_comentario}", response_model=ComentarioRead)
def actualizar_comentario(
    datos_entrada: ComentarioUpdate,
    id_comentario: int = Path(..., description="ID del comentario"),
    session: Session = Depends(get_session)
):
    servicio = ServicioComentario(session)
    return servicio.actualizar_comentario(id_comentario, datos_entrada)

@router.delete("/comentarios/{id_comentario}")
def eliminar_comentario(
    id_comentario: int = Path(..., description="ID del comentario a borrar"),
    session: Session = Depends(get_session)
):
    servicio = ServicioComentario(session)
    return servicio.borrar_comentario(id_comentario)