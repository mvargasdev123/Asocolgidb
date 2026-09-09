from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from domain.models.expediente import Expediente
from domain.schemas.expediente_schemas import (
    ExpedienteCreateRequest,
    ExpedienteUpdateRequest,
    ExpedienteResponse,
    PersonaSummarySchema
)
from infrastructure.expediente_repository import ExpedienteRepository
from infrastructure.persona_repository import PersonaRepository

class ExpedienteService:
    def __init__(self, repository: ExpedienteRepository, persona_repository: PersonaRepository):
        self.repository = repository
        self.persona_repository = persona_repository

    def _to_response(self, expediente: Expediente) -> ExpedienteResponse:
        persona = self.persona_repository.get_by_id(expediente.id_persona)
        persona_summary = None
        if persona:
            persona_summary = PersonaSummarySchema(
                id=persona.id,
                nombre_completo=persona.nombre_completo,
                numero_identificacion=persona.numero_identificacion
            )

        return ExpedienteResponse(
            id=expediente.id,
            id_persona=expediente.id_persona,
            numero_registro=expediente.numero_registro,
            tipo_tramite=expediente.tipo_tramite,
            fecha_presentacion=expediente.fecha_presentacion,
            estado=expediente.estado,
            numero_expediente_asignado=expediente.numero_expediente_asignado,
            representante_legal=expediente.representante_legal,
            consultorio_juridico=expediente.consultorio_juridico,
            aporte_social=expediente.aporte_social,
            solicitante_extranjeria=expediente.solicitante_extranjeria,
            antecedentes_traducidos_y_apostillados=expediente.antecedentes_traducidos_y_apostillados,
            fecha_resolucion=expediente.fecha_resolucion,
            creado_en=expediente.creado_en,
            persona=persona_summary
        )

    def crear_expediente(self, id_persona: int, request: ExpedienteCreateRequest) -> ExpedienteResponse:
        persona = self.persona_repository.get_by_id(id_persona)
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada"
            )

        # Asegurar que la persona tenga datos_voluntario registrados
        if not persona.datos_voluntario:
            from domain.models.roles import DatosVoluntario
            vol = DatosVoluntario(
                id_persona=id_persona,
                cargo="Voluntario",
                campo_accion="General",
                tipo="Presencial",
                horas_semana=1
            )
            self.persona_repository.session.add(vol)
            self.persona_repository.session.commit()
            self.persona_repository.session.refresh(persona)

        # Regla: Solo un expediente activo ("En tramite") a la vez
        expediente_activo = self.repository.get_active_by_persona_id(id_persona)
        if expediente_activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta persona ya cuenta con un expediente en trámite (activo)"
            )

        # Generar secuencia EXP-YYYY-XXXX
        year = request.fecha_presentacion.year if request.fecha_presentacion else datetime.now().year
        next_seq = self.repository.get_next_sequence_number(year)
        numero_registro = f"EXP-{year}-{next_seq:04d}"

        nuevo = Expediente(
            id_persona=id_persona,
            numero_registro=numero_registro,
            tipo_tramite=request.tipo_tramite.strip(),
            fecha_presentacion=request.fecha_presentacion,
            estado="En tramite",
            numero_expediente_asignado=request.numero_expediente_asignado.strip() if request.numero_expediente_asignado else None,
            representante_legal=request.representante_legal.strip() if request.representante_legal else None,
            consultorio_juridico=request.consultorio_juridico.strip() if request.consultorio_juridico else None,
            aporte_social=request.aporte_social or "Sí",
            solicitante_extranjeria=request.solicitante_extranjeria,
            antecedentes_traducidos_y_apostillados=request.antecedentes_traducidos_y_apostillados,
            fecha_resolucion=request.fecha_resolucion
        )

        creado = self.repository.create(nuevo)
        return self._to_response(creado)

    def obtener_todos_expedientes(self, estado: Optional[str] = None) -> List[ExpedienteResponse]:
        expedientes = self.repository.get_all(estado=estado)
        return [self._to_response(e) for e in expedientes]

    def obtener_expedientes_persona(self, id_persona: int) -> List[ExpedienteResponse]:
        persona = self.persona_repository.get_by_id(id_persona)
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada"
            )
        expedientes = self.repository.get_by_persona_id(id_persona)
        return [self._to_response(e) for e in expedientes]

    def obtener_expediente_por_id(self, id_expediente: int) -> ExpedienteResponse:
        expediente = self.repository.get_by_id(id_expediente)
        if not expediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expediente no encontrado"
            )
        return self._to_response(expediente)

    def actualizar_expediente(self, id_expediente: int, request: ExpedienteUpdateRequest) -> ExpedienteResponse:
        expediente = self.repository.get_by_id(id_expediente)
        if not expediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expediente no encontrado"
            )

        if request.tipo_tramite is not None and request.tipo_tramite.strip():
            expediente.tipo_tramite = request.tipo_tramite.strip()

        if request.estado is not None and request.estado.strip():
            nuevo_estado = request.estado.strip()
            if nuevo_estado == "En tramite" and expediente.estado != "En tramite":
                activo_existente = self.repository.get_active_by_persona_id(expediente.id_persona)
                if activo_existente and activo_existente.id != expediente.id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El voluntario ya cuenta con otro expediente en trámite (activo)"
                    )
            expediente.estado = nuevo_estado

        if request.numero_expediente_asignado is not None:
            expediente.numero_expediente_asignado = request.numero_expediente_asignado
        if request.representante_legal is not None:
            expediente.representante_legal = request.representante_legal
        if request.consultorio_juridico is not None:
            expediente.consultorio_juridico = request.consultorio_juridico
        if request.aporte_social is not None:
            expediente.aporte_social = request.aporte_social
        if request.solicitante_extranjeria is not None:
            expediente.solicitante_extranjeria = request.solicitante_extranjeria
        if request.antecedentes_traducidos_y_apostillados is not None:
            expediente.antecedentes_traducidos_y_apostillados = request.antecedentes_traducidos_y_apostillados
        if request.fecha_resolucion is not None:
            expediente.fecha_resolucion = request.fecha_resolucion

        actualizado = self.repository.update(expediente)
        return self._to_response(actualizado)

    def eliminar_expediente(self, id_expediente: int):
        expediente = self.repository.get_by_id(id_expediente)
        if not expediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expediente no encontrado"
            )
        self.repository.delete(expediente)
