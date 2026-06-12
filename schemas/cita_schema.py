from pydantic import BaseModel, Field
from datetime import date

class CitaCreate(BaseModel):
    fecha: date
    # No queremos citas vacías, que nos expliquen al menos por qué vinieron
    motivo: str = Field(..., min_length=5, max_length=255) 

class CitaRead(BaseModel):
    id: int
    fecha: date
    motivo: str