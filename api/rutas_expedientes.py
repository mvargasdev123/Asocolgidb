from fastapi import APIRouter, Depends
from sqlmodel import Session

# Ajusta estos imports a cómo se llamen tus archivos y carpetas reales
from database import get_session # Tu función que genera la sesión de la base de datos
from api.dependencias import obtener_usuario_actual
from schemas.expediente_schema import ExpedienteCreate
from repositories.repositorio_expediente import RepositorioExpediente
from repositories.repositorio_persona import RepositorioPersona
from services.servicio_expediente import ServicioExpediente

router = APIRouter(prefix="/expedientes", tags=["Expedientes Legales"], dependencies=[Depends(obtener_usuario_actual)])

@router.post("/", status_code=201)
def crear_expediente(expediente_in: ExpedienteCreate, db: Session = Depends(get_session)):
    # 1. Despertamos a los esclavos (Repositorios)
    repo_exp = RepositorioExpediente(db)
    # Nota de la IA: Si aún no tienes RepositorioPersona, tendrás que crear uno simple 
    # que tenga una función "obtener_por_id" para que el servicio pueda validar el rol.
    repo_per = RepositorioPersona(db) 
    
    # 2. Invocamos al cerebro dictatorial (Servicio)
    servicio = ServicioExpediente(repo_exp, repo_per)
    
    # 3. Ejecutamos la orden. Si el usuario rompe una regla, 
    # el servicio lanzará el Error 400 antes de llegar al return.
    nuevo_expediente = servicio.crear_nuevo_expediente(expediente_in)
    
    return {
        "mensaje": "Expediente creado con éxito", 
        "id_expediente": nuevo_expediente.id,
        "numero_registro": nuevo_expediente.numero_registro
    }