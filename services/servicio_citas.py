from sqlmodel import Session
from fastapi import HTTPException
from repositories.repositorio_citas import RepositorioCitas
from repositories.repositorio_persona import RepositorioPersona
from models.cita_atencion import CitaAtencion
from schemas.cita_schema import CitaCreate

class ServicioCitas:
    def __init__(self, session: Session):
        self.session = session
        self.repo_citas = RepositorioCitas(session)
        self.repo_persona = RepositorioPersona(session)

    def agendar_cita(self, id_persona: int, datos: CitaCreate) -> CitaAtencion:
        # Verificamos que la persona exista y no sea un fantasma (Soft Delete)
        persona = self.repo_persona.obtener_por_id(id_persona)
        if not persona or not persona.activo:
            raise HTTPException(status_code=404, detail="Persona no encontrada o inactiva.")

        # Creamos el modelo de base de datos
        nueva_cita = CitaAtencion(
            id_persona=id_persona,
            fecha=datos.fecha,
            motivo=datos.motivo
        )

        try:
            self.repo_citas.registrar_cita(nueva_cita)
            self.session.commit()
            self.session.refresh(nueva_cita)
            return nueva_cita
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Fallo al guardar cita: {str(e)}")