from typing import List, Optional
from fastapi import HTTPException, status
from domain.models.roles import DatosVoluntario
from domain.schemas.voluntario_schemas import (
    VoluntarioCreateRequest,
    VoluntarioUpdateRequest,
    VoluntarioResponse,
    PersonaMinimaVoluntarioSchema
)
from infrastructure.voluntario_repository import VoluntarioRepository
from infrastructure.persona_repository import PersonaRepository

class VoluntarioService:
    def __init__(self, repository: VoluntarioRepository, persona_repository: PersonaRepository):
        self.repository = repository
        self.persona_repository = persona_repository

    def _to_response(self, voluntario: DatosVoluntario) -> VoluntarioResponse:
        persona = self.persona_repository.get_by_id(voluntario.id_persona)
        persona_minima = None
        if persona:
            persona_minima = PersonaMinimaVoluntarioSchema(
                id=persona.id,
                numero_identificacion=persona.numero_identificacion,
                nombre_completo=persona.nombre_completo,
                correo_electronico=persona.correo_electronico,
                telefono_principal=persona.telefono_principal
            )
        return VoluntarioResponse(
            id=voluntario.id,
            id_persona=voluntario.id_persona,
            cargo=voluntario.cargo,
            campo_accion=voluntario.campo_accion,
            tipo=voluntario.tipo,
            horas_semana=voluntario.horas_semana,
            url_doc=voluntario.url_doc,
            url_cv=voluntario.url_cv,
            fecha_vinculacion=voluntario.fecha_vinculacion,
            carta_compromiso_firmada=voluntario.carta_compromiso_firmada,
            formulario_inscripcion=voluntario.formulario_inscripcion,
            persona=persona_minima
        )

    def obtener_todos(self, limit: int = 50, offset: int = 0) -> List[VoluntarioResponse]:
        voluntarios = self.repository.get_all(limit=limit, offset=offset)
        return [self._to_response(v) for v in voluntarios]

    def obtener_por_id(self, id_voluntario: int) -> VoluntarioResponse:
        voluntario = self.repository.get_by_id(id_voluntario)
        if not voluntario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voluntario no encontrado")
        return self._to_response(voluntario)

    def crear_voluntario(self, request: VoluntarioCreateRequest) -> VoluntarioResponse:
        persona = self.persona_repository.get_by_id(request.id_persona)
        if not persona:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada")

        existente = self.repository.get_by_persona_id(request.id_persona)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta persona ya está registrada como voluntario")

        nuevo = DatosVoluntario(
            id_persona=request.id_persona,
            cargo=request.cargo or "Voluntario",
            campo_accion=request.campo_accion or "General",
            tipo=request.tipo or "Presencial",
            horas_semana=request.horas_semana or 1,
            url_doc=request.url_doc,
            url_cv=request.url_cv,
            fecha_vinculacion=request.fecha_vinculacion,
            carta_compromiso_firmada=request.carta_compromiso_firmada,
            formulario_inscripcion=request.formulario_inscripcion
        )
        creado = self.repository.create(nuevo)
        return self._to_response(creado)

    def actualizar_voluntario(self, id_voluntario: int, request: VoluntarioUpdateRequest) -> VoluntarioResponse:
        voluntario = self.repository.get_by_id(id_voluntario)
        if not voluntario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voluntario no encontrado")

        if request.cargo is not None:
            voluntario.cargo = request.cargo
        if request.campo_accion is not None:
            voluntario.campo_accion = request.campo_accion
        if request.tipo is not None:
            voluntario.tipo = request.tipo
        if request.horas_semana is not None:
            voluntario.horas_semana = request.horas_semana
        if request.url_doc is not None:
            voluntario.url_doc = request.url_doc
        if request.url_cv is not None:
            voluntario.url_cv = request.url_cv
        if request.fecha_vinculacion is not None:
            voluntario.fecha_vinculacion = request.fecha_vinculacion
        if request.carta_compromiso_firmada is not None:
            voluntario.carta_compromiso_firmada = request.carta_compromiso_firmada
        if request.formulario_inscripcion is not None:
            voluntario.formulario_inscripcion = request.formulario_inscripcion

        actualizado = self.repository.update(voluntario)
        return self._to_response(actualizado)

    def eliminar_voluntario(self, id_voluntario: int):
        voluntario = self.repository.get_by_id(id_voluntario)
        if not voluntario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voluntario no encontrado")
        self.repository.delete(voluntario)
