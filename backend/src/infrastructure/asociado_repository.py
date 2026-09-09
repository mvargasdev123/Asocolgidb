from typing import Optional, List
from sqlmodel import Session, select
from domain.models.roles import DatosAsociado

class AsociadoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, limit: int = 50, offset: int = 0) -> List[DatosAsociado]:
        statement = select(DatosAsociado).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, id_asociado: int) -> Optional[DatosAsociado]:
        statement = select(DatosAsociado).where(DatosAsociado.id == id_asociado)
        return self.session.exec(statement).first()

    def get_by_persona_id(self, id_persona: int) -> Optional[DatosAsociado]:
        statement = select(DatosAsociado).where(DatosAsociado.id_persona == id_persona)
        return self.session.exec(statement).first()

    def create(self, datos: DatosAsociado) -> DatosAsociado:
        self.session.add(datos)
        self.session.commit()
        self.session.refresh(datos)
        return datos

    def update(self, datos: DatosAsociado) -> DatosAsociado:
        self.session.add(datos)
        self.session.commit()
        self.session.refresh(datos)
        return datos

    def delete(self, datos: DatosAsociado):
        self.session.delete(datos)
        self.session.commit()
