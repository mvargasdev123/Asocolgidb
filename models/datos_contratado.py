from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class DatosContratado(SQLModel, table=True):
    # El ID es foráneo y primario a la vez. Garantiza que una persona solo tenga UN registro aquí.
    id_persona: Optional[int] = Field(default=None, foreign_key="persona.id", primary_key=True)
    
    funcion: str = Field(max_length=150)
    horas_contratadas: int
    fecha_inicio: date
    fecha_termino: Optional[date] = Field(default=None) # Puede que siga contratado, no lo despidas por código