from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class DatosAsociado(SQLModel, table=True):
    id_persona: Optional[int] = Field(default=None, foreign_key="persona.id", primary_key=True)
    
    tramites: str # Podríamos usar un JSON o un string largo dependiendo de qué guardes aquí
    fecha_inicio: date