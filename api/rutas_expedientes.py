from fastapi import APIRouter, Depends
from sqlmodel import Session

# Ajusta estos imports a cómo se llamen tus archivos y carpetas reales
from database import get_session
from api.dependencias import obtener_usuario_actual
from schemas.expediente_schema import ExpedienteCreate, ExpedienteUpdate, ExpedienteRead
from repositories.repositorio_expediente import RepositorioExpediente
from repositories.repositorio_persona import RepositorioPersona
from services.servicio_expediente import ServicioExpediente

router = APIRouter(tags=["Expedientes Legales"], dependencies=[Depends(obtener_usuario_actual)])

@router.post("/personas/{id_persona}/expedientes", response_model=ExpedienteRead, status_code=201)
def crear_expediente(id_persona: int, expediente_in: ExpedienteCreate, db: Session = Depends(get_session)):
    # 1. Despertamos a los esclavos (Repositorios)
    repo_exp = RepositorioExpediente(db)
    # Nota de la IA: Si aún no tienes RepositorioPersona, tendrás que crear uno simple 
    # que tenga una función "obtener_por_id" para que el servicio pueda validar el rol.
    repo_per = RepositorioPersona(db) 
    
    # 2. Invocamos al cerebro dictatorial (Servicio)
    servicio = ServicioExpediente(repo_exp, repo_per)
    return servicio.crear_nuevo_expediente(id_persona, expediente_in)

@router.get("/personas/{id_persona}/expedientes", response_model=list[ExpedienteRead])
def obtener_expedientes_persona(id_persona: int, db: Session = Depends(get_session)):
    repo_exp = RepositorioExpediente(db)
    repo_per = RepositorioPersona(db)
    servicio = ServicioExpediente(repo_exp, repo_per)
    return servicio.obtener_expedientes_persona(id_persona)

@router.get("/expedientes/{id_expediente}", response_model=ExpedienteRead)
def obtener_expediente(id_expediente: int, db: Session = Depends(get_session)):
    repo_exp = RepositorioExpediente(db)
    repo_per = RepositorioPersona(db)
    servicio = ServicioExpediente(repo_exp, repo_per)
    return servicio.obtener_expediente(id_expediente)

@router.patch("/expedientes/{id_expediente}", response_model=ExpedienteRead)
def actualizar_expediente(id_expediente: int, expediente_in: ExpedienteUpdate, db: Session = Depends(get_session)):
    repo_exp = RepositorioExpediente(db)
    repo_per = RepositorioPersona(db)
    servicio = ServicioExpediente(repo_exp, repo_per)
    return servicio.actualizar_expediente(id_expediente, expediente_in)

@router.delete("/expedientes/{id_expediente}")
def borrar_expediente(id_expediente: int, db: Session = Depends(get_session)):
    repo_exp = RepositorioExpediente(db)
    repo_per = RepositorioPersona(db)
    servicio = ServicioExpediente(repo_exp, repo_per)
    return servicio.borrar_expediente(id_expediente)