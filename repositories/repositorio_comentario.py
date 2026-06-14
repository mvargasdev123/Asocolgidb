from sqlmodel import Session
from models.comentario import Comentario

class RepositorioComentario:
    def __init__(self, session: Session):
        self.session = session

    def obtener_por_id(self, id_comentario: int) -> Comentario | None:
        return self.session.get(Comentario, id_comentario)

    def registrar_comentario(self, nuevo_comentario: Comentario):
        self.session.add(nuevo_comentario)
        
    def eliminar_comentario(self, comentario: Comentario):
        self.session.delete(comentario)