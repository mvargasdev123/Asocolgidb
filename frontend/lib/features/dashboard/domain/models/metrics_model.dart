class PersonaMetricSummary {
  final int id;
  final String nombreCompleto;
  final String numeroIdentificacion;
  final String? correoElectronico;
  final String? estadoPago;
  final String? situacionAdmin;

  PersonaMetricSummary({
    required this.id,
    required this.nombreCompleto,
    required this.numeroIdentificacion,
    this.correoElectronico,
    this.estadoPago,
    this.situacionAdmin,
  });

  factory PersonaMetricSummary.fromJson(Map<String, dynamic> json) {
    return PersonaMetricSummary(
      id: json['id'] as int,
      nombreCompleto: json['nombre_completo'] as String? ?? '',
      numeroIdentificacion: json['numero_identificacion'] as String? ?? '',
      correoElectronico: json['correo_electronico'] as String?,
      estadoPago: json['estado_pago'] as String?,
      situacionAdmin: json['situacion_admin'] as String?,
    );
  }
}

class MetricsSummaryModel {
  final int totalPersonas;
  final int totalExpedientes;
  final int expedientesActivos;
  final int asociadosActivos;
  final int asociadosMorososCount;
  final int asociadosPendientesCount;
  final int totalVoluntarios;

  final Map<String, int> distribucionRoles;
  final Map<String, int> situacionAdministrativa;
  final Map<String, int> demografiaGenero;
  final Map<String, int> nacionalidadesTop5;
  final Map<String, int> ciudadesTop5;
  final Map<String, int> motivosConsultaTop5;

  MetricsSummaryModel({
    required this.totalPersonas,
    required this.totalExpedientes,
    required this.expedientesActivos,
    required this.asociadosActivos,
    required this.asociadosMorososCount,
    required this.asociadosPendientesCount,
    required this.totalVoluntarios,
    required this.distribucionRoles,
    required this.situacionAdministrativa,
    required this.demografiaGenero,
    required this.nacionalidadesTop5,
    required this.ciudadesTop5,
    required this.motivosConsultaTop5,
  });

  factory MetricsSummaryModel.fromJson(Map<String, dynamic> json) {
    Map<String, int> parseMap(dynamic mapData) {
      if (mapData == null || mapData is! Map) return {};
      return mapData.map((k, v) => MapEntry(k.toString(), (v as num).toInt()));
    }

    return MetricsSummaryModel(
      totalPersonas: json['total_personas'] as int? ?? 0,
      totalExpedientes: json['total_expedientes'] as int? ?? 0,
      expedientesActivos: json['expedientes_activos'] as int? ?? 0,
      asociadosActivos: json['asociados_activos'] as int? ?? 0,
      asociadosMorososCount: json['asociados_morosos_count'] as int? ?? 0,
      asociadosPendientesCount: json['asociados_pendientes_count'] as int? ?? 0,
      totalVoluntarios: json['total_voluntarios'] as int? ?? 0,
      distribucionRoles: parseMap(json['distribucion_roles']),
      situacionAdministrativa: parseMap(json['situacion_administrativa']),
      demografiaGenero: parseMap(json['demografia_genero']),
      nacionalidadesTop5: parseMap(json['nacionalidades_top5']),
      ciudadesTop5: parseMap(json['ciudades_top5']),
      motivosConsultaTop5: parseMap(json['motivos_consulta_top5']),
    );
  }
}

class AsociadosMorososPendientesModel {
  final List<PersonaMetricSummary> morosos;
  final List<PersonaMetricSummary> pendientes;

  AsociadosMorososPendientesModel({
    required this.morosos,
    required this.pendientes,
  });

  factory AsociadosMorososPendientesModel.fromJson(Map<String, dynamic> json) {
    return AsociadosMorososPendientesModel(
      morosos: (json['morosos'] as List<dynamic>?)
              ?.map((e) => PersonaMetricSummary.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      pendientes: (json['pendientes'] as List<dynamic>?)
              ?.map((e) => PersonaMetricSummary.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}
