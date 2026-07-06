from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Importa tu Enum de la tabla de comentarios
from models.comentario import TipoComentarioEnum

class ComentarioCreate(BaseModel):
    id_persona: int = Field(..., description="ID de la persona implicada en el chisme")
    
    # Ajusta 'contenido' por 'texto' si así lo bautizaste en tu modelo SQLModel
    contenido: str = Field(..., min_length=1, description="El texto del comentario")
    
    # AQUÍ ESTÁ LA MAGIA: Obligamos a mandar el tipo
    tipo: TipoComentarioEnum = Field(..., description="Clasificación: Persona, Voluntario, Asociado, Expediente")
    
    # Y si es de expediente, que manden el ID del expediente
    id_expediente: Optional[int] = Field(None, description="Obligatorio si el tipo es Expediente, sino se deja en null")

    class Config:
        from_attributes = True

class ComentarioRead(BaseModel):
    id: int
    id_persona: int
    contenido: str
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