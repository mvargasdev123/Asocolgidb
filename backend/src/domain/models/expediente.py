from typing import Optional
from datetime import date, datetime
from sqlmodel import Field, SQLModel, Relationship

class Expediente(SQLModel, table=True):
    __tablename__ = "expediente"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_persona: int = Field(foreign_key="persona.id", index=True)
    
    numero_registro: str = Field(max_length=50, unique=True, index=True)
    tipo_tramite: str = Field(max_length=150)
    fecha_presentacion: date
    estado: str = Field(default="En tramite", max_length=50)

    # Campos extendidos
    numero_expediente_asignado: Optional[str] = Field(default=None, max_length=100)
    representante_legal: Optional[str] = Field(default=None, max_length=150)
    consultorio_juridico: Optional[str] = Field(default=None, max_length=150)
    aporte_social: Optional[str] = Field(default="Sí", max_length=10)
    solicitante_extranjeria: bool = Field(default=False)
    antecedentes_traducidos_y_apostillados: bool = Field(default=False)
    fecha_resolucion: Optional[date] = Field(default=None)

    creado_en: datetime = Field(default_factory=datetime.utcnow)

    persona: Optional["Persona"] = Relationship(back_populates="expedientes")
