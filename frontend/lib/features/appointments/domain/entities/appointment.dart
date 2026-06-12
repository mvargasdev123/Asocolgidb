/// ---- ENTIDAD DE CITA (APPOINTMENT) ----
/// ¿Qué es?: Es la plantilla para una "Cita de Atención".
/// ¿Por qué está aquí?: Cumple con la regla de negocio que dice que 
/// una Persona puede tener múltiples citas (Relación 1 a Muchos / 1:N).
class AppointmentEntity {
  /// Identificador único de la cita en la base de datos.
  final int id;
  
  /// El ID de la persona a la que pertenece esta cita.
  /// ¡Esta es la clave para conectar "Muchas" citas con "1" sola persona!
  final int personId;
  
  /// La fecha y hora exacta en la que ocurrirá la cita.
  /// Usamos 'DateTime' que es una herramienta especial de Flutter para manejar tiempos.
  final DateTime scheduledAt;
  
  /// Notas sobre el motivo de la cita (ej. "Entrevista inicial").
  final String notes;

  /// El constructor que obliga a darle valor a todos estos datos.
  const AppointmentEntity({
    required this.id,
    required this.personId,
    required this.scheduledAt,
    required this.notes,
  });
}
