from typing import Optional
from sqlmodel import SQLModel, Field

# 1. El Catálogo de Niveles Educativos
class NivelEducativo(SQLModel, table=True):
    __tablename__ = "nivel_educativo"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, max_length=100)

# 2. El Catálogo de Motivos de Consulta
class MotivoConsulta(SQLModel, table=True):
    __tablename__ = "motivo_consulta"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, max_length=150)

# 3. El Catálogo de Derivaciones
class Derivacion(SQLModel, table=True):
    __tablename__ = "derivacion"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, max_length=100)

# 4. El Catálogo de Técnicas de Acogida
class TecnicaAcogida(SQLModel, table=True):
    __tablename__ = "tecnica_acogida"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, max_length=100)