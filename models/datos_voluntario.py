from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class DatosVoluntario(SQLModel, table=True):
    id_persona: Optional[int] = Field(default=None, foreign_key="persona.id", primary_key=True)
    
    area_voluntariado: str = Field(max_length=150)
    horas_disponibles: int
    fecha_inicio: date
    fecha_termino: Optional[date] = Field(default=None)