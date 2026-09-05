from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=150)
    hashed_password: str 
    es_admin: bool = Field(default=False)
    activo: bool = Field(default=True)

class IntentoLoginIP(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ip_address: str = Field(unique=True, index=True, max_length=50)
    intentos_fallidos: int = Field(default=0)
    bloqueado_hasta: Optional[datetime] = Field(default=None)
    ultimo_intento: datetime = Field(default_factory=datetime.utcnow)
