from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Telefono(SQLModel, table=True):
    __tablename__ = "telefono"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    numero: str = Field(max_length=50, description="El número de teléfono completo")
    tipo: Optional[str] = Field(default="Principal", max_length=50, description="Ej: Móvil, Fijo, Trabajo, WhatsApp")
    
    # La llave foránea que une este teléfono con su dueño en la tabla Persona
    id_persona: int = Field(foreign_key="persona.id")
    persona: Optional["Persona"] = Relationship(back_populates="telefonos")
    # Nota mental: En el próximo paso, cuando toquemos el modelo Persona, 
    # le pondremos la relación bidireccional para que FastAPI pueda leer esto automáticamente.