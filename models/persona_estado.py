from typing import Optional
from sqlmodel import Field, SQLModel

class PersonaEstado(SQLModel, table=True):
    # En una tabla pivote, la combinación de ambas foráneas forma la llave primaria compuesta
    id_persona: Optional[int] = Field(default=None, foreign_key="persona.id", primary_key=True)
    id_estado: Optional[int] = Field(default=None, foreign_key="estado.id", primary_key=True)