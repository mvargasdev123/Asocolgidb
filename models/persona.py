from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel, Relationship

from models.nacionalidad import Nacionalidad
from models.tipo_documento import TipoDocumento

class Persona(SQLModel, table=True):
    # El ID es opcional al crear el objeto en Python, pero la BD lo llenará al guardar (autoincremental)
    id: Optional[int] = Field(default=None, primary_key=True)
    id_tipo_documento: Optional[int] = Field(default=None, foreign_key="tipodocumento.id")
    id_nacionalidad: Optional[int] = Field(default=None, foreign_key="nacionalidad.id")
    
    nombre: str = Field(max_length=150)
    correo: str = Field(unique=True, index=True) # Indexado porque seguro buscaremos mucho por correo
    fecha_nacimiento: date
    direccion: Optional[str] = Field(default=None)
    
    # Asumimos que si no dicen nada, no nos han dado los derechos de sus datos. 
    # Siempre asume lo peor del usuario.
    proteccion_datos: bool = Field(default=False) 
    
    imagen: bool = Field(default=False) # Aquí guardaremos la URL o ruta de la imagen, no la imagen en sí
    fecha_ingreso: date
    
    # Usamos strings ("Nacionalidad") en vez de importar la clase directamente 
    # para evitar un error mortal de Python llamado "Importación Circular".
    nacionalidad: Optional["Nacionalidad"] = Relationship()
    tipo_documento: Optional["TipoDocumento"] = Relationship()