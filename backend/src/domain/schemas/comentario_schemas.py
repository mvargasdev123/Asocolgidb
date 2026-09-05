from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ComentarioCreateRequest(BaseModel):
    texto: str = Field(..., min_length=1, max_length=1000)
    tipo: Optional[str] = "Persona"
    fecha_creacion: Optional[datetime] = None

class ComentarioUpdateRequest(BaseModel):
    texto: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    tipo: Optional[str] = None
    fecha_creacion: Optional[datetime] = None

class ComentarioResponse(BaseModel):
    id: int
    id_persona: int
    texto: str
    tipo: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True
