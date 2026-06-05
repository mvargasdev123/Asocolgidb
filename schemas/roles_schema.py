from pydantic import BaseModel, Field
from datetime import date

class VoluntarioCreate(BaseModel):
    # Usamos Field de Pydantic para poner reglas estrictas.
    # El '...' significa que el campo es obligatorio.
    area_voluntariado: str = Field(..., min_length=3, max_length=150)
    
    # gt=0 significa "Greater Than 0" (Mayor a cero). 
    # Si alguien manda 0 o un número negativo, Pydantic le lanza un error 422 automático.
    horas_disponibles: int = Field(..., gt=0) 
    
    fecha_inicio: date