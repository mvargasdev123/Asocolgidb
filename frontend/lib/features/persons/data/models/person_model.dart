import '../../domain/entities/person.dart';

/// La capa de "Datos" es la encargada de hablar con el mundo exterior
/// (en este caso, la API del backend hecho en Python).

/// El PersonModel es un "traductor".
/// ¿Qué hace?: Extiende (copia) todo lo de PersonEntity, pero añade la capacidad
/// de convertirse desde y hacia el formato JSON (texto estructurado) que envía internet.
/// ¿Por qué lo hacemos separado de la Entidad pura?: Porque la Entidad no debe saber
/// que internet existe. El Modelo sí.
class PersonModel extends PersonEntity {
  
  /// El constructor simplemente le pasa los datos a la Entidad "padre".
  const PersonModel({
    required super.id,
    required super.fullName,
    required super.role,
    required super.biography,
    required super.email,
    super.birthDate,
    super.isActive = true,
    super.address,
    super.tipoDocumento,
    super.proteccionDatos = false,
    super.manejoImagen = false,
  });

  /// Transforma JSON a PersonModel.
  factory PersonModel.fromJson(Map<String, dynamic> json) {
    // Si viene anidado el tipo de documento, extraemos el nombre.
    String? tipoDocStr;
    if (json['tipo_documento'] != null && json['tipo_documento'] is Map) {
      tipoDocStr = json['tipo_documento']['tipo'];
    }

    return PersonModel(
      id: json['id'] as int, 
      fullName: json['nombre'] as String? ?? 'Sin nombre', 
      role: _extractRoleFromEstados(json['estados'] as List<dynamic>?), 
      email: json['correo'] as String? ?? 'sin@correo.com',
      birthDate: json['fecha_nacimiento'] != null 
          ? DateTime.tryParse(json['fecha_nacimiento'].toString()) 
          : null,
      isActive: json['activo'] as bool? ?? true,
      biography: "Fecha de ingreso: ${json['fecha_ingreso'] ?? 'Desconocida'}",
      address: json['direccion'] as String?,
      tipoDocumento: tipoDocStr,
      proteccionDatos: json['proteccion_datos'] as bool? ?? false,
      manejoImagen: json['imagen'] as bool? ?? false,
    );
  }

  /// Transforma PersonCreateEntity a JSON para enviarlo por POST a FastAPI.
  static Map<String, dynamic> createToJson(PersonCreateEntity entity) {
    // IMPORTANTE: Aquí solo enviamos los campos que la API de FastAPI
    // acepta explícitamente en el esquema PersonaCreate.
    // Omitimos intencionalmente 'numeroDocumento', 'manejoImagen', 'fechaIngreso'
    // y 'notes' porque la API devolvería un Error 422 (Unprocessable Entity).
    
    final map = <String, dynamic>{
      'nombre': entity.fullName,
      'correo': entity.email,
      'fecha_nacimiento': "${entity.birthDate.year.toString().padLeft(4, '0')}-${entity.birthDate.month.toString().padLeft(2, '0')}-${entity.birthDate.day.toString().padLeft(2, '0')}",
      'proteccion_datos': entity.proteccionDatos,
    };
    
    // Solo los añadimos si no son nulos
    if (entity.address != null && entity.address!.isNotEmpty) {
      map['direccion'] = entity.address;
    }
    if (entity.idTipoDocumento != null) {
      map['id_tipo_documento'] = entity.idTipoDocumento;
    }
    
    return map;
  }

  /// Función auxiliar para extraer el rol principal.
  static PersonRole _extractRoleFromEstados(List<dynamic>? estados) {
    if (estados == null || estados.isEmpty) return PersonRole.externo;
    
    // Verificamos si tiene roles superiores
    final strings = estados.map((e) => e['nombre_estado'].toString().toLowerCase()).toList();
    if (strings.contains('contratado')) return PersonRole.contratado;
    if (strings.contains('asociado')) return PersonRole.asociado;
    if (strings.contains('voluntario')) return PersonRole.voluntario;
    
    return PersonRole.externo;
  }
}
