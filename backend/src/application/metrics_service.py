from domain.schemas.metrics_schemas import (
    MetricsSummaryResponse,
    AsociadosMorososPendientesResponse,
    PersonaMetricSummary
)
from infrastructure.metrics_repository import MetricsRepository

class MetricsService:
    def __init__(self, repository: MetricsRepository):
        self.repository = repository

    def obtener_metricas_dashboard(self) -> MetricsSummaryResponse:
        data = self.repository.get_kpis_and_distributions()
        return MetricsSummaryResponse(**data)

    def obtener_asociados_morosos_y_pendientes(self) -> AsociadosMorososPendientesResponse:
        morosos_entities, pendientes_entities = self.repository.get_asociados_morosos_y_pendientes()

        morosos_list = [
            PersonaMetricSummary(
                id=p.id,
                nombre_completo=p.nombre_completo,
                numero_identificacion=p.numero_identificacion,
                correo_electronico=p.correo_electronico,
                estado_pago=p.datos_asociado.estado_pago if p.datos_asociado else None,
                situacion_admin=p.situacion_admin
            )
            for p in morosos_entities
        ]

        pendientes_list = [
            PersonaMetricSummary(
                id=p.id,
                nombre_completo=p.nombre_completo,
                numero_identificacion=p.numero_identificacion,
                correo_electronico=p.correo_electronico,
                estado_pago=p.datos_asociado.estado_pago if p.datos_asociado else None,
                situacion_admin=p.situacion_admin
            )
            for p in pendientes_entities
        ]

        return AsociadosMorososPendientesResponse(
            morosos=morosos_list,
            pendientes=pendientes_list
        )
