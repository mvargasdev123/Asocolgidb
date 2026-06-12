/// El "Dominio" es la capa más pura de la aplicación. No sabe nada de Internet,
/// bases de datos o pantallas. Solo contiene las reglas de negocio y las "Entidades"
/// puras.

/// Enum (Enumeración) para los roles de la máquina de estados.
/// ¿Qué es?: Es como una lista de opciones fijas. Una persona solo puede tener uno
/// de estos roles, ¡no puede inventarse otro!
/// ¿Por qué lo usamos?: Para evitar errores de escritura (ej. escribir "VoIuntario" mal)
/// y para saber exactamente qué niveles de acceso existen en la ONG.
enum PersonRole {
  externo,    // Nivel más bajo: Alguien externo a la ONG.
  voluntario, // Alguien que ayuda.
  asociado,   // Miembro formal de la ONG.
  contratado  // Nivel más alto: Empleado de la ONG.
}

/// Esta es la Entidad "Person" (Persona).
/// ¿Qué hace?: Es una plantilla o "molde" que define qué datos conforman a una
/// persona dentro de nuestro sistema.
/// ¿Para qué sirve?: En lugar de tener los datos sueltos (un texto para el nombre,
/// un número para la edad), agrupamos todo en un "paquete" llamado PersonEntity.
class PersonEntity {
  /// Identificador único de la persona en la base de datos (como su número de cédula interno).
  final int id;
  
  /// El nombre completo de la persona.
  final String fullName;
  
  /// El rol actual en la máquina de estados de la ONG.
  final PersonRole role;
  
  /// Una breve descripción biográfica o datos adicionales.
  final String biography;
  
  /// El correo electrónico de contacto.
  final String email;
  
  /// La fecha de nacimiento de la persona.
  final DateTime? birthDate;
  
  /// Indica si la persona está activa en el sistema.
  final bool isActive;
  
  // Nuevos campos
  final String? address;
  final String? tipoDocumento;
  final bool proteccionDatos;
  final bool manejoImagen;

  /// El constructor de la clase.
  const PersonEntity({
    required this.id,
    required this.fullName,
    required this.role,
    required this.biography,
    required this.email,
    this.birthDate,
    this.isActive = true,
    this.address,
    this.tipoDocumento,
    this.proteccionDatos = false,
    this.manejoImagen = false,
  });
}

/// ---- ENTIDAD PARA CREACIÓN ----
/// ¿Qué es?: Es un subconjunto de datos que enviamos al servidor cuando
/// queremos registrar a alguien nuevo. No incluye ID porque la base de datos lo genera.
class PersonCreateEntity {
  final String fullName;
  final String email;
  final DateTime birthDate;
  
  final String? address;
  final int? idTipoDocumento;
  final String? numeroDocumento;
  
  final bool proteccionDatos;
  final bool manejoImagen;
  
  final DateTime? fechaIngreso;
  
  final PersonRole role;
  final String? notes;

  const PersonCreateEntity({
    required this.fullName,
    required this.email,
    required this.birthDate,
    this.address,
    this.idTipoDocumento,
    this.numeroDocumento,
    this.proteccionDatos = false,
    this.manejoImagen = false,
    this.fechaIngreso,
    this.role = PersonRole.externo,
    this.notes,
  });
}
