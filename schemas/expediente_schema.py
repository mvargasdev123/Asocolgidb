from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, constr
from models.expediente import EstadoExpedienteEnum, AporteSocialEnum

class ExpedienteCreate(BaseModel):
    # Obligatorios (El portero no los deja pasar sin esto)
    numero_registro: str = Field(..., min_length=3, max_length=50, description="Ej: EXP-2026-001")
    tipo_tramite: str = Field(..., min_length=3, max_length=150, description="Ej: Renovación NIE")
    fecha_presentacion: date
    
    # Opcionales (Tienen valores por defecto o pueden ser null)
    # Si el frontend no lo envía, asumimos que está "En trámite"
    estado: Optional[EstadoExpedienteEnum] = Field(default=EstadoExpedienteEnum.EN_TRAMITE) 
    
    numero_expediente_asignado: Optional[str] = None
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[AporteSocialEnum] = None
    
    solicitante_extranjeria: Optional[bool] = False
    antecedentes_traducidos_y_apostillados: Optional[bool] = False
    fecha_resolucion: Optional[date] = None

    class Config:
        from_attributes = True

class ExpedienteUpdate(BaseModel):
    numero_registro: Optional[str] = Field(None, min_length=3, max_length=50)
    tipo_tramite: Optional[str] = Field(None, min_length=3, max_length=150)
    fecha_presentacion: Optional[date] = None
    estado: Optional[EstadoExpedienteEnum] = None
    numero_expediente_asignado: Optional[str] = None
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[AporteSocialEnum] = None
    solicitante_extranjeria: Optional[bool] = None
    antecedentes_traducidos_y_apostillados: Optional[bool] = None
    fecha_resolucion: Optional[date] = None

    class Config:
        from_attributes = True

class ExpedienteRead(BaseModel):
    id: int
    id_persona: int
    numero_registro: str
    numero_expediente_asignado: Optional[str] = None
    tipo_tramite: str
    fecha_presentacion: date
    estado: EstadoExpedienteEnum
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[AporteSocialEnum] = None
    solicitante_extranjeria: bool
    antecedentes_traducidos_y_apostillados: bool
    fecha_resolucion: Optional[date] = None

    class Config:
        from_attributes = True
