class ComentarioModel {
  final int id;
  final int idPersona;
  final String texto;
  final String tipo;
  final DateTime fechaCreacion;

  ComentarioModel({
    required this.id,
    required this.idPersona,
    required this.texto,
    required this.tipo,
    required this.fechaCreacion,
  });

  factory ComentarioModel.fromJson(Map<String, dynamic> json) {
    return ComentarioModel(
      id: json['id'] as int,
      idPersona: json['id_persona'] as int,
      texto: json['texto'] as String,
      tipo: json['tipo'] as String? ?? 'Persona',
      fechaCreacion: DateTime.parse(json['fecha_creacion'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'id_persona': idPersona,
      'texto': texto,
      'tipo': tipo,
      'fecha_creacion': fechaCreacion.toIso8601String(),
    };
  }

  ComentarioModel copyWith({
    int? id,
    int? idPersona,
    String? texto,
    String? tipo,
    DateTime? fechaCreacion,
  }) {
    return ComentarioModel(
      id: id ?? this.id,
      idPersona: idPersona ?? this.idPersona,
      texto: texto ?? this.texto,
      tipo: tipo ?? this.tipo,
      fechaCreacion: fechaCreacion ?? this.fechaCreacion,
    );
  }
}
