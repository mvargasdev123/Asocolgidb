from typing import Dict, List, Optional
from pydantic import BaseModel

class PersonaMetricSummary(BaseModel):
    id: int
    nombre_completo: str
    numero_identificacion: str
    correo_electronico: Optional[str] = None
    estado_pago: Optional[str] = None
    situacion_admin: Optional[str] = None

class MetricsSummaryResponse(BaseModel):
    total_personas: int
    total_expedientes: int
    expedientes_activos: int
    asociados_activos: int
    asociados_morosos_count: int
    asociados_pendientes_count: int
    total_voluntarios: int

    distribucion_roles: Dict[str, int]
    situacion_administrativa: Dict[str, int]
    demografia_genero: Dict[str, int]
    nacionalidades_top5: Dict[str, int]
    ciudades_top5: Dict[str, int]
    motivos_consulta_top5: Dict[str, int]

class AsociadosMorososPendientesResponse(BaseModel):
    morosos: List[PersonaMetricSummary]
    pendientes: List[PersonaMetricSummary]
