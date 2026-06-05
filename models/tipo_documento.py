from typing import Optional
from sqlmodel import Field, SQLModel

class TipoDocumento(SQLModel, table=True):
    # La convención en Python es PascalCase para las clases, aunque la tabla se cree en minúsculas.
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str = Field(max_length=50, unique=True, index=True) 
    # Le ponemos unique=True porque no queremos dos IDs distintos para "Cédula"