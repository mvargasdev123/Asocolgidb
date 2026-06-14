from sqlmodel import Session, select, func
from models.persona import Persona
from models.cita_atencion import CitaAtencion
# Podríamos importar los roles también, pero mantengámoslo simple por ahora

class ServicioEstadisticas:
    def __init__(self, session: Session):
        self.session = session

    def obtener_panel_principal(self) -> dict:
        # 1. Contamos cuántas personas NO son fantasmas
        total_personas = self.session.exec(
            select(func.count(Persona.id)).where(Persona.activo == True)
        ).one()

        # 2. Contamos cuántas citas de atención se han dado en la historia
        total_citas = self.session.exec(
            select(func.count(CitaAtencion.id))
        ).one()

        # Devolvemos un simple diccionario súper ligero
        return {
            "total_personas_activas": total_personas,
            "total_citas_historicas": total_citas,
            "estado_servidor": "Saludable"
        }