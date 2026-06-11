from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class VoluntarioCreate(BaseModel):
    # Usamos Field de Pydantic para poner reglas estrictas.
    # El '...' significa que el campo es obligatorio.
    area_voluntariado: str = Field(..., min_length=3, max_length=150)
    
    # gt=0 significa "Greater Than 0" (Mayor a cero). 
    # Si alguien manda 0 o un número negativo, Pydantic le lanza un error 422 automático.
    horas_disponibles: int = Field(..., gt=0) 
    
    fecha_inicio: date

class AsociadoCreate(BaseModel):

    fecha_inicio: date
    tramites: str = Field(..., min_length=3, max_length=150)

class ContratadoCreate(BaseModel):
    funcion: str = Field(..., min_length=3, max_length=150)
    horas_contratadas: int = Field(..., gt=0)
    fecha_inicio: date
    fecha_termino: Optional[date] = None