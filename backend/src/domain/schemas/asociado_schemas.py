from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class AsociadoCreateRequest(BaseModel):
    id_persona: int = Field(..., description="ID de la persona a asociar", json_schema_extra={"example": 1})
    metodo_pago: Optional[str] = Field("Efectivo", description="Método de pago de cuota", json_schema_extra={"example": "Efectivo"})
    estado_membresia: Optional[str] = Field("Activo", description="Estado de membresía", json_schema_extra={"example": "Activo"})
    estado_pago: Optional[str] = Field("Al dia", description="Estado de pago", json_schema_extra={"example": "Al dia"})
    autoriza_whatsapp: bool = Field(False, description="Autorización de WhatsApp", json_schema_extra={"example": True})
    fecha_vinculacion: Optional[date] = Field(None, description="Fecha de vinculación", json_schema_extra={"example": "2026-09-06"})

class AsociadoUpdateRequest(BaseModel):
    metodo_pago: Optional[str] = Field(None, description="Método de pago de cuota")
    estado_membresia: Optional[str] = Field(None, description="Estado de membresía")
    estado_pago: Optional[str] = Field(None, description="Estado de pago")
    autoriza_whatsapp: Optional[bool] = Field(None, description="Autorización de WhatsApp")
    fecha_vinculacion: Optional[date] = Field(None, description="Fecha de vinculación")

class PersonaMinimaSchema(BaseModel):
    id: int
    numero_identificacion: str
    nombre_completo: str
    correo_electronico: Optional[str] = None
    telefono_principal: Optional[str] = None

class AsociadoResponse(BaseModel):
    id: int
    id_persona: int
    metodo_pago: Optional[str] = None
    estado_membresia: Optional[str] = None
    estado_pago: Optional[str] = None
    autoriza_whatsapp: bool = False
    fecha_vinculacion: Optional[date] = None
    persona: Optional[PersonaMinimaSchema] = None

    class Config:
        from_attributes = True
