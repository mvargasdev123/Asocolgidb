from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class Comentario(SQLModel, table=True):
    __tablename__ = "comentario"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_persona: int = Field(foreign_key="persona.id", index=True)
    
    texto: str = Field(max_length=1000)
    tipo: str = Field(default="Persona", max_length=50)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    persona: Optional["Persona"] = Relationship(back_populates="comentarios")
