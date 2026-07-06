from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from models.datos_asociado import MetodoPagoEnum, EstadoAsociadoEnum, EstadoPagoEnum

class VoluntarioCreate(BaseModel):
    # NOTA: id_persona se removió de aquí porque se pedirá por la URL
    cargo: str = Field(..., min_length=2, max_length=150, description="Ej: Coordinador de Logística")
    campo_accion: str = Field(..., min_length=2, max_length=150, description="Ej: Legal, Eventos")
    tipo_voluntariado: Optional[str] = Field(default=None, max_length=100)
    horas_disponibles: int = Field(..., ge=1, description="Mínimo 1 hora, no aceptamos perezosos")
    
    # Documentos
    carta_compromiso_entregada: bool = Field(default=False)
    formulario_inscripcion_entregado: bool = Field(default=False)
    copia_documento_url: Optional[str] = Field(default=None)
    curriculum_url: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True

class VoluntarioUpdate(BaseModel):
    cargo: Optional[str] = Field(None, min_length=2, max_length=150)
    campo_accion: Optional[str] = Field(None, min_length=2, max_length=150)
    tipo_voluntariado: Optional[str] = Field(None, max_length=100)
    horas_disponibles: Optional[int] = Field(None, ge=1)
    
    carta_compromiso_entregada: Optional[bool] = None
    formulario_inscripcion_entregado: Optional[bool] = None
    copia_documento_url: Optional[str] = None
    curriculum_url: Optional[str] = None
    fecha_baja: Optional[date] = None
    activo: Optional[bool] = None

class VoluntarioRead(BaseModel):
    cargo: str
    campo_accion: str
    tipo_voluntariado: Optional[str] = None
    horas_disponibles: int
    carta_compromiso_entregada: bool
    formulario_inscripcion_entregado: bool
    copia_documento_url: Optional[str] = None
    curriculum_url: Optional[str] = None
    fecha_alta: date
    fecha_baja: Optional[date] = None
    activo: bool

    class Config:
        from_attributes = True

class VoluntarioConPersonaRead(BaseModel):
    id: int
    nombre: str
    correo: str
    numero_identificacion: str
    datos_voluntariado: Optional[VoluntarioRead] = Field(alias="datos_voluntario")
    
    class Config:
        from_attributes = True
        populate_by_name = True

class AsociadoCreate(BaseModel):
    id_persona: int = Field(..., description="ID de la persona a ascender")
    numero_registro_asociado: str = Field(..., min_length=1, max_length=50)
    metodo_pago: MetodoPagoEnum
    autoriza_whatsapp: bool = Field(default=False)
    estado_membresia: EstadoAsociadoEnum = Field(default=EstadoAsociadoEnum.ACTIVO)
    estado_pago: EstadoPagoEnum = Field(default=EstadoPagoEnum.AL_DIA)
    
    class Config:
        from_attributes = True