from typing import Optional
from sqlmodel import Field, SQLModel

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Usamos el correo como nombre de usuario (es único y no se olvida)
    email: str = Field(unique=True, index=True, max_length=150)
    
    # JAMÁS, bajo ninguna circunstancia, guardamos la contraseña real.
    # Aquí guardaremos el "Hash" (la versión encriptada e irreversible).
    hashed_password: str 
    
    # Para saber si este usuario tiene permisos divinos en la API
    es_admin: bool = Field(default=False)
    
    # Nuestro confiable botón de apagado (Soft Delete) por si despiden al administrador
    activo: bool = Field(default=True)