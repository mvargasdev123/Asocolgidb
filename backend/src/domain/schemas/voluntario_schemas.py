from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class VoluntarioCreateRequest(BaseModel):
    id_persona: int = Field(..., description="ID de la persona a registrar como voluntario", json_schema_extra={"example": 1})
    cargo: Optional[str] = Field(None, description="Cargo del voluntario", json_schema_extra={"example": "Coordinador"})
    campo_accion: Optional[str] = Field(None, description="Campo de acción", json_schema_extra={"example": "Jurídico"})
    tipo: Optional[str] = Field(None, description="Tipo de voluntario", json_schema_extra={"example": "Activo"})
    horas_semana: Optional[int] = Field(None, description="Horas por semana", json_schema_extra={"example": 5})
    url_doc: Optional[str] = Field(None, description="URL del documento")
    url_cv: Optional[str] = Field(None, description="URL del CV")
    fecha_vinculacion: Optional[date] = Field(None, description="Fecha de vinculación", json_schema_extra={"example": "2026-09-06"})
    fecha_alta: Optional[date] = Field(None, description="Fecha de alta")
    fecha_baja: Optional[date] = Field(None, description="Fecha de baja")
    carta_compromiso_firmada: bool = Field(False, description="Carta de compromiso firmada", json_schema_extra={"example": True})
    formulario_inscripcion: bool = Field(False, description="Formulario de inscripción completado", json_schema_extra={"example": True})

class VoluntarioUpdateRequest(BaseModel):
    cargo: Optional[str] = Field(None, description="Cargo del voluntario")
    campo_accion: Optional[str] = Field(None, description="Campo de acción")
    tipo: Optional[str] = Field(None, description="Tipo de voluntario")
    horas_semana: Optional[int] = Field(None, description="Horas por semana")
    url_doc: Optional[str] = Field(None, description="URL del documento")
    url_cv: Optional[str] = Field(None, description="URL del CV")
    fecha_vinculacion: Optional[date] = Field(None, description="Fecha de vinculación")
    fecha_alta: Optional[date] = Field(None, description="Fecha de alta")
    fecha_baja: Optional[date] = Field(None, description="Fecha de baja")
    carta_compromiso_firmada: Optional[bool] = Field(None, description="Carta de compromiso firmada")
    formulario_inscripcion: Optional[bool] = Field(None, description="Formulario de inscripción completado")

class PersonaMinimaVoluntarioSchema(BaseModel):
    id: int
    numero_identificacion: str
    nombre_completo: str
    correo_electronico: Optional[str] = None
    telefono_principal: Optional[str] = None

class VoluntarioResponse(BaseModel):
    id: int
    id_persona: int
    cargo: Optional[str] = None
    campo_accion: Optional[str] = None
    tipo: Optional[str] = None
    horas_semana: Optional[int] = None
    url_doc: Optional[str] = None
    url_cv: Optional[str] = None
    fecha_vinculacion: Optional[date] = None
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None
    carta_compromiso_firmada: bool = False
    formulario_inscripcion: bool = False
    persona: Optional[PersonaMinimaVoluntarioSchema] = None

    class Config:
        from_attributes = True
