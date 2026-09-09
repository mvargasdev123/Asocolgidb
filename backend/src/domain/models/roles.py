from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel, Relationship

class DatosAsociado(SQLModel, table=True):
    __tablename__ = "datos_asociado"
    id: Optional[int] = Field(default=None, primary_key=True)
    id_persona: int = Field(foreign_key="persona.id", unique=True)
    
    metodo_pago: Optional[str] = Field(default=None)
    estado_membresia: Optional[str] = Field(default=None)
    estado_pago: Optional[str] = Field(default=None)
    autoriza_whatsapp: Optional[bool] = Field(default=False)
    fecha_vinculacion: Optional[date] = Field(default=None)
    
    persona: Optional["Persona"] = Relationship(back_populates="datos_asociado")

class DatosVoluntario(SQLModel, table=True):
    __tablename__ = "datos_voluntario"
    id: Optional[int] = Field(default=None, primary_key=True)
    id_persona: int = Field(foreign_key="persona.id", unique=True)
    
    cargo: Optional[str] = Field(default=None)
    campo_accion: Optional[str] = Field(default=None)
    tipo: Optional[str] = Field(default=None)
    horas_semana: Optional[int] = Field(default=None)
    url_doc: Optional[str] = Field(default=None)
    url_cv: Optional[str] = Field(default=None)
    fecha_vinculacion: Optional[date] = Field(default=None)
    fecha_alta: Optional[date] = Field(default=None)
    fecha_baja: Optional[date] = Field(default=None)
    carta_compromiso_firmada: Optional[bool] = Field(default=False)
    formulario_inscripcion: Optional[bool] = Field(default=False)
    
    persona: Optional["Persona"] = Relationship(back_populates="datos_voluntario")
