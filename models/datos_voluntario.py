from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class DatosVoluntario(SQLModel, table=True):
    __tablename__ = "datos_voluntario"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relación 1:1 estricta
    id_persona: int = Field(foreign_key="persona.id", unique=True)
    
    # Datos específicos del Excel (Hoja VOL)
    cargo: str = Field(max_length=150, description="Ej: Coordinador de Logística")
    area_voluntariado: str = Field(max_length=150, description="Ej: Eventos, Legal, Redes")
    horas_disponibles: int = Field(ge=1, description="Horas a la semana/mes")
    
    # Documentación
    carta_compromiso_entregada: bool = Field(default=False)
    formulario_inscripcion_entregado: bool = Field(default=False)
    curriculum_url: Optional[str] = Field(default=None, description="Link al Drive o S3 con el CV")
    
    # Control de estado (Soft Delete)
    fecha_alta: date = Field(default_factory=date.today)
    fecha_baja: Optional[date] = Field(default=None)
    activo: bool = Field(default=True)
    
    # --- RELACIÓN BIDIRECCIONAL 1:1 ---
    persona: Optional["Persona"] = Relationship(back_populates="datos_voluntario")