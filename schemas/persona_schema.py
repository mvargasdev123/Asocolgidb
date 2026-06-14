from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from schemas.cita_schema import CitaRead
from schemas.comentario_schema import ComentarioRead, ComentarioCreate

# 1. Definimos cómo se ven los catálogos cuando salen de la API
class NacionalidadRead(BaseModel):
    id: int
    pais: str

class TipoDocumentoRead(BaseModel):
    id: int
    tipo: str

class EstadoRead(BaseModel):
    id: int
    nombre_estado: str

# Esquema para RECIBIR datos (Crear una Persona)
# Fíjate que aquí no pedimos el 'id' ni la 'fecha_ingreso', porque esos los genera el sistema.

class PersonaCreate(BaseModel):
    nombre: str
    correo: EmailStr # Magia pura: Pydantic validará automáticamente que tenga un '@' y un dominio válido
    fecha_nacimiento: date
    direccion: Optional[str] = None
    proteccion_datos: bool = False
    tipo_documento: str = Field(..., description="Ej: Cédula, Pasaporte, DNI")
    nacionalidad: str = Field(..., description="Ej: Colombiano, Argentino, Mexicano")

class PersonaUpdate(BaseModel):
    # Todo es opcional, así el frontend solo manda lo que quiere cambiar
    nombre: Optional[str] = Field(default=None, max_length=150)
    correo: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    proteccion_datos: Optional[bool] = None
    tipo_documento: str = Field(..., description="Ej: Cédula, Pasaporte, DNI")
    nacionalidad: str = Field(..., description="Ej: Colombiano, Argentino, Mexicano")


# Esquema para DEVOLVER datos (Leer una Persona)
# Aquí sí incluimos el 'id' y la 'fecha_ingreso', porque ya existen en la base de datos.
class PersonaRead(BaseModel):
    id: int
    nombre: str
    correo: str
    fecha_nacimiento: date
    fecha_ingreso: date
    proteccion_datos: bool
    activo: bool
    # Podemos omitir datos que no queramos que el frontend vea por defecto

# En lugar de mostrar el ID foráneo feo, anidamos los esquemas completos.
    # Así, el JSON de respuesta tendrá un sub-objeto con los datos reales.
    nacionalidad: Optional[NacionalidadRead] = None
    tipo_documento: Optional[TipoDocumentoRead] = None

    estados: List[EstadoRead] = []
    citas: list[CitaRead] = []
    comentarios: list[ComentarioRead] = []