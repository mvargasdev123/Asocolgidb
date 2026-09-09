class ExpedienteModel {
  final int id;
  final int idPersona;
  final String numeroRegistro;
  final String tipoTramite;
  final String fechaPresentacion;
  final String estado;
  final String? numeroExpedienteAsignado;
  final String? representanteLegal;
  final String? consultorioJuridico;
  final String aporteSocial;
  final bool solicitanteExtranjeria;
  final bool antecedentesTraducidosYApostillados;
  final String? fechaResolucion;
  final String creadoEn;
  final String? personaNombre;
  final String? personaIdentificacion;

  ExpedienteModel({
    required this.id,
    required this.idPersona,
    required this.numeroRegistro,
    required this.tipoTramite,
    required this.fechaPresentacion,
    required this.estado,
    this.numeroExpedienteAsignado,
    this.representanteLegal,
    this.consultorioJuridico,
    this.aporteSocial = 'Sí',
    this.solicitanteExtranjeria = false,
    this.antecedentesTraducidosYApostillados = false,
    this.fechaResolucion,
    required this.creadoEn,
    this.personaNombre,
    this.personaIdentificacion,
  });

  factory ExpedienteModel.fromJson(Map<String, dynamic> json) {
    final persona = json['persona'] as Map<String, dynamic>?;
    return ExpedienteModel(
      id: json['id'] as int,
      idPersona: json['id_persona'] as int,
      numeroRegistro: json['numero_registro'] as String? ?? '',
      tipoTramite: json['tipo_tramite'] as String? ?? '',
      fechaPresentacion: json['fecha_presentacion'] as String? ?? '',
      estado: json['estado'] as String? ?? 'En tramite',
      numeroExpedienteAsignado: json['numero_expediente_asignado'] as String?,
      representanteLegal: json['representante_legal'] as String?,
      consultorioJuridico: json['consultorio_juridico'] as String?,
      aporteSocial: json['aporte_social'] as String? ?? 'Sí',
      solicitanteExtranjeria: json['solicitante_extranjeria'] as bool? ?? false,
      antecedentesTraducidosYApostillados: json['antecedentes_traducidos_y_apostillados'] as bool? ?? false,
      fechaResolucion: json['fecha_resolucion'] as String?,
      creadoEn: json['creado_en'] as String? ?? '',
      personaNombre: persona?['nombre_completo'] as String?,
      personaIdentificacion: persona?['numero_identificacion'] as String?,
    );
  }
}
