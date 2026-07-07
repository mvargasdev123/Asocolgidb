from sqlmodel import Session, select
from models.comentario import Comentario

class RepositorioComentario:
    def __init__(self, session: Session):
        self.session = session

    def obtener_por_id(self, id_comentario: int) -> Comentario | None:
        return self.session.get(Comentario, id_comentario)

    def obtener_por_persona(self, id_persona: int) -> list[Comentario]:
        return self.session.exec(
            select(Comentario)
            .where(Comentario.id_persona == id_persona)
            .order_by(Comentario.fecha.desc())
        ).all()

    def registrar_comentario(self, nuevo_comentario: Comentario):
        self.session.add(nuevo_comentario)
        
    def eliminar_comentario(self, comentario: Comentario):
        self.session.delete(comentario)