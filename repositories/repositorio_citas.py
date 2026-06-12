from sqlmodel import Session
from models.cita_atencion import CitaAtencion

class RepositorioCitas:
    def __init__(self, session: Session):
        self.session = session

    def registrar_cita(self, nueva_cita: CitaAtencion):
        self.session.add(nueva_cita)
        # El commit lo hará el servicio