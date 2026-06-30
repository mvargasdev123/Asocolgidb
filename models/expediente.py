import enum
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

# --- EL ENUM DE ESTADOS DEL TRÁMITE ---
# Esto evitará que alguien escriba "en tramit" o "terminao"
class EstadoExpedienteEnum(str, enum.Enum):
    EN_TRAMITE = "En trámite"
    RESUELTO = "Resuelto"
    DENEGADO = "Denegado"
    ARCHIVADO = "Archivado"

# --- EL MODELO EXPEDIENTE ---
class Expediente(SQLModel, table=True):
    __tablename__ = "expediente"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Identificadores
    numero_registro: str = Field(unique=True, index=True, description="No. REGISTRO EXPEDIENTE")
    numero_expediente_asignado: Optional[str] = Field(default=None)
    
    # Datos del Trámite
    tipo_tramite: str = Field(max_length=150)
    fecha_presentacion: date
    estado: EstadoExpedienteEnum = Field(default=EstadoExpedienteEnum.EN_TRAMITE)
    
    # Datos Legales y Extra
    representante_legal: Optional[str] = Field(default=None, max_length=150)
    consultorio_juridico: Optional[str] = Field(default=None, max_length=150)
    aporte_social: Optional[str] = Field(default=None, max_length=100)
    
    # Booleanos de control
    solicitante_extranjeria: bool = Field(default=False)
    antecedentes_traducidos: bool = Field(default=False)
    
    # Finalización
    fecha_resolucion: Optional[date] = Field(default=None)
    
    # --- LA LLAVE FORÁNEA (El ancla a la Persona) ---
    id_persona: int = Field(foreign_key="persona.id")
    
    # --- LA RELACIÓN BIDIRECCIONAL ---
    persona: Optional["Persona"] = Relationship(back_populates="expedientes")
    comentarios_historial: list["Comentario"] = Relationship(
        back_populates="expediente",
        sa_relationship_kwargs={
            "primaryjoin": "Expediente.id == Comentario.id_expediente"
        }
        )