from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

# Importamos nuestras herramientas habituales
from database import get_session
from schemas.roles_schema import VoluntarioCreate, AsociadoCreate
from services.servicio_roles import ServicioRoles
# Borré el import de ServicioPersona, ya no lo necesitamos aquí.
from api.dependencias import obtener_usuario_actual

# Creamos el enrutador específico para las operaciones de roles
router = APIRouter( 
    prefix="/roles", 
    tags=["Gestión de Roles"],
    dependencies=[Depends(obtener_usuario_actual)]
)

# 1. URL limpia: solo el sustantivo. Pydantic ya valida el id_persona por dentro.
@router.post("/voluntarios", status_code=201)
def ascender_persona_a_voluntario(
    datos_entrada: VoluntarioCreate, 
    session: Session = Depends(get_session) 
):
    servicio = ServicioRoles(session)
    
    # Extraemos el id_persona que viene escondido en el JSON validado
    resultado = servicio.ascender_a_voluntario(datos_entrada.id_persona, datos_entrada)
    
    return resultado

# 2. URL limpia para asociados.
@router.post("/asociados", status_code=201)
def ascender_persona_a_asociado(
    datos_entrada: AsociadoCreate,
    session: Session = Depends(get_session)
):
    servicio = ServicioRoles(session)
    # Pasamos el id_persona extraído del esquema y luego el objeto completo
    return servicio.ascender_a_asociado(datos_entrada.id_persona, datos_entrada)

# 3. El Soft-Delete que arreglamos antes.
@router.delete("/{id_persona}/quitar/{nombre_rol}")
def quitar_rol_de_persona(
    id_persona: int = Path(..., description="ID de la persona"),
    nombre_rol: str = Path(..., description="Nombre del rol a quitar (ej. Voluntario, Asociado)"),
    session: Session = Depends(get_session)
):
    # ¡OJO AL CAMBIO AQUÍ! 
    # Antes llamabas a ServicioPersona.quitar_rol_a_persona, 
    # pero toda la lógica pro de "Soft Delete" la metimos en ServicioRoles.remover_rol
    servicio = ServicioRoles(session)
    return servicio.remover_rol(id_persona, nombre_rol)