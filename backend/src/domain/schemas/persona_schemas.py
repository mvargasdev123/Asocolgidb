from typing import Optional
from datetime import date
from pydantic import BaseModel

class IdentificacionSchema(BaseModel):
    tipo_documento: Optional[str] = None
    numero_identificacion: str
    nacionalidad: Optional[str] = None

class DatosPersonalesSchema(BaseModel):
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    correo_electronico: Optional[str] = None
    direccion_residencia: Optional[str] = None
    codigo_postal: Optional[str] = None
    ciudad: Optional[str] = None

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

class ContactoEmergenciaSchema(BaseModel):
    nombre: Optional[str] = None
    parentesco: Optional[str] = None
    telefono: Optional[str] = None

class DatosAsociadoSchema(BaseModel):
    metodo_pago: Optional[str] = None
    estado_membresia: Optional[str] = None
    estado_pago: Optional[str] = None
    autoriza_whatsapp: Optional[bool] = None

class DatosVoluntarioSchema(BaseModel):
    cargo: Optional[str] = None
    campo_accion: Optional[str] = None
    tipo: Optional[str] = None
    horas_semana: Optional[int] = None
    url_doc: Optional[str] = None
    url_cv: Optional[str] = None
    carta_compromiso_firmada: Optional[bool] = None
    formulario_inscripcion: Optional[bool] = None

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

