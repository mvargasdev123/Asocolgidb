from typing import List, Optional
from fastapi import HTTPException, status
from domain.models.roles import DatosAsociado
from domain.schemas.asociado_schemas import (
    AsociadoCreateRequest,
    AsociadoUpdateRequest,
    AsociadoResponse,
    PersonaMinimaSchema
)
from infrastructure.asociado_repository import AsociadoRepository
from infrastructure.persona_repository import PersonaRepository

class AsociadoService:
    def __init__(self, repository: AsociadoRepository, persona_repository: PersonaRepository):
        self.repository = repository
        self.persona_repository = persona_repository

    def _to_response(self, asociado: DatosAsociado) -> AsociadoResponse:
        persona = self.persona_repository.get_by_id(asociado.id_persona)
        persona_minima = None
        if persona:
            persona_minima = PersonaMinimaSchema(
                id=persona.id,
                numero_identificacion=persona.numero_identificacion,
                nombre_completo=persona.nombre_completo,
                correo_electronico=persona.correo_electronico,
                telefono_principal=persona.telefono_principal
            )
        return AsociadoResponse(
            id=asociado.id,
            id_persona=asociado.id_persona,
            metodo_pago=asociado.metodo_pago,
            estado_membresia=asociado.estado_membresia,
            estado_pago=asociado.estado_pago,
            autoriza_whatsapp=asociado.autoriza_whatsapp,
            persona=persona_minima
        )

    def obtener_todos(self, limit: int = 50, offset: int = 0) -> List[AsociadoResponse]:
        asociados = self.repository.get_all(limit=limit, offset=offset)
        return [self._to_response(a) for a in asociados]

    def obtener_por_id(self, id_asociado: int) -> AsociadoResponse:
        asociado = self.repository.get_by_id(id_asociado)
        if not asociado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asociado no encontrado")
        return self._to_response(asociado)

    def crear_asociado(self, request: AsociadoCreateRequest) -> AsociadoResponse:
        persona = self.persona_repository.get_by_id(request.id_persona)
        if not persona:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada")

        existente = self.repository.get_by_persona_id(request.id_persona)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta persona ya está registrada como asociado")

        nuevo = DatosAsociado(
            id_persona=request.id_persona,
            metodo_pago=request.metodo_pago or "Efectivo",
            estado_membresia=request.estado_membresia or "Activo",
            estado_pago=request.estado_pago or "Al dia",
            autoriza_whatsapp=request.autoriza_whatsapp
        )
        creado = self.repository.create(nuevo)
        return self._to_response(creado)

    def actualizar_asociado(self, id_asociado: int, request: AsociadoUpdateRequest) -> AsociadoResponse:
        asociado = self.repository.get_by_id(id_asociado)
        if not asociado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asociado no encontrado")

        if request.metodo_pago is not None:
            asociado.metodo_pago = request.metodo_pago
        if request.estado_membresia is not None:
            asociado.estado_membresia = request.estado_membresia
        if request.estado_pago is not None:
            asociado.estado_pago = request.estado_pago
        if request.autoriza_whatsapp is not None:
            asociado.autoriza_whatsapp = request.autoriza_whatsapp

        actualizado = self.repository.update(asociado)
        return self._to_response(actualizado)

    def eliminar_asociado(self, id_asociado: int):
        asociado = self.repository.get_by_id(id_asociado)
        if not asociado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asociado no encontrado")
        self.repository.delete(asociado)
