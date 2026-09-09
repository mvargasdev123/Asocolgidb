from typing import Optional, List
from sqlmodel import Session, select
from domain.models.roles import DatosVoluntario

class VoluntarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, limit: int = 50, offset: int = 0) -> List[DatosVoluntario]:
        statement = select(DatosVoluntario).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, id_voluntario: int) -> Optional[DatosVoluntario]:
        statement = select(DatosVoluntario).where(DatosVoluntario.id == id_voluntario)
        return self.session.exec(statement).first()

    def get_by_persona_id(self, id_persona: int) -> Optional[DatosVoluntario]:
        statement = select(DatosVoluntario).where(DatosVoluntario.id_persona == id_persona)
        return self.session.exec(statement).first()

    def create(self, datos: DatosVoluntario) -> DatosVoluntario:
        self.session.add(datos)
        self.session.commit()
        self.session.refresh(datos)
        return datos

    def update(self, datos: DatosVoluntario) -> DatosVoluntario:
        self.session.add(datos)
        self.session.commit()
        self.session.refresh(datos)
        return datos

    def delete(self, datos: DatosVoluntario):
        self.session.delete(datos)
        self.session.commit()
