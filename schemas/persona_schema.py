from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# 1. Definimos cómo se ven los catálogos cuando salen de la API
class NacionalidadRead(BaseModel):
    id: int
    pais: str

class TipoDocumentoRead(BaseModel):
    id: int
    tipo: str

# Esquema para RECIBIR datos (Crear una Persona)
# Fíjate que aquí no pedimos el 'id' ni la 'fecha_ingreso', porque esos los genera el sistema.

class PersonaCreate(BaseModel):
    nombre: str
    correo: EmailStr # Magia pura: Pydantic validará automáticamente que tenga un '@' y un dominio válido
    fecha_nacimiento: date
    direccion: Optional[str] = None
    proteccion_datos: bool = False
    id_tipo_documento: Optional[int] = None
    id_nacionalidad: Optional[int] = None


# Esquema para DEVOLVER datos (Leer una Persona)
# Aquí sí incluimos el 'id' y la 'fecha_ingreso', porque ya existen en la base de datos.
class PersonaRead(BaseModel):
    id: int
    nombre: str
    correo: str
    fecha_nacimiento: date
    fecha_ingreso: date
    proteccion_datos: bool
    # Podemos omitir datos que no queramos que el frontend vea por defecto

# En lugar de mostrar el ID foráneo feo, anidamos los esquemas completos.
    # Así, el JSON de respuesta tendrá un sub-objeto con los datos reales.
    nacionalidad: Optional[NacionalidadRead] = None
    tipo_documento: Optional[TipoDocumentoRead] = None