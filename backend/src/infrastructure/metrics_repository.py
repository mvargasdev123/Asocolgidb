from typing import Dict, List, Tuple
from sqlmodel import Session, select, func
from sqlalchemy.orm import joinedload
from domain.models.persona import Persona
from domain.models.roles import DatosAsociado, DatosVoluntario
from domain.models.expediente import Expediente
from domain.models.catalogos import Nacionalidad, Ciudad, MotivoConsulta

class MetricsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_kpis_and_distributions(self) -> dict:
        personas = self.session.exec(
            select(Persona)
            .options(joinedload(Persona.datos_asociado), joinedload(Persona.datos_voluntario))
            .where(Persona.activo == True)
        ).unique().all()

        total_personas = len(personas)

        # Expedientes
        total_expedientes = self.session.exec(select(func.count(Expediente.id))).one() or 0
        expedientes_activos = self.session.exec(
            select(func.count(Expediente.id)).where(Expediente.estado == "En tramite")
        ).one() or 0

        asociados_activos_count = 0
        asociados_morosos_count = 0
        asociados_pendientes_count = 0
        voluntarios_count = 0

        roles_dist = {"Asociados": 0, "Voluntarios": 0, "Externos": 0}
        situacion_dist = {"Regular": 0, "Irregular": 0, "En Trámite": 0}
        genero_dist = {"Hombres": 0, "Mujeres": 0, "LGTBI": 0}

        for p in personas:
            es_aso = p.datos_asociado is not None
            es_vol = p.datos_voluntario is not None

            if es_vol:
                voluntarios_count += 1
                roles_dist["Voluntarios"] += 1

            if es_aso:
                roles_dist["Asociados"] += 1
                estado_pago = (p.datos_asociado.estado_pago or "").lower()
                estado_membresia = (p.datos_asociado.estado_membresia or "").lower()

                if "moroso" in estado_pago or "moroso" in estado_membresia:
                    asociados_morosos_count += 1
                elif "pendiente" in estado_pago or "tramite" in estado_membresia or "irregular" in estado_membresia:
                    asociados_pendientes_count += 1
                else:
                    asociados_activos_count += 1
            
            if not es_aso and not es_vol:
                roles_dist["Externos"] += 1

            # Situacion Admin
            sit = (p.situacion_admin or "").strip().lower()
            if "regular" in sit:
                situacion_dist["Regular"] += 1
            elif "irregular" in sit:
                situacion_dist["Irregular"] += 1
            elif "tramite" in sit or "trámite" in sit:
                situacion_dist["En Trámite"] += 1
            elif sit:
                situacion_dist["Regular"] += 1

            # Genero
            gen = (p.genero or "").strip().lower()
            if "hombre" in gen or "masculino" in gen:
                genero_dist["Hombres"] += 1
            elif "mujer" in gen or "femenino" in gen:
                genero_dist["Mujeres"] += 1
            elif "lgtb" in gen or "trans" in gen or "queer" in gen or "non-binary" in gen or "no binario" in gen:
                genero_dist["LGTBI"] += 1
            elif gen:
                genero_dist["Hombres"] += 1

        # Top 5 Nacionalidades
        nac_query = (
            select(Nacionalidad.nombre, func.count(Persona.id))
            .join(Persona, Persona.id_nacionalidad == Nacionalidad.id)
            .where(Persona.activo == True)
            .group_by(Nacionalidad.nombre)
            .order_by(func.count(Persona.id).desc())
            .limit(5)
        )
        nacionalidades_top5 = dict(self.session.exec(nac_query).all())

        # Top 5 Ciudades
        ciudad_query = (
            select(Ciudad.nombre, func.count(Persona.id))
            .join(Persona, Persona.id_ciudad == Ciudad.id)
            .where(Persona.activo == True)
            .group_by(Ciudad.nombre)
            .order_by(func.count(Persona.id).desc())
            .limit(5)
        )
        ciudades_top5 = dict(self.session.exec(ciudad_query).all())

        # Top 5 Motivos Consulta
        motivo_query = (
            select(MotivoConsulta.nombre, func.count(Persona.id))
            .join(Persona, Persona.id_motivo_consulta == MotivoConsulta.id)
            .where(Persona.activo == True)
            .group_by(MotivoConsulta.nombre)
            .order_by(func.count(Persona.id).desc())
            .limit(5)
        )
        motivos_top5 = dict(self.session.exec(motivo_query).all())

        return {
            "total_personas": total_personas,
            "total_expedientes": total_expedientes,
            "expedientes_activos": expedientes_activos,
            "asociados_activos": asociados_activos_count,
            "asociados_morosos_count": asociados_morosos_count,
            "asociados_pendientes_count": asociados_pendientes_count,
            "total_voluntarios": voluntarios_count,
            "distribucion_roles": roles_dist,
            "situacion_administrativa": situacion_dist,
            "demografia_genero": genero_dist,
            "nacionalidades_top5": nacionalidades_top5,
            "ciudades_top5": ciudades_top5,
            "motivos_consulta_top5": motivos_top5,
        }

    def get_asociados_morosos_y_pendientes(self) -> Tuple[List[Persona], List[Persona]]:
        personas = self.session.exec(
            select(Persona)
            .options(joinedload(Persona.datos_asociado))
            .where(Persona.activo == True)
        ).unique().all()

        morosos: List[Persona] = []
        pendientes: List[Persona] = []

        for p in personas:
            if p.datos_asociado:
                estado_pago = (p.datos_asociado.estado_pago or "").lower()
                estado_membresia = (p.datos_asociado.estado_membresia or "").lower()

                if "moroso" in estado_pago or "moroso" in estado_membresia:
                    morosos.append(p)
                elif "pendiente" in estado_pago or "tramite" in estado_membresia or "irregular" in estado_membresia:
                    pendientes.append(p)

        return morosos, pendientes
