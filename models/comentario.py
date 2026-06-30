import enum
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# --- LA BRILLANTE IDEA DEL SÚBDITO ---
class TipoComentarioEnum(str, enum.Enum):
    PERSONA = "Persona"
    VOLUNTARIO = "Voluntario"
    ASOCIADO = "Asociado"
    EXPEDIENTE = "Expediente"

class Comentario(SQLModel, table=True):
    __tablename__ = "comentario"

    id: Optional[int] = Field(default=None, primary_key=True)
    texto: str = Field(max_length=500)
    fecha: datetime = Field(default_factory=datetime.utcnow)
    
    # La categorización para el frontend
    tipo: TipoComentarioEnum = Field(default=TipoComentarioEnum.PERSONA)
    
    # --- LAS LLAVES FORÁNEAS ---
    id_persona: int = Field(foreign_key="persona.id")
    
    # El Upgrade: Si el comentario es de un expediente, lo anclamos al expediente exacto
    id_expediente: Optional[int] = Field(default=None, foreign_key="expediente.id")
    
    # --- RELACIONES BIDIRECCIONALES ---
    # (Recuerda mantener los strings para evitar el error circular)
    persona: Optional["Persona"] = Relationship(back_populates="comentarios")
    expediente: Optional["Expediente"] = Relationship(
        back_populates="comentarios_historial",
        sa_relationship_kwargs={
            "primaryjoin": "Comentario.id_expediente == Expediente.id"
        }
    )