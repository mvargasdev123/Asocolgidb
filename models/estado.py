from typing import Optional
from sqlmodel import Field, SQLModel

class Estado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_estado: str = Field(max_length=50, unique=True, index=True) 
    # Aquí irán: "Asociado", "Voluntario", "Contratado"