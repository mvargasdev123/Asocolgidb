from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel, Relationship

# Usamos string references en Relationship ("DatosAsociado", "DatosVoluntario") 
# para evitar importaciones circulares en tiempo de ejecución.

class Persona(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numero_identificacion: str = Field(max_length=50, unique=True, index=True)
    nombre_completo: str = Field(max_length=150)
    fecha_nacimiento: Optional[date] = Field(default=None)
    fecha_atencion: Optional[date] = Field(default=None)
    telefono_principal: Optional[str] = Field(default=None, max_length=50)
    genero: Optional[str] = Field(default=None)
    correo_electronico: Optional[str] = Field(default=None)
    direccion_residencia: Optional[str] = Field(default=None)
    codigo_postal: Optional[str] = Field(default=None)
    
    situacion_admin: Optional[str] = Field(default=None)
    unidad_familiar: Optional[int] = Field(default=None)
    madre_soltera: Optional[str] = Field(default=None)
    violencia_genero: Optional[str] = Field(default=None)
    
    tiene_padron: Optional[bool] = Field(default=None)
    fecha_padron: Optional[date] = Field(default=None)
    autoriza_datos: Optional[bool] = Field(default=False)
    autoriza_imagen: Optional[bool] = Field(default=False)
    
    contacto_emergencia_nombre: Optional[str] = Field(default=None)
    contacto_emergencia_parentesco: Optional[str] = Field(default=None)
    contacto_emergencia_telefono: Optional[str] = Field(default=None)

    activo: bool = Field(default=True)
    contador_visitas: int = Field(default=1)

    id_tipo_documento: Optional[int] = Field(default=None, foreign_key="tipodocumento.id")
    id_nacionalidad: Optional[int] = Field(default=None, foreign_key="nacionalidad.id")
    id_ciudad: Optional[int] = Field(default=None, foreign_key="ciudad.id")
    id_nivel_educativo: Optional[int] = Field(default=None, foreign_key="niveleducativo.id")
    id_motivo_consulta: Optional[int] = Field(default=None, foreign_key="motivoconsulta.id")
    id_derivacion: Optional[int] = Field(default=None, foreign_key="derivacion.id")
    id_tecnica_acogida: Optional[int] = Field(default=None, foreign_key="tecnicaacogida.id")

    datos_asociado: Optional["DatosAsociado"] = Relationship(back_populates="persona")
    datos_voluntario: Optional["DatosVoluntario"] = Relationship(back_populates="persona")
    comentarios: list["Comentario"] = Relationship(back_populates="persona")
    expedientes: list["Expediente"] = Relationship(back_populates="persona")
