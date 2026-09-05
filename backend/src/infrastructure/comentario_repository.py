from typing import Optional, List
from sqlmodel import Session, select
from domain.models.comentario import Comentario

class ComentarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, comentario: Comentario) -> Comentario:
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario

    def get_by_persona_id(self, id_persona: int) -> List[Comentario]:
        statement = (
            select(Comentario)
            .where(Comentario.id_persona == id_persona)
            .order_by(Comentario.fecha_creacion.desc())
        )
        return self.session.exec(statement).all()

    def get_by_id(self, id_comentario: int) -> Optional[Comentario]:
        statement = select(Comentario).where(Comentario.id == id_comentario)
        return self.session.exec(statement).first()

    def update(self, comentario: Comentario) -> Comentario:
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario

    def delete(self, comentario: Comentario):
        self.session.delete(comentario)
        self.session.commit()
