from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Importa tu Enum de la tabla de comentarios
from models.comentario import TipoComentarioEnum

class ComentarioCreate(BaseModel):
    texto: str = Field(..., min_length=1, description="El texto del comentario")
    
    # Obligamos a mandar el tipo
    tipo: TipoComentarioEnum = Field(..., description="Clasificación: Persona, Voluntario, Asociado, Expediente")

    class Config:
        from_attributes = True

class ComentarioRead(BaseModel):
    id: int
    id_persona: int
    texto: str
    fecha: datetime
    tipo: TipoComentarioEnum
    id_expediente: Optional[int] = None
    
    class Config:
        from_attributes = True

class ComentarioUpdate(BaseModel):
    # Solo permitimos actualizar el texto del chisme, nada de cambiar fechas ni IDs
    texto: str = Field(..., min_length=1, description="El nuevo texto corregido del comentario")

    class Config:
        from_attributes = True