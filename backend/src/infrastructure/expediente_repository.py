from typing import Optional, List
from sqlmodel import Session, select, func
from domain.models.expediente import Expediente

class ExpedienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, expediente: Expediente) -> Expediente:
        self.session.add(expediente)
        self.session.commit()
        self.session.refresh(expediente)
        return expediente

    def get_all(self, estado: Optional[str] = None) -> List[Expediente]:
        statement = select(Expediente)
        if estado:
            statement = statement.where(Expediente.estado == estado)
        statement = statement.order_by(Expediente.creado_en.desc())
        return list(self.session.exec(statement).all())

    def get_by_persona_id(self, id_persona: int) -> List[Expediente]:
        statement = (
            select(Expediente)
            .where(Expediente.id_persona == id_persona)
            .order_by(Expediente.creado_en.desc())
        )
        return list(self.session.exec(statement).all())

    def get_active_by_persona_id(self, id_persona: int) -> Optional[Expediente]:
        # El único estado activo es "En tramite"
        statement = select(Expediente).where(
            Expediente.id_persona == id_persona,
            Expediente.estado == "En tramite"
        )
        return self.session.exec(statement).first()

    def get_by_id(self, id_expediente: int) -> Optional[Expediente]:
        statement = select(Expediente).where(Expediente.id == id_expediente)
        return self.session.exec(statement).first()

    def count_all(self) -> int:
        statement = select(func.count(Expediente.id))
        return self.session.exec(statement).one() or 0

    def count_activos(self) -> int:
        statement = select(func.count(Expediente.id)).where(Expediente.estado == "En tramite")
        return self.session.exec(statement).one() or 0

    def get_next_sequence_number(self, year: int) -> int:
        prefix = f"EXP-{year}-"
        statement = select(Expediente.numero_registro).where(Expediente.numero_registro.like(f"{prefix}%"))
        registros = self.session.exec(statement).all()
        max_seq = 0
        for reg in registros:
            try:
                seq_str = reg.split("-")[-1]
                seq = int(seq_str)
                if seq > max_seq:
                    max_seq = seq
            except (ValueError, IndexError):
                continue
        return max_seq + 1

    def update(self, expediente: Expediente) -> Expediente:
        self.session.add(expediente)
        self.session.commit()
        self.session.refresh(expediente)
        return expediente

    def delete(self, expediente: Expediente):
        self.session.delete(expediente)
        self.session.commit()
