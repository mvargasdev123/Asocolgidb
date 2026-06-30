from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, constr
# Nota: Importamos el Enum para que Pydantic valide que manden estados correctos
from models.expediente import EstadoExpedienteEnum 

class ExpedienteCreate(BaseModel):
    # Obligatorios (El portero no los deja pasar sin esto)
    id_persona: int = Field(..., description="ID del Asociado dueño del trámite")
    numero_registro: str = Field(..., min_length=3, max_length=50, description="Ej: EXP-2026-001")
    tipo_tramite: str = Field(..., min_length=3, max_length=150, description="Ej: Renovación NIE")
    fecha_presentacion: date
    
    # Opcionales (Tienen valores por defecto o pueden ser null)
    # Si el frontend no lo envía, asumimos que está "En trámite"
    estado: Optional[EstadoExpedienteEnum] = Field(default=EstadoExpedienteEnum.EN_TRAMITE) 
    
    numero_expediente_asignado: Optional[str] = None
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[str] = None
    
    solicitante_extranjeria: Optional[bool] = False
    antecedentes_traducidos: Optional[bool] = False
    fecha_resolucion: Optional[date] = None

    class Config:
        # Esto permite que Pydantic entienda los objetos de SQLModel
        orm_mode = True 
        # (Si usas Pydantic v2, esto se cambia a from_attributes = True)
