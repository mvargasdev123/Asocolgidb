from typing import Optional
from sqlmodel import Session, select
from domain.models.usuario import Usuario, IntentoLoginIP

class AuthRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_usuario_por_email(self, email: str) -> Optional[Usuario]:
        return self.session.exec(select(Usuario).where(Usuario.email == email)).first()

    def get_intento_ip(self, ip_address: str) -> Optional[IntentoLoginIP]:
        return self.session.exec(select(IntentoLoginIP).where(IntentoLoginIP.ip_address == ip_address)).first()

    def guardar_intento_ip(self, intento: IntentoLoginIP):
        self.session.add(intento)
        self.session.commit()
        self.session.refresh(intento)
        return intento
