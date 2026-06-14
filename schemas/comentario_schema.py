from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ComentarioCreate(BaseModel):
    texto: str = Field(..., min_length=3, max_length=500, description="Nota o comentario sobre la persona")

class ComentarioUpdate(BaseModel):
    texto: Optional[str] = Field(None, min_length=3, max_length=500)

class ComentarioRead(BaseModel):
    id: int
    fecha: date
    texto: str