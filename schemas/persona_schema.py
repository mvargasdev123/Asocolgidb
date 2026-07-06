from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from models.persona import GeneroEnum, SituacionAdminEnum, OpcionNAEnum, PadronEnum
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
    # --- LOS CLÁSICOS (Los de tu imagen) ---
    nombre: str = Field(..., max_length=150)
    correo: Optional[EmailStr] = None
    fecha_nacimiento: date
    direccion: Optional[str] = None
    proteccion_datos: bool = Field(default=False)
    tipo_documento: str = Field(..., max_length=50)
    nacionalidad: str = Field(..., max_length=50)
    
    # --- LOS NUEVOS MONSTRUOS OBLIGATORIOS (Para que Postgres no llore) ---
    numero_identificacion: str = Field(..., max_length=50)
    genero: GeneroEnum
    situacion_administrativa: SituacionAdminEnum
    madre_soltera: OpcionNAEnum
    violencia_genero: OpcionNAEnum
    tiene_padron: PadronEnum
    autoriza_uso_imagen: bool = Field(default=False)

    # --- ALGUNOS OPCIONALES QUE AÑADIMOS ---
    codigo_postal: Optional[str] = None
    ciudad_residencia: Optional[str] = None
    
    # --- CAMPOS NUEVOS DEL EXCEL (POST INICIAL) ---
    fecha_atencion: Optional[date] = None
    telefono_principal: Optional[str] = None
    motivo_consulta: Optional[str] = None
    nivel_educativo: Optional[str] = None
    unidad_familiar: int = Field(default=1)
    contacto_emergencia_nombre: Optional[str] = Field(None, max_length=150)
    contacto_emergencia_parentesco: Optional[str] = Field(None, max_length=50)
    contacto_emergencia_telefono: Optional[str] = Field(None, max_length=50)
    fecha_padron: Optional[date] = None
    derivacion: Optional[str] = None
    tecnica_acogida: Optional[str] = None

    class Config:
        orm_mode = True

class PersonaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    correo: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    proteccion_datos: Optional[bool] = None
    tipo_documento: Optional[str] = Field(None, max_length=50)
    nacionalidad: Optional[str] = Field(None, max_length=50)
    
    numero_identificacion: Optional[str] = Field(None, max_length=50)
    genero: Optional[GeneroEnum] = None
    situacion_administrativa: Optional[SituacionAdminEnum] = None
    madre_soltera: Optional[OpcionNAEnum] = None
    violencia_genero: Optional[OpcionNAEnum] = None
    tiene_padron: Optional[PadronEnum] = None
    autoriza_uso_imagen: Optional[bool] = None
    
    codigo_postal: Optional[str] = Field(None, max_length=20)
    ciudad_residencia: Optional[str] = Field(None, max_length=100)
    unidad_familiar: Optional[int] = None
    fecha_padron: Optional[date] = None
    contacto_emergencia_nombre: Optional[str] = Field(None, max_length=150)
    contacto_emergencia_parentesco: Optional[str] = Field(None, max_length=50)
    contacto_emergencia_telefono: Optional[str] = Field(None, max_length=50)
    id_nivel_educativo: Optional[int] = None
    id_motivo_consulta: Optional[int] = None
    id_derivacion: Optional[int] = None
    id_tecnica_acogida: Optional[int] = None


# Esquema para DEVOLVER datos (Leer una Persona)
# Aquí sí incluimos el 'id' y la 'fecha_ingreso', porque ya existen en la base de datos.
class PersonaRead(BaseModel):
    id: int
    nombre: str
    correo: Optional[EmailStr] = None
    fecha_nacimiento: date
    direccion: Optional[str] = None
    proteccion_datos: bool
    tipo_documento: Optional[TipoDocumentoRead] = None
    nacionalidad: Optional[NacionalidadRead] = None
    
    # Los monstruos obligatorios
    numero_identificacion: str
    genero: GeneroEnum
    situacion_administrativa: SituacionAdminEnum
    madre_soltera: OpcionNAEnum
    violencia_genero: OpcionNAEnum
    tiene_padron: PadronEnum
    autoriza_uso_imagen: bool
    
    # Opcionales y foráneas
    codigo_postal: Optional[str] = None
    ciudad_residencia: Optional[str] = None
    unidad_familiar: Optional[int] = None
    fecha_padron: Optional[date] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_parentesco: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None
    id_nivel_educativo: Optional[int] = None
    id_motivo_consulta: Optional[int] = None
    id_derivacion: Optional[int] = None
    id_tecnica_acogida: Optional[int] = None
    
    class Config:
        from_attributes = True