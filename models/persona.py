from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class Persona(SQLModel, table=True):
    # El ID es opcional al crear el objeto en Python, pero la BD lo llenará al guardar (autoincremental)
    id: Optional[int] = Field(default=None, primary_key=True)
    
    nombre: str = Field(max_length=150)
    correo: str = Field(unique=True, index=True) # Indexado porque seguro buscaremos mucho por correo
    fecha_nacimiento: date
    direccion: Optional[str] = Field(default=None)
    
    # Asumimos que si no dicen nada, no nos han dado los derechos de sus datos. 
    # Siempre asume lo peor del usuario.
    proteccion_datos: bool = Field(default=False) 
    
    imagen: bool = Field(default=None) # Aquí guardaremos la URL o ruta de la imagen, no la imagen en sí
    fecha_ingreso: date
    
    # --- Llaves Foráneas (El techo sin paredes) ---
    # Apuntan a tablas que aún no hemos creado, pero SQLModel nos deja prepararlas.
    id_tipo_documento: Optional[int] = Field(default=None, foreign_key="tipodocumento.id")
    id_nacionalidad: Optional[int] = Field(default=None, foreign_key="nacionalidad.id")