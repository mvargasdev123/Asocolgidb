from typing import Optional, Any
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator

def parse_flexible_date(v: Any) -> Optional[date]:
    if v is None or v == "":
        return None
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    if isinstance(v, datetime):
        return v.date()
    val_str = str(v).strip()
    if not val_str or val_str.lower() in ["none", "null", "nan", "n/a"]:
        return None
    if " " in val_str:
        val_str = val_str.split(" ")[0]
    elif "T" in val_str:
        val_str = val_str.split("T")[0]

    for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y", "%m-%d-%y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(val_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Formato de fecha inválido: '{val_str}'. Use MM/DD/YYYY o YYYY-MM-DD.")

class ExpedienteCreateRequest(BaseModel):
    tipo_tramite: str = Field(..., description="Tipo de trámite legal", json_schema_extra={"example": "Renovación NIE"})
    fecha_presentacion: date = Field(..., description="Fecha de presentación", json_schema_extra={"example": "09/06/2026"})
    numero_expediente_asignado: Optional[str] = Field(None, description="Número de expediente asignado opcional", json_schema_extra={"example": "EXP-2026-001"})
    representante_legal: Optional[str] = Field(None, description="Representante legal", json_schema_extra={"example": "Dr. Carlos Ruiz"})
    consultorio_juridico: Optional[str] = Field(None, description="Consultorio jurídico", json_schema_extra={"example": "Consultorio Central"})
    aporte_social: Optional[str] = Field("Sí", description="Aporte social ('Sí' / 'No')", json_schema_extra={"example": "Sí"})
    solicitante_extranjeria: bool = Field(False, description="Solicitante de extranjería", json_schema_extra={"example": False})
    antecedentes_traducidos_y_apostillados: bool = Field(False, description="Antecedentes traducidos y apostillados", json_schema_extra={"example": False})
    fecha_resolucion: Optional[date] = Field(None, description="Fecha de resolución opcional", json_schema_extra={"example": None})

    @field_validator("fecha_presentacion", "fecha_resolucion", mode="before")
    def validate_dates(cls, v: Any) -> Optional[date]:
        return parse_flexible_date(v)

class ExpedienteUpdateRequest(BaseModel):
    tipo_tramite: Optional[str] = None
    estado: Optional[str] = None
    numero_expediente_asignado: Optional[str] = None
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[str] = None
    solicitante_extranjeria: Optional[bool] = None
    antecedentes_traducidos_y_apostillados: Optional[bool] = None
    fecha_resolucion: Optional[date] = None

    @field_validator("fecha_resolucion", mode="before")
    def validate_dates(cls, v: Any) -> Optional[date]:
        return parse_flexible_date(v)

class PersonaSummarySchema(BaseModel):
    id: int
    nombre_completo: str
    numero_identificacion: str

class ExpedienteResponse(BaseModel):
    id: int
    id_persona: int
    numero_registro: str
    tipo_tramite: str
    fecha_presentacion: str
    estado: str
    numero_expediente_asignado: Optional[str] = None
    representante_legal: Optional[str] = None
    consultorio_juridico: Optional[str] = None
    aporte_social: Optional[str] = "Sí"
    solicitante_extranjeria: bool = False
    antecedentes_traducidos_y_apostillados: bool = False
    fecha_resolucion: Optional[str] = None
    creado_en: datetime
    persona: Optional[PersonaSummarySchema] = None

    @field_validator("fecha_presentacion", "fecha_resolucion", mode="before")
    def format_dates_response(cls, v: Any) -> Optional[str]:
        if v is None: return None
        if isinstance(v, datetime): v = v.date()
        if isinstance(v, date): return v.strftime("%m/%d/%Y")
        return str(v)

    class Config:
        from_attributes = True

