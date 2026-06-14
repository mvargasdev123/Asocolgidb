from sqlmodel import Session
from fastapi import HTTPException
from models.comentario import Comentario
from schemas.comentario_schema import ComentarioCreate, ComentarioUpdate
from repositories.repositorio_comentario import RepositorioComentario
from repositories.repositorio_persona import RepositorioPersona

class ServicioComentario:
    def __init__(self, session: Session):
        self.session = session
        self.repo_comentario = RepositorioComentario(session)
        self.repo_persona = RepositorioPersona(session)

    def agregar_comentario(self, id_persona: int, datos: ComentarioCreate) -> Comentario:
        persona = self.repo_persona.obtener_por_id(id_persona)
        if not persona or not persona.activo:
            raise HTTPException(status_code=404, detail="Persona no encontrada o inactiva.")

        nuevo_comentario = Comentario(id_persona=id_persona, texto=datos.texto)
        
        try:
            self.repo_comentario.registrar_comentario(nuevo_comentario)
            self.session.commit()
            self.session.refresh(nuevo_comentario)
            return nuevo_comentario
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Fallo al guardar el comentario.")

    def borrar_comentario(self, id_comentario: int):
        comentario = self.repo_comentario.obtener_por_id(id_comentario)
        if not comentario:
            raise HTTPException(status_code=404, detail="Comentario no encontrado.")
            
        try:
            self.repo_comentario.eliminar_comentario(comentario)
            self.session.commit()
            return {"mensaje": "Comentario eliminado con éxito."}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Fallo al borrar el comentario.")