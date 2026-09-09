abstract class ExpedientesEvent {}

class LoadExpedientes extends ExpedientesEvent {
  final String? estado;
  LoadExpedientes({this.estado});
}

class CreateExpedienteEvent extends ExpedientesEvent {
  final int idPersona;
  final String tipoTramite;
  final String fechaPresentacion;

  CreateExpedienteEvent({
    required this.idPersona,
    required this.tipoTramite,
    required this.fechaPresentacion,
  });
}

class UpdateExpedienteStatusEvent extends ExpedientesEvent {
  final int idExpediente;
  final String nuevoEstado;

  UpdateExpedienteStatusEvent({
    required this.idExpediente,
    required this.nuevoEstado,
  });
}
