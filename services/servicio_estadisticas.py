from sqlmodel import Session, select, func
from models.persona import Persona, GeneroEnum, SituacionAdminEnum
from models.estado import Estado
from models.persona_estado import PersonaEstado
from models.expediente import Expediente, EstadoExpedienteEnum
from models.comentario import Comentario
class ServicioEstadisticas:
    def __init__(self, session: Session):
        self.session = session

    def obtener_panel_principal(self) -> dict:
        # --- 1. MÉTRICAS POBLACIONALES ---
        total_personas = self.session.exec(select(func.count(Persona.id)).where(Persona.activo == True)).one()
        
        # Desglose por Situación Administrativa
        regulares = self.session.exec(select(func.count(Persona.id)).where(Persona.situacion_administrativa == SituacionAdminEnum.REGULAR, Persona.activo == True)).one()
        irregulares = self.session.exec(select(func.count(Persona.id)).where(Persona.situacion_administrativa == SituacionAdminEnum.IRREGULAR, Persona.activo == True)).one()
        en_tramite_admin = self.session.exec(select(func.count(Persona.id)).where(Persona.situacion_administrativa == SituacionAdminEnum.TRAMITE, Persona.activo == True)).one()

        # Desglose por Género
        hombres = self.session.exec(select(func.count(Persona.id)).where(Persona.genero == GeneroEnum.H, Persona.activo == True)).one()
        mujeres = self.session.exec(select(func.count(Persona.id)).where(Persona.genero == GeneroEnum.M, Persona.activo == True)).one()
        lgtbi = self.session.exec(select(func.count(Persona.id)).where(Persona.genero == GeneroEnum.LGTBI, Persona.activo == True)).one()

        # --- 2. MÉTRICAS DE ROLES / ESTADOS ---
        # Contamos cuántas relaciones hay por cada tipo de estado principal
        asociados = self.session.exec(select(func.count(PersonaEstado.id_persona)).join(Estado).where(Estado.nombre_estado == "Asociado")).one()
        voluntarios = self.session.exec(select(func.count(PersonaEstado.id_persona)).join(Estado).where(Estado.nombre_estado == "Voluntario")).one()
        externos = self.session.exec(select(func.count(PersonaEstado.id_persona)).join(Estado).where(Estado.nombre_estado == "Externo")).one()

        # --- 3. MÉTRICAS LEGALES (EXPEDIENTES) ---
        total_expedientes = self.session.exec(select(func.count(Expediente.id))).one()
        exp_en_tramite = self.session.exec(select(func.count(Expediente.id)).where(Expediente.estado == EstadoExpedienteEnum.EN_TRAMITE)).one()
        exp_resueltos = self.session.exec(select(func.count(Expediente.id)).where(Expediente.estado == EstadoExpedienteEnum.RESUELTO)).one()
        exp_denegados = self.session.exec(select(func.count(Expediente.id)).where(Expediente.estado == EstadoExpedienteEnum.DENEGADO)).one()
        
        # --- 4. MÉTRICAS OPERATIVAS ---
        total_comentarios = self.session.exec(select(func.count(Comentario.id))).one()

        # Consolidamos todo en un JSON hermoso para el frontend
        return {
            "poblacion": {
                "total_activos": total_personas,
                "situacion_administrativa": {
                    "regular": regulares,
                    "irregular": irregulares,
                    "en_tramite": en_tramite_admin
                },
                "genero": {
                    "hombres": hombres,
                    "mujeres": mujeres,
                    "lgtbi": lgtbi
                }
            },
            "roles": {
                "asociados": asociados,
                "voluntarios": voluntarios,
                "externos": externos
            },
            "expedientes": {
                "total": total_expedientes,
                "en_tramite": exp_en_tramite,
                "resueltos": exp_resueltos,
                "denegados": exp_denegados
            },
            "operatividad": {
                "total_comentarios": total_comentarios
            }
        }