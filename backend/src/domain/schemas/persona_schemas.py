from typing import Optional, Any
from datetime import date, datetime
from pydantic import BaseModel, field_validator

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

class IdentificacionSchema(BaseModel):
    tipo_documento: Optional[str] = None
    numero_identificacion: Optional[str] = None
    nacionalidad: Optional[str] = None

class DatosPersonalesSchema(BaseModel):
    nombre_completo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    fecha_atencion: Optional[date] = None
    telefono_principal: Optional[str] = None
    genero: Optional[str] = None
    correo_electronico: Optional[str] = None
    direccion_residencia: Optional[str] = None
    codigo_postal: Optional[str] = None
    ciudad: Optional[str] = None

    @field_validator("fecha_nacimiento", "fecha_atencion", mode="before")
    def validate_dates(cls, v: Any) -> Optional[date]:
        return parse_flexible_date(v)

class SituacionSocialSchema(BaseModel):
    situacion_admin: Optional[str] = None
    unidad_familiar: Optional[int] = None
    madre_soltera: Optional[str] = None
    violencia_genero: Optional[str] = None
    nivel_educativo: Optional[str] = None

class LegalAcogidaSchema(BaseModel):
    tiene_padron: Optional[bool] = None
    fecha_padron: Optional[date] = None
    motivo_consulta: Optional[str] = None
    derivacion: Optional[str] = None
    tecnica_acogida: Optional[str] = None
    autoriza_datos: Optional[bool] = None
    autoriza_imagen: Optional[bool] = None

    @field_validator("fecha_padron", mode="before")
    def validate_dates(cls, v: Any) -> Optional[date]:
        return parse_flexible_date(v)

class ContactoEmergenciaSchema(BaseModel):
    nombre: Optional[str] = None
    parentesco: Optional[str] = None
    telefono: Optional[str] = None

class DatosAsociadoSchema(BaseModel):
    metodo_pago: Optional[str] = None
    estado_membresia: Optional[str] = None
    estado_pago: Optional[str] = None
    autoriza_whatsapp: Optional[bool] = None
    fecha_vinculacion: Optional[date] = None

    @field_validator("fecha_vinculacion", mode="before")
    def validate_dates(cls, v: Any) -> Optional[date]:
        return parse_flexible_date(v)

class DatosVoluntarioSchema(BaseModel):
    cargo: Optional[str] = None
    campo_accion: Optional[str] = None
    tipo: Optional[str] = None
    horas_semana: Optional[int] = None
    url_doc: Optional[str] = None
    url_cv: Optional[str] = None
    fecha_vinculacion: Optional[date] = None
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None
    carta_compromiso_firmada: Optional[bool] = None
    formulario_inscripcion: Optional[bool] = None

    @field_validator("fecha_vinculacion", "fecha_alta", "fecha_baja", mode="before")
    def validate_dates(cls, v: Any) -> Optional[date]:
        return parse_flexible_date(v)

class PersonaCreateRequest(BaseModel):
    identificacion: IdentificacionSchema
    datos_personales: DatosPersonalesSchema
    situacion_social: Optional[SituacionSocialSchema] = None
    legal_acogida: Optional[LegalAcogidaSchema] = None
    contacto_emergencia: Optional[ContactoEmergenciaSchema] = None
    
    es_asociado: bool = False
    datos_asociado: Optional[DatosAsociadoSchema] = None
    
    es_voluntario: bool = False
    datos_voluntario: Optional[DatosVoluntarioSchema] = None

class PersonaUpdateRequest(BaseModel):
    identificacion: Optional[IdentificacionSchema] = None
    datos_personales: Optional[DatosPersonalesSchema] = None
    situacion_social: Optional[SituacionSocialSchema] = None
    legal_acogida: Optional[LegalAcogidaSchema] = None
    contacto_emergencia: Optional[ContactoEmergenciaSchema] = None
    
    es_asociado: Optional[bool] = None
    datos_asociado: Optional[DatosAsociadoSchema] = None
    
    es_voluntario: Optional[bool] = None
    datos_voluntario: Optional[DatosVoluntarioSchema] = None

