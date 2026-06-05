from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class CitaAtencion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_persona: Optional[int] = Field(default=None, foreign_key="persona.id")
    
    fecha: date
    motivo: str = Field(max_length=255)