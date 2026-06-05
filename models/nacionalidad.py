from typing import Optional
from sqlmodel import Field, SQLModel

class Nacionalidad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pais: str = Field(max_length=100, unique=True, index=True)
