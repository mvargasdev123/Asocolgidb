import enum
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class MetodoPagoEnum(str, enum.Enum):
    EFECTIVO = "Efectivo"
    BANCO = "Banco"

class EstadoAsociadoEnum(str, enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    RENOVADO = "Renovado"

class EstadoPagoEnum(str, enum.Enum):
    AL_DIA = "Al día"
    PENDIENTE = "Pendiente"
    MOROSO = "Moroso"

class DatosAsociado(SQLModel, table=True):
    __tablename__ = "datos_asociado"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_persona: int = Field(foreign_key="persona.id", unique=True)
    
    # Datos del Excel (Hoja ASO) y tus mejoras
    numero_registro_asociado: str = Field(unique=True, index=True)
    metodo_pago: MetodoPagoEnum = Field(default=MetodoPagoEnum.EFECTIVO)
    autoriza_whatsapp: bool = Field(default=False)
    
    estado_membresia: EstadoAsociadoEnum = Field(default=EstadoAsociadoEnum.ACTIVO)
    estado_pago: EstadoPagoEnum = Field(default=EstadoPagoEnum.PENDIENTE)
    
    # La antigüedad se calculará mágicamente usando esta fecha
    fecha_alta: date = Field(default_factory=date.today)
    fecha_baja: Optional[date] = Field(default=None)
    comentarios: Optional[str] = Field(default=None, description="Resumen del trámite o seguimiento")
    
    # --- RELACIÓN BIDIRECCIONAL 1:1 ---
    persona: Optional["Persona"] = Relationship(back_populates="datos_asociado")