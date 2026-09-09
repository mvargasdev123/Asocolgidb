from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field

class ExpedienteCreateRequest(BaseModel):
    tipo_tramite: str = Field(..., description="Tipo de trámite legal", json_schema_extra={"example": "Renovación NIE"})
    fecha_presentacion: date = Field(..., description="Fecha de presentación", json_schema_extra={"example": "2026-09-06"})
    numero_expediente_asignado: Optional[str] = Field(None, description="Número de expediente asignado opcional", json_schema_extra={"example": "EXP-2026-001"})
    representante_legal: Optional[str] = Field(None, description="Representante legal", json_schema_extra={"example": "Dr. Carlos Ruiz"})
    consultorio_juridico: Optional[str] = Field(None, description="Consultorio jurídico", json_schema_extra={"example": "Consultorio Central"})
    aporte_social: Optional[str] = Field("Sí", description="Aporte social ('Sí' / 'No')", json_schema_extra={"example": "Sí"})
    solicitante_extranjeria: bool = Field(False, description="Solicitante de extranjería", json_schema_extra={"example": False})
    antecedentes_traducidos_y_apostillados: bool = Field(False, description="Antecedentes traducidos y apostillados", json_schema_extra={"example": False})
    fecha_resolucion: Optional[date] = Field(None, description="Fecha de resolución opcional", json_schema_extra={"example": None})

class ExpedienteUpdateRequest(BaseModel):
    tipo_tramite: Optional[str] = None
    estado: Optional[str] = None
    numero_expediente_asignado: Optional[str] = None
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[str] = None
    solicitante_extranjeria: Optional[bool] = None
    antecedentes_traducidos_y_apostillados: Optional[bool] = None
    fecha_resolucion: Optional[date] = None

class PersonaSummarySchema(BaseModel):
    id: int
    nombre_completo: str
    numero_identificacion: str

class ExpedienteResponse(BaseModel):
    id: int
    id_persona: int
    numero_registro: str
    tipo_tramite: str
    fecha_presentacion: date
    estado: str
    numero_expediente_asignado: Optional[str] = None
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[str] = "Sí"
    solicitante_extranjeria: bool = False
    antecedentes_traducidos_y_apostillados: bool = False
    fecha_resolucion: Optional[date] = None
    creado_en: datetime
    persona: Optional[PersonaSummarySchema] = None

    class Config:
        from_attributes = True
