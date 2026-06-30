import enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

# IMPORTACIÓN ESTRICTA: Evita que SQLModel rompa la relación N:M
from models.persona_estado import PersonaEstado

# --- LOS ENUMS ESTRICTOS ---
class GeneroEnum(str, enum.Enum):
    M = "M"  # Cambia a "Mujer" si prefieres mantener el formato largo anterior
    H = "H"  # Cambia a "Hombre" si prefieres mantener el formato largo anterior
    LGTBI = "LGTBI+"

class SituacionAdminEnum(str, enum.Enum):
    REGULAR = "Regular"
    IRREGULAR = "Irregular"
    TRAMITE = "En trámite"

class OpcionNAEnum(str, enum.Enum):
    SI = "Sí"
    NO = "No"
    NA = "No aplica"

class PadronEnum(str, enum.Enum):
    SI = "Sí"
    NO = "No"
    OTRO = "Otro"

# --- EL MODELO PERSONA DEFINITIVO ---
class Persona(SQLModel, table=True):
    __tablename__ = "persona"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # --- LOS CLÁSICOS INTOCABLES ---
    nombre: str = Field(max_length=150)
    correo: str = Field(unique=True, index=True) 
    fecha_nacimiento: date
    direccion: Optional[str] = Field(default=None)
    proteccion_datos: bool = Field(default=False) 
    fecha_ingreso: date
    activo: bool = Field(default=True) 
    
    # --- LA INYECCIÓN DEL EXCEL ---
    numero_identificacion: str = Field(max_length=50, unique=True, index=True)
    genero: GeneroEnum
    codigo_postal: Optional[str] = Field(default=None, max_length=20)
    ciudad_residencia: Optional[str] = Field(default=None, max_length=100)
    
    situacion_administrativa: SituacionAdminEnum
    unidad_familiar: Optional[int] = Field(default=1, description="Número de personas en la unidad")
    
    madre_soltera: OpcionNAEnum = Field(default=OpcionNAEnum.NA)
    violencia_genero: OpcionNAEnum = Field(default=OpcionNAEnum.NA)
    tiene_padron: PadronEnum = Field(default=PadronEnum.NO)
    fecha_padron: Optional[date] = Field(default=None)
    
    autoriza_uso_imagen: bool = Field(default=False) 
    
    # --- CONTACTO DE EMERGENCIA ---
    contacto_emergencia_nombre: Optional[str] = Field(default=None, max_length=150)
    contacto_emergencia_parentesco: Optional[str] = Field(default=None, max_length=50)
    contacto_emergencia_telefono: Optional[str] = Field(default=None, max_length=50)
    
    # --- LAS LLAVES FORÁNEAS ---
    id_tipo_documento: Optional[int] = Field(default=None, foreign_key="tipodocumento.id")
    id_nacionalidad: Optional[int] = Field(default=None, foreign_key="nacionalidad.id")
    
    # ⚠️ ADVERTENCIA: Comenta estas 4 líneas si aún no has creado los modelos de estos catálogos
    id_nivel_educativo: Optional[int] = Field(default=None, foreign_key="nivel_educativo.id")
    id_motivo_consulta: Optional[int] = Field(default=None, foreign_key="motivo_consulta.id")
    id_derivacion: Optional[int] = Field(default=None, foreign_key="derivacion.id")
    id_tecnica_acogida: Optional[int] = Field(default=None, foreign_key="tecnica_acogida.id")
    
    # --- LAS RELACIONES BIDIRECCIONALES (Uso de strings seguro contra bucles circulares) ---
    nacionalidad: Optional["Nacionalidad"] = Relationship()
    tipo_documento: Optional["TipoDocumento"] = Relationship()
    datos_asociado: Optional["DatosAsociado"] = Relationship(back_populates="persona")
    datos_voluntario: Optional["DatosVoluntario"] = Relationship(back_populates="persona")
    # CORREGIDO: link_model ahora usa la clase real importada arriba
    estados: list["Estado"] = Relationship(link_model=PersonaEstado)
    
    citas: list["CitaAtencion"] = Relationship(back_populates="persona")
    comentarios: list["Comentario"] = Relationship(back_populates="persona")
    telefonos: list["Telefono"] = Relationship(back_populates="persona")
    expedientes: list["Expediente"] = Relationship(back_populates="persona")
