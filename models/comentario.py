from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel, Relationship

class Comentario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_persona: Optional[int] = Field(default=None, foreign_key="persona.id")
    
    # Registramos cuándo se hizo el comentario
    fecha: date = Field(default_factory=date.today)
    
    # El texto del comentario puede ser largo
    texto: str = Field(max_length=500)

    # La conexión bidireccional
    persona: Optional["Persona"] = Relationship(back_populates="comentarios")