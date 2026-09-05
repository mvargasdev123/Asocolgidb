from typing import List
from fastapi import HTTPException, status
from domain.models.comentario import Comentario
from domain.schemas.comentario_schemas import (
    ComentarioCreateRequest,
    ComentarioUpdateRequest,
    ComentarioResponse
)
from infrastructure.comentario_repository import ComentarioRepository
from infrastructure.persona_repository import PersonaRepository

class ComentarioService:
    def __init__(self, repository: ComentarioRepository, persona_repository: PersonaRepository):
        self.repository = repository
        self.persona_repository = persona_repository

    def crear_comentario(self, id_persona: int, request: ComentarioCreateRequest) -> ComentarioResponse:
        persona = self.persona_repository.get_by_id(id_persona)
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada"
            )

        texto_clean = request.texto.strip()
        if not texto_clean:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El texto del comentario no puede estar vacío"
            )

        kwargs = {
            "id_persona": id_persona,
            "texto": texto_clean,
            "tipo": request.tipo if request.tipo else "Persona"
        }
        if request.fecha_creacion is not None:
            kwargs["fecha_creacion"] = request.fecha_creacion

        nuevo_comentario = Comentario(**kwargs)

        creado = self.repository.create(nuevo_comentario)
        return ComentarioResponse.model_validate(creado)

    def obtener_comentarios_persona(self, id_persona: int) -> List[ComentarioResponse]:
        persona = self.persona_repository.get_by_id(id_persona)
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada"
            )

        comentarios = self.repository.get_by_persona_id(id_persona)
        return [ComentarioResponse.model_validate(c) for c in comentarios]

    def actualizar_comentario(self, id_comentario: int, request: ComentarioUpdateRequest) -> ComentarioResponse:
        comentario = self.repository.get_by_id(id_comentario)
        if not comentario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentario no encontrado"
            )

        if request.texto is not None:
            texto_clean = request.texto.strip()
            if not texto_clean:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El texto del comentario no puede estar vacío"
                )
            comentario.texto = texto_clean

        if request.tipo is not None:
            comentario.tipo = request.tipo

        if request.fecha_creacion is not None:
            comentario.fecha_creacion = request.fecha_creacion

        actualizado = self.repository.update(comentario)
        return ComentarioResponse.model_validate(actualizado)

    def eliminar_comentario(self, id_comentario: int):
        comentario = self.repository.get_by_id(id_comentario)
        if not comentario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentario no encontrado"
            )

        self.repository.delete(comentario)
