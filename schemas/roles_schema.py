from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from models.datos_asociado import MetodoPagoEnum, EstadoAsociadoEnum, EstadoPagoEnum

class VoluntarioCreate(BaseModel):
    id_persona: int = Field(..., description="ID de la víctima... digo, del voluntario")
    cargo: str = Field(..., min_length=2, max_length=150, description="Ej: Coordinador de Logística")
    area_voluntariado: str = Field(..., min_length=2, max_length=150, description="Ej: Legal, Eventos")
    horas_disponibles: int = Field(..., ge=1, description="Mínimo 1 hora, no aceptamos perezosos")
    
    # Documentos
    carta_compromiso_entregada: bool = Field(default=False)
    formulario_inscripcion_entregado: bool = Field(default=False)
    curriculum_url: Optional[str] = Field(default=None)

    class Config:
        orm_mode = True

class AsociadoCreate(BaseModel):
    id_persona: int = Field(..., description="ID de la persona a ascender")
    numero_registro_asociado: str = Field(..., min_length=1, max_length=50)
    metodo_pago: MetodoPagoEnum
    autoriza_whatsapp: bool = Field(default=False)
    estado_membresia: EstadoAsociadoEnum = Field(default=EstadoAsociadoEnum.ACTIVO)
    estado_pago: EstadoPagoEnum = Field(default=EstadoPagoEnum.AL_DIA)
    
    class Config:
        orm_mode = True