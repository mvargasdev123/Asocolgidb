from sqlmodel import Session, select
from models.expediente import Expediente, EstadoExpedienteEnum

class RepositorioExpediente:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, expediente: Expediente) -> Expediente:
        self.session.add(expediente)
        self.session.commit()
        self.session.refresh(expediente)
        return expediente

    def obtener_activo_por_persona(self, id_persona: int) -> Expediente | None:
        # Busca si existe un expediente que le pertenezca a la persona Y que esté "En trámite"
        statement = select(Expediente).where(
            Expediente.id_persona == id_persona,
            Expediente.estado == EstadoExpedienteEnum.EN_TRAMITE
        )
        return self.session.exec(statement).first()
    
